# Backend-Registrierung für der_don EA

## 📝 Registrierung in lic.prophelper.org/office

### Schritte zur Registrierung:
1. Login unter https://lic.prophelper.org/office (admin/admin)
2. "Adding products" → "Show" klicken
3. Neues Produkt am Ende der Liste hinzufügen

### Einstellungen für der_don:
```
Program: der_don
Version: 1.00
Account type: Full
Trial version days: 7
Check period: 1 (1 Stunde wie bei don_gpt)
Message: (optional, leer lassen)
```

### Nach der Registrierung:
- "Update" Button klicken
- Produkt erscheint in der Dropdown-Liste
- EA kann nun lizenziert werden

## ✅ Status-Check:
- [ ] Produkt "der_don" angelegt
- [ ] Version 1.00 eingetragen
- [ ] Check-Period auf 1 Stunde gesetzt
- [ ] Trial auf 7 Tage gesetzt
- [ ] Update durchgeführt

## 🔧 Kompilierung:

### Option 1: Direkt auf Windows (WIN11NEU)
- MetaEditor auf Windows öffnen
- der_don.mq5 laden
- F7 drücken oder Compile-Button

### Option 2: Wine auf Linux
```bash
wine /home/rodemkay/.wine-mt5/drive_c/Program\ Files/MetaTrader\ 5/metaeditor64.exe /compile:der_don.mq5
```

### Option 3: Remote Kompilierung
- Auf Windows-System einloggen
- MetaEditor64.exe starten
- Kompilieren

## 📊 Erste Tests:
1. der_don.ex5 wurde erstellt?
2. EA in MT5 laden
3. Lizenz-Check im Journal prüfen
4. Backend-Kommunikation verifizieren