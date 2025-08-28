<?php
/**
 * Sichere Datenbank-API für prophelp_users_1
 * Korrigierte Version mit konsistenter Response-Struktur
 */

// CORS-Header für Cross-Origin-Requests
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Content-Type: application/json; charset=UTF-8');

// Bei OPTIONS-Request (Preflight) direkt beenden
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// ===== KONFIGURATION =====
$API_TOKEN = '250277100311270613';

// Datenbankverbindung
$DB_CONFIG = [
    'host' => 'localhost',
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
    
    // Token aus verschiedenen Quellen lesen
    $token = null;
    
    // Aus JSON-Body
    $input = json_decode(file_get_contents('php://input'), true);
    if (isset($input['token'])) {
        $token = $input['token'];
    }
    // Aus POST-Daten
    elseif (isset($_POST['token'])) {
        $token = $_POST['token'];
    }
    // Aus Authorization-Header
    elseif (isset($_SERVER['HTTP_AUTHORIZATION'])) {
        $token = str_replace('Bearer ', '', $_SERVER['HTTP_AUTHORIZATION']);
    }
    
    if (!$token || $token !== $API_TOKEN) {
        send_response([
            'status' => 'error',
            'message' => 'Unauthorized: Invalid or missing token'
        ], 401);
    }
    
    return $input ?: $_POST;
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
        send_response([
            'status' => 'error',
            'message' => 'Database connection failed: ' . $e->getMessage()
        ], 500);
    }
}

/**
 * Führt eine Query aus
 */
function execute_query($pdo, $query, $params = []) {
    try {
        $stmt = $pdo->prepare($query);
        $stmt->execute($params);
        
        // Bestimme Query-Typ
        $query_type = strtoupper(substr(trim($query), 0, 6));
        
        if (in_array($query_type, ['SELECT', 'SHOW', 'DESCRI'])) {
            return [
                'type' => 'select',
                'data' => $stmt->fetchAll(),
                'count' => $stmt->rowCount()
            ];
        } else {
            return [
                'type' => 'modify',
                'affected_rows' => $stmt->rowCount(),
                'last_insert_id' => $pdo->lastInsertId()
            ];
        }
    } catch (PDOException $e) {
        return [
            'type' => 'error',
            'message' => 'Query failed: ' . $e->getMessage()
        ];
    }
}

// ===== HAUPTLOGIK =====

// Authentifizierung prüfen und Input lesen
$input = check_auth();

// Action bestimmen
$action = $input['action'] ?? 'test';

// Datenbankverbindung
$pdo = get_db_connection();

// Response vorbereiten - IMMER mit status: success
$response = ['status' => 'success'];

switch ($action) {
    case 'test':
        // Verbindungstest
        $response['message'] = 'Connection successful';
        $response['database'] = $DB_CONFIG['database'];
        $response['timestamp'] = date('Y-m-d H:i:s');
        break;
        
    case 'query':
        // Beliebige Query ausführen
        if (!isset($input['query'])) {
            send_response([
                'status' => 'error',
                'message' => 'Missing query parameter'
            ], 400);
        }
        
        $result = execute_query($pdo, $input['query'], $input['params'] ?? []);
        
        if ($result['type'] === 'error') {
            send_response([
                'status' => 'error',
                'message' => $result['message']
            ], 400);
        } elseif ($result['type'] === 'select') {
            $response['data'] = $result['data'];
            $response['count'] = $result['count'];
        } else {
            $response['affected_rows'] = $result['affected_rows'];
            $response['last_insert_id'] = $result['last_insert_id'];
        }
        break;
        
    case 'tables':
        // Alle Tabellen auflisten
        $result = execute_query($pdo, "SHOW TABLES");
        if ($result['type'] === 'error') {
            send_response([
                'status' => 'error',
                'message' => $result['message']
            ], 400);
        }
        $response['data'] = array_map(function($row) {
            return array_values($row)[0];
        }, $result['data']);
        break;
        
    case 'describe':
        // Tabellenstruktur anzeigen
        if (!isset($input['table'])) {
            send_response([
                'status' => 'error',
                'message' => 'Missing table parameter'
            ], 400);
        }
        
        $result = execute_query($pdo, "DESCRIBE " . $input['table']);
        if ($result['type'] === 'error') {
            send_response([
                'status' => 'error',
                'message' => $result['message']
            ], 400);
        }
        $response['data'] = $result['data'];
        break;
        
    case 'license_check':
        // Spezielle Funktion für Lizenz-Checks
        if (!isset($input['account'])) {
            send_response([
                'status' => 'error',
                'message' => 'Missing account parameter'
            ], 400);
        }
        
        $query = "SELECT * FROM lnative WHERE account = ? AND status = 'active'";
        $result = execute_query($pdo, $query, [$input['account']]);
        
        if ($result['type'] === 'error') {
            send_response([
                'status' => 'error',
                'message' => $result['message']
            ], 400);
        }
        
        $licenses = $result['data'];
        $response['has_license'] = count($licenses) > 0;
        if (count($licenses) > 0) {
            $response['license_details'] = $licenses[0];
        }
        break;
        
    case 'get_all':
        // Alle Datensätze aus lnative abrufen
        $query = "SELECT * FROM lnative";
        $result = execute_query($pdo, $query);
        
        if ($result['type'] === 'error') {
            send_response([
                'success' => false,
                'error' => $result['message']
            ], 400);
        }
        
        $response = [
            'success' => true,
            'data' => $result['data']
        ];
        break;
        
    case 'get_account':
        // Ein spezifisches Konto abrufen
        if (!isset($input['account'])) {
            send_response([
                'success' => false,
                'error' => 'Missing account parameter'
            ], 400);
        }
        
        $query = "SELECT * FROM lnative WHERE account = ?";
        $result = execute_query($pdo, $query, [$input['account']]);
        
        if ($result['type'] === 'error') {
            send_response([
                'success' => false,
                'error' => $result['message']
            ], 400);
        }
        
        $response = [
            'success' => true,
            'data' => count($result['data']) > 0 ? $result['data'][0] : null
        ];
        break;
        
    case 'update_affiliate':
        // Affiliate-Status aktualisieren
        if (!isset($input['account']) || !isset($input['affiliate_status'])) {
            send_response([
                'success' => false,
                'error' => 'Missing account or affiliate_status parameter'
            ], 400);
        }
        
        // Prüfe ob die Spalte existiert
        $check_column = execute_query($pdo, "SHOW COLUMNS FROM lnative LIKE 'roboaffiliate'");
        if (count($check_column['data']) == 0) {
            // Spalte existiert nicht, versuche sie zu erstellen
            $create_column = execute_query($pdo, "ALTER TABLE lnative ADD COLUMN roboaffiliate VARCHAR(10) DEFAULT 'unknown'");
            if ($create_column['type'] === 'error') {
                send_response([
                    'success' => false,
                    'error' => "Column 'roboaffiliate' doesn't exist and could not be created"
                ], 400);
            }
        }
        
        // Update durchführen
        $query = "UPDATE lnative SET roboaffiliate = ? WHERE account = ?";
        $result = execute_query($pdo, $query, [$input['affiliate_status'], $input['account']]);
        
        if ($result['type'] === 'error') {
            send_response([
                'success' => false,
                'error' => $result['message']
            ], 400);
        }
        
        $response = [
            'success' => true,
            'message' => 'Affiliate status updated',
            'affected_rows' => $result['affected_rows']
        ];
        break;
        
    default:
        send_response([
            'status' => 'error',
            'message' => 'Invalid action: ' . $action
        ], 400);
}

// Response senden
send_response($response);
?>
