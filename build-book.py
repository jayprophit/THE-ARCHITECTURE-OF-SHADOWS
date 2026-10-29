#!/usr/bin/env python3
"""Build The Architecture of Shadows.

The book is Markdown organised as front matter, volumes, parts and chapters.
This script builds the master and student editions as EPUB and PDF.

EPUB is built by Pandoc directly. PDF is built by Pandoc to a standalone HTML
file and then printed to PDF by a headless Chromium browser (Microsoft Edge by
default), because no LaTeX engine is installed on this host. The PDF is A4 with
the margins in print.css; it is not the XeLaTeX layout described in the
original BUILD-INSTRUCTIONS.md.

Usage:
    python build-book.py --edition all --format all
    python build-book.py --edition master --format epub
    python build-book.py --edition student --format pdf

Environment:
    PANDOC  path to the pandoc executable
    EDGE    path to the Edge/Chromium executable used for PDF printing

No third-party Python package is required.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parent
TITLE = "The Architecture of Shadows"
LANG = "en-GB"

EDITIONS = {
    "master": {
        "dir": "MASTER-EDITION",
        "front_matter": True,
        "slug": "MASTER",
    },
    "student": {
        "dir": "STUDENT-EDITION",
        "front_matter": False,
        "slug": "STUDENT",
    },
}

PRINT_CSS = """@page {
  size: A4;
  margin: 18mm 16mm 20mm 16mm;
}
html { font-size: 11pt; }
body {
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.45;
  color: #111;
  max-width: none;
  margin: 0;
}
h1, h2, h3, h4 { font-family: "Segoe UI", Arial, sans-serif; color: #111; }
h1 { font-size: 20pt; page-break-before: always; margin: 0 0 0.8em 0; }
h1:first-of-type { page-break-before: avoid; }
h2 { font-size: 14pt; margin: 1.2em 0 0.4em; }
h3 { font-size: 12pt; margin: 1em 0 0.3em; }
p { margin: 0 0 0.7em; text-align: justify; hyphens: auto; }
ul, ol { margin: 0 0 0.8em 1.4em; }
li { margin-bottom: 0.25em; }
blockquote { margin: 0 0 0.8em 1.2em; padding-left: 0.8em; border-left: 3px solid #bbb; color: #333; }
code, pre { font-family: Consolas, monospace; font-size: 9.5pt; }
pre { white-space: pre-wrap; page-break-inside: avoid; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 9.5pt; }
th, td { border: 1px solid #999; padding: 4px 6px; vertical-align: top; }
a { color: #111; text-decoration: none; }
nav#TOC { page-break-after: always; }
nav#TOC ul { list-style: none; margin-left: 0; }
nav#TOC > ul > li { margin-top: 0.5em; }
.title { font-size: 26pt; }
.subtitle { font-size: 14pt; }
hr { border: 0; border-top: 1px solid #bbb; margin: 1em 0; }
"""


def find_pandoc() -> str:
    candidates = [
        os.environ.get("PANDOC"),
        shutil.which("pandoc"),
        r"C:\Users\jpowe\AppData\Local\Temp\opencode\pandoc-3.13\pandoc-3.13\pandoc.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise SystemExit("pandoc not found; set PANDOC or install pandoc")


def find_browser() -> str:
    candidates = [
        os.environ.get("EDGE"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("msedge"),
        shutil.which("google-chrome"),
        shutil.which("chromium"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise SystemExit("no Chromium browser found; set EDGE or install Microsoft Edge")


def input_files(edition: str) -> list[str]:
    spec = EDITIONS[edition]
    root = BOOK_ROOT / spec["dir"]
    files: list[Path] = []
    if spec["front_matter"]:
        files.extend(sorted((root / "00-FRONT-MATTER").glob("*.md")))
    files.extend(sorted(root.glob("VOLUME-*/PART-*/chapter-*.md")))
    if not files:
        raise SystemExit(f"no input files for {edition}")
    return [p.relative_to(BOOK_ROOT).as_posix() for p in files]


def yaml_list(values: list[str], indent: int = 2) -> str:
    pad = " " * indent
    return "\n".join(f"{pad}- {json.dumps(value)}" for value in values)


def write_defaults(
    path: Path,
    *,
    target: str,
    files: list[str],
    css: Path | None = None,
) -> None:
    lines = [
        "from: markdown",
        f"to: {target}",
        "toc: true",
        "toc-depth: 3",
        "metadata:",
        f"  title: {json.dumps(TITLE)}",
        f"  lang: {json.dumps(LANG)}",
    ]
    if target == "html5":
        lines.append("  document-css: false")
        lines += [
            "standalone: true",
            "embed-resources: true",
            "css:",
            f"  - {json.dumps(css.as_posix() if css else '')}",
        ]
    if target == "epub3":
        lines.append("epub-title-page: false")
    lines += ["input-files:", yaml_list(files)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=BOOK_ROOT, check=True)


def build_epub(edition: str, pandoc: str, work: Path, output_dir: Path) -> Path:
    spec = EDITIONS[edition]
    files = input_files(edition)
    defaults = work / f"{edition}-epub.yaml"
    write_defaults(defaults, target="epub3", files=files)
    out = output_dir / f"THE-ARCHITECTURE-OF-SHADOWS-{spec['slug']}.epub"
    run([pandoc, f"--defaults={defaults}", "-o", str(out)])
    return out


def build_html(edition: str, pandoc: str, work: Path, css: Path, output: Path | None = None) -> Path:
    files = input_files(edition)
    defaults = work / f"{edition}-html.yaml"
    write_defaults(defaults, target="html5", files=files, css=css)
    out = output or work / f"{edition}.html"
    run([pandoc, f"--defaults={defaults}", "-o", str(out)])
    return out


def build_pdf(edition: str, pandoc: str, browser: str, work: Path, output_dir: Path) -> Path:
    spec = EDITIONS[edition]
    css = work / "print.css"
    css.write_text(PRINT_CSS, encoding="utf-8")
    html = build_html(edition, pandoc, work, css, work / f"{edition}.html")
    out = output_dir / f"THE-ARCHITECTURE-OF-SHADOWS-{spec['slug']}.pdf"
    profile = work / f"edge-profile-{edition}"
    run(
        [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=10000",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={out}",
            f"file:///{html.as_posix()}",
        ]
    )
    return out


def describe(path: Path) -> str:
    size = path.stat().st_size
    if path.suffix == ".pdf":
        data = path.read_bytes()
        import re

        counts = [int(value) for value in re.findall(rb"/Count\s+(\d+)", data)]
        pages = max(counts) if counts else None
        return f"{path.name}: {size / 1024 / 1024:.2f} MB, {pages} pages"
    if path.suffix == ".epub":
        import zipfile
        import xml.etree.ElementTree as ET

        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            container = ET.fromstring(archive.read("META-INF/container.xml"))
            opf_path = container.find(
                ".//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile"
            ).get("full-path")
            opf = ET.fromstring(archive.read(opf_path))
            spine = opf.find("{http://www.idpf.org/2007/opf}spine")
            items = spine.findall("{http://www.idpf.org/2007/opf}itemref")
        return f"{path.name}: {size / 1024 / 1024:.2f} MB, {len(items)} spine items"
    return f"{path.name}: {size} bytes"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edition", choices=["master", "student", "all"], default="all")
    parser.add_argument("--format", choices=["epub", "pdf", "html", "all"], default="all")
    parser.add_argument("--output-dir", default=str(BOOK_ROOT))
    args = parser.parse_args()

    editions = ["master", "student"] if args.edition == "all" else [args.edition]
    formats = ["epub", "pdf"] if args.format == "all" else [args.format]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pandoc = find_pandoc()
    browser = find_browser() if "pdf" in formats else None
    print(f"pandoc: {pandoc}")
    if browser:
        print(f"browser: {browser}")

    built: list[Path] = []
    with tempfile.TemporaryDirectory(prefix="aos-book-") as temporary:
        work = Path(temporary)
        for edition in editions:
            if "epub" in formats:
                built.append(build_epub(edition, pandoc, work, output_dir))
            if "html" in formats:
                css = work / "print.css"
                css.write_text(PRINT_CSS, encoding="utf-8")
                built.append(
                    build_html(
                        edition,
                        pandoc,
                        work,
                        css,
                        output_dir / f"THE-ARCHITECTURE-OF-SHADOWS-{EDITIONS[edition]['slug']}.html",
                    )
                )
            if "pdf" in formats:
                built.append(build_pdf(edition, pandoc, browser, work, output_dir))

    print("\nBuilt:")
    for path in built:
        print("  " + describe(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
