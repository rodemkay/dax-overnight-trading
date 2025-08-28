"""
Upload der korrigierten API-Datei
"""

import ftplib
import os
from datetime import datetime

def upload_fixed_api():
    """Lädt die korrigierte API auf den Server"""
    
    print("=" * 60)
    print("📤 UPLOAD DER KORRIGIERTEN API")
    print("=" * 60)
    
    # FTP-Verbindungsdaten (aus network_credentials.txt)
    FTP_HOST = "162.55.90.123"
    FTP_USER = "prophelp"
    FTP_PASS = ".Propt333doka?"
    REMOTE_PATH = "/www/lic.prophelper.org/api/"
    
    # Lokale Datei
    local_file = "db_api_fixed.php"
    remote_file = "db_api.php"  # Überschreibt die alte Version
    
    print(f"\nZeit: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Server: {FTP_HOST}")
    print(f"Zielordner: {REMOTE_PATH}")
    
    try:
        # Verbindung herstellen
        print("\n📡 Stelle FTP-Verbindung her...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ Verbindung erfolgreich!")
        
        # Zum richtigen Verzeichnis wechseln
        print(f"\n📂 Wechsle zu: {REMOTE_PATH}")
        ftp.cwd(REMOTE_PATH)
        print("✅ Verzeichnis gefunden!")
        
        # Alte Datei sichern (falls vorhanden)
        try:
            print(f"\n💾 Sichere alte Version...")
            backup_name = f"db_api_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.php"
            ftp.rename(remote_file, backup_name)
            print(f"✅ Backup erstellt: {backup_name}")
        except:
            print("ℹ️  Keine alte Version vorhanden")
        
        # Neue Datei hochladen
        print(f"\n📤 Lade korrigierte API hoch...")
        with open(local_file, 'rb') as file:
            ftp.storbinary(f'STOR {remote_file}', file)
        print("✅ Upload erfolgreich!")
        
        # Dateigröße prüfen
        size = ftp.size(remote_file)
        print(f"📊 Dateigröße: {size} Bytes")
        
        # Verbindung schließen
        ftp.quit()
        
        print("\n" + "=" * 60)
        print("🎉 API ERFOLGREICH AKTUALISIERT!")
        print("=" * 60)
        print("\nDie korrigierte API ist jetzt verfügbar unter:")
        print(f"https://lic.prophelper.org/api/{remote_file}")
        print("\nDie Verbindung sollte jetzt funktionieren!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Fehler beim Upload: {e}")
        return False

if __name__ == "__main__":
    upload_fixed_api()
