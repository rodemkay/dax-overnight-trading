<?php
/**
 * Demo-Status Prüfung für EA Lizenzsystem
 * Prüft ob ein Account noch im Demo-Zeitraum ist
 * 
 * Parameter:
 * - account: MT5 Account-Nummer
 * - program: Programmname (z.B. "der_don")
 * 
 * Rückgabe:
 * - wait|X: Warte X Sekunden
 * - valid|datum|tage: Demo gültig bis datum, noch X tage
 * - expired|datum|0: Demo abgelaufen seit datum
 */

// Fehlerbehandlung
error_reporting(E_ALL);
ini_set('display_errors', 0);

// Datenbank-Verbindung
$servername = "localhost";
$username = "prophelp_adm";
$password = "mW0uG1pG9b";
$dbname = "prophelp_users_1";

$db = mysqli_connect($servername, $username, $password, $dbname);

if (!$db) {
    die("error|db_connection_failed");
}

// Parameter validieren
if (!isset($_GET['account']) || !isset($_GET['program'])) {
    die("error|missing_parameters");
}

$account = mysqli_real_escape_string($db, $_GET['account']);
$program = mysqli_real_escape_string($db, $_GET['program']);

// Debug-Logging (optional)
$debug = false;
if ($debug) {
    error_log("check_demo_status: account=$account, program=$program");
}

// 1. Prüfe ob Account bereits in DB existiert
$query = "SELECT full_name, test, payment, roboaffiliate 
          FROM lnative 
          WHERE account='$account' 
          LIMIT 1";

$result = mysqli_query($db, $query);

if (!$result) {
    die("error|query_failed_1");
}

if (mysqli_num_rows($result) == 0) {
    // Account noch nicht in DB - EA soll warten
    echo "wait|20";  // Warte 20 Sekunden auf ersten DB-Eintrag
    mysqli_close($db);
    exit;
}

$row = mysqli_fetch_assoc($result);
$full_name = $row['full_name'];
$roboaffiliate = $row['roboaffiliate'];

// Spezialfall: RoboForex Affiliate hat unbegrenzte Nutzung
if ($roboaffiliate == 'yes' || $roboaffiliate == '1') {
    echo "unlimited|roboforex|0";
    mysqli_close($db);
    exit;
}

// 2. Prüfe ob Spalten existieren und Demo-Zeitraum gesetzt ist
// Prüfe erstmal ob die Spalten existieren
$check_columns = "SHOW COLUMNS FROM lnative LIKE 'demo_expires'";
$col_result = mysqli_query($db, $check_columns);
if (mysqli_num_rows($col_result) == 0) {
    // Spalte existiert noch nicht - warten
    echo "wait|30";
    mysqli_close($db);
    exit;
}

// 2. Prüfe ob für full_name + program bereits ein Demo-Zeitraum existiert
$query = "SELECT id, account 
          FROM lnative 
          WHERE full_name='$full_name' 
          AND program='$program' 
          AND demo_expires IS NOT NULL 
          ORDER BY id DESC 
          LIMIT 1";

$result = mysqli_query($db, $query);

if (!$result) {
    die("error|query_failed_2");
}

if (mysqli_num_rows($result) > 0) {
    // Demo-Zeitraum existiert bereits für diesen User + Program
    $row = mysqli_fetch_assoc($result);
    $demo_expires = $row['demo_expires'];
    $existing_account = $row['account'];
    
    // Wenn es ein anderer Account ist, update account nummer
    if ($existing_account != $account) {
        $update = "UPDATE lnative 
                   SET account='$account' 
                   WHERE full_name='$full_name' 
                   AND program='$program' 
                   AND id=" . $row['id'];
        mysqli_query($db, $update);
    }
    
    // Prüfe ob noch gültig
    if (strtotime($demo_expires) >= time()) {
        $days_left = floor((strtotime($demo_expires) - time()) / 86400);
        echo "valid|$demo_expires|$days_left";
    } else {
        echo "expired|$demo_expires|0";
    }
} else {
    // Kein Demo-Zeitraum gefunden - prüfe ob schon für diesen Account gesetzt
    $query = "SELECT id 
              FROM lnative 
              WHERE account='$account' 
              AND program='$program' 
              LIMIT 1";
    
    $result = mysqli_query($db, $query);
    
    if (!$result) {
        die("error|query_failed_3");
    }
    
    if (mysqli_num_rows($result) > 0) {
        $row = mysqli_fetch_assoc($result);
        
        if ($row['demo_expires'] != NULL) {
            // Demo wurde inzwischen gesetzt (durch Office)
            $demo_expires = $row['demo_expires'];
            
            if (strtotime($demo_expires) >= time()) {
                $days_left = floor((strtotime($demo_expires) - time()) / 86400);
                echo "valid|$demo_expires|$days_left";
            } else {
                echo "expired|$demo_expires|0";
            }
        } else {
            // Demo-Zeitraum wird von Office automatisch gesetzt
            // EA soll nochmal warten
            echo "wait|10";
        }
    } else {
        // Account + Program Kombination existiert noch nicht
        // Wird beim nächsten Connect automatisch angelegt
        echo "wait|15";
    }
}

mysqli_close($db);
?>