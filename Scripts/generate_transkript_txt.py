#!/usr/bin/env python3
"""Regenerate Transkript.txt from merged transcript files (Phase 3)."""

import glob, os, re, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(SCRIPT_DIR, "..")
TRANSKRIPT_DIR = os.path.join(ROOT, "Transkript")
OUTPUT = os.path.join(ROOT, "Transkript.txt")
SEPARATOR = "------------"

def extract_text_block(md_path):
    """Extract lines inside ```text fenced code block."""
    lines = []
    in_block = False
    with open(md_path, encoding="utf-8") as f:
        for line in f:
            if line.strip() == "```text":
                in_block = True
                continue
            if in_block and line.strip() == "```":
                break
            if in_block:
                lines.append(line.rstrip("\n"))
    return lines

def main():
    # Find all NNN.md files (exclude subdirectories claude/, gemini/, codex/)
    pattern = os.path.join(TRANSKRIPT_DIR, "[0-9][0-9][0-9].md")
    files = sorted(glob.glob(pattern))

    if not files:
        print("No transcript files found.", file=sys.stderr)
        sys.exit(1)

    blocks = []
    for f in files:
        text = extract_text_block(f)
        if text:
            blocks.append("\n".join(text))

    result = ("\n" + SEPARATOR + "\n").join(blocks) + "\n"

    if "--stdout" in sys.argv:
        sys.stdout.write(result)
    else:
        with open(OUTPUT, "w", encoding="utf-8") as out:
            out.write(result)
        print(f"Wrote {len(blocks)} pages to Transkript.txt")

if __name__ == "__main__":
    main()
