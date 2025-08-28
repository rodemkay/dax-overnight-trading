# 📊 CONNECT vs OFFICE - Dokumentation

## Übersicht der Web-Interfaces

### 🔵 /connect (connect.php)
**URL:** https://lic.prophelper.org/connect  
**Titel:** "Auto registration"  
**Zweck:** Automatische Registrierung neuer Lizenzen  
**Zugang:** HTTP Basic Auth (admin/admin)

#### Funktionen:
- **Primär:** Neue EA-Installationen registrieren sich automatisch
- **Anzeige:** Alle auto-registrierten Accounts
- **Filter:** Nach Program Name (z.B. don_gpt)
- **Test-Flag:** test=2 (Connect-Modus)

#### Besonderheiten:
- EA sendet bei erstem Start Daten hierher
- Hardware-ID wird automatisch erfasst
- Account-Nummer wird gespeichert
- 10 Tage Auto-Trial möglich (konfiguriert in /files/names)

### 🔴 /office (office.php)
**URL:** https://lic.prophelper.org/office  
**Titel:** "Purchases"  
**Zweck:** Verwaltung gekaufter Lizenzen  
**Zugang:** HTTP Basic Auth (admin/admin)

#### Funktionen:
- **Primär:** Manuelle Lizenzverwaltung
- **Anzeige:** Gekaufte/permanente Lizenzen
- **Admin-Features:** Erweiterte Bearbeitungsmöglichkeiten
- **Test-Flag:** test=1 (Office-Modus)

#### Besonderheiten:
- Nur für Administrator-Zugriff
- Kann Lizenzen verlängern/deaktivieren
- Zahlungsstatus verwaltbar
- Mehr Bearbeitungsoptionen

## 🔄 Gemeinsame Basis: template.inc.php

Beide Interfaces nutzen **dieselbe** template.inc.php Datei!

```php
// In connect.php:
require "template.inc.php";

// In office.php:
require "template.inc.php";
```

### Template unterscheidet via:
```php
$url = ($_SERVER['PHP_SELF'] == '/office') ? 1 : 2;
// 1 = Office Mode
// 2 = Connect Mode
```

## 📋 Datenbank-Struktur

### Tabelle: lnative
```sql
-- Wichtige Felder:
test         INT      -- 1=Office, 2=Connect
program      VARCHAR  -- z.B. 'don_gpt'
account      VARCHAR  -- MT5 Account
accountLogin VARCHAR  -- Alternative Account-Anzeige
roboaffiliate VARCHAR -- 'yes'/'no' Partner-Status
serialNo     VARCHAR  -- Hardware-ID
full_name    VARCHAR  -- Benutzername
last_connect INT      -- Unix Timestamp
deactivate_date DATE  -- Lizenz-Ablauf
```

## 🔀 Workflow

### Neue Installation:
1. EA startet → sendet Daten an /connect
2. Auto-Registrierung mit test=2
3. 10 Tage Trial (aus /files/names)
4. Erscheint in /connect Liste

### Lizenz-Kauf:
1. Admin ändert in /office
2. test=1 setzen (Office-Modus)
3. deactivate_date verlängern
4. payment Status ändern

### RoboForex-Integration:
1. EA prüft Partner-Status bei Start
2. Sendet Update an update_robo_status.php
3. Spalte `roboaffiliate` wird aktualisiert
4. Beide Interfaces zeigen ✓/✗ Status

## 🎨 Visuelle Unterschiede

### /connect:
- Hintergrund: Hellrosa (#FFE4E1)
- Header: "Auto registration"
- Buttons: Download, Purchases (→office)
- Focus: Neue Registrierungen

### /office:
- Hintergrund: Standard
- Header: "Purchases"  
- Buttons: Download, Auto registration (→connect)
- Focus: Verwaltung

## 📁 Datei-Struktur

```
/www/lic.prophelper.org/
├── connect              # Rewrite → files/connect.php
├── office               # Rewrite → files/office.php
├── files/
│   ├── connect.php      # Auto-Registration Interface
│   ├── office.php       # Admin Interface
│   ├── template.inc.php # Gemeinsame Tabellen-Logik
│   ├── session.php      # Session-Management
│   ├── update.php       # AJAX Updates
│   ├── style.css        # Styling
│   └── .htaccess        # URL Rewriting + Auth
```

## 🔐 Sicherheit

### .htaccess Regeln:
```apache
# URL Rewriting
RewriteRule ^connect$ /files/connect.php [L]
RewriteRule ^office$ /files/office.php [L]

# HTTP Basic Auth
<FilesMatch "office\.php|connect\.php">
AuthType Basic
AuthName "Private zone"
AuthUserFile /files/hpassword
require valid-user
</FilesMatch>
```

## 💡 Wichtige Hinweise

1. **Änderungen in template.inc.php wirken auf BEIDE Interfaces!**
2. **RoboForex-Spalte erscheint in beiden Listen**
3. **test=1 (Office) hat Priorität über test=2 (Connect)**
4. **Accounts können zwischen beiden Modi wechseln**
5. **Del-Button löscht komplett aus Datenbank**

## 🚀 Praktische Nutzung

### Für EA-Entwickler:
- Neue Installationen → /connect prüfen
- Trial-Lizenzen → automatisch 10 Tage
- Partner-Status → RoboForex-Spalte

### Für Administratoren:
- Lizenzverwaltung → /office
- Zahlungen erfassen → Payment-Spalte
- Verlängerungen → Expire Date ändern

### Für Support:
- Problem-Diagnose → beide Interfaces prüfen
- Account-Suche → Filter nach Program/Account
- Status-Check → RoboForex ✓/✗ Spalte