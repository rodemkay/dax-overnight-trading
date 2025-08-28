"""
Test-Script für API-Debugging
Testet die PHP-API Schritt für Schritt
"""

import requests
import json

def test_api():
    """Testet die API-Funktionalität"""
    
    print("=" * 60)
    print("API DEBUG TEST")
    print("=" * 60)
    
    # Test 1: Ohne Token
    print("\n1. Test ohne Token:")
    url = "https://lic.prophelper.org/api/test_api.php"
    
    try:
        response = requests.post(url, json={})
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print(f"Fehler: {response.text}")
    except Exception as e:
        print(f"Fehler: {e}")
    
    # Test 2: Mit Token
    print("\n2. Test mit Token:")
    data = {'token': '250277100311270613'}
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print(f"Fehler: {response.text}")
    except Exception as e:
        print(f"Fehler: {e}")
    
    # Test 3: Haupt-API testen
    print("\n3. Test der Haupt-API (db_api.php):")
    main_url = "https://lic.prophelper.org/api/db_api.php"
    test_data = {
        'token': '250277100311270613',
        'action': 'test'
    }
    
    try:
        response = requests.post(main_url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")  # Erste 500 Zeichen
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    test_api()
