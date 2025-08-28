"""
Python-Client für die prophelp_users_1 Datenbank-API
Verwendet die PHP-API auf dem Server für sichere Datenbankzugriffe

WICHTIG: Token ist konfiguriert: 250277100311270613
"""

import requests
import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

class DatabaseClient:
    """Client für die prophelp_users_1 Datenbank über die PHP-API"""
    
    def __init__(self, api_url: str = None, token: str = None):
        """
        Initialisiert den Datenbank-Client
        
        Args:
            api_url: URL zur db_api.php Datei
            token: API-Token für Authentifizierung
        """
        # Standard-Werte verwenden, wenn nicht angegeben
        self.api_url = api_url or "https://lic.prophelper.org/api/db_api.php"
        self.token = token or "250277100311270613"  # Korrektes Token gesetzt
        
        # Session für bessere Performance bei mehreren Requests
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'DAX-Overnight-DB-Client/1.0'
        })
        
    def _make_request(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Führt einen API-Request aus
        
        Args:
            action: Die auszuführende Aktion
            **kwargs: Zusätzliche Parameter für die Aktion
            
        Returns:
            API-Response als Dictionary
        """
        data = {
            'token': self.token,
            'action': action,
            **kwargs
        }
        
        try:
            response = self.session.post(self.api_url, json=data)
            response.raise_for_status()
            
            result = response.json()
            if not result.get('success', False):
                raise Exception(f"API Error: {result.get('error', 'Unknown error')}")
                
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Testet die Verbindung zur Datenbank
        
        Returns:
            True wenn Verbindung erfolgreich
        """
        try:
            result = self._make_request('test')
            print(f"✅ Verbindung erfolgreich zur Datenbank: {result.get('database')}")
            return True
        except Exception as e:
            print(f"❌ Verbindungsfehler: {e}")
            return False
    
    def query(self, sql: str, params: List[Any] = None) -> Union[List[Dict], Dict]:
        """
        Führt eine beliebige SQL-Query aus
        
        Args:
            sql: SQL-Query
            params: Parameter für Prepared Statements
            
        Returns:
            Query-Ergebnis
        """
        result = self._make_request('query', query=sql, params=params or [])
        
        if 'data' in result:
            return result['data']
        else:
            return {
                'affected_rows': result.get('affected_rows', 0),
                'last_insert_id': result.get('last_insert_id')
            }
    
    def select(self, sql: str, params: List[Any] = None) -> List[Dict]:
        """
        Führt eine SELECT-Query aus
        
        Args:
            sql: SELECT-Query
            params: Parameter für Prepared Statements
            
        Returns:
            Liste der Ergebnisse
        """
        if not sql.strip().upper().startswith('SELECT'):
            sql = f"SELECT {sql}"
            
        return self.query(sql, params)
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        Fügt einen Datensatz ein
        
        Args:
            table: Tabellenname
            data: Dictionary mit Spaltennamen und Werten
            
        Returns:
            ID des eingefügten Datensatzes
        """
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ', '.join(['?' for _ in columns])
        
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        result = self.query(sql, values)
        
        return result.get('last_insert_id', 0)
    
    def update(self, table: str, data: Dict[str, Any], where: str, where_params: List[Any] = None) -> int:
        """
        Aktualisiert Datensätze
        
        Args:
            table: Tabellenname
            data: Dictionary mit zu aktualisierenden Spalten
            where: WHERE-Bedingung
            where_params: Parameter für WHERE-Bedingung
            
        Returns:
            Anzahl der aktualisierten Datensätze
        """
        set_clause = ', '.join([f"{col} = ?" for col in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        
        params = list(data.values()) + (where_params or [])
        result = self.query(sql, params)
        
        return result.get('affected_rows', 0)
    
    def delete(self, table: str, where: str, params: List[Any] = None) -> int:
        """
        Löscht Datensätze
        
        Args:
            table: Tabellenname
            where: WHERE-Bedingung
            params: Parameter für WHERE-Bedingung
            
        Returns:
            Anzahl der gelöschten Datensätze
        """
        sql = f"DELETE FROM {table} WHERE {where}"
        result = self.query(sql, params)
        
        return result.get('affected_rows', 0)
    
    def get_tables(self) -> List[str]:
        """
        Listet alle Tabellen auf
        
        Returns:
            Liste der Tabellennamen
        """
        result = self._make_request('tables')
        tables = result.get('data', [])
        
        # Extrahiere Tabellennamen aus dem Result
        return [list(table.values())[0] for table in tables]
    
    def describe_table(self, table: str) -> List[Dict]:
        """
        Zeigt die Struktur einer Tabelle
        
        Args:
            table: Tabellenname
            
        Returns:
            Tabellenstruktur
        """
        result = self._make_request('describe', table=table)
        return result.get('data', [])
    
    def check_license(self, account: str) -> Dict[str, Any]:
        """
        Prüft Lizenz für einen Account
        
        Args:
            account: Account-Nummer
            
        Returns:
            Lizenzinformationen
        """
        result = self._make_request('license_check', account=account)
        return {
            'has_license': result.get('has_license', False),
            'licenses': result.get('data', [])
        }
    
    def to_dataframe(self, data: List[Dict]) -> Any:
        """
        Konvertiert Query-Ergebnis zu Pandas DataFrame
        
        Args:
            data: Query-Ergebnis
            
        Returns:
            Pandas DataFrame oder die Daten selbst wenn pandas nicht installiert
        """
        try:
            import pandas as pd
            return pd.DataFrame(data)
        except ImportError:
            print("⚠️ Pandas nicht installiert. Installieren mit: pip install pandas")
            return data


# Beispiel-Funktionen für häufige Operationen
class LicenseManager:
    """Verwaltung der Lizenzen in der lnative Tabelle"""
    
    def __init__(self, db_client: DatabaseClient):
        self.db = db_client
    
    def get_all_licenses(self) -> List[Dict]:
        """Alle Lizenzen abrufen"""
        return self.db.select("SELECT * FROM lnative")
    
    def get_active_licenses(self) -> List[Dict]:
        """Nur aktive Lizenzen abrufen"""
        return self.db.select("SELECT * FROM lnative WHERE status = 'active'")
    
    def get_license_by_account(self, account: str) -> Optional[Dict]:
        """Lizenz für bestimmten Account abrufen"""
        licenses = self.db.select(
            "SELECT * FROM lnative WHERE account = ?", 
            [account]
        )
        return licenses[0] if licenses else None
    
    def activate_license(self, account: str, product: str) -> bool:
        """Neue Lizenz aktivieren"""
        data = {
            'account': account,
            'product': product,
            'status': 'active',
            'activated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        license_id = self.db.insert('lnative', data)
        return license_id > 0
    
    def deactivate_license(self, account: str) -> bool:
        """Lizenz deaktivieren"""
        affected = self.db.update(
            'lnative',
            {'status': 'inactive'},
            'account = ?',
            [account]
        )
        return affected > 0


def main():
    """Hauptfunktion zum Testen"""
    print("=" * 60)
    print("DAX OVERNIGHT - Datenbank Client")
    print("=" * 60 + "\n")
    
    # Client initialisieren
    db = DatabaseClient()
    
    print("Token konfiguriert: 250277100311270613")
    print("API-URL: https://lic.prophelper.org/api/db_api.php\n")
    
    # Verbindung testen
    if not db.test_connection():
        print("\n❌ Verbindung fehlgeschlagen!")
        print("\nMögliche Ursachen:")
        print("1. Die db_api.php ist noch nicht auf dem Server")
        print("2. Die URL ist falsch")
        print("3. Das Token stimmt nicht überein")
        return
    
    print("\n=== Verfügbare Tabellen ===")
    try:
        tables = db.get_tables()
        for table in tables[:10]:
            print(f"  - {table}")
        if len(tables) > 10:
            print(f"  ... und {len(tables) - 10} weitere")
        
        # Prüfe ob lnative Tabelle existiert
        if 'lnative' in tables:
            print("\n=== Struktur der Lizenz-Tabelle (lnative) ===")
            structure = db.describe_table('lnative')
            for col in structure:
                print(f"  - {col['Field']}: {col['Type']} {col['Null']} {col.get('Key', '')}")
            
            # Beispiel-Query
            print("\n=== Beispiel: Erste 5 Lizenzen ===")
            licenses = db.select("SELECT * FROM lnative LIMIT 5")
            for i, license in enumerate(licenses, 1):
                print(f"{i}. Account: {license.get('account', 'N/A')}, Status: {license.get('status', 'N/A')}")
    except Exception as e:
        print(f"\nFehler beim Abrufen der Daten: {e}")
    
    print("\n✅ Datenbank-Client ist einsatzbereit!")
    print("\nBeispiel-Code:")
    print("```python")
    print("from db_client import DatabaseClient")
    print("db = DatabaseClient()")
    print("result = db.select('SELECT * FROM lnative WHERE account = ?', ['12345'])")
    print("```")


if __name__ == "__main__":
    main()
