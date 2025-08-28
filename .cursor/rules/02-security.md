# Editor-Regel: Sicherheit, Browser & Umgang mit Geheimnissen

Zweck
- Diese Regel verankert Sicherheitsvorgaben und verhindert den Einsatz unerwünschter Tools im Entwicklungsprozess.

Verbindliche Browser-Vorgabe
- Keine Nutzung/Installation von Chrome/Chromium für automatisierte Tests.
- Ausschließlich Firefox für Playwright-gestützte Abläufe (siehe MCP-Server-Konfiguration).

Umgang mit Geheimnissen
- Keine sensiblen Inhalte in Commits, Logs oder Assistenten-Ausgaben.
- Beispiele sensibler Artefakte:
  - server_credentials.txt
  - Verzeichnisse/Dateien unter LicProphelper/files/ (z. B. Zugangsdaten, Sessions, PHP-Skripte)
  - Alle Schlüssel, Passwörter, Tokens und personenbezogene Daten
- Bei Bedarf Maskierung vornehmen oder auf sichere Speicherorte verweisen.

Netzwerk- und Lizenzaspekte
- WebRequest-/Netzwerkzugriffe nur, wenn erforderlich und dokumentiert.
- Lizenz- und Server-Abhängigkeiten gemäß Projektdokumentation beachten (siehe CLAUDE.md und docs).

MCP-Server-Hinweis
- Konfigurationen siehe:
  - .cursor/mcp.json
  - .kilocode/mcp.json
- Playwright MCP nutzt Firefox; Context-Tools nur für dokumentationsbezogene Recherche.

Quellen & Referenzen
- Kilo Code Guide: KILO_CODE_GUIDE.md
- Projekt-Gedächtnis: .kilocode/memory.json
- Projektdokumentation: CLAUDE.md, SESSION_SUMMARY.md, docs/*

Scope
- Nur die oben spezifizierten Dateien erstellen mit exakt diesen Inhalten. Keine weiteren Dateien ändern oder anlegen.