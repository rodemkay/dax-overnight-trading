# Testzeitraum-Management Implementierung

## ✅ Version 1.25 - Erfolgreich implementiert!

### EA-Seite (the_don v1.25)
1. **Stop-Loss Prozent-Modus**
   - Neuer Parameter: `StopLossMode` (SL_POINTS / SL_PERCENT)
   - `StopLossPercent` für prozentuale Berechnung
   - Berechnung: `sl = ask * (1 - StopLossPercent/100)`

2. **EA sendet bereits alle benötigten Daten**:
   - `req1`: ACCOUNT_LOGIN (Kontonummer)
   - `req2`: ACCOUNT_NAME (Name des Accounts) ⭐ WICHTIG für Testzeitraum
   - `req4`: PROGRAM_NAME (z.B. "the_don")
   - `req6`: VERSION (z.B. "1.25")
   - `req5`: ACCOUNT_TYPE (Demo/Real)
   - `req13`: SERVER_NAME

### Server-Seite (PropHelper)

#### 1. Datenbank-Tabelle erstellt ✅
```sql
CREATE TABLE test_period_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_name VARCHAR(255),      -- Name aus MT5
    program_name VARCHAR(100),      -- EA-Name
    program_version VARCHAR(50),    -- Version
    first_test_date DATETIME,
    test_count INT DEFAULT 1,
    account_type VARCHAR(20),
    account_number VARCHAR(50),
    server_name VARCHAR(255),
    UNIQUE KEY (account_name, program_name, program_version)
)
```

#### 2. PHP-Logik implementiert ✅
**Dateien auf Server:**
- `test_period_check.inc.php` - Testzeitraum-Funktionen
- `metatrader.php` - Modifiziert mit Testzeitraum-Check
- `metatrader_backup_20250829.php` - Backup der Original-Version

#### 3. Prioritäten-Hierarchie:
1. **RoboForex Affiliate** → Immer erlaubt (unbegrenzt)
2. **Server-Lizenz** → Überschreibt Testzeitraum
3. **Testzeitraum** → 1x pro Name+EA+Version (14 Tage)

### Funktionsweise:

1. **Erster Start eines neuen Accounts:**
   - EA sendet Account-Name "Max Mustermann" + "the_don" + "1.25"
   - Server prüft: Noch kein Eintrag → Testzeitraum aktiviert
   - 14 Tage kostenlose Nutzung

2. **Zweiter Start mit gleichem Account:**
   - Gleicher Name + EA + Version
   - Server prüft: Eintrag vorhanden → Testzeitraum bereits genutzt
   - Zugang verweigert (außer RoboForex oder Server-Lizenz)

3. **Neue Version:**
   - "Max Mustermann" + "the_don" + "1.26"
   - Neue Kombination → Neuer Testzeitraum möglich

4. **Anderer EA:**
   - "Max Mustermann" + "breakout_brain" + "1.0"
   - Andere EA → Neuer Testzeitraum möglich

### Test-URLs:
- Tabellen-Status: https://lic.prophelper.org/files/create_test_period_table.php
- Dashboard: https://lic.prophelper.org/connect (admin/admin)

### Wichtige Hinweise:
- ⚠️ EA muss Account-NAME senden, nicht nur Nummer
- ✅ Funktioniert für DEMO und LIVE Konten
- ✅ Pro Version neuer Testzeitraum möglich
- ✅ Verschiedene EAs = separate Testzeiträume

### Nächste Schritte:
1. ✅ EA v1.25 in MetaTrader testen
2. ✅ Prüfen ob Account-Name korrekt übertragen wird
3. 🔄 Dashboard-Interface für Testzeitraum-Verwaltung (optional)
4. 🔄 Konfigurierbare Testzeitraum-Tage (aktuell fix 14 Tage)

### Backup & Rollback:
Falls Probleme auftreten:
```bash
# Rollback auf Server:
# 1. FTP zu lic.prophelper.org/files/
# 2. Rename: metatrader.php → metatrader_with_test.php
# 3. Rename: metatrader_backup_20250829.php → metatrader.php
```

## Status: ✅ PRODUKTIV - System ist live!