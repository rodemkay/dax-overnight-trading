<?php
/**
 * Update RoboForex Status in Database
 * This script updates OR INSERTS the roboaffiliate status for MT5 accounts
 * Version 2.0 - Mit INSERT Support für neue Konten
 */

// Set headers
header('Content-Type: text/plain; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Function to log messages
function logMessage($message) {
    $logFile = __DIR__ . '/robo_update.log';
    $timestamp = date('Y-m-d H:i:s');
    file_put_contents($logFile, "[$timestamp] $message\n", FILE_APPEND);
}

// Get input data
$input = file_get_contents('php://input');
logMessage("Received request: " . $input);

// Parse JSON or form data
$data = null;
if (!empty($input)) {
    $jsonData = json_decode($input, true);
    if ($jsonData !== null) {
        $data = $jsonData;
    }
}

// Fallback to GET/POST parameters
if (!$data) {
    $data = array_merge($_GET, $_POST);
}

// Validate required parameters
if (!isset($data['account']) || !isset($data['status'])) {
    echo "error: Missing required parameters (account, status)";
    logMessage("Error: Missing parameters");
    exit;
}

$account = $data['account'];
$status = $data['status'];
$program = isset($data['program']) ? $data['program'] : 'don_gpt';

// Database configuration - KORREKTE ZUGANGSDATEN aus server_credentials.txt
$db_host = 'localhost';
$db_user = 'prophelp_adm';
$db_pass = 'mW0uG1pG9b';
$db_name = 'prophelp_users_1';
$db_table = 'lnative';

// Connect to database
$mysqli = new mysqli($db_host, $db_user, $db_pass, $db_name);

// Check connection
if ($mysqli->connect_error) {
    $error = "Database connection failed: " . $mysqli->connect_error;
    echo "error: " . $error;
    logMessage($error);
    exit;
}

// Set charset
$mysqli->set_charset("utf8");

// Check if roboaffiliate column exists
$checkColumn = "SHOW COLUMNS FROM `$db_table` LIKE 'roboaffiliate'";
$result = $mysqli->query($checkColumn);

if ($result->num_rows == 0) {
    // Column doesn't exist, create it
    $addColumn = "ALTER TABLE `$db_table` ADD COLUMN `roboaffiliate` VARCHAR(10) DEFAULT 'no' AFTER `fee`";
    if (!$mysqli->query($addColumn)) {
        $error = "Failed to add roboaffiliate column: " . $mysqli->error;
        echo "error: " . $error;
        logMessage($error);
        $mysqli->close();
        exit;
    }
    logMessage("Created roboaffiliate column");
}

// Prepare status value
$status_value = ($status === 'yes' || $status === '1' || $status === 1 || $status === true) ? 'yes' : 'no';

// WICHTIG: Erst prüfen ob Account existiert
$check_query = "SELECT * FROM `$db_table` WHERE `account` = ? LIMIT 1";
$check_stmt = $mysqli->prepare($check_query);
$check_stmt->bind_param("s", $account);
$check_stmt->execute();
$check_result = $check_stmt->get_result();

if ($check_result->num_rows > 0) {
    // Account existiert - UPDATE
    $existing_row = $check_result->fetch_assoc();
    $check_stmt->close();
    
    $update_query = "UPDATE `$db_table` SET `roboaffiliate` = ? WHERE `account` = ?";
    $stmt = $mysqli->prepare($update_query);
    
    if (!$stmt) {
        $error = "Prepare UPDATE failed: " . $mysqli->error;
        echo "error: " . $error;
        logMessage($error);
        $mysqli->close();
        exit;
    }
    
    $stmt->bind_param("ss", $status_value, $account);
    
    if ($stmt->execute()) {
        echo "success: Updated account $account with status $status_value";
        logMessage("Successfully updated account $account with status $status_value");
    } else {
        $error = "Update failed: " . $stmt->error;
        echo "error: " . $error;
        logMessage($error);
    }
    $stmt->close();
    
} else {
    // Account existiert NICHT - INSERT neuen Datensatz
    $check_stmt->close();
    
    // Hole aktuelle Zeit und IP
    $current_time = date('Y-m-d H:i:s');
    $ip_address = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
    
    // INSERT mit minimalen Pflichtfeldern
    // Die meisten Felder haben Defaults oder können NULL sein
    $insert_query = "INSERT INTO `$db_table` 
                    (`account`, `roboaffiliate`, `program`, `ip`, `last_connect`, `created`) 
                    VALUES (?, ?, ?, ?, ?, ?)";
    
    $stmt = $mysqli->prepare($insert_query);
    
    if (!$stmt) {
        // Falls der einfache INSERT fehlschlägt, versuche mit mehr Defaults
        $insert_query = "INSERT INTO `$db_table` 
                        (`account`, `roboaffiliate`, `program`, `ip`, `last_connect`, 
                         `serialNo`, `UUID`, `company`, `server`, `currency`, 
                         `type`, `mt`, `version`, `balance`, `equity`, 
                         `hist_balance`, `close_profit`, `trading`, `test`, 
                         `comment`, `ref`, `registrar`, `fee`, `created`) 
                        VALUES (?, ?, ?, ?, ?, 
                                '', '', 'RoboForex', '', 'USD', 
                                'Real', '5', '0', '0', '0', 
                                '0', '0', 'Investor', '0', 
                                '', '', 'site', '0', ?)";
        
        $stmt = $mysqli->prepare($insert_query);
        
        if (!$stmt) {
            $error = "Prepare INSERT failed: " . $mysqli->error;
            echo "error: " . $error;
            logMessage($error);
            $mysqli->close();
            exit;
        }
        
        // Bind für erweiterten INSERT
        $stmt->bind_param("ssssss", $account, $status_value, $program, $ip_address, $current_time, $current_time);
    } else {
        // Bind für einfachen INSERT
        $stmt->bind_param("ssssss", $account, $status_value, $program, $ip_address, $current_time, $current_time);
    }
    
    if ($stmt->execute()) {
        echo "success: Created new account $account with status $status_value";
        logMessage("Successfully created new account $account with status $status_value");
    } else {
        // Falls INSERT fehlschlägt, versuche es mit minimal INSERT
        $stmt->close();
        
        $minimal_insert = "INSERT IGNORE INTO `$db_table` (`account`, `roboaffiliate`) VALUES (?, ?)";
        $stmt = $mysqli->prepare($minimal_insert);
        
        if ($stmt) {
            $stmt->bind_param("ss", $account, $status_value);
            if ($stmt->execute()) {
                echo "success: Created minimal entry for account $account with status $status_value";
                logMessage("Created minimal entry for account $account");
            } else {
                $error = "All INSERT attempts failed: " . $stmt->error;
                echo "error: " . $error;
                logMessage($error);
            }
        }
    }
    $stmt->close();
}

// Close connection
$mysqli->close();

?>