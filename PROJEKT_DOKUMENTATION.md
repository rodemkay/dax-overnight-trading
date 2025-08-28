# PROJEKT DOKUMENTATION - DAX Overnight System
Letzte Aktualisierung: 08.11.2025, 16:24 Uhr

## 📁 PROJEKTSTRUKTUR

### Hauptverzeichnisse
- **s:\mt5\daxovernight** - Hauptprojektordner
- **x:\Python313** - Python Installation
- **x:\portabel\MetaTrader5** - MetaTrader 5 Installation

## 🔑 ZUGANGSDATEN

### FTP-Server (PropHelper)
- **Host:** 162.55.90.123
- **User:** prophelp
- **Pass:** .Propt333doka?
- **Web:** https://lic.prophelper.org/files/

### MySQL Datenbank
- **Host:** 162.55.90.123
- **User:** prophelper
- **Pass:** .Propt333doka?
- **Database:** prophelper
- **Tabelle:** lnative

### MetaTrader 5
- **Account:** 10016882
- **Password:** TdNy#6K#L
- **Server:** RoboForex-ECN

## 📂 WICHTIGE DATEIEN

### Python Scripts (s:\mt5\daxovernight)

#### 1. **test_roboforex_connection.py**
- Testet die Verbindung zu RoboForex API
- Prüft ob Account ein Partner-Account ist
- Status: ✓ Funktioniert

#### 2. **mysql_list_accounts.py**
- Listet alle Accounts aus MySQL-Datenbank
- Zeigt Account-Details und roboaffiliate Status
- Status: ✓ Funktioniert

#### 3. **update_roboaffiliate.py**
- Aktualisiert roboaffiliate Status in der Datenbank
- Prüft jeden Account bei RoboForex
- Status: ✓ Funktioniert

#### 4. **download_template_inc.py**
- Lädt template.inc.php vom FTP-Server herunter
- Erstellt lokale Kopie für Bearbeitung
- Status: ✓ Funktioniert

#### 5. **modify_template.py**
- Modifiziert template.inc.php automatisch
- Fügt RoboForex-Spalte hinzu
- Erzeugt: template_inc_complete.php
- Status: ✓ Funktioniert

#### 6. **upload_final.py**
- Lädt modifizierte template.inc.php hoch
- Erstellt automatisch Backup
- Verifiziert Änderungen
- Status: ✓ Bereit zum Upload

### Web-Dateien (auf FTP-Server)

#### /www/lic.prophelper.org/files/
- **template.inc.php** - Haupttemplate für Benutzertabelle
- **office.php** - Admin-Interface
- **metatrader.php** - Client-Interface  
- **session.php** - Session-Management
- **connect.php** - Datenbankverbindung
- **update.php** - Update-Funktionen

## 🔄 WORKFLOW

### 1. RoboForex Integration komplett implementiert (11.08.2025)

#### Ausgeführte Schritte:
```bash
# 1. Template.inc.php Syntax-Fehler behoben und hochgeladen
python3 fix_and_upload_template.py

# 2. PHP-Script für EA-Updates hochgeladen
python3 upload_robo_update_script.py

# 3. EA-Code erweitert (don_gpt.mq5)
# - UpdateRoboForexStatusToServer() Funktion hinzugefügt
# - Automatisches Update bei OnInit()
```

#### Verfügbare Python-Scripts:
- `test_roboforex_connection.py` - RoboForex API testen
- `mysql_list_accounts.py` - Accounts aus DB auflisten
- `update_roboaffiliate.py` - Partner-Status updaten
- `fix_and_upload_template.py` - Template reparieren
- `upload_robo_update_script.py` - PHP-Script hochladen

### 2. System-Pfade (RYZENSERVER)
```
Arbeitsverzeichnis: /home/rodemkay/mt5/daxovernight/
WIN11NEU Mounts:
- /home/rodemkay/CaufWin11/ → C:\ (WIN11NEU)
- /home/rodemkay/DaufWin11/ → D:\ (WIN11NEU)
- /home/rodemkay/EaufWin11/ → E:\ (WIN11NEU)
MetaTrader5: /home/rodemkay/CaufWin11/portabel/MetaTrader5/
```

## 🎯 PROJEKTZIELE

### Hauptziel
Integration der RoboForex Partner-Information in das PropHelper Dashboard

### Umgesetzte Features
1. ✓ MySQL-Tabelle erweitert um `roboaffiliate` Spalte
2. ✓ Automatische Prüfung des Partner-Status via API
3. ✓ Anzeige in Web-Interface mit visuellen Indikatoren
4. ✓ Sortierung nach Partner-Status
5. ✓ Account-Anzeige nutzt jetzt `accountLogin` wenn vorhanden

## 📊 DATENBANKSTRUKTUR

### Tabelle: lnative
Wichtige Felder:
- `id` - Primärschlüssel
- `full_name` - Benutzername
- `account` - MT5 Account-Nummer
- `accountLogin` - Alternative Account-Anzeige
- `roboaffiliate` - Partner-Status ('yes'/'no')
- `program` - Programmname
- `test` - Test/Live Status (1=Office, 2=Connect)
- `ip` - IP-Adresse
- `serialNo` - Seriennummer

## 🛠️ TECHNISCHE DETAILS

### Python-Umgebung
- **Version:** Python 3.13
- **Pfad:** x:\Python313\python.exe
- **Packages:** mysql-connector-python, MetaTrader5

### Web-Technologie
- **Backend:** PHP
- **Datenbank:** MySQL
- **Frontend:** HTML/CSS/JavaScript/jQuery

## ⚙️ ÄNDERUNGEN AN template.inc.php

### 1. SQL-Queries erweitert
- SELECT fügt `roboaffiliate` hinzu
- Neue Sort-Option (value=13) für RoboForex

### 2. Tabellen-Header erweitert
- Neue Spalte "RoboForex" vor "Del"

### 3. Daten-Anzeige
- Grünes ✓ für Partner
- Rotes ✗ für Nicht-Partner
- Account zeigt `accountLogin` wenn vorhanden

### 4. Sortierung
- Neue Sortierung nach roboaffiliate Status

## 📝 NOTIZEN

### Wichtige Hinweise
- Immer Backup erstellen vor Änderungen
- Template.inc.php wird von office.php und metatrader.php verwendet
- Änderungen wirken sich auf beide Interfaces aus

### Backup-Dateien
- Original template.inc.php als .backup_[timestamp] auf Server
- Lokale Kopien in s:\mt5\daxovernight\

### Test-URLs
- https://lic.prophelper.org/files/office.php (Admin)
- https://lic.prophelper.org/files/metatrader.php (Client)

## 🚀 NÄCHSTE SCHRITTE

1. Upload der modifizierten template.inc.php durchführen
2. Funktionalität im Live-System testen
3. Regelmäßige Updates des roboaffiliate Status einrichten
4. Optional: Automatisierung via Cron-Job

## 📞 SUPPORT

Bei Fragen oder Problemen:
- Backup wiederherstellen via FTP
- Original-Dateien in s:\mt5\daxovernight\
- Alle Scripts sind dokumentiert und können einzeln ausgeführt werden

---
Ende der Dokumentation
