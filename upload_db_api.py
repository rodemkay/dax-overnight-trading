"""
Upload der db_api.php zum Server
"""

import ftplib
import os

def upload_db_api():
    """Lädt db_api.php auf den Server"""
    
    print("=" * 60)
    print("UPLOAD DB_API.PHP")
    print("=" * 60)
    
    FTP_HOST = "162.55.90.123"
    FTP_USER = "prophelp"
    FTP_PASS = ".Propt333doka?"
    FTP_PATH = "/www/lic.prophelper.org/api/"
    
    try:
        # Verbindung aufbauen
        print("\n1. Verbinde mit FTP-Server...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ FTP-Verbindung hergestellt")
        
        # Zum richtigen Verzeichnis wechseln
        print("\n2. Wechsle zum API-Verzeichnis...")
        ftp.cwd(FTP_PATH)
        print(f"✅ Aktuelles Verzeichnis: {ftp.pwd()}")
        
        # db_api.php hochladen
        print("\n3. Lade db_api.php hoch...")
        local_file = 'r:/mt5/daxovernight/db_api.php'
        
        if os.path.exists(local_file):
            file_size = os.path.getsize(local_file)
            print(f"   Datei gefunden: {file_size} bytes")
            
            with open(local_file, 'rb') as file:
                ftp.storbinary('STOR db_api.php', file)
            
            print("✅ db_api.php erfolgreich hochgeladen")
        else:
            print("❌ db_api.php nicht gefunden!")
            return
        
        # Dateien im Verzeichnis anzeigen
        print("\n4. Dateien im API-Verzeichnis:")
        print("-" * 40)
        files = []
        ftp.retrlines('LIST', files.append)
        for file in files:
            if 'db_api.php' in file or 'test' in file or 'simple' in file:
                print(f"   {file}")
        
        ftp.quit()
        print("\n✅ Upload abgeschlossen!")
        
    except Exception as e:
        print(f"❌ FTP-Fehler: {e}")
        return
    
    print("\n" + "=" * 60)
    print("NÄCHSTE SCHRITTE:")
    print("=" * 60)
    print("1. Öffnen Sie test_api.html im Browser")
    print("2. Klicken Sie auf 'Verbindung testen'")
    print("3. Die API sollte jetzt erreichbar sein")
    print("\nAPI-URL: https://lic.prophelper.org/api/db_api.php")
    print("Token: 250277100311270613")

if __name__ == "__main__":
    upload_db_api()
