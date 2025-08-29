#!/usr/bin/env python3
"""
Remote-Script zum Erstellen der test_period_history Tabelle
Dieses Script wird direkt auf dem Server ausgeführt
"""

import os
import sys

# MySQL-Befehle als String
SQL_COMMANDS = """
-- Wechsel zur Datenbank
USE prophelp_users_1;

-- Erstelle Tabelle falls nicht vorhanden
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Testzeitraum-Historie für EA Lizenzsystem';

-- Prüfe ob Tabelle erstellt wurde
SHOW TABLES LIKE 'test_period_history';

-- Zeige Struktur
DESCRIBE test_period_history;

-- Zeige Anzahl der Einträge
SELECT COUNT(*) as total_entries FROM test_period_history;
"""

# Schreibe SQL in temporäre Datei
with open('/tmp/create_test_period_table.sql', 'w') as f:
    f.write(SQL_COMMANDS)

# Führe MySQL-Befehle aus
mysql_cmd = 'mysql -u prophelp_adm -pmW0uG1pG9b prophelp_users_1 < /tmp/create_test_period_table.sql'
result = os.system(mysql_cmd)

if result == 0:
    print("✅ Tabelle test_period_history erfolgreich erstellt!")
    print("\nTabellen-Struktur:")
    
    # Zeige Tabellen-Info
    check_cmd = """mysql -u prophelp_adm -pmW0uG1pG9b prophelp_users_1 -e "
    SELECT 'Tabelle existiert:' as Status;
    SHOW TABLES LIKE 'test_period_history';
    SELECT '---' as '';
    SELECT 'Anzahl Einträge:' as Info;
    SELECT COUNT(*) as Entries FROM test_period_history;
    " """
    os.system(check_cmd)
else:
    print("❌ Fehler beim Erstellen der Tabelle")
    sys.exit(1)

# Aufräumen
os.remove('/tmp/create_test_period_table.sql')
print("\n✓ Setup abgeschlossen!")