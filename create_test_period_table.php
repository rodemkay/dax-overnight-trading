<?php
/**
 * Script zum Erstellen der test_period_history Tabelle
 * Dieses Script direkt über Browser aufrufen: 
 * https://lic.prophelper.org/files/create_test_period_table.php
 */

// Datenbank-Verbindung
$db_host = 'localhost';
$db_user = 'prophelp_adm';
$db_pass = 'mW0uG1pG9b';
$db_name = 'prophelp_users_1';

// Verbindung herstellen
$mysqli = new mysqli($db_host, $db_user, $db_pass, $db_name);

if ($mysqli->connect_error) {
    die("❌ Verbindungsfehler: " . $mysqli->connect_error);
}

echo "<h2>Test Period History - Tabellen-Setup</h2>";
echo "<pre>";

// SQL für Tabellen-Erstellung
$create_table_sql = "
CREATE TABLE IF NOT EXISTS test_period_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_name VARCHAR(255) NOT NULL COMMENT 'Name aus MT5 Account',
    program_name VARCHAR(100) NOT NULL COMMENT 'EA-Name (the_don, breakout_brain, etc.)',
    program_version VARCHAR(50) NOT NULL COMMENT 'Version (1.24, 1.25, etc.)',
    first_test_date DATETIME NOT NULL COMMENT 'Wann Testzeitraum gestartet wurde',
    test_count INT DEFAULT 1 COMMENT 'Anzahl genutzter Testzeiträume',
    account_type VARCHAR(20) DEFAULT NULL COMMENT 'DEMO oder LIVE',
    account_number VARCHAR(50) DEFAULT NULL COMMENT 'MT5 Kontonummer',
    server_name VARCHAR(255) DEFAULT NULL COMMENT 'MT5 Server Name',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_test (account_name, program_name, program_version),
    KEY idx_account_name (account_name),
    KEY idx_program (program_name, program_version),
    KEY idx_test_date (first_test_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Testzeitraum-Historie für EA Lizenzsystem'
";

// Tabelle erstellen
if ($mysqli->query($create_table_sql)) {
    echo "✅ Tabelle test_period_history erfolgreich erstellt/aktualisiert\n\n";
} else {
    echo "❌ Fehler beim Erstellen der Tabelle: " . $mysqli->error . "\n\n";
}

// Prüfe ob Tabelle existiert
$check_table = $mysqli->query("SHOW TABLES LIKE 'test_period_history'");
if ($check_table->num_rows > 0) {
    echo "✅ Tabelle existiert in der Datenbank\n\n";
    
    // Zeige Tabellen-Struktur
    echo "📊 Tabellen-Struktur:\n";
    echo str_repeat("-", 80) . "\n";
    
    $describe = $mysqli->query("DESCRIBE test_period_history");
    if ($describe) {
        printf("%-20s %-25s %-10s %-10s %-10s\n", "Field", "Type", "Null", "Key", "Default");
        echo str_repeat("-", 80) . "\n";
        
        while ($row = $describe->fetch_assoc()) {
            printf("%-20s %-25s %-10s %-10s %-10s\n", 
                $row['Field'], 
                $row['Type'], 
                $row['Null'], 
                $row['Key'], 
                $row['Default'] ?? 'NULL'
            );
        }
    }
    
    echo "\n";
    
    // Zeige Anzahl der Einträge
    $count_result = $mysqli->query("SELECT COUNT(*) as total FROM test_period_history");
    if ($count_result) {
        $count = $count_result->fetch_assoc();
        echo "📈 Anzahl Einträge: " . $count['total'] . "\n\n";
    }
    
    // Zeige letzte 5 Einträge (falls vorhanden)
    $recent_result = $mysqli->query("
        SELECT account_name, program_name, program_version, 
               first_test_date, account_type, test_count
        FROM test_period_history
        ORDER BY first_test_date DESC
        LIMIT 5
    ");
    
    if ($recent_result && $recent_result->num_rows > 0) {
        echo "📋 Letzte Testzeiträume:\n";
        echo str_repeat("-", 100) . "\n";
        printf("%-25s %-15s %-10s %-20s %-10s %-10s\n", 
            "Account", "Program", "Version", "Start", "Type", "Count");
        echo str_repeat("-", 100) . "\n";
        
        while ($row = $recent_result->fetch_assoc()) {
            printf("%-25s %-15s %-10s %-20s %-10s %-10s\n",
                substr($row['account_name'], 0, 24),
                $row['program_name'],
                $row['program_version'],
                $row['first_test_date'],
                $row['account_type'] ?? 'N/A',
                $row['test_count']
            );
        }
    } else {
        echo "ℹ️ Noch keine Testzeiträume registriert\n";
    }
    
    echo "\n" . str_repeat("=", 80) . "\n";
    echo "✅ Setup erfolgreich abgeschlossen!\n\n";
    echo "Nächste Schritte:\n";
    echo "1. Integration der Testzeitraum-Logik in check.php\n";
    echo "2. EA sendet account_name, program_name und version\n";
    echo "3. Dashboard-Interface für Verwaltung erstellen\n";
    
    // Test-Eintrag Option
    echo "\n" . str_repeat("=", 80) . "\n";
    echo "Test-Eintrag hinzufügen?\n";
    echo '<a href="?action=add_test">Klicke hier um einen Test-Eintrag zu erstellen</a>' . "\n";
    
    // Test-Eintrag hinzufügen wenn angefordert
    if (isset($_GET['action']) && $_GET['action'] == 'add_test') {
        $test_sql = "INSERT INTO test_period_history 
                    (account_name, program_name, program_version, first_test_date, account_type, account_number)
                    VALUES ('Test User', 'the_don', '1.25', NOW(), 'DEMO', '99999999')
                    ON DUPLICATE KEY UPDATE test_count = test_count + 1";
        
        if ($mysqli->query($test_sql)) {
            echo "\n✅ Test-Eintrag erfolgreich hinzugefügt!\n";
        } else {
            echo "\nℹ️ Test-Eintrag existiert bereits oder Fehler: " . $mysqli->error . "\n";
        }
    }
    
} else {
    echo "❌ Tabelle wurde nicht gefunden!\n";
}

echo "</pre>";

// Verbindung schließen
$mysqli->close();

// Security: Lösche dieses Script nach Ausführung
echo '<hr>';
echo '<p style="color: red;">⚠️ SICHERHEITSHINWEIS: Dieses Script sollte nach erfolgreicher Ausführung gelöscht werden!</p>';
echo '<form method="post">';
echo '<input type="submit" name="delete_script" value="Script jetzt löschen" style="background: red; color: white; padding: 10px;">';
echo '</form>';

if (isset($_POST['delete_script'])) {
    if (unlink(__FILE__)) {
        echo '<p style="color: green;">✅ Script wurde gelöscht!</p>';
    } else {
        echo '<p style="color: red;">❌ Script konnte nicht gelöscht werden. Bitte manuell löschen!</p>';
    }
}
?>