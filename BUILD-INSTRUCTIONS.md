# Build Instructions for THE ARCHITECTURE OF SHADOWS

## Working build (verified 2026-10-29)

This is the build that was actually run. It needs **Pandoc** and a **Chromium
browser**; it does **not** need LaTeX.

### Prerequisites

- **Python 3.10+** — runs the two scripts; no third-party package is used.
- **Pandoc 3.13** — converts Markdown to EPUB 3 and to standalone HTML.
- **Microsoft Edge or another Chromium browser** — prints the HTML to PDF.

The scripts find the tools in this order:

1. `PANDOC` / `EDGE` environment variables.
2. `pandoc` on `PATH`; Edge at its standard Windows install paths.
3. The portable Pandoc path used on this machine
   (`C:\Users\jpowe\AppData\Local\Temp\opencode\pandoc-3.13\pandoc-3.13\pandoc.exe`).

Set the variables explicitly if the defaults do not match your machine:

```powershell
$env:PANDOC = "C:\path\to\pandoc.exe"
$env:EDGE   = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

### Build everything

```sh
python build-book.py --edition all --format all
```

### Build one edition or one format

```sh
python build-book.py --edition master  --format epub
python build-book.py --edition master  --format pdf
python build-book.py --edition student --format epub
python build-book.py --edition student --format pdf
python build-book.py --edition all     --format html
```

Outputs are written to the book root:

| Artifact | Size (2026-10-29) | Structure |
|---|---|---|
| `THE-ARCHITECTURE-OF-SHADOWS-MASTER.epub` | 0.57 MB | 410 spine items, 410 XHTML, 0 malformed XML |
| `THE-ARCHITECTURE-OF-SHADOWS-MASTER.pdf` | 8.60 MB | 462 pages, PDF 1.4 |
| `THE-ARCHITECTURE-OF-SHADOWS-STUDENT.epub` | 0.51 MB | 365 spine items, 365 XHTML, 0 malformed XML |
| `THE-ARCHITECTURE-OF-SHADOWS-STUDENT.pdf` | 7.47 MB | 397 pages, PDF 1.4 |

### Verify the artifacts

```sh
python verify-book.py
```

This checks the ZIP container, `META-INF/container.xml`, the OPF, the spine
count, XML well-formedness, the PDF header and page count, and the source
chapter counts. It reports the title-page placeholders and the 17-vs-16 volume
label as **content findings** without failing, because they are owner
decisions. Use `--strict` to make those findings fail.

### How the PDF is made

There is no LaTeX distribution on this machine. `build-book.py` therefore:

1. asks Pandoc for a standalone HTML5 file with embedded resources and a
   print stylesheet;
2. opens that file in headless Edge and prints it to PDF with
   `--no-pdf-header-footer`.

The PDF is **A4** with 18/16/20/16 mm margins. It is not the XeLaTeX layout
described below, and there is no print-ready letter-size PDF.

### Reproducibility note

The master edition is 409 Markdown inputs (6 front-matter files and 403
chapters); the student edition is 364 chapters. `build-book.py` writes a
Pandoc defaults file in a temporary directory instead of passing every path on
the command line, which avoids the Windows command-line length limit.

---

## Alternative: XeLaTeX build (not installed here)

The original commands are retained for a machine that has a LaTeX
distribution. They have **not** been run in this workspace.

### Prerequisites

- **Pandoc**: https://pandoc.org/installing.html
- **LaTeX** (for the PDF engine): https://www.latex-project.org/get/
  - On Windows: MiKTeX or TeX Live
  - On macOS: MacTeX
  - On Linux: TeX Live

### Master Edition (all content, including hidden/esoteric)

```bash
cd MASTER-EDITION
pandoc --pdf-engine=xelatex --variable=geometry:margin=1in --variable fontsize=11pt --toc --toc-depth=3 -o ../THE-ARCHITECTURE-OF-SHADOWS-MASTER.pdf 00-FRONT-MATTER/*.md VOLUME-*/PART-*/chapter-*.md
pandoc --toc --toc-depth=3 -o ../THE-ARCHITECTURE-OF-SHADOWS-MASTER.epub 00-FRONT-MATTER/*.md VOLUME-*/PART-*/chapter-*.md
```

### Student Edition (foundational content only)

```bash
cd STUDENT-EDITION
pandoc --pdf-engine=xelatex --variable=geometry:margin=1in --variable fontsize=11pt --toc --toc-depth=3 -o ../THE-ARCHITECTURE-OF-SHADOWS-STUDENT.pdf VOLUME-*/PART-*/chapter-*.md
pandoc --toc --toc-depth=3 -o ../THE-ARCHITECTURE-OF-SHADOWS-STUDENT.epub VOLUME-*/PART-*/chapter-*.md
```

### Print-ready version

```bash
cd MASTER-EDITION
pandoc --pdf-engine=xelatex --variable=geometry:margin=0.75in --variable fontsize=10pt --variable papersize:letter --toc --toc-depth=3 -o ../THE-ARCHITECTURE-OF-SHADOWS-PRINT.pdf 00-FRONT-MATTER/*.md VOLUME-*/PART-*/chapter-*.md
```

## Known content issues

These are not build failures, but they block a publication claim:

- `MASTER-EDITION/00-FRONT-MATTER/title-page.md` still contains
  `[Author Name]`, `[Publisher Name]` and `[ISBN Number]`.
- The title page and copyright page say **17-Volume**, but the master tree has
  **16** volumes (`VOLUME-I` to `VOLUME-XVI`).
- The book carries both the Pandoc navigation document and the hand-written
  `00-FRONT-MATTER/table-of-contents.md`.
- No `epubcheck` run and no editorial fact-check, legal review or source audit
  has been performed.
- `THE ARCHITECTURE OF SHADOWS.txt` (138 KB) is a transcript, not the build
  source; it is not read by the build.

## Other notes

- The build commands assume the Markdown tree keeps its current folder
  structure.
- EPUB files can be converted to MOBI for Kindle using Calibre.
- The manifest `build.yaml` is the authoritative record of commands, evidence
  and open issues; update it when a build claim changes.
