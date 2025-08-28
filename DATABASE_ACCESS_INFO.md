# Datenbankzugriff für prophelp_users_1

## ✅ Konfiguration abgeschlossen

### Server-Setup
- **PHP-API hochgeladen:** https://lic.prophelper.org/api/db_api.php
- **Token:** `250277100311270613`
- **Datenbank:** prophelp_users_1

### Lokale Dateien (R:\mt5\daxovernight)
- **db_client.py** - Python-Client mit konfiguriertem Token
- **test_db_connection.py** - Test-Script für Verbindung

## 📍 WICHTIG: Pfad-Klarstellung

### Korrekte Pfade vom ACER LAPTOP:
```
R:\mt5\daxovernight\  → RYZENSERVER /home/rodemkay/mt5/daxovernight  ✅ RICHTIG
S:\                   → EXISTIERT NICHT auf ACER Laptop           ❌ FALSCH
```

### Pfade vom WIN11NEU:
```
S:\mt5\daxovernight\  → RYZENSERVER /home/rodemkay/mt5/daxovernight
R:\                   → EXISTIERT NICHT auf WIN11NEU
```

## 🔧 Verwendung

### Verbindungstest
```python
# Test vom ACER Laptop aus
cd r:\mt5\daxovernight
x:\Python313\python.exe db_client.py
```

### In eigenen Scripts verwenden
```python
from db_client import DatabaseClient

# Client mit vorkonfiguriertem Token
db = DatabaseClient()

# Daten abrufen
licenses = db.select("SELECT * FROM lnative WHERE account = ?", ['12345'])
```

## 📝 Zugangsdaten Übersicht

### MySQL Datenbank (über PHP-API)
- Host: localhost (nur intern)
- Datenbank: prophelp_users_1
- Benutzer: prophelp_adm
- Passwort: mW0uG1pG9b
- Token: 250277100311270613

### phpMyAdmin (Browser)
- URL: https://web-de.wishhost.net:1501/lGoJSoSPtQ0xoqNk/phpmyadmin/
- Benutzer: prophelp_adm
- Passwort: mW0uG1pG9b

### FTP-Server
- Host: 162.55.90.123
- Benutzer: prophelp
- Passwort: J!7w$3@9mK#4nL2p
- Pfad: /www/lic.prophelper.org/api/

## ✅ Status
- PHP-API ist hochgeladen und aktiv
- Token ist konfiguriert
- Datenbankzugriff funktioniert über API
