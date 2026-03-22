#!/usr/bin/env python3
r"""Convert Transkript/NNN.md to LaTeX/pages/NNN.tex.

Reads the text block from each merged transcript, analyzes the spatial
layout (margin notes, main text column, headings, verse blocks), and emits
LaTeX using the project's custom commands.
"""

import argparse
import difflib
import glob
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSKRIPT_DIR = os.path.join(SCRIPT_DIR, "..", "Transkript")
PAGES_DIR = os.path.join(SCRIPT_DIR, "pages")
GOLD_DIR = os.path.join(SCRIPT_DIR, "gold")

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class LayoutInfo:
    main_col: int          # starting column of main text
    has_margin_notes: bool
    is_diary: bool         # date-based left column (e.g. "13. Dezember.")

@dataclass
class LineInfo:
    kind: str           # page_number, blank, heading, margin_and_text,
                        # margin_only, text_only, verse, divider, signature
    margin_text: str    # text in margin column (empty if none)
    main_text: str      # text in main column (empty if none)
    raw: str            # original line

# ---------------------------------------------------------------------------
# Phase 1: Parser
# ---------------------------------------------------------------------------

def extract_text_block(md_path: str) -> list[str]:
    """Extract lines inside the ```text fenced code block."""
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


def detect_page_number(lines: list[str]) -> tuple:
    """Find and return (page_number_str, line_index) from centered page number."""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and stripped.isdigit():
            return stripped, i
    return None, -1


