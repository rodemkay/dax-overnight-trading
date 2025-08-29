<?php
// MODIFIKATION: Testzeitraum-Check Integration
// Diese Zeilen müssen nach Zeile 99 (nach DB-Check) eingefügt werden:

// Include Test Period Management
require_once 'test_period_check.inc.php';

// Nach der Datenbank-Verbindung und Variablen-Extraktion (nach Zeile 99):
// Füge diese Logik ein:

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

// Debug-Logging (optional)
if (file_exists('debug_test_period.log')) {
    $debug_msg = date('Y-m-d H:i:s') . " | $req1 | $req2 | $req4 v$req6 | " . 
                 $test_period_result['status'] . " | " . 
                 $test_period_result['type'] . "\n";
    file_put_contents('debug_test_period.log', $debug_msg, FILE_APPEND);
}

// Verarbeite Testzeitraum-Ergebnis
if ($test_period_result['status'] == 'OK') {
    // Testzeitraum aktiv oder andere Lizenz gefunden
    $test_period_days = $test_period_result['days'];
    $test_period_type = $test_period_result['type'];
    
    // Setze Periode auf Testzeitraum-Tage wenn TEST_PERIOD
    if ($test_period_type == 'TEST_PERIOD' && !isset($period)) {
        $period = $test_period_days;
    }
    
} else if ($test_period_result['status'] == 'USED') {
    // Testzeitraum bereits genutzt
    // WICHTIG: Diese Nachricht muss an den EA zurückgegeben werden
    // Das Format muss mit dem erwarteten Format übereinstimmen
    
    // Prüfe ob andere Lizenz vorhanden ist
    $check_license = mysqli_query($db, 
        "SELECT * FROM lnative 
         WHERE acc='$req1' 
         AND program='$req4' 
         AND (expiry IS NULL OR expiry > NOW()) 
         LIMIT 1"
    );
    
    if (mysqli_num_rows($check_license) == 0) {
        // Keine andere Lizenz vorhanden - verweigere Zugang
        $error_msg = "Test period already used for: " . $req2;
        exit(StringEncrypt("::$error_msg|end", $criptkey));
    }
}

// Der Rest des Original-Codes bleibt unverändert...

?>