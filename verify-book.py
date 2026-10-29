#!/usr/bin/env python3
"""Verify the built Architecture of Shadows artifacts.

This checks structure, not prose. It answers four questions:

  1. Do the four artifacts exist, and are their sizes non-trivial?
  2. Is each EPUB a valid container with the expected spine and no malformed
     XML?
  3. Is each PDF a real PDF with the expected page count?
  4. Do the source tree counts match what the manifest records?

It also reports content findings that a structural gate cannot fix: the
title-page placeholders and the 17-volume label on a 16-volume tree. Those
are warnings by default and failures with --strict, because they are owner
decisions, not build regressions.

Usage:
    python verify-book.py
    python verify-book.py --strict

No third-party Python package is required.
"""
from __future__ import annotations

import argparse
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parent
OPF = "http://www.idpf.org/2007/opf"
DC = "http://purl.org/dc/elements/1.1/"
CONTAINER = "urn:oasis:names:tc:opendocument:xmlns:container"

EXPECTED = {
    "master": {
        "epub": BOOK_ROOT / "THE-ARCHITECTURE-OF-SHADOWS-MASTER.epub",
        "pdf": BOOK_ROOT / "THE-ARCHITECTURE-OF-SHADOWS-MASTER.pdf",
        "spine": 410,
        "pages": 462,
        "chapters": 403,
        "front_matter": 6,
        "volume_dir": "MASTER-EDITION",
    },
    "student": {
        "epub": BOOK_ROOT / "THE-ARCHITECTURE-OF-SHADOWS-STUDENT.epub",
        "pdf": BOOK_ROOT / "THE-ARCHITECTURE-OF-SHADOWS-STUDENT.pdf",
        "spine": 365,
        "pages": 397,
        "chapters": 364,
        "front_matter": 0,
        "volume_dir": "STUDENT-EDITION",
    },
}

failures: list[str] = []
warnings: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def warn(condition: bool, message: str) -> None:
    if not condition:
        warnings.append(message)


def verify_epub(label: str, path: Path, expected_spine: int) -> None:
    if not path.is_file():
        failures.append(f"{label}: missing {path.name}")
        return
    size = path.stat().st_size
    check(size > 100_000, f"{label}: EPUB is only {size} bytes")
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            check(names and names[0] == "mimetype", f"{label}: first ZIP entry is not mimetype")
            check(
                archive.read("mimetype") == b"application/epub+zip",
                f"{label}: wrong mimetype payload",
            )
            container = ET.fromstring(archive.read("META-INF/container.xml"))
            rootfile = container.find(f".//{{{CONTAINER}}}rootfile")
            check(rootfile is not None, f"{label}: container has no rootfile")
            if rootfile is None:
                return
            opf_path = rootfile.get("full-path")
            check(bool(opf_path), f"{label}: rootfile has no full-path")
            if not opf_path:
                return
            opf = ET.fromstring(archive.read(opf_path))
            title = opf.find(f".//{{{DC}}}title")
            language = opf.find(f".//{{{DC}}}language")
            check(title is not None and bool(title.text), f"{label}: no dc:title")
            check(language is not None and language.text == "en-GB", f"{label}: language is not en-GB")
            manifest = opf.find(f"{{{OPF}}}manifest")
            spine = opf.find(f"{{{OPF}}}spine")
            check(manifest is not None, f"{label}: no manifest")
            check(spine is not None, f"{label}: no spine")
            if manifest is None or spine is None:
                return
            items = manifest.findall(f"{{{OPF}}}item")
            itemrefs = spine.findall(f"{{{OPF}}}itemref")
            check(
                len(itemrefs) == expected_spine,
                f"{label}: spine has {len(itemrefs)} items, expected {expected_spine}",
            )
            xhtml = [name for name in names if name.endswith(".xhtml")]
            check(
                len(xhtml) == expected_spine,
                f"{label}: {len(xhtml)} XHTML files, expected {expected_spine}",
            )
            check(
                any(item.get("properties") == "nav" for item in items),
                f"{label}: no navigation document",
            )
            malformed = 0
            for name in names:
                if name.endswith((".xml", ".xhtml", ".opf", ".ncx")):
                    try:
                        ET.fromstring(archive.read(name))
                    except ET.ParseError:
                        malformed += 1
            check(malformed == 0, f"{label}: {malformed} malformed XML documents")
            print(
                f"  EPUB {path.name}: {size / 1024 / 1024:.2f} MB, "
                f"{len(itemrefs)} spine items, {len(xhtml)} XHTML, {malformed} malformed"
            )
    except (zipfile.BadZipFile, KeyError, ET.ParseError) as error:
        failures.append(f"{label}: unreadable EPUB ({error})")