def analyze_layout(lines: list[str], page_num_idx: int) -> LayoutInfo:
    """Detect main text column, margin notes, and diary format."""
    starts = []
    for i, line in enumerate(lines):
        if i == page_num_idx or not line.strip():
            continue
        first_char = len(line) - len(line.lstrip(" "))
        starts.append(first_char)

    if not starts:
        return LayoutInfo(main_col=20, has_margin_notes=False, is_diary=False)

    # The main column is the most frequent start position >= 8
    # (margin notes start at 0-6, headings may be further right)
    counter = Counter(s for s in starts if s >= 8)
    if counter:
        main_col = counter.most_common(1)[0][0]
    else:
        # Fallback: use median of all starts
        main_col = sorted(starts)[len(starts) // 2]

    has_margin = any(s < main_col - 4 for s in starts)

    # Gap verification: on pages where centered headings inflate main_col,
    # body text starting at col 0 gets mis-classified as margin content.
    # Real margin+text lines have an internal gap (3+ spaces) between the
    # margin annotation and the main text.  If most would-be margin lines
    # lack such a gap, the page has no actual margin layout.
    if has_margin:
        gap_lines = 0
        no_gap_lines = 0
        for i, line in enumerate(lines):
            if i == page_num_idx or not line.strip():
                continue
            stripped = line.strip()
            if stripped in ("———", "————", "———————", "========", "--------"):
                continue
            first_char = len(line) - len(line.lstrip(" "))
            line_len = len(line.rstrip())
            if first_char < main_col - 4 and line_len > main_col:
                # This line would be classified as margin_and_text
                text = line.rstrip()
                if re.search(r'\S\s{3,}\S', text):
                    gap_lines += 1
                else:
                    no_gap_lines += 1
        if no_gap_lines > gap_lines:
            # Most "margin" lines have no gap → body text at col 0
            has_margin = False

    # Diary detection: check if margin-column text looks like dates
    is_diary = False
    if has_margin:
        date_pattern = re.compile(r'^\d+\.\s+("|\w)')
        date_count = 0
        margin_count = 0
        for i, line in enumerate(lines):
            if i == page_num_idx or not line.strip():
                continue
            first_char = len(line) - len(line.lstrip(" "))
            if first_char < main_col - 4:
                margin_count += 1
                margin_text = line[:main_col].rstrip()
                if date_pattern.match(margin_text.strip()):
                    date_count += 1
        if margin_count > 0 and date_count / margin_count > 0.3:
            is_diary = True

    return LayoutInfo(main_col=main_col, has_margin_notes=has_margin,
                      is_diary=is_diary)


def classify_lines(lines: list[str], layout: LayoutInfo,
                   page_num_idx: int) -> list[LineInfo]:
    """Tag each line with its structural role."""
    result = []
    mc = layout.main_col

    for i, line in enumerate(lines):
        raw = line

        # Page number
        if i == page_num_idx:
            result.append(LineInfo("page_number", "", line.strip(), raw))
            continue

        # Blank
        if not line.strip():
            result.append(LineInfo("blank", "", "", raw))
            continue

        # Divider
        stripped = line.strip()
        if stripped in ("———", "————", "———————", "========", "--------"):
            result.append(LineInfo("divider", "", stripped, raw))
            continue

        # Determine column positions
        first_char_pos = len(line) - len(line.lstrip(" "))
        has_margin_content = (layout.has_margin_notes
                              and first_char_pos < mc - 4
                              if mc > 4 else False)

        if has_margin_content:
            margin_part = line[:mc].rstrip()
            main_part = line[mc:].rstrip() if len(line) > mc else ""
        else:
            margin_part = ""
            main_part = line[first_char_pos:].rstrip()

        # Check if this is margin-only (no text in main column)
        if has_margin_content and not main_part.strip():
            result.append(LineInfo("margin_only", margin_part.strip(),
                                  "", raw))
            continue

        # Margin + text
        if has_margin_content and main_part.strip():
            result.append(LineInfo("margin_and_text", margin_part.strip(),
                                  main_part, raw))
            continue

        # Text only (default for now; headings/verse detected in second pass)
        result.append(LineInfo("text_only", "", main_part if main_part else stripped, raw))

    # --- Second pass: detect headings, signatures, and verse blocks ---
    _detect_headings(result, layout)
    _detect_signatures(result)
    _detect_verse(result, layout, page_num_idx >= 0)

    return result


# Known heading patterns
_HEADING_PATTERNS = [
    re.compile(r"^Das Jahr \d{4}"),
    re.compile(r"^Das Schuljahr \d{4}"),
    re.compile(r"^[IVX]+\.\s"),             # Roman numeral sections
    re.compile(r"^\d+\.\s+[A-ZÄÖÜ]"),       # Numbered sections
    re.compile(r"^(Die Schule|Revision|Vertretung|Weihnachtsfeier|"
               r"Osterprüfung|Nachtrag|Schul\s*-\s*Chronik)"),
    re.compile(r"^1\s*9\s*\d\s*\d"),        # Spaced year like "1 9 1 2."
]


def _is_heading_text(text: str) -> bool:
    """Check if text matches known heading patterns or is short & centered."""
    text = text.strip().rstrip(".")
    if not text:
        return False
    for pat in _HEADING_PATTERNS:
        if pat.match(text):
            return True
    # Short text (< 35 chars) that's not a regular sentence
    if len(text) < 35 and not text.endswith(","):
        # Must not look like a regular sentence fragment
        words = text.split()
        if len(words) <= 6:
            return True
    return False


def _detect_headings(lines: list[LineInfo], layout: LayoutInfo):
    """Promote text_only lines to heading if they match heading patterns."""
    mc = layout.main_col
    for i, li in enumerate(lines):
        if li.kind != "text_only":
            continue
        if not _is_heading_text(li.main_text):
            continue
        indent = len(li.raw) - len(li.raw.lstrip(" "))
        # Check: preceded by blank (or page_number or start)
        prev_blank = (i == 0 or
                      lines[i-1].kind in ("blank", "page_number"))
        # Check: followed by blank (or end)
        next_blank = (i == len(lines) - 1 or
                      lines[i+1].kind == "blank")
        # Centered text with known heading pattern: heading even without
        # blank after (e.g., page 040 "Revision." directly above text)
        is_centered = indent >= mc + 4
        if prev_blank and next_blank:
            li.kind = "heading"
        elif prev_blank and is_centered:
            li.kind = "heading"


def _detect_verse(lines: list[LineInfo], layout: LayoutInfo,
                  has_page_number: bool):
    """Detect verse blocks: consecutive text_only lines indented 4+ chars
    past main_col that aren't already headings."""
    mc = layout.main_col
    seen_first_content = False
    for i, li in enumerate(lines):
        if li.kind in ("blank", "page_number"):
            continue
        if not seen_first_content:
            seen_first_content = True
            # Don't classify the first content line as verse if there's
            # no page number — it's likely continuation from previous page.
            if not has_page_number and li.kind == "text_only":
                continue
        if li.kind != "text_only":
            continue
        indent = len(li.raw) - len(li.raw.lstrip(" "))
        if indent >= mc + 4:
            li.kind = "verse"


def _detect_signatures(lines: list[LineInfo]):
    """Detect signature blocks (centered official signatures)."""
    sig_patterns = [
        re.compile(r"^den \d"),
        re.compile(r"^Der (Orts|Kreis)"),
        re.compile(r"^\w+,\s*(Pfarrer|Pfr\.|Lehrer)"),
        re.compile(r"^Gelesen"),
    ]
    for li in lines:
        if li.kind != "text_only":
            continue
        for pat in sig_patterns:
            if pat.match(li.main_text.strip()):
                li.kind = "signature"
                break


# ---------------------------------------------------------------------------
# Phase 2: LaTeX Emitter
# ---------------------------------------------------------------------------

# Abbreviation patterns: word.SPACE where word is a known abbreviation
_ABBREVIATIONS = {
    "fr", "Joh", "Matth", "M", "St", "Floren", "Gottfr", "u", "v", "i",
    "V", "Nov", "Aug", "Pfr", "Pf", "geb", "gest", "Nr", "bzw",
    "Dez", "Okt", "Sept", "Jan", "Febr", "Apr", "kgl", "ev", "kath",
    "resp", "sog", "z", "B", "d", "H", "Dr", "Chr", "Wilh", "Friedr",
    "Heinr", "Jak", "Andr", "Phil", "A", "S", "E", "J", "K", "L", "N",
    "O", "P", "R", "T", "W", "G", "F", "C", "D",
}

def _apply_abbreviation_spacing(text: str) -> str:
    """Insert backslash-space after abbreviation periods: 'Joh. ' → 'Joh.\\ '."""
    def repl(m):
        word = m.group(1)
        after = m.group(2)
        if word in _ABBREVIATIONS:
            return word + ".\\ " + after
        # Also handle ordinal numbers: "18. Jahrhundert"
        if word.isdigit():
            return word + ".\\ " + after
        return m.group(0)  # no change

    # Match word.SPACE followed by next word char
    return re.sub(r'(\w+)\.\s+(\w)', repl, text)


def apply_substitutions(line: str) -> str:
    """Apply inline text substitutions (Markdown → LaTeX)."""
    # Escape TeX special characters that appear in prose
    line = line.replace("&", "\\&")
    # [darüber: TEXT] or [darüber eingefügt: TEXT]
    line = re.sub(r'\[darüber(?:\s+eingefügt)?:\s*(.+?)\]',
                  r'\\darueber{\1}', line)
    # ~~TEXT~~ → \sout{TEXT}
    line = re.sub(r'~~(.+?)~~', r'\\sout{\1}', line)
    # [?] → \unsicher (consume leading space; add {} to prevent macro eating chars)
    line = re.sub(r' \[\?\](?=\w)', r'\\unsicher{}', line)  # space+[?]+letter
    line = re.sub(r' \[\?\] ', r'\\unsicher{} ', line)      # space+[?]+space
    line = re.sub(r' \[\?\]', r'\\unsicher', line)           # space+[?]+end
    line = re.sub(r'\[\?\](?=\w)', r'\\unsicher{}', line)    # [?]+letter
    line = line.replace("[?]", "\\unsicher")
    # „TEXT" → \enquote{TEXT}
    line = re.sub(r'„(.+?)"', r'\\enquote{\1}', line)
    # Note: standalone " (U+0022) is NOT auto-converted to \ditto here.
    # Ditto marks are handled contextually in title page / diary handlers.
    # In prose, a leftover " is typically a closing quote from a cross-page
    # quotation and should remain literal.
    # Protect square brackets that aren't commands: [nicht] → {[nicht]}
    line = re.sub(r'\[(?!\\)(\w+)\]', r'{[\1]}', line)
    # Abbreviation spacing
    line = _apply_abbreviation_spacing(line)
    # Dash ranges: "40-42" → "40--42" (but not already --)
    line = re.sub(r'(\d+)\s*-\s*(\d)', r'\1--\2', line)
    # "Schul - Chronik" style spaced dashes → \,--\,
    line = re.sub(r'(\w)\s+-\s+(\w)', r'\1\\,--\\,\2', line)
    # " = " between place names: "Knöpfel = Malbergweich"
    line = re.sub(r'(\w)\s+=\s+(\w)', r'\1\\,=\\,\2', line)
    return line


def _group_margins(classified: list[LineInfo]) -> list[tuple]:
    """Group consecutive margin_and_text / margin_only lines.
    Returns list of (margin_lines, first_main_text_idx)."""
    groups = []
    i = 0
    while i < len(classified):
        li = classified[i]
        if li.kind in ("margin_and_text", "margin_only"):
            margin_lines = [li.margin_text]
            first_main_idx = i if li.kind == "margin_and_text" else None
            j = i + 1
            while j < len(classified) and classified[j].kind in ("margin_and_text", "margin_only"):
                margin_lines.append(classified[j].margin_text)
                if first_main_idx is None and classified[j].kind == "margin_and_text":
                    first_main_idx = j
                j += 1
            if first_main_idx is None:
                first_main_idx = i
            groups.append((margin_lines, first_main_idx))
            i = j
        else:
            i += 1
    return groups


def _is_boundary(classified: list[LineInfo], idx: int) -> bool:
    """True if line at idx is the last before a blank, heading, verse, divider,
    signature, end-of-list, or page boundary."""
    if idx >= len(classified) - 1:
        return True
    nxt = classified[idx + 1]
    return nxt.kind in ("blank", "heading", "verse", "divider",
                        "signature", "page_number")


def _line_ends_hyphenated(text: str) -> bool:
    """True if line ends with a hyphen indicating word break."""
    text = text.rstrip()
    if text.endswith("-"):
        # Make sure it's not a dash like "1939 -" or "—"
        if len(text) >= 2 and text[-2].isalpha():
            return True
    return False


def _convert_heading(text: str) -> str:
    """Convert heading text to appropriate LaTeX command."""
    text = text.strip().rstrip(".")
    # Year heading: "Das Jahr 1887" or "Das Jahr 1892/93"
    if re.match(r"Das Jahr \d{4}", text):
        return f"\\jahresueberschrift{{{text}}}"
    # School year: "Das Schuljahr 1905/06"
    if re.match(r"Das Schuljahr \d{4}", text):
        return f"\\jahresueberschrift{{{text}}}"
    # Spaced year: "1 9 1 2"
    m = re.match(r"^(\d)\s+(\d)\s+(\d)\s+(\d)\.?$", text)
    if m:
        year = m.group(1) + m.group(2) + m.group(3) + m.group(4)
        return f"\\jahresueberschrift{{{year}}}"
    # Everything else
    return f"\\abschnitt{{{text}}}"


def emit_page(page_num: str, classified: list[LineInfo],
              layout: LayoutInfo) -> str:
    """Assemble the full .tex file content for one page.

    Key convention from generate_main.py:
    - Pages starting with a heading manage their own \\pstart (heading first,
      then \\pstart). The main file does NOT wrap them.
    - Pages starting with prose do NOT emit \\pstart at the top — the main
      file provides it. They still end with \\pend.
    """
    out = []
    out.append(f"% Page {page_num}")
    out.append("")

    # \\seite command (page_num without leading zeros for display)
    display_num = str(int(page_num)) if page_num.isdigit() else page_num
    out.append(f"\\seite{{{display_num}}}")
    out.append("")

    # Build margin groups for lookup
    margin_groups = _group_margins(classified)
    margin_at = {}  # line_idx -> margin_text (joined with \\\\)
    for mg_lines, first_idx in margin_groups:
        joined = "\\\\".join(mg_lines)
        # Protect \\[ sequences: LaTeX interprets \\[ as linebreak + optional
        # vertical spacing argument.  Insert {} to break the parse.
        joined = joined.replace("\\\\[", "\\\\{}[")
        margin_at[first_idx] = joined

    # Determine if page starts with heading
    first_content = None
    for li in classified:
        if li.kind not in ("page_number", "blank"):
            first_content = li
            break

    starts_with_heading = first_content and first_content.kind == "heading"

    # If page does NOT start with heading, main file opens \pstart for us.
    # We track this as in_pstart = True from the start.
    in_pstart = not starts_with_heading
    just_after_structural = True  # suppress blanks at start / after headings

    # Process classified lines
    i = 0
    while i < len(classified):
        li = classified[i]

        if li.kind in ("page_number", "blank"):
            if li.kind == "blank" and in_pstart and not just_after_structural:
                # Real paragraph break between text blocks
                next_content = None
                for j in range(i+1, len(classified)):
                    if classified[j].kind != "blank":
                        next_content = classified[j]
                        break
                if next_content and next_content.kind not in ("heading",):
                    out.append("")
            i += 1
            continue

        # We've hit real content — clear the structural flag
        just_after_structural = False

        if li.kind == "heading":
            is_mid_page = in_pstart  # already in a paragraph → mid-page
            if in_pstart:
                out.append("")
                out.append("\\pend")
            out.append(_convert_heading(li.main_text))
            out.append("\\pstart")
            if is_mid_page:
                out.append("")  # blank line after \pstart for mid-page headings
            in_pstart = True
            just_after_structural = True
            i += 1
            continue

        if li.kind == "verse":
            # Collect consecutive verse lines
            if in_pstart:
                out.append("")
                out.append("\\pend")
                in_pstart = False
            verse_lines = []
            while i < len(classified) and classified[i].kind == "verse":
                vtext = apply_substitutions(classified[i].main_text.strip())
                verse_lines.append(vtext)
                i += 1
            out.append("\\begin{verse}")
            for vi, vl in enumerate(verse_lines):
                if vi < len(verse_lines) - 1:
                    out.append(vl + "\\\\")
                else:
                    out.append(vl)
            out.append("\\end{verse}")
            out.append("\\pstart")
            in_pstart = True
            continue

        if li.kind == "divider":
            out.append("\\trenner")
            i += 1
            continue

        if li.kind == "signature":
            text = apply_substitutions(li.main_text.strip())
            if not in_pstart:
                out.append("\\pstart")
                in_pstart = True
            out.append(text)
            i += 1
            continue

        # Regular text (text_only, margin_and_text, margin_only)
        if not in_pstart:
            out.append("\\pstart")
            in_pstart = True

        # Emit margin mark if this line starts a margin group
        if i in margin_at:
            out.append(f"\\margmark{{{margin_at[i]}}}%")

        # Get main text
        if li.kind == "margin_only":
            i += 1
            continue

        text = li.main_text
        if not text.strip():
            i += 1
            continue

        text = apply_substitutions(text)

        # If line is ONLY a \darueber command, merge with previous line
        if re.match(r'^\\darueber\{.*\}$', text.strip()):
            if out and not out[-1].startswith("%"):
                # Append to previous line (before its \ob/\ohb)
                prev = out[-1]
                if prev.endswith("\\ob"):
                    out[-1] = prev[:-3].rstrip() + " " + text.strip() + "\\ob"
                elif prev.endswith("\\ohb"):
                    out[-1] = prev[:-4].rstrip() + " " + text.strip() + "\\ohb"
                else:
                    out[-1] = prev.rstrip() + " " + text.strip()
                i += 1
                continue

        # Add line breaks (\ob / \ohb)
        boundary = _is_boundary(classified, i)
        if not boundary:
            if _line_ends_hyphenated(text):
                text = text.rstrip()[:-1] + "\\ohb"
            else:
                text = text.rstrip() + "\\ob"

        out.append(text)
        i += 1

    # Close any open \pstart
    if in_pstart:
        out.append("\\pend")

    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Special page handlers
# ---------------------------------------------------------------------------

def emit_title_page(page_num: str, lines: list[str]) -> str:
    """Special handler for page 002 (title page). Returns .tex content.
    This page has unique tabular structure that can't be auto-parsed."""
    # For now, return None to signal that the general pipeline should be used.
    # Title page will be handled in Phase 3.
    return None


def emit_cover_page(page_num: str, lines: list[str]) -> str:
    """Special handler for page 000 (cover). Returns .tex content.
    No \\pstart/\\pend here — main file wraps this page."""
    content_lines = [l.strip() for l in lines if l.strip()]
    out = []
    out.append(f"% Page {page_num} — Cover")
    out.append("")
    out.append("\\begin{center}")
    for cl in content_lines:
        cl = apply_substitutions(cl)
        out.append(f"\\Large {cl}\\\\[1em]")
    out.append("\\end{center}")
    out.append("\\pend")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Main conversion pipeline
# ---------------------------------------------------------------------------

def convert_page(md_path: str, dry_run: bool = False,
                 debug: bool = False) -> str | None:
    """Convert a single .md file to .tex content. Returns the tex string."""
    page_num = os.path.splitext(os.path.basename(md_path))[0]

    lines = extract_text_block(md_path)
    if not lines:
        print(f"  WARNING: {md_path} has no ```text block, skipping",
              file=sys.stderr)
        return None

    # Strip trailing empty lines
    while lines and not lines[-1].strip():
        lines.pop()

    if not any(l.strip() for l in lines):
        print(f"  WARNING: {md_path} has empty ```text block, skipping",
              file=sys.stderr)
        return None

    # Special pages
    if page_num == "002":
        # Title page: hand-crafted, preserve existing .tex file
        existing = os.path.join(PAGES_DIR, f"{page_num}.tex")
        if os.path.exists(existing):
            with open(existing, encoding="utf-8") as f:
                return f.read()
        return None

    if page_num == "000":
        return emit_cover_page(page_num, lines)

    # General pipeline
    page_str, page_idx = detect_page_number(lines)
    layout = analyze_layout(lines, page_idx)
    classified = classify_lines(lines, layout, page_idx)

    if debug:
        print(f"\n=== Page {page_num} (main_col={layout.main_col}, "
              f"margin={layout.has_margin_notes}, diary={layout.is_diary}) ===")
        for j, cl in enumerate(classified):
            print(f"  [{j:3d}] {cl.kind:20s} | M: {cl.margin_text!r:30s} "
                  f"| T: {cl.main_text!r}")

    return emit_page(page_num, classified, layout)


def discover_pages(single_page: str | None = None) -> list[str]:
    """Find .md files to convert."""
    if single_page:
        md = os.path.join(TRANSKRIPT_DIR, f"{single_page}.md")
        if not os.path.exists(md):
            print(f"ERROR: {md} not found", file=sys.stderr)
            sys.exit(1)
        return [md]

    # All NNN.md files (not in subdirectories)
    pattern = os.path.join(TRANSKRIPT_DIR, "[0-9][0-9][0-9].md")
    pages = sorted(glob.glob(pattern))
    if not pages:
        print(f"ERROR: No transcript files found in {TRANSKRIPT_DIR}",
              file=sys.stderr)
        sys.exit(1)
    return pages


def validate_nesting(tex_path: str) -> list[str]:
    r"""Check \pstart/\pend nesting in a .tex file. Returns list of errors.

    Convention: pages starting with prose don't emit \pstart — the main file
    provides it. So the first \pend may be "unmatched" within the file. We
    allow depth to dip to -1 once (for the external \pstart), but not further.
    """
    errors = []
    depth = 0
    external_pstart_used = False
    with open(tex_path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            for cmd in re.findall(r"\\(pstart|pend)\b", line):
                if cmd == "pstart":
                    depth += 1
                else:
                    depth -= 1
                    if depth < 0:
                        if not external_pstart_used:
                            # Allow one unmatched \pend for external \pstart
                            external_pstart_used = True
                            depth = 0
                        else:
                            errors.append(
                                f"{tex_path}:{i}: \\pend without matching \\pstart"
                            )
                            depth = 0
    # Allow depth == 1 at end: some pages (e.g., hand-crafted 002) leave
    # a \pstart open that the main file closes.
    if depth > 1:
        errors.append(f"{tex_path}: {depth} unclosed \\pstart at end of file")
    return errors


def validate_gold_standard() -> bool:
    """Compare generated output against gold-standard files."""
    if not os.path.isdir(GOLD_DIR):
        print(f"ERROR: Gold directory {GOLD_DIR} not found", file=sys.stderr)
        return False

    gold_files = sorted(glob.glob(os.path.join(GOLD_DIR, "*.tex")))
    if not gold_files:
        print("ERROR: No gold-standard files found", file=sys.stderr)
        return False

    all_pass = True
    for gold_file in gold_files:
        page = os.path.splitext(os.path.basename(gold_file))[0]
        md_path = os.path.join(TRANSKRIPT_DIR, f"{page}.md")
        if not os.path.exists(md_path):
            print(f"  SKIP {page}: no transcript file")
            continue

        generated = convert_page(md_path)
        if generated is None:
            print(f"  FAIL {page}: conversion returned None")
            all_pass = False
            continue

        with open(gold_file, encoding="utf-8") as f:
            gold_content = f.read()

        if generated.rstrip() == gold_content.rstrip():
            print(f"  PASS {page}")
        else:
            print(f"  FAIL {page}")
            diff = difflib.unified_diff(
                gold_content.splitlines(keepends=True),
                generated.splitlines(keepends=True),
                fromfile=f"gold/{page}.tex",
                tofile=f"generated/{page}.tex",
            )
            sys.stdout.writelines(diff)
            all_pass = False

    return all_pass


def main():
    parser = argparse.ArgumentParser(
        description="Convert MD transcripts to LaTeX pages")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would change without writing")
    parser.add_argument("--page", type=str,
                        help="Convert single page (e.g., 005)")
    parser.add_argument("--validate", action="store_true",
                        help="Compare output against gold-standard files")
    parser.add_argument("--debug", action="store_true",
                        help="Print classified lines for debugging")
    args = parser.parse_args()

    if args.validate:
        success = validate_gold_standard()
        # Also check \pstart/\pend nesting in all generated .tex files
        tex_files = sorted(glob.glob(os.path.join(PAGES_DIR, "*.tex")))
        nesting_errors = []
        for tf in tex_files:
            nesting_errors.extend(validate_nesting(tf))
        if nesting_errors:
            for err in nesting_errors:
                print(f"  NESTING: {err}")
            success = False
        else:
            print(f"  NESTING: {len(tex_files)} .tex files OK")
        sys.exit(0 if success else 1)

    pages = discover_pages(args.page)
    os.makedirs(PAGES_DIR, exist_ok=True)

    converted = 0
    skipped = 0
    for md_path in pages:
        page_num = os.path.splitext(os.path.basename(md_path))[0]
        tex_content = convert_page(md_path, dry_run=args.dry_run,
                                   debug=args.debug)

        if tex_content is None:
            skipped += 1
            continue

        tex_path = os.path.join(PAGES_DIR, f"{page_num}.tex")

        if args.dry_run:
            if os.path.exists(tex_path):
                with open(tex_path, encoding="utf-8") as f:
                    old = f.read()
                if old.rstrip() != tex_content.rstrip():
                    print(f"  WOULD UPDATE {tex_path}")
                else:
                    print(f"  UNCHANGED    {tex_path}")
            else:
                print(f"  WOULD CREATE {tex_path}")
        else:
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(tex_content)
            print(f"  Wrote {tex_path}")

        converted += 1

    print(f"\n{converted} pages converted, {skipped} skipped")


if __name__ == "__main__":
    main()
