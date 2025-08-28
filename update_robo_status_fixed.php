<?php
/**
 * Update RoboForex Status in Database
 * This script updates the roboaffiliate status for MT5 accounts
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

// Prepare update query
$status_value = ($status === 'yes' || $status === '1' || $status === 1 || $status === true) ? 'yes' : 'no';

$update_query = "UPDATE `$db_table` SET `roboaffiliate` = ? WHERE `account` = ?";
$stmt = $mysqli->prepare($update_query);

if (!$stmt) {
    $error = "Prepare failed: " . $mysqli->error;
    echo "error: " . $error;
    logMessage($error);
    $mysqli->close();
    exit;
}

// Bind parameters
$stmt->bind_param("ss", $status_value, $account);

// Execute update
if ($stmt->execute()) {
    $affected_rows = $stmt->affected_rows;
    
    if ($affected_rows > 0) {
        echo "success: Updated account $account with status $status_value";
        logMessage("Successfully updated account $account with status $status_value");
    } else {
        // Check if account exists
        $check_query = "SELECT COUNT(*) as count FROM `$db_table` WHERE `account` = ?";
        $check_stmt = $mysqli->prepare($check_query);
        $check_stmt->bind_param("s", $account);
        $check_stmt->execute();
        $check_result = $check_stmt->get_result();
        $row = $check_result->fetch_assoc();
        
        if ($row['count'] > 0) {
            echo "info: Account $account already has status $status_value";
            logMessage("Account $account already has status $status_value");
        } else {
            echo "warning: Account $account not found in database";
            logMessage("Account $account not found in database");
        }
        $check_stmt->close();
    }
} else {
    $error = "Update failed: " . $stmt->error;
    echo "error: " . $error;
    logMessage($error);
}

// Close connections
$stmt->close();
$mysqli->close();

?>