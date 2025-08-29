<?php
/**
 * Test Period Management Include
 * Wird in metatrader.php eingebunden für Testzeitraum-Verwaltung
 */

/**
 * Prüft und verwaltet Testzeiträume
 * 
 * @param mysqli $db Database connection
 * @param string $account_name Name aus MT5 Account ($req2)
 * @param string $program_name EA Name ($req4)
 * @param string $program_version Version ($req6)
 * @param string $account_number Account Login ($req1)
 * @param string $account_type Demo/Real ($req5)
 * @param string $server_name Server ($req13)
 * @return array Status information
 */
function checkTestPeriod($db, $account_name, $program_name, $program_version, 
                         $account_number = null, $account_type = null, $server_name = null) {
    
    // Sanitize inputs
    $account_name = mysqli_real_escape_string($db, trim($account_name));
    $program_name = mysqli_real_escape_string($db, trim($program_name));
    $program_version = mysqli_real_escape_string($db, trim($program_version));
    
    // Leere Namen ignorieren
    if (empty($account_name) || $account_name == 'NULL' || $account_name == '') {
        return ['status' => 'SKIP', 'message' => 'No account name provided'];
    }
    
    // PRIORITÄT 1: Prüfe RoboForex Affiliate Status
    if (!empty($account_number)) {
        $robo_query = "SELECT roboaffiliate FROM lnative WHERE account = ? LIMIT 1";
        if ($stmt = mysqli_prepare($db, $robo_query)) {
            mysqli_stmt_bind_param($stmt, "s", $account_number);
            mysqli_stmt_execute($stmt);
            $result = mysqli_stmt_get_result($stmt);
            
            if ($row = mysqli_fetch_assoc($result)) {
                if ($row['roboaffiliate'] == 1) {
                    mysqli_stmt_close($stmt);
                    return [
                        'status' => 'OK',
                        'type' => 'AFFILIATE',
                        'days' => 9999,
                        'message' => 'RoboForex Affiliate Account'
                    ];
                }
            }
            mysqli_stmt_close($stmt);
        }
    }
    
    // PRIORITÄT 2: Prüfe Server-Lizenz
    if (!empty($account_number) && !empty($program_name)) {
        // Original verwendet 'account' statt 'acc' für die Spalte
        $license_query = "SELECT * FROM lnative 
                         WHERE account = ? 
                         AND program = ? 
                         AND deactivate_date >= UNIX_TIMESTAMP() 
                         LIMIT 1";
        
        if ($stmt = mysqli_prepare($db, $license_query)) {
            mysqli_stmt_bind_param($stmt, "ss", $account_number, $program_name);
            mysqli_stmt_execute($stmt);
            $result = mysqli_stmt_get_result($stmt);
            
            if (mysqli_num_rows($result) > 0) {
                $row = mysqli_fetch_assoc($result);
                $days_left = ceil(($row['deactivate_date'] - time()) / 86400);
                mysqli_stmt_close($stmt);
                return [
                    'status' => 'OK',
                    'type' => 'LICENSE',
                    'days' => $days_left > 0 ? $days_left : 9999,
                    'message' => 'Server License Active'
                ];
            }
            mysqli_stmt_close($stmt);
        }
    }
    
    // PRIORITÄT 3: Prüfe Testzeitraum
    $check_query = "SELECT * FROM test_period_history 
                   WHERE account_name = ? 
                   AND program_name = ? 
                   AND program_version = ? 
                   LIMIT 1";
    
    if ($stmt = mysqli_prepare($db, $check_query)) {
        mysqli_stmt_bind_param($stmt, "sss", $account_name, $program_name, $program_version);
        mysqli_stmt_execute($stmt);
        $result = mysqli_stmt_get_result($stmt);
        
        if (mysqli_num_rows($result) > 0) {
            // Testzeitraum bereits genutzt
            $row = mysqli_fetch_assoc($result);
            mysqli_stmt_close($stmt);
            
            return [
                'status' => 'USED',
                'type' => 'TEST_PERIOD_USED',
                'days' => 0,
                'message' => 'Test period already used',
                'first_test_date' => $row['first_test_date'],
                'test_count' => $row['test_count']
            ];
        }
        mysqli_stmt_close($stmt);
    }
    
    // Testzeitraum verfügbar - registrieren
    $insert_query = "INSERT INTO test_period_history 
                    (account_name, program_name, program_version, first_test_date, 
                     account_type, account_number, server_name)
                    VALUES (?, ?, ?, NOW(), ?, ?, ?)
                    ON DUPLICATE KEY UPDATE 
                    test_count = test_count + 1,
                    updated_at = CURRENT_TIMESTAMP";
    
    if ($stmt = mysqli_prepare($db, $insert_query)) {
        mysqli_stmt_bind_param($stmt, "ssssss", 
            $account_name, $program_name, $program_version,
            $account_type, $account_number, $server_name
        );
        
        if (mysqli_stmt_execute($stmt)) {
            mysqli_stmt_close($stmt);
            
            // Testzeitraum erfolgreich registriert
            return [
                'status' => 'OK',
                'type' => 'TEST_PERIOD',
                'days' => 14,  // Standard 14 Tage - kann aus Config geladen werden
                'message' => 'Test period activated'
            ];
        }
        mysqli_stmt_close($stmt);
    }
    
    // Fehler beim Registrieren
    return [
        'status' => 'ERROR',
        'type' => 'SYSTEM_ERROR',
        'days' => 0,
        'message' => 'Could not process test period'
    ];
}

/**
 * Loggt Testzeitraum-Aktivitäten
 */
function logTestPeriodActivity($db, $account_name, $program_name, $status, $message) {
    $log_file = 'test_period_log.txt';
    $timestamp = date('Y-m-d H:i:s');
    $log_entry = "[$timestamp] $account_name | $program_name | $status | $message\n";
    file_put_contents($log_file, $log_entry, FILE_APPEND | LOCK_EX);
}

/**
 * Holt Testzeitraum-Tage aus Konfiguration
 */
function getTestPeriodDays($db, $program_name) {
    // Kann später aus einer config-Tabelle geladen werden
    // Für jetzt: Standard 14 Tage
    return 14;
}
?>