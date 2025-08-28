#!/usr/bin/env python3
"""
Download template.php vom FTP-Server zur Analyse
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

# Hauptprogramm
if __name__ == "__main__":
    print("=== FTP Download: template.php ===")
    
    # Verschiedene mögliche Pfade für template.php
    files_to_check = [
        ('/www/lic.prophelper.org/template.php', 's:\\mt5\\daxovernight\\template_root.php'),
        ('/www/lic.prophelper.org/files/template.php', 's:\\mt5\\daxovernight\\template_files.php'),
        ('/www/lic.prophelper.org/connect.php', 's:\\mt5\\daxovernight\\connect_root.php'),
        ('/www/lic.prophelper.org/files/connect.php', 's:\\mt5\\daxovernight\\connect_files.php')
    ]
    
    for ftp_path, local_path in files_to_check:
        print(f"\nVersuche: {ftp_path}")
        download_file(ftp_path, local_path)
    
    print("\n=== Fertig ===")
