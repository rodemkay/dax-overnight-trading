<?php
/**
 * Test Period Management System
 * Erweiterung für check.php zur Verwaltung von Testzeiträumen
 * 
 * Diese Funktionen sollen in check.php integriert werden
 */

// Datenbank-Konfiguration (bereits in check.php vorhanden)
// $mysqli = new mysqli($db_host, $db_user, $db_pass, $db_name);

/**
 * Prüft ob ein Testzeitraum bereits genutzt wurde
 * 
 * @param mysqli $mysqli Database connection
 * @param string $account_name Name aus MT5 Account
 * @param string $program_name EA Name (the_don, breakout_brain, etc.)
 * @param string $program_version Version (1.24, 1.25, etc.)
 * @return array Status und Details
 */
function checkTestPeriod($mysqli, $account_name, $program_name, $program_version) {
    
    // Sanitize inputs
    $account_name = $mysqli->real_escape_string($account_name);
    $program_name = $mysqli->real_escape_string($program_name);
    $program_version = $mysqli->real_escape_string($program_version);
    
    // Prüfe ob Testzeitraum bereits genutzt wurde
    $query = "SELECT * FROM test_period_history 
              WHERE account_name = ? 
              AND program_name = ? 
              AND program_version = ?";
    
    $stmt = $mysqli->prepare($query);
    $stmt->bind_param("sss", $account_name, $program_name, $program_version);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows > 0) {
        // Testzeitraum bereits genutzt
        $row = $result->fetch_assoc();
        return [
            'status' => 'USED',
            'message' => 'Testzeitraum bereits genutzt',
            'first_test_date' => $row['first_test_date'],
            'test_count' => $row['test_count']
        ];
    }
    
    // Testzeitraum noch nicht genutzt - kann aktiviert werden
    return [
        'status' => 'AVAILABLE',
        'message' => 'Testzeitraum verfügbar'
    ];
}

/**
 * Registriert einen neuen Testzeitraum
 * 
 * @param mysqli $mysqli Database connection
 * @param string $account_name Name aus MT5 Account
 * @param string $program_name EA Name
 * @param string $program_version Version
 * @param string $account_type DEMO oder LIVE
 * @param string $account_number MT5 Kontonummer (optional)
 * @param string $server_name MT5 Server (optional)
 * @return bool Success status
 */
function registerTestPeriod($mysqli, $account_name, $program_name, $program_version, 
                           $account_type = null, $account_number = null, $server_name = null) {
    
    $query = "INSERT INTO test_period_history 
              (account_name, program_name, program_version, first_test_date, 
               account_type, account_number, server_name)
              VALUES (?, ?, ?, NOW(), ?, ?, ?)
              ON DUPLICATE KEY UPDATE 
              test_count = test_count + 1,
              updated_at = CURRENT_TIMESTAMP";
    
    $stmt = $mysqli->prepare($query);
    $stmt->bind_param("ssssss", $account_name, $program_name, $program_version, 
                      $account_type, $account_number, $server_name);
    
    return $stmt->execute();
}

/**
 * Hauptlogik für Lizenzprüfung mit Testzeitraum-Management
 * Diese Funktion ersetzt/erweitert die bestehende Check-Logik
 * 
 * @param array $request_data Daten vom EA
 * @return array Response für EA
 */
