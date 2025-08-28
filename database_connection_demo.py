"""
Vollständige Datenbank-Demo für DAX Overnight EA
=================================================
Zeigt alle verfügbaren Datenbankfunktionen
"""

import urllib.request
import ssl
import json
from datetime import datetime
from typing import Optional, Dict, List, Any

class DatabaseManager:
    """Verwaltet die Datenbankverbindung und Operationen"""
    
    def __init__(self):
        self.api_url = "https://lic.prophelper.org/api/db_api.php"
        self.token = "250277100311270613"
        self.connected = False
        
    def _make_request(self, action: str, **kwargs) -> Optional[Dict]:
        """Führt eine API-Anfrage aus"""
        try:
            # SSL-Kontext ohne Verifikation
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            # Request-Daten vorbereiten
            request_data = {
                'token': self.token,
                'action': action
            }
            request_data.update(kwargs)
            
            data = json.dumps(request_data).encode('utf-8')
            
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
                return result
                
        except Exception as e:
            print(f"❌ API-Fehler: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Testet die Verbindung zur Datenbank"""
        result = self._make_request('test')
        if result and result.get('status') == 'success':
            self.connected = True
            return True
        return False
    
    def get_tables(self) -> List[str]:
        """Ruft alle Tabellen ab"""
        result = self._make_request('tables')
        if result and result.get('status') == 'success':
            return result.get('data', [])
        return []
    
    def describe_table(self, table_name: str) -> List[Dict]:
        """Zeigt die Struktur einer Tabelle"""
        result = self._make_request('describe', table=table_name)
        if result and result.get('status') == 'success':
            return result.get('data', [])
        return []
    
    def execute_query(self, query: str, params: List = None) -> Optional[Dict]:
        """Führt eine beliebige SQL-Query aus"""
        kwargs = {'query': query}
        if params:
            kwargs['params'] = params
        return self._make_request('query', **kwargs)
    
    def check_license(self, account: str) -> Dict:
        """Prüft ob ein Account eine aktive Lizenz hat"""
        result = self._make_request('license_check', account=account)
        if result and result.get('status') == 'success':
            return {
                'has_license': result.get('has_license', False),
                'details': result.get('license_details', {})
            }
        return {'has_license': False, 'details': {}}
    
    def add_license(self, account: str, broker: str, license_type: str = 'standard') -> bool:
        """Fügt eine neue Lizenz hinzu"""
        query = """
        INSERT INTO lnative 
        (account, broker, license_type, status, add_date, registrar) 
        VALUES (?, ?, ?, 'active', ?, 'Python API')
        """
        params = [
            account,
            broker,
            license_type,
            datetime.now().strftime('%d.%m.%Y %H:%M')
        ]
        
        result = self.execute_query(query, params)
        if result and result.get('status') == 'success':
            return result.get('affected_rows', 0) > 0
        return False
    
    def update_license_status(self, account: str, status: str) -> bool:
        """Aktualisiert den Status einer Lizenz"""
        query = "UPDATE lnative SET status = ? WHERE account = ?"
        params = [status, account]
        
        result = self.execute_query(query, params)
        if result and result.get('status') == 'success':
            return result.get('affected_rows', 0) > 0
        return False
    
    def get_all_licenses(self, limit: int = 10) -> List[Dict]:
        """Ruft alle Lizenzen ab"""
        query = f"SELECT * FROM lnative ORDER BY id DESC LIMIT {limit}"
        result = self.execute_query(query)
        if result and result.get('status') == 'success':
            return result.get('data', [])
        return []

def main():
    """Hauptdemo-Funktion"""
    
    print("=" * 70)
    print("🚀 DATENBANK-DEMO FÜR DAX OVERNIGHT EA")
    print("=" * 70)
    
    # Manager initialisieren
    db = DatabaseManager()
    
    # 1. Verbindung testen
    print("\n1️⃣  VERBINDUNGSTEST")
    print("-" * 40)
    if db.test_connection():
        print("✅ Verbindung erfolgreich hergestellt!")
    else:
        print("❌ Verbindung fehlgeschlagen!")
        return
    
    # 2. Tabellen anzeigen
    print("\n2️⃣  VERFÜGBARE TABELLEN")
    print("-" * 40)
    tables = db.get_tables()
    if tables:
        print(f"📊 {len(tables)} Tabellen gefunden:")
        for table in tables[:5]:
            print(f"   • {table}")
    else:
        print("❌ Keine Tabellen gefunden")
    
    # 3. Tabellenstruktur
    print("\n3️⃣  TABELLENSTRUKTUR VON 'lnative'")
    print("-" * 40)
    structure = db.describe_table('lnative')
    if structure:
        print("📋 Spalten:")
        for field in structure[:5]:
            print(f"   • {field.get('Field', 'N/A'):15} {field.get('Type', 'N/A'):20} {field.get('Null', 'N/A')}")
    
    # 4. Lizenzen anzeigen
    print("\n4️⃣  AKTUELLE LIZENZEN")
    print("-" * 40)
    licenses = db.get_all_licenses(5)
    if licenses:
        print(f"📝 {len(licenses)} Lizenzen gefunden:")
        for i, lic in enumerate(licenses, 1):
            print(f"\n   Lizenz {i}:")
            print(f"   • Account:  {lic.get('account', 'N/A')}")
            print(f"   • Broker:   {lic.get('broker', 'N/A')}")
            print(f"   • Status:   {lic.get('status', 'N/A')}")
            print(f"   • Datum:    {lic.get('add_date', 'N/A')}")
    else:
        print("ℹ️  Keine Lizenzen vorhanden")
    
    # 5. Lizenz-Check
    print("\n5️⃣  LIZENZ-CHECK FÜR ACCOUNT")
    print("-" * 40)
    test_account = "89211195"
    license_info = db.check_license(test_account)
    if license_info['has_license']:
        print(f"✅ Account {test_account} hat eine aktive Lizenz!")
        if license_info['details']:
            print(f"   • Broker: {license_info['details'].get('broker', 'N/A')}")
            print(f"   • Typ: {license_info['details'].get('license_type', 'N/A')}")
    else:
        print(f"❌ Account {test_account} hat keine aktive Lizenz")
    
    # 6. Statistiken
    print("\n6️⃣  STATISTIKEN")
    print("-" * 40)
    
    # Aktive Lizenzen zählen
    query = "SELECT COUNT(*) as total FROM lnative WHERE status = 'active'"
    result = db.execute_query(query)
    if result and result.get('status') == 'success':
        data = result.get('data', [])
        if data:
            total = data[0].get('total', 0)
            print(f"📊 Aktive Lizenzen: {total}")
    
    # Lizenzen nach Broker
    query = "SELECT broker, COUNT(*) as count FROM lnative GROUP BY broker"
    result = db.execute_query(query)
    if result and result.get('status') == 'success':
        data = result.get('data', [])
        if data:
            print("\n📈 Lizenzen nach Broker:")
            for row in data:
                broker = row.get('broker', 'Unknown')
                count = row.get('count', 0)
                print(f"   • {broker}: {count} Lizenzen")
    
    # 7. Zusammenfassung
    print("\n" + "=" * 70)
    print("✨ ZUSAMMENFASSUNG")
    print("=" * 70)
    print("✅ Datenbankverbindung funktioniert einwandfrei")
    print("✅ Alle CRUD-Operationen verfügbar")
    print("✅ Lizenz-Management vollständig implementiert")
    print("\n📌 Die Datenbank kann jetzt in MetaTrader 5 genutzt werden!")
    print("   Verwenden Sie die API-URL und den Token in Ihrem EA.")
    
    # API-Info
    print("\n" + "=" * 70)
    print("🔗 API-ZUGANGSDATEN")
    print("=" * 70)
    print(f"URL:   {db.api_url}")
    print(f"Token: {db.token}")
    print("\n💡 Diese Daten in Ihrem MT5 EA verwenden!")

if __name__ == "__main__":
    main()
