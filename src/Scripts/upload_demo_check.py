#!/usr/bin/env python3
"""
Lädt das check_demo_status.php Script auf den Server hoch
"""

import ftplib
from datetime import datetime

# FTP Verbindung
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"

def upload_demo_check():
    """Upload check_demo_status.php auf Server"""
    
    try:
        # Verbinde zu FTP
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"✓ FTP Verbindung hergestellt zu {FTP_HOST}")
        
        # Wechsel in www/lic.prophelper.org/files Verzeichnis  
        ftp.cwd('www/lic.prophelper.org/files')
        print("✓ In Verzeichnis www/lic.prophelper.org/files gewechselt")
        
        # Upload check_demo_status.php
        local_file = '/home/rodemkay/mt5/daxovernight/check_demo_status.php'
        remote_file = 'check_demo_status.php'
        
        with open(local_file, 'rb') as f:
            ftp.storbinary(f'STOR {remote_file}', f)
        print(f"✓ {remote_file} erfolgreich hochgeladen")
        
        # Zeige Datei-Info
        try:
            size = ftp.size(remote_file)
            print(f"  Dateigröße: {size} bytes")
        except:
            pass
            
        ftp.quit()
        print("\n✓ Upload abgeschlossen")
        print(f"  URL: https://lic.prophelper.org/files/{remote_file}")
        
        return True
        
    except Exception as e:
        print(f"✗ Fehler beim Upload: {e}")
        return False

if __name__ == "__main__":
    print("=== Demo Check Script Upload ===")
    print(f"Zeitstempel: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    if upload_demo_check():
        print("\nNächste Schritte:")
        print("1. Teste Script: https://lic.prophelper.org/files/check_demo_status.php?account=TEST&program=der_don")
        print("2. EA kompilieren und testen in MT5")
    else:
        print("\n✗ Upload fehlgeschlagen")