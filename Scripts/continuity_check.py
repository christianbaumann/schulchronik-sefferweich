#!/usr/bin/env python3
"""Flag potential continuity breaks between consecutive transcript pages.

Heuristic: if page N ends without sentence-ending punctuation and
page N+1 starts with an uppercase letter, flag the pair.
"""

import glob, os, re, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSKRIPT_DIR = os.path.join(SCRIPT_DIR, "..", "Transkript")

def extract_text_block(md_path):
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

def last_text_line(lines):
    """Return last non-blank, non-page-number line."""
    for line in reversed(lines):
        stripped = line.strip()
        if stripped and not re.match(r"^\d{1,3}$", stripped):
            return stripped
    return ""

def first_text_line(lines):
    """Return first non-blank, non-page-number, non-heading line."""
    for line in lines:
        stripped = line.strip()
        if stripped and not re.match(r"^\d{1,3}$", stripped):
            return stripped
    return ""

def main():
    files = sorted(glob.glob(os.path.join(TRANSKRIPT_DIR, "[0-9][0-9][0-9].md")))
    flags = []

    for i in range(len(files) - 1):
        block_a = extract_text_block(files[i])
        block_b = extract_text_block(files[i + 1])
        if not block_a or not block_b:
            continue

        last = last_text_line(block_a)
        first = first_text_line(block_b)

        # Flag if last line doesn't end with sentence punctuation
        if last and not re.search(r'[.!?:;]"?\s*$', last):
            page_a = os.path.basename(files[i])[:3]
            page_b = os.path.basename(files[i + 1])[:3]
            flags.append((page_a, page_b, last[-60:], first[:60]))

    if flags:
        print(f"Potential continuity issues ({len(flags)} pairs):\n")
        for pa, pb, last, first in flags:
            print(f"  {pa} -> {pb}")
            print(f"    ends:   ...{last}")
            print(f"    starts: {first}...")
            print()
    else:
        print("No continuity issues detected.")

if __name__ == "__main__":
    main()
