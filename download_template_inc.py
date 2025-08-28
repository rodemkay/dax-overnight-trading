#!/usr/bin/env python3
"""
Download template.inc.php und andere relevante Dateien vom FTP-Server
"""

from ftplib import FTP
import os

# FTP-Zugangsdaten
FTP_HOST = '162.55.90.123'
FTP_USER = 'prophelp'
FTP_PASS = '.Propt333doka?'

def download_file(ftp_path, local_path):
    """Download einer Datei vom FTP-Server"""
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"✓ Verbunden mit FTP-Server {FTP_HOST}")
        
        # Datei herunterladen
        with open(local_path, 'wb') as local_file:
            ftp.retrbinary(f'RETR {ftp_path}', local_file.write)
        print(f"✓ Heruntergeladen: {ftp_path} → {local_path}")
        
        ftp.quit()
        return True
    except Exception as e:
        print(f"✗ Fehler: {e}")
        return False

def list_directory(ftp_path):
    """Verzeichnisinhalt anzeigen"""
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"✓ Verbunden mit FTP-Server {FTP_HOST}")
        
        ftp.cwd(ftp_path)
        print(f"\nVerzeichnis: {ftp_path}")
        print("-" * 50)
        
        files = []
        ftp.dir(files.append)
        for file in files:
            print(file)
        
        ftp.quit()
    except Exception as e:
        print(f"✗ Fehler: {e}")

# Hauptprogramm
if __name__ == "__main__":
    print("=== FTP Download: template.inc.php ===")
    
    # Zuerst Verzeichnis anzeigen
    list_directory('/www/lic.prophelper.org/files/')
    
    # Wichtige Dateien herunterladen
    files_to_download = [
        ('/www/lic.prophelper.org/files/template.inc.php', 's:\\mt5\\daxovernight\\template.inc.php'),
        ('/www/lic.prophelper.org/files/session.php', 's:\\mt5\\daxovernight\\session.php'),
        ('/www/lic.prophelper.org/files/style.css', 's:\\mt5\\daxovernight\\style.css'),
    ]
    
    print("\n=== Downloads ===")
    for ftp_path, local_path in files_to_download:
        print(f"\nVersuche: {ftp_path}")
        download_file(ftp_path, local_path)
    
    print("\n=== Fertig ===")
