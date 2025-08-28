# CHANGELOG - the_don EA (DAX Overnight Trading System)

## [1.10] - 2025-08-13

### Added
- GitHub repository integration
- Comprehensive project documentation  
- Organized project structure with src/, docs/, config/ directories
- Symlink integration for Windows-mounted EA files

### Changed
- **RENAMED:** Project from `der_don` to `the_don` for consistency
- Updated version from 1.00 to 1.10
- Reorganized file structure for better maintainability
- Moved Python scripts to src/Scripts/
- Moved Include files to src/Include/

### Technical
- Initialized Git version control
- Created .gitignore for sensitive files
- Set up main branch as default
- Prepared for GitHub Actions CI/CD

---

## Version 2.00 Build 20250811
*Release Date: 11. August 2025*

### 🎯 Major Features
- **RoboForex Affiliate Integration** vollständig implementiert
- **Dual-Lizenz-System**: Server-Lizenz ODER Affiliate-Account
- **Web-Interface** mit Affiliate-Status Anzeige

### ✨ New Features
- Automatische Affiliate-Verifikation via RoboForex API
- Affiliate-Status wird in Datenbank gespeichert
- Web-Interface zeigt "Affil" Spalte mit ✓/✗
- Unlimitierte Nutzung für Affiliate-Konten
- Sanfte Hinweise für Affiliate-Registrierung

### 🔧 Technical Improvements
- WinInet statt WebRequest (stabiler)
- INSERT-Logik für neue Konten in DB
- Verzögerte zweite Übertragung (3 Sek)
- Massiv reduzierte Log-Ausgaben
- "Partner" → "Affiliate" Begriffe vereinheitlicht

### 🐛 Bug Fixes
- DB-Verbindungsfehler behoben (korrekte Credentials)
- Tabellen-Header Verschiebung korrigiert
- WinInet Parameter-Fehler behoben
- Neue Konten werden sofort in DB eingetragen
- Doppelte RoboForex-Spalte entfernt

### 📊 Database Changes
- Neue Spalte: `roboaffiliate` (yes/no)
- DB: prophelp_users_1 (nicht prophelper)
- User: prophelp_adm (nicht prophelper)

### 🔐 Security
- API-Keys fest im Code
- Sichere WinInet-Verbindungen
- Keine sensiblen Daten in Logs

### 📝 Documentation
- CLAUDE.md aktualisiert
- Tageslog erstellt
- Playwright Firefox-Warnung dokumentiert

### ⚠️ Breaking Changes
- WebRequest nicht mehr unterstützt
- Nur Firefox für Playwright MCP Server

### 💡 Known Issues
- "Leaked strings" Meldungen (harmlos, MQL5-intern)
- Chrome/Chromium funktioniert NICHT mit Playwright

---

## Version 1.99 Build 20250810
*Release Date: 10. August 2025*

### Features
- Basis RoboForex Integration
- Server-Lizenz System
- Web-Interface Template

---

## Version 1.00 Build 20250801
*Release Date: 1. August 2025*

### Initial Release
- DAX Overnight Trading Strategie
- Stochastic-basierte Entry-Signale
- ATR Filter
- Server-Lizenz Prüfung