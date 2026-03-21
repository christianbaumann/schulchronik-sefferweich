# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains the transcription of the historical "Schulchronik" (School Chronicle) of Sefferweich, Kreis Bitburg, spanning from 1851 through the mid-20th century. The chronicle is handwritten in Sütterlin/Kurrent script. The project digitizes these scans into structured text.

## Three-Phase Transcription Pipeline

### Phase 1: Preparation (`Scans/raw/` → `Scans/`)
- Raw photos in `Scans/raw/` are sorted by filename (timestamp-based ordering corresponds to page order).
- Files are renamed to sequential format (`011.jpg`, `012.jpg`, etc.) and placed in `Scans/`.
- `Scans/raw/` file index 0 corresponds to page 011.
- **Inverted scans:** If a scan is upside down (180° rotated), rotate the source file first (e.g., using `sips --rotate 180`), then re-copy to `Scans/` and re-transcribe. Do not attempt to transcribe inverted scans — rotate first.
- After copying, processed raw files are moved to `Scans/raw/done/`.
- The mapping from numbered scan to original raw filename is kept in `Scans/raw_mapping.json`. **Keep this file updated** when adding new pages.

### Phase 2: Triple-LLM Transcription (`Scans/` → `Transkript/`)

Every page is independently transcribed by **three LLMs** (Claude, Gemini, Codex), then merged by Claude into a definitive result using cautious 3-way voting with sanity checks.

**Exception:** Pages 002–004 currently retain their original Gemini-only transcripts (scans now available — will be re-transcribed in the triple-LLM pipeline).

#### Folder Structure
```
Transkript/
├── claude/NNN.md    # Claude's raw transcription (005–054 done, 055–110 in progress)
├── gemini/NNN.md    # Gemini's raw transcription (005–014, 021–028, 031–039 done)
├── codex/NNN.md     # Codex's raw transcription (005–006, 011–012, 021–022, 036–038 done)
├── NNN.md           # Merged final transcript (002–044 exist; 005–006, 011–012, 021–022, 036–038 are proper 3-way merges)
└── ...
```

Raw subfolders (`claude/`, `gemini/`, `codex/`) store **verbatim LLM output** — no reformatting.

#### Phase 2a: Claude Transcription (`Scans/` → `Transkript/claude/`)
- Claude reads each scan and produces a full transcription in standard format.
- Use subagents to parallelize.

#### Phase 2b: Gemini Transcription (`Scans/` → `Transkript/gemini/`)
- **Gemini CLI invocation (isolated):** Copy the scan to `/tmp/`, then invoke Gemini **from `/tmp/`** with sandbox flags to prevent it from reading project files:
  ```bash
  cp Scans/NNN.jpg /tmp/gemini_scan_NNN.jpg && cd /tmp && gemini -s --approval-mode plan -m gemini-2.5-pro -p "Transcribe the text in the image as Markdown. Try to preserve the layout. The language is German. The script is Kurrent (old German handwriting). Add transcription notes at the beginning and historical explanations at the end. Do NOT write any files — only output the text. @/tmp/gemini_scan_NNN.jpg" -o text
  ```
- **Isolation flags:**
  - `cd /tmp` — sets CWD so `-s` restricts file reads to `/tmp/` only
  - `-s` — sandbox mode: restricts `read_file`, `list_directory`, `glob`, `grep_search` to CWD
  - `--approval-mode plan` — removes `run_shell_command` (no shell escape) and `web_fetch`
  - `-o text` output is unaffected by write restrictions
- **Important:** Always copy the scan to `/tmp/` first. The combination of `cd /tmp` + `-s` + `--approval-mode plan` ensures Gemini can only read files in `/tmp/` and cannot execute shell commands. Also explicitly instruct Gemini not to write files (it sometimes tries to use write_file tools and fails).
- Timeout: 5 minutes per call.

#### Phase 2c: Codex Transcription (`Scans/` → `Transkript/codex/`)
- **Codex CLI invocation (isolated):** Clean leftover temp files, create a unique temp directory with a disposable git repo, copy only the scan, and run Codex from there:
  ```bash
  rm -f /tmp/codex_*.md /tmp/gemini_scan_*.jpg
  CODEX_DIR=$(mktemp -d /tmp/codex_XXXXXXXX) && cd "$CODEX_DIR" && git init --quiet
  cp Scans/NNN.jpg "$CODEX_DIR/scan.jpg"
  cd "$CODEX_DIR" && codex exec -i scan.jpg -m gpt-5.4 -s read-only --ephemeral "Transcribe the text in the image scan.jpg as Markdown. Use ONLY your built-in vision capability — do NOT use OCR, Tesseract, or any external tools. Try to preserve the layout. The language is German. The script is Kurrent (old German handwriting). Add transcription notes at the beginning and historical explanations at the end. Do NOT read any files other than scan.jpg and do NOT run any shell commands." -o /tmp/codex_NNN.md
  rm -rf "$CODEX_DIR"
  ```
