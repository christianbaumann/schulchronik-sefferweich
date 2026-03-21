# Merge-Bericht

## Begriffserklärung

**3-Wege-Übereinstimmung** — Alle drei LLMs (Claude, Gemini, Codex) liefern dieselbe Lesung. Höchste Konfidenz.

**2-von-3 Akzeptiert** — Zwei LLMs stimmen überein und die Mehrheitslesung besteht die Plausibilitätsprüfung (echtes Wort, Kontextpassung, keine Kurrent-Verwechslung).

**2-von-3 Abgelehnt** — Zwei LLMs stimmen überein, aber die Mehrheitslesung fällt bei der Plausibilitätsprüfung durch (z. B. kein sinnvolles Wort, Kontextbruch). Die abweichende Lesung oder eine manuelle Korrektur wird bevorzugt.

**Alle Abweichend** — Alle drei LLMs liefern unterschiedliche Lesungen. Entscheidung erfolgt durch Scan-Abgleich und Kontextanalyse.

**Manuelle Prüfung** — Anzahl der Stellen, die für eine menschliche Überprüfung markiert wurden (z. B. irreconcilable Lesarten, sehr unsichere Passagen).

| Seite | 3-Wege-Übereinstimmung | 2-von-3 Akzeptiert | 2-von-3 Abgelehnt | Alle Abweichend | Manuelle Prüfung | Anmerkungen |
|-------|------------------------|--------------------|--------------------|-----------------|------------------|-------------|
| 005   | ~45%                   | ~40%               | ~5%                | ~10%            | 2                | Claude divergiert stark von Gemini/Codex; „Filialen" (2-von-3) statt „Pfarren"; Gedichtzeile 1 irreconcilable; interlineare „[nicht]"-Einfügung |
| 006   | ~45%                   | ~40%               | ~5%                | ~10%            | 1                | Claude bei Gedichtzeilen und Grabzerstörungs-Passage abweichend; Ortsnamenformen (Wrivic, Uwriche etc.) unsicher |
| 011   | ~15%                   | ~55%               | ~5%                | ~25%            | 2                | Codex halluzinierte komplett anderen Text; effektiv 2-Wege-Merge Claude/Gemini. Bürgermeistername (Heer vs Axer+Ehlenz), Roths vs Kotts |
| 012   | ~45%                   | ~30%               | ~10%               | ~15%            | 1                | Gemini bei Schulmeister-Passage stärker; Henrion korrigiert (statt Henrior); Landbewohner vs unbedeutend irreconcilable |
| 021   | ~15%                   | ~25%               | ~5%                | ~55%            | 2                | Codex unbrauchbar (meist [...]-Marker); effektiv Claude-vs-Gemini; Schülerzahl 54/52, Name Pardon/Factors |
| 022   | ~15%                   | ~60%               | ~5%                | ~20%            | 1                | Codex gescheitert; Gemini klar stärkste Transkription; viele Korrekturen vs Claude-only (Schuljahr, Schulfeiern, 50 Häuser) |
| 036   | ~55%                   | ~25%               | ~5%                | ~15%            | 3                | Überschrift von Gemini/Codex falsch gelesen („Jammerstimmung" statt „Einweihung"); Codex viele [unleserlich]; Ortsname Dusemond vs. Düsseldorf |
| 037   | ~70%                   | ~20%               | ~3%                | ~7%             | 1                | Gute Übereinstimmung bei Ernte-Abschnitt; „Nisten" nur von Claude erkannt; Codex hat Konversationstext am Ende |
| 017   | —                      | —                  | —                  | —               | 1                | 2-Wege-Merge (Claude + Codex, Gemini fehlt). Sehr hohe Übereinstimmung; Codex markiert „C. Engen" und „Submittenten" als unsicher; Bürgermeister-Passage schwer lesbar |
| 038   | ~50%                   | ~25%               | ~5%                | ~20%            | 4                | Codex >70% unleserlich; Revisionsdaten divergieren; Schülerzahl 60 vs. 29; Entlassungen: nur Knaben oder auch Mädchen? |
| 023   | ~20%                   | ~50%               | ~5%                | ~25%            | 1                | Claude-Lesung durchgehend unzuverlässig; Gemini/Codex-Mehrheit für oberen Teil; Gemini allein beste Lesung für Wasserabschnitt; untere Zeilen teilweise unleserlich |
| 082   | ~70%                   | ~20%               | ~5%                | ~5%             | 2                | 3-Wege-Merge (Claude + Codex + Gemini). Sehr gute Übereinstimmung Codex/Gemini beim Haupttext. Lehrername: Gemini „Rumpp", Codex „Rumpf", Claude „Philipp" — Philipp bevorzugt (Kontextkonsistenz S.081/083). Ortsname: 3 Lesungen (Wäschbännen/Waschbrennen/Waxbrunnen) — „Waxbrunnen" per Benutzerhinweis. Klassenstärke 22+20 von Gemini. |
| 083   | —                      | ~65%               | ~5%                | ~30%            | 3                | 2-Wege-Merge (Claude + Codex). Codex bestätigt Hindenburg-Feier, Schulrevision, Glockenersatz, Versetzung Düsseldorf. Glocken-Absatz und Versetzungsnachricht deutlich klarer durch Codex. Wetterpassage bleibt teilweise unsicher. |
| 084   | —                      | —                  | —                  | —               | 4                | Claude-only. Jahreseinleitung 1928 teilweise lesbar, 10. Februar Sturm, 14. Februar unklar, Klassenfrequenz. Zweiter Absatz der Einleitung sehr schwer lesbar. |
| 085   | —                      | —                  | —                  | —               | 3                | Claude-only. Wahlergebnisse 1928 (historisch wertvoll), Stallbrand, Glockenankunft. Wahltabelle gut lesbar, Brandpassage unsicher. |
| 086   | —                      | —                  | —                  | —               | 3                | Claude-only. Glockenweihe, Firma Mabilon & Co. Saarburg. Glockenbeschreibungen und Inschriften teilweise unsicher. |

