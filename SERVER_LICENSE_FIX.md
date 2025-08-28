# Server-Lizenz Fix Documentation

## Problem gelöst:
1. **Hartcodiertes Datum entfernt** (war: 17.08.2025)
2. **MQL_License.mqh** in Don Ordner kopiert für lokalen Include

## Wie die Server-Lizenz funktioniert:

### Validierung durch Server:
```cpp
if(Activation())  // Diese Funktion fragt den Server!
{
    serverActivated = true;
    serverLicenseStatus = "✓ Server-Lizenz aktiv";
}
```

### Die `Activation()` Funktion:
- Kommt aus MQL_License.mqh
- Sendet Request an lic.prophelper.org
- Prüft Account-Nummer gegen Server-Datenbank
- Gibt `true` zurück NUR wenn Server die Lizenz bestätigt
- Gibt `false` zurück wenn keine gültige Lizenz

### Status-Anzeige:
- **"✓ Server-Lizenz aktiv"** → Server hat bestätigt
- **"✗ Nicht aktiviert"** → Server hat abgelehnt
- **"Prüfung läuft..."** → Warte auf Server-Antwort

## Wichtig:
- Die Lizenz ist NUR aktiv wenn `Activation()` true zurückgibt
- Der Server entscheidet über die Gültigkeit
- Keine hardcodierten Werte mehr!
- Status wird alle X Sekunden neu geprüft (Check-Period)

## Kompilierung:
1. MQL_License.mqh muss im Include Ordner ODER im EA Ordner sein
2. Jetzt liegt eine Kopie in: `/MQL5/Experts/Don/MQL_License.mqh`
3. Include geändert zu: `#include "MQL_License.mqh"` (lokal)

## Version:
- **the_don v1.11** - Server-Lizenz Fix implementiert