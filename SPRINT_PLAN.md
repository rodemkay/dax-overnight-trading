# 📋 SPRINT PLAN - DAX Overnight EA Entwicklung

## 🎯 Sprint-Ziele
Umbenennung des EA von `don_gpt` zu `der_don` und Implementierung neuer Trading-Features mit Code-Optimierungen.

---

## 📅 PHASE 1: EA-UMBENENNUNG (Tag 1)
**Status:** In Bearbeitung

### ✅ Erledigte Tasks:
- [x] Symlinks im Arbeitsverzeichnis erstellt
- [x] CLAUDE.md aktualisiert mit Pfadstruktur

### 🔄 Aktuelle Tasks:
- [ ] Backup von don_gpt.mq5 erstellen
- [ ] der_don.mq5 mit folgenden Änderungen:
  - PROGRAM_NAME: "der_don"
  - Version: "1.00"
  - LICENSE_CODE: "DERDON"
  - Link: "www.forexsignale.trade/dax_over_night"

### 📝 Backend-Registrierung:
- [ ] Produkt "der_don" in lic.prophelper.org/office anlegen
- [ ] Version: 1.00
- [ ] Check-Period: 1 Stunde
- [ ] Trial: 7 Tage

---

## ⚡ PHASE 2: CODE-OPTIMIERUNG (Tag 1-2)
**Status:** Geplant

### Performance-Optimierungen:
- [ ] Lizenzprüfungen im Backtest komplett entfernen
- [ ] "Serverlizenzprüfung alle X Minuten" Meldung entfernen
- [ ] Check-Period System beibehalten (Backend-gesteuert)
- [ ] Indikator-Handle-Verwaltung optimieren

### Demo-Account-Tracking:
- [ ] Account-Name Duplikat-Check implementieren
- [ ] Über vorhandenes Lizenz-System (Backend: 7 Tage Trial)
- [ ] Gleicher Name = keine neue Demo-Zeit

---

## 📊 PHASE 3: NEUE TRADING-FEATURES (Tag 2-4)
**Status:** Geplant

### 3.1 Gap-Filter (SICHTBAR)
```cpp
input group "════════ GAP FILTER ════════"
input bool    enableGapFilter = false;              // Gap-Filter aktivieren
input double  maxDailyGapPercent = 2.0;            // Max. Tagessteigerung in %
```
- [ ] Prüfung nur 5 Sekunden vor Kauf
- [ ] Berechnung: (Open_heute - Close_gestern) / Close_gestern * 100
- [ ] Chart-Anzeige bei aktivem Filter

### 3.2 Nacht-Trading-Schutz (SICHTBAR)
```cpp
input group "════════ NACHT-SCHUTZ ════════"
input bool    enableNightProtection = false;        // Nacht-Schutz aktivieren
input int     nightProtectionStartHour = 18;        // Start (Stunde)
input int     nightProtectionEndHour = 9;           // Ende (Stunde)
```
- [ ] Kein Stop-Loss zwischen Start und Ende
- [ ] RoboForex-Simulation (kein Verkauf möglich)

### 3.3 RSI-Filter (SICHTBAR)
```cpp
input group "════════ RSI FILTER ════════"
input bool    enableRSIFilter = false;              // RSI Filter aktivieren
input int     rsiPeriod = 14;                       // RSI Periode
input double  rsiOversold = 30.0;                   // Überverkauft Level
input double  rsiOverbought = 70.0;                 // Überkauft Level
```
- [ ] Standard RSI-Indikator implementieren
- [ ] Integration in OpenPosition() Logik

### 3.4 ADX-Filter (SICHTBAR)
```cpp
input group "════════ ADX FILTER ════════"
input bool    enableADXFilter = false;              // ADX Filter aktivieren
input int     adxPeriod = 14;                       // ADX Periode
input double  minADXValue = 25.0;                   // Minimum ADX Wert
```
- [ ] Trend-Stärke Prüfung
- [ ] Nur bei starkem Trend einsteigen

### 3.5 MACD-Filter (SICHTBAR)
```cpp
input group "════════ MACD FILTER ════════"
input bool    enableMACDFilter = false;             // MACD Filter aktivieren
input int     macdFastEMA = 12;                     // Fast EMA
input int     macdSlowEMA = 26;                     // Slow EMA
input int     macdSignalSMA = 9;                    // Signal SMA
```
- [ ] MACD-Signal Crossover prüfen
- [ ] Momentum-Bestätigung

---

## 🔒 PHASE 4: INDIKATOR-VERSTECKEN (Später)
**Status:** Zurückgestellt

### Nach erfolgreichem Test:
- [ ] StochRSI als versteckte const Variable
- [ ] ATR-Filter als versteckte const Variable
- [ ] Alle Log/Print-Ausgaben für versteckte Indikatoren entfernen
- [ ] Leicht deaktivierbar für interne Tests

---

## 🧪 PHASE 5: TESTS & VALIDIERUNG
**Status:** Geplant

### Kompilierung:
- [ ] MetaEditor64.exe auf Windows-Mount nutzen
- [ ] Alternative: Wine-Installation verwenden
- [ ] der_don.ex5 erfolgreich erstellt?

### Funktionstests:
- [ ] Lizenz-Check funktioniert?
- [ ] Backend erkennt der_don?
- [ ] Alle neuen Features testbar?
- [ ] Backtest-Performance verbessert?

### Integration:
- [ ] RoboForex Affiliate-Check weiterhin funktional
- [ ] Demo-Account-Limitierung aktiv
- [ ] Check-Period vom Backend übernommen

---

## 📈 Erfolgskriterien

### Sprint 1 (EA-Umbenennung):
- ✅ der_don.mq5 erstellt und kompiliert
- ✅ Backend-Registrierung abgeschlossen
- ✅ Lizenz-System funktioniert

### Sprint 2 (Optimierung):
- ✅ Backtest 50-70% schneller
- ✅ Keine nervigen Log-Meldungen
- ✅ Demo-Tracking funktioniert

### Sprint 3 (Features):
- ✅ Alle Filter implementiert und testbar
- ✅ Default-Werte = false (keine Änderung für User)
- ✅ Saubere Integration in bestehenden Code

---

## 🚀 Nächste Schritte
1. **JETZT:** Backup erstellen und der_don.mq5 anlegen
2. **HEUTE:** Backend-Registrierung und erste Tests
3. **MORGEN:** Code-Optimierungen beginnen
4. **TAG 3-4:** Neue Features implementieren

---

## 📝 Notizen
- Windows-Mount nutzen für direkte Kompilierung
- Check-Period wird vom Backend gesteuert (nicht hardcoded!)
- Alle neuen Features sind SICHTBAR (nicht versteckt)
- StochRSI und ATR erst SPÄTER verstecken (nach Tests)