function processLicenseCheck($mysqli, $request_data) {
    
    // Extrahiere Daten aus Request
    $account_number = $request_data['acc'] ?? '';
    $account_name = $request_data['name'] ?? '';
    $program_name = $request_data['program'] ?? '';
    $program_version = $request_data['version'] ?? '';
    $account_type = $request_data['type'] ?? 'UNKNOWN'; // DEMO oder LIVE
    $server_name = $request_data['server'] ?? '';
    
    // PRIORITÄT 1: Prüfe RoboForex Affiliate Status
    // (Diese Prüfung sollte aus der bestehenden check.php übernommen werden)
    $roboaffiliate_query = "SELECT roboaffiliate FROM lnative WHERE acc = ?";
    $stmt = $mysqli->prepare($roboaffiliate_query);
    $stmt->bind_param("s", $account_number);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if ($row['roboaffiliate'] == 1) {
            // RoboForex Affiliate - unbegrenzter Zugang
            return [
                'status' => 'OK',
                'type' => 'AFFILIATE',
                'message' => 'RoboForex Affiliate Account',
                'days' => 9999  // Praktisch unbegrenzt
            ];
        }
    }
    
    // PRIORITÄT 2: Prüfe Server-Lizenz
    // (Diese Prüfung sollte aus der bestehenden check.php übernommen werden)
    $license_query = "SELECT * FROM lnative 
                     WHERE acc = ? 
                     AND program = ? 
                     AND active = 1 
                     AND (expiry_date IS NULL OR expiry_date > NOW())";
    
    $stmt = $mysqli->prepare($license_query);
    $stmt->bind_param("ss", $account_number, $program_name);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows > 0) {
        // Server-Lizenz aktiv
        return [
            'status' => 'OK',
            'type' => 'LICENSE',
            'message' => 'Server License Active',
            'days' => 9999  // Abhängig von expiry_date
        ];
    }
    
    // PRIORITÄT 3: Prüfe Testzeitraum
    if (!empty($account_name) && !empty($program_name) && !empty($program_version)) {
        
        $test_period = checkTestPeriod($mysqli, $account_name, $program_name, $program_version);
        
        if ($test_period['status'] == 'AVAILABLE') {
            // Testzeitraum verfügbar - registrieren und aktivieren
            registerTestPeriod($mysqli, $account_name, $program_name, $program_version,
                             $account_type, $account_number, $server_name);
            
            // Hole Testzeitraum-Tage aus Konfiguration (Standard: 14 Tage)
            // Diese Werte könnten aus einer config-Tabelle kommen
            $test_days = 14;  // TODO: Aus Dashboard-Konfiguration holen
            
            return [
                'status' => 'OK',
                'type' => 'TEST_PERIOD',
                'message' => 'Test period activated',
                'days' => $test_days
            ];
            
        } else if ($test_period['status'] == 'USED') {
            // Testzeitraum bereits genutzt
            return [
                'status' => 'ERROR',
                'type' => 'TEST_PERIOD_USED',
                'message' => 'Testzeitraum bereits genutzt für ' . $account_name,
                'first_used' => $test_period['first_test_date']
            ];
        }
    }
    
    // Keine Lizenz gefunden
    return [
        'status' => 'ERROR',
        'type' => 'NO_LICENSE',
        'message' => 'Keine gültige Lizenz gefunden'
    ];
}

/**
 * Beispiel-Integration in bestehende check.php
 * 
 * Die check.php sollte etwa so angepasst werden:
 */

// In check.php würde die Integration so aussehen:
/*
// Empfange Daten vom EA
$request_data = [
    'acc' => $_POST['acc'] ?? $_GET['acc'] ?? '',
    'name' => $_POST['name'] ?? $_GET['name'] ?? '',
    'program' => $_POST['program'] ?? $_GET['program'] ?? '',
    'version' => $_POST['version'] ?? $_GET['version'] ?? '',
    'type' => $_POST['type'] ?? $_GET['type'] ?? '',
    'server' => $_POST['server'] ?? $_GET['server'] ?? ''
];

// Verarbeite Lizenz-Check mit Testzeitraum-Logik
$response = processLicenseCheck($mysqli, $request_data);

// Sende Antwort an EA
if ($response['status'] == 'OK') {
    // Format für EA: OK|DAYS|MESSAGE
    echo "OK|" . $response['days'] . "|" . $response['message'];
} else {
    // Format für EA: ERROR|0|MESSAGE
    echo "ERROR|0|" . $response['message'];
}
*/

// Zusätzliche Admin-Funktionen für Dashboard:

/**
 * Zeigt alle Testzeiträume eines Accounts
 */
function getTestPeriodsForAccount($mysqli, $account_name) {
    $query = "SELECT * FROM test_period_history 
              WHERE account_name = ? 
              ORDER BY first_test_date DESC";
    
    $stmt = $mysqli->prepare($query);
    $stmt->bind_param("s", $account_name);
    $stmt->execute();
    
    return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
}

/**
 * Löscht Testzeitraum-Historie (Admin-Funktion)
 */
function resetTestPeriod($mysqli, $account_name, $program_name, $program_version) {
    $query = "DELETE FROM test_period_history 
              WHERE account_name = ? 
              AND program_name = ? 
              AND program_version = ?";
    
    $stmt = $mysqli->prepare($query);
    $stmt->bind_param("sss", $account_name, $program_name, $program_version);
    
    return $stmt->execute();
}

/**
 * Statistik: Testzeiträume pro EA/Version
 */
function getTestPeriodStatistics($mysqli) {
    $query = "SELECT program_name, program_version, 
                     COUNT(*) as total_tests,
                     COUNT(DISTINCT account_name) as unique_users,
                     MIN(first_test_date) as first_test,
                     MAX(first_test_date) as last_test
              FROM test_period_history
              GROUP BY program_name, program_version
              ORDER BY total_tests DESC";
    
    $result = $mysqli->query($query);
    return $result->fetch_all(MYSQLI_ASSOC);
}

?>