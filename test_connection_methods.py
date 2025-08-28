"""
Test verschiedene Verbindungsmethoden zur API
"""

import requests
import json
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# SSL-Warnungen unterdrücken für Tests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_connections():
    """Testet verschiedene Verbindungsmethoden"""
    
    print("=" * 60)
    print("API VERBINDUNGSTEST - VERSCHIEDENE METHODEN")
    print("=" * 60)
    
    base_url = "https://lic.prophelper.org/api/"
    token = "250277100311270613"
    
    # Test 1: GET Request
    print("\n1. GET Request (simple_test.php):")
    print("-" * 40)
    try:
        response = requests.get(base_url + "simple_test.php", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Erste 200 Zeichen: {response.text[:200]}...")
    except Exception as e:
        print(f"Fehler: {e}")
    
    # Test 2: POST mit verschiedenen Content-Types
    print("\n2. POST mit application/json:")
    print("-" * 40)
    try:
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'token': token})
        response = requests.post(base_url + "simple_test.php", 
                                data=data, 
                                headers=headers,
                                timeout=10)
        print(f"Status: {response.status_code}")
        print(response.text[:300])
    except Exception as e:
        print(f"Fehler: {e}")
    
    # Test 3: POST mit Form-Data
    print("\n3. POST mit application/x-www-form-urlencoded:")
    print("-" * 40)
    try:
        data = {'token': token}
        response = requests.post(base_url + "simple_test.php",
                                data=data,
                                timeout=10)
        print(f"Status: {response.status_code}")
        print(response.text[:300])
    except Exception as e:
        print(f"Fehler: {e}")
    
    # Test 4: POST ohne SSL-Verifikation
    print("\n4. POST ohne SSL-Verifikation:")
    print("-" * 40)
    try:
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'token': token, 'action': 'test'})
        response = requests.post(base_url + "db_api.php",
                                data=data,
                                headers=headers,
                                verify=False,
                                timeout=10)
        print(f"Status: {response.status_code}")
        print(response.text[:300])
    except Exception as e:
        print(f"Fehler: {e}")
    
    # Test 5: Mit Session und Retry-Strategie
    print("\n5. Mit Session und Retry-Strategie:")
    print("-" * 40)
    try:
        session = requests.Session()
        retry = Retry(
            total=3,
            read=3,
            connect=3,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 503, 504)
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'token': token, 'action': 'test'})
        
        response = session.post(base_url + "db_api.php",
                               data=data,
                               headers=headers,
                               verify=False,
                               timeout=10)
        print(f"Status: {response.status_code}")
        print(response.text[:300])
    except Exception as e:
        print(f"Fehler: {e}")
    
    # Test 6: Direkter Test der db_api.php mit minimalem Request
    print("\n6. Minimaler Test db_api.php:")
    print("-" * 40)
    try:
        # Nur Token senden, action sollte default sein
        simple_data = {'token': token}
        response = requests.post(base_url + "db_api.php",
                                json=simple_data,
                                verify=False,
                                timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Response:")
            print(response.text)
        else:
            print(f"Fehler-Response: {response.text[:500]}")
    except Exception as e:
        print(f"Fehler: {e}")
    
    print("\n" + "=" * 60)
    print("TESTS ABGESCHLOSSEN")
    print("=" * 60)

if __name__ == "__main__":
    test_connections()
