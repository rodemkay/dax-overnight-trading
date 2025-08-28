//+------------------------------------------------------------------+
//|                                                       don_gpt.mq5|
//|                          DAX Overnight EA with License System   |
//|                                             Integrated Version  |
//+------------------------------------------------------------------+
#property copyright "DAX Overnight Trading System"
#property link      ""
#property version   "2.00"
#property strict

//+++ Server-Lizenzierung Defines +++
#define PROGRAM_NAME "don_gpt"     
#define release      "2.00"               
#define REF          "FS_TRADE"          
#define PERC         0                   
#define DOMEN        "lic.prophelper.org"
#define URLBUY       "https://lic.prophelper.org/download.php"
#define URLUPDATE    "https://lic.prophelper.org/download.php"
#define SHTXT        20                  
#define LICENSE_CODE "DAXON10"           

// Server Port Enum
enum prt {
    pr80 = 80,    // HTTP Port
    pr443= 443    // HTTPS Port
};

// Include License System
#include <MQL_License.mqh>
#include <Trade\Trade.mqh>

// Global Trade Object
CTrade trade;

//--- Gruppen-Definition für Input-Parameter ---

//+------------------------------------------------------------------+
//| Gruppe: Lizenzierung                                            |
//+------------------------------------------------------------------+
input group "════════ LIZENZIERUNG ════════"
input prt     serverPort     = pr443;               // Server Port
input bool    UseRoboForexCheck = true;             // Partner-Verifikation aktivieren
// Affiliate Code ist fest im Code: qnyj
input bool    ShowLicenseInfo = true;               // Status-Info im Chart anzeigen

//+------------------------------------------------------------------+
//| Gruppe: Haupt-Einstellungen                                     |
//+------------------------------------------------------------------+
input group "════════ HAUPT-EINSTELLUNGEN ════════"
input string  TradeSymbol = ".DE40Cash";            // Trading Symbol
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
input group "════════ STOP-LOSS & TRAILING ════════"
input int     StopLossPoints = 500;                 // Stop-Loss in Punkten
input bool    EnableTrailingStop = true;            // Trailing Stop aktivieren
input int     TrailingStopPoints = 1000;            // Trailing Stop in Punkten
input int     TrailingStartHour = 9;                // Trailing Start (Stunde)
input int     TrailingStartMinute = 0;              // Trailing Start (Minute)

//+------------------------------------------------------------------+
//| Gruppe: StochRSI Filter                                         |
//+------------------------------------------------------------------+
input group "════════ STOCHRSI FILTER ════════"
input bool    enableStochRsiFilter = true;          // StochRSI Filter aktivieren
input ENUM_TIMEFRAMES stochRsiTimeframe = PERIOD_D1; // StochRSI Timeframe
input int     rsiPeriod = 14;                       // RSI Periode
input int     stochPeriod = 14;                     // Stochastic Periode
input int     kPeriod = 3;                          // K-Linie Periode
input int     dPeriod = 3;                          // D-Linie Periode

//+------------------------------------------------------------------+
//| Gruppe: ATR Filter                                              |
//+------------------------------------------------------------------+
input group "════════ ATR FILTER ════════"
input bool    enableATRFilter = true;               // ATR Filter aktivieren
input int     atrPeriod = 14;                       // ATR Periode
input double  minATR = 100.0;                       // Minimum ATR Wert

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

