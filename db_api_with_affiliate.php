<?php
/**
 * Erweiterte Datenbank-API mit Affiliate-Status Support
 * Für prophelp_users_1 Database
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

/**
 * Prüft und erstellt ggf. die affiliate_status Spalte
 */
function ensure_affiliate_column($pdo) {
    // Prüfe ob Spalte existiert
    $result = execute_query($pdo, "SHOW COLUMNS FROM lnative LIKE 'affiliate_status'");
    
    if ($result['type'] === 'select' && count($result['data']) === 0) {
        // Spalte existiert nicht, füge sie hinzu
        $alter_result = execute_query($pdo, "ALTER TABLE lnative ADD COLUMN affiliate_status VARCHAR(10) DEFAULT 'unknown'");
        
        if ($alter_result['type'] === 'error') {
            // Möglicherweise existiert die Spalte bereits (race condition)
            // Das ist OK, wir machen einfach weiter
            return true;
        }
        
        return $alter_result['type'] === 'modify';
    }
    
    return true; // Spalte existiert bereits
}

// ===== HAUPTLOGIK =====

// Authentifizierung prüfen und Input lesen
$input = check_auth();

// Action bestimmen
$action = $input['action'] ?? 'test';

// Datenbankverbindung
$pdo = get_db_connection();

// Response vorbereiten
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
        
    case 'update_affiliate_status':
        // Neue Funktion: Update Affiliate Status
        if (!isset($input['account']) || !isset($input['affiliate_status'])) {
            send_response([
                'status' => 'error',
                'message' => 'Missing account or affiliate_status parameter'
            ], 400);
        }
        
        // Stelle sicher, dass die affiliate_status Spalte existiert
        ensure_affiliate_column($pdo);
        
        $account = $input['account'];
        $affiliate_status = $input['affiliate_status'];
        
        // Validiere Status
        if (!in_array($affiliate_status, ['yes', 'no', 'unknown'])) {
            send_response([
                'status' => 'error',
                'message' => 'Invalid affiliate_status. Must be yes, no, or unknown'
            ], 400);
        }
        
        // Update den Status für alle Einträge dieses Accounts
        $query = "UPDATE lnative SET affiliate_status = ? WHERE account = ?";
        $result = execute_query($pdo, $query, [$affiliate_status, $account]);
        
        if ($result['type'] === 'error') {
            send_response([
                'status' => 'error',
                'message' => $result['message']
            ], 400);
        }
        
        $response['affected_rows'] = $result['affected_rows'];
        $response['account'] = $account;
        $response['affiliate_status'] = $affiliate_status;
        
        // Hole aktualisierten Datensatz
        $check_query = "SELECT account, broker, affiliate_status FROM lnative WHERE account = ? LIMIT 1";
        $check_result = execute_query($pdo, $check_query, [$account]);
        
        if ($check_result['type'] === 'select' && count($check_result['data']) > 0) {
            $response['updated_record'] = $check_result['data'][0];
        }
        break;
        
    case 'get_affiliate_status':
        // Neue Funktion: Affiliate Status abrufen
        if (!isset($input['account'])) {
            send_response([
                'status' => 'error',
                'message' => 'Missing account parameter'
            ], 400);
        }
        
        // Stelle sicher, dass die affiliate_status Spalte existiert
        ensure_affiliate_column($pdo);
        
        $account = $input['account'];
        
        $query = "SELECT account, broker, affiliate_status FROM lnative WHERE account = ?";
        $result = execute_query($pdo, $query, [$account]);
        
        if ($result['type'] === 'error') {
            send_response([
                'status' => 'error',
                'message' => $result['message']
            ], 400);
        }
        
        if (count($result['data']) > 0) {
            $response['found'] = true;
            $response['affiliate_status'] = $result['data'][0]['affiliate_status'] ?? 'unknown';
            $response['broker'] = $result['data'][0]['broker'] ?? '';
        } else {
            $response['found'] = false;
            $response['affiliate_status'] = 'unknown';
        }
        break;
        
    case 'get_all_affiliate_status':
        // Neue Funktion: Alle Accounts mit Affiliate Status abrufen
        
        // Stelle sicher, dass die affiliate_status Spalte existiert
        ensure_affiliate_column($pdo);
        
        $query = "SELECT account, broker, programm, affiliate_status, add_date, 
                         last_connect, balance, currency 
                  FROM lnative 
                  WHERE account IS NOT NULL 
                  ORDER BY last_connect DESC 
                  LIMIT " . ($input['limit'] ?? 100);
        
        $result = execute_query($pdo, $query);
        
        if ($result['type'] === 'error') {
            send_response([
                'status' => 'error',
                'message' => $result['message']
            ], 400);
        }
        
        $response['data'] = $result['data'];
        $response['count'] = $result['count'];
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