def verify_pdf(label: str, path: Path, expected_pages: int) -> None:
    if not path.is_file():
        failures.append(f"{label}: missing {path.name}")
        return
    data = path.read_bytes()
    size = len(data)
    check(data.startswith(b"%PDF-"), f"{label}: not a PDF")
    check(size > 1_000_000, f"{label}: PDF is only {size} bytes")
    counts = [int(value) for value in re.findall(rb"/Count\s+(\d+)", data)]
    pages = max(counts) if counts else 0
    objects = len(re.findall(rb"/Type\s*/Page\b", data))
    check(pages == expected_pages, f"{label}: {pages} pages, expected {expected_pages}")
    check(
        objects == expected_pages,
        f"{label}: {objects} page objects, expected {expected_pages}",
    )
    print(f"  PDF  {path.name}: {size / 1024 / 1024:.2f} MB, {pages} pages")


def verify_sources(label: str, spec: dict[str, object]) -> None:
    root = BOOK_ROOT / str(spec["volume_dir"])
    check(root.is_dir(), f"{label}: missing source directory {root.name}")
    if not root.is_dir():
        return
    chapters = sorted(root.glob("VOLUME-*/PART-*/chapter-*.md"))
    check(
        len(chapters) == spec["chapters"],
        f"{label}: {len(chapters)} chapter files, expected {spec['chapters']}",
    )
    empty = [path for path in chapters if path.stat().st_size == 0]
    check(not empty, f"{label}: {len(empty)} empty chapter files")
    volumes = sorted(path for path in root.glob("VOLUME-*") if path.is_dir())
    print(f"  SRC  {root.name}: {len(volumes)} volumes, {len(chapters)} chapters, {len(empty)} empty")


def verify_content_findings() -> None:
    title = BOOK_ROOT / "MASTER-EDITION" / "00-FRONT-MATTER" / "title-page.md"
    copyright_page = BOOK_ROOT / "MASTER-EDITION" / "00-FRONT-MATTER" / "copyright.md"
    title_text = title.read_text(encoding="utf-8") if title.is_file() else ""
    copyright_text = copyright_page.read_text(encoding="utf-8") if copyright_page.is_file() else ""
    for marker in ("[Author Name]", "[Publisher Name]", "[ISBN Number]"):
        warn(marker not in title_text, f"content: title page still contains {marker}")
    volumes = len(list((BOOK_ROOT / "MASTER-EDITION").glob("VOLUME-*")))
    label = "17-Volume"
    warn(
        not (label in title_text or label in copyright_text) or volumes == 17,
        f"content: title/copyright say {label} but the master tree has {volumes} volumes",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="treat content findings as failures")
    args = parser.parse_args()

    print("Artifacts")
    for label, spec in EXPECTED.items():
        verify_epub(label, Path(spec["epub"]), int(spec["spine"]))
        verify_pdf(label, Path(spec["pdf"]), int(spec["pages"]))
    print("Sources")
    for label, spec in EXPECTED.items():
        verify_sources(label, spec)

    verify_content_findings()

    if warnings:
        print("\nContent findings (owner decisions, not build regressions):")
        for warning in warnings:
            print(f"  WARN {warning}")
    if failures:
        print("\nFailures:")
        for failure in failures:
            print(f"  FAIL {failure}")
        return 1
    if args.strict and warnings:
        print("\n--strict: content findings are failures")
        return 1
    print("\nPASS: four artifacts and both source trees match the manifest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
