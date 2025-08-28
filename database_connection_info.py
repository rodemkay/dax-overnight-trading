"""
Datenbankverbindung zu prophelp_users_1
========================================

PROBLEM:
Die MySQL-Datenbank ist von außen (IP 185.72.234.93) nicht direkt erreichbar.

VERFÜGBARE ZUGÄNGE:
1. phpMyAdmin (Web-Interface)
   - URL: https://web-de.wishhost.net:1501/lGoJSoSPtQ0xoqNk/phpmyadmin/index.php
   - Benutzer: prophelp_adm
   - Passwort: mW0uG1pG9b
   - Datenbank: prophelp_users_1

2. Direkte MySQL-Verbindung (nur von bestimmten IPs)
   - Host: 162.55.90.123
   - Port: 3306
   - Datenbank: prophelp_users_1
   - Benutzer: prophelp_adm
   - Passwort: mW0uG1pG9b

LÖSUNGSANSÄTZE:
"""

import mysql.connector
from mysql.connector import Error
import subprocess
import platform

def check_tailscale_connection():
    """Prüft ob Tailscale VPN aktiv ist"""
    print("=== Prüfe Tailscale VPN Status ===\n")
    
    try:
        # Windows-Befehl für Tailscale Status
        if platform.system() == 'Windows':
            result = subprocess.run(['tailscale', 'status'], 
                                  capture_output=True, 
                                  text=True, 
                                  shell=True)
            
            if result.returncode == 0:
                print("✅ Tailscale ist installiert")
                if "100." in result.stdout:  # Tailscale IPs beginnen mit 100.
                    print("✅ Tailscale VPN ist aktiv")
                    print("\nTailscale Geräte im Netzwerk:")
                    print(result.stdout)
                    return True
                else:
                    print("❌ Tailscale VPN ist nicht verbunden")
            else:
                print("❌ Tailscale ist nicht installiert oder nicht im PATH")
    except Exception as e:
        print(f"❌ Fehler beim Prüfen von Tailscale: {e}")
    
    return False

def test_connection_via_ryzenserver():
    """Teste Verbindung über RYZENSERVER (Tailscale)"""
    print("\n=== Teste Verbindung über RYZENSERVER (100.89.207.122) ===\n")
    
    try:
        # Versuche Verbindung über RYZENSERVER im Tailscale-Netzwerk
        connection = mysql.connector.connect(
            host='100.89.207.122',  # RYZENSERVER Tailscale IP
            database='prophelp_users_1',
            user='prophelp_adm',
            password='mW0uG1pG9b',
            port=3306
        )
        
        if connection.is_connected():
            print("✅ Verbindung über RYZENSERVER erfolgreich!")
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Verbindung über RYZENSERVER fehlgeschlagen: {e}")
        return False

def test_connection_via_localhost():
    """Teste ob MySQL lokal läuft (für Tests auf dem Server selbst)"""
    print("\n=== Teste lokale MySQL-Verbindung ===\n")
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='prophelp_users_1',
            user='prophelp_adm',
            password='mW0uG1pG9b',
            port=3306
        )
        
        if connection.is_connected():
            print("✅ Lokale Verbindung erfolgreich (Script läuft auf dem Server)!")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"✅ Verbunden mit Datenbank: {record[0]}")
            
            # Prüfe Lizenz-Tabelle
            cursor.execute("SHOW TABLES LIKE 'lnative';")
            if cursor.fetchone():
                print("✅ Lizenz-Tabelle 'lnative' gefunden")
                
                # Zeige Struktur der Lizenz-Tabelle
                cursor.execute("DESCRIBE lnative;")
                columns = cursor.fetchall()
                print("\n📊 Struktur der Lizenz-Tabelle:")
                for col in columns:
                    print(f"   - {col[0]}: {col[1]}")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Lokale Verbindung fehlgeschlagen: {e}")
        return False

def show_connection_solutions():
    """Zeigt mögliche Lösungen für die Datenbankverbindung"""
    print("\n" + "="*60)
    print("EMPFOHLENE LÖSUNGEN FÜR DIE DATENBANKVERBINDUNG")
    print("="*60 + "\n")
    
    print("1. TAILSCALE VPN VERWENDEN (Empfohlen)")
    print("   - Tailscale auf diesem Computer installieren")
    print("   - Mit dem Tailscale-Netzwerk verbinden")
    print("   - Dann über RYZENSERVER (100.89.207.122) verbinden")
    print()
    
    print("2. phpMyAdmin VERWENDEN (Für manuelle Operationen)")
    print("   - URL: https://web-de.wishhost.net:1501/lGoJSoSPtQ0xoqNk/phpmyadmin/")
    print("   - Benutzer: prophelp_adm")
    print("   - Passwort: mW0uG1pG9b")
    print()
    
    print("3. REST API ERSTELLEN (Für programmatischen Zugriff)")
    print("   - PHP-API auf dem Server erstellen")
    print("   - Über HTTPS-Requests auf die Datenbank zugreifen")
    print("   - Sicherer als direkte MySQL-Verbindung von außen")
    print()
    
    print("4. SSH-TUNNEL EINRICHTEN")
    print("   - SSH-Zugang zum Server einrichten")
    print("   - MySQL über SSH-Tunnel verbinden")
    print("   - Installation: pip install sshtunnel paramiko")
    print()
    
    print("5. IP-WHITELIST ANPASSEN (Server-Admin erforderlich)")
    print("   - Ihre IP 185.72.234.93 auf dem MySQL-Server freigeben")
    print("   - In MySQL: GRANT ALL ON prophelp_users_1.* TO 'prophelp_adm'@'185.72.234.93'")

if __name__ == "__main__":
    print("="*60)
    print("ANALYSE DER DATENBANKVERBINDUNGSMÖGLICHKEITEN")
    print("="*60 + "\n")
    
    # Teste verschiedene Verbindungsmöglichkeiten
    success = False
    
    # 1. Prüfe Tailscale
    if check_tailscale_connection():
        # Wenn Tailscale aktiv, teste Verbindung über RYZENSERVER
        if test_connection_via_ryzenserver():
            success = True
    
    # 2. Teste lokale Verbindung (falls Script auf Server läuft)
    if not success:
        if test_connection_via_localhost():
            success = True
    
    # 3. Zeige Lösungsvorschläge
    if not success:
        show_connection_solutions()
    else:
        print("\n✅ ERFOLG: Datenbankverbindung hergestellt!")
        print("\nSie können nun mit der Datenbank arbeiten.")
