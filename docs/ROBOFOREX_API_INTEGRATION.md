# RoboForex Partner API Integration

## Übersicht
Der DAX Overnight EA nutzt jetzt die RoboForex Partner Web API, um zu verifizieren, ob ein Trading-Konto tatsächlich über den Affiliate-Code "qnyj" registriert wurde.

## API-Konfiguration

### 1. API-Key erhalten
- Sende ein Ticket an die RoboForex Partnership Department
- Fordere einen API-Key für dein Partner-Konto an

### 2. EA Konfiguration
Neue Input-Parameter im EA:
- **RoboForexPartnerAccount**: Deine Partner-Kontonummer
- **RoboForexAPIKey**: Dein persönlicher API-Key

### 3. MetaTrader 5 WebRequest Einstellungen
**WICHTIG**: Füge folgende URL zu den erlaubten URLs in MT5 hinzu:
1. Extras → Optionen → Expert Advisors
2. Haken bei "WebRequest für aufgelistete URLs erlauben"
3. URL hinzufügen: `https://my.roboforex.com`

## Funktionsweise

### API-Endpunkt
Der EA nutzt den Tree-API-Endpunkt:
```
https://my.roboforex.com/api/partners/tree?account_id=[partner_account]&api_key=[api_key]&referral_account_id=[client_account]
```

### Verifizierungsprozess
1. **Mit API-Credentials**: 
   - Prüft ob das Konto im Partner-Tree des qnyj-Partners ist
   - Authentische Verifizierung über RoboForex Server

2. **Ohne API-Credentials (Fallback)**:
   - Prüft ob "qnyj" im Account-Namen enthalten ist
   - Erkennt bekannte Test-Konten (z.B. 77022300)

### XML Response Format
Erfolgreiche Antwort wenn Konto im Partner-Tree:
```xml
<partner>
  <id>77022300</id>
  <path>partner_account/.../77022300</path>
</partner>
```

## Implementierung

### CheckAccountInPartnerTree()
- Sendet HTTP GET Request an RoboForex API
- Parst XML Response
- Prüft ob Konto im Partner-Tree vorhanden ist

### CheckRoboForexAffiliate()
- Versucht zuerst API-Verifizierung
- Fällt auf alternative Methoden zurück wenn API nicht verfügbar
- Speichert erfolgreiche Verifizierung permanent

## Fehlerbehebung

### Error 4060
- URL nicht in MT5 erlaubt → Füge URL zu WebRequest-Liste hinzu

### Keine API Response
- Prüfe Internet-Verbindung
- Verifiziere API-Key und Partner-Account
- Stelle sicher dass Account bei RoboForex aktiv ist

## Sicherheit
- API-Key niemals öffentlich teilen
- Credentials nur in persönlichen EA-Einstellungen speichern
- Bei Kompromittierung neuen API-Key anfordern