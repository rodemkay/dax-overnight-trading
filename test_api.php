<?php
/**
 * Test-Script für API-Debugging
 * Testet Schritt für Schritt die Funktionalität
 */

// Error Reporting aktivieren für Debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Header setzen
header('Content-Type: application/json; charset=UTF-8');

// Test-Response vorbereiten
$response = array(
    'test' => 'basic',
    'php_version' => phpversion(),
    'server' => $_SERVER['SERVER_SOFTWARE'] ?? 'unknown'
);

// Schritt 1: Basis-Test
$response['step1_basic'] = 'OK';

// Schritt 2: JSON-Funktionen testen
$response['step2_json'] = function_exists('json_encode') ? 'OK' : 'FEHLER';

// Schritt 3: PDO-Verfügbarkeit prüfen
$response['step3_pdo'] = class_exists('PDO') ? 'OK' : 'FEHLER';

// Schritt 4: MySQL-PDO Treiber prüfen
$response['step4_mysql_driver'] = in_array('mysql', PDO::getAvailableDrivers()) ? 'OK' : 'FEHLER';

// Schritt 5: Token-Test
$token = '250277100311270613';
$input = json_decode(file_get_contents('php://input'), true);
$received_token = $input['token'] ?? 'no_token';
$response['step5_token'] = ($received_token === $token) ? 'OK' : 'Token erwartet: ' . $token . ', erhalten: ' . $received_token;

// Schritt 6: Datenbankverbindung testen (nur wenn Token stimmt)
if ($received_token === $token) {
    try {
        $pdo = new PDO(
            'mysql:host=localhost;dbname=prophelp_users_1;charset=utf8mb4',
            'prophelp_adm',
            'mW0uG1pG9b'
        );
        $response['step6_database'] = 'OK - Verbindung erfolgreich';
        
        // Test-Query
        $stmt = $pdo->query("SELECT COUNT(*) as count FROM lnative");
        $result = $stmt->fetch(PDO::FETCH_ASSOC);
        $response['step7_query'] = 'OK - lnative hat ' . $result['count'] . ' Einträge';
        
    } catch (PDOException $e) {
        $response['step6_database'] = 'FEHLER: ' . $e->getMessage();
    }
} else {
    $response['step6_database'] = 'Übersprungen - Token nicht korrekt';
}

// Response senden
echo json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
?>
