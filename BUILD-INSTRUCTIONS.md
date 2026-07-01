# Build Instructions for THE ARCHITECTURE OF SHADOWS

## Prerequisites

To generate output formats, you need to install the following tools:

### PDF Generation
- **Pandoc**: https://pandoc.org/installing.html
- **LaTeX** (for PDF engine): https://www.latex-project.org/get/
  - On Windows: MiKTeX or TeX Live
  - On macOS: MacTeX
  - On Linux: TeX Live

### EPUB Generation
- **Pandoc**: https://pandoc.org/installing.html

### Print-Ready PDF
- **Pandoc**: https://pandoc.org/installing.html
- **LaTeX**: https://www.latex-project.org/get/

## Build Commands

### Master Edition (All Content Including Hidden/Esoteric)

```bash
# Build Master Edition PDF
cd MASTER-EDITION
pandoc --pdf-engine=xelatex --variable=geometry:margin=1in --variable fontsize=11pt --toc --toc-depth=3 -o ../THE-ARCHITECTURE-OF-SHADOWS-MASTER.pdf 00-FRONT-MATTER/*.md VOLUME-*/PART-*/chapter-*.md

# Build Master Edition EPUB
pandoc --toc --toc-depth=3 -o ../THE-ARCHITECTURE-OF-SHADOWS-MASTER.epub 00-FRONT-MATTER/*.md VOLUME-*/PART-*/chapter-*.md
```

### Student Edition (Foundational Content Only)

```bash
# Build Student Edition PDF
cd STUDENT-EDITION
pandoc --pdf-engine=xelatex --variable=geometry:margin=1in --variable fontsize=11pt --toc --toc-depth=3 -o ../THE-ARCHITECTURE-OF-SHADOWS-STUDENT.pdf VOLUME-*/PART-*/chapter-*.md

# Build Student Edition EPUB
pandoc --toc --toc-depth=3 -o ../THE-ARCHITECTURE-OF-SHADOWS-STUDENT.epub VOLUME-*/PART-*/chapter-*.md
```

### Print-Ready Version

```bash
# Build Print-Ready PDF (Master Edition)
cd MASTER-EDITION
pandoc --pdf-engine=xelatex --variable=geometry:margin=0.75in --variable fontsize=10pt --variable papersize:letter --toc --toc-depth=3 -o ../THE-ARCHITECTURE-OF-SHADOWS-PRINT.pdf 00-FRONT-MATTER/*.md VOLUME-*/PART-*/chapter-*.md
```

## Notes

- The build commands assume all markdown files are in the correct folder structure
- You may need to adjust the file glob patterns based on your actual structure
- For large books, consider building in sections or using a build script
- EPUB files can be converted to MOBI for Kindle using Calibre
