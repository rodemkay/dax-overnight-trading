# Changelog - the_don EA

Alle wichtigen Änderungen am Projekt werden hier dokumentiert.

## [1.25 FINAL CLEAN] - 2025-08-29

### 🎯 Hauptänderungen
- Redundante `CheckLicenseBeforeTrade()` Funktion entfernt
- Lizenz-Checks laufen nur noch automatisch über Dashboard
- Performance-Optimierungen für Backtests (50-70% schneller)

### ✨ Verbessert
- Testzeitraum-Meldung erweitert mit detaillierter Erklärung
- Journal-Ausgaben nur noch zur konfigurierten Handelszeit
- Trade-Checks nur ±1 Minute um Handelszeit
- Server-PHP mit verbesserter Fehlermeldung

### 🐛 Behoben
- Doppelte Lizenz-Checks eliminiert
- Pre-Filter Spam im Journal behoben
- OnTick Trading-Block optimiert

## [1.25 OPTIMIZED] - 2025-08-29

### ✨ Verbessert
- Lizenz-Status wird nur einmal beim erfolgreichen Trade gemeldet
- Im Backtest keine Lizenz-Checks mehr
- Vereinfachte OnTick Funktion
- Weniger CPU-Last im Live-Trading

## [1.25 FIXED] - 2025-08-29

### ✨ Neue Features
- Strukturierte Journal-Ausgaben mit [LICENSE], [FILTERS], [TRADE] Tags
- Dynamische Filter-Meldungen zur konfigurierten Handelszeit
- Lizenz-Prüfung VOR technischen Filtern
- Verbesserte Chart-Anzeige mit Farbkodierung

### 🐛 Behoben
- Pre-Filter Meldungen erscheinen nur noch zur Handelszeit
- Lizenz-Status wird korrekt im Chart angezeigt

## [1.25] - 2025-08-29

### ✨ Neue Features
- **Stop-Loss Prozent-Modus** implementiert
  - Wählbar zwischen Punkten und Prozent
  - Standard: 0.5% vom Entry-Preis
- **Testzeitraum-Management System**
  - Ein kostenloser Test pro Account-Name + EA + Version
  - Server-seitige Validierung
  - MySQL-Tracking in `test_period_history` Tabelle

### 🐛 Behoben
- Server-Lizenz Bug (falsche Spaltennamen)
- Pre-Filter Spam im Journal
- Testzeitraum-Prüfung mit korrekten Prioritäten

### ✨ Verbessert
- Standard-Settings: MaxSimultaneousPositions = 7
- RoboForex Hinweise bei abgelaufenem Testzeitraum

## [1.24] - 2025-08-28

### ✨ Neue Features
- Testzeitraum-Grundgerüst implementiert
- PHP-Integration für Server-Prüfung

## [1.20] - 2025-08-27

### ✨ Neue Features
- Multi-Position Support
- Verbesserte Filter-Logik

## [1.10] - 2025-08-26

### ✨ Neue Features
- StochRSI Pre-Filter
- Dashboard-Anzeige
- Performance-Tracking

## [1.00] - 2025-08-25

### 🎉 Initial Release
- Basis DAX Overnight Trading
- Server-Lizenzierung
- RoboForex Integration

---

## Legende
- 🎉 Initial Release
- ✨ Neue Features
- 🐛 Bugfixes
- 🎯 Hauptänderungen
- 📊 Performance
- 🔐 Sicherheit