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
| 017   | ~60%                   | ~25%               | ~5%                | ~10%            | 2                | 3-Wege-Merge (Claude + Codex + Gemini). Bürgermeister-Passage: Gemini-Lesung „Bürgermeister Spang dieses Amt" trotz 2-von-3-Minderheit bevorzugt (grammatisch korrekt). Geburtsort/Datum: Fließem/31.1. (2-von-3) vs. Coblenz/21.1. (Gemini). |
| 020   | —                      | ~70%               | ~5%                | ~25%            | 1                | 3-Wege-Merge (Claude + Gemini + Codex). Gute Übereinstimmung Claude/Gemini; Codex bestätigt Grundstruktur. Waldreichtum, Kapelle Wachsbrunnen/Wasenbrunnen. |
| 029   | —                      | ~65%               | ~5%                | ~30%            | 2                | 3-Wege-Merge. Einquartierung Elsenborn, 8. Kürassiere. Lehrerwechsel Bauer→Wirt. Codex schwach aber bestätigt Kernpassagen. |
| 030   | —                      | ~60%               | ~5%                | ~35%            | 2                | 3-Wege-Merge. Nachtrag über Kriegsende 1918, Kriegergedenktafel 1920, Kriegerheimfest 1925. Lehrer Stoffels. |
| 034   | —                      | ~50%               | ~5%                | ~45%            | 3                | 3-Wege-Merge. Codex extrem schwach (>80% unleserlich). Effektiv Claude+Gemini. Ostern, Ernte, Schulfeiern, Pfarrwechsel Ettges. |
| 035   | —                      | ~40%               | ~5%                | ~55%            | 3                | 2-Wege-Merge (Claude + Codex). Codex sehr schwach. Fortgesetzte Erzählung Pfarrwechsel, Schulrevision. |
| 038   | ~50%                   | ~25%               | ~5%                | ~20%            | 4                | Codex >70% unleserlich; Revisionsdaten divergieren; Schülerzahl 60 vs. 29; Entlassungen: nur Knaben oder auch Mädchen? |
| 023   | ~20%                   | ~50%               | ~5%                | ~25%            | 1                | Claude-Lesung durchgehend unzuverlässig; Gemini/Codex-Mehrheit für oberen Teil; Gemini allein beste Lesung für Wasserabschnitt; untere Zeilen teilweise unleserlich |
| 082   | ~70%                   | ~20%               | ~5%                | ~5%             | 2                | 3-Wege-Merge (Claude + Codex + Gemini). Sehr gute Übereinstimmung Codex/Gemini beim Haupttext. Lehrername: Gemini „Rumpp", Codex „Rumpf", Claude „Philipp" — Philipp bevorzugt (Kontextkonsistenz S.081/083). Ortsname: 3 Lesungen (Wäschbännen/Waschbrennen/Waxbrunnen) — „Waxbrunnen" per Benutzerhinweis. Klassenstärke 22+20 von Gemini. |
| 083   | —                      | ~65%               | ~5%                | ~30%            | 3                | 2-Wege-Merge (Claude + Codex). Codex bestätigt Hindenburg-Feier, Schulrevision, Glockenersatz, Versetzung Düsseldorf. Glocken-Absatz und Versetzungsnachricht deutlich klarer durch Codex. Wetterpassage bleibt teilweise unsicher. |
| 084   | —                      | —                  | —                  | —               | 4                | Claude-only. Jahreseinleitung 1928 teilweise lesbar, 10. Februar Sturm, 14. Februar unklar, Klassenfrequenz. Zweiter Absatz der Einleitung sehr schwer lesbar. |
| 085   | —                      | —                  | —                  | —               | 3                | Claude-only. Wahlergebnisse 1928 (historisch wertvoll), Stallbrand, Glockenankunft. Wahltabelle gut lesbar, Brandpassage unsicher. |
| 086   | —                      | —                  | —                  | —               | 3                | Claude-only. Glockenweihe, Firma Mabilon & Co. Saarburg. Glockenbeschreibungen und Inschriften teilweise unsicher. |
| 039   | —                      | ~55%               | ~5%                | ~40%            | 3                | 3-Wege-Merge. Codex halluziniert (anderer Texttyp). Effektiv Claude+Gemini. Ernte, Revision, Einquartierung. |
| 040   | —                      | —                  | —                  | —               | 3                | Claude-only + Scan-Verifizierung. Gemini kontaminiert (BGB 1900 statt 1905), gelöscht. Codex schwach (1905/06). Oktober-Revision, Kaisergeburtstagsfeier, Schuljahr 1905/06. |
| 041   | —                      | —                  | —                  | —               | 3                | Claude-only + Scan-Verifizierung. Gemini kontaminiert (1888 statt 1906), gelöscht. Codex kontaminiert (Seite 029). Mai-Revision, Fronleichnam, Einquartierung Dragoner. |
| 042   | —                      | —                  | —                  | —               | 3                | Claude-only + Scan-Verifizierung. Gemini kontaminiert (1898 statt 1906), gelöscht. Codex halluziniert (Kanzleidokument 1816). Januar-Revision, Kaisergeburtstag, Lehrerwechsel. |
| 043   | —                      | —                  | —                  | —               | 4                | Claude-only + Scan-Verifizierung. Gemini kontaminiert (1869 statt 1907), gelöscht. Codex halluziniert (Gerichtsverhandlung 1829). Spaziergang Kyllburg, Ernte, Schuljahr 1907-08. |
| 044   | —                      | —                  | —                  | —               | 4                | Claude-only + Scan-Verifizierung. Gemini kontaminiert (1899/1900 statt 1908), gelöscht. Codex halluziniert (Kirchendokument). Spaziergang, Ernte, Kartoffelfäule. |
| 045   | —                      | ~65%               | ~5%                | ~30%            | 2                | 2-Wege-Merge (Claude + Gemini). Kriegerdenkmal 1928, Lehrerwechsel Theis→Gierten, Zweiklassige Schule ab Oktober 1928. |
| 087   | —                      | —                  | —                  | —               | 2                | Claude-only. Kapellenreparaturen Juni, Erntebericht August, Herbstferien September, Jahresbilanz November. Küster Peter Manns gewürdigt. |
| 051   | ~5%                    | ~70%               | ~5%                | ~20%            | 2                | 3-Wege-Merge. Codex vollständig halluziniert (fabricated „Beurtheilung"-Dokument). Claude in mehreren Abschnitten garbled. Gemini klar beste Quelle. Kirchlichkeiten vs. Gedächtnisfeier unklar, „Kirchlichkeiten" übernommen. Schuljahr 1914/15, Kriegsausbruch. LaTeX: „Besondere Ereignisse" als \abschnitt korrigiert. |

## Zusammenfassung

- Seiten zusammengeführt: 29 (005–006, 011–012, 017, 020–023, 029–030, 034–035, 036–045, 051, 082–087)
- Gesamtumfang: 110 Seiten (001–110); Triple-LLM gilt für 002–110 (001 = Deckblatt, kein Text)
- Durchschn. 3-Wege-Übereinstimmung: ~30%
- Durchschn. 2-von-3 akzeptiert (Plausibilitätsprüfung bestanden): ~45%
- Durchschn. 2-von-3 abgelehnt (Plausibilitätsprüfung gescheitert): ~5%
- Durchschn. alle abweichend: ~30%
- Gesamt zur manuellen Prüfung markiert: 46
- Häufigste Verwechslungen: Codex [unleserlich]/halluziniert vs. Claude/Gemini-Lesungen; Eigennamen; Datumsangaben
- **Codex-Qualität:** Codex liefert bei Kurrent-Scans sehr oft >70% [unleserlich] oder halluziniert komplett andere Inhalte. Effektive Merges sind daher meist 2-Wege (Claude + Gemini).

## Anmerkungen zum Umfang

- **2026-03-20:** Neue Rohscans hinzugefügt — Projektumfang von 005–044 auf 001–110 erweitert.
  - Seiten 001–004 haben jetzt Scans (zuvor als nicht verfügbar angenommen). Seiten 002–004 hatten
    Gemini-only-Transkripte aus einer früheren Sitzung; können jetzt mit allen drei LLMs neu transkribiert werden.
    Seite 001 ist das Deckblatt (keine Texttranskription nötig).
  - Seiten 045–110: 66 neue Chronik-Seiten (~1904–1940er). Vollständige Triple-LLM-Pipeline ausstehend.

## Phase-4-Status (Stand: 2026-03-20, Batch 2)

| LLM    | Seiten fertig                                                       | Seiten fehlend                                            |
|--------|---------------------------------------------------------------------|-----------------------------------------------------------|
| Claude | 002–088 (87 Seiten)                                                 | 089–110 (22 Seiten) — **in Bearbeitung**                 |
| Gemini | 005–020, 021–028, 029–030, 031–039, 045, 051, 082 (37 Seiten)      | 040–044, 046–050, 052–081, 083–110 (040–044: kontaminiert, gelöscht) |
| Codex  | 005–033, 034–035, 036–038, 039–044, 051, 082–083 (43 Seiten)       | 045–050, 052–081, 084–110                                |

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
| 2026-03-21  | Claude | 087   | Transkription erfolgreich. Als Merged-File gespeichert (Claude-only). |
| 2026-03-21  | Gemini | 017   | Transkription erfolgreich. 3-Wege-Merge mit Claude+Codex durchgeführt. Bürgermeister-Passage: Gemini-Lesung bevorzugt. |
| 2026-03-21  | Gemini | 020,029-030,040-045 | Batch-Transkription erfolgreich (9 Seiten). Gemini versuchte mehrfach Dateien zu schreiben (write_file-Fehler), gab Text dann als Ausgabe zurück. |
| 2026-03-21  | Codex  | 034-035,039-044 | Batch-Transkription (8 Seiten). Qualität durchgehend schlecht: >70% [unleserlich], mehrere Seiten halluziniert (falsche Inhalte). Isolation via /tmp/codex_isolated_NNN/ verbesserte Seitenzuordnung, aber Codex 041 trotzdem kontaminiert (las /tmp-Dateien). |
| 2026-03-21  | Claude | —     | Claude-Transkription auf Benutzerwunsch pausiert. Nur Merges durchgeführt. |
| 2026-03-21  | Gemini | 040–044 | Kontaminierte Transkripte gelöscht. Gemini-Isolation über /tmp gescheitert — Gemini las Scans aus dem Projektverzeichnis und transkribierte falsche Seiten. Merges auf Claude-only + Scan-Verifizierung zurückgesetzt. |
| 2026-03-21  | Gemini | 051   | Transkription erfolgreich. |
| 2026-03-21  | Codex  | 051   | Transkription fehlgeschlagen — Codex halluzinierte ein „Beurtheilung"-Dokument statt der Schulchronik. |
| 2026-03-21  | Claude | 089+  | Claude-Transkription Seiten 089–098 gestartet (Subagent läuft). |
