"""
Test der API mit verschiedenen Methoden
"""

import subprocess
import json

def test_with_curl():
    """Testet die API direkt mit curl"""
    
    print("=" * 60)
    print("CURL API TEST")
    print("=" * 60)
    
    api_url = "https://lic.prophelper.org/api/db_api.php"
    token = "250277100311270613"
    
    # Test 1: Verbindungstest
    print("\n1. Verbindungstest mit curl:")
    print("-" * 40)
    
    data = json.dumps({
        'token': token,
        'action': 'test'
    })
    
    curl_cmd = [
        'curl',
        '-X', 'POST',
        '-H', 'Content-Type: application/json',
        '-d', data,
        '-k',  # Ignoriere SSL-Zertifikatfehler
        api_url
    ]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=10)
        print("Response:")
        print(result.stdout)
        if result.stderr:
            print("Fehler:", result.stderr)
    except Exception as e:
        print(f"Fehler: {e}")
    
    # Test 2: Tabellen abrufen
    print("\n2. Tabellen abrufen:")
    print("-" * 40)
    
    data = json.dumps({
        'token': token,
        'action': 'tables'
    })
    
    curl_cmd[6] = data  # Update data parameter
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=10)
        print("Response:")
        response_text = result.stdout[:500]  # Erste 500 Zeichen
        print(response_text)
    except Exception as e:
        print(f"Fehler: {e}")
    
    print("\n" + "=" * 60)
    print("Alternative: Nutzen Sie test_api.html im Browser!")
    print("=" * 60)

if __name__ == "__main__":
    test_with_curl()
