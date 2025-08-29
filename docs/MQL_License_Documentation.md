# MQL_License.mqh - Vollständige Technische Dokumentation

## Übersicht
Die MQL_License.mqh ist eine professionelle Lizenzbibliothek für MetaTrader 4/5 Expert Advisors mit Hardware-Bindung, Online-Validierung und umfassenden Sicherheitsfunktionen.

## Inhaltsverzeichnis
1. [Windows API Imports](#1-windows-api-imports)
2. [MqlNet Klasse](#2-mqlnet-klasse---httphttps-kommunikation)
3. [Globale Lizenzvariablen](#3-globale-lizenzvariablen)
4. [Hauptfunktionen](#4-hauptfunktionen)
5. [Initialisierung](#5-initialisierung)
6. [UI-Funktionen](#6-ui-funktionen)
7. [Hardware-Identifikation](#7-hardware-identifikation)
8. [Profit-Tracking](#8-profit-tracking)
9. [Verschlüsselung](#9-verschlüsselung)
10. [Hilfsfunktionen](#10-hilfsfunktionen)
11. [Server-Protokoll](#11-server-protokoll)
12. [Sicherheitsfeatures](#12-sicherheitsfeatures)
13. [Integration in EA](#13-integration-in-ea)

## 1. Windows API Imports

### Shell32.dll
```cpp
int ShellExecuteW(int hwnd, string Operation, string File, 
                  string Parameters, string Directory, int ShowCmd)
```
- **Zweck**: Öffnet URLs im Standard-Browser
- **Parameter**:
  - `hwnd`: Window Handle (0 für kein Fenster)
  - `Operation`: "Open", "Print", "Explore"
  - `File`: URL oder Dateipfad
  - `Parameters`: Zusätzliche Parameter
  - `Directory`: Arbeitsverzeichnis
  - `ShowCmd`: Anzeigemodus (1 = normal)

### Kernel32.dll
```cpp
DWORD GetLastError(uint)
```
- Gibt den letzten Windows-Fehlercode zurück

```cpp
bool GetVolumeInformationW(const string root_path_name, string volume_name_buffer, 
                          uint volume_name_size, uint &volume_serial_number[], ...)
```
- Liest Laufwerksinformationen (insbesondere Seriennummer)

```cpp
uint GetSystemFirmwareTable(uint firmware_table_provider_signature, 
                           uint firmware_table_id, uchar &firmware_table_buffer[], 
                           uint buffer_size)
```
- Liest BIOS/UEFI Firmware-Tabellen (für UUID)

### Wininet.dll (Internet-Funktionen)
```cpp
DWORD InternetAttemptConnect(DWORD dwReserved)
```
- Prüft ob Internetverbindung verfügbar ist

```cpp
HINTERNET InternetOpenW(LPCTSTR lpszAgent, DWORD dwAccessType, 
                       LPCTSTR lpszProxyName, LPCTSTR lpszProxyBypass, 
                       DWORD dwFlags)
```
- Initialisiert WinInet-Bibliothek

```cpp
HINTERNET InternetConnectW(HINTERNET hInternet, LPCTSTR lpszServerName, 
                          INTERNET_PORT nServerPort, LPCTSTR lpszUsername, 
                          LPCTSTR lpszPassword, DWORD dwService, 
                          DWORD dwFlags, DWORD_PTR dwContext)
```
- Erstellt Verbindung zu Server

## 2. MqlNet Klasse - HTTP/HTTPS Kommunikation

### Struktur tagRequest
```cpp
struct tagRequest {
    string stVerb;      // HTTP-Methode: "GET" oder "POST"
    string stObject;    // Pfad: "/api/check.php?param=value"
    string stHead;      // Header: "Content-Type: application/x-www-form-urlencoded"
    string stData;      // POST-Daten oder Dateiname für Upload
    bool fromFile;      // true = stData ist Dateiname, false = direkte Daten
    string stOut;       // Antwort-String oder Dateiname für Download
    bool toFile;        // true = Antwort in Datei speichern
    
    void Init(string aVerb, string aObject, string aHead, 
              string aData, bool from, string aOut, bool to);
}
```

### MqlNet Klassenmethoden

#### Konstruktor/Destruktor
```cpp
MqlNet()  // Initialisiert alle Handles mit -1
~MqlNet() // Schließt alle offenen Verbindungen
```

#### Verbindungsverwaltung
```cpp
bool _Open(string aHost, int aPort, string aUser, string aPass, int aService)
```
- **Parameter**:
  - `aHost`: Server-Domain (z.B. "lic.prophelper.org")
  - `aPort`: 80 (HTTP) oder 443 (HTTPS)
  - `aUser`: Benutzername (optional)
  - `aPass`: Passwort (optional)
  - `aService`: INTERNET_SERVICE_HTTP (3)
- **Rückgabe**: true bei Erfolg
- **Details**:
  - Prüft DLL-Erlaubnis
  - Erstellt Internet-Session
  - Verbindet zum Server

```cpp
void _Close()
```
- Schließt Session und Connection Handles

#### Request-Funktionen
```cpp
bool Request(tagRequest &req)
```
- **Hauptfunktion für HTTP/HTTPS Requests**
- **Features**:
  - Automatische SSL-Zertifikatsfehler-Behandlung
  - Datei-Upload/Download Support
  - Wiederholung bei Fehlern (max. 2 Versuche)
- **Ablauf**:
  1. Prüft/öffnet Verbindung
  2. Erstellt HTTP Request
  3. Sendet Daten (aus String oder Datei)
  4. Empfängt Antwort (in String oder Datei)

```cpp
bool OpenURL(string aURL, string &Out, bool toFile)
```
- Vereinfachte Funktion zum URL-Lesen
- Nutzt InternetOpenUrlW() API

```cpp
void ReadPage(int hRequest, string &Out, bool toFile)
```
- Liest HTTP-Response in 100-Byte Blöcken
- Speichert in String oder Datei

```cpp
long GetContentSize(int hRequest)
```
- Ermittelt Content-Length Header
- Rückgabe: Größe in Bytes oder -1 bei Fehler

```cpp
int FileToArray(string aFileName, uchar &_data[])
```
- Liest Datei in Byte-Array für Upload
- Rückgabe: Dateigröße oder -1 bei Fehler

## 3. Globale Lizenzvariablen

```cpp
int License = 0;        // Lizenzstatus
                       // 0 = nicht geprüft
                       // 1 = ungültig/abgelaufen
                       // 2 = gültig und aktiv

bool YesKey = false;    // true wenn Lizenz aktiv und validiert

string Package = "";    // Lizenzpaket-Typ
                       // z.B. "MAX", "STANDARD", "BASIC"

string _ansTime = "";   // Ablaufdatum der Lizenz
                       // Format: "YYYY.MM.DD"

bool _email = false;    // Email-Registrierung erforderlich

int _check = 0;         // Server-Check-Intervall in Stunden
                       // 0 = 15 Minuten (Standardintervall)
                       // >0 = Stunden * 3600 + Zufallswert

long _TL = 0;          // Aktuelle Zeit (Local oder Current)

MqlDateTime dml;       // Aktuelle Zeit als Struktur
```

## 4. Hauptfunktionen

### bool Activation()
```cpp
bool Activation()
```
**Zweck**: Hauptfunktion für Lizenzprüfung
**Rückgabe**: true wenn Lizenz aktiv
**Ablauf**:
1. Im Tester-Modus: Immer true (YesKey=true, Package="MAX")
2. Prüft Account-Login-Änderungen
3. Bei fehlender Lizenz: Zeigt Kauf-UI
4. Bei Email-Problem: Zeigt Registrierungs-UI
5. Nur wenn YesKey=true und Package!="" ist EA aktiv

### bool GetAnswer()
```cpp
bool GetAnswer()
```
**Zweck**: Koordiniert Lizenzprüfung mit Server
**Details**:
- Setzt _TL basierend auf Wochentag (Wochenende=LocalTime, sonst=CurrentTime)
- Ruft IsDelay() für Timing-Check
- Ruft SendServer() für Server-Validierung
- Aktualisiert UI bei Statusänderungen
- Verwaltet License-Variable (0→1→2)

### bool SendServer()
```cpp
bool SendServer()
```
**Zweck**: Kommunikation mit Lizenzserver
**Datensammlung**:
```cpp
// Account-Daten
accL: Login-Nummer
accN: Account-Name
accC: Broker-Company
acct: Trade-Mode (Demo/Real)
accS: Server-Name
accCurr: Kontowährung
accTA: Trade-Allowed Status
accO: Order-Limit
accB: Balance
accE: Equity

// Profit-Daten
acpr: Gesamtprofit für Magic Number
accH: Format "Tag~Woche~Monat:Profit~Monat:Profit"

// System-Daten
prog: Programmname
vers: Version
mt: "4" oder "5"
ref: Referrer-Code
perc: Provision in %
driveID: Laufwerks-Seriennummer
UUID: System-UUID aus BIOS
code: Zusätzlicher Code
check: Check-Intervall
```

**Verschlüsselung**:
```cpp
salt = Zufallszahl 1000-9999
key = "h4yT!H3/dA3K9z" + salt + "trl/xdFgj#erPjm"
psalt = CryptEncodeA(salt, "jlY2E9rz/qJOd1S#G!28/k10C3!Skuo")
data = "r1=" + psalt + "$" + CryptEncodeA(rs1, key) + "$" + CryptEncodeA(rs2, key)
```

**Server-Antwort** (6 Felder getrennt durch '|'):
1. Ablaufdatum ("YYYY.MM.DD") oder Fehlercode
2. Paketname ("MAX", "STANDARD", etc.)
3. Status ("Registered") oder neue Version
4. Update-Nachricht (optional)
5. Check-Intervall in Stunden
6. Reserviert

**Fehlerbehandlung**:
- "::503 Service Unavailable"
- "::404 Program not registered"
- "Email not registered"
- Nach 3 Fehlversuchen: Deaktivierung

## 5. Initialisierung

### bool DataOnInit(...)
```cpp
bool DataOnInit(string _domen_, int _port_, string _program_, 
                string _prog_, string _version_, string _URLbuy_, 
                string _URLupdate_, string _ref_, int _perc_, 
                int _tx_sh_, int _mg_, string _code_)
```

**Parameter**:
- `_domen_`: Lizenzserver-Domain (z.B. "lic.prophelper.org")
- `_port_`: Server-Port (80 oder 443)
- `_program_`: Original EA-Name (für Umbenennungs-Check)
- `_prog_`: Aktueller Dateiname (__FILE__)
- `_version_`: EA-Version (z.B. "1.27")
- `_URLbuy_`: URL für Lizenzkauf
- `_URLupdate_`: URL für Updates
- `_ref_`: Referrer-Code für Provisionen
- `_perc_`: Provisionssatz in Prozent
- `_tx_sh_`: UI-Position von oben (Pixel)
- `_mg_`: Magic Number für Profit-Tracking (-1 = alle)
- `_code_`: Zusätzlicher Identifikationscode

**Funktionalität**:
1. Setzt Codepage (CP_ACP)
2. Initialisiert globale Strukturen (idt, aInf)
3. Liest Hardware-IDs:
   - UUID via SMBIOS::Read()
   - Laufwerks-Seriennummer
4. Sammelt Account-Informationen
5. Prüft Programm-Umbenennung
6. Erstellt "Site" Button (rechts unten)

**Sicherheit**:
- Bei Umbenennung: Alert + ExpertRemove()
- Rückgabe: false bei Erfolg, true bei Fehler

### void DataOnDeinit(int reason)
```cpp
void DataOnDeinit(int reason = 0)
```
- Löscht alle UI-Objekte (Warning_*, Site)
- Aktualisiert Chart

## 6. UI-Funktionen

### void lSetLabel(...)
```cpp
void lSetLabel(int nwin=0, string nm="Label", string tx="txt", 
               color clr=clrRed, int xd=0, int yd=0, 
               ENUM_BASE_CORNER cr=0, int _font_size=8, 
               string font="Arial", ENUM_ANCHOR_POINT an=0, 
               bool sel=false, bool back=false, string tooltip="")
```

**Zweck**: Erstellt/aktualisiert Text-Labels
**Features**:
- Automatische Erstellung wenn nicht vorhanden
- Position relativ zu Corner
- Anchor-Point für präzise Ausrichtung
- Tooltip-Support

**Verwendung für Lizenz-UI**:
- Warnmeldungen (rot)
- Status-Anzeigen (türkis/blau)
- Ablauf-Warnungen (orange)

### void lButtonCreate(...)
```cpp
void lButtonCreate(string name="Button", int _xx=0, int _yy=0, 
                   int _width=50, int _height=18,
                   ENUM_BASE_CORNER _corner=CORNER_LEFT_UPPER, 
                   string _text="Button", string _tooltip="Button",
                   string _font="Arial", int _font_size=10, 
                   color _clr=clrBlack, color _back_clr=C'236,233,216')
```

**Zweck**: Erstellt interaktive Buttons
**Button-Typen**:
- `Warning_b`: Kauf-Button
- `Warning_bu`: Update-Button  
- `Warning_be`: Email-Registrierung
- `Site`: Webseiten-Link

### void ChartEventA(const int _id_, const string _sparam_)
```cpp
void ChartEventA(const int _id_, const string _sparam_)
```

**Zweck**: Verarbeitet Chart-Events (Button-Klicks)
**Aktionen**:
- Öffnet URLs via ShellExecuteW()
- Setzt Button-State zurück
- Löscht Warnmeldungen bei Klick auf Label

## 7. Hardware-Identifikation

### string SystemDriveSerialNumber()
```cpp
string SystemDriveSerialNumber()
```
**Ablauf**:
1. Versucht GetVolumeInformationW("C:\\")
2. Bei Erfolg: Konvertiert zu Hex "XXXX-XXXX"
3. Bei Fehler: Nutzt GetID() als Fallback

### string GetID()
```cpp
string GetID()
```
**Zweck**: Persistente ID aus Datei
**Ablauf**:
1. Prüft "mqlfil.dat" in FILE_COMMON
2. Wenn nicht vorhanden:
   - Generiert ID aus TimeLocal()
   - Speichert in Datei
3. Wenn vorhanden: Liest gespeicherte ID
**Format**: Hexadezimal-String

### class SMBIOS
```cpp
class SMBIOS {
    static UUID16 uuid;
    static string Read();
}
```

**UUID16 Union**:
```cpp
union UUID16 {
    uchar b[16];  // 16 Bytes für System-UUID
}
```

**SMBIOS::Read()**:
**Zweck**: Liest System-UUID aus BIOS/UEFI
**Ablauf**:
1. GetSystemFirmwareTable('RSMB', 0, ...) für Größe
2. Allokiert Buffer und liest Daten
3. Parst SMBIOS-Struktur:
   - Sucht Type 1 (System Information)
   - Offset 8: UUID (16 Bytes)
4. Prüft auf ungültige UUIDs (alle 0x00 oder 0xFF)
5. Formatiert als Standard-UUID:
   "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

**SMBIOS Struktur-Details**:
- Type 1 beginnt mit: [Type=1][Length][Handle]
- UUID bei Offset 8 vom Type-1 Header
- Byte-Order: Mixed Endian (erste 3 Gruppen reversed)

## 8. Profit-Tracking

### string _GetProfitMG(long _mg_)
```cpp
string _GetProfitMG(long _mg_)
```
**Parameter**: 
- `_mg_`: Magic Number (-1 = alle Trades)
**Rückgabe**: Gesamtprofit als String
**Details**:
- Durchsucht komplette History
- Nur geschlossene Trades (Type < 2)
- Inklusive Commission + Swap + Fee (MT5)

### string GetProfit(ENUM_TIMEFRAMES _p_, int _n_)
```cpp
string GetProfit(ENUM_TIMEFRAMES _p_, int _n_)
```
**Parameter**:
- `_p_`: Zeitrahmen (D1, W1, MN1)
- `_n_`: Shift (0=aktuell, 1=vorherig)
**Rückgabe**: Profit für Zeitraum
**Logik**:
- _n_=0: Trades seit Periodenbeginn
- _n_>0: Trades in vorheriger Periode
- Nutzt iTime() für Zeitgrenzen

## 9. Verschlüsselung

### string CryptEncodeA(string InputText, string key)
```cpp
string CryptEncodeA(string InputText, string key)
```
**Ablauf**:
1. String → uchar Array
2. AES256-Verschlüsselung mit 32-Byte Key
3. Base64-Encoding des Ergebnisses
4. Rückgabe als String

### string CryptDecodeA(string InputText, string key)
```cpp
string CryptDecodeA(string InputText, string key)
```
**Ablauf**:
1. Base64-Decoding
2. AES256-Entschlüsselung
3. uchar Array → String (mit ArrayToString)

**Wichtig**: Key muss genau 32 Zeichen lang sein!

## 10. Hilfsfunktionen

### bool IsDelay()
```cpp
bool IsDelay()
```
**Zweck**: Verhindert zu häufige Server-Anfragen
**Logik**:
```cpp
_delay = _check==0 ? 15 : _check*3600 + (rand()%299+1)
```
- Erste Prüfung: 15 Minuten
- Weitere: _check Stunden + Zufallswert (1-299 Sek)

**GlobalVariables**:
- `prog_g`: Für License==1 (nicht lizenziert)
- `prog_q`: Für License==2 (lizenziert)
- Divisor: 590.0 bzw. 790.0

### String-Konvertierungen
```cpp
string DecToHex(int n)          // Dezimal → Hex
string HexToInteger(string str) // Hex → Integer (custom)
string IntegerToHexString(uint num) // Integer → Hex (optimiert)
```

### Zufallszahlen
```cpp
int rndr(int mn, int mx, bool inclusive=true)
int rndn(int n)  // Gleichverteilte Zufallszahl 0 bis n-1
```

### template ArrayToString
```cpp
template<typename TChar>
string ArrayToString(const TChar &input_array[], 
                    bool remove_non_printable=false, 
                    int start=0, int count=-1, int codepage=CP_ACP)
```
**Features**:
- Template für uchar/short Arrays
- Filtert nicht-druckbare Zeichen
- Unterstützt verschiedene Codepages
- Stoppt bei Null-Terminator

## 11. Server-Protokoll

### Request-Format
```
POST /metatrader HTTP/1.1
Host: lic.prophelper.org
Content-Type: application/x-www-form-urlencoded

r1=[encrypted_salt]$[encrypted_data1]$[encrypted_data2]
```

### Datenstruktur
**rs1** (Account & Program):
```
AccLogin|AccName|AccCompany|Program|TradeMode|Version|MT|Ref|Percent|Balance|Equity
```

**rs2** (System & Profit):
```
ProfitMG|Server|Currency|TradeAllowed|DriveID|UUID|Code~ProfitHistory|Check|OrderLimit
```

**ProfitHistory Format**:
```
DayProfit~WeekProfit~LastMonth:MonthProfit~CurrentMonth:MonthProfit
```

### Server-Antworten

**Erfolg** (6 Felder):
```
2025.12.31|MAX|Registered|UpdateMsg|24|Reserved
```

**Fehler** (2 Felder):
```
::404 Program not registered|Details
::503 Service Unavailable|Retry later
```

**Spezielle Status**:
- "Email not registered" → Registrierungs-Button
- Versionsnummer → Update-Button
- Ablaufdatum < 24h → Verlängerungs-Button

## 12. Sicherheitsfeatures

### 1. Anti-Manipulation
- **Programm-Umbenennung**: Sofortige Deaktivierung
- **Hardware-Bindung**: UUID + Laufwerk
- **Account-Bindung**: Login-Nummer
- **Zeitvalidierung**: Server-basiert

### 2. Verschlüsselung
- **Transport**: AES256 + Base64
- **Dynamischer Salt**: 4-stellig, pro Request
- **Key-Generierung**: Salt in Key integriert

### 3. Zeitkontrolle
- **Verzögerte Prüfungen**: Verhindert Überlastung
- **GlobalVariables**: Persistente Zeitstempel
- **Wochenend-Modus**: LocalTime statt ServerTime

### 4. UI-Sicherheit
- **Visuelle Warnungen**: Rot bei Problemen
- **Interaktive Buttons**: Direkte Aktionen
- **Auto-Cleanup**: OnDeinit löscht UI

## 13. Integration in EA

### Minimal-Beispiel
```cpp
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
#define program "MyEA"
#define release "1.0"
#define ref "REF"
#define perc 35
#define domen "lic.prophelper.org"
input prt port = 443;
#define URLbuy "https://lic.prophelper.org/buy.php"
#define URLupdate "https://lic.prophelper.org/download.php"

#include <MQL_License.mqh>

int OnInit() {
    int MG = 12345; // Magic Number
    if(DataOnInit(domen, port, program, __FILE__, release,
                  URLbuy, URLupdate, ref, perc, 20, MG, ""))
        return(INIT_FAILED);
    return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason) {
    DataOnDeinit();
}

void OnTick() {
    if(!Activation()) {
        // Zeigt Lizenz-UI, EA inaktiv
        return;
    }
    if(YesKey == false) return;
    if(Package == "") return;
    
    // Ihr EA-Code hier
    // Lizenz ist aktiv, Package enthält Lizenztyp
}

void OnChartEvent(const int id, const long &lparam,
                  const double &dparam, const string &sparam) {
    ChartEventA(id, sparam);
    // Ihr Event-Code
}
```

### Erweiterte Integration
```cpp
// Lizenztyp-basierte Features
if(Package == "MAX") {
    // Alle Features aktiv
} else if(Package == "STANDARD") {
    // Standard Features
} else if(Package == "BASIC") {
    // Basis Features
}

// Ablaufdatum prüfen

## 7. Bekannte Probleme und Lösungen (Stand: 03.08.2025)

### Hardware-ID Bindung
**Problem**: "The number of activations has ended: 1"
- Dies ist KEINE Begrenzung der Anzahl, sondern eine Hardware-Bindung
- Server speichert die erste Hardware-ID und lehnt andere ab

**Lösung**:
1. Server-seitig: In `metatrader.php` Zeile 177-181 auskommentieren
2. Client-seitig: `//#define USE_SERVER_LICENSE` setzen

### Fehler 12029 (ERROR_INTERNET_CANNOT_CONNECT)
**Problem**: EA kann Lizenzserver nicht erreichen
- Häufig auf Linux/Wine
- Firewall/DNS Probleme

**Lösung**: Server-Lizenzierung deaktivieren

### Access Violation auf Linux/Wine
**Problem**: Absturz bei Adresse 0x00006FFFFF4F24D3
- Wine-spezifisches Problem mit Windows API Calls

**Lösung**: Server-Lizenzierung deaktivieren

### Server-Konfiguration (Datei: names)
```
programm~version~typ~tage~UUID-limit~account-limit~check~nachricht
daxovernight~1.00~Full~10~30~50~1~~
```

### Datenbank-Struktur (Tabelle: lnative)
- `serialNo`: Hardware-ID der Installation
- `connect`: Anzahl aktiver Verbindungen
- `deactivate_date`: Lizenzablauf
if(StringLen(_ansTime) == 10) {
    datetime expiry = StringToTime(_ansTime);
    int daysLeft = (int)((expiry - TimeCurrent()) / 86400);
    Print("Lizenz läuft in ", daysLeft, " Tagen ab");
}

// Profit-Tracking nutzen
string monthProfit = GetProfit(PERIOD_MN1, 0);
Print("Profit diesen Monat: ", monthProfit);
```

### Debugging
```cpp
// Lizenzstatus prüfen
Print("License: ", License, " YesKey: ", YesKey, 
      " Package: ", Package, " Expires: ", _ansTime);

// Hardware-IDs anzeigen
Print("UUID: ", idt._UUID);
Print("Drive: ", idt._driveID);
Print("Account: ", aInf.accL);
```

## Wichtige Hinweise

1. **Server-Credentials**: Die server_credentials.txt enthält sensible Daten und darf NIEMALS öffentlich geteilt werden!

2. **Tester-Modus**: Im Strategy Tester ist die Lizenz immer aktiv (Package="MAX")

3. **DLL-Erlaubnis**: Muss in MT4/5 aktiviert sein, sonst Fehlermeldung

4. **Zeitzone**: Wochenende nutzt LocalTime, Wochentage CurrentTime

5. **Magic Number**: -1 bedeutet alle Trades werden getrackt

6. **Update-Check**: Bei Versionsdifferenz wird Update-Button angezeigt

7. **Email-Registrierung**: Einmalig erforderlich für Account-Bindung

Diese Dokumentation deckt alle Aspekte der MQL_License.mqh ab und sollte als Referenz für die Integration und Wartung dienen.