#!/usr/bin/env python3
"""
Test-Script für RoboForex Affiliate Spalte
Prüft ob die roboaffiliate Spalte existiert und funktioniert
"""

import requests
import json
import sys

# API-Konfiguration
API_URL = "https://lic.prophelper.org/api/db_api.php"
TOKEN = "250277100311270613"

def test_get_all_data():
    """Hole alle Daten um zu prüfen ob roboaffiliate Spalte existiert"""
    print("\n=== Teste Datenbank-Abfrage ===")
    
    data = {
        "action": "get_all",
        "token": TOKEN
    }
    
    try:
        response = requests.post(API_URL, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                records = result.get("data", [])
                print(f"✓ {len(records)} Datensätze gefunden")
                
                # Prüfe ob roboaffiliate Spalte existiert
                if records:
                    first_record = records[0]
                    if 'roboaffiliate' in first_record:
                        print("✓ 'roboaffiliate' Spalte existiert in der Datenbank!")
                        
                        # Zeige Statistik
                        yes_count = sum(1 for r in records if r.get('roboaffiliate') == 'yes')
                        no_count = sum(1 for r in records if r.get('roboaffiliate') == 'no')
                        unknown_count = sum(1 for r in records if r.get('roboaffiliate') == 'unknown' or not r.get('roboaffiliate'))
                        
                        print(f"\nAffiliate-Statistik:")
                        print(f"  Yes: {yes_count}")
                        print(f"  No: {no_count}")
                        print(f"  Unknown: {unknown_count}")
                        
                        # Zeige erste 5 Einträge mit Affiliate-Status
                        print(f"\nBeispiel-Einträge:")
                        for i, record in enumerate(records[:5]):
                            account = record.get('account', 'N/A')
                            name = record.get('full_name', 'N/A')
                            status = record.get('roboaffiliate', 'unknown')
                            print(f"  {i+1}. Account {account} ({name}): {status}")
                    else:
                        print("✗ 'roboaffiliate' Spalte FEHLT in der Datenbank!")
                        print("  Bitte führe das SQL-Script 'add_roboaffiliate_complete.sql' aus")
                        return False
                else:
                    print("⚠ Keine Datensätze in der Datenbank")
            else:
                print(f"✗ API-Fehler: {result.get('error', 'Unbekannt')}")
                return False
                
        else:
            print(f"✗ HTTP-Fehler: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Fehler bei API-Aufruf: {str(e)}")
        return False
    
    return True

def test_update_affiliate(account_number="77022300", status="yes"):
    """Teste Update der Affiliate-Spalte"""
    print(f"\n=== Teste Affiliate-Update für Konto {account_number} ===")
    
    data = {
        "action": "update_affiliate",
        "token": TOKEN,
        "account": account_number,
        "affiliate_status": status
    }
    
    try:
        response = requests.post(API_URL, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                print(f"✓ Affiliate-Status erfolgreich auf '{status}' gesetzt")
                
                # Verifiziere Update
                verify_data = {
                    "action": "get_account",
                    "token": TOKEN,
                    "account": account_number
                }
                
                verify_response = requests.post(API_URL, json=verify_data, timeout=10)
                if verify_response.status_code == 200:
                    verify_result = verify_response.json()
                    if verify_result.get("success"):
                        account_data = verify_result.get("data", {})
                        actual_status = account_data.get("roboaffiliate", "unknown")
                        if actual_status == status:
                            print(f"✓ Verifikation erfolgreich: Status ist '{actual_status}'")
                        else:
                            print(f"✗ Verifikation fehlgeschlagen: Erwarte '{status}', gefunden '{actual_status}'")
            else:
                error_msg = result.get("error", "Unbekannt")
                if "Column 'roboaffiliate' doesn't exist" in error_msg:
                    print("✗ Die 'roboaffiliate' Spalte existiert nicht in der Datenbank!")
                    print("  Bitte führe das SQL-Script 'add_roboaffiliate_complete.sql' aus")
                else:
                    print(f"✗ API-Fehler: {error_msg}")
                return False
                
        else:
            print(f"✗ HTTP-Fehler: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Fehler bei API-Aufruf: {str(e)}")
        return False
    
    return True

def main():
    print("=" * 60)
    print("RoboForex Affiliate Spalten-Test")
    print("=" * 60)
    
    # Test 1: Prüfe ob Spalte existiert
    if not test_get_all_data():
        print("\n❌ Die roboaffiliate Spalte existiert nicht!")
        print("\nBitte führe folgendes SQL aus:")
        print("-" * 40)
        print("ALTER TABLE lnative ADD COLUMN roboaffiliate VARCHAR(10) DEFAULT 'unknown';")
        print("-" * 40)
        sys.exit(1)
    
    # Test 2: Teste Update (optional)
    print("\nMöchtest du einen Test-Update durchführen? (j/n): ", end="")
    answer = input().strip().lower()
    
    if answer == 'j':
        print("Account-Nummer eingeben (oder Enter für 77022300): ", end="")
        account = input().strip() or "77022300"
        
        print("Status (yes/no/unknown): ", end="")
        status = input().strip() or "yes"
        
        if status in ["yes", "no", "unknown"]:
            test_update_affiliate(account, status)
        else:
            print("Ungültiger Status. Nutze: yes, no oder unknown")
    
    print("\n" + "=" * 60)
    print("Test abgeschlossen")
    print("=" * 60)

if __name__ == "__main__":
    main()
