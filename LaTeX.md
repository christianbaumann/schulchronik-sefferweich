# LaTeX Publishing Pipeline

This document covers the LaTeX setup for producing faithful-layout PDF output from the Schulchronik transcripts. For the research background (toolchain evaluation, rejected alternatives, font recommendations), see `Docs/agents/research/2026-03-20-latex-multi-format-publishing.md`.

## Architecture

```
Transkript/*.md ──► md2tex.py ──► LaTeX/pages/*.tex ──► generate_main.py ──► lualatex ──► PDF
                   (automated)     (LaTeX source)       (schulchronik.tex)    (reledmac)
```

The full pipeline runs automatically via GitHub Actions on every push to `main`.

Future: HTML via `make4ht`/`lwarp`, EPUB via `tex4ebook` (deferred until PDF template is validated).

## Directory Structure

```
LaTeX/
├── schulchronik.tex          # Main document (\input commands)
├── preamble.tex              # Package loading, custom commands, toggles
├── pages/
│   └── NNN.tex               # One file per manuscript page
├── annotations/
│   ├── NNN-hinweise.tex      # Hinweise per page (optional inclusion)
│   └── NNN-analyse.tex       # Analyse per page (optional inclusion)
└── Makefile                  # Build targets: pdf, clean
```

## Build

```bash
cd LaTeX && make pdf          # two-pass lualatex
cd LaTeX && make clean        # remove auxiliary files
```

Requires: LuaLaTeX (TeX Live), packages `reledmac`, `ebgaramond`, `csquotes`, `fontspec`, `geometry`, `ulem`, `babel-german`, `bigfoot` (provides `suffix.sty`), `xargs`, `xstring`, `ragged2e`, `xkeyval`.

## Core Packages and Why

| Package | Purpose |
|---|---|
| `scrbook` (KOMA-Script) | Document class; flexible page geometry, `oneside` for consistent margins |
| `reledmac` | Left-margin notes (`\ledleftnote{}`), scholarly critical edition features |
| `fontspec` | Font loading under LuaLaTeX; EB Garamond as main font |
| `geometry` | Page layout: `left=5cm` (wide left margin for margin notes) |
| `babel[ngerman]` | German typographic conventions |

## Layout Toggles

All configurable via boolean flags in `preamble.tex`:

| Toggle | Default | Effect when on |
|---|---|---|
| `\originallbreaks` | off (LaTeX reflows) | Preserve exact manuscript line breaks |
| `\originalpagebreaks` | off (decorative separator) | Force page break at manuscript boundaries |
| `\frakturheadings` | off (EB Garamond) | UnifrakturMaguntia for major headings |
| `\annotations` | on (footnotes visible) | Show Hinweise + Analyse as footnotes |
| `\endnotes` | off (per-page footnotes) | Collect annotations as endnotes |

## Custom Commands

| Command | Purpose | Example |
|---|---|---|
| `\seite{N}` | Manuscript page marker (structural only, no visible output), opens `\pstart` | `\seite{12}` |
| `\margmark{text}` | Left margin note | `\margmark{Die Schule.}` |
| `\ueberschrift{text}` | Centered heading in italics (unified style for all headings) | `\ueberschrift{Das Jahr 1887}` |
| `\jahresueberschrift{text}` | Alias for `\ueberschrift` | `\jahresueberschrift{Das Jahr 1887}` |
| `\abschnitt{text}` | Alias for `\ueberschrift` | `\abschnitt{Die Schule}` |
| `\titelseite{text}` | Title with underline rule | `\titelseite{Schul\,--\,Chronik}` |
| `\ob` | Original line break (space in reflow, `\\` in original-break mode) | `Schleid u\ob Heilenbach` |
| `\ohb` | Original hyphenated break (nothing in reflow, `-\\` in original-break mode) | `An\ohb siedlung` → "Ansiedlung" |
| `\originalpagebreak` | Page break or decorative separator between manuscript pages | |
| `\ditto` | Literal `"` repetition mark | `\ditto{} Alter.` |
| `\unsicher` | Uncertainty marker `[?]` | `Abende was\unsicher` |
| `\darueber{text}` | Interlinear correction | `\darueber{6° 32'}` |
| `\trenner` | Horizontal rule (decorative separator) | |
| `\hinweise{text}` | Transcription notes (configurable footnote/endnote/hidden) | |
| `\analyse{text}` | Historical analysis (configurable footnote/endnote/hidden) | |

## Key Lessons Learned

### Heading Style

All headings (year headings like "Das Jahr 1887", section headings like "Die Schule", "II. Alter") use the **same font style**: centered, `\Large\textit` (italic). There is one unified `\ueberschrift` command; `\jahresueberschrift` and `\abschnitt` are aliases. **Omit trailing periods** from heading text.

### Babel `"` Shorthand Conflict

German babel interprets `"` as a shorthand prefix: `"A` → `Ä`, `"o` → `ö`, etc. This breaks the Schulchronik convention where `"` is a repetition/ditto mark. **Solution:** Disable babel shorthands and use `\ditto` command for repetition marks, `\enquote{}` (csquotes) for actual quotation marks.

```latex
\addto\extrasgerman{\languageshorthands{none}}
\addto\extrasngerman{\languageshorthands{none}}
```

### `oneside` vs. `twoside`

With `twoside`, margins flip on even pages: the left margin (where margin notes live) becomes the narrow right margin, causing notes to be clipped at the page edge. **Solution:** Use `oneside` so margins are consistent on every page. The original manuscript is single-sided.

