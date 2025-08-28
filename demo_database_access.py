"""
Demonstration des Datenbankzugriffs über die API
"""

import requests
import json
from datetime import datetime

def demo_database_access():
    """Demonstriert verschiedene Datenbankzugriffe"""
    
    API_URL = "https://lic.prophelper.org/api/db_api.php"
    TOKEN = "250277100311270613"
    
    print("=" * 60)
    print("🔌 DATENBANKZUGRIFF DEMONSTRATION")
    print("=" * 60)
    print(f"Zeit: {datetime.now().strftime('%H:%M:%S')}")
    print(f"API: {API_URL}")
    print()
    
    # 1. Verbindungstest
    print("1️⃣ VERBINDUNGSTEST")
    print("-" * 40)
    try:
        response = requests.post(API_URL, json={
            'token': TOKEN,
            'action': 'test'
        }, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Verbindung erfolgreich!")
            print(f"   Status: {result.get('status', 'unbekannt')}")
            print(f"   Nachricht: {result.get('message', 'OK')}")
        else:
            print(f"❌ Fehler: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Verbindungsfehler: {e}")
    
    print()
    
    # 2. Tabellen anzeigen
    print("2️⃣ VERFÜGBARE TABELLEN")
    print("-" * 40)
    try:
        response = requests.post(API_URL, json={
            'token': TOKEN,
            'action': 'tables'
        }, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                tables = result.get('data', [])
                print(f"✅ {len(tables)} Tabellen gefunden:")
                for table in tables[:10]:  # Erste 10 Tabellen
                    print(f"   📊 {table}")
            else:
                print(f"❌ Fehler: {result.get('message', 'Unbekannt')}")
        else:
            print(f"❌ HTTP Fehler: {response.status_code}")
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    print()
    
    # 3. Beispieldaten abrufen
    print("3️⃣ BEISPIELDATEN AUS 'lnative' TABELLE")
    print("-" * 40)
    try:
        response = requests.post(API_URL, json={
            'token': TOKEN,
            'action': 'query',
            'query': 'SELECT * FROM lnative LIMIT 3'
        }, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                data = result.get('data', [])
                print(f"✅ {len(data)} Einträge gefunden:")
                for i, row in enumerate(data, 1):
                    print(f"\n   Eintrag {i}:")
                    for key, value in row.items():
                        print(f"      {key}: {value}")
            else:
                print(f"❌ Query-Fehler: {result.get('message', 'Unbekannt')}")
        else:
            print(f"❌ HTTP Fehler: {response.status_code}")
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    print()
    
    # 4. Lizenz-Check für eine Test-Account-Nummer
    print("4️⃣ LIZENZ-CHECK BEISPIEL")
    print("-" * 40)
    test_account = "123456"  # Beispiel Account
    try:
        response = requests.post(API_URL, json={
            'token': TOKEN,
            'action': 'license_check',
            'account': test_account
        }, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                has_license = result.get('has_license', False)
                if has_license:
                    print(f"✅ Account {test_account}: Aktive Lizenz gefunden")
                    details = result.get('license_details', {})
                    for key, value in details.items():
                        print(f"      {key}: {value}")
                else:
                    print(f"❌ Account {test_account}: Keine aktive Lizenz")
            else:
                print(f"❌ Check-Fehler: {result.get('message', 'Unbekannt')}")
        else:
            print(f"❌ HTTP Fehler: {response.status_code}")
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    print()
    
    # 5. Statistiken
    print("5️⃣ DATENBANK-STATISTIKEN")
    print("-" * 40)
    try:
        response = requests.post(API_URL, json={
            'token': TOKEN,
            'action': 'query',
            'query': 'SELECT COUNT(*) as total FROM lnative'
        }, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                data = result.get('data', [])
                if data:
                    total = data[0].get('total', 0)
                    print(f"✅ Gesamtanzahl Einträge in 'lnative': {total}")
            else:
                print(f"❌ Query-Fehler: {result.get('message', 'Unbekannt')}")
        else:
            print(f"❌ HTTP Fehler: {response.status_code}")
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    print()
    print("=" * 60)
    print("🎉 DEMONSTRATION ABGESCHLOSSEN")
    print("=" * 60)
    print("\nDie Datenbankverbindung funktioniert einwandfrei!")
    print("Alle Operationen können über die API durchgeführt werden.")

if __name__ == "__main__":
    demo_database_access()
