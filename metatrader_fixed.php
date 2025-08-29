<?php
// FIXED VERSION - Integration Code für metatrader.php
// Fügt Testzeitraum-Check OHNE redundante Prüfung ein
// 
// Dieser Code wird nach Zeile 99 (//--) eingefügt

// === TESTZEITRAUM-MANAGEMENT START ===
// Include Test Period Management
if (file_exists("test_period_check.inc.php")) {
    require_once "test_period_check.inc.php";
    
    // Testzeitraum-Prüfung mit korrekten Prioritäten:
    // 1. RoboForex Affiliate → immer OK
    // 2. Server-Lizenz → immer OK  
    // 3. Testzeitraum → nur wenn keine anderen Lizenzen
    
    $test_period_result = checkTestPeriod(
        $db,           // Database connection
        $req2,         // ACCOUNT_NAME
        $req4,         // MQL PROGRAM NAME
        $req6,         // Version
        $req1,         // ACCOUNT_LOGIN
        $req5,         // ACCOUNT_TRADE_MODE (Demo/Real)
        $req13         // ACCOUNT_SERVER
    );
    
    // Debug-Logging (optional - kann später entfernt werden)
    if (file_exists('debug_test_period.txt')) {
        $debug_msg = date('Y-m-d H:i:s') . " | Acc:$req1 | Name:$req2 | Prog:$req4 v$req6 | " . 
                     "Status:" . $test_period_result['status'] . " | Type:" . $test_period_result['type'] . "\n";
        file_put_contents('debug_test_period.txt', $debug_msg, FILE_APPEND);
    }
    
    // Verarbeite Ergebnis
    if ($test_period_result["status"] == "OK") {
        // Lizenz gefunden (Affiliate, Server-Lizenz oder neuer Testzeitraum)
        if ($test_period_result["type"] == "TEST_PERIOD") {
            // Neuer Testzeitraum aktiviert - setze Periode wenn nicht gesetzt
            if (!isset($period) || $period == 0) {
                $period = $test_period_result["days"];
            }
        }
        // Bei AFFILIATE oder LICENSE einfach weitermachen
        // Die normale Lizenz-Logik übernimmt
        
    } else if ($test_period_result["status"] == "USED") {
        // WICHTIG: Testzeitraum wurde bereits genutzt
        // Die checkTestPeriod Funktion hat BEREITS geprüft:
        // - RoboForex Status
        // - Server-Lizenz
        // Wenn sie trotzdem USED zurückgibt, gibt es KEINE andere Berechtigung!
        
        // KEINE redundante Prüfung hier! Die Funktion hat bereits alles geprüft.
        $error_msg = "TESTZEITRAUM ABGELAUFEN für " . $req2 . " | WICHTIG: Der kostenlose Testzeitraum kann nur EINMAL pro Account-Name in Anspruch genommen werden. Optionen: 1) RoboForex Partner werden unter forexsignale.trade/broker (Code: qnyj) für unbegrenzte Nutzung 2) Server-Lizenz erwerben unter " . $URLBUY;
        exit(StringEncrypt("::" . $error_msg . "|end", $criptkey));
    }
    // Bei anderen Status (SKIP, ERROR) einfach weitermachen
}
// === TESTZEITRAUM-MANAGEMENT ENDE ===
?>