# Trade Rejection Display System - the_don v1.15

## ✅ Implementiert am 28.08.2025

### Was wurde hinzugefügt:
Ein **Trade Rejection Display System**, das im Chart anzeigt, warum an einem bestimmten Tag kein Trade eingegangen wurde.

### Neuer Parameter:
```cpp
input bool ShowTradeRejection = true;  // Trade-Ablehnungsgrund anzeigen
```

### Wie es funktioniert:

1. **Beim Trade-Versuch:** Wenn der EA versucht einen Trade zu öffnen und ein Filter dies verhindert, wird der Grund gespeichert
2. **Chart-Anzeige:** Der Ablehnungsgrund wird im Chart angezeigt mit dem Text "Kein Trade heute: [Grund]"
3. **Farbcodierung:** Verschiedene Filter haben unterschiedliche Farben:
   - **Orange:** Pre-Filter (versteckte Filter)
   - **Gelb:** Gap Filter
   - **Cyan:** Volatilitäts-Filter (ATR, Bollinger, StdDev)
   - **Hellgrau:** Andere Filter (RSI, ADX, MACD)

### Mögliche Ablehnungsgründe:

- **"Pre-Filter"** - Versteckter StochRSI Filter hat Trade verhindert
- **"Gap Filter"** - Tägliche Gap-Grenze überschritten
- **"ATR Filter"** - ATR-Volatilität zu niedrig
- **"Bollinger Filter"** - Bollinger Band Width zu gering
- **"StdDev Filter"** - Standard Deviation zu niedrig
- **"RSI Filter"** - RSI überkauft/überverkauft
- **"ADX Filter"** - ADX unter Minimum (kein Trend)
- **"MACD Filter"** - MACD-Signal ungünstig

### Technische Details:

#### Neue globale Variablen (Zeile 36-39):
```cpp
// Trade Rejection Tracking
string lastRejectionReason = "";      // Grund für letzten abgelehnten Trade
datetime lastRejectionTime = 0;        // Zeit der letzten Ablehnung
string todayRejectionReason = "";      // Heutiger Ablehnungsgrund
```

#### OpenPosition() Funktion erweitert:
- Bei jedem Filter-Check wird der Ablehnungsgrund gespeichert
- UpdateTradeRejectionDisplay() wird aufgerufen

#### Neue Funktion UpdateTradeRejectionDisplay() (Zeile 1728-1785):
- Zeigt den Ablehnungsgrund im Chart an
- Position: Unter den anderen Anzeigen (Y=150)
- Nur wenn Trade heute abgelehnt wurde

### Beispiele im Chart:

- **"Kein Trade heute: Gap Filter"** - Der heutige Gap war zu groß
- **"Kein Trade heute: Pre-Filter"** - Der versteckte StochRSI Filter hat verhindert
- **"Kein Trade heute: RSI Filter"** - RSI war überkauft/überverkauft

### Version:
- **the_don v1.15** - Trade Rejection Display System
- Kompiliert: 28.08.2025 18:33 Uhr
- Dateigröße: 118286 Bytes

### Nutzen:
- Nutzer sieht sofort warum kein Trade eingegangen wurde
- Hilft bei der Analyse und Optimierung der Filter-Einstellungen
- Transparenz über EA-Entscheidungen
- Besseres Verständnis der Marktsituation