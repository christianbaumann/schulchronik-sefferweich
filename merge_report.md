# Merge-Bericht

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
| 038   | ~50%                   | ~25%               | ~5%                | ~20%            | 4                | Codex >70% unleserlich; Revisionsdaten divergieren; Schülerzahl 60 vs. 29; Entlassungen: nur Knaben oder auch Mädchen? |

## Zusammenfassung

- Seiten zusammengeführt: 9 (005–006, 011–012, 021–022, 036–038)
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

## Phase-4-Status (Stand: 2026-03-20, nach Rate-Limit)

| LLM    | Seiten fertig                             | Seiten fehlend                                            |
|--------|-------------------------------------------|-----------------------------------------------------------|
| Claude | 005–061 (57 Seiten)                       | 002–004 (Scans jetzt verfügbar); 062–110 (neu)           |
| Gemini | 005–015, 021–028, 031–039 (28 Seiten)     | 016–020, 029–030, 040–044; auch 002–004, 045–110         |
| Codex  | 005–007, 011–012, 021–022, 036–038 (10 Seiten) | 008–010, 013–020, 023–030, 031–035, 039–044; auch 002–004, 045–110 |

## Rate-Limit-Protokoll

| Zeitstempel | LLM    | Seite | Aktion                                                                                                                                          |
|-------------|--------|-------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| 2026-03-20  | Gemini | ~015  | Tages-Kontingent erreicht — „Reset 17 Uhr (Europe/Berlin)". Gespeichert: 005–014, 021–028, 031–039. Fehlend: 015–020, 029–030, 040–044         |
| 2026-03-20  | Codex  | ~013  | Tages-Kontingent erreicht — „Reset 17 Uhr (Europe/Berlin)". Gespeichert: 005–006, 011–012, 021–022, 036–038. Fehlend: 007–010, 013–020, 023–030, 031–035, 039–044 |
| 2026-03-20  | Gemini | 015   | Seite 015 erfolgreich transkribiert. Seite 016: QUOTA_EXHAUSTED (retryDelay ~12,7h). Gemini-Verarbeitung gestoppt. |
| 2026-03-20  | Codex  | 007   | Seite 007 transkribiert (niedrige Qualität, viele [unleserlich]). Seite 008 in Bearbeitung. |
| 2026-03-20  | Gemini | 017   | QUOTA_EXHAUSTED — „Reset nach 11h47m". Gemini-Verarbeitung gestoppt. |
| 2026-03-20  | Claude | 061   | Seite 061 erfolgreich transkribiert und als Merged-File gespeichert. |
