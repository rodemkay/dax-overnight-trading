#!/usr/bin/env python3
"""
Download.php vom Server herunterladen
"""

import ftplib
import os

# FTP-Zugangsdaten
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_DIR = "/www/lic.prophelper.org"

def download_file():
    """download.php herunterladen"""
    try:
        print(f"📡 Verbinde mit FTP-Server {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ FTP-Verbindung hergestellt")
        
        # In Verzeichnis wechseln
        ftp.cwd(FTP_DIR)
        print(f"📂 Verzeichnis: {FTP_DIR}")
        
        # Datei herunterladen
        local_file = "/home/rodemkay/mt5/daxovernight/download.php"
        remote_file = "download.php"
        
        print(f"📥 Lade {remote_file} herunter...")
        with open(local_file, 'wb') as f:
            ftp.retrbinary(f'RETR {remote_file}', f.write)
        
        print(f"✅ Datei gespeichert als: {local_file}")
        
        ftp.quit()
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    download_file()