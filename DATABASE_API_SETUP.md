# Datenbank-API Setup für prophelp_users_1

## 📋 Übersicht

Da die direkte MySQL-Verbindung von außen nicht möglich ist (IP-Whitelisting nicht verfügbar), verwenden wir eine PHP-API als Vermittler. Die PHP-API läuft auf dem Server und verbindet sich lokal zur Datenbank.

```
Ihre Maschine (Python) → HTTPS → PHP-API (Server) → MySQL (localhost)
```

## 🚀 Installation

### Schritt 1: PHP-API vorbereiten

1. **WICHTIG**: Öffnen Sie die Datei `db_api.php` und ändern Sie das Token:
   ```php
   $API_TOKEN = 'ihr_eigenes_sicheres_token_hier_2025';
   ```

2. Erstellen Sie auf dem Server einen neuen Ordner:
   - Verbinden Sie sich per FTP zu: `162.55.90.123`
   - Navigieren Sie zu: `/www/lic.prophelper.org/`
   - Erstellen Sie einen Ordner: `api/`

### Schritt 2: PHP-API hochladen

1. Laden Sie `db_api.php` hoch nach:
   ```
   /www/lic.prophelper.org/api/db_api.php
   ```

2. Setzen Sie die Dateiberechtigungen auf `644` (oder `755` falls nötig)

3. Testen Sie die API im Browser:
   ```
   https://lic.prophelper.org/api/db_api.php
   ```
   Sie sollten einen Fehler sehen: `{"error":"Unauthorized: Invalid or missing token"}`
   Das ist gut - die API funktioniert!

### Schritt 3: Python-Client einrichten

1. Installieren Sie die benötigten Python-Pakete:
   ```bash
   x:\Python313\python.exe -m pip install requests pandas
   ```

2. Öffnen Sie `db_client.py` und passen Sie die Konfiguration an:
   ```python
   self.api_url = "https://lic.prophelper.org/api/db_api.php"
   self.token = "ihr_eigenes_sicheres_token_hier_2025"  # Gleiches Token wie in PHP!
   ```

## 💻 Verwendung

### Verbindungstest

```python
from db_client import DatabaseClient

# Client initialisieren
db = DatabaseClient()

# Verbindung testen
db.test_connection()
```

### Beispiele für Datenbankoperationen

#### 1. Daten abfragen
```python
# Alle Lizenzen abrufen
licenses = db.select("SELECT * FROM lnative")

# Mit Parametern (SQL-Injection sicher)
account_licenses = db.select(
    "SELECT * FROM lnative WHERE account = ? AND status = ?",
    ['12345', 'active']
)
```

#### 2. Daten einfügen
```python
# Neue Lizenz hinzufügen
new_id = db.insert('lnative', {
    'account': '98765',
    'product': 'DAX_OVERNIGHT_EA',
    'status': 'active',
    'expiry_date': '2025-12-31'
})
print(f"Neue Lizenz ID: {new_id}")
```

#### 3. Daten aktualisieren
```python
# Lizenz verlängern
updated = db.update(
    'lnative',
    {'expiry_date': '2026-12-31'},
    'account = ?',
    ['98765']
)
print(f"{updated} Datensätze aktualisiert")
```

#### 4. Mit Lizenz-Manager arbeiten
```python
from db_client import DatabaseClient, LicenseManager

db = DatabaseClient()
licenses = LicenseManager(db)

# Lizenz prüfen
license = licenses.get_license_by_account('12345')
if license:
    print(f"Lizenz gefunden: {license}")
else:
    print("Keine Lizenz vorhanden")

# Alle aktiven Lizenzen
active = licenses.get_active_licenses()
print(f"{len(active)} aktive Lizenzen")
```

#### 5. Mit Pandas DataFrame arbeiten
```python
# Query-Ergebnis als DataFrame
licenses = db.select("SELECT * FROM lnative")
df = db.to_dataframe(licenses)

# Datenanalyse mit Pandas
print(df.describe())
print(df.groupby('status').count())
```

## 🔒 Sicherheitshinweise

1. **Token geheim halten**: Niemals das Token in öffentlichen Repositories speichern!

2. **HTTPS verwenden**: Die API sollte nur über HTTPS erreichbar sein

3. **IP-Beschränkung** (optional): In der `db_api.php` können Sie zusätzlich IP-Checks einbauen:
   ```php
   $allowed_ips = ['185.72.234.93'];
   if (!in_array($_SERVER['REMOTE_ADDR'], $allowed_ips)) {
       die(json_encode(['error' => 'IP not allowed']));
   }
   ```

4. **Rate Limiting** (optional): Begrenzen Sie die Anzahl der Requests pro Minute

5. **Logging**: Protokollieren Sie alle API-Zugriffe für Sicherheitsaudits

## 🔧 Fehlerbehebung

### Problem: "Connection failed"
- Prüfen Sie, ob die URL korrekt ist
- Prüfen Sie, ob das Token in PHP und Python identisch ist
- Testen Sie die URL im Browser

### Problem: "404 Not Found"
- Prüfen Sie den Upload-Pfad der PHP-Datei
- Stellen Sie sicher, dass der Ordner `api/` existiert

### Problem: "500 Internal Server Error"
- Prüfen Sie die PHP-Version auf dem Server (mindestens PHP 7.0)
- Prüfen Sie die Datenbankzugangsdaten in der PHP-Datei

### Problem: SSL-Zertifikatsfehler
```python
# Nur für Tests - NICHT in Produktion!
import urllib3
urllib3.disable_warnings()
db.session.verify = False
```

## 📊 Erweiterte Funktionen

### Batch-Operationen
```python
# Mehrere Inserts auf einmal
accounts = ['11111', '22222', '33333']
for account in accounts:
    db.insert('lnative', {
        'account': account,
        'product': 'DAX_EA',
        'status': 'trial'
    })
```

### Export/Import
```python
# Daten exportieren
all_data = db.select("SELECT * FROM lnative")
import json
with open('backup.json', 'w') as f:
    json.dump(all_data, f, indent=2)

# Daten importieren
with open('backup.json', 'r') as f:
    data = json.load(f)
for record in data:
    db.insert('lnative', record)
```

## ✅ Checkliste

- [ ] Token in `db_api.php` geändert
- [ ] `db_api.php` auf Server hochgeladen
- [ ] API-URL im Browser getestet
- [ ] Token in `db_client.py` angepasst
- [ ] Python-Pakete installiert (`requests`, `pandas`)
- [ ] Verbindungstest erfolgreich
- [ ] Erste Query ausgeführt

## 📞 Support

Bei Problemen prüfen Sie:
1. phpMyAdmin funktioniert: https://web-de.wishhost.net:1501/lGoJSoSPtQ0xoqNk/phpmyadmin/
2. FTP-Zugang funktioniert: 162.55.90.123
3. Die Dateien sind am richtigen Ort

Viel Erfolg mit der Datenbank-API! 🚀
