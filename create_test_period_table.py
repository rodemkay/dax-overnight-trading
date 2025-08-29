#!/usr/bin/env python3
"""
Erstellt die test_period_history Tabelle in der prophelp_users_1 Datenbank
für das Testzeitraum-Management System
"""

import pymysql
import sys
from datetime import datetime

# Datenbank-Verbindungsdaten
DB_CONFIG = {
    'host': 'localhost',  # Verwende SSH-Tunnel oder direkte Server-Verbindung
    'user': 'prophelp_adm',
    'password': 'mW0uG1pG9b',
    'database': 'prophelp_users_1',
    'charset': 'utf8mb4',
    'port': 3306
}

def create_connection():
    """Erstellt Verbindung zur MySQL-Datenbank"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print(f"✓ Verbindung zur Datenbank {DB_CONFIG['database']} hergestellt")
        return connection
    except Exception as e:
        print(f"✗ Fehler bei Datenbankverbindung: {e}")
        sys.exit(1)

def create_test_period_table(connection):
    """Erstellt die test_period_history Tabelle"""
    
    create_table_sql = """
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
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_sql)
            connection.commit()
            print("✓ Tabelle test_period_history erfolgreich erstellt/aktualisiert")
            
            # Prüfe ob Tabelle existiert
            cursor.execute("SHOW TABLES LIKE 'test_period_history'")
            if cursor.fetchone():
                print("✓ Tabelle existiert und ist bereit")
                
                # Zeige Tabellen-Struktur
                cursor.execute("DESCRIBE test_period_history")
                columns = cursor.fetchall()
                print("\nTabellen-Struktur:")
                print("-" * 50)
                for col in columns:
                    print(f"  {col[0]:20} {col[1]:20}")
                    
            return True
            
    except Exception as e:
        print(f"✗ Fehler beim Erstellen der Tabelle: {e}")
        return False

def check_existing_data(connection):
    """Prüft ob bereits Daten in der Tabelle vorhanden sind"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM test_period_history")
            result = cursor.fetchone()
            count = result[0] if result else 0
            
            if count > 0:
                print(f"\n📊 Tabelle enthält bereits {count} Einträge")
                
                # Zeige die letzten 5 Einträge
                cursor.execute("""
                    SELECT account_name, program_name, program_version, 
                           first_test_date, account_type
                    FROM test_period_history
                    ORDER BY first_test_date DESC
                    LIMIT 5
                """)
                recent = cursor.fetchall()
                
                if recent:
                    print("\nLetzte Testzeiträume:")
                    print("-" * 80)
                    for row in recent:
                        print(f"  {row[0]:20} | {row[1]:15} | v{row[2]:5} | {row[3]} | {row[4] or 'N/A'}")
            else:
                print("\n📊 Tabelle ist leer (keine Testzeiträume registriert)")
                
    except Exception as e:
        print(f"✗ Fehler beim Prüfen der Daten: {e}")

def add_test_entry(connection):
    """Fügt einen Test-Eintrag hinzu (optional)"""
    response = input("\nMöchtest du einen Test-Eintrag hinzufügen? (j/n): ")
    
    if response.lower() == 'j':
        try:
            with connection.cursor() as cursor:
                test_sql = """
                INSERT INTO test_period_history 
                (account_name, program_name, program_version, first_test_date, account_type, account_number)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                test_data = (
                    'Test User',
                    'the_don',
                    '1.25',
                    datetime.now(),
                    'DEMO',
                    '99999999'
                )
                
                cursor.execute(test_sql, test_data)
                connection.commit()
                print("✓ Test-Eintrag erfolgreich hinzugefügt")
                
        except pymysql.err.IntegrityError:
            print("ℹ Test-Eintrag existiert bereits (Duplikat)")
        except Exception as e:
            print(f"✗ Fehler beim Hinzufügen: {e}")

def main():
    """Hauptfunktion"""
    print("=" * 50)
    print("Test Period History - Tabellen-Setup")
    print("=" * 50)
    
    # Verbindung herstellen
    connection = create_connection()
    
    try:
        # Tabelle erstellen
        if create_test_period_table(connection):
            # Vorhandene Daten prüfen
            check_existing_data(connection)
            
            # Optional: Test-Eintrag hinzufügen
            add_test_entry(connection)
            
        print("\n✅ Setup abgeschlossen!")
        print("\nDie Tabelle ist bereit für die Integration in check.php")
        print("Nächste Schritte:")
        print("1. check.php mit Testzeitraum-Logik erweitern")
        print("2. EA testet automatisch beim Start")
        print("3. Dashboard-Integration für Verwaltung")
        
    finally:
        connection.close()
        print("\n✓ Datenbankverbindung geschlossen")

if __name__ == "__main__":
    main()