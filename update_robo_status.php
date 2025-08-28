<?php
/**
 * update_robo_status.php
 * Aktualisiert den RoboForex Partner Status in der Datenbank
 * Wird vom EA (don_gpt.mq5) aufgerufen
 */

// Error reporting für Debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Database Configuration
// Use localhost instead of IP (must run on same server)
$db_host = 'localhost';
$db_user = 'prophelper';
$db_pass = '.Propt333doka?';
$db_name = 'prophelper';

// Response header
header('Content-Type: text/plain');

// Get Parameters (unterstützt GET und POST)
$account = isset($_REQUEST['account']) ? trim($_REQUEST['account']) : '';
$robo_status = isset($_REQUEST['robo_status']) ? trim($_REQUEST['robo_status']) : 'no';
$program = isset($_REQUEST['program']) ? trim($_REQUEST['program']) : '';
$api_key = isset($_REQUEST['api_key']) ? trim($_REQUEST['api_key']) : '';

// Log incoming request
$log_entry = date('Y-m-d H:i:s') . " - Account: $account, Status: $robo_status, Program: $program\n";
file_put_contents('robo_updates.log', $log_entry, FILE_APPEND);

// Validate account number
if(empty($account)) {
    die('error: no account number provided');
}

// Validate API Key
$expected_key = 'ec4d40c4343ee741';
if(!empty($api_key) && $api_key != $expected_key) {
    die('error: invalid api key');
}

// Validate robo_status
if(!in_array($robo_status, ['yes', 'no', '1', '0'])) {
    $robo_status = 'no';
}

// Normalize status
if($robo_status == '1') $robo_status = 'yes';
if($robo_status == '0') $robo_status = 'no';

try {
    // Connect to database
    $conn = new mysqli($db_host, $db_user, $db_pass, $db_name);
    
    if($conn->connect_error) {
        throw new Exception('Database connection failed: ' . $conn->connect_error);
    }
    
    // Set charset
    $conn->set_charset("utf8");
    
    // First check if account exists
    $check_sql = "SELECT id, accountLogin, account, program, roboaffiliate 
                  FROM lnative 
                  WHERE accountLogin = ? OR account = ?";
    
    $check_stmt = $conn->prepare($check_sql);
    $check_stmt->bind_param("ss", $account, $account);
    $check_stmt->execute();
    $result = $check_stmt->get_result();
    
    if($result->num_rows == 0) {
        $check_stmt->close();
        $conn->close();
        die('error: account ' . $account . ' not found in database');
    }
    
    $row = $result->fetch_assoc();
    $current_status = $row['roboaffiliate'];
    $check_stmt->close();
    
    // Update roboaffiliate status
    if($program) {
        // Update nur für spezifisches Programm
        $update_sql = "UPDATE lnative 
                      SET roboaffiliate = ?, last_robo_check = NOW() 
                      WHERE (accountLogin = ? OR account = ?) 
                      AND program = ?";
        $update_stmt = $conn->prepare($update_sql);
        $update_stmt->bind_param("ssss", $robo_status, $account, $account, $program);
    } else {
        // Update für alle Einträge mit diesem Account
        $update_sql = "UPDATE lnative 
                      SET roboaffiliate = ?, last_robo_check = NOW() 
                      WHERE accountLogin = ? OR account = ?";
        $update_stmt = $conn->prepare($update_sql);
        $update_stmt->bind_param("sss", $robo_status, $account, $account);
    }
    
    if($update_stmt->execute()) {
        $affected = $update_stmt->affected_rows;
        
        if($affected > 0) {
            echo "success: updated $affected rows (status changed from '$current_status' to '$robo_status')";
            
            // Log successful update
            $log_entry = date('Y-m-d H:i:s') . " - SUCCESS: Account $account updated to $robo_status\n";
            file_put_contents('robo_updates.log', $log_entry, FILE_APPEND);
        } else {
            if($current_status == $robo_status) {
                echo "success: status unchanged (already '$robo_status')";
            } else {
                echo "success: no rows updated";
            }
        }
    } else {
        throw new Exception('Update query failed: ' . $update_stmt->error);
    }
    
    $update_stmt->close();
    $conn->close();
    
} catch(Exception $e) {
    // Log error
    $error_log = date('Y-m-d H:i:s') . " - ERROR: " . $e->getMessage() . "\n";
    file_put_contents('robo_errors.log', $error_log, FILE_APPEND);
    
    echo 'error: ' . $e->getMessage();
}

// Optional: Cleanup old log entries (älter als 30 Tage)
$log_file = 'robo_updates.log';
if(file_exists($log_file) && filesize($log_file) > 1048576) { // > 1MB
    $lines = file($log_file);
    $recent_lines = array_slice($lines, -1000); // Behalte nur die letzten 1000 Zeilen
    file_put_contents($log_file, implode('', $recent_lines));
}
?>