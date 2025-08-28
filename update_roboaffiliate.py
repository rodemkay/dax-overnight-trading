#!/usr/bin/env python3
"""
Update RoboAffiliate Status
Aktualisiert den roboaffiliate Status für alle Accounts in der Datenbank
"""

import mysql.connector
import requests
import time
from datetime import datetime

# MySQL Configuration
DB_HOST = "162.55.90.123"
DB_USER = "prophelper"
DB_PASS = ".Propt333doka?"
DB_NAME = "prophelper"
DB_TABLE = "lnative"

# RoboForex API Configuration
PARTNER_ACCOUNT = "30218520"
API_KEY = "ec4d40c4343ee741"
AFFILIATE_CODE = "qnyj"

def connect_database():
    """Verbindung zur MySQL Datenbank herstellen"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as e:
        print(f"✗ Database connection failed: {e}")
        return None

def check_roboforex_partner(account_number):
    """Prüft ob ein Account ein Partner-Account ist"""
    url = f"https://my.roboforex.com/api/affiliate/check-partner/{PARTNER_ACCOUNT}"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY
    }
    
    data = {
        "account": str(account_number),
        "affiliate_code": AFFILIATE_CODE
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            is_partner = result.get('is_partner', False)
            return 'yes' if is_partner else 'no'
        else:
            return 'error'
            
    except Exception as e:
        print(f"  ⚠ API Error for {account_number}: {e}")
        return 'error'

def update_roboaffiliate_status(conn, account_id, account_number, status):
    """Update roboaffiliate Status in der Datenbank"""
    cursor = conn.cursor()
    
    try:
        query = f"UPDATE {DB_TABLE} SET roboaffiliate = %s WHERE id = %s"
        cursor.execute(query, (status, account_id))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"  ✗ Update failed for ID {account_id}: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def ensure_roboaffiliate_column(conn):
    """Stelle sicher dass die roboaffiliate Spalte existiert"""
    cursor = conn.cursor()
    
    try:
        # Prüfe ob Spalte existiert
        cursor.execute(f"SHOW COLUMNS FROM {DB_TABLE} LIKE 'roboaffiliate'")
        result = cursor.fetchone()
        
        if not result:
            print("Creating roboaffiliate column...")
            cursor.execute(f"""
                ALTER TABLE {DB_TABLE} 
                ADD COLUMN roboaffiliate VARCHAR(10) DEFAULT 'no'
            """)
            conn.commit()
            print("✓ Column created successfully")
        else:
            print("✓ roboaffiliate column already exists")
            
    except mysql.connector.Error as e:
        print(f"✗ Error checking/creating column: {e}")
        conn.rollback()
    finally:
        cursor.close()

def update_all_accounts(filter_program=None, limit=None):
    """
    Aktualisiert roboaffiliate Status für alle Accounts
    
    Args:
        filter_program: Nur bestimmtes Programm updaten (z.B. 'don_gpt')
        limit: Maximale Anzahl von Updates
    """
    print("=== RoboAffiliate Status Update ===\n")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    conn = connect_database()
    if not conn:
        return
    
    # Stelle sicher dass Spalte existiert
    ensure_roboaffiliate_column(conn)
    
    cursor = conn.cursor(dictionary=True)
    
    # Query alle Accounts
    query = f"SELECT id, accountLogin, account, program, full_name, roboaffiliate FROM {DB_TABLE}"
    
    if filter_program:
        query += f" WHERE program = '{filter_program}'"
    
    query += " ORDER BY id DESC"
    
    if limit:
        query += f" LIMIT {limit}"
    
    try:
        cursor.execute(query)
        accounts = cursor.fetchall()
        
        print(f"\nFound {len(accounts)} accounts to check")
        print("-" * 50)
        
        stats = {
            'total': len(accounts),
            'updated': 0,
            'partners': 0,
            'non_partners': 0,
            'errors': 0,
            'skipped': 0
        }
        
        for i, acc in enumerate(accounts, 1):
            account_id = acc['id']
            account_number = acc.get('accountLogin') or acc.get('account')
            name = acc.get('full_name', 'Unknown')[:30]
            program = acc.get('program', 'Unknown')
            current_status = acc.get('roboaffiliate', 'unknown')
            
            if not account_number:
                print(f"{i}/{stats['total']}: ID {account_id} ({name}) - No account number")
                stats['skipped'] += 1
                continue
            
            print(f"{i}/{stats['total']}: Checking {account_number} ({name}, {program})", end='')
            
            # Prüfe RoboForex Status
            new_status = check_roboforex_partner(account_number)
            
            if new_status == 'error':
                print(" → Error")
                stats['errors'] += 1
            else:
                # Update nur wenn sich Status geändert hat
                if current_status != new_status:
                    if update_roboaffiliate_status(conn, account_id, account_number, new_status):
                        print(f" → Updated: {current_status} → {new_status}")
                        stats['updated'] += 1
                    else:
                        print(" → Update failed")
                        stats['errors'] += 1
                else:
                    print(f" → No change ({new_status})")
                
                if new_status == 'yes':
                    stats['partners'] += 1
                else:
                    stats['non_partners'] += 1
            
            # Rate limiting (0.5 Sekunden zwischen Requests)
            time.sleep(0.5)
        
        # Summary
        print("\n" + "=" * 50)
        print("UPDATE SUMMARY:")
        print(f"Total accounts checked: {stats['total']}")
        print(f"Updated: {stats['updated']}")
        print(f"Partners: {stats['partners']}")
        print(f"Non-Partners: {stats['non_partners']}")
        print(f"Errors: {stats['errors']}")
        print(f"Skipped: {stats['skipped']}")
        print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except mysql.connector.Error as e:
        print(f"\n✗ Database error: {e}")
    finally:
        cursor.close()
        conn.close()
        print("\n✓ Database connection closed")

def update_single_account(account_number):
    """Update einzelnen Account"""
    print(f"=== Single Account Update: {account_number} ===\n")
    
    conn = connect_database()
    if not conn:
        return
    
    ensure_roboaffiliate_column(conn)
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Finde Account in DB
        query = f"""
            SELECT id, accountLogin, account, program, full_name, roboaffiliate 
            FROM {DB_TABLE} 
            WHERE accountLogin = %s OR account = %s
        """
        cursor.execute(query, (account_number, account_number))
        result = cursor.fetchone()
        
        if not result:
            print(f"✗ Account {account_number} not found in database")
            return
        
        print(f"Found: {result['full_name']} (ID: {result['id']})")
        print(f"Program: {result['program']}")
        print(f"Current status: {result.get('roboaffiliate', 'unknown')}")
        
        # Check RoboForex
        print(f"\nChecking RoboForex API...")
        new_status = check_roboforex_partner(account_number)
        
        if new_status == 'error':
            print("✗ API check failed")
        else:
            print(f"RoboForex Status: {new_status}")
            
            # Update
            if update_roboaffiliate_status(conn, result['id'], account_number, new_status):
                print(f"✓ Database updated successfully")
            else:
                print("✗ Database update failed")
                
    except mysql.connector.Error as e:
        print(f"✗ Database error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--single' and len(sys.argv) > 2:
            # Update einzelnen Account
            update_single_account(sys.argv[2])
        elif sys.argv[1] == '--program' and len(sys.argv) > 2:
            # Update nur bestimmtes Programm
            update_all_accounts(filter_program=sys.argv[2])
        elif sys.argv[1] == '--limit' and len(sys.argv) > 2:
            # Update mit Limit
            update_all_accounts(limit=int(sys.argv[2]))
        else:
            print("Usage:")
            print("  python update_roboaffiliate.py          # Update all")
            print("  python update_roboaffiliate.py --single 10016882")
            print("  python update_roboaffiliate.py --program don_gpt")
            print("  python update_roboaffiliate.py --limit 10")
    else:
        # Update alle Accounts
        update_all_accounts()