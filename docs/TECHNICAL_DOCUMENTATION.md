# Technische Dokumentation - DAX Overnight EA (don_gpt)

## 🔧 Technische Architektur

### MQL5 Code-Struktur
```
don_gpt.mq5
├── Defines & Properties
├── Include: MQL_License.mqh
├── Input Parameter (Gruppen)
├── Globale Variablen
├── OnInit() - Initialisierung
├── OnTick() - Hauptlogik
├── Trading-Funktionen
├── Filter-Funktionen
└── Lizenz-Funktionen
```

### Encoding & Kompilierung
- **File Encoding:** UTF-16 LE (WICHTIG!)
- **Compiler:** MetaEditor (MT5)
- **Target:** .ex5 executable
- **Keine Emojis in Print()** - führt zu Compiler-Fehlern

## 📡 Lizenzierungs-System

### 1. Server-Lizenz (MQL_License.mqh)
```cpp
// Kommunikation über WinInet API
DataOnInit() → Initialisierung
Activation() → Lizenz-Prüfung
DataOnDeinit() → Cleanup

// Server-Konfiguration
DOMEN = "lic.prophelper.org"
Port = 443 (HTTPS)
PROGRAM_NAME = "don_gpt"
LICENSE_CODE = "DAXON10"
```

### 2. RoboForex Partner API
```cpp
// API-Endpunkt
https://my.roboforex.com/api/partners/tree

// Parameter
account_id = 30218520
api_key = ec4d40c4343ee741
referral_account_id = [MT5-Kontonummer]

// Prüflogik
- Einmalige Prüfung in OnInit()
- Status wird gespeichert
- Keine periodische Neuprüfung
```

### 3. Hardware-ID System
```cpp
// Generierung
GetVolumeInformation() → SerialNumber
MQL5InfoString(MQL5_PROGRAM_PATH) → Path Hash
Kombination → Unique Hardware ID

// Speicherung
GlobalVariableSet("MACHINE_GUID", serialNo)
```

## 🗄️ Datenbank-Schema

### Tabelle: prophelp_users_1.lnative
```sql
CREATE TABLE lnative (
    id INT AUTO_INCREMENT PRIMARY KEY,
    program VARCHAR(50),        -- 'don_gpt'
    accountLogin VARCHAR(50),   -- MT5 Kontonummer
    serialNo VARCHAR(255),      -- Hardware-ID
    deactivate_date DATE,       -- Lizenz-Ablauf
    roboaffiliate TINYINT(1),   -- Partner-Status
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Server-Konfiguration (/files/names)
```
don_gpt~2.00~Full~10~9999~9999~1~~
│      │    │    │   │    │    │
│      │    │    │   │    │    └─ Check-Intervall (Stunden)
│      │    │    │   │    └─ Max Accounts
│      │    │    │   └─ Max Hardware-IDs
│      │    │    └─ Auto-Registrierung (Tage)
│      │    └─ Lizenz-Typ
│      └─ Version
└─ Program Name
```

## 🔄 Trading-Logik

### Position-Öffnung (18:00 Uhr)
```cpp
OpenPosition() {
    1. Prüfe Handelstag
    2. Prüfe StochRSI Filter
    3. Prüfe ATR Filter
    4. Berechne Lot-Größe
    5. Setze Stop-Loss
    6. Sende Buy-Order
}
```

### Position-Management
```cpp
// Trailing Stop (ab 09:00)
if (EnableTrailingStop && next_day) {
    new_sl = bid - TrailingStopPoints * point;
    if (new_sl > current_sl) {
        trade.PositionModify(ticket, new_sl, 0);
    }
}

// Position schließen (09:00)
if (!EnableTrailingStop && next_day) {
    trade.PositionClose(ticket);
}
```

## 🔍 Filter-Implementierung

### StochRSI Filter
```cpp
// Interne Berechnung (nicht extern Indikator)
1. RSI berechnen (14 Perioden, D1)
2. Min/Max der letzten 14 RSI-Werte
3. StochRSI = (RSI - Min) / (Max - Min) * 100
4. Trade nur wenn > 50
```

### ATR Filter
```cpp
// Volatilitätsprüfung
ATR = iATR(Symbol, H1, 14)
if (ATR / Point < 100) return false;  // Min 100 Punkte
```

## 🌐 Netzwerk-Kommunikation

### WinInet API (MQL_License.mqh)
```cpp
MqlNet net;
net._Open(host, port, user, pass, INTERNET_SERVICE_HTTP);
net.Request(tagRequest);
// Kein WebRequest() nötig!
```

### Error Handling
```cpp
// Verbindungsfehler
if (!net._Open()) {
    Print("Connection failed");
    return false;
}

// Response validierung
if (StringFind(response, "Registered") >= 0) {
    // Lizenz gültig
}
```

## ⚙️ Performance-Optimierungen

### Backtest-Modus
```cpp
if (MQLInfoInteger(MQL_TESTER)) {
    // Deaktiviere Lizenzprüfung
    // Vereinfache Filter
    // Reduziere Logging
}
```

### Periodische Prüfungen
```cpp
// Server-Check nur alle X Minuten
if (TimeCurrent() - lastServerCheck >= serverCheckPeriod) {
    Activation();
    lastServerCheck = TimeCurrent();
}
```

## 🔐 Sicherheit

### Kritische Credentials
```cpp
// NIEMALS in GitHub!
const string ROBOFOREX_API_KEY = "ec4d40c4343ee741";
const string FTP_PASSWORD = ".Propt333doka?";
```

### Zugriffskontrolle
- Hardware-ID Bindung
- Kontonummer Verifizierung
- Zeitbasierte Limits
- Partner-Status Prüfung

## 🐛 Bekannte Probleme & Lösungen

### 1. UTF-16 Encoding
**Problem:** MQL5 erwartet UTF-16 LE
**Lösung:** Notepad++ → Encoding → UCS-2 LE BOM

### 2. WebRequest Fehler
**Problem:** "no permission for WebRequest"
**Lösung:** MT5 → Extras → Optionen → Expert Advisors → URL erlauben

### 3. Hardware-ID Mismatch
**Problem:** Lizenz nach PC-Wechsel ungültig
**Lösung:** Datenbank-Update oder neue Registrierung

### 4. Wine/Linux Probleme
**Problem:** GetVolumeInformation() liefert andere IDs
**Lösung:** Native Windows-Installation verwenden

## 📋 Deployment Checklist

### Vor Produktiv-Einsatz
- [ ] Lizenz-Server erreichbar (ping lic.prophelper.org)
- [ ] Datenbank-Eintrag vorhanden
- [ ] Hardware-ID registriert
- [ ] Partner-Account verifiziert
- [ ] WebRequest URLs erlaubt
- [ ] Indikator installiert (Stochastics_RSI.ex5)
- [ ] Include-Datei vorhanden (MQL_License.mqh)
- [ ] EA kompiliert ohne Fehler

### Test-Protokoll
1. Backtest mit historischen Daten
2. Demo-Account Test (1 Woche)
3. Live-Account mit Min-Lot (0.01)
4. Schrittweise Erhöhung

---
Stand: 08.11.2025 | Version: don_gpt v2.00
