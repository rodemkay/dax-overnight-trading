# Vollständige Analyse des Lizenzsystems

## Wie das System funktioniert:

### 1. Konfiguration (Datei: `names`)
```
daxovernight~1.00~Full~10~30~50~1~~
```
- **10** = Neue Registrierungen für 10 Tage
- **30** = Max. 30 verschiedene Hardware-IDs (UUID)
- **50** = Max. 50 verschiedene Accounts
- **1** = Check-Intervall (Stunden)

### 2. Der kritische Code (metatrader.php, Zeile 176-181)
```php
if($Account_exists) {
   if($_serialNo!=$req16) {
      echo StringEncrypt("::The number of activations has ended: 1|end",$criptkey);
      mysqli_close($db);
      exit;
   }
}
```

## Das Problem:
Wenn ein Account bereits in der Datenbank existiert, wird geprüft ob die Hardware-ID (`serialNo`) identisch ist. Wenn nicht → "The number of activations has ended: 1"

## LÖSUNGEN:

### Lösung 1: Code in metatrader.php ändern
Kommentieren Sie Zeile 177-181 aus:
```php
// if($_serialNo!=$req16) {
//    echo StringEncrypt("::The number of activations has ended: 1|end",$criptkey);
//    mysqli_close($db);
//    exit;
// }
```

### Lösung 2: Datei names anpassen
Erhöhen Sie die Limits:
```
daxovernight~1.00~Full~10~9999~9999~1~~
```
Dies erlaubt 9999 verschiedene Hardware-IDs und Accounts.

### Lösung 3: Datenbank-Eintrag anpassen
```sql
-- SerialNo für alle daxovernight Einträge löschen
UPDATE lnative SET serialNo = '' WHERE program = 'daxovernight';
```

### Lösung 4: Hardware-ID Check komplett entfernen
In metatrader.php, ersetzen Sie Zeile 177-181 durch:
```php
// Hardware-ID Check deaktiviert für unbegrenzte Installationen
```

## Zusätzliche Prüfungen im Code:

1. **UUID-Limit** (Zeile 185-190): Prüft ob mehr als 30 verschiedene Hardware-IDs verwendet wurden
2. **Blockierungsliste** (Zeile 112): Datei `blocking/daxovernight.csv` kann Hardware-IDs blockieren
3. **Lizenzablauf** (Zeile 213): Prüft ob `deactivate_date` noch gültig ist

## Empfehlung:
Die einfachste Lösung ist, die Hardware-ID-Prüfung in Zeile 177-181 zu deaktivieren. Dies erlaubt unbegrenzte Installationen solange die Lizenz zeitlich gültig ist.