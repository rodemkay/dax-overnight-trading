#!/usr/bin/env python3
"""
Prüft und erstellt die demo_expires Spalte in der lnative Tabelle
"""

import mysql.connector
from datetime import datetime

# MySQL Verbindung
db_config = {
    'host': 'localhost',
    'user': 'prophelp_adm', 
    'password': 'mW0uG1pG9b',
    'database': 'prophelp_users_1'
}

def check_and_create_demo_column():
    """Prüft ob demo_expires Spalte existiert und erstellt sie bei Bedarf"""
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Prüfe ob Spalte existiert
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'prophelp_users_1' 
            AND TABLE_NAME = 'lnative'
            AND COLUMN_NAME = 'demo_expires'
        """)
        
        if cursor.fetchone():
            print("✓ demo_expires Spalte existiert bereits")
        else:
            print("→ demo_expires Spalte fehlt, wird erstellt...")
            
            # Spalte hinzufügen
            cursor.execute("""
                ALTER TABLE lnative 
                ADD COLUMN demo_expires DATE NULL DEFAULT NULL 
                COMMENT 'Demo-Ablaufdatum für Nutzer+Programm Kombination'
            """)
            conn.commit()
            print("✓ demo_expires Spalte erfolgreich erstellt")
        
        # Prüfe ob program Spalte existiert  
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'prophelp_users_1' 
            AND TABLE_NAME = 'lnative'
            AND COLUMN_NAME = 'program'
        """)
        
        if cursor.fetchone():
            print("✓ program Spalte existiert bereits")
        else:
            print("→ program Spalte fehlt, wird erstellt...")
            
            # Spalte hinzufügen
            cursor.execute("""
                ALTER TABLE lnative 
                ADD COLUMN program VARCHAR(50) NULL DEFAULT NULL 
                COMMENT 'Programmname für Demo-Zeitraum Tracking'
            """)
            conn.commit()
            print("✓ program Spalte erfolgreich erstellt")
            
        # Zeige aktuelle Struktur
        cursor.execute("DESCRIBE lnative")
        columns = cursor.fetchall()
        
        print("\nAktuelle lnative Struktur:")
        print("-" * 50)
        for col in columns:
            if col[0] in ['full_name', 'account', 'program', 'demo_expires', 'roboaffiliate', 'test', 'payment']:
                print(f"  {col[0]:20} {col[1]:20} {col[2] or 'NOT NULL':10}")
        
        # Zeige Demo-Einträge falls vorhanden
        cursor.execute("""
            SELECT account, full_name, program, demo_expires, roboaffiliate
            FROM lnative 
            WHERE demo_expires IS NOT NULL OR program IS NOT NULL
            LIMIT 5
        """)
        
        results = cursor.fetchall()
        if results:
            print("\nBeispiel Demo-Einträge:")
            print("-" * 50)
            for row in results:
                print(f"  Account: {row[0]}, Name: {row[1]}, Program: {row[2]}, Expires: {row[3]}, RoboAffiliate: {row[4]}")
        else:
            print("\nNoch keine Demo-Einträge vorhanden")
            
    except mysql.connector.Error as err:
        print(f"✗ MySQL Fehler: {err}")
        return False
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            
    return True

if __name__ == "__main__":
    print("=== Demo-Spalten Prüfung ===")
    print(f"Zeitstempel: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    if check_and_create_demo_column():
        print("\n✓ Datenbank ist bereit für Demo-System")
    else:
        print("\n✗ Fehler bei Datenbank-Vorbereitung")