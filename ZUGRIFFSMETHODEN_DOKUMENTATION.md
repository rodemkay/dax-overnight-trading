# 📡 ZUGRIFFSMETHODEN DOKUMENTATION

## Übersicht der Kommunikationswege

### 1. EA → lic.prophelper.org (Lizenzserver)

#### Primäre Methode: WinInet (via MQL_License.mqh)
```mql5
// Verwendet in CheckRoboForexViaWinInet() und DataOnInit()
InternetOpenW()
InternetConnectW()
HttpOpenRequestW()
HttpSendRequestW()
InternetReadFile()
```

**Vorteile:**
- Funktioniert zuverlässig
- Keine WebRequest-Erlaubnis in MT5 nötig
- Direkte Windows API

**Verwendet für:**
- Server-Lizenzprüfung (DataOnInit)
- Activation() Checks
- Hardware-ID Übertragung

#### Fallback: WebRequest
```mql5
// In UpdateRoboForexStatusToServer()
WebRequest("POST", url, headers, timeout, post, result, headers);
```

**Vorteile:**
- Native MQL5 Funktion
- Einfacher zu verwenden

**Nachteile:**
- Muss in MT5 erlaubt werden (Extras → Optionen → Expert Advisors)
- URL muss in Whitelist

**Verwendet für:**
- RoboForex Status Updates (primär)

### 2. EA → my.roboforex.com (Partner API)

#### Methode: WinInet (via CheckRoboForexViaWinInet)
```mql5
string path = "/api/partners/tree?account_id=" + ROBOFOREX_PARTNER_ACCOUNT + 
              "&api_key=" + ROBOFOREX_API_KEY + 
              "&referral_account_id=" + accountNumber;
```

**Details:**
- HTTPS (Port 443)
- GET Request
- API Key: ec4d40c4343ee741
- Partner Account: 30218520

### 3. Python Scripts → lic.prophelper.org

#### FTP Zugriff
```python
import ftplib
ftp = ftplib.FTP("162.55.90.123")
ftp.login("prophelp", ".Propt333doka?")
```

**Verwendet für:**
- template.inc.php Upload/Download
- PHP Scripts Upload
- Backup-Erstellung

#### MySQL Zugriff (nur lokal möglich)
```python
# Funktioniert NUR vom Server selbst
mysql.connector.connect(
    host="162.55.90.123",
    user="prophelper",
    password=".Propt333doka?",
    database="prophelper"
)
```

**Hinweis:** Remote-Zugriff blockiert, nur via PHP API möglich

### 4. Update-Flow für RoboForex Status

```
1. EA Start (OnInit)
   ↓
2. CheckRoboForexLicense() via WinInet
   ↓
3. Partner-Status ermittelt (yes/no)
   ↓
4. UpdateRoboForexStatusToServer()
   ├── Primär: WebRequest zu update_robo_status.php
   └── Fallback: WinInet zu update_robo_status.php
   ↓
5. PHP Script schreibt in MySQL
   ↓
6. Web-Interface zeigt Status (✓/✗)
```

## Wichtige Pfade und URLs

### Server-Endpoints
- **Lizenz-Check:** https://lic.prophelper.org/connect.php (via MQL_License.mqh)
- **Status-Update:** https://lic.prophelper.org/files/update_robo_status.php
- **RoboForex API:** https://my.roboforex.com/api/partners/tree

### Lokale Dateien
- **EA:** /home/rodemkay/CaufWin11/portabel/MetaTrader5/MQL5/Experts/Don/don_gpt.mq5
- **Include:** /home/rodemkay/CaufWin11/portabel/MetaTrader5/MQL5/Include/MQL_License.mqh
- **Scripts:** /home/rodemkay/mt5/daxovernight/*.py

## Sicherheit

### Authentifizierung
1. **Server-Lizenz:** Hardware-ID + Account + Program Name
2. **RoboForex:** API Key + Partner Account + Affiliate Code
3. **FTP:** Username + Password
4. **Web-Interface:** HTTP Basic Auth (admin/admin)

### Ports
- **HTTP:** 80 (selten verwendet)
- **HTTPS:** 443 (Standard)
- **FTP:** 21 (Standard)
- **MySQL:** 3306 (nur lokal)

## Fehlerbehebung

### WebRequest funktioniert nicht
1. MT5 → Extras → Optionen → Expert Advisors
2. ✅ "WebRequest für URLs erlauben"
3. URL hinzufügen: https://lic.prophelper.org
4. URL hinzufügen: https://my.roboforex.com

### WinInet Fehler
- Prüfe Firewall-Einstellungen
- Prüfe Proxy-Einstellungen
- Wine/Linux kann Probleme verursachen

### Status wird nicht aktualisiert
1. Prüfe Experts-Tab für Fehlermeldungen
2. Prüfe ob update_robo_status.php erreichbar ist
3. Prüfe MySQL-Tabelle für roboaffiliate Spalte