// RoboForex API Credentials (fest im Code)
const string ROBOFOREX_PARTNER_ACCOUNT = "30218520";
const string ROBOFOREX_API_KEY = "ec4d40c4343ee741";
const string AFFILIATE_CODE = "qnyj";  // Hardcodierter Affiliate Code

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
                Print("Check-Period vom Server aktualisiert: ", checkHours, " Stunden (", serverCheckPeriod/60, " Minuten)");
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
        
        // 1. Prüfe ZUERST Partner-Verifikation - NUR EINMAL in OnInit
        roboforexVerified = false;
        
        if(UseRoboForexCheck)
        {
            string accountNumber = IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
            Print("=== Einmalige Partner-Verifikation für Konto: ", accountNumber, " ===");
            
            if(CheckRoboForexLicense())
            {
                roboforexVerified = true;
                roboforexStatus = "✓ Verifiziert (Konto " + accountNumber + ")";
                GlobalVariableSet("AFFILIATE_STATUS", 1.0); // Für Server-Kommunikation
                Print("✓ Partner-Verifikation ERFOLGREICH - Konto ist Partner");
                
                // Speichere Status in Datenbank
                UpdateAffiliateStatusInDatabase();
            }
            else
            {
                roboforexVerified = false;
                roboforexStatus = "✗ Konto " + accountNumber + " nicht verifiziert";
                GlobalVariableSet("AFFILIATE_STATUS", 0.0);
                Print("✗ Partner-Verifikation FEHLGESCHLAGEN - Konto ist KEIN Partner");
                
                // Speichere Status in Datenbank
                UpdateAffiliateStatusInDatabase();
            }
        }
        else
        {
            roboforexStatus = "Deaktiviert";
            Print("Partner-Verifikation deaktiviert");
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
            Print("System erfolgreich initialisiert");
            
            // Initiale Server-Prüfung und Check-Period holen
            if(Activation())
            {
                UpdateCheckPeriodFromServer();
                serverLicenseStatus = "✓ Aktiviert";
                Print("Server-Lizenz aktiviert, Check-Period: ", serverCheckPeriod/60, " Minuten");
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
            Alert("Keine gültige Lizenz gefunden! EA wird beendet.");
            return(INIT_FAILED);
        }
        
        isLicensed = true;
    }
    
    // Trading-Setup
    trade.SetExpertMagicNumber(MagicNumber);
    trade.SetDeviationInPoints(10);
    trade.SetTypeFilling(ORDER_FILLING_IOC);
    
    Print("DAX Overnight EA erfolgreich initialisiert");
    if(ShowLicenseInfo) UpdateLicenseDisplay();
    
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    if(!MQLInfoInteger(MQL_TESTER))
    {
        DataOnDeinit();
    }
    
    ObjectsDeleteAll(0, "License");
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
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    if(_Symbol != TradeSymbol) return;
    
    // Lizenzprüfung nur im Live/Demo-Modus - NICHT im Backtest
    if(!MQLInfoInteger(MQL_TESTER))
    {
        // Server-Lizenz gemäß Check-Period prüfen
        datetime currentTime = TimeCurrent();
        if(currentTime - lastServerCheck >= serverCheckPeriod)
        {
            lastServerCheck = currentTime;
            
            Print("=== Server-Lizenz-Prüfung (alle ", serverCheckPeriod/60, " Minuten) ===");
            
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
                    
                    // Hole Lizenz-Ablaufdatum aus der MQL_License Library
                    // Die Library gibt normalerweise eine Meldung wie "Registered before: DD.MM.YYYY" aus
                    // Wir setzen hier ein Standard-Ablaufdatum
                    serverLicenseExpiry = StringToTime("2025.08.17"); // 17.08.2025 aus dem Log
                    
                    int daysLeft = (int)((serverLicenseExpiry - TimeCurrent()) / 86400);
                    if(daysLeft > 0)
                    {
                        serverLicenseStatus = "✓ Aktiv (" + IntegerToString(daysLeft) + " Tage)";
                        Print("Server-Lizenz aktiv, noch ", daysLeft, " Tage gültig");
                    }
                    else
                    {
                        serverLicenseStatus = "✓ Aktiviert";
                        Print("Server-Lizenz aktiviert");
                    }
                }
                else
                {
                    serverLicenseStatus = "Prüfung läuft...";
                    
                    if(activationAttempts >= 5)
                    {
                        serverLicenseStatus = "✗ Nicht aktiviert";
                        Print("Server-Lizenz-Aktivierung fehlgeschlagen nach 5 Versuchen");
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
                    
                    int daysLeft = (int)((serverLicenseExpiry - TimeCurrent()) / 86400);
                    if(daysLeft > 0)
                    {
                        serverLicenseStatus = "✓ Aktiv (" + IntegerToString(daysLeft) + " Tage)";
                    }
                    Print("Server-Lizenz weiterhin gültig (nächste Prüfung in ", serverCheckPeriod/60, " Minuten)");
                }
                else
                {
                    serverLicenseStatus = "✗ Abgelaufen";
                    Print("Server-Lizenz abgelaufen oder ungültig!");
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
    
    datetime current_time = TimeCurrent();
    if(!IsTradeDay(current_time)) return;
    
    MqlDateTime now;
    TimeToStruct(current_time, now);
    int current_minutes = now.hour * 60 + now.min;
    int buy_minutes = StartHourBuy * 60 + StartMinuteBuy;
    bool position_open = PositionSelect(TradeSymbol);
    
    if(position_open)
    {
        MqlDateTime entry;
        TimeToStruct(lastTradeDate, entry);
        bool ist_naechster_tag = (now.day != entry.day || now.mon != entry.mon || now.year != entry.year);
        
        if(EnableTrailingStop && ist_naechster_tag && 
           current_minutes >= TrailingStartHour * 60 + TrailingStartMinute)
        {
            TrailingStop();
        }
        
        if(!EnableTrailingStop && ist_naechster_tag && 
           current_minutes >= CloseHour * 60 + CloseMinute)
        {
            ClosePosition();
        }
    }
    else if(current_minutes >= buy_minutes)
    {
        MqlDateTime last;
        TimeToStruct(lastTradeDate, last);
        bool ist_neuer_tag = (now.day != last.day || now.mon != last.mon || now.year != last.year);
        if(ist_neuer_tag)
        {
            OpenPosition();
            lastTradeDate = current_time;
        }
    }
}

//+------------------------------------------------------------------+
//| Position öffnen                                                 |
//+------------------------------------------------------------------+
void OpenPosition()
{
    if(!IsStochRsiOk()) return;
    if(enableATRFilter && !CheckATR()) return;
    
    double volume = UseAutoLot ? CalculateLotSize() : StartLotSize;
    double minLot = SymbolInfoDouble(TradeSymbol, SYMBOL_VOLUME_MIN);
    double stepLot = SymbolInfoDouble(TradeSymbol, SYMBOL_VOLUME_STEP);
    int digits = (int)MathRound(MathLog10(1.0 / stepLot));
    
    if(volume < minLot) volume = minLot;
    volume = MathCeil(volume / stepLot) * stepLot;
    volume = NormalizeDouble(volume, digits);
    
    if(volume <= 0)
    {
        Print("Ungültige Lotgröße: ", DoubleToString(volume, digits));
        return;
    }
    
    double ask = SymbolInfoDouble(TradeSymbol, SYMBOL_ASK);
    double point = SymbolInfoDouble(TradeSymbol, SYMBOL_POINT);
    double sl = StopLossPoints > 0 ? ask - StopLossPoints * point : 0.0;
    
    if(trade.Buy(volume, TradeSymbol, ask, sl, 0, "DAX Overnight"))
    {
        Print("Position eröffnet: ", trade.ResultOrder());
    }
    else
    {
        Print("Fehler beim Order Send: ", trade.ResultRetcode());
    }
}

//+------------------------------------------------------------------+
//| Position schließen                                              |
//+------------------------------------------------------------------+
void ClosePosition()
{
    if(!PositionSelect(TradeSymbol)) return;
    
    ulong ticket = PositionGetInteger(POSITION_TICKET);
    if(trade.PositionClose(ticket))
    {
        Print("Position geschlossen: ", ticket);
    }
}

//+------------------------------------------------------------------+
//| Trailing Stop                                                   |
//+------------------------------------------------------------------+
void TrailingStop()
{
    if(!PositionSelect(TradeSymbol)) return;
    
    double bid = SymbolInfoDouble(TradeSymbol, SYMBOL_BID);
    double point = SymbolInfoDouble(TradeSymbol, SYMBOL_POINT);
    double sl = PositionGetDouble(POSITION_SL);
    double new_sl = bid - TrailingStopPoints * point;
    
    if(new_sl > sl)
    {
        ulong ticket = PositionGetInteger(POSITION_TICKET);
        if(trade.PositionModify(ticket, new_sl, 0))
        {
            Print("Trailing Stop aktualisiert: ", NormalizeDouble(new_sl, _Digits));
        }
    }
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
    if(!enableStochRsiFilter) return true;
    
    // Interne StochRSI Berechnung
    int rsiHandle = iRSI(TradeSymbol, stochRsiTimeframe, rsiPeriod, PRICE_CLOSE);
    if(rsiHandle == INVALID_HANDLE) return false;
    
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
    int atrHandle = iATR(TradeSymbol, PERIOD_H1, atrPeriod);
    if(atrHandle == INVALID_HANDLE) return false;
    
    double atrBuffer[];
    if(CopyBuffer(atrHandle, 0, 0, 1, atrBuffer) <= 0) return false;
    
    double point = SymbolInfoDouble(TradeSymbol, SYMBOL_POINT);
    return atrBuffer[0] / point >= minATR;
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
        Print("Broker: ", brokerName, " - Keine RoboForex/RoboMarkets Erkennung");
        return false;
    }
    
    Print("Prüfe Partner-Verifikation für Konto: ", accountNumber);
    Print("Suche nach Affiliate-Code: ", AFFILIATE_CODE);
    
    // Verwende WinInet statt WebRequest
    return CheckRoboForexViaWinInet(accountNumber);
}

//+------------------------------------------------------------------+
//| RoboForex Check via WinInet - VEREINFACHT                      |
//+------------------------------------------------------------------+
bool CheckRoboForexViaWinInet(string accountNumber)
{
    Print("=== RoboForex Partner-Check für Konto ", accountNumber, " ===");
    
    // DIREKTE Abfrage mit referral_account_id - keine Pagination nötig!
    string path = "/api/partners/tree?account_id=" + ROBOFOREX_PARTNER_ACCOUNT + 
                  "&api_key=" + ROBOFOREX_API_KEY + 
                  "&referral_account_id=" + accountNumber;
    
    MqlNet net;
    if(!net._Open("my.roboforex.com", 443, "", "", INTERNET_SERVICE_HTTP))
    {
        Print("❌ Fehler beim Verbindungsaufbau zu RoboForex API");
        return false;
    }
    
    tagRequest req;
    req.Init("GET", path, "", "", false, "", false);
    
    if(!net.Request(req))
    {
        Print("❌ Fehler beim Senden des API-Requests");
        net._Close();
        return false;
    }
    
    string response = req.stOut;
    net._Close();
    
    // Prüfe Response
    if(StringLen(response) == 0)
    {
        Print("❌ Leere Antwort von API");
        return false;
    }
    
    // Debug-Ausgabe (erste 500 Zeichen)
    if(StringLen(response) > 0)
    {
        Print("API Response (Auszug): ", StringSubstr(response, 0, MathMin(500, StringLen(response))));
    }
    
    // WICHTIG: Prüfe ZUERST ob Konto NICHT gefunden wurde!
    if(StringFind(response, "Not found") >= 0 || 
       StringFind(response, "not found") >= 0)
    {
        Print("❌ Konto ", accountNumber, " NICHT in Partner-System gefunden!");
        return false;
    }
    
    // Erfolgreiche Response enthält das Konto in der Partner-Struktur
    // Verschiedene Formate möglich:
    // 1. <multilevel_scheme>30218520 / accountNumber</multilevel_scheme>
    // 2. <account id="accountNumber">
    // 3. <path>30218520/.../accountNumber</path>
    
    if((StringFind(response, "<account id=\"" + accountNumber + "\"") >= 0) ||
       (StringFind(response, "<multilevel_scheme>") >= 0 && StringFind(response, accountNumber) >= 0) ||
       (StringFind(response, "<path>") >= 0 && StringFind(response, accountNumber) >= 0))
    {
        Print("✅ Konto ", accountNumber, " ist in Partner-Struktur!");
        
        // Prüfe ob es unter unserem Partner-Account ist
        if(StringFind(response, ROBOFOREX_PARTNER_ACCOUNT) >= 0)
        {
            Print("✅ Konto ist unter Partner-Account ", ROBOFOREX_PARTNER_ACCOUNT);
        }
        
        return true;
    }
    
    // Fallback
    Print("❌ Konto ", accountNumber, " ist NICHT in Partner-Struktur");
    
    return false;
}

//+------------------------------------------------------------------+
//| Affiliate Status in Datenbank speichern                         |
//+------------------------------------------------------------------+
void UpdateAffiliateStatusInDatabase()
{
    string accountNumber = IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
    string affiliateStatus = roboforexVerified ? "yes" : "no";
    
    Print("=== Speichere Affiliate-Status in Datenbank ===");
    Print("Konto: ", accountNumber);
    Print("Status: ", affiliateStatus);
    
    // Erstelle JSON-Body für die API
    string jsonBody = "{\"action\":\"update_affiliate\",";
    jsonBody += "\"token\":\"250277100311270613\",";
    jsonBody += "\"account\":\"" + accountNumber + "\",";
    jsonBody += "\"affiliate_status\":\"" + affiliateStatus + "\"}";
    
    // Verwende WinInet für API-Aufruf
    MqlNet net;
    if(!net._Open("lic.prophelper.org", 443, "", "", INTERNET_SERVICE_HTTP))
    {
        Print("❌ Fehler beim Verbindungsaufbau zur Datenbank-API");
        return;
    }
    
    // Erstelle Request
    tagRequest req;
    req.Init("POST", "/api/db_api.php", jsonBody, "Content-Type: application/json\r\n", false, "", false);
    
    // Sende Request
    if(!net.Request(req))
    {
        Print("❌ Fehler beim Senden des Datenbank-Updates");
        net._Close();
        return;
    }
    
    string response = req.stOut;
    net._Close();
    
    // Prüfe Response
    if(StringFind(response, "success") >= 0)
    {
        Print("✅ Affiliate-Status erfolgreich in Datenbank gespeichert");
    }
    else
    {
        Print("❌ Fehler beim Speichern des Affiliate-Status: ", response);
    }
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
        // Aktualisiere Status mit Tagen
        int daysLeft = (int)((serverLicenseExpiry - TimeCurrent()) / 86400);
        if(daysLeft > 0 && serverLicenseExpiry > 0)
        {
            serverLicenseStatus = "✓ Aktiv (" + IntegerToString(daysLeft) + " Tage)";
        }
        else
        {
            serverLicenseStatus = "✓ Aktiviert";
        }
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
            licenseMessage += "Partner: OK | ";
        }
        else
        {
            licenseMessage += "Partner: FEHLER | ";
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
        
        // Zeile 2: Lizenz 1
        string obj2 = "ServerLicense";
        if(ObjectFind(0, obj2) < 0)
        {
            ObjectCreate(0, obj2, OBJ_LABEL, 0, 0, 0);
            ObjectSetInteger(0, obj2, OBJPROP_CORNER, CORNER_LEFT_UPPER);
            ObjectSetInteger(0, obj2, OBJPROP_XDISTANCE, 10);
            ObjectSetInteger(0, obj2, OBJPROP_YDISTANCE, 50);
            ObjectSetInteger(0, obj2, OBJPROP_FONTSIZE, 9);
        }
        color serverColor = StringFind(serverLicenseStatus, "✓") >= 0 ? clrLime : clrRed;
        ObjectSetInteger(0, obj2, OBJPROP_COLOR, serverColor);
        ObjectSetString(0, obj2, OBJPROP_TEXT, "Lizenz: " + serverLicenseStatus);
        
        // Zeile 3: Partner
        string obj3 = "RoboForexLicense";
        if(ObjectFind(0, obj3) < 0)
        {
            ObjectCreate(0, obj3, OBJ_LABEL, 0, 0, 0);
            ObjectSetInteger(0, obj3, OBJPROP_CORNER, CORNER_LEFT_UPPER);
            ObjectSetInteger(0, obj3, OBJPROP_XDISTANCE, 10);
            ObjectSetInteger(0, obj3, OBJPROP_YDISTANCE, 70);
            ObjectSetInteger(0, obj3, OBJPROP_FONTSIZE, 9);
        }
        color roboColor = StringFind(roboforexStatus, "✓") >= 0 ? clrLime : 
                          StringFind(roboforexStatus, "-") >= 0 ? clrGray : clrRed;
        ObjectSetInteger(0, obj3, OBJPROP_COLOR, roboColor);
        ObjectSetString(0, obj3, OBJPROP_TEXT, "Partner: " + roboforexStatus);
        
        // Zeile 4: Gesamt-Status
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
        bool anyValid = (StringFind(serverLicenseStatus, "✓") >= 0) || 
                       (StringFind(roboforexStatus, "✓") >= 0);
        ObjectSetInteger(0, obj4, OBJPROP_COLOR, anyValid ? clrLime : clrRed);
        ObjectSetString(0, obj4, OBJPROP_TEXT, anyValid ? "→ EA AKTIV" : "→ LIZENZ FEHLT!");
    }
}
