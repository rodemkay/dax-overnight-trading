# Account 77022300 - Datenbankeinträge

## Übersicht
Account 77022300 hat **2 aktive Einträge** in der Datenbank.

## Detaillierte Daten

### Eintrag 1 (ID: 62)
```
Registrierungsdatum:     04.08.2025 23:40
Registrar:              MT5
Firma:                  M Values GmbH
Account:                77022300
Broker:                 RoboForex Ltd
Server:                 RoboForex-ECN
MT Version:             5
Typ:                    Real
Trading:                Trader
Deaktivierungsdatum:    18.08.2025
Balance:                0
Currency:               USD
Connects:               57
Letzter Connect:        1754665273
Programm:               daxovernight
Package:                MAX
Version:                1.00
UUID:                   422b6e96-6e8e-271c-a8ac-00d8611f89a89
Serial:                 3C1671AF
IP:                     185.72.232.173
Referenz:               FS_TRADE
MT Code:                DAXON10~0.0~0.0~7:0.0~8:0.0
```

### Eintrag 2 (ID: 66)
```
Registrierungsdatum:     08.08.2025 19:51
Registrar:              MT5
Firma:                  M Values GmbH
Account:                77022300
Broker:                 RoboForex Ltd
Server:                 RoboForex-ECN
MT Version:             5
Typ:                    Real
Trading:                Trader
Deaktivierungsdatum:    21.08.2025
Balance:                0
Currency:               USD
Connects:               27
Letzter Connect:        1754910874
Programm:               don_gpt
Package:                MAX
Version:                2.00
UUID:                   422b6e96-6e8e-271c-a8ac-00d8611f89a89
Serial:                 3C1671AF
IP:                     185.72.232.151
Referenz:               FS_TRADE
MT Code:                DAXON10~0.0~0.0~7:0.0~8:0.0
```

## Wichtige Beobachtungen

1. **Zwei verschiedene Programme:**
   - Eintrag 1 nutzt `daxovernight` (Version 1.00)
   - Eintrag 2 nutzt `don_gpt` (Version 2.00)

2. **Gleiche Hardware:**
   - Beide Einträge haben die gleiche UUID und Serial Number
   - Dies bedeutet, es ist derselbe Computer/Installation

3. **Verschiedene IPs:**
   - 185.72.232.173 (Eintrag 1)
   - 185.72.232.151 (Eintrag 2)
   - Beide IPs sind aus demselben Subnetz

4. **Aktive Lizenzen:**
   - Beide Einträge haben Package "MAX"
   - Deaktivierung erst im August 2025

## API-Zugriff

Die Daten wurden über die REST API abgerufen:
- **Endpunkt:** https://lic.prophelper.org/api/db_api.php
- **Query:** `SELECT * FROM lnative WHERE account = '77022300'`
- **Token:** 250277100311270613

## Script zum Abrufen

Nutzen Sie `get_account_data.py` um Account-Daten abzurufen:
```bash
python get_account_data.py
```

---
*Stand: 08.11.2025 13:38 Uhr*