- **Isolation strategy** (Codex `read-only` sandbox cannot restrict reads — it only restricts writes):
  1. **Pre-run cleanup:** `rm -f /tmp/codex_*.md /tmp/gemini_scan_*.jpg` removes all leftover artifacts that Codex could read
  2. **Unique temp dir:** `mktemp -d` prevents reuse of a fixed directory that might accumulate files across runs
  3. **Prompt instruction:** Explicit "Do NOT read any files other than scan.jpg" as defense-in-depth
  4. **Post-run cleanup:** `rm -rf "$CODEX_DIR"` removes the disposable git repo
- **Important:** Codex requires a git repo. The pre-run cleanup is critical — without it, Codex reads `/tmp/codex_*.md` files from previous runs and produces contaminated output (confirmed on page 041).
- Timeout: 5 minutes per call.

#### Parallelization Strategy
- **Only one transcription process per LLM at a time.** Do not run multiple Claude subagents, Gemini calls, or Codex calls concurrently.
- **Different LLMs can run in parallel** — one Claude + one Gemini + one Codex at the same time is fine (different providers).
- Process pages sequentially within each LLM stream.

#### Phase 2d: 3-Way Merge (`claude/ + gemini/ + codex/` → `Transkript/`)
- **Codex reliability warning (Kurrent):** Codex/GPT-5.4 consistently hallucinates on Kurrent handwriting — it fabricates entirely unrelated documents instead of reading the actual scan. During merges, be extra suspicious of Codex results. When in doubt, **Codex loses**. Only trust Codex readings when independently confirmed by at least one other LLM. Never let a Codex-only reading override Claude or Gemini consensus.
- Claude reads all three raw transcriptions + the scan, performs word-by-word 3-way comparison using Tiers 0–8:
  - **Tier 0:** 3-way agreement → accept
  - **Tier 1:** 2-of-3 majority → sanity check (real word? context fit? dissenter better? Sütterlin confusion pair?) → accept or reject. **If Codex is the majority partner on a Kurrent page, verify extra carefully against the scan.**
  - **Tiers 2–6:** Handle uncertainty markers, real-word vs. non-word, confusion matrix, layout, hallucination
  - **Tier 7:** Merge notes/analysis from all three into Hinweise and Analyse sections
  - **Tier 8:** Irreconcilable conflicts → flag in Hinweise with `**Abweichende Lesarten:**`
- Writes merged `Transkript/NNN.md` in standard format.
- Updates `merge_report.md` with per-page statistics.

#### Merge Report
- `merge_report.md` (project root) tracks per-page 3-way merge statistics and human review flags.
- **Language:** `merge_report.md` is written in German.
- **Update frequency:** `merge_report.md` MUST be updated with every commit — at minimum: new merge table rows, Phase-4-Status table, and rate-limit log entries.
- Pages where confidence is low are flagged for human review in both the merge report and the Hinweise section.

#### Rate Limit Handling
- Check output after each Gemini/Codex call for "Rate Limit" or suspiciously short output (< 50 chars).
- On trigger: **HALT all processing** (including other models). Parse the wait time from the error response and sleep for that duration.
- If no wait time is provided, fall back to probing at 10-minute intervals.
- Log all rate limit events in `merge_report.md` Rate Limit Log section.

