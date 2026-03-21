#!/usr/bin/env python3
"""Convert merge_report.md tables to card layout for A4 portrait PDF."""

import re
import sys
from pathlib import Path

FRONTMATTER = """\
---
title: "Transkriptionsbericht"
subtitle: "Schulchronik Sefferweich — Qualitätskontrolle der KI-Transkription"
author: "Arbeitskreis Geschichte Sefferweich"
date: \\today
lang: de
geometry: a4paper,margin=2.5cm
fontsize: 11pt
colorlinks: true
toc: false
---
"""


def parse_pipe_table(lines):
    """Parse markdown pipe table into list of dicts.

    Returns (headers, rows) where rows is a list of dicts keyed by header.
    """
    if len(lines) < 3:
        return []
    # Parse header
    headers = [h.strip() for h in lines[0].strip().strip("|").split("|")]
    # Skip separator line (lines[1])
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        row = {}
        for i, h in enumerate(headers):
            row[h] = cells[i] if i < len(cells) else ""
        rows.append(row)
    return headers, rows


def escape_latex(text):
    r"""Escape bare LaTeX commands (e.g. \abschnitt) in prose text.

    Wraps lone backslash-sequences in backticks so Pandoc does not pass
    them through as LaTeX control sequences.  Already backtick-wrapped
    commands are left untouched.
    """
    # Match \word that is NOT already inside backticks
    return re.sub(r'(?<!`)\\([a-zA-Z]+)(?!`)', r'`\\\1`', text)


def format_merge_cards(rows):
    """Convert merge stats rows to card layout."""
    out = []
    for row in rows:
        seite = row.get("Seite", "???")
        out.append(f"### Seite {seite}\n")
        for key in [
            "3-Wege-Übereinstimmung",
            "2-von-3 Akzeptiert",
            "2-von-3 Abgelehnt",
            "Alle Abweichend",
            "Manuelle Prüfung",
        ]:
            val = row.get(key, "—")
            out.append(f"**{key}:** {val}  ")
        anm = row.get("Anmerkungen", "")
        if anm:
            out.append(f"\n{escape_latex(anm)}\n")
        out.append("")
    return "\n".join(out)


def format_phase4_cards(rows):
    """Convert Phase-4 status rows to card layout."""
    out = []
    for row in rows:
        llm = row.get("LLM", "???")
        out.append(f"### {llm}\n")
        fertig = row.get("Seiten fertig", "—")
        fehlend = row.get("Seiten fehlend", "—")
        out.append(f"- **Seiten fertig:** {fertig}")
        out.append(f"- **Seiten fehlend:** {fehlend}")
        out.append("")
    return "\n".join(out)


def format_ratelimit_list(rows):
    """Convert rate-limit log rows to chronological list."""
    out = []
    for row in rows:
        ts = row.get("Zeitstempel", "")
        llm = row.get("LLM", "")
        seite = row.get("Seite", "")
        aktion = row.get("Aktion", "")
        out.append(f"- **{ts} — {llm}, Seite {seite}:** {aktion}")
    return "\n".join(out)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <merge_report.md> <output.md>", file=sys.stderr)
        sys.exit(1)

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])

    content = src.read_text(encoding="utf-8")
    lines = content.splitlines()

    output_parts = [FRONTMATTER]

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect pipe table start (line with | that is followed by a separator)
        if (
            "|" in line
            and i + 1 < len(lines)
            and re.match(r"\s*\|[\s\-:|]+\|\s*$", lines[i + 1])
        ):
            # Collect all table lines
            table_lines = []
            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i])
                i += 1

            headers, rows = parse_pipe_table(table_lines)

            # Identify which table this is by headers
            if "Seite" in headers and "3-Wege-Übereinstimmung" in headers:
                output_parts.append(format_merge_cards(rows))
            elif "LLM" in headers and "Seiten fertig" in headers:
                output_parts.append(format_phase4_cards(rows))
            elif "Zeitstempel" in headers and "Aktion" in headers:
                output_parts.append(format_ratelimit_list(rows))
            else:
                # Unknown table — pass through as-is
                output_parts.append("\n".join(table_lines))
                output_parts.append("")
        else:
            output_parts.append(line)
            i += 1

    dst.write_text("\n".join(output_parts), encoding="utf-8")
    print(f"Written: {dst}")


if __name__ == "__main__":
    main()
