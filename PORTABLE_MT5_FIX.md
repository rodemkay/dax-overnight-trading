# Portable MetaTrader 5 - Include Path Fix

## Problem:
Die portable MT5 Version sucht Include-Dateien im falschen Pfad:
- **Erwartet:** `C:\Users\rodemkay\AppData\Roaming\MetaQuotes\Terminal\[ID]\MQL5\Include\`
- **Tatsächlich:** `C:\portabel\MetaTrader5\MQL5\Include\`

## Lösung implementiert:

### 1. MQL_License.mqh kopiert in BEIDE Pfade:
```
✅ C:\portabel\MetaTrader5\MQL5\Include\MQL_License.mqh (Original)
✅ C:\Users\rodemkay\AppData\Roaming\...\MQL5\Include\MQL_License.mqh (Kopie)
✅ C:\portabel\MetaTrader5\MQL5\Experts\Don\MQL_License.mqh (Backup)
```

### 2. Zwei Include-Optionen im Code:

**Option A - Global Include (empfohlen):**
```cpp
#include <MQL_License.mqh>  // Sucht in Include-Ordnern
```

**Option B - Lokaler Include (falls A nicht funktioniert):**
```cpp
#include "MQL_License.mqh"  // Sucht im EA-Ordner
```

## Terminal ID:
`9EEB4DABED062ABA081392271E6AA903`

## Dateipfade (Linux-Mount):
- **Portable:** `/home/rodemkay/CaufWin11/portabel/MetaTrader5/`
- **AppData:** `/home/rodemkay/CaufWin11/Users/rodemkay/AppData/Roaming/MetaQuotes/Terminal/[ID]/`

## Status:
✅ MQL_License.mqh in allen relevanten Pfaden vorhanden
✅ the_don.mq5 v1.11 bereit zum Kompilieren

## Tipp:
Falls weiterhin Probleme: Ändere in the_don.mq5 Zeile 29:
- Von: `#include <MQL_License.mqh>`
- Zu: `#include "MQL_License.mqh"`