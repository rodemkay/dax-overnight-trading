//+------------------------------------------------------------------+
//|                                                       the_don.mq5|
//|                          DAX Overnight EA with License System   |
//|                                             Integrated Version  |
//+------------------------------------------------------------------+
#property copyright "DAX Overnight Trading System"
#property link      "www.forexsignale.trade/daxovernight"
#property version   "1.25"
#property strict

//+++ Server-Lizenzierung Defines +++
#define PROGRAM_NAME "the_don"     
#define release      "1.25"               
#define REF          "FS_TRADE"          
#define PERC         0                   
#define DOMEN        "lic.prophelper.org"
#define URLBUY       "https://lic.prophelper.org/download.php"
#define URLUPDATE    "https://lic.prophelper.org/download.php"
#define SHTXT        20                  
#define LICENSE_CODE "THEDON"           

// Server Port Enum
enum prt {
    pr80 = 80,    // HTTP Port
    pr443= 443    // HTTPS Port
};

// Include License System
#include <MQL_License.mqh>
#include <Trade\Trade.mqh>

// Externe Variable aus MQL_License.mqh für Lizenz-Ablaufdatum
extern string _ansTime;  // Format: "YYYY.MM.DD" vom Server

// Global Trade Object
CTrade trade;

// Trade Status Tracking
string lastTradeStatus = "";           // "SUCCESS" oder "REJECTED"
string lastRejectionReason = "";       // Grund für letzten abgelehnten Trade
datetime lastTradeAttemptTime = 0;     // Zeit des letzten Trade-Versuchs
double lastTradeLotSize = 0;           // Lotsize des letzten erfolgreichen Trades
string lastTradeSymbol = "";           // Symbol des letzten Trades
string todayRejectionReason = "";      // Heutiger Ablehnungsgrund

//--- Gruppen-Definition für Input-Parameter ---

//+------------------------------------------------------------------+
//| Gruppe: Lizenzierung                                            |
//+------------------------------------------------------------------+
input group "════════ LIZENZIERUNG ════════"
input prt     serverPort     = pr443;               // Server Port
input bool    UseRoboForexCheck = true;             // Affiliate-Verifikation aktivieren

input group "════════ ANZEIGE & LOGGING ════════"
input bool    ShowLicenseInfo = true;               // Status-Info im Chart anzeigen
input bool    ShowPerformance = true;               // Symbol Performance anzeigen
input bool    ShowTradeStatus = true;               // Trade-Status anzeigen (Erfolg/Ablehnung)
input bool    EnableTradeLogging = true;            // Journal-Logging für Trades aktivieren
input bool    EnableBacktestLogging = false;        // Journal-Logging im Backtest (Standard: AUS)

//+------------------------------------------------------------------+
//| Gruppe: Haupt-Einstellungen                                     |
//+------------------------------------------------------------------+
input group "════════ HAUPT-EINSTELLUNGEN ════════"
input bool    UseCoreStrategy = false;              // Core Strategy (18:00 rein, 09:05 raus, kein SL)
input int     MaxSimultaneousPositions = 7;         // Max. gleichzeitige Positionen (0 = unbegrenzt)
input bool    UsePreFilter = true;                  // Pre-Filter (versteckte Filter) aktivieren
input int     MagicNumber = 123456;                 // Magic Number für diesen EA

//+------------------------------------------------------------------+
//| Gruppe: Handelszeiten                                           |
//+------------------------------------------------------------------+
input group "════════ HANDELSZEITEN ════════"
input int     StartHourBuy = 18;                    // Kaufzeit (Stunde)
input int     StartMinuteBuy = 0;                   // Kaufzeit (Minute)
input int     CloseHour = 9;                        // Schließzeit (Stunde)
input int     CloseMinute = 0;                      // Schließzeit (Minute)

//+------------------------------------------------------------------+
//| Gruppe: Handelstage                                             |
//+------------------------------------------------------------------+
input group "════════ HANDELSTAGE ════════"
input bool    TradeMonday = true;                   // Montag handeln
input bool    TradeTuesday = true;                  // Dienstag handeln
input bool    TradeWednesday = true;                // Mittwoch handeln
input bool    TradeThursday = true;                 // Donnerstag handeln
input bool    TradeFriday = true;                   // Freitag handeln

//+------------------------------------------------------------------+
//| Gruppe: Positionsgrößen                                         |
//+------------------------------------------------------------------+
input group "════════ POSITIONSGRÖSSEN ════════"
input double  StartLotSize = 0.05;                  // Basis Lot-Größe
input bool    UseAutoLot = true;                    // AutoLot verwenden
input double  AutoLotBalance = 1000.0;              // Balance pro AutoLot
input double  AutoLotSize = 0.15;                   // Lot-Größe pro Balance

//+------------------------------------------------------------------+
//| Gruppe: Stop-Loss & Trailing                                    |
//+------------------------------------------------------------------+
// Stop-Loss Modus Enum
enum ENUM_SL_MODE
{
    SL_POINTS,     // Stop-Loss in Punkten
    SL_PERCENT     // Stop-Loss in Prozent
};

input group "════════ STOP-LOSS & TRAILING ════════"
input ENUM_SL_MODE StopLossMode = SL_POINTS;        // Stop-Loss Modus
input int     StopLossPoints = 500;                 // Stop-Loss in Punkten (wenn Punkte-Modus)
input double  StopLossPercent = 0.5;                // Stop-Loss in % (wenn Prozent-Modus)
input bool    EnableTrailingStop = true;            // Trailing Stop aktivieren
input int     TrailingStopPoints = 1000;            // Trailing Stop in Punkten
input int     TrailingStartHour = 9;                // Trailing Start (Stunde)
input int     TrailingStartMinute = 0;              // Trailing Start (Minute)

//+------------------------------------------------------------------+
//| Gruppe: StochRSI Filter                                         |
//+------------------------------------------------------------------+
// StochRSI Filter - INTERN (nicht sichtbar für User)
// Pre-Filter Variablen (versteckt, werden durch UsePreFilter gesteuert)
bool    enableStochRsiFilter = true;                // StochRSI Filter aktivieren (INTERN)
ENUM_TIMEFRAMES stochRsiTimeframe = PERIOD_H4;      // StochRSI Timeframe (INTERN - H4)
int     rsiPeriod = 14;                             // RSI Periode (INTERN)
int     stochPeriod = 14;                           // Stochastic Periode (INTERN)
int     kPeriod = 3;                                // K-Linie Periode (INTERN)
int     dPeriod = 3;                                // D-Linie Periode (INTERN)

//+------------------------------------------------------------------+
//| Gruppe: Nacht-Schutz                                           |
//+------------------------------------------------------------------+
input group "════════ NACHT-SCHUTZ ════════"
input bool    enableNightProtection = false;        // Nacht-Schutz aktivieren
input int     nightProtectionStartHour = 18;        // Start (Stunde)
input int     nightProtectionEndHour = 9;           // Ende (Stunde)

//+------------------------------------------------------------------+
//| Gruppe: ATR Filter                                              |
//+------------------------------------------------------------------+
// ATR Filter - INTERN (nicht sichtbar für User)
// input group "════════ ATR FILTER ════════"
bool    enableATRFilter = false;                    // ATR Filter aktivieren (INTERN - AUS)
int     atrPeriod = 14;                             // ATR Periode (INTERN)
double  minATR = 100.0;                             // Minimum ATR Wert (INTERN)

//+------------------------------------------------------------------+
//| Gruppe: Volatilitäts-Filter (Alternative zu ATR)               |
//+------------------------------------------------------------------+
input group "════════ VOLATILITÄTS-FILTER ════════"
input bool    enableBollingerFilter = false;        // Bollinger Bands Width Filter
input int     bollingerPeriod = 20;                 // Bollinger Bands Periode
input double  bollingerDeviation = 2.0;             // Standard-Abweichung
input double  minBollingerWidth = 0.01;             // Min. BB Width (% vom Preis)
input bool    enableStdDevFilter = false;           // Standard Deviation Filter
input int     stdDevPeriod = 14;                    // Standard Deviation Periode
input double  minStdDev = 10.0;                     // Min. Standard Deviation

//+------------------------------------------------------------------+
//| Gruppe: Gap Filter                                              |
//+------------------------------------------------------------------+
input group "════════ GAP FILTER ════════"
input bool    enableGapFilter = false;              // Gap-Filter aktivieren
input double  maxDailyGapPercent = 2.0;            // Max. Tagessteigerung in %

//+------------------------------------------------------------------+
//| Gruppe: RSI Filter                                             |
//+------------------------------------------------------------------+
input group "════════ RSI FILTER ════════"
input bool    enableRSIFilter = false;              // RSI Filter aktivieren
input int     rsiFilterPeriod = 14;                 // RSI Periode
input double  rsiOversold = 30.0;                   // Überverkauft Level
input double  rsiOverbought = 70.0;                 // Überkauft Level

//+------------------------------------------------------------------+
//| Gruppe: ADX Filter                                             |
//+------------------------------------------------------------------+
input group "════════ ADX FILTER ════════"
input bool    enableADXFilter = false;              // ADX Filter aktivieren
input int     adxPeriod = 14;                       // ADX Periode
input double  minADXValue = 25.0;                   // Minimum ADX Wert

//+------------------------------------------------------------------+
//| Gruppe: MACD Filter                                            |
//+------------------------------------------------------------------+
input group "════════ MACD FILTER ════════"
input bool    enableMACDFilter = false;             // MACD Filter aktivieren
input int     macdFastEMA = 12;                     // Fast EMA
input int     macdSlowEMA = 26;                     // Slow EMA
input int     macdSignalSMA = 9;                    // Signal SMA

