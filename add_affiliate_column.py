"""
Script zum Hinzufügen der affiliate_status Spalte zur Datenbank
=================================================================
"""

import urllib.request
import ssl
import json
from datetime import datetime

def execute_api_request(action, **kwargs):
    """Führt eine API-Anfrage aus"""
    api_url = "https://lic.prophelper.org/api/db_api.php"
    token = "250277100311270613"
    
    # SSL-Kontext ohne Verifikation
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # Request-Daten
    request_data = {
        'token': token,
        'action': action
    }
    request_data.update(kwargs)
    
    data = json.dumps(request_data).encode('utf-8')
    
    req = urllib.request.Request(
        api_url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            result = json.loads(response.read().decode())
            return result
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None

def main():
    print("=" * 70)
    print("📊 DATENBANK-ERWEITERUNG: Affiliate-Status")
    print("=" * 70)
    
    # 1. Prüfe aktuelle Tabellenstruktur
    print("\n1️⃣ Prüfe aktuelle Tabellenstruktur...")
    result = execute_api_request('describe', table='lnative')
    
    if result and result.get('status') == 'success':
        columns = result.get('data', [])
        column_names = [col.get('Field') for col in columns]
        
        print(f"✅ Tabelle hat {len(columns)} Spalten")
        
        # Prüfe ob affiliate_status bereits existiert
        if 'affiliate_status' in column_names:
            print("ℹ️ Spalte 'affiliate_status' existiert bereits!")
            
            # Zeige aktuelle Werte
            print("\n2️⃣ Prüfe aktuelle Affiliate-Status Werte...")
            query = "SELECT account, affiliate_status FROM lnative WHERE account IN ('77022300', '89211195') LIMIT 5"
            result = execute_api_request('query', query=query)
            
            if result and result.get('status') == 'success':
                data = result.get('data', [])
                if data:
                    print("📋 Aktuelle Status:")
                    for row in data:
                        print(f"   • Account {row.get('account')}: {row.get('affiliate_status', 'NULL')}")
                else:
                    print("   Keine Daten gefunden")
        else:
            print("ℹ️ Spalte 'affiliate_status' existiert noch nicht")
            
            # 2. Füge neue Spalte hinzu
            print("\n2️⃣ Füge Spalte 'affiliate_status' hinzu...")
            
            # ALTER TABLE Befehl
            alter_query = "ALTER TABLE lnative ADD COLUMN affiliate_status VARCHAR(10) DEFAULT 'unknown'"
            result = execute_api_request('query', query=alter_query)
            
            if result:
                if result.get('status') == 'success':
                    print("✅ Spalte erfolgreich hinzugefügt!")
                else:
                    # Möglicherweise existiert die Spalte bereits
                    error = result.get('message', '')
                    if 'Duplicate column name' in error:
                        print("ℹ️ Spalte existiert bereits")
                    else:
                        print(f"❌ Fehler: {error}")
            else:
                print("❌ Keine Antwort vom Server")
    
    # 3. Test: Update eines Accounts
    print("\n3️⃣ Test-Update für Account 77022300...")
    
    test_query = "UPDATE lnative SET affiliate_status = ? WHERE account = ?"
    test_params = ['test', '77022300']
    
    result = execute_api_request('query', query=test_query, params=test_params)
    
    if result and result.get('status') == 'success':
        affected = result.get('affected_rows', 0)
        if affected > 0:
            print(f"✅ {affected} Zeile(n) aktualisiert")
            
            # Verifiziere Update
            verify_query = "SELECT account, affiliate_status FROM lnative WHERE account = '77022300'"
            result = execute_api_request('query', query=verify_query)
            
            if result and result.get('status') == 'success':
                data = result.get('data', [])
                if data:
                    status = data[0].get('affiliate_status', 'NULL')
                    print(f"📋 Neuer Status für 77022300: {status}")
        else:
            print("⚠️ Keine Zeilen aktualisiert")
    
    print("\n" + "=" * 70)
    print("✅ DATENBANK-VORBEREITUNG ABGESCHLOSSEN")
    print("=" * 70)
    print("\nNächste Schritte:")
    print("1. API erweitern für update_affiliate_status")
    print("2. MQL5 Code anpassen")
    print("3. Webseite erstellen")

if __name__ == "__main__":
    main()
