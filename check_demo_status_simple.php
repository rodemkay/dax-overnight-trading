<?php
/**
 * Vereinfachte Demo-Status Prüfung
 * Gibt immer wait|20 zurück bis die Spalten existieren
 */

// Fehlerbehandlung
error_reporting(0);
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

// Prüfe ob Account existiert und RoboAffiliate ist
$query = "SELECT full_name, roboaffiliate FROM lnative WHERE account='$account' LIMIT 1";
$result = mysqli_query($db, $query);

if (!$result) {
    // Tabelle oder Spalte existiert nicht
    echo "wait|20";
    mysqli_close($db);
    exit;
}

if (mysqli_num_rows($result) == 0) {
    // Account noch nicht in DB
    echo "wait|20";
    mysqli_close($db);
    exit;
}

$row = mysqli_fetch_assoc($result);
$full_name = $row['full_name'];
$roboaffiliate = $row['roboaffiliate'];

// RoboForex Affiliate = unbegrenzt
if ($roboaffiliate == 'yes' || $roboaffiliate == '1') {
    echo "unlimited|roboforex|0";
    mysqli_close($db);
    exit;
}

// Prüfe ob demo_expires Spalte existiert
$check = "SHOW COLUMNS FROM lnative LIKE 'demo_expires'";
$check_result = mysqli_query($db, $check);

if (!$check_result || mysqli_num_rows($check_result) == 0) {
    // Spalte existiert noch nicht
    echo "wait|30";
    mysqli_close($db);
    exit;
}

// Prüfe ob program Spalte existiert  
$check2 = "SHOW COLUMNS FROM lnative LIKE 'program'";
$check_result2 = mysqli_query($db, $check2);

if (!$check_result2 || mysqli_num_rows($check_result2) == 0) {
    // Spalte existiert noch nicht
    echo "wait|30";
    mysqli_close($db);
    exit;
}

// Suche Demo-Eintrag für full_name + program
$query2 = "SELECT demo_expires FROM lnative 
           WHERE full_name='$full_name' 
           AND program='$program' 
           AND demo_expires IS NOT NULL 
           LIMIT 1";

$result2 = mysqli_query($db, $query2);

if ($result2 && mysqli_num_rows($result2) > 0) {
    $row2 = mysqli_fetch_assoc($result2);
    $demo_expires = $row2['demo_expires'];
    
    // Prüfe ob noch gültig
    if (strtotime($demo_expires) >= time()) {
        $days_left = floor((strtotime($demo_expires) - time()) / 86400);
        echo "valid|$demo_expires|$days_left";
    } else {
        echo "expired|$demo_expires|0";
    }
} else {
    // Noch kein Demo-Zeitraum - Office soll anlegen
    echo "wait|15";
}

mysqli_close($db);
?>