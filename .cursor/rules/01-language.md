# Editor-Regel: Sprache & Ausgabe

Zweck
- Diese Regel stellt sicher, dass alle Ausgaben des Assistenten strikt auf Deutsch erfolgen und die Kommunikation klar und technisch bleibt.

Verbindliche Vorgaben
- Ausgabesprache: Deutsch (de-DE).
- Klare, präzise, technische Formulierungen. Keine Smalltalk-Floskeln.
- Dateiverweise stets als relative Pfade.
- Bei Mehrdeutigkeiten: konkrete Rückfragen stellen, ansonsten selbstständig mit vorhandenen Informationen fortfahren.

Kontextquellen
- Kilo Code Guide: KILO_CODE_GUIDE.md
- Projekt-Gedächtnis: .kilocode/memory.json
- Projekt-Dokumentation: u. a. CLAUDE.md, SESSION_SUMMARY.md, docs/*

Durchsetzung
- Wenn Eingaben mehrsprachig sind, bleibt die Ausgabe Deutsch.
- Abweichungen von Deutsch sind nur zulässig, wenn eine konkrete Projektregel oder Nutzeranweisung dies ausdrücklich verlangt und im Projekt-Gedächtnis vermerkt wurde.

Hinweise
- MQL5-Code verwendet UTF-16 LE Encoding; bei Code-Änderungen auf korrekte Kodierung achten (siehe Projekt-Dokumentation).