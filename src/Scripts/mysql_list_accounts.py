#!/usr/bin/env python3
"""
MySQL List Accounts
Listet alle Accounts aus der PropHelper Datenbank
"""

import mysql.connector
from datetime import datetime
import sys

# MySQL Configuration
DB_HOST = "162.55.90.123"
DB_USER = "prophelper"
DB_PASS = ".Propt333doka?"
DB_NAME = "prophelper"
DB_TABLE = "lnative"

def connect_database():
    """Verbindung zur MySQL Datenbank herstellen"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        print("✓ Connected to MySQL database")
        return conn
    except mysql.connector.Error as e:
        print(f"✗ Database connection failed: {e}")
        return None

def list_accounts(filter_program=None, show_roboaffiliate=False):
    """
    Liste alle Accounts aus der Datenbank
    
    Args:
        filter_program: Filtere nach Program Name (z.B. 'don_gpt')
        show_roboaffiliate: Zeige nur roboaffiliate Status
    """
    conn = connect_database()
    if not conn:
        return
    
    cursor = conn.cursor(dictionary=True)
    
    # SQL Query
    query = f"SELECT * FROM {DB_TABLE}"
    conditions = []
    
    if filter_program:
        conditions.append(f"program = '{filter_program}'")
    
    if show_roboaffiliate:
        conditions.append("roboaffiliate IS NOT NULL")
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY id DESC"
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        print(f"\n=== Account List ({len(results)} entries) ===\n")
        
        # Header
        print(f"{'ID':<6} {'Name':<20} {'Account':<12} {'Program':<15} {'RoboAffiliate':<15} {'Last Connect':<20}")
        print("-" * 100)
        
        # Data
        for row in results:
            account_id = row.get('id', '')
            name = row.get('full_name', '')[:20]
            account = row.get('accountLogin', row.get('account', ''))
            program = row.get('program', '')[:15]
            robo_status = row.get('roboaffiliate', 'unknown')
            last_connect = row.get('last_connect', 0)
            
            # Format last connect timestamp
            if last_connect:
                try:
                    last_date = datetime.fromtimestamp(last_connect).strftime('%Y-%m-%d %H:%M')
                except:
                    last_date = 'Invalid date'
            else:
                last_date = 'Never'
            
            # Format roboaffiliate status
            if robo_status == 'yes' or robo_status == '1':
                robo_display = "✓ Partner"
            elif robo_status == 'no' or robo_status == '0':
                robo_display = "✗ Not Partner"
            else:
                robo_display = "? Unknown"
            
            print(f"{account_id:<6} {name:<20} {account:<12} {program:<15} {robo_display:<15} {last_date:<20}")
        
        # Summary
        print("\n" + "=" * 100)
        print("SUMMARY:")
        print(f"Total accounts: {len(results)}")
        
        # Count by program
        programs = {}
        robo_yes = 0
        robo_no = 0
        robo_unknown = 0
        
        for row in results:
            prog = row.get('program', 'Unknown')
            programs[prog] = programs.get(prog, 0) + 1
            
            robo = row.get('roboaffiliate', '')
            if robo in ['yes', '1', 1]:
                robo_yes += 1
            elif robo in ['no', '0', 0]:
                robo_no += 1
            else:
                robo_unknown += 1
        
        print("\nBy Program:")
        for prog, count in sorted(programs.items()):
            print(f"  {prog}: {count}")
        
        print("\nRoboForex Partner Status:")
        print(f"  ✓ Partners: {robo_yes}")
        print(f"  ✗ Not Partners: {robo_no}")
        print(f"  ? Unknown: {robo_unknown}")
        
    except mysql.connector.Error as e:
        print(f"✗ Query failed: {e}")
    finally:
        cursor.close()
        conn.close()
        print("\n✓ Database connection closed")

def check_table_structure():
    """Prüfe die Tabellenstruktur und zeige verfügbare Spalten"""
    conn = connect_database()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"DESCRIBE {DB_TABLE}")
        columns = cursor.fetchall()
        
        print("\n=== Table Structure ===")
        print(f"Table: {DB_TABLE}")
        print("-" * 50)
        
        for col in columns:
            field = col[0]
            dtype = col[1]
            null = col[2]
            key = col[3]
            default = col[4]
            
            print(f"{field:<20} {dtype:<20} {'NULL' if null == 'YES' else 'NOT NULL':<10}")
            
            if field == 'roboaffiliate':
                print(f"  → RoboForex column found! ✓")
        
    except mysql.connector.Error as e:
        print(f"✗ Could not describe table: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("=== MySQL Account List Tool ===")
    
    # Prüfe Tabellenstruktur
    check_table_structure()
    
    # Liste alle Accounts
    print("\n1. Showing all accounts:")
    list_accounts()
    
    # Filtere nach don_gpt
    print("\n2. Showing only 'don_gpt' accounts:")
    list_accounts(filter_program='don_gpt')
    
    # Command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--robo':
            print("\n3. Showing only accounts with roboaffiliate data:")
            list_accounts(show_roboaffiliate=True)
        elif sys.argv[1] == '--program':
            if len(sys.argv) > 2:
                program = sys.argv[2]
                print(f"\n3. Showing accounts for program '{program}':")
                list_accounts(filter_program=program)