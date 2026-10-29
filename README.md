# THE ARCHITECTURE OF SHADOWS

A complete encyclopedia of the global drug trade: every continent, every
player, every process, every consequence, every angle.

## Editions

- `MASTER-EDITION/` — 16 volumes, 53 parts, 403 chapters, plus 6 front-matter
  files, including the hidden and esoteric material.
- `STUDENT-EDITION/` — 12 volumes, 46 parts, 364 chapters.
- `WEB-VERSION/` — a separate static presentation.

`THE ARCHITECTURE OF SHADOWS.txt` (138 KB) is a transcript, not the build
source. The build reads only the chapter trees.

## Build

The verified build uses Pandoc 3.13 for EPUB and standalone HTML, then prints
the HTML to PDF with headless Microsoft Edge. LaTeX is not required.

```sh
python build-book.py --edition all --format all
python verify-book.py
```

Set `PANDOC` and `EDGE` if the tools are not on the default paths. See
`BUILD-INSTRUCTIONS.md` for the full commands, the artifact table and the
unrun XeLaTeX alternative.

## Artifacts (2026-10-29)

| Artifact | Size | Structure |
|---|---|---|
| Master EPUB | 0.57 MB | 410 spine items, 410 XHTML, 0 malformed XML |
| Master PDF | 8.60 MB | 462 pages, A4, PDF 1.4 |
| Student EPUB | 0.51 MB | 365 spine items, 365 XHTML, 0 malformed XML |
| Student PDF | 7.47 MB | 397 pages, A4, PDF 1.4 |

## Publication status

The artifacts are built and structurally verified, but the book is not
publication-ready:

- the PDF is A4 Chromium print output, not the documented XeLaTeX layout, and
  there is no print-ready letter PDF;
- the title page still contains `[Author Name]`, `[Publisher Name]` and
  `[ISBN Number]`;
- the title and copyright pages say **17-Volume** while the master tree has
  **16** volumes;
- the book carries both the Pandoc navigation document and the hand-written
  `00-FRONT-MATTER/table-of-contents.md`;
- no `epubcheck` run and no editorial, source or legal review has been done.

`build.yaml` is the authoritative record of commands, evidence and open
issues.