// Zeitbasierte Lizenz DEAKTIVIERT

// Globale Variablen
ulong position_ticket = 0;
datetime lastTradeDate = 0;
bool isLicensed = false;
string licenseMessage = "";
string serverLicenseStatus = "Nicht geprüft";
string roboforexStatus = "Nicht geprüft";
datetime serverLicenseExpiry = 0;
int displayCounter = 0;
datetime lastServerCheck = 0;
bool roboforexVerified = false; // Einmal in OnInit gesetzt
int serverCheckPeriod = 600; // Standard: 10 Minuten, wird vom Server überschrieben
datetime affiliateSecondCheckTime = 0; // Für verzögerte zweite Prüfung
bool affiliateSecondCheckDone = false; // Flag ob zweite Prüfung erfolgt ist

// Demo-Account Tracking Variablen
string currentAccountName = "";
bool isKnownDemoAccount = false;

// Demo-Zeitraum Prüfung
string demoStatus = "";               // Status: "WAITING", "CHECKING", "VALID", "EXPIRED", "UNLIMITED", "SERVER_LICENSE"
datetime demoExpires = 0;             // Ablaufdatum der Demo
datetime demoCheckScheduledTime = 0;  // Nächste geplante Prüfung
int demoRemainingDays = 0;            // Verbleibende Tage

// RoboForex API Credentials (fest im Code)
const string ROBOFOREX_PARTNER_ACCOUNT = "30218520";
const string ROBOFOREX_API_KEY = "ec4d40c4343ee741";
const string AFFILIATE_CODE = "qnyj";  // Hardcodierter Affiliate Code

//+------------------------------------------------------------------+
//| Demo-Zeitraum Status prüfen (Server-basiert)                   |
//+------------------------------------------------------------------+
bool CheckDemoStatus()
{
    // 1. RoboForex-Affiliate = immer OK
    if(roboforexVerified)
    {
        demoStatus = "UNLIMITED";
        demoRemainingDays = 0;
        return true;
    }
    
    // 2. Server-Lizenz = eigene Laufzeit
    if(StringFind(serverLicenseStatus, "✓") >= 0)
    {
        // Server-Lizenz hat eigenes Ablaufdatum
        demoStatus = "SERVER_LICENSE";
        demoRemainingDays = 0;
        return true;
    }
    
    // Status auf CHECKING setzen während der Prüfung
    demoStatus = "CHECKING";
    
    // 3. Alle anderen = Demo-Zeitraum prüfen
    string accountNumber = IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
    
    MqlNet net;
    if(!net._Open(DOMEN, 443, "", "", INTERNET_SERVICE_HTTP))
    {
        Print("Warnung: Demo-Status konnte nicht geprüft werden");
        return true;  // Bei Fehler erlauben
    }
    
    string path = "/files/check_demo_status.php?" +
                  "account=" + accountNumber +
                  "&program=" + PROGRAM_NAME;
    
    tagRequest req;
    req.Init("GET", path, "", "", false, "", false);
    
    string response = "";
    if(net.Request(req))
    {
        response = req.stOut;
    }
    net._Close();
    
    // Response auswerten
    if(StringFind(response, "wait") >= 0)
    {
        // Noch warten - nochmal in X Sekunden prüfen
        string parts[];
        int num = StringSplit(response, '|', parts);
        if(num >= 2)
        {
            int waitSeconds = (int)StringToInteger(parts[1]);
            demoCheckScheduledTime = TimeCurrent() + waitSeconds;
            demoStatus = "WAITING";
            demoRemainingDays = 0;
            Print("Warte ", waitSeconds, " Sekunden auf Demo-Status...");
        }
        return true;  // Erstmal weiterlaufen
    }
    else if(StringFind(response, "unlimited") >= 0)
    {
        demoStatus = "UNLIMITED";
        demoRemainingDays = 0;
        Print("Unbegrenzte Nutzung aktiviert");
        return true;
    }
    else if(StringFind(response, "valid") >= 0)
    {
        // Demo gültig
        string parts[];
        int num = StringSplit(response, '|', parts);
        if(num >= 3)
        {
            demoExpires = StringToTime(parts[1]);
            demoRemainingDays = (int)StringToInteger(parts[2]);
            demoStatus = "VALID";
            Print("Demo gültig bis: ", parts[1], " (", demoRemainingDays, " Tage)");
            
            // Warnung bei wenigen Tagen
            if(demoRemainingDays <= 3 && demoRemainingDays > 0)
            {
                Alert("Hinweis: Demo läuft in ", demoRemainingDays, " Tagen ab!\n\n" +
                      "Sichern Sie sich rechtzeitig eine Lizenz!");
            }
        }
        return true;
    }
    else if(StringFind(response, "expired") >= 0)
    {
        // Demo abgelaufen
        string parts[];
        int num = StringSplit(response, '|', parts);
        if(num >= 2)
        {
            string expiryDate = parts[1];
            demoStatus = "EXPIRED";
            demoRemainingDays = 0;
            Print("Testzeitraum abgelaufen seit: ", expiryDate);
            
            // Alert nur einmal zeigen
            static bool expiredAlertShown = false;
            if(!expiredAlertShown)
            {
                expiredAlertShown = true;
                Alert("TESTZEITRAUM ABGELAUFEN!\n\n" +
                      "Trading wurde deaktiviert.\n\n" +
                      "Optionen zur Fortsetzung:\n" +
                      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" +
                      "1. KOSTENLOS mit RoboForex:\n" +
                      "   → Eröffne ein Konto unter forexsignale.trade/broker\n" +
                      "   → Verwende Code: qnyj\n" +
                      "   → Unbegrenzte Nutzung als Partner!\n\n" +
                      "2. Server-Lizenz erwerben\n" +
                      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" +
                      "Hinweis: Als RoboForex Partner erhältst du\n" +
                      "dauerhaft kostenlosen Zugang zu allen EAs!");
            }
        }
        return false;
    }
    else if(StringFind(response, "error") >= 0)
    {
        Print("Fehler bei Demo-Prüfung: ", response);
        demoStatus = "CHECKING";
        return true;  // Bei Fehler erlauben
    }
    
    // Wenn keine klare Antwort, Status auf CHECKING setzen
    demoStatus = "CHECKING";
    return true;  // Default: erlauben
}

//+------------------------------------------------------------------+
//| Demo-Account Name Tracking - LEGACY (wird nicht mehr verwendet) |
//+------------------------------------------------------------------+
void CheckDemoAccountTracking()
{
    currentAccountName = AccountInfoString(ACCOUNT_NAME);
    
    // Diese Funktion wird beibehalten für Kompatibilität
    // aber nicht mehr aktiv genutzt
    string globalVarName = "DEMO_ACCOUNT_" + currentAccountName;
    
    if(GlobalVariableCheck(globalVarName))
    {
        isKnownDemoAccount = true;
        datetime firstSeen = (datetime)GlobalVariableGet(globalVarName);
    }
    else
    {
        isKnownDemoAccount = false;
        GlobalVariableSet(globalVarName, (double)TimeCurrent());
    }
}

