# CLAUDE.md - System Integration Dokumentation

## ⚡ ARBEITSWEISE - SEHR WICHTIG!
**ALLE Anfragen werden IMMER zuerst an den PROJECT-ORCHESTRATOR weitergeleitet!**
- Der Orchestrator analysiert, plant und delegiert an spezialisierte Agenten
- Direkte Implementierung ohne Orchestrator ist NICHT erlaubt
- Dies garantiert strukturierte, dokumentierte und koordinierte Entwicklung

## 📁 VERSIONSVERWALTUNG - WICHTIG!

### Bei neuen EA-Versionen (the_don):
1. **VOR Änderungen:** Backup der aktuellen .mq5 mit Versionsnummer erstellen
   ```bash
   cp the_don.mq5 the_don_v1.XX.mq5
   ```

2. **Nach Kompilierung:**
   - Die kompilierte .ex5 bleibt IMMER `the_don.ex5` (keine Versionsnummer!)
   - Nur die .mq5 Backups haben Versionsnummern
   
3. **Git Push nach jeder Version:**
   ```bash
   git add .
   git commit -m "Version 1.XX - [Beschreibung der Änderungen]"
   git push origin main
   ```

### Warum diese Struktur?
- **MetaTrader** sieht nur eine `the_don.ex5` (kein Spam im Navigator)
- **Backups** der .mq5 ermöglichen Rollback zu jeder Version
- **Git-Historie** dokumentiert alle Änderungen
- **Saubere Struktur** im EA-Ordner

### Beispiel-Workflow:
```bash
# 1. Backup erstellen
cp the_don.mq5 the_don_v1.24.mq5

# 2. Änderungen machen
# ... Code editieren ...

# 3. Kompilieren (erzeugt the_don.ex5)
wine MetaEditor64.exe /compile:MQL5/Experts/Don/the_don.mq5

# 4. Git commit & push
git add -A
git commit -m "v1.24 - Fixed multiple positions bug"
git push origin main
```

## System-Umgebung

### Hauptarbeitsverzeichnis
- **RYZENSERVER (Linux):** /home/rodemkay/mt5/daxovernight/
- **Symlinks im Arbeitsverzeichnis:**
  - `./MT5_Windows` → /home/rodemkay/CaufWin11/portabel/MetaTrader5/
  - `./EA_Entwicklung` → /home/rodemkay/CaufWin11/portabel/MetaTrader5/MQL5/Experts/Don/

### MetaTrader5 Installationen
#### 1. Windows-Mount (HAUPTNUTZUNG)
- **Mount-Point:** /home/rodemkay/CaufWin11/ → C:\ auf WIN11NEU (IP: 100.122.144.89)
- **MT5-Pfad:** /home/rodemkay/CaufWin11/portabel/MetaTrader5/
- **EA-Pfad:** /home/rodemkay/CaufWin11/portabel/MetaTrader5/MQL5/Experts/Don/
- **⚠️ WICHTIG:** Dies ist ein Windows-Mount (CIFS)! MetaEditor64.exe läuft auf Windows, KEIN Wine nötig!

#### 2. Wine-Installation (ALTERNATIV)
- **Pfad:** /home/rodemkay/.wine-mt5/drive_c/Program Files/MetaTrader 5/
- **Verwendung:** Für Linux-basierte Tests und Kompilierung mit Wine

### Python-Installationen
- **Windows Python:** /home/rodemkay/CaufWin11/Python313/
- **Windows Python Portable:** /home/rodemkay/CaufWin11/python-portable/
- **Linux Python:** System Python3 auf RYZENSERVER

### EA-Versionen
- **Aktuell:** don_gpt v2.00 (PROGRAM_NAME: "don_gpt", LICENSE_CODE: "DAXON10")
- **Neu:** der_don v1.00 (PROGRAM_NAME: "der_don", LICENSE_CODE: "DERDON")

### FTP/MySQL Zugangsdaten
```
FTP_HOST: 162.55.90.123
FTP_USER: prophelp
FTP_PASS: .Propt333doka?
MySQL_HOST: localhost
MySQL_DB: prophelp_users_1
MySQL_USER: prophelp_adm
MySQL_PASS: mW0uG1pG9b
MySQL_TABLE: lnative
```

