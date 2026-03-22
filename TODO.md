# TODO

## Planned Features

- [ ] **Annotation footnotes (configurable):** Extract Hinweise and Analyse sections from `Transkript/NNN.md` and convert them to `\hinweise{...}` / `\analyse{...}` LaTeX commands in the generated `.tex` page files. The `\annotations` toggle in `preamble.tex` already supports showing/hiding these as footnotes or endnotes. Implementation: add a `--annotations` flag to `LaTeX/md2tex.py`.

## Ongoing: Gold Standard Review for md2tex.py

The `md2tex.py` converter uses spatial heuristics to classify lines (headings, margin notes, verse, signatures, etc.). Because every page in the Schulchronik has unique layout quirks, **new page types will surface that the heuristic parser cannot handle correctly**. This requires continuous review:

- [ ] **After every batch of new pages:** Run `python3 LaTeX/md2tex.py --dry-run` and spot-check the generated `.tex` files against the original scans. Look for:
  - Headings misclassified as verse (or vice versa)
  - Margin notes incorrectly grouped or missed
  - Signature blocks rendered as prose
  - Diary-format dates not detected
  - Continuation lines from previous pages misclassified
- [ ] **When a new layout pattern is found:** Add a representative page to `LaTeX/gold/` as a regression reference and adjust the heuristic parser in `md2tex.py` to handle it. Then verify all existing gold pages still pass with `python3 LaTeX/md2tex.py --validate`.
- **Known heuristic limitations discovered so far:**
  - Heading detection requires the heading to be preceded by a blank line and either followed by a blank line OR centered past `main_col + 4`. Pages where headings run directly into text without spacing need the centering heuristic.
  - The `_is_heading_text()` function uses a list of known patterns (e.g., "Revision", "Das Jahr NNNN"). New heading forms need to be added as encountered.
  - Verse detection is purely indent-based (indent >= main_col + 4). First-line continuations from a previous page that happen to be indented can be misclassified as verse.
  - Abbreviation detection uses a fixed list (`_ABBREVIATIONS`). Words like "Lud." (Ludovicus) can be ambiguous — sometimes abbreviation, sometimes sentence-ending period.
  - The `"` ditto mark is not auto-converted in prose; it's only meaningful in title page / diary contexts. Cross-page closing quotes (`"`) are left as-is.
  - Diary-format pages (dates in left margin) are detected by a date-pattern ratio heuristic; unusual date formats may be missed.
- **Current gold-standard pages:** 002, 005, 012, 015, 020 (in `LaTeX/gold/` once Phase 4 is completed).

## Transcript Structure Fixes

- [ ] **Fix pre-pipeline transcripts (000, 003, 004, 008-010):** These early pages lack the standard `### Hinweise zur Transkription` and `### Historische und sprachliche Analyse` sections. They need to be re-transcribed through the triple-LLM pipeline or manually reformatted to pass `Scripts/validate_transcripts.py`.
- [ ] **Fix recent incomplete transcripts (051-057):** These pages also lack standard sections — likely added before the structural convention was fully established. Reformat or re-merge.
- [ ] **Update gold/020.tex:** The gold-standard file for page 020 is outdated (based on an older, less accurate transcription). Update it to match the current merged transcript.

## Research Tasks

- [ ] **Robust layout detection for MD→LaTeX conversion:** The current `md2tex.py` conversion relies on spatial heuristics (column positions, indentation patterns) to detect margin notes, headings, and main text in the `` ```text `` blocks of `Transkript/NNN.md`. This layout is produced by Claude during the merge step but is an implicit convention — not a formal contract. If the merge format drifts over time, the heuristic parser may break silently. Research directions:
  - **Semantic markers in merge output:** Have Claude emit lightweight markup during the merge step (e.g., `<!-- margin: ... -->`, `[margin:]...[/margin]`, or similar) so the converter can parse structure deterministically without spatial heuristics.
  - **Layout descriptor:** Add structured metadata (YAML frontmatter or sidecar JSON) per page during merge, describing margin note positions, heading types, verse blocks, etc.
  - **Hybrid approach:** Keep the spatial heuristic parser but add a validation/confidence pass that flags pages where layout detection is uncertain, requiring human review.
  - **Contract in CLAUDE.md:** Document the exact spatial layout conventions as a formal spec in CLAUDE.md so the merge step and the converter share a stable contract.

## Known LaTeX Compilation Issues

- [ ] **`\darueber` + reledmac interaction (page 010):** The `\darueber` command (textsuperscript annotation) triggers "Missing number" and "Illegal unit of measure" errors when used with reledmac line tracking. The PDF still compiles (nonstopmode) but these errors should be resolved. Possible fix: redefine `\darueber` to be reledmac-aware, or use a different annotation mechanism.
- [ ] **Margin dates treated as inline text (page 057 and similar):** When margin dates like „15. Mai 1921" and „24. Mai" appear at the start of a line with body text following, md2tex.py's heuristic sometimes fails to detect them as margin notes and instead emits them as inline body text. This is a known limitation of the spatial column detection — the margin/body gap may be too small for the heuristic to trigger `\margmark`. Affects pages with date-margin diary-like layouts where the main column starts at a low column position.
- [ ] **Title page (002) automation:** The title page has unique tabular structure with ditto marks, margin notes, and centered blocks. Currently preserved as a hand-crafted `.tex` file. Could be automated with a dedicated parser, but low priority since this page rarely changes.

## Future Ideas

- [ ] **Scan + Transcription side-by-side book:** Generate a publication-quality "book" format where each spread shows the original scan on the left page and the transcription (with Hinweise/Analyse remarks and commentary) on the right page. This would serve as a complete reference edition of the Schulchronik.
