# Schulchronik [Sefferweich](https://www.sefferweich.de) — Digitale Transkription

In der Gemeinde [Sefferweich](https://www.sefferweich.de) (Eifelkreis Bitburg-Prüm) existiert eine handgeschriebene Schulchronik aus dem 19. und 20. Jahrhundert. Generationen von Lehrern haben darin das Leben in den Dörfern [Sefferweich](https://www.sefferweich.de), Seffern, Bickendorf und Malbergweich festgehalten — von Schulalltag und Wetter über Ernten und Epidemien bis hin zu Kriegen und politischen Umbrüchen. Die ältesten Einträge stammen aus dem Jahr 1851.

Die Chronik ist in *Kurrentschrift* und *Sütterlin* verfasst, alten deutschen Handschriften, die heute kaum noch jemand lesen kann. Um den Inhalt zugänglich zu machen, wird der Text mit Hilfe von künstlicher Intelligenz entziffert und in eine moderne, lesbare Form gebracht.

## Wie funktioniert das?

Als Vorlage dient eine Fotokopie der Originalchronik. Die einzelnen Seiten werden mit [Google Fotoscanner](https://www.google.com/intl/de/photos/scan/) digitalisiert und dann von **drei verschiedenen KI-Systemen** unabhängig voneinander gelesen (Claude von Anthropic, Gemini von Google und Codex von OpenAI). Jedes System liefert seine eigene Lesung — und wie bei drei unabhängigen Zeugen lassen sich die Ergebnisse anschließend vergleichen: Wo alle drei übereinstimmen, ist der Text so gut wie sicher. Wo sie voneinander abweichen, wird anhand des Originalfotos geprüft, welche Lesung am plausibelsten ist. Stellen, die auch nach diesem Abgleich unklar bleiben, werden als unsicher markiert.

Aus den zusammengeführten Ergebnissen entsteht am Ende ein durchsuchbarer Gesamttext sowie eine druckfertige PDF-Ausgabe.

**[→ Aktuelle PDF-Version der Schulchronik herunterladen](https://christianbaumann.github.io/schulchronik-sefferweich/schulchronik.pdf)**
Die PDF wird bei jedem neuen Transkriptionsfortschritt automatisch aktualisiert.

Das Projekt ist ein Vorhaben des **Arbeitskreises Geschichte [Sefferweich](https://www.sefferweich.de)**.

## Technische Details

### Projektstruktur

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

### Pipeline

1. **Scan-Vorbereitung** — Rohfotos werden sortiert, nummeriert und in `Scans/` abgelegt.
2. **Triple-LLM-Transkription** — Jede Seite wird unabhängig von Claude, Gemini und Codex transkribiert.
3. **3-Wege-Merge** — Wortweiser Abgleich aller drei Lesungen mit Plausibilitätsprüfung am Scan.
4. **Konsolidierung** — Aus den zusammengeführten Markdown-Dateien wird `Transkript.txt` erzeugt.
5. **LaTeX-Ausgabe** — Automatische Konvertierung zu LaTeX; PDF-Erzeugung via GitHub Actions.

Details zu Pipeline, Transkriptionskonventionen und Merge-Verfahren: siehe [CLAUDE.md](CLAUDE.md).
Details zur LaTeX-Pipeline: siehe [LaTeX.md](LaTeX.md).

### Fortschritt

- **Umfang:** 110 Seiten (scannen der Chronik ist in Arbeit)
- **Claude-Transkriptionen:** 005–044
- **Gemini-Transkriptionen:** 005–014, 021–028, 031–039
- **Codex-Transkriptionen:** 005–006, 011–012, 021–022, 036–038
- **3-Wege-Merges:** 005–006, 011–012, 017, 021–022, 036–038

Aktuelle Merge-Statistiken: siehe [merge_report.md](merge_report.md).

> **Hinweis zum aktuellen Stand:** Dieses Projekt befindet sich in aktiver Bearbeitung. Die drei eingesetzten KI-Systeme (Claude, Gemini, Codex) unterscheiden sich deutlich in ihrer Fähigkeit, Kurrentschrift zu entziffern — manche liefern sehr gute Ergebnisse, andere haben noch erhebliche Schwächen. Da die Transkription pro KI unterschiedlich weit fortgeschritten ist, kann es vorkommen, dass für eine bestimmte Seite bisher nur die Lesung des schwächsten Systems in der zusammengeführten Fassung steht. Die Qualität einzelner Seiten kann daher derzeit noch stark schwanken. Mit jedem weiteren abgeschlossenen Transkriptionsdurchlauf und dem anschließenden 3-Wege-Abgleich verbessert sich die Gesamtqualität spürbar.

### Lokaler Build (LaTeX → PDF)

```bash
cd latex && make pdf
```

Voraussetzung: LuaLaTeX mit `reledmac`-Paket. Die PDF wird auch automatisch per GitHub Actions bei jedem Push erzeugt.

## Lizenz

Dieses Projekt dient der lokalen Geschichtsforschung. Die Originalscans sind Eigentum der Gemeinde bzw. des Arbeitskreises Geschichte [Sefferweich](https://www.sefferweich.de).
