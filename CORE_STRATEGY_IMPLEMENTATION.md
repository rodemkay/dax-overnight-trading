# Core Strategy Implementation - the_don v1.21

## ✅ Implementiert am 29.08.2025

### Was ist die Core Strategy?
Die **reine Originalstrategie** ohne jegliches Risikomanagement:
- **18:00 Uhr:** Position eröffnen (Long)
- **09:05 Uhr:** Position schließen
- **KEIN Stop-Loss**
- **KEIN Trailing Stop**
- **Reines Buy & Hold über Nacht**

### Neuer Parameter:
```cpp
input bool UseCoreStrategy = false;  // Core Strategy (18:00 rein, 09:05 raus, kein SL)
```
- Standard: **false** (bisherige Funktionalität bleibt erhalten)
- Bei **true**: Aktiviert die Core Strategy

### Was passiert bei UseCoreStrategy = true?

1. **Feste Schließzeit:**
   - Ignoriert CloseHour/CloseMinute Einstellungen
   - Schließt IMMER um 09:05 Uhr

2. **Kein Risikomanagement:**
   - Stop-Loss wird NICHT gesetzt (auch wenn StopLossPoints > 0)
   - Trailing Stop wird NICHT aktiviert
   - Position bleibt offen bis 09:05 Uhr

3. **Filter bleiben aktiv:**
   - Pre-Filter, Gap-Filter etc. funktionieren weiterhin
   - Nur das Risikomanagement wird deaktiviert

### Weitere Änderungen:

#### IsMarketOpen() Funktion ENTFERNT:
- Keine künstlichen Handelszeitenbeschränkungen mehr
- EA funktioniert auf allen Börsen/Brokern
- Market closed Fehler werden weiterhin unterdrückt (10018, 132, 4756)

### Code-Änderungen:

#### OnTick() - Zeile 734-739:
```cpp
// Core Strategy: Immer um 09:05 schließen, kein Trailing
if(UseCoreStrategy)
{
    if(ist_naechster_tag && current_minutes >= 9 * 60 + 5)  // 09:05 Uhr
    {
        ClosePosition();
    }
}
```

#### OpenPosition() - Zeile 1024:
```cpp
// Stop-Loss nur setzen wenn nicht Core Strategy
if(!UseCoreStrategy && StopLossPoints > 0 && !IsNightProtectionActive())
{
    sl = ask - StopLossPoints * point;
}
```

#### TrailingStop() - Zeile 1095:
```cpp
// Kein Trailing Stop bei Core Strategy
if(UseCoreStrategy) return;
```

### Version:
- **the_don v1.21** - Core Strategy Implementation
- Kompiliert: 29.08.2025 00:20 Uhr
- Dateigröße: 123768 Bytes

### Verwendung:

**Für Core Strategy:**
- UseCoreStrategy = **true**
- Alle anderen Stop-Loss/Trailing Einstellungen werden ignoriert

**Für erweiterte Strategie:**
- UseCoreStrategy = **false** (Standard)
- Alle Einstellungen funktionieren wie gewohnt

### Vorteile:
- Echte Umsetzung der Originalstrategie
- Flexibler Wechsel zwischen Core und erweiterter Strategie
- Keine künstlichen Beschränkungen
- Funktioniert auf allen Märkten