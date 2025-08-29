# Server-Lizenz Ablaufdatum Fix - the_don v1.13

## ✅ Implementiert am 28.08.2025

### Was wurde gefixt:
1. **_ansTime Variable** aus MQL_License.mqh wird jetzt korrekt ausgelesen
2. **Server-Lizenz Ablaufdatum** zeigt echte Restlaufzeit vom Server
3. **Keine hardcodierten Werte** mehr - alles kommt vom Server

### Technische Änderungen:

#### 1. Externe Variable deklariert (Zeile 33):
```cpp
// Externe Variable aus MQL_License.mqh für Lizenz-Ablaufdatum
extern string _ansTime;  // Format: "YYYY.MM.DD" vom Server
```

#### 2. Server-Datum bei Aktivierung lesen (Zeile 630-648):
```cpp
if(Activation())
{
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
```

#### 3. Bei periodischer Prüfung aktualisieren (Zeile 664-673):
```cpp
// Server-Lizenz bleibt aktiv
serverLicenseStatus = "✓ Server-Lizenz aktiv";

// Lizenz-Ablaufdatum aktualisieren
if(StringLen(_ansTime) == 10)
{
    serverLicenseExpiry = StringToTime(_ansTime);
}
```

### Wie es funktioniert:

1. **MQL_License.mqh** macht Server-Request und füllt `_ansTime` Variable
2. **_ansTime** enthält Ablaufdatum im Format "YYYY.MM.DD" (z.B. "2025.09.30")
3. **the_don.mq5** liest diese Variable und zeigt verbleibende Tage im Chart
4. Bei jeder Server-Prüfung wird das Datum aktualisiert

### Chart-Anzeige:
- **Grün (Lime):** Mehr als 30 Tage verbleibend
- **Hellgrün:** 7-30 Tage verbleibend  
- **Gelb:** Weniger als 7 Tage verbleibend
- **Rot:** Lizenz abgelaufen

### Version:
- **the_don v1.13** - Server-Lizenz Ablaufdatum Fix
- Kompiliert: 28.08.2025 18:14 Uhr
- Dateigröße: 116754 Bytes

### Wichtig:
- Die angezeigte Restlaufzeit kommt DIREKT vom Lizenz-Server
- Keine hardcodierten Daten mehr
- Automatische Aktualisierung bei jeder Server-Prüfung