## RoboForex Integration - Implementierung

### 1. Template.inc.php Fix
- **Problem:** Syntax-Fehler Zeile 334 (doppeltes else)
- **Lösung:** Automatisches Fix-Script erstellt
- **Status:** ✓ Bereit zur Ausführung

### 2. Python-Scripts
Alle Scripts sind erstellt und bereit:
- `test_roboforex_connection.py` - API Test
- `mysql_list_accounts.py` - DB Account Liste
- `update_roboaffiliate.py` - Status Updates
- `fix_and_upload_template.py` - Template Reparatur
- `upload_robo_update_script.py` - PHP Upload

### 3. EA Integration
- Code für don_gpt.mq5 vorbereitet in `ea_roboforex_db_update.mq5`
- PHP-Endpoint `update_robo_status.php` für EA-Updates

### 4. Web-Interface
- RoboForex-Spalte wird in /connect und /office angezeigt
- ✓ für Partner, ✗ für Nicht-Partner
- Sortierung nach RoboForex-Status möglich

## ✅ IMPLEMENTIERUNG ABGESCHLOSSEN (11.08.2025)

### Version 2.0 - Finale Optimierungen (11.08.2025 Nachmittag)
1. ✅ DB-Zugangsdaten korrigiert (prophelp_adm / prophelp_users_1)
2. ✅ WinInet als primäre Methode (WebRequest entfernt)
3. ✅ INSERT-Logik für neue Konten implementiert
4. ✅ Verzögerte zweite Übertragung (3 Sek) für neue Konten
5. ✅ Log-Ausgaben massiv reduziert (nur noch wichtige Infos)
6. ✅ "Partner" → "Affiliate" global geändert
7. ✅ Sanftere Hinweise bei aktiver Server-Lizenz
8. ✅ Header "RoboForex" → "Affil" in Web-Interface

### Version 1.0 - Basis-Implementation
1. ✅ Template.inc.php Syntax-Fehler behoben und hochgeladen
2. ✅ update_robo_status.php auf Server installiert
3. ✅ RoboForex-Spalte in Web-Interface integriert
4. ✅ EA-Code in don_gpt.mq5 erweitert mit:
   - UpdateRoboForexStatusToServer() Funktion (nur WinInet)
   - Automatisches Update bei jedem OnInit()
   - Verzögerte zweite Übertragung nach 3 Sekunden
5. ✅ Alle Python-Scripts erstellt und getestet

### EA-Integration:
Der EA schreibt nun bei jedem Start den RoboForex-Status in die Datenbank:
- Account-Nummer und Partner-Status werden übertragen
- Funktioniert via WebRequest oder WinInet
- Update erfolgt an: https://lic.prophelper.org/files/update_robo_status.php

### Dateipfade:
- EA: /home/rodemkay/CaufWin11/portabel/MetaTrader5/MQL5/Experts/Don/don_gpt.mq5
- Scripts: /home/rodemkay/mt5/daxovernight/*.py
- Web: https://lic.prophelper.org/connect

## URLs zum Testen
- https://lic.prophelper.org/connect (User: admin/admin)
- https://lic.prophelper.org/office (User: admin/admin)

## Wichtige Hinweise
- **IMMER den PROJECT-ORCHESTRATOR für ALLE Aufgaben nutzen!**
- Der Orchestrator delegiert automatisch an:
  - code-generator für Implementierungen
  - performance-auditor für Optimierungen
  - test-automation-agent für Tests
  - Weitere spezialisierte Agenten nach Bedarf
- Alle Scripts nutzen Python3 auf RYZENSERVER
- EA muss WebRequest für lic.prophelper.org erlauben
- roboaffiliate Spalte wird automatisch erstellt falls nicht vorhanden
- Check-Period wird vom Backend gesteuert (0-5 Stunden einstellbar)
- Demo-Limit über Backend steuerbar (aktuell 7 Tage für don_gpt)

## ⚠️ PLAYWRIGHT BROWSER - SEHR WICHTIG!
**NIEMALS Chrome oder Chromium für Playwright verwenden!**
- Browser bleibt immer hängen bei Chrome/Chromium
- **NUR Firefox verwenden** für alle Playwright-Operationen
- Firefox ist bereits installiert und konfiguriert