"""
FTP Upload Script für die PHP-API Dateien
Lädt db_api.php und test_api.php auf den Server hoch
"""

import ftplib
import os
from pathlib import Path

def upload_files():
    """Lädt die PHP-Dateien per FTP hoch"""
    
    # FTP-Zugangsdaten
    FTP_HOST = "162.55.90.123"
    FTP_USER = "prophelp"
    FTP_PASS = ".Propt333doka?"
    FTP_PATH = "/www/lic.prophelper.org/api/"
    
    # Dateien zum Hochladen
    files_to_upload = [
        ("r:/mt5/daxovernight/db_api.php", "db_api.php"),
        ("r:/mt5/daxovernight/test_api.php", "test_api.php")
    ]
    
    print("=" * 60)
    print("FTP UPLOAD - PHP API DATEIEN")
    print("=" * 60)
    print(f"\nVerbinde zu FTP-Server: {FTP_HOST}")
    
    try:
        # FTP-Verbindung herstellen
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"✅ Erfolgreich eingeloggt als: {FTP_USER}")
        
        # Zum richtigen Verzeichnis wechseln
        ftp.cwd(FTP_PATH)
        print(f"✅ Verzeichnis gewechselt zu: {FTP_PATH}")
        
        # Dateien hochladen
        for local_file, remote_name in files_to_upload:
            if os.path.exists(local_file):
                print(f"\nLade hoch: {remote_name}")
                
                # Datei öffnen und hochladen
                with open(local_file, 'rb') as file:
                    ftp.storbinary(f'STOR {remote_name}', file)
                
                print(f"  ✅ {remote_name} erfolgreich hochgeladen")
                
                # Größe überprüfen
                try:
                    size = ftp.size(remote_name)
                    local_size = os.path.getsize(local_file)
                    print(f"  📊 Größe: Server={size} bytes, Lokal={local_size} bytes")
                    
                    if size == local_size:
                        print(f"  ✅ Größe stimmt überein")
                    else:
                        print(f"  ⚠️ Größe unterschiedlich!")
                except:
                    pass
            else:
                print(f"❌ Datei nicht gefunden: {local_file}")
        
        # Verzeichnisinhalt anzeigen
        print("\n📂 Verzeichnisinhalt von /api/:")
        files = ftp.nlst()
        for file in files:
            if file.endswith('.php'):
                try:
                    size = ftp.size(file)
                    print(f"  - {file} ({size} bytes)")
                except:
                    print(f"  - {file}")
        
        # FTP-Verbindung schließen
        ftp.quit()
        print("\n✅ FTP-Verbindung geschlossen")
        
        print("\n" + "=" * 60)
        print("UPLOAD ABGESCHLOSSEN!")
        print("=" * 60)
        
        print("\n🔧 Teste die API:")
        print("1. Basis-Test: https://lic.prophelper.org/api/test_api.php")
        print("2. Haupt-API: https://lic.prophelper.org/api/db_api.php")
        print("\nFühre aus: x:\\Python313\\python.exe r:\\mt5\\daxovernight\\test_api_debug.py")
        
    except ftplib.error_perm as e:
        print(f"❌ FTP Berechtigung verweigert: {e}")
    except ftplib.error_temp as e:
        print(f"❌ Temporärer FTP-Fehler: {e}")
    except Exception as e:
        print(f"❌ Fehler beim FTP-Upload: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    upload_files()
