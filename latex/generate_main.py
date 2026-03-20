#!/usr/bin/env python3
"""Generate latex/schulchronik.tex from all page files in latex/pages/.

Detection rules for each page file:
- "starts_with_heading": first non-comment, non-blank, non-\\seite line is
  \\jahresueberschrift or \\abschnitt → the page manages its own \\pstart,
  so the main file does NOT wrap it.
- "ends_with_pend": last non-comment, non-blank line is \\pend →
  the main file does NOT add a closing \\pend after \\input.
"""

import glob
import os
import re
import sys

PAGES_DIR = os.path.join(os.path.dirname(__file__), "pages")
OUTPUT = os.path.join(os.path.dirname(__file__), "schulchronik.tex")

HEADING_RE = re.compile(r"\\(jahresueberschrift|abschnitt|ueberschrift)\{")
SEITE_RE = re.compile(r"\\seite\{")


def meaningful_lines(filepath):
    """Yield non-blank, non-comment lines from a .tex file."""
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("%"):
                yield stripped


def starts_with_heading(filepath):
    """True if the first content command (after \\seite) is a heading."""
    for line in meaningful_lines(filepath):
        if SEITE_RE.match(line):
            continue
        return bool(HEADING_RE.match(line))
    return False


def ends_with_pend(filepath):
    """True if the last meaningful line is \\pend."""
    last = None
    for line in meaningful_lines(filepath):
        last = line
    return last is not None and last == r"\pend"


def generate():
    pages = sorted(glob.glob(os.path.join(PAGES_DIR, "*.tex")))
    if not pages:
        print("No page files found in", PAGES_DIR, file=sys.stderr)
        sys.exit(1)

    entries = []
    for p in pages:
        name = os.path.splitext(os.path.basename(p))[0]  # e.g. "002"
        heading = starts_with_heading(p)
        pend = ends_with_pend(p)
        entries.append((name, heading, pend))

    lines = []
    lines.append(r"\input{preamble}")
    lines.append("")
    lines.append(r"\begin{document}")
    lines.append("")
    lines.append(r"\frontmatter")
    lines.append(r"\title{Schul-Chronik}")
    lines.append(r"\subtitle{Sefferweich, Kreis Bitburg}")
    lines.append(r"\author{Transkription: Arbeitskreis Geschichte Sefferweich}")
    lines.append(r"\date{1851\,ff.}")
    lines.append(r"\maketitle")
    lines.append("")
    lines.append(r"\mainmatter")
    lines.append(r"\beginnumbering")

    for i, (name, heading, pend) in enumerate(entries):
        lines.append("")
        if heading:
            lines.append(f"% Page {name} starts with a heading — manages its own \\pstart")
            lines.append(f"\\input{{pages/{name}}}")
        else:
            lines.append(r"\pstart")
            lines.append(f"\\input{{pages/{name}}}")
            if not pend:
                lines.append(r"\pend")

        # Add page separator between pages (not after the last one)
        if i < len(entries) - 1:
            lines.append("")
            lines.append(r"\originalpagebreak")

    lines.append("")
    lines.append(r"\endnumbering")
    lines.append(r"\end{document}")
    lines.append("")  # trailing newline

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated {OUTPUT} with {len(entries)} pages:")
    for name, heading, pend in entries:
        flags = []
        if heading:
            flags.append("heading-start")
        if pend:
            flags.append("self-closing")
        print(f"  {name}: {', '.join(flags) if flags else 'wrapped'}")


if __name__ == "__main__":
    generate()
