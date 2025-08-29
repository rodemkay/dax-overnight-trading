# the_don v1.25 - Pre-Filter Fix & Verbesserte Meldungen

## Änderungen

### 1. Pre-Filter Spam im Journal behoben
**Problem:** Pre-Filter Ablehnungsmeldungen erschienen alle paar Sekunden im Journal
**Lösung:** ProcessTradeRejection() Funktion modifiziert - Journal-Meldungen nur noch innerhalb 1 Minute zur tatsächlichen Handelszeit (18:00)

```cpp
// Neue Logik in ProcessTradeRejection():
MqlDateTime now;
TimeToStruct(TimeCurrent(), now);
int current_minutes = now.hour * 60 + now.min;
int buy_minutes = StartHourBuy * 60 + StartMinuteBuy;

// Nur loggen wenn wir innerhalb von 1 Minute zur Handelszeit sind
bool isNearTradeTime = MathAbs(current_minutes - buy_minutes) <= 1;

if(ShouldLogToJournal() && isNearTradeTime)
{
    // Journal-Ausgabe nur zur Handelszeit
}
```

### 2. Verbesserte Testzeitraum-Meldungen
**Verbesserung:** Klarere Hinweise auf RoboForex Partner-Option bei abgelaufenem Testzeitraum

#### Initiale Alert-Meldung:
```
TESTZEITRAUM ABGELAUFEN!

Trading wurde deaktiviert.

Optionen zur Fortsetzung:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. KOSTENLOS mit RoboForex:
   → Eröffne ein Konto unter forexsignale.trade/broker
   → Verwende Code: qnyj
   → Unbegrenzte Nutzung als Partner!

2. Server-Lizenz erwerben
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hinweis: Als RoboForex Partner erhältst du
dauerhaft kostenlosen Zugang zu allen EAs!
```

#### Stündliche Erinnerung (kompakter):
```
⚠️ TESTZEITRAUM ABGELAUFEN

Trading ist deaktiviert!

KOSTENLOSE Option:
→ RoboForex Konto: forexsignale.trade/broker
→ Mit Code 'qnyj' als Partner registrieren
→ Unbegrenzte EA-Nutzung!

Alternative: Server-Lizenz erwerben
```

### 3. Display-Text verbessert
- "✗ ABGELAUFEN" → "✗ TESTZEITRAUM ABGELAUFEN"
- Klarere Kennzeichnung des Testzeitraum-Status

## Version
- Bleibt bei v1.25 (wie vom User gewünscht)
- Alle Änderungen in der bestehenden Version integriert

## Dateien
- `/home/rodemkay/CaufWin11/portabel/MetaTrader5/MQL5/Experts/Don/the_don.mq5`

## Deployment
EA muss neu kompiliert und in MetaTrader 5 neu geladen werden.