# Schulchronik [Sefferweich](https://www.sefferweich.de) — Digitale Transkription

Transkription der historischen Schulchronik von [Sefferweich](https://www.sefferweich.de) (Eifelkreis Bitburg-Prüm), handschriftlich in deutscher Kurrentschrift verfasst, mit Einträgen ab 1851 bis Mitte des 20. Jahrhunderts.

## Über das Projekt

Die Schulchronik dokumentiert das dörfliche und schulische Leben der Gemeinden [Sefferweich](https://www.sefferweich.de), Seffern, Bickendorf und Malbergweich über rund 100 Jahre. Die handschriftlichen Originalseiten werden in einem mehrstufigen Verfahren mit Hilfe von drei KI-Modellen (Claude, Gemini, Codex) unabhängig transkribiert und anschließend per 3-Wege-Merge zu einem konsolidierten Ergebnis zusammengeführt.

Das Projekt ist ein Vorhaben des **Arbeitskreises Geschichte [Sefferweich](https://www.sefferweich.de)**.

## Projektstruktur

```
Scans/                  Digitalisierte Originalseiten (JPG)
Transkript/             Zusammengeführte Transkripte (Markdown)
  ├── claude/           Rohtranskriptionen — Claude
  ├── gemini/           Rohtranskriptionen — Gemini
  └── codex/            Rohtranskriptionen — Codex
Transkript.txt          Gesamttranskript (Reintext)
latex/                  LaTeX-Quellen für PDF-Ausgabe
merge_report.md         Merge-Statistiken und Prüfhinweise
```

## Pipeline

1. **Scan-Vorbereitung** — Rohfotos werden sortiert, nummeriert und in `Scans/` abgelegt.
2. **Triple-LLM-Transkription** — Jede Seite wird unabhängig von Claude, Gemini und Codex transkribiert.
3. **3-Wege-Merge** — Wortweiser Abgleich aller drei Lesungen mit Plausibilitätsprüfung am Scan.
4. **Konsolidierung** — Aus den zusammengeführten Markdown-Dateien wird `Transkript.txt` erzeugt.
5. **LaTeX-Ausgabe** — Automatische Konvertierung zu LaTeX; PDF-Erzeugung via GitHub Actions.

Details zu Pipeline, Transkriptionskonventionen und Merge-Verfahren: siehe [CLAUDE.md](CLAUDE.md).
Details zur LaTeX-Pipeline: siehe [LaTeX.md](LaTeX.md).

## Fortschritt

- **Umfang:** 110 Seiten (scannen der Chronik ist in Arbeit)
- **Claude-Transkriptionen:** 005–044
- **Gemini-Transkriptionen:** 005–014, 021–028, 031–039
- **Codex-Transkriptionen:** 005–006, 011–012, 021–022, 036–038
- **3-Wege-Merges:** 005–006, 011–012, 017, 021–022, 036–038

Aktuelle Merge-Statistiken: siehe [merge_report.md](merge_report.md).

## Lokaler Build (LaTeX → PDF)

```bash
cd latex && make pdf
```

Voraussetzung: LuaLaTeX mit `reledmac`-Paket. Die PDF wird auch automatisch per GitHub Actions bei jedem Push erzeugt.

## Lizenz

Dieses Projekt dient der lokalen Geschichtsforschung. Die Originalscans sind Eigentum der Gemeinde bzw. des Arbeitskreises Geschichte [Sefferweich](https://www.sefferweich.de).
