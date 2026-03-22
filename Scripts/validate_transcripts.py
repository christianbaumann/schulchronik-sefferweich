#!/usr/bin/env python3
"""Validate that merged transcripts have required structure."""

import glob, os, re, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSKRIPT_DIR = os.path.join(SCRIPT_DIR, "..", "Transkript")

CHECKS = [
    ("Hinweise section", r"^###\s+Hinweise zur Transkription"),
    ("Text block",       r"^```text"),
    ("Text block end",   r"^```$"),
    ("Analyse section",  r"^###\s+Historische und sprachliche Analyse"),
]

def validate(path):
    """Return list of failed checks for a transcript file."""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    failures = []
    for name, pattern in CHECKS:
        if not re.search(pattern, content, re.MULTILINE):
            failures.append(name)
    # Check text block is non-empty
    m = re.search(r"```text\n(.*?)```", content, re.DOTALL)
    if m and not m.group(1).strip():
        failures.append("Text block is empty")
    return failures

def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else sorted(
        glob.glob(os.path.join(TRANSKRIPT_DIR, "[0-9][0-9][0-9].md"))
    )
    errors = 0
    for f in files:
        failures = validate(f)
        if failures:
            name = os.path.basename(f)
            for fail in failures:
                print(f"FAIL {name}: missing {fail}")
            errors += 1
    if errors:
        print(f"\n{errors} file(s) with structural issues.")
        sys.exit(1)
    else:
        print(f"OK: {len(files)} file(s) validated.")

if __name__ == "__main__":
    main()
