import mysql.connector
from mysql.connector import Error
import sys

# Optional imports for SSH tunnel
try:
    import paramiko
    from sshtunnel import SSHTunnelForwarder
    SSH_AVAILABLE = True
except ImportError:
    SSH_AVAILABLE = False

def test_database_connection_direct():
    """Direkter Verbindungsversuch"""
    print("=== VERSUCH 1: Direkte Verbindung ===\n")
    
    try:
        connection = mysql.connector.connect(
            host='162.55.90.123',
            database='prophelp_users_1',
            user='prophelp_adm',
            password='mW0uG1pG9b',
            port=3306
        )
        
        if connection.is_connected():
            print("✅ Direkte Verbindung erfolgreich!")
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Direkte Verbindung fehlgeschlagen: {e}\n")
        return False

def test_database_connection_ssh():
    """Verbindung über SSH-Tunnel"""
    print("=== VERSUCH 2: Verbindung über SSH-Tunnel ===\n")
    
    try:
        # SSH-Tunnel-Konfiguration
        server = SSHTunnelForwarder(
            ('162.55.90.123', 22),  # SSH-Server
            ssh_username='prophelp',  # SSH-Benutzer aus FTP-Credentials
            ssh_password='.Propt333doka?',  # SSH-Passwort aus FTP-Credentials
            remote_bind_address=('127.0.0.1', 3306)  # MySQL auf dem Server
        )
        
        server.start()
        print(f"✅ SSH-Tunnel erfolgreich aufgebaut auf lokalem Port: {server.local_bind_port}")
        
        # Verbindung über den Tunnel
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='prophelp_users_1',
            user='prophelp_adm',
            password='mW0uG1pG9b',
            port=server.local_bind_port
        )
        
        if connection.is_connected():
            print("✅ Datenbankverbindung über SSH-Tunnel erfolgreich!")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"✅ Verbunden mit Datenbank: {record[0]}")
            
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print(f"\n📊 Gefundene Tabellen ({len(tables)} insgesamt):")
            for table in tables[:10]:
                print(f"   - {table[0]}")
            
            cursor.close()
            connection.close()
            server.stop()
            return True
            
    except Exception as e:
        print(f"❌ SSH-Tunnel Verbindung fehlgeschlagen: {e}\n")
        return False

def test_alternative_credentials():
    """Teste mit Web-Server Credentials"""
    print("=== VERSUCH 3: Alternative Anmeldedaten (Web-Server) ===\n")
    
    try:
        connection = mysql.connector.connect(
            host='45.145.52.200',  # Web-Server IP
            database='prophelp_users_1',
            user='prophelp',
            password='3h:4cWBQ5rh8*K',  # Web-Server Passwort
            port=3306
        )
        
        if connection.is_connected():
            print("✅ Verbindung mit alternativen Credentials erfolgreich!")
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Alternative Verbindung fehlgeschlagen: {e}\n")
        return False

if __name__ == "__main__":
    print("="*60)
    print("TEST DER DATENBANKVERBINDUNG ZU prophelp_users_1")
    print("="*60 + "\n")
    
    # Teste verschiedene Verbindungsmethoden
    success = False
    
    # 1. Direkter Versuch
    if test_database_connection_direct():
        success = True
    
    # 2. SSH-Tunnel Versuch (nur wenn paramiko und sshtunnel installiert sind)
    try:
        import sshtunnel
        if not success and test_database_connection_ssh():
            success = True
    except ImportError:
        print("ℹ️ SSH-Tunnel-Test übersprungen (sshtunnel nicht installiert)")
        print("   Installation mit: pip install sshtunnel paramiko\n")
    
    # 3. Alternative Credentials
    if not success and test_alternative_credentials():
        success = True
    
    if success:
        print("\n✅ ERFOLG: Mindestens eine Verbindungsmethode funktioniert!")
    else:
        print("\n❌ FEHLER: Keine Verbindungsmethode war erfolgreich.")
        print("\nMögliche Lösungen:")
        print("1. IP-Adresse 185.72.234.93 muss auf dem MySQL-Server freigegeben werden")
        print("2. Verbindung über VPN (Tailscale) herstellen")
        print("3. SSH-Tunnel verwenden (pip install sshtunnel paramiko)")
