# Markitdown Reference Converter

Converts a folder of reference documents into individual Markdown files.

Works with any reference folder.

---

## What it does

Reads every supported file in your `references/` folder and outputs one `.md` file per document into `references/markdown/`. Re-running the script skips files that are already up-to-date.

## Supported file types

| Category | Extensions |
|---|---|
| Documents | `.pdf`, `.docx`, `.doc` |
| Presentations | `.pptx`, `.ppt` |
| Spreadsheets | `.xlsx`, `.xls`, `.csv`, `.tsv` |
| Data / Web | `.json`, `.xml`, `.html` |
| Text | `.txt`, `.md`, `.rst` |
| Images | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp` |
| Archives | `.zip` |

## Folder structure

```
kenyan-context/
├── convert_references.py
├── references/
│   ├── paper1.pdf
│   ├── report.docx
│   └── ...
└── references/markdown/     ← generated, gitignored
    ├── paper1.md
    └── report.md
```

## Setup

**Requirements:** Python 3.8+

Install the dependency:

```bash
pip install "markitdown[all]"
```

## Usage

Run from the project root:

```bash
python convert_references.py
```

Or point it at a custom folder:

```bash
python convert_references.py --folder /path/to/references
```

## Notes

- **Scanned PDFs** (image-only, no text layer) will produce empty output — an OCR tool is needed for those.
- The `references/` folder itself and generated `markdown/` output are gitignored. Only the script and this README are tracked.
