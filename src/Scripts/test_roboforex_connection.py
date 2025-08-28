#!/usr/bin/env python3
"""
Test RoboForex API Connection
Prüft ob ein Account ein Partner-Account ist
"""

import requests
import json

# RoboForex API Configuration
PARTNER_ACCOUNT = "30218520"
API_KEY = "ec4d40c4343ee741"
AFFILIATE_CODE = "qnyj"  # Hardcoded wie im EA

def check_roboforex_partner(account_number):
    """
    Prüft ob ein Account über unseren Partner-Link registriert wurde
    
    Args:
        account_number: MT5 Account Nummer
    
    Returns:
        'yes' wenn Partner, 'no' wenn nicht, 'error' bei Fehler
    """
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
        print(f"Checking account {account_number}...")
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            is_partner = result.get('is_partner', False)
            
            if is_partner:
                print(f"✓ Account {account_number} is a PARTNER account")
                return 'yes'
            else:
                print(f"✗ Account {account_number} is NOT a partner account")
                return 'no'
        else:
            print(f"⚠ API returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return 'error'
            
    except requests.exceptions.Timeout:
        print(f"⚠ Timeout while checking account {account_number}")
        return 'error'
    except requests.exceptions.RequestException as e:
        print(f"⚠ Error checking account {account_number}: {e}")
        return 'error'
    except Exception as e:
        print(f"⚠ Unexpected error: {e}")
        return 'error'

def test_api_connection():
    """Test die API-Verbindung mit verschiedenen Accounts"""
    print("=== RoboForex API Connection Test ===\n")
    print(f"Partner Account: {PARTNER_ACCOUNT}")
    print(f"API Key: {API_KEY[:10]}...")
    print(f"Affiliate Code: {AFFILIATE_CODE}")
    print("-" * 40)
    
    # Test-Accounts (aus der Dokumentation)
    test_accounts = [
        "10016882",  # DAX EA Account
        "77022300",  # Test Account aus Doku
        "12345678",  # Fake Account zum Testen
    ]
    
    results = {}
    for account in test_accounts:
        print(f"\nTesting account: {account}")
        status = check_roboforex_partner(account)
        results[account] = status
        print(f"Status: {status}")
    
    print("\n" + "=" * 40)
    print("SUMMARY:")
    print("-" * 40)
    for account, status in results.items():
        symbol = "✓" if status == "yes" else "✗" if status == "no" else "⚠"
        print(f"{symbol} {account}: {status}")
    
    # Test direkte API Verbindung
    print("\n" + "=" * 40)
    print("Testing direct API connection...")
    try:
        test_url = "https://my.roboforex.com/api/health"
        response = requests.get(test_url, timeout=5)
        if response.status_code == 200:
            print("✓ API is reachable")
        else:
            print(f"⚠ API returned status: {response.status_code}")
    except:
        print("✗ Could not reach API")

if __name__ == "__main__":
    test_api_connection()
    
    print("\n" + "=" * 40)
    print("You can also test individual accounts:")
    print("Example: python test_roboforex_connection.py 10016882")
    
    import sys
    if len(sys.argv) > 1:
        account = sys.argv[1]
        print(f"\nChecking account from command line: {account}")
        status = check_roboforex_partner(account)
        print(f"Result: {status}")