## Zusammenfassung

- Seiten zusammengeführt: 15 (005–006, 011–012, 017, 021–023, 036–038, 082–086)
- Gesamtumfang: 110 Seiten (001–110); Triple-LLM gilt für 002–110 (001 = Deckblatt, kein Text)
- Durchschn. 3-Wege-Übereinstimmung: ~39%
- Durchschn. 2-von-3 akzeptiert (Plausibilitätsprüfung bestanden): ~36%
- Durchschn. 2-von-3 abgelehnt (Plausibilitätsprüfung gescheitert): ~5%
- Durchschn. alle abweichend: ~20%
- Gesamt zur manuellen Prüfung markiert: 17
- Häufigste Verwechslungen: Codex [unleserlich]/halluziniert vs. Claude/Gemini-Lesungen; Eigennamen; Datumsangaben

## Anmerkungen zum Umfang

- **2026-03-20:** Neue Rohscans hinzugefügt — Projektumfang von 005–044 auf 001–110 erweitert.
  - Seiten 001–004 haben jetzt Scans (zuvor als nicht verfügbar angenommen). Seiten 002–004 hatten
    Gemini-only-Transkripte aus einer früheren Sitzung; können jetzt mit allen drei LLMs neu transkribiert werden.
    Seite 001 ist das Deckblatt (keine Texttranskription nötig).
  - Seiten 045–110: 66 neue Chronik-Seiten (~1904–1940er). Vollständige Triple-LLM-Pipeline ausstehend.

## Phase-4-Status (Stand: 2026-03-20, Batch 2)

| LLM    | Seiten fertig                             | Seiten fehlend                                            |
|--------|-------------------------------------------|-----------------------------------------------------------|
| Claude | 002–086 (85 Seiten)                       | 087–110 (25 Seiten)                                      |
| Gemini | 005–016, 021–028, 031–039 (29 Seiten)     | 017–020, 029–030, 040–110                                |
| Codex  | 005–030, 036–038, 082 (30 Seiten)         | 031–035, 039–081, 083–110                                |

## Rate-Limit-Protokoll

| Zeitstempel | LLM    | Seite | Aktion                                                                                                                                          |
|-------------|--------|-------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| 2026-03-20  | Gemini | ~015  | Tages-Kontingent erreicht — „Reset 17 Uhr (Europe/Berlin)". Gespeichert: 005–014, 021–028, 031–039. Fehlend: 015–020, 029–030, 040–044         |
| 2026-03-20  | Codex  | ~013  | Tages-Kontingent erreicht — „Reset 17 Uhr (Europe/Berlin)". Gespeichert: 005–006, 011–012, 021–022, 036–038. Fehlend: 007–010, 013–020, 023–030, 031–035, 039–044 |
| 2026-03-20  | Gemini | 015   | Seite 015 erfolgreich transkribiert. Seite 016: QUOTA_EXHAUSTED (retryDelay ~12,7h). Gemini-Verarbeitung gestoppt. |
| 2026-03-20  | Codex  | 007   | Seite 007 transkribiert (niedrige Qualität, viele [unleserlich]). Seite 008 in Bearbeitung. |
| 2026-03-20  | Gemini | 017   | QUOTA_EXHAUSTED — „Reset nach 11h47m". Gemini-Verarbeitung gestoppt. |
| 2026-03-20  | Claude | 061   | Seite 061 erfolgreich transkribiert und als Merged-File gespeichert. |
| 2026-03-20  | Gemini | 016   | QUOTA_EXHAUSTED — „Reset nach 11h27m". Gemini-Verarbeitung gestoppt. |
| 2026-03-20  | Codex  | 008   | Seite 008 erfolgreich transkribiert. |
| 2026-03-20  | Claude | 062–065 | Seiten 062–065 erfolgreich transkribiert und als Merged-Files gespeichert. |
| 2026-03-20  | Codex  | 009   | Seite 009 erfolgreich transkribiert. |
| 2026-03-21  | Gemini | 017   | QUOTA_EXHAUSTED — „Reset nach 8h20m". Gemini-Verarbeitung gestoppt. |
| 2026-03-21  | Codex  | 023   | Seite 023 erfolgreich transkribiert. 3-Wege-Merge mit Claude+Gemini durchgeführt. |
| 2026-03-21  | Claude | 070   | Seite 070 erfolgreich transkribiert. Als Merged-File gespeichert (Claude-only). |
| 2026-03-21  | Claude | 082–086 | Seiten 082–086 erfolgreich transkribiert. |
| 2026-03-21  | Codex  | 082   | Seite 082 transkribiert (gute Qualität). 2-Wege-Merge mit Claude durchgeführt. Codex hat Claude-Transkript vorab gelesen — keine volle Unabhängigkeit. |
| 2026-03-21  | Gemini | 082   | Erster Versuch: Tool-Fehler (write_file nicht verfügbar). Retry läuft. |
| 2026-03-21  | Gemini | 082   | Retry erfolgreich — vollständige Transkription erhalten. 3-Wege-Merge mit Claude+Codex durchgeführt. |
| 2026-03-21  | Codex  | 083   | Transkription erfolgreich. 2-Wege-Merge mit Claude durchgeführt. Codex hat Claude-Transkript vorab gelesen. |