//+------------------------------------------------------------------+
//| Check-Period vom Server auslesen                                |
//+------------------------------------------------------------------+
void UpdateCheckPeriodFromServer()
{
    // Prüfe ob GlobalVariable mit Check-Period existiert
    if(GlobalVariableCheck("LICENSE_CHECK_PERIOD"))
    {
        double checkHours = GlobalVariableGet("LICENSE_CHECK_PERIOD");
        if(checkHours > 0)
        {
            // Konvertiere Stunden in Sekunden
            int newPeriod = (int)(checkHours * 3600);
            if(newPeriod != serverCheckPeriod)
            {
                serverCheckPeriod = newPeriod;
                // Check-Period aktualisiert (stillschweigend für Performance)
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    // Im Backtest keine Lizenzprüfung
    if(MQLInfoInteger(MQL_TESTER))
    {
        isLicensed = true;
        licenseMessage = "BACKTEST MODUS - Keine Lizenzprüfung";
        Print("Backtest Modus erkannt - Lizenzprüfung deaktiviert");
    }
    else
    {
        // Live/Demo Modus - Lizenzierung erforderlich
        // WebRequest nicht nötig - wir nutzen WinInet über MQL_License.mqh
        isLicensed = false;
        licenseMessage = "";
        
        // 0. Demo-Account Tracking - nur im Live/Demo-Modus
        CheckDemoAccountTracking();
        
        // 1. Prüfe ZUERST Affiliate-Verifikation - NUR EINMAL in OnInit
        roboforexVerified = false;
        
        if(UseRoboForexCheck)
        {
            string accountNumber = IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
            // Einmalige Affiliate-Verifikation
            
            if(CheckRoboForexLicense())
            {
                roboforexVerified = true;
                roboforexStatus = "✓ Affiliate verifiziert";
                GlobalVariableSet("AFFILIATE_STATUS", 1.0); // Für Server-Kommunikation
                // Affiliate-Verifikation erfolgreich
                // Speichere Affiliate-Status in Datenbank - ERSTE Übertragung
                UpdateRoboForexStatusToServer(accountNumber, "yes");
            }
            else
            {
                roboforexVerified = false;
                roboforexStatus = "✗ Kein Affiliate";
                GlobalVariableSet("AFFILIATE_STATUS", 0.0);
                // Affiliate-Verifikation fehlgeschlagen
                
                // Erste Status-Speicherung
                UpdateRoboForexStatusToServer(accountNumber, "no");
                
                // Zeige sanfteren Hinweis nur im Print (kein Alert wenn Server-Lizenz aktiv)
                Print("═══════════════════════════════════════════════════════════════════");
                Print("INFO: Konto ", accountNumber, " ist kein RoboForex Affiliate");
                Print("Für unlimitierte Nutzung ohne Server-Lizenz:");
                Print("Eröffne ein Konto unter forexsignale.trade/broker mit Code: qnyj");
                Print("═══════════════════════════════════════════════════════════════════");
            }
            
            // Plane zweite Prüfung in 3 Sekunden FÜR ALLE KONTEN
            affiliateSecondCheckTime = TimeCurrent() + 3;
            affiliateSecondCheckDone = false;
        }
        else
        {
            roboforexStatus = "Deaktiviert";
            Print("Affiliate-Verifikation deaktiviert");
        }
        
        // 2. Initialisiere Server-Lizenz MIT Affiliate-Status
        bool serverLicense = false;
        int MG = MagicNumber;
        
        int initResult = DataOnInit(DOMEN, serverPort, PROGRAM_NAME, __FILE__, release,
                                    URLBUY, URLUPDATE, REF, PERC, SHTXT, MG, LICENSE_CODE);
        if(initResult == 0)
        {
            serverLicense = true;
            serverLicenseStatus = "Initialisiert";
            // System erfolgreich initialisiert
            
            // Initiale Server-Prüfung und Check-Period holen
            if(Activation())
            {
                UpdateCheckPeriodFromServer();
                serverLicenseStatus = "✓ Aktiviert";
                // Server-Lizenz aktiviert (stillschweigend für Performance)
            }
        }
        else
        {
            serverLicenseStatus = "Fehler: " + IntegerToString(initResult);
            Print("Initialisierung fehlgeschlagen: ", initResult);
        }
        
        // Mindestens eine Lizenz muss gültig sein
        if(!serverLicense && !roboforexVerified)
        {
            Print("═══════════════════════════════════════════════════════════════════");
            Print("FEHLER: Keine gültige Lizenz gefunden!");
            Print("Benötigt: Server-Lizenz ODER RoboForex Affiliate-Konto");
            Print("═══════════════════════════════════════════════════════════════════");
            
            Alert("Keine gültige Lizenz gefunden!\n\n" +
                  "Optionen:\n" +
                  "1. Server-Lizenz erwerben\n" +
                  "2. RoboForex Affiliate-Konto unter forexsignale.trade/broker (Code: qnyj)");
            
            return(INIT_FAILED);
        }
        
        isLicensed = true;
    }
    
    // Trading-Setup
    trade.SetExpertMagicNumber(MagicNumber);
    trade.SetDeviationInPoints(10);
    trade.SetTypeFilling(ORDER_FILLING_IOC);
    
    // Status wurde bereits oben in der Verifikation gesetzt - kein doppelter Aufruf nötig
    
    // Demo-Check initialisieren (nach 20 Sekunden für nicht-RoboForex)
    if(!roboforexVerified && StringFind(serverLicenseStatus, "✓") < 0)
    {
        // Wenn weder RoboForex noch Server-Lizenz, starte Demo-Check nach 20 Sekunden
        demoCheckScheduledTime = TimeCurrent() + 20;
        Print("Demo-Check geplant in 20 Sekunden...");
    }
    else if(roboforexVerified)
    {
        demoStatus = "UNLIMITED";
        demoRemainingDays = 0;
        Print("RoboForex Affiliate erkannt - Unbegrenzte Nutzung");
    }
    else if(StringFind(serverLicenseStatus, "✓") >= 0)
    {
        demoStatus = "SERVER_LICENSE";
        demoRemainingDays = 0;
        Print("Server-Lizenz aktiv - Kein Demo-Zeitraum");
    }
    
    // Timer für Performance-Update alle 5 Sekunden
    EventSetTimer(5);
    
    Print("DAX Overnight EA erfolgreich initialisiert");
    if(ShowLicenseInfo) UpdateLicenseDisplay();
    
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    EventKillTimer();
    
    if(!MQLInfoInteger(MQL_TESTER))
    {
        DataOnDeinit();
    }
    
    ObjectsDeleteAll(0, "License");
    ObjectsDeleteAll(0, "Performance");
}

//+------------------------------------------------------------------+
//| Chart Event Handler                                             |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
{
    if(!MQLInfoInteger(MQL_TESTER))
    {
        ChartEventA(id, sparam);
    }
}

//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
{
    // Performance-Display aktualisieren (nur wenn aktiviert)
    if(ShowPerformance) 
    {
        UpdatePerformanceDisplay();
    }
    
    // Demo-Check durchführen wenn geplant
    if(demoCheckScheduledTime > 0 && TimeCurrent() >= demoCheckScheduledTime)
    {
        CheckDemoStatus();
        demoCheckScheduledTime = 0; // Nur einmal checken
        
        // Display aktualisieren
        if(ShowLicenseInfo) UpdateLicenseDisplay();
    }
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    // Alert nur bei abgelaufenem Testzeitraum (stündlich, aber Trading wird nicht blockiert hier)
    if(demoStatus == "EXPIRED" && !MQLInfoInteger(MQL_TESTER))
    {
        static datetime lastDemoWarning = 0;
        
        // Stündliche Alert-Box
        if(TimeCurrent() - lastDemoWarning > 3600)
        {
            lastDemoWarning = TimeCurrent();
            Alert("⚠️ TESTZEITRAUM ABGELAUFEN\n\n" +
                  "Trading ist deaktiviert!\n\n" +
                  "KOSTENLOSE Option:\n" +
                  "→ RoboForex Konto: forexsignale.trade/broker\n" +
                  "→ Mit Code 'qnyj' als Partner registrieren\n" +
                  "→ Unbegrenzte EA-Nutzung!\n\n" +
                  "Alternative: Server-Lizenz erwerben");
        }
    }
    
    // BACKTEST-PERFORMANCE-OPTIMIERUNG: Alle Lizenzprüfungen deaktiviert im Backtest
    if(!MQLInfoInteger(MQL_TESTER))
    {
        // Verzögerte zweite Affiliate-Status Prüfung (nach 3 Sekunden) - NUR Live/Demo
        if(!affiliateSecondCheckDone && affiliateSecondCheckTime > 0 && TimeCurrent() >= affiliateSecondCheckTime)
        {
            affiliateSecondCheckDone = true;
            string accountNumber = IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
            string roboStatus = roboforexVerified ? "yes" : "no";
            
            // Zweite Übertragung (stillschweigend)
            UpdateRoboForexStatusToServer(accountNumber, roboStatus);
            
            // Nur Alert zeigen wenn KEIN Affiliate UND keine Server-Lizenz
            if(!roboforexVerified && StringFind(serverLicenseStatus, "✓") < 0)
            {
                Alert("RoboForex Affiliate Registrierung empfohlen!\n\n" +
                      "Für dauerhaft unlimitierte Nutzung:\n" +
                      "Eröffne ein Konto unter forexsignale.trade/broker\n" +
                      "mit Code: qnyj");
            }
        }
        
        // Server-Lizenz gemäß Check-Period prüfen - NUR Live/Demo
        datetime currentTime = TimeCurrent();
        if(currentTime - lastServerCheck >= serverCheckPeriod)
        {
            lastServerCheck = currentTime;
            
            // Server-Lizenz prüfen (RoboForex-Status wurde bereits in OnInit gesetzt)
            static bool serverActivated = false;
            static int activationAttempts = 0;
            
            if(!serverActivated && activationAttempts < 5)
            {
                activationAttempts++;
                
                if(Activation())
                {
                    serverActivated = true;
                    
                    // Check-Period vom Server aktualisieren
                    UpdateCheckPeriodFromServer();
                    
                    // Server hat Lizenz bestätigt - Status setzen
                    serverLicenseStatus = "✓ Server-Lizenz aktiv";
                    
                    // Lizenz-Ablaufdatum aus _ansTime vom Server übernehmen
                    if(StringLen(_ansTime) == 10)  // Format: "YYYY.MM.DD"
                    {
                        serverLicenseExpiry = StringToTime(_ansTime);
                    }
                    else
                    {
                        // Fallback: 30 Tage default wenn Server kein Datum liefert
                        serverLicenseExpiry = TimeCurrent() + (30 * 86400);
                    }
                }
                else
                {
                    serverLicenseStatus = "Prüfung läuft...";
                    
                    if(activationAttempts >= 5)
                    {
                        serverLicenseStatus = "✗ Nicht aktiviert";
                        Print("Server-Lizenz-Aktivierung fehlgeschlagen");
                    }
                }
            }
            else if(serverActivated)
            {
                // Periodische Prüfung der bestehenden Lizenz
                if(Activation())
                {
                    // Check-Period vom Server aktualisieren
                    UpdateCheckPeriodFromServer();
                    
                    // Server-Lizenz bleibt aktiv
                    serverLicenseStatus = "✓ Server-Lizenz aktiv";
                    
                    // Lizenz-Ablaufdatum aktualisieren
                    if(StringLen(_ansTime) == 10)
                    {
                        serverLicenseExpiry = StringToTime(_ansTime);
                    }
                    // Weniger verbose Lizenz-Logs für Performance
                }
                else
                {
                    serverLicenseStatus = "✗ Abgelaufen";
                    Print("Server-Lizenz abgelaufen!");
                }
            }
            
            // Lizenzstatus prüfen
            if(!CheckAllLicenses())
            {
                Alert("Lizenz ungültig! EA wird gestoppt.");
                ExpertRemove();
                return;
            }
            
            // Display aktualisieren
            if(ShowLicenseInfo) UpdateLicenseDisplay();
        }
    }
    // BACKTEST: Keine Lizenzprüfungen = 50-70% Performance-Boost
    
    datetime current_time = TimeCurrent();
    if(!IsTradeDay(current_time)) return;
    
    MqlDateTime now;
    TimeToStruct(current_time, now);
    int current_minutes = now.hour * 60 + now.min;
    int buy_minutes = StartHourBuy * 60 + StartMinuteBuy;
    
    // Prüfe ob wir Positionen mit unserer MagicNumber haben
    if(HasOpenPosition())
    {
        MqlDateTime entry;
        TimeToStruct(lastTradeDate, entry);
        bool ist_naechster_tag = (now.day != entry.day || now.mon != entry.mon || now.year != entry.year);
        
        // Core Strategy: Immer um 09:05 schließen, kein Trailing
        if(UseCoreStrategy)
        {
            if(ist_naechster_tag && current_minutes >= 9 * 60 + 5)  // 09:05 Uhr
            {
                CloseAllPositions();
            }
        }
        else
        {
            // Normale Strategie mit konfigurierbaren Zeiten
            if(EnableTrailingStop && ist_naechster_tag && 
               current_minutes >= TrailingStartHour * 60 + TrailingStartMinute)
            {
                TrailingStop();
            }
            
            if(!EnableTrailingStop && ist_naechster_tag && 
               current_minutes >= CloseHour * 60 + CloseMinute)
            {
                CloseAllPositions();
            }
        }
    }
    
    // Neue Position öffnen - mit mehreren Positionen Support
    if(current_minutes >= buy_minutes)
    {
        int openPositions = CountOpenPositions();
        
        // Prüfe ob wir neue Position öffnen dürfen
        if(MaxSimultaneousPositions == 0 || openPositions < MaxSimultaneousPositions)
        {
            MqlDateTime last;
            TimeToStruct(lastTradeDate, last);
            bool ist_neuer_tag = (now.day != last.day || now.mon != last.mon || now.year != last.year);
            
            if(ist_neuer_tag)
            {
                // Reset rejection reason für neuen Tag
                todayRejectionReason = "";
                
                // Versuche Position zu öffnen
                if(OpenPosition())  // WICHTIG: Nur bei Erfolg lastTradeDate setzen!
                {
                    lastTradeDate = current_time;
                }
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Prüfen ob Journal-Logging aktiv sein soll                      |
//+------------------------------------------------------------------+
bool ShouldLogToJournal()
{
    if(MQLInfoInteger(MQL_TESTER))
    {
        return EnableBacktestLogging;  // Im Backtest nur wenn explizit aktiviert
    }
    return EnableTradeLogging;  // Live/Demo gemäß Einstellung
}

//+------------------------------------------------------------------+
//| Lizenz vor Trade prüfen                                        |
//+------------------------------------------------------------------+
bool CheckLicenseBeforeTrade()
{
    // Im Backtest keine Lizenzprüfung
    if(MQLInfoInteger(MQL_TESTER))
    {
        return true;
    }
    
    // 1. Prüfe ob Testzeitraum abgelaufen
    if(demoStatus == "EXPIRED")
    {
        ProcessTradeRejection("TESTZEITRAUM ABGELAUFEN - Nutze RoboForex oder Server-Lizenz");
        return false;
    }
    
    // 2. RoboForex Partner - kein Log nötig, ist bereits bekannt
    if(roboforexVerified)
    {
        return true;
    }
    
    // 3. Server-Lizenz aktiv - kein Log nötig, ist bereits bekannt
    if(StringFind(serverLicenseStatus, "✓") >= 0)
    {
        return true;
    }
    
    // 4. Testzeitraum aktiv - kein Log nötig
    if(demoStatus == "VALID")
    {
        return true;
    }
    
    // 5. Lizenz noch in Prüfung - erlaube Trade
    if(demoStatus == "WAITING" || demoStatus == "CHECKING")
    {
        return true;
    }
    
    // Keine Lizenz vorhanden
    ProcessTradeRejection("KEINE LIZENZ - Testzeitraum verfügbar oder nutze RoboForex");
    return false;
}

//+------------------------------------------------------------------+
//| Trade-Ablehnung verarbeiten                                    |
//+------------------------------------------------------------------+
void ProcessTradeRejection(string reason)
{
    todayRejectionReason = reason;
    lastRejectionReason = reason;
    lastTradeStatus = "REJECTED";
    lastTradeAttemptTime = TimeCurrent();
    
    // Journal-Logging zur konfigurierten Handelszeit
    MqlDateTime now;
    TimeToStruct(TimeCurrent(), now);
    int current_minutes = now.hour * 60 + now.min;
    int buy_minutes = StartHourBuy * 60 + StartMinuteBuy;
    
    // Nur loggen wenn wir innerhalb von 1 Minute zur konfigurierten Handelszeit sind
    bool isNearTradeTime = MathAbs(current_minutes - buy_minutes) <= 1;
    
    if(ShouldLogToJournal() && isNearTradeTime)
    {
        string timeStr = TimeToString(lastTradeAttemptTime, TIME_DATE|TIME_SECONDS);
        
        // Strukturierte Ausgabe je nach Grund
        if(StringFind(reason, "LIZENZ") >= 0 || StringFind(reason, "TESTZEITRAUM") >= 0)
        {
            // Lizenz-bezogene Ablehnung
            Print("[LICENSE] ✗ ", reason);
            Print("[INFO] Für kostenlose Nutzung: RoboForex Konto unter forexsignale.trade/broker mit Code 'qnyj'");
        }
        else
        {
            // Filter-bezogene Ablehnung
            Print("[FILTER BLOCKED] ", timeStr, " - ", reason, " verhindert Trade auf ", _Symbol);
        }
    }
    
    UpdateTradeStatusDisplay();
}

//+------------------------------------------------------------------+
//| Gap Filter prüfen                                              |
//+------------------------------------------------------------------+
bool CheckGapFilter()
{
    if(!enableGapFilter) return true;
    
    // Hole heutige und gestrige Kurse
    double open_today = iOpen(_Symbol, PERIOD_D1, 0);
    double close_yesterday = iClose(_Symbol, PERIOD_D1, 1);
    
    if(close_yesterday == 0) return false;
    
    // Berechne Gap in Prozent
    double gap_percent = (open_today - close_yesterday) / close_yesterday * 100;
    
    // Prüfe ob Gap innerhalb der erlaubten Grenzen liegt
    return MathAbs(gap_percent) <= maxDailyGapPercent;
}

//+------------------------------------------------------------------+
//| RSI Filter prüfen                                              |
//+------------------------------------------------------------------+
bool CheckRSI()
{
    if(!enableRSIFilter) return true;
    
    int rsiHandle = iRSI(_Symbol, PERIOD_H1, rsiFilterPeriod, PRICE_CLOSE);
    if(rsiHandle == INVALID_HANDLE) 
    {
        return true;  // Bei Fehler Trade erlauben statt blockieren
    }
    
    double rsiBuffer[];
    ArraySetAsSeries(rsiBuffer, true);
    
    if(CopyBuffer(rsiHandle, 0, 0, 1, rsiBuffer) <= 0)
    {
        IndicatorRelease(rsiHandle);
        return false;
    }
    
    double rsiValue = rsiBuffer[0];
    IndicatorRelease(rsiHandle);
    
    // Für Long-Positionen: RSI sollte nicht überkauft sein
    return rsiValue < rsiOverbought && rsiValue > rsiOversold;
}

//+------------------------------------------------------------------+
//| ADX Filter prüfen                                              |
//+------------------------------------------------------------------+
bool CheckADX()
{
    if(!enableADXFilter) return true;
    
    int adxHandle = iADX(_Symbol, PERIOD_H1, adxPeriod);
    if(adxHandle == INVALID_HANDLE) 
    {
        return true;  // Bei Fehler Trade erlauben statt blockieren
    }
    
    double adxBuffer[];
    ArraySetAsSeries(adxBuffer, true);
    
    if(CopyBuffer(adxHandle, 0, 0, 1, adxBuffer) <= 0)
    {
        IndicatorRelease(adxHandle);
        return false;
    }
    
    double adxValue = adxBuffer[0];
    IndicatorRelease(adxHandle);
    
    // ADX sollte mindestens den Minimum-Wert erreichen
    return adxValue >= minADXValue;
}

//+------------------------------------------------------------------+
//| MACD Filter prüfen                                             |
//+------------------------------------------------------------------+
bool CheckMACD()
{
    if(!enableMACDFilter) return true;
    
    int macdHandle = iMACD(_Symbol, PERIOD_H1, macdFastEMA, macdSlowEMA, macdSignalSMA, PRICE_CLOSE);
    if(macdHandle == INVALID_HANDLE) 
    {
        return true;  // Bei Fehler Trade erlauben statt blockieren
    }
    
    double macdMain[], macdSignal[];
    ArraySetAsSeries(macdMain, true);
    ArraySetAsSeries(macdSignal, true);
    
    if(CopyBuffer(macdHandle, 0, 0, 2, macdMain) <= 0 || 
       CopyBuffer(macdHandle, 1, 0, 2, macdSignal) <= 0)
    {
        IndicatorRelease(macdHandle);
        return false;
    }
    
    // Bullish Signal: MACD kreuzt Signal-Linie von unten
    bool bullishCross = (macdMain[0] > macdSignal[0]) && (macdMain[1] <= macdSignal[1]);
    
    IndicatorRelease(macdHandle);
    
    return bullishCross || (macdMain[0] > macdSignal[0]);
}

//+------------------------------------------------------------------+
//| Nacht-Schutz prüfen                                            |
//+------------------------------------------------------------------+
bool IsNightProtectionActive()
{
    if(!enableNightProtection) return false;
    
    MqlDateTime now;
    TimeToStruct(TimeCurrent(), now);
    
    int currentHour = now.hour;
    
    // Prüfe ob wir in der Nacht-Schutz Zeit sind
    if(nightProtectionStartHour <= nightProtectionEndHour)
    {
        // Normaler Fall: z.B. 22:00 bis 06:00 (nächster Tag)
        return (currentHour >= nightProtectionStartHour && currentHour < nightProtectionEndHour);
    }
    else
    {
        // Über Mitternacht: z.B. 18:00 bis 09:00 (nächster Tag)
        return (currentHour >= nightProtectionStartHour || currentHour < nightProtectionEndHour);
    }
}

//+------------------------------------------------------------------+
//| Position öffnen                                                 |
//+------------------------------------------------------------------+
bool OpenPosition()
{
    // Reset rejection reason am Anfang
    todayRejectionReason = "";
    
    // ZUERST: Lizenz-Status prüfen
    if(!CheckLicenseBeforeTrade())
    {
        // Lizenz-Problem bereits in CheckLicenseBeforeTrade behandelt
        return false;
    }
    
    // Pre-Filter (versteckter StochRSI Filter) - nur wenn UsePreFilter = true
    if(UsePreFilter && !IsStochRsiOk()) 
    {
        ProcessTradeRejection("Pre-Filter");
        return false;
    }
    
    // Volatilitäts-Filter (nur wenn aktiviert)
    if(enableATRFilter && !CheckATR()) 
    {
        ProcessTradeRejection("ATR Filter");
        return false;
    }
    
    if(enableBollingerFilter && !CheckBollingerBandsWidth()) 
    {
        ProcessTradeRejection("Bollinger Filter");
        return false;
    }
    
    if(enableStdDevFilter && !CheckStandardDeviation()) 
    {
        ProcessTradeRejection("StdDev Filter");
        return false;
    }
    
    // Weitere Filter
    if(!CheckGapFilter()) 
    {
        ProcessTradeRejection("Gap Filter");
        return false;
    }
    
    if(!CheckRSI()) 
    {
        ProcessTradeRejection("RSI Filter");
        return false;
    }
    
    if(!CheckADX()) 
    {
        ProcessTradeRejection("ADX Filter");
        return false;
    }
    
    if(!CheckMACD()) 
    {
        ProcessTradeRejection("MACD Filter");
        return false;
    }
    
    double volume = UseAutoLot ? CalculateLotSize() : StartLotSize;
    double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
    double stepLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
    int digits = (int)MathRound(MathLog10(1.0 / stepLot));
    
    if(volume < minLot) volume = minLot;
    volume = MathCeil(volume / stepLot) * stepLot;
    volume = NormalizeDouble(volume, digits);
    
    if(volume <= 0)
    {
        Print("Ungültige Lotgröße: ", DoubleToString(volume, digits));
        return false;
    }
    
    double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
    double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
    
    // Stop-Loss nur setzen wenn nicht Core Strategy und nicht im Nacht-Schutz
    double sl = 0.0;
    if(!UseCoreStrategy && !IsNightProtectionActive())
    {
        // Stop-Loss basierend auf Modus berechnen
        if(StopLossMode == SL_POINTS && StopLossPoints > 0)
        {
            // Punkte-Modus: Verwende StopLossPoints
            sl = ask - StopLossPoints * point;
        }
        else if(StopLossMode == SL_PERCENT && StopLossPercent > 0)
        {
            // Prozent-Modus: Berechne SL als Prozentsatz vom Entry-Preis
            sl = ask * (1 - StopLossPercent / 100);
        }
    }
    
    if(trade.Buy(volume, _Symbol, ask, sl, 0, "DAX Overnight"))
    {
        // Position erfolgreich eröffnet
        todayRejectionReason = "";
        lastRejectionReason = "";
        lastTradeStatus = "SUCCESS";
        lastTradeAttemptTime = TimeCurrent();
        lastTradeLotSize = volume;
        lastTradeSymbol = _Symbol;
        
        // Strukturiertes Journal-Logging für erfolgreichen Trade
        if(ShouldLogToJournal())
        {
            string timeStr = TimeToString(lastTradeAttemptTime, TIME_DATE|TIME_SECONDS);
            
            // Einmal Lizenz-Status anzeigen
            if(roboforexVerified)
                Print("[LICENSE] ✓ RoboForex Affiliate (Unlimitiert)");
            else if(StringFind(serverLicenseStatus, "✓") >= 0)
            {
                int daysLeft = serverLicenseExpiry > 0 ? (int)((serverLicenseExpiry - TimeCurrent()) / 86400) : 999;
                Print("[LICENSE] ✓ Server-Lizenz aktiv (", daysLeft, " Tage)");
            }
            else if(demoStatus == "VALID")
                Print("[LICENSE] ✓ Testzeitraum aktiv (", demoRemainingDays, " Tage)");
            
            Print("[FILTERS] ✓ Alle Filter bestanden");
            Print("[TRADE OPENED] ", timeStr, " - ", _Symbol, " - ", DoubleToString(volume, 2), " Lots - Ask: ", DoubleToString(ask, _Digits));
        }
        
        UpdateTradeStatusDisplay();
        return true;  // Trade erfolgreich
    }
    else
    {
        Print("Trade-Fehler: ", trade.ResultRetcode());
        return false;  // Trade fehlgeschlagen
    }
}

//+------------------------------------------------------------------+
//| Alle Positionen mit unserer MagicNumber schließen              |
//+------------------------------------------------------------------+
void CloseAllPositions()
{
    // Prüfe Nacht-Schutz - während der Nacht-Schutz Zeit nicht schließen
    if(IsNightProtectionActive())
    {
        // Position bleibt während Nacht-Schutz offen (RoboForex-Simulation)
        return;
    }
    
    // Schließe alle Positionen mit unserer MagicNumber
    for(int i = PositionsTotal() - 1; i >= 0; i--)
    {
        if(PositionSelectByTicket(PositionGetTicket(i)))
        {
            if(PositionGetString(POSITION_SYMBOL) == _Symbol &&
               PositionGetInteger(POSITION_MAGIC) == MagicNumber)
            {
                ulong ticket = PositionGetInteger(POSITION_TICKET);
                if(!trade.PositionClose(ticket))
                {
                    // Fehler nur loggen wenn NICHT "Market closed"
                    int error = GetLastError();
                    // 10018 = Market closed, 132 = Market closed, 4756 = Trade request sending failed
                    if(error != 10018 && error != 132 && error != 4756)
                    {
                        Print("Position Close Fehler: ", error);
                    }
                }
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Position schließen (alte Funktion für Kompatibilität)          |
//+------------------------------------------------------------------+
void ClosePosition()
{
    CloseAllPositions();  // Verwende neue Funktion
}

//+------------------------------------------------------------------+
//| Trailing Stop                                                   |
//+------------------------------------------------------------------+
void TrailingStop()
{
    // Kein Trailing Stop bei Core Strategy
    if(UseCoreStrategy) return;
    
    if(!PositionSelect(_Symbol)) return;
    
    // Prüfe Nacht-Schutz - während der Nacht-Schutz Zeit kein Stop-Loss setzen
    if(IsNightProtectionActive())
    {
        // Während Nacht-Schutz kein Trailing Stop (RoboForex-Simulation)
        return;
    }
    
    double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
    double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
    double sl = PositionGetDouble(POSITION_SL);
    double new_sl = bid - TrailingStopPoints * point;
    
    if(new_sl > sl)
    {
        ulong ticket = PositionGetInteger(POSITION_TICKET);
        if(!trade.PositionModify(ticket, new_sl, 0))
        {
            // Fehler nur loggen wenn NICHT "Market closed"
            int error = GetLastError();
            // 10018 = Market closed, 132 = Market closed, 4756 = Trade request sending failed
            if(error != 10018 && error != 132 && error != 4756)
            {
                Print("Trailing Stop Fehler: ", error);
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Prüft ob Position mit unserer MagicNumber offen ist            |
//+------------------------------------------------------------------+
bool HasOpenPosition()
{
    for(int i = PositionsTotal() - 1; i >= 0; i--)
    {
        if(PositionSelectByTicket(PositionGetTicket(i)))
        {
            if(PositionGetString(POSITION_SYMBOL) == _Symbol &&
               PositionGetInteger(POSITION_MAGIC) == MagicNumber)
            {
                return true;
            }
        }
    }
    return false;
}

//+------------------------------------------------------------------+
//| Zählt offene Positionen mit unserer MagicNumber                |
//+------------------------------------------------------------------+
int CountOpenPositions()
{
    int count = 0;
    for(int i = PositionsTotal() - 1; i >= 0; i--)
    {
        if(PositionSelectByTicket(PositionGetTicket(i)))
        {
            if(PositionGetString(POSITION_SYMBOL) == _Symbol &&
               PositionGetInteger(POSITION_MAGIC) == MagicNumber)
            {
                count++;
            }
        }
    }
    return count;
}

//+------------------------------------------------------------------+
//| Handelstag prüfen                                               |
//+------------------------------------------------------------------+
bool IsTradeDay(datetime current_time)
{
    MqlDateTime t;
    TimeToStruct(current_time, t);
    switch(t.day_of_week)
    {
        case 0: return false;      // Sonntag
        case 1: return TradeMonday;
        case 2: return TradeTuesday;
        case 3: return TradeWednesday;
        case 4: return TradeThursday;
        case 5: return TradeFriday;
        case 6: return false;      // Samstag
    }
    return false;
}

//+------------------------------------------------------------------+
//| StochRSI Filter                                                 |
//+------------------------------------------------------------------+
bool IsStochRsiOk()
{
    // Pre-Filter wird über UsePreFilter gesteuert
    if(!UsePreFilter) return true;
    
    // Interne StochRSI Berechnung
    int rsiHandle = iRSI(_Symbol, stochRsiTimeframe, rsiPeriod, PRICE_CLOSE);
    if(rsiHandle == INVALID_HANDLE) 
    {
        return true;  // Bei Fehler Trade erlauben statt blockieren
    }
    
    double rsiBuffer[];
    ArraySetAsSeries(rsiBuffer, true);
    if(CopyBuffer(rsiHandle, 0, 0, stochPeriod + 10, rsiBuffer) <= 0) return false;
    
    double minRSI = rsiBuffer[0], maxRSI = rsiBuffer[0];
    for(int i = 0; i < stochPeriod; i++)
    {
        if(rsiBuffer[i] < minRSI) minRSI = rsiBuffer[i];
        if(rsiBuffer[i] > maxRSI) maxRSI = rsiBuffer[i];
    }
    
    double stochRsi = (maxRSI - minRSI > 0) ? 
                      (rsiBuffer[0] - minRSI) / (maxRSI - minRSI) * 100 : 50;
    
    return stochRsi > 50;
}

//+------------------------------------------------------------------+
//| ATR Filter                                                      |
//+------------------------------------------------------------------+
bool CheckATR()
{
    // ATR Filter Check - Qualitäts-Filter für bessere Trades
    
    if(!enableATRFilter) 
    {
        return true; // ATR Filter deaktiviert
    }
    
    int atrHandle = iATR(_Symbol, PERIOD_H1, atrPeriod);
    if(atrHandle == INVALID_HANDLE) 
    {
        return true;  // Bei Fehler Trade erlauben statt blockieren
    }
    
    double atrBuffer[];
    ArraySetAsSeries(atrBuffer, true);
    if(CopyBuffer(atrHandle, 0, 0, 1, atrBuffer) <= 0) 
    {
        IndicatorRelease(atrHandle);
        return false;
    }
    
    double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
    double atrRaw = atrBuffer[0];
    double atrValue = atrRaw / point;
    
    
    bool result = atrValue >= minATR;
    
    IndicatorRelease(atrHandle);
    
    return result;
}

//+------------------------------------------------------------------+
//| Bollinger Bands Width Filter                                   |
//+------------------------------------------------------------------+
bool CheckBollingerBandsWidth()
{
    if(!enableBollingerFilter) return true;
    
    // Bollinger Bands mit korrekten Parametern
    int bbHandle = iBands(_Symbol, PERIOD_H1, bollingerPeriod, 0, bollingerDeviation, PRICE_CLOSE);
    if(bbHandle == INVALID_HANDLE)
    {
        Print("Fehler beim Erstellen des Bollinger Bands Indikators");
        return true;  // Bei Fehler Trade erlauben statt blockieren
    }
    
    double upperBuffer[], lowerBuffer[];
    ArraySetAsSeries(upperBuffer, true);
    ArraySetAsSeries(lowerBuffer, true);
    
    if(CopyBuffer(bbHandle, 1, 0, 1, upperBuffer) <= 0 || 
       CopyBuffer(bbHandle, 2, 0, 1, lowerBuffer) <= 0)
    {
        IndicatorRelease(bbHandle);
        return false;
    }
    
    double currentPrice = SymbolInfoDouble(_Symbol, SYMBOL_BID);
    double bbWidth = (upperBuffer[0] - lowerBuffer[0]) / currentPrice;
    
    IndicatorRelease(bbHandle);
    
    // Bollinger Bands Width sollte mindestens den Minimum-Wert erreichen
    return bbWidth >= minBollingerWidth;
}

//+------------------------------------------------------------------+
//| Standard Deviation Filter                                       |
//+------------------------------------------------------------------+
bool CheckStandardDeviation()
{
    if(!enableStdDevFilter) return true;
    
    int stdDevHandle = iStdDev(_Symbol, PERIOD_H1, stdDevPeriod, 0, MODE_SMA, PRICE_CLOSE);
    if(stdDevHandle == INVALID_HANDLE) 
    {
        return true;  // Bei Fehler Trade erlauben statt blockieren
    }
    
    double stdDevBuffer[];
    ArraySetAsSeries(stdDevBuffer, true);
    
    if(CopyBuffer(stdDevHandle, 0, 0, 1, stdDevBuffer) <= 0)
    {
        IndicatorRelease(stdDevHandle);
        return false;
    }
    
    double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
    double stdDevValue = stdDevBuffer[0] / point;
    IndicatorRelease(stdDevHandle);
    
    // Standard Deviation sollte mindestens den Minimum-Wert erreichen
    return stdDevValue >= minStdDev;
}

//+------------------------------------------------------------------+
//| Lot-Größe berechnen                                             |
//+------------------------------------------------------------------+
double CalculateLotSize()
{
    double balance = AccountInfoDouble(ACCOUNT_BALANCE);
    double lot = balance / AutoLotBalance * AutoLotSize;
    return lot;
}


//+------------------------------------------------------------------+
//| RoboForex Lizenz prüfen via WinInet                            |
//+------------------------------------------------------------------+
bool CheckRoboForexLicense()
{
    if(!UseRoboForexCheck) return false;
    
    string accountNumber = IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
    string brokerName = AccountInfoString(ACCOUNT_COMPANY);
    
    // Prüfe ob es ein RoboForex Konto ist
    if(StringFind(brokerName, "RoboForex") < 0 && 
       StringFind(brokerName, "RoboMarkets") < 0)
    {
        // Broker nicht RoboForex/RoboMarkets
        return false;
    }
    
    // Affiliate-Verifikation (stillschweigend für Performance)
    
    // Verwende WinInet statt WebRequest
    return CheckRoboForexViaWinInet(accountNumber);
}

//+------------------------------------------------------------------+
//| RoboForex Check via WinInet - VEREINFACHT                      |
//+------------------------------------------------------------------+
bool CheckRoboForexViaWinInet(string accountNumber)
{
    // Affiliate-Check für Konto
    
    // DIREKTE Abfrage mit referral_account_id - keine Pagination nötig!
    string path = "/api/partners/tree?account_id=" + ROBOFOREX_PARTNER_ACCOUNT + 
                  "&api_key=" + ROBOFOREX_API_KEY + 
                  "&referral_account_id=" + accountNumber;
    
    MqlNet net;
    if(!net._Open("my.roboforex.com", 443, "", "", INTERNET_SERVICE_HTTP))
    {
        // Fehler beim Verbindungsaufbau zu RoboForex API
        return false;
    }
    
    tagRequest req;
    req.Init("GET", path, "", "", false, "", false);
    
    if(!net.Request(req))
    {
        // Fehler beim Senden des API-Requests
        net._Close();
        return false;
    }
    
    string response = req.stOut;
    net._Close();
    
    // Prüfe Response
    if(StringLen(response) == 0)
    {
        // Leere Antwort von API
        return false;
    }
    
    // Debug-Ausgabe (erste 500 Zeichen)
    if(StringLen(response) > 0)
    {
        // Debug: API Response erhalten
    }
    
    // WICHTIG: Prüfe ZUERST ob Konto NICHT gefunden wurde!
    if(StringFind(response, "Not found") >= 0 || 
       StringFind(response, "not found") >= 0)
    {
        // Konto nicht in Affiliate-System gefunden
        return false;
    }
    
    // Erfolgreiche Response enthält das Konto in der Affiliate-Struktur
    // Verschiedene Formate möglich:
    // 1. <multilevel_scheme>30218520 / accountNumber</multilevel_scheme>
    // 2. <account id="accountNumber">
    // 3. <path>30218520/.../accountNumber</path>
    
    if(StringFind(response, "<account id=\"" + accountNumber + "\"") >= 0 ||
       StringFind(response, "<multilevel_scheme>") >= 0 && StringFind(response, accountNumber) >= 0 ||
       StringFind(response, "<path>") >= 0 && StringFind(response, accountNumber) >= 0)
    {
        // Konto ist in Affiliate-Struktur
        
        // Prüfe ob es unter unserem Affiliate-Account ist
        if(StringFind(response, ROBOFOREX_PARTNER_ACCOUNT) >= 0)
        {
            // Konto ist unter Affiliate-Account
        }
        
        return true;
    }
    
    // Fallback
    // Konto ist NICHT in Affiliate-Struktur
    
    return false;
}

//+------------------------------------------------------------------+
//| Alle Lizenzen prüfen                                            |
//+------------------------------------------------------------------+
bool CheckAllLicenses()
{
    // Im Backtest immer true - KEINE Lizenzprüfung
    if(MQLInfoInteger(MQL_TESTER)) return true;
    
    bool valid = false;
    licenseMessage = "";
    
    // 1. Server-Lizenz
    bool serverOK = Activation();
    if(serverOK)
    {
        valid = true;
        // Server-Lizenz ist aktiv
        serverLicenseStatus = "✓ Server-Lizenz aktiv";
        licenseMessage += "Server: OK | ";
    }
    else
    {
        serverLicenseStatus = "✗ Nicht registriert";
        licenseMessage += "Server: FEHLER | ";
    }
    
    // 2. RoboForex - Verwende gespeicherten Status aus OnInit
    if(UseRoboForexCheck)
    {
        if(roboforexVerified)
        {
            valid = true;
            licenseMessage += "Affiliate: OK | ";
        }
        else
        {
            licenseMessage += "Affiliate: FEHLER | ";
        }
    }
    else
    {
        roboforexStatus = "- Deaktiviert";
    }
    
    if(!valid)
    {
        licenseMessage = "KEINE GÜLTIGE LIZENZ!";
    }
    
    return valid;
}

// Die alte UpdateAffiliateStatusInDatabase Funktion wurde entfernt
// Verwende stattdessen UpdateRoboForexStatusToServer()

//+------------------------------------------------------------------+
//| Update RoboForex Status to Server (via update_robo_status.php)  |
//+------------------------------------------------------------------+
void UpdateRoboForexStatusToServer(string accountNumber, string roboStatus)
{
    // Update RoboForex Status to Server
    
    // Verwende direkt WinInet (funktioniert zuverlässiger)
    UpdateRoboStatusViaWinInet(accountNumber, roboStatus);
}

//+------------------------------------------------------------------+
//| Alternative Update via WinInet                                  |
//+------------------------------------------------------------------+
void UpdateRoboStatusViaWinInet(string accountNumber, string roboStatus)
{
    // Verwende WinInet für Status Update
    
    string agent = "DAX_EA";
    string proxy = "";
    string bypass = "";
    
    int hSession = InternetOpenW(agent, 1, proxy, bypass, 0);
    if(hSession == 0)
    {
        // InternetOpen fehlgeschlagen
        return;
    }
    
    string server = DOMEN;
    string user = "";
    string pass = "";
    
    int hConnect = InternetConnectW(hSession, server, serverPort, 
                                    user, pass, 3, 0, 0);
    if(hConnect == 0)
    {
        InternetCloseHandle(hSession);
        // InternetConnect fehlgeschlagen
        return;
    }
    
    // Erstelle Request Path mit Parametern (inkl. Account-Name für Demo-Tracking)
    string method = "GET";
    string path = "/files/update_robo_status.php?" +
                 "account=" + accountNumber + 
                 "&status=" + roboStatus +
                 "&program=" + PROGRAM_NAME +
                 "&account_name=" + currentAccountName +
                 "&known_demo=" + (isKnownDemoAccount ? "yes" : "no") +
                 "&api_key=" + ROBOFOREX_API_KEY;
    string version = "";
    string referer = "";
    long context = 0;
    
    int hRequest = HttpOpenRequestW(hConnect, method, path, 
                                    version, referer, context, 
                                    0x84800200, 0); // HTTPS Flags
    
    if(hRequest == 0)
    {
        InternetCloseHandle(hConnect);
        InternetCloseHandle(hSession);
        // HttpOpenRequest fehlgeschlagen
        return;
    }
    
    string headers = "";
    uchar post[];
    
    if(HttpSendRequestW(hRequest, headers, 0, post, 0))
    {
        uchar buffer[1024];
        uint bytesRead = 0;
        
        if(InternetReadFile(hRequest, buffer, 1024, bytesRead))
        {
            string response = CharArrayToString(buffer, 0, (int)bytesRead);
            // Debug: WinInet Response
            if(StringFind(response, "error") >= 0)
            {
                Print("⚠ Status-Update fehlgeschlagen: ", response);
            }
            
            if(StringFind(response, "success") >= 0)
            {
                // Status via WinInet aktualisiert
            }
        }
    }
    else
    {
        // HttpSendRequest fehlgeschlagen
    }
    
    InternetCloseHandle(hRequest);
    InternetCloseHandle(hConnect);
    InternetCloseHandle(hSession);
}

//+------------------------------------------------------------------+
//| Lizenz-Anzeige aktualisieren                                    |
//+------------------------------------------------------------------+
void UpdateLicenseDisplay()
{
    if(!ShowLicenseInfo) return;
    
    if(MQLInfoInteger(MQL_TESTER))
    {
        // Im Backtest nur eine Zeile
        string objName = "LicenseInfo";
        if(ObjectFind(0, objName) < 0)
        {
            ObjectCreate(0, objName, OBJ_LABEL, 0, 0, 0);
            ObjectSetInteger(0, objName, OBJPROP_CORNER, CORNER_LEFT_UPPER);
            ObjectSetInteger(0, objName, OBJPROP_XDISTANCE, 10);
            ObjectSetInteger(0, objName, OBJPROP_YDISTANCE, 30);
            ObjectSetInteger(0, objName, OBJPROP_COLOR, clrYellow);
            ObjectSetInteger(0, objName, OBJPROP_FONTSIZE, 9);
        }
        ObjectSetString(0, objName, OBJPROP_TEXT, "BACKTEST MODUS - Keine Lizenzprüfung");
    }
    else
    {
        // Live/Demo Modus - Drei separate Zeilen
        
        // Zeile 1: Überschrift
        string obj1 = "LicenseHeader";
        if(ObjectFind(0, obj1) < 0)
        {
            ObjectCreate(0, obj1, OBJ_LABEL, 0, 0, 0);
            ObjectSetInteger(0, obj1, OBJPROP_CORNER, CORNER_LEFT_UPPER);
            ObjectSetInteger(0, obj1, OBJPROP_XDISTANCE, 10);
            ObjectSetInteger(0, obj1, OBJPROP_YDISTANCE, 30);
            ObjectSetInteger(0, obj1, OBJPROP_COLOR, clrWhite);
            ObjectSetInteger(0, obj1, OBJPROP_FONTSIZE, 9);
            ObjectSetString(0, obj1, OBJPROP_FONT, "Arial Bold");
        }
        ObjectSetString(0, obj1, OBJPROP_TEXT, "═══ EA STATUS ═══");
        
        // Zeile 2: Server-Lizenz mit Ablaufdatum
        string obj2 = "ServerLicense";
        if(ObjectFind(0, obj2) < 0)
        {
            ObjectCreate(0, obj2, OBJ_LABEL, 0, 0, 0);
            ObjectSetInteger(0, obj2, OBJPROP_CORNER, CORNER_LEFT_UPPER);
            ObjectSetInteger(0, obj2, OBJPROP_XDISTANCE, 10);
            ObjectSetInteger(0, obj2, OBJPROP_YDISTANCE, 50);
            ObjectSetInteger(0, obj2, OBJPROP_FONTSIZE, 9);
        }
        
        // Formatiere Anzeige für Server-Lizenz
        string serverText = "Server-Lizenz: ";
        
        // Farbe basierend auf Status
        color serverColor = clrGray;
        if(StringFind(serverLicenseStatus, "✓") >= 0)
        {
            // Server-Lizenz ist aktiv
            // Prüfe ob wir eine gespeicherte Ablaufzeit haben
            if(serverLicenseExpiry > 0)
            {
                int daysLeft = (int)((serverLicenseExpiry - TimeCurrent()) / 86400);
                if(daysLeft > 0)
                {
                    serverText += "✓ Aktiv (" + IntegerToString(daysLeft) + " Tage verbleibend)";
                    // Farbe nach verbleibenden Tagen
                    if(daysLeft <= 7)
                        serverColor = clrYellow;  // Weniger als 7 Tage = Gelb
                    else if(daysLeft <= 30)
                        serverColor = clrLightGreen;  // Weniger als 30 Tage = Hellgrün
                    else
                        serverColor = clrLime;  // Mehr als 30 Tage = Grün
                }
                else
                {
                    serverText += "✗ Abgelaufen";
                    serverColor = clrRed;
                }
            }
            else
            {
                // Standard-Anzeige ohne Zeitinfo
                serverText += serverLicenseStatus;
                serverColor = clrLime;
            }
        }
        else if(StringFind(serverLicenseStatus, "✗") >= 0)
        {
            serverColor = clrRed;       // Fehler = Rot
            serverText += serverLicenseStatus;
        }
        else
        {
            serverColor = clrYellow;    // Prüfung = Gelb
            serverText += serverLicenseStatus;
        }
        
        ObjectSetInteger(0, obj2, OBJPROP_COLOR, serverColor);
        ObjectSetString(0, obj2, OBJPROP_TEXT, serverText);
        
        // Zeile 3: Affiliate Konto
        string obj3 = "RoboForexLicense";
        if(ObjectFind(0, obj3) < 0)
        {
            ObjectCreate(0, obj3, OBJ_LABEL, 0, 0, 0);
            ObjectSetInteger(0, obj3, OBJPROP_CORNER, CORNER_LEFT_UPPER);
            ObjectSetInteger(0, obj3, OBJPROP_XDISTANCE, 10);
            ObjectSetInteger(0, obj3, OBJPROP_YDISTANCE, 70);
            ObjectSetInteger(0, obj3, OBJPROP_FONTSIZE, 9);
        }
        
        // Affiliate Status Anzeige
        string affiliateText = "Affiliate Konto: ";
        color roboColor = clrGray;
        
        if(roboforexVerified)
        {
            affiliateText += "Unlimitiert";
            roboColor = clrLime;
        }
        else if(StringFind(roboforexStatus, "Deaktiviert") >= 0)
        {
            affiliateText += "Deaktiviert";
            roboColor = clrGray;
        }
        else
        {
            affiliateText += "Nicht verifiziert";
            roboColor = clrRed;
        }
        
        ObjectSetInteger(0, obj3, OBJPROP_COLOR, roboColor);
        ObjectSetString(0, obj3, OBJPROP_TEXT, affiliateText);
        
        // Zeile 4: Demo-Status (nur wenn relevant)
        if(demoStatus != "UNLIMITED" && demoStatus != "SERVER_LICENSE" && demoStatus != "")
        {
            string obj4 = "DemoStatus";
            if(ObjectFind(0, obj4) < 0)
            {
                ObjectCreate(0, obj4, OBJ_LABEL, 0, 0, 0);
                ObjectSetInteger(0, obj4, OBJPROP_CORNER, CORNER_LEFT_UPPER);
                ObjectSetInteger(0, obj4, OBJPROP_XDISTANCE, 10);
                ObjectSetInteger(0, obj4, OBJPROP_YDISTANCE, 90);
                ObjectSetInteger(0, obj4, OBJPROP_FONTSIZE, 9);
            }
            
            string demoText = "Demo-Status: ";
            color demoColor = clrWhite;
            
            if(demoStatus == "VALID")
            {
                demoText += "✓ Aktiv (" + IntegerToString(demoRemainingDays) + " Tage)";
                demoColor = (demoRemainingDays > 7) ? clrLime : clrYellow;
            }
            else if(demoStatus == "EXPIRED")
            {
                demoText += "✗ TESTZEITRAUM ABGELAUFEN";
                demoColor = clrRed;
            }
            else if(demoStatus == "CHECKING")
            {
                demoText += "Prüfung läuft...";
                demoColor = clrYellow;
            }
            else if(demoStatus == "WAITING")
            {
                demoText += "Warte auf Server...";
                demoColor = clrGray;
            }
            
            ObjectSetInteger(0, obj4, OBJPROP_COLOR, demoColor);
            ObjectSetString(0, obj4, OBJPROP_TEXT, demoText);
            
            // Gesamt-Status in Zeile 5
            string obj5 = "LicenseOverall";
            if(ObjectFind(0, obj5) < 0)
            {
                ObjectCreate(0, obj5, OBJ_LABEL, 0, 0, 0);
                ObjectSetInteger(0, obj5, OBJPROP_CORNER, CORNER_LEFT_UPPER);
                ObjectSetInteger(0, obj5, OBJPROP_XDISTANCE, 10);
                ObjectSetInteger(0, obj5, OBJPROP_YDISTANCE, 110);
                ObjectSetInteger(0, obj5, OBJPROP_FONTSIZE, 9);
                ObjectSetString(0, obj5, OBJPROP_FONT, "Arial Bold");
            }
            bool anyValid = ((StringFind(serverLicenseStatus, "✓") >= 0) || roboforexVerified || demoStatus == "VALID");
            ObjectSetInteger(0, obj5, OBJPROP_COLOR, anyValid ? clrLime : clrRed);
            ObjectSetString(0, obj5, OBJPROP_TEXT, anyValid ? "→ EA AKTIV" : "→ LIZENZ FEHLT!");
        }
        else
        {
            // Zeile 4: Gesamt-Status (wenn kein Demo-Status angezeigt wird)
            string obj4 = "LicenseOverall";
            if(ObjectFind(0, obj4) < 0)
            {
                ObjectCreate(0, obj4, OBJ_LABEL, 0, 0, 0);
                ObjectSetInteger(0, obj4, OBJPROP_CORNER, CORNER_LEFT_UPPER);
                ObjectSetInteger(0, obj4, OBJPROP_XDISTANCE, 10);
                ObjectSetInteger(0, obj4, OBJPROP_YDISTANCE, 90);
                ObjectSetInteger(0, obj4, OBJPROP_FONTSIZE, 9);
                ObjectSetString(0, obj4, OBJPROP_FONT, "Arial Bold");
            }
            bool anyValid = (StringFind(serverLicenseStatus, "✓") >= 0) || roboforexVerified;
            ObjectSetInteger(0, obj4, OBJPROP_COLOR, anyValid ? clrLime : clrRed);
            ObjectSetString(0, obj4, OBJPROP_TEXT, anyValid ? "→ EA AKTIV" : "→ LIZENZ FEHLT!");
            
            // Demo-Status Objekt löschen falls vorhanden
            if(ObjectFind(0, "DemoStatus") >= 0)
            {
                ObjectDelete(0, "DemoStatus");
            }
        }
    }
}

//+------------------------------------------------------------------+
//| DAX Performance Display aktualisieren                           |
//+------------------------------------------------------------------+
void UpdatePerformanceDisplay()
{
    if(!ShowPerformance) return;
    
    // Hole heutige und gestrige Schlusskurse für Symbol Performance
    double close_today = iClose(_Symbol, PERIOD_D1, 0);
    double close_yesterday = iClose(_Symbol, PERIOD_D1, 1);
    
    if(close_yesterday == 0 || close_today == 0) return;
    
    // Berechne Performance in Punkten und Prozent
    double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
    double performance_points = (close_today - close_yesterday) / point;
    double performance_percent = (close_today - close_yesterday) / close_yesterday * 100;
    
    // Performance Display Objekt - LINKS unter EA AKTIV
    string perfObj = "PerformanceDisplay";
    if(ObjectFind(0, perfObj) < 0)
    {
        ObjectCreate(0, perfObj, OBJ_LABEL, 0, 0, 0);
        ObjectSetInteger(0, perfObj, OBJPROP_CORNER, CORNER_LEFT_UPPER);
        ObjectSetInteger(0, perfObj, OBJPROP_XDISTANCE, 10);
        ObjectSetInteger(0, perfObj, OBJPROP_YDISTANCE, 115);
        ObjectSetInteger(0, perfObj, OBJPROP_FONTSIZE, 10);
        ObjectSetString(0, perfObj, OBJPROP_FONT, "Arial Bold");
    }
    
    // Formatiere Performance Text: Symbol + Punkte + Prozent
    string sign_points = (performance_points >= 0) ? "+" : "";
    string sign_percent = (performance_percent >= 0) ? "+" : "";
    string perfText = _Symbol + ": " + sign_points + DoubleToString(performance_points, 1) + " (" + sign_percent + DoubleToString(performance_percent, 2) + "%)";
    
    // Farbe basierend auf Performance
    color perfColor = clrWhite;
    if(performance_percent > 0.5)
        perfColor = clrLime;      // Deutlich positiv = Grün
    else if(performance_percent < -0.5)
        perfColor = clrRed;       // Deutlich negativ = Rot
    else if(performance_percent > 0)
        perfColor = clrYellow;    // Leicht positiv = Gelb
    else
        perfColor = clrOrange;    // Leicht negativ = Orange
    
    ObjectSetInteger(0, perfObj, OBJPROP_COLOR, perfColor);
    ObjectSetString(0, perfObj, OBJPROP_TEXT, perfText);
}

//+------------------------------------------------------------------+
//| Trade Status Display aktualisieren (Erfolg oder Ablehnung)     |
//+------------------------------------------------------------------+
void UpdateTradeStatusDisplay()
{
    if(!ShowTradeStatus) return;
    
    // Trade-Status Info anzeigen
    string objStatus = "TradeStatus";
    
    if(ObjectFind(0, objStatus) < 0)
    {
        ObjectCreate(0, objStatus, OBJ_LABEL, 0, 0, 0);
        ObjectSetInteger(0, objStatus, OBJPROP_CORNER, CORNER_LEFT_UPPER);
        ObjectSetInteger(0, objStatus, OBJPROP_XDISTANCE, 10);
        ObjectSetInteger(0, objStatus, OBJPROP_YDISTANCE, 150);  // Unter den anderen Anzeigen
        ObjectSetInteger(0, objStatus, OBJPROP_FONTSIZE, 9);
        ObjectSetString(0, objStatus, OBJPROP_FONT, "Arial");
    }
    
    // Text und Farbe setzen
    string statusText = "";
    color statusColor = clrWhite;
    
    if(lastTradeStatus == "SUCCESS")
    {
        // Erfolgreicher Trade - zeige Details
        string timeStr = TimeToString(lastTradeAttemptTime, TIME_MINUTES);
        string dateStr = TimeToString(lastTradeAttemptTime, TIME_DATE);
        
        // Format: "Trade heute: 18:00 - DE40Cash - 0.01 Lots"
        statusText = "Trade " + dateStr + " " + timeStr + " - " + lastTradeSymbol + " - " + 
                     DoubleToString(lastTradeLotSize, 2) + " Lots";
        statusColor = clrLime;  // Grün für Erfolg
    }
    else if(lastTradeStatus == "REJECTED")
    {
        // Abgelehnter Trade - zeige Grund und Zeit
        string timeStr = TimeToString(lastTradeAttemptTime, TIME_MINUTES);
        string dateStr = TimeToString(lastTradeAttemptTime, TIME_DATE);
        
        // Prüfe ob es ein Lizenz-Problem ist
        if(StringFind(lastRejectionReason, "LIZENZ") >= 0 || 
           StringFind(lastRejectionReason, "TESTZEITRAUM") >= 0)
        {
            // Lizenz-Problem - spezielle Anzeige
            statusText = "BLOCKIERT: " + lastRejectionReason;
            statusColor = clrRed;  // Rot für Lizenz-Probleme
        }
        else
        {
            // Filter-Problem - normale Anzeige
            statusText = "Kein Trade: " + dateStr + " " + timeStr + " - " + lastRejectionReason;
            
            // Farbe nach Filter-Typ
            if(lastRejectionReason == "Pre-Filter")
                statusColor = clrOrange;
            else if(lastRejectionReason == "Gap Filter")
                statusColor = clrYellow;
            else if(StringFind(lastRejectionReason, "ATR") >= 0 || 
                    StringFind(lastRejectionReason, "Bollinger") >= 0 ||
                    StringFind(lastRejectionReason, "StdDev") >= 0)
                statusColor = clrCyan;  // Volatilitäts-Filter
            else
                statusColor = clrLightGray;  // Andere Filter (RSI, ADX, MACD)
        }
    }
    
    // Text setzen oder ausblenden
    if(statusText == "")
    {
        ObjectSetString(0, objStatus, OBJPROP_TEXT, "");
    }
    else
    {
        ObjectSetInteger(0, objStatus, OBJPROP_COLOR, statusColor);
        ObjectSetString(0, objStatus, OBJPROP_TEXT, statusText);
    }
}
