#!/usr/bin/env python3
"""
convert_references.py
---------------------
Converts all files in a `references` folder into individual Markdown files
saved in `references/markdown/`. Supports PDFs, Word docs, PowerPoint,
Excel, images, HTML, CSV, JSON, XML, ZIP, and plain text.

Usage:
    python convert_references.py [--folder PATH]

Default folder: ./references  (same directory as this script)
"""

import argparse
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Supported extensions (markitdown handles all of these)
# ---------------------------------------------------------------------------
SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".doc",
    ".pptx", ".ppt",
    ".xlsx", ".xls",
    ".csv", ".tsv",
    ".json", ".xml",
    ".html", ".htm",
    ".txt", ".md", ".rst",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp",
    ".zip",
    ".wav", ".mp3",
}


def convert_file(md, source_path: Path, output_dir: Path) -> bool:
    """Convert a single file to Markdown. Returns True on success."""
    out_path = output_dir / (source_path.stem + ".md")

    # Skip if output already exists and is newer than source
    if out_path.exists() and out_path.stat().st_mtime >= source_path.stat().st_mtime:
        print(f"  [skip]  {source_path.name}  (up-to-date)")
        return True

    try:
        result = md.convert(str(source_path))
        text = result.text_content or ""

        if not text.strip():
            print(f"  [warn]  {source_path.name}  → empty output (may be scanned/image-only)")
            # Still write the file so the user can see what happened
            text = f"<!-- markitdown produced no text for {source_path.name} -->\n"

        header = (
            f"<!-- Source: {source_path.name} -->\n"
            f"<!-- Converted by convert_references.py -->\n\n"
        )
        out_path.write_text(header + text, encoding="utf-8")
        print(f"  [ok]    {source_path.name}  →  markdown/{out_path.name}")
        return True

    except Exception as exc:
        print(f"  [fail]  {source_path.name}  →  {exc}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Convert reference files to Markdown for LLM prompting."
    )
    parser.add_argument(
        "--folder",
        default="references",
        help="Path to the references folder (default: ./references)",
    )
    args = parser.parse_args()

    references_dir = Path(args.folder).resolve()

    if not references_dir.exists():
        print(f"ERROR: Folder not found: {references_dir}")
        print("  Create a 'references' folder next to this script and put your files in it.")
        sys.exit(1)

    output_dir = references_dir / "markdown"
    output_dir.mkdir(exist_ok=True)

    # Collect files (non-recursive by default; skip files already in markdown/)
    files = [
        f for f in references_dir.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files:
        print(f"No supported files found in: {references_dir}")
        print(f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
        sys.exit(0)

    print(f"\nReferences folder : {references_dir}")
    print(f"Output folder     : {output_dir}")
    print(f"Files to convert  : {len(files)}\n")

    # Lazy-import so the error message is clear if markitdown isn't installed
    try:
        from markitdown import MarkItDown
    except ImportError:
        print("ERROR: markitdown is not installed.")
        print("  Run:  pip install markitdown")
        sys.exit(1)

    md = MarkItDown()

    ok = fail = skipped = 0
    for f in sorted(files):
        before_mtime = (output_dir / (f.stem + ".md")).stat().st_mtime \
            if (output_dir / (f.stem + ".md")).exists() else None
        success = convert_file(md, f, output_dir)
        after_exists = (output_dir / (f.stem + ".md")).exists()

        if success:
            # Detect whether it was actually newly written or skipped
            after_mtime = (output_dir / (f.stem + ".md")).stat().st_mtime if after_exists else None
            if before_mtime is not None and after_mtime == before_mtime:
                skipped += 1
            else:
                ok += 1
        else:
            fail += 1

    print(f"\nDone.  Converted: {ok}  |  Skipped (up-to-date): {skipped}  |  Failed: {fail}")
    if ok or skipped:
        print(f"\nMarkdown files are in: {output_dir}")


if __name__ == "__main__":
    main()