### `\ob` Spacing in Reflow Mode

When `\ob` (original line break) is inactive (reflow mode), it must produce an explicit `\space` — otherwise words at line boundaries run together ("Schleid uHeilenbach" instead of "Schleid u Heilenbach"). A TeX newline after a macro does NOT reliably produce a space.

```latex
\newcommand{\ob}{\iforiginallbreaks\\\else\space\fi}
```

### `\ob` vs. `\ohb` for Hyphenated Words

When the original manuscript breaks a word across lines with a hyphen (e.g., "An-" / "siedlung"), `\ob` would produce a spurious space+hyphen in reflow mode ("An- siedlung"). **Solution:** Use `\ohb` (original hyphenated break) which produces nothing in reflow mode (word rejoins: "Ansiedlung") and `-\\` in original-break mode.

```latex
\newcommand{\ohb}{\iforiginallbreaks-\\\fi}
% Source: An\ohb siedlung  →  reflow: "Ansiedlung"  |  original: "An-\\"
```

### reledmac Line Numbering

`reledmac` enables line numbering by default. The Schulchronik has no line numbers in the original. Suppress them by pushing the first line number far away:

```latex
\firstlinenum{10000}
\linenumincrement{10000}
```

### reledmac `\pstart`/`\pend` Structure

Every text paragraph inside `\beginnumbering`/`\endnumbering` must be wrapped in `\pstart`/`\pend`. Heading commands (`\jahresueberschrift`, `\abschnitt`) must appear **between** `\pend` and `\pstart` — they do NOT manage paragraph boundaries themselves. The calling code (page file or main file) is responsible for closing `\pend` before and opening `\pstart` after each heading.

**Pattern for pages starting with a heading** (e.g., year heading):
```latex
% In main file: do NOT open \pstart before \input
\input{pages/015}

% In pages/015.tex:
\seite{15}
\jahresueberschrift{Das Jahr 1887.}
\pstart
Text content...
\pend
```

**Pattern for headings in the middle of a page:**
```latex
...text before heading...
\pend
\abschnitt{Die Schule.}
\pstart
...text after heading...
```

### Structured Content (Lists, Tables)

Not all manuscript content is prose. Structured content like the title page teacher list should use `tabular` environments with forced line breaks, not `\ob`. These structures must preserve their layout regardless of the `\originallbreaks` toggle.

### Page Numbering

Suppress automatic LaTeX page numbering with `\pagestyle{empty}`. The page numbers visible in the scans (e.g., "5", "12", "15") were added retrospectively and are **not part of the original chronicle** — do not render them. `\seite{N}` is a structural-only marker (no visible output).

### TeX Live Basic Installation

The basic TeX Live installation lacks many packages. Install missing ones via `tlmgr`. If the local TeX Live version is older than the remote repository, use the historic archive:

```bash
sudo tlmgr --repository https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/YYYY/tlnet-final install <package>
```

Key dependency chain for `reledmac`: requires `xargs`, `suffix` (in `bigfoot` package), `xstring`, `ragged2e`, `xkeyval`.

## Converting Markdown Transcripts to LaTeX

**Automated by `LaTeX/md2tex.py`** — run manually or via GitHub Actions.

```bash
python3 LaTeX/md2tex.py              # Convert all pages
python3 LaTeX/md2tex.py --page 005   # Convert single page
python3 LaTeX/md2tex.py --dry-run    # Show what would change
python3 LaTeX/md2tex.py --validate   # Compare against gold-standard files
python3 LaTeX/md2tex.py --debug      # Print line classification debug output
```

### Conversion Rules (applied by md2tex.py)

1. `\seite{N}` — structural marker from centered page number
2. Page-start headings: `\jahresueberschrift{...}` or `\abschnitt{...}` before `\pstart`
3. Prose-start pages: no `\pstart` (main file provides it)
4. Left-column text → `\margmark{text}` with `\\` for multi-line margins
5. Mid-page headings: `\pend` before, `\pstart` after
6. Line breaks: `\ob` (word boundary) or `\ohb` (hyphenated break); none on last line of paragraph
7. `[?]` → `\unsicher` (leading space consumed, `{}` added when followed by letters)
8. `[darüber: ...]` → `\darueber{...}`
9. `~~text~~` → `\sout{text}`
10. `„text"` → `\enquote{text}`
11. Abbreviation periods: `Joh. ` → `Joh.\ ` (prevents TeX sentence-end spacing)
12. Verse/poetry → `\pend` + `\begin{verse}...\end{verse}` + `\pstart`
13. End file with `\pend`

### Special Pages

- **Page 002 (title page):** Hand-crafted `.tex` preserved as-is (tabular structure with ditto marks)
- **Page 000 (cover):** Simple centered layout, auto-generated
- **Gold standard:** `LaTeX/gold/` contains reference `.tex` files for regression testing

## References

- [reledmac manual (PDF)](http://mirrors.ibiblio.org/CTAN/macros/latex/contrib/reledmac/reledmac.pdf)
- [reledmac sidenotes example](https://mirrors.mit.edu/CTAN/macros/latex2e/contrib/reledmac/examples/1-sidenotes.tex)
- [KOMA-Script scrbook documentation](https://ctan.org/pkg/koma-script)
- Research: `Docs/agents/research/2026-03-20-latex-multi-format-publishing.md`
- Plan: `Docs/agents/plans/2026-03-20-latex-prototype.md`
