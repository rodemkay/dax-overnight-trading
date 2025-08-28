<?php
/**
 * Sichere Datenbank-API für prophelp_users_1
 * Dieses Script auf dem Server unter /www/lic.prophelper.org/api/ hochladen
 * 
 * KONFIGURIERT MIT TOKEN: 250277100311270613
 */

// CORS-Header für Cross-Origin-Requests
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json; charset=UTF-8');

// Bei OPTIONS-Request (Preflight) direkt beenden
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// ===== KONFIGURATION =====
// Token wie vom Benutzer angegeben
$API_TOKEN = '250277100311270613';

// Datenbankverbindung
$DB_CONFIG = [
    'host' => 'localhost',  // Auf dem Server selbst
    'database' => 'prophelp_users_1',
    'username' => 'prophelp_adm',
    'password' => 'mW0uG1pG9b',
    'charset' => 'utf8mb4'
];

// ===== FUNKTIONEN =====

/**
 * Sendet JSON-Response und beendet Script
 */
function send_response($data, $status_code = 200) {
    http_response_code($status_code);
    echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit();
}

/**
 * Prüft die Authentifizierung
 */
function check_auth() {
    global $API_TOKEN;
    
    // Token aus POST oder Header lesen
    $token = null;
    
    // 1. Aus POST-Daten
    if (isset($_POST['token'])) {
        $token = $_POST['token'];
    }
    // 2. Aus JSON-Body
    else {
        $input = json_decode(file_get_contents('php://input'), true);
        if (isset($input['token'])) {
            $token = $input['token'];
        }
    }
    // 3. Aus Authorization-Header
    else if (isset($_SERVER['HTTP_AUTHORIZATION'])) {
        $token = str_replace('Bearer ', '', $_SERVER['HTTP_AUTHORIZATION']);
    }
    
    if (!$token || $token !== $API_TOKEN) {
        send_response(['error' => 'Unauthorized: Invalid or missing token'], 401);
    }
}

/**
 * Stellt Datenbankverbindung her
 */
function get_db_connection() {
    global $DB_CONFIG;
    
    try {
        $dsn = sprintf(
            'mysql:host=%s;dbname=%s;charset=%s',
            $DB_CONFIG['host'],
            $DB_CONFIG['database'],
            $DB_CONFIG['charset']
        );
        
        $pdo = new PDO($dsn, $DB_CONFIG['username'], $DB_CONFIG['password']);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        
        return $pdo;
    } catch (PDOException $e) {
        send_response(['error' => 'Database connection failed: ' . $e->getMessage()], 500);
    }
}

/**
 * Führt eine SELECT-Query aus
 */
function execute_select($pdo, $query, $params = []) {
    try {
        $stmt = $pdo->prepare($query);
        $stmt->execute($params);
        return $stmt->fetchAll();
    } catch (PDOException $e) {
        send_response(['error' => 'Query failed: ' . $e->getMessage()], 400);
    }
}

/**
 * Führt INSERT/UPDATE/DELETE aus
 */
function execute_modify($pdo, $query, $params = []) {
    try {
        $stmt = $pdo->prepare($query);
        $stmt->execute($params);
        return [
            'affected_rows' => $stmt->rowCount(),
            'last_insert_id' => $pdo->lastInsertId()
        ];
    } catch (PDOException $e) {
        send_response(['error' => 'Query failed: ' . $e->getMessage()], 400);
    }
}

// ===== HAUPTLOGIK =====

// Authentifizierung prüfen
check_auth();

// Request-Daten lesen (POST oder JSON)
$input = json_decode(file_get_contents('php://input'), true) ?: $_POST;

// Action bestimmen
$action = $input['action'] ?? 'query';

// Datenbankverbindung
$pdo = get_db_connection();

// Response vorbereiten
$response = ['success' => true];

switch ($action) {
    case 'test':
        // Verbindungstest
        $response['message'] = 'Connection successful';
        $response['database'] = $DB_CONFIG['database'];
        break;
        
    case 'query':
        // Beliebige Query ausführen
        if (!isset($input['query'])) {
            send_response(['error' => 'Missing query parameter'], 400);
        }
        
        $query = $input['query'];
        $params = $input['params'] ?? [];
        
        // Bestimme Query-Typ
        $query_type = strtoupper(substr(trim($query), 0, 6));
        
        if ($query_type === 'SELECT' || $query_type === 'SHOW' || $query_type === 'DESCRI') {
            $response['data'] = execute_select($pdo, $query, $params);
            $response['count'] = count($response['data']);
        } else {
            $result = execute_modify($pdo, $query, $params);
            $response['affected_rows'] = $result['affected_rows'];
            $response['last_insert_id'] = $result['last_insert_id'];
        }
        break;
        
    case 'tables':
        // Alle Tabellen auflisten
        $response['data'] = execute_select($pdo, "SHOW TABLES");
        break;
        
    case 'describe':
        // Tabellenstruktur anzeigen
        if (!isset($input['table'])) {
            send_response(['error' => 'Missing table parameter'], 400);
        }
        $response['data'] = execute_select($pdo, "DESCRIBE " . $input['table']);
        break;
        
    case 'license_check':
        // Spezielle Funktion für Lizenz-Checks
        if (!isset($input['account'])) {
            send_response(['error' => 'Missing account parameter'], 400);
        }
        
        $query = "SELECT * FROM lnative WHERE account = ? AND status = 'active'";
        $licenses = execute_select($pdo, $query, [$input['account']]);
        
        $response['data'] = $licenses;
        $response['has_license'] = count($licenses) > 0;
        break;
        
    default:
        send_response(['error' => 'Invalid action: ' . $action], 400);
}

// Response senden
send_response($response);
?>