#### Required structure of each merged `.md` file:
  1. **Hinweise zur Transkription** — issues, hard-to-read passages, contradictions. Stick to factual observations only; do not add advisory comments like "hier ist eine Überprüfung ratsam" or similar recommendations. Include 1-3 German-language web links per bullet where applicable — not only for historical facts (dates, persons, events) but also for uncommon/archaic knowledge (old units of measurement, forgotten customs, obsolete terms, etc.).
  2. **Transcription block** — inside a `` ```text `` code block to preserve spatial layout (marginalia, indentations).
  3. **Historische und sprachliche Analyse** (preceded by `***`) — fact-checked annotations (100% accuracy required), 2-3 web links to reliable German sources, linguistic explanations for archaic terms.
- **Continuity check:** Verify that the first sentence of a new page continues the last sentence of the previous page.

### Workflow
- **Always start with the lowest page number not yet transcribed** for each LLM stream.
- **After EVERY saved LLM transcription:** (1) update the merged transcript `Transkript/NNN.md` for that page, (2) validate and generate LaTeX (see below), (3) fully regenerate `Transkript.txt`, (4) **commit, pull (rebase), and push immediately**. No exceptions. **Do NOT skip the merge update** even if the new transcript "confirms" an existing one — a 2-way or 3-way merge always produces a better result than a single-LLM transcript.
- **Git push rule:** ALWAYS run `git pull --rebase` before `git push`. A CI workflow auto-generates LaTeX files and pushes to the same branch, so the remote may have new commits at any time. Failing to pull first causes rejected pushes and wastes time.
- **Updating merged transcripts (`Transkript/NNN.md`):** Whenever a new raw LLM transcript is saved, update the corresponding merged file:
  - **3 LLMs available:** Perform proper 3-way merge (Tiers 0–8, read scan + all 3 transcripts).
  - **2 LLMs available:** Perform 2-way comparison with scan verification.
  - **1 LLM available:** Use that transcript as the merged file (reformat to standard merge structure if needed).
  - The merged file always reflects the **best available data** at any point in time.
- **Regenerating `Transkript.txt`:** Rebuild from scratch every time using `Transkript/NNN.md` (merged files only). Never append — always regenerate the full file.
- **Progress output:** Give detailed status updates: which page is being read, transcribed, or written. Announce each sub-task (e.g., "Reading scan 016...", "Writing Transkript/016.md...", "Regenerating Transkript.txt...", "Committing...").
- **LaTeX validation and override:** After updating a merged transcript, run `python3 LaTeX/md2tex.py --page NNN`. Read the generated `LaTeX/pages/NNN.tex` and check for significant deviations:
  - **Missing content** — text in the .md not present in the .tex (e.g., second text block dropped, year heading consumed as page number).
  - **Wrong structural element** — content classified as the wrong LaTeX construct (e.g., name → `\abschnitt`, prose → `\begin{verse}`, date → heading).
  - **Broken `\pstart`/`\pend` nesting** — spurious or missing paragraph boundaries from misclassification.
  - **Incorrect margin attribution** — margin text in body or body text in margin.
  - If a significant deviation is found: write the corrected `LaTeX/pages/NNN.tex` directly, update `LaTeX/gold/NNN.tex` if this represents a new pattern, and log the override in `merge_report.md`.
  - If no significant deviation: accept md2tex.py's output as-is.
  - Minor differences (whitespace, abbreviation spacing, `\ob` at paragraph boundaries) do NOT warrant override.
- **Gold standards (`LaTeX/gold/`):** Can be updated or added when Claude overrides md2tex.py on a page that represents a new layout pattern. Gold files serve as regression anchors for `md2tex.py --validate`.
- **Update CLAUDE.md after every relevant workflow or structural change.**

### Phase 3: Consolidation (`Transkript/` → `Transkript.txt`)
- Extract text from inside the `` ```text `` code blocks only (strip AI wrapper/metadata).
- Separate page sections with `------------`.
- Output is `Transkript.txt` — a seamless plain-text reconstruction of the entire chronicle.

## Script Type (Kurrent vs. Sütterlin)

- The chronicle is written in **Kurrent** (deutsche Kurrentschrift), not Sütterlin. Sütterlin was only introduced in 1911 and the chronicle predates this.
- **Do not include comments** about whether the script is Sütterlin or Kurrent in any transcript file (raw or merged). This applies to Hinweise sections, Analyse sections, and Codex/Gemini prompts.
- **Prompts to Gemini/Codex** should say "Schrift ist Kurrent" (not "Sütterlin oder Kurrent").
- **Claude sub-agent prompts** should say "script is Kurrent" (not "Sütterlin/Kurrent").

## Transcription Conventions

- `"` (double quotes) = repetition marks for words like "Fortgesetzt von" or "Lehrer".
- `[?]` = illegible or unclear text. Use sparingly: only when genuinely unsure (<80% confidence). If the word can be reasonably guessed from context, write it without `[?]`.
- `[darüber: ...]` = text written above the line as a correction/addition.
- `~~text~~` = struck-through text in the original.
- Marginal notes are placed at the left side of the text block, matching the original layout.
- **Embedded images** (e.g., Totenzettel, photos, documents): Extract each image individually into `Scans/embedded/` with naming `{page}_{index}.jpg` (e.g., `031_1.jpg`, `031_2.jpg`). Use Python/Pillow for precise cropping. **Quality-check** each extracted image by reading it back. Link from the transcript using `![description](../Scans/embedded/031_1.jpg)`.

## LaTeX Publishing Pipeline

See **[LaTeX.md](LaTeX.md)** for the complete LaTeX setup: build instructions, custom commands, layout toggles, lessons learned, and the Markdown→LaTeX conversion guide.

## Key Locations

- Historical context: villages Sefferweich, Seffern, Bickendorf, Malbergweich (all Kreis Bitburg/Eifel region).
- **No links needed for villages/towns within ~15 km of Sefferweich** (e.g., Fließem, Dudeldorf, Bickendorf, Schleid, Heilenbach, Idenheim, Schönecken, etc.) — these are local and need no Wikipedia reference.
- The Gemini conversation used during initial transcription is linked in `gemini_link.txt`.
