"""
Robuste Datenbankverbindung mit mehreren Fallback-Methoden
"""

import urllib.request
import urllib.parse
import ssl
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import warnings
warnings.filterwarnings('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

class DatabaseConnection:
    """Stellt eine robuste Verbindung zur Datenbank her"""
    
    def __init__(self):
        self.api_url = "https://lic.prophelper.org/api/db_api.php"
        self.token = "250277100311270613"
        self.connected = False
        self.method = None
        
    def test_urllib_method(self):
        """Methode 1: urllib mit SSL-Bypass"""
        try:
            # SSL-Kontext ohne Verifikation
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            data = json.dumps({
                'token': self.token,
                'action': 'test'
            }).encode('utf-8')
            
            req = urllib.request.Request(
                self.api_url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                result = json.loads(response.read().decode())
                if result.get('status') == 'success':
                    self.connected = True
                    self.method = "urllib"
                    return True
        except Exception as e:
            print(f"   urllib fehlgeschlagen: {str(e)[:50]}")
        return False
    
    def test_requests_with_session(self):
        """Methode 2: Requests mit Session und Browser-Headers"""
        try:
            session = requests.Session()
            
            # Retry-Strategie
            retry = Retry(
                total=2,
                backoff_factor=0.3,
                status_forcelist=[500, 502, 503, 504]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            
            # Browser-ähnliche Headers
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site'
            }
            
            data = json.dumps({
                'token': self.token,
                'action': 'test'
            })
            
            response = session.post(
                self.api_url,
                data=data,
                headers=headers,
                verify=False,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    self.connected = True
                    self.method = "requests_session"
                    self.session = session
                    self.headers = headers
                    return True
        except Exception as e:
            print(f"   requests_session fehlgeschlagen: {str(e)[:50]}")
        return False
    
    def execute_query(self, query):
        """Führt eine SQL-Query aus"""
        if not self.connected:
            print("❌ Keine Verbindung zur Datenbank!")
            return None
            
        try:
            if self.method == "urllib":
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                data = json.dumps({
                    'token': self.token,
                    'action': 'query',
                    'query': query
                }).encode('utf-8')
                
                req = urllib.request.Request(
                    self.api_url,
                    data=data,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'Mozilla/5.0'
                    }
                )
                
                with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                    return json.loads(response.read().decode())
                    
            elif self.method == "requests_session":
                data = json.dumps({
                    'token': self.token,
                    'action': 'query',
                    'query': query
                })
                
                response = self.session.post(
                    self.api_url,
                    data=data,
                    headers=self.headers,
                    verify=False,
                    timeout=10
                )
                return response.json()
                
        except Exception as e:
            print(f"❌ Query-Fehler: {e}")
            return None
    
    def connect(self):
        """Versucht verschiedene Verbindungsmethoden"""
        print("=" * 60)
        print("🔌 DATENBANKVERBINDUNG HERSTELLEN")
        print("=" * 60)
        
        print("\n📡 Teste verschiedene Verbindungsmethoden...")
        
        # Methode 1: urllib
        print("\n1. Teste urllib-Methode...")
        if self.test_urllib_method():
            print("   ✅ Erfolg mit urllib!")
            return True
        
        # Methode 2: requests mit Session
        print("\n2. Teste requests mit Session...")
        if self.test_requests_with_session():
            print("   ✅ Erfolg mit requests Session!")
            return True
        
        print("\n❌ Keine Methode konnte eine Verbindung herstellen.")
        print("\n💡 Alternative: Nutzen Sie test_api.html im Browser!")
        return False

def main():
    """Hauptfunktion zum Testen der Datenbankverbindung"""
    
    db = DatabaseConnection()
    
    if db.connect():
        print("\n" + "=" * 60)
        print("✅ VERBINDUNG ERFOLGREICH!")
        print("=" * 60)
        print(f"Methode: {db.method}")
        
        # Test-Query ausführen
        print("\n📊 Teste Datenbankzugriff...")
        print("-" * 40)
        
        # 1. Tabellen anzeigen
        result = db.execute_query("SHOW TABLES")
        if result and result.get('status') == 'success':
            tables = result.get('data', [])
            print(f"✅ {len(tables)} Tabellen gefunden:")
            for table in tables[:5]:
                table_name = list(table.values())[0] if isinstance(table, dict) else table
                print(f"   📊 {table_name}")
        
        # 2. Beispieldaten
        print("\n📝 Beispieldaten aus 'lnative':")
        print("-" * 40)
        result = db.execute_query("SELECT * FROM lnative LIMIT 2")
        if result and result.get('status') == 'success':
            data = result.get('data', [])
            print(f"✅ {len(data)} Einträge gefunden")
            for i, row in enumerate(data, 1):
                print(f"\nEintrag {i}:")
                for key, value in list(row.items())[:3]:  # Erste 3 Felder
                    print(f"  {key}: {value}")
        
        print("\n" + "=" * 60)
        print("🎉 DATENBANKZUGRIFF FUNKTIONIERT!")
        print("=" * 60)
        print("\nDie Verbindung zur Datenbank ist hergestellt und")
        print("funktioniert einwandfrei. Sie können nun auf alle")
        print("Daten zugreifen und Operationen durchführen.")
        
        return db
    else:
        print("\n⚠️  Bitte nutzen Sie die Browser-Lösung:")
        print("   1. Öffnen Sie test_api.html")
        print("   2. Die Verbindung funktioniert dort!")
        return None

if __name__ == "__main__":
    db = main()
