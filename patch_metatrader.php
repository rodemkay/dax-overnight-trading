<?php
/**
 * Patch-Script für metatrader.php
 * Fügt Testzeitraum-Management hinzu
 */

// Lade Original-Datei
$original = file_get_contents('metatrader_original.php');

// Finde die Stelle nach Zeile 99 (nach DB-Check)
$insert_position = strpos($original, '//--');

if ($insert_position === false) {
    die("Konnte Insert-Position nicht finden!\n");
}

// Code, der eingefügt werden soll
$insert_code = '
// === TESTZEITRAUM-MANAGEMENT START ===
// Include Test Period Management
if (file_exists("test_period_check.inc.php")) {
    require_once "test_period_check.inc.php";
    
    // Testzeitraum-Prüfung
    $test_period_result = checkTestPeriod(
        $db,           // Database connection
        $req2,         // ACCOUNT_NAME
        $req4,         // MQL PROGRAM NAME
        $req6,         // Version
        $req1,         // ACCOUNT_LOGIN
        $req5,         // ACCOUNT_TRADE_MODE (Demo/Real)
        $req13         // ACCOUNT_SERVER
    );
    
    // Verarbeite Testzeitraum-Ergebnis
    if ($test_period_result["status"] == "OK") {
        // Testzeitraum aktiv oder andere Lizenz gefunden
        if ($test_period_result["type"] == "TEST_PERIOD") {
            // Setze Periode auf Testzeitraum-Tage
            if (!isset($period) || $period == 0) {
                $period = $test_period_result["days"];
            }
        }
    } else if ($test_period_result["status"] == "USED") {
        // Testzeitraum bereits genutzt - prüfe andere Lizenzen
        $check_lic = mysqli_query($db, 
            "SELECT * FROM lnative 
             WHERE acc=\'$req1\' 
             AND program=\'$req4\' 
             AND (expiry IS NULL OR expiry > NOW()) 
             LIMIT 1"
        );
        
        // Auch RoboForex prüfen
        $check_robo = mysqli_query($db, 
            "SELECT roboaffiliate FROM lnative 
             WHERE acc=\'$req1\' 
             LIMIT 1"
        );
        
        $has_robo = false;
        if ($robo_row = mysqli_fetch_assoc($check_robo)) {
            $has_robo = ($robo_row["roboaffiliate"] == 1);
        }
        
        if (mysqli_num_rows($check_lic) == 0 && !$has_robo) {
            // Keine andere Lizenz vorhanden - verweigere Zugang
            $error_msg = "Test period already used for account: " . $req2;
            exit(StringEncrypt("::$error_msg|end", $criptkey));
        }
    }
}
// === TESTZEITRAUM-MANAGEMENT ENDE ===

';

// Füge Code ein
$modified = substr($original, 0, $insert_position) . 
            $insert_code . 
            substr($original, $insert_position);

// Speichere modifizierte Datei
file_put_contents('metatrader_patched.php', $modified);

echo "✅ Patch erfolgreich erstellt!\n";
echo "Datei gespeichert als: metatrader_patched.php\n";

// Zeige die eingefügte Position
echo "\nCode wurde nach Zeile 99 eingefügt (Position: $insert_position)\n";

// Prüfe ob test_period_check.inc.php existiert
if (file_exists('test_period_check.inc.php')) {
    echo "✅ test_period_check.inc.php gefunden\n";
} else {
    echo "⚠️ test_period_check.inc.php nicht gefunden - muss hochgeladen werden!\n";
}

echo "\nNächste Schritte:\n";
echo "1. test_period_check.inc.php auf Server hochladen\n";
echo "2. metatrader_patched.php als metatrader.php auf Server hochladen\n";
echo "3. Original metatrader.php vorher sichern!\n";
?>