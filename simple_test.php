<?php
// Ganz einfacher Test ohne Datenbank
header('Content-Type: text/plain; charset=UTF-8');

echo "Simple Test PHP\n";
echo "===============\n\n";

echo "PHP Version: " . phpversion() . "\n";
echo "Server: " . ($_SERVER['SERVER_SOFTWARE'] ?? 'unknown') . "\n\n";

// Token Test
$token = '250277100311270613';
$input = file_get_contents('php://input');
echo "Raw Input: " . $input . "\n\n";

$json = json_decode($input, true);
if ($json) {
    echo "JSON decoded successfully\n";
    echo "Received token: " . ($json['token'] ?? 'no token') . "\n";
    echo "Expected token: " . $token . "\n";
    
    if (isset($json['token']) && $json['token'] === $token) {
        echo "\n✓ Token is correct!\n";
    } else {
        echo "\n✗ Token is incorrect or missing!\n";
    }
} else {
    echo "No JSON input received\n";
}

echo "\nPDO Available: " . (class_exists('PDO') ? 'Yes' : 'No') . "\n";
echo "MySQL Driver: " . (in_array('mysql', PDO::getAvailableDrivers()) ? 'Yes' : 'No') . "\n";

// Versuche Datenbank-Verbindung nur wenn Token stimmt
if (isset($json['token']) && $json['token'] === $token) {
    echo "\nTrying database connection...\n";
    try {
        $pdo = new PDO(
            'mysql:host=localhost;dbname=prophelp_users_1;charset=utf8mb4',
            'prophelp_adm',
            'mW0uG1pG9b'
        );
        echo "✓ Database connection successful!\n";
        
        $stmt = $pdo->query("SELECT VERSION() as version");
        $result = $stmt->fetch(PDO::FETCH_ASSOC);
        echo "MySQL Version: " . $result['version'] . "\n";
        
    } catch (PDOException $e) {
        echo "✗ Database connection failed: " . $e->getMessage() . "\n";
    }
}

echo "\n[End of test]\n";
?>
