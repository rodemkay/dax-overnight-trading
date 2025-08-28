import mysql.connector
from mysql.connector import Error

def test_database_connection():
    """Test connection to the prophelp database"""
    
    connection = None
    try:
        # Database configuration from server_credentials.txt
        connection = mysql.connector.connect(
            host='162.55.90.123',
            database='prophelp_users_1',
            user='prophelp_adm',
            password='mW0uG1pG9b',
            port=3306
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✅ Erfolgreich mit MySQL Server verbunden, Version: {db_info}")
            
            # Get database name
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"✅ Verbunden mit Datenbank: {record[0]}")
            
            # Test query - list tables
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print(f"\n📊 Gefundene Tabellen ({len(tables)} insgesamt):")
            for table in tables[:10]:  # Show first 10 tables
                print(f"   - {table[0]}")
            if len(tables) > 10:
                print(f"   ... und {len(tables) - 10} weitere Tabellen")
            
            # Check for license table
            cursor.execute("SHOW TABLES LIKE '%native%';")
            native_tables = cursor.fetchall()
            if native_tables:
                print(f"\n🔑 Lizenz-Tabellen gefunden:")
                for table in native_tables:
                    print(f"   - {table[0]}")
                    
            cursor.close()
            return True
            
    except Error as e:
        print(f"❌ Fehler bei der Datenbankverbindung: {e}")
        return False
        
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\n✅ Datenbankverbindung geschlossen")

if __name__ == "__main__":
    print("=== Test der Datenbankverbindung zu prophelp_users_1 ===\n")
    test_database_connection()
