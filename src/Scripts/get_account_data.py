"""
Ruft alle Daten für einen spezifischen Account ab
"""

import urllib.request
import ssl
import json
from pprint import pprint

def get_account_data(account_number):
    """Ruft alle Daten für einen Account aus der Datenbank ab"""
    
    print("=" * 70)
    print(f"📊 DATEN FÜR ACCOUNT {account_number}")
    print("=" * 70)
    
    # API-Konfiguration
    api_url = "https://lic.prophelper.org/api/db_api.php"
    token = "250277100311270613"
    
    # SSL-Kontext ohne Verifikation
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # Query vorbereiten
    query = f"SELECT * FROM lnative WHERE account = '{account_number}'"
    
    request_data = {
        'token': token,
        'action': 'query',
        'query': query
    }
    
    try:
        print(f"\n🔍 Suche nach Account: {account_number}")
        print(f"📡 Sende Anfrage an: {api_url}")
        print(f"📝 SQL-Query: {query}\n")
        
        # Request senden
        data = json.dumps(request_data).encode('utf-8')
        req = urllib.request.Request(
            api_url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            }
        )
        
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            result = json.loads(response.read().decode())
            
            if result.get('status') == 'success':
                data = result.get('data', [])
                count = result.get('count', 0)
                
                print("=" * 70)
                if count > 0:
                    print(f"✅ {count} EINTRAG/EINTRÄGE GEFUNDEN")
                    print("=" * 70)
                    
                    for i, entry in enumerate(data, 1):
                        print(f"\n📌 Eintrag {i}:")
                        print("-" * 40)
                        
                        # Alle Felder anzeigen
                        for key, value in entry.items():
                            # Formatierte Ausgabe
                            if value is None:
                                value = "NULL"
                            elif value == "":
                                value = "(leer)"
                            
                            print(f"  {key:20} : {value}")
                        
                        print("-" * 40)
                else:
                    print("❌ KEIN EINTRAG GEFUNDEN")
                    print("=" * 70)
                    print(f"\nKein Account mit der Nummer '{account_number}' in der Datenbank.")
                
                # Zusätzliche Informationen
                print("\n" + "=" * 70)
                print("📊 WEITERE INFORMATIONEN")
                print("=" * 70)
                
                # Prüfe ob Account existiert (auch mit anderen Status)
                query2 = f"SELECT account, status, add_date FROM lnative WHERE account LIKE '%{account_number[-4:]}%'"
                request_data2 = {
                    'token': token,
                    'action': 'query',
                    'query': query2
                }
                
                data2 = json.dumps(request_data2).encode('utf-8')
                req2 = urllib.request.Request(
                    api_url,
                    data=data2,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'Mozilla/5.0'
                    }
                )
                
                with urllib.request.urlopen(req2, context=ctx, timeout=10) as response2:
                    result2 = json.loads(response2.read().decode())
                    
                    if result2.get('status') == 'success':
                        similar = result2.get('data', [])
                        if similar and len(similar) > 0:
                            print(f"\n💡 Ähnliche Accounts (letzte 4 Ziffern: {account_number[-4:]}):")
                            for acc in similar:
                                print(f"   • Account: {acc.get('account', 'N/A'):15} Status: {acc.get('status', 'N/A'):10} Datum: {acc.get('add_date', 'N/A')}")
                
                # Alle verfügbaren Accounts anzeigen
                print("\n" + "=" * 70)
                print("📋 ALLE VERFÜGBAREN ACCOUNTS (Top 10)")
                print("=" * 70)
                
                query3 = "SELECT account, add_date, registrar FROM lnative ORDER BY id DESC LIMIT 10"
                request_data3 = {
                    'token': token,
                    'action': 'query',
                    'query': query3
                }
                
                data3 = json.dumps(request_data3).encode('utf-8')
                req3 = urllib.request.Request(
                    api_url,
                    data=data3,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'Mozilla/5.0'
                    }
                )
                
                with urllib.request.urlopen(req3, context=ctx, timeout=10) as response3:
                    result3 = json.loads(response3.read().decode())
                    
                    if result3.get('status') == 'success':
                        all_accounts = result3.get('data', [])
                        if all_accounts:
                            for acc in all_accounts:
                                print(f"• Account: {acc.get('account', 'N/A'):15} Datum: {acc.get('add_date', 'N/A'):20} Registrar: {acc.get('registrar', 'N/A')}")
                
            else:
                print(f"❌ Fehler: {result.get('message', 'Unbekannter Fehler')}")
                
    except Exception as e:
        print(f"❌ Verbindungsfehler: {e}")

if __name__ == "__main__":
    # Account 77022300 abrufen
    get_account_data("77022300")
