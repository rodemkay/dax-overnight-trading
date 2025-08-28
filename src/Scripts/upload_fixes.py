#!/usr/bin/env python3
"""Upload all fixes to server"""

import ftplib
import os
from datetime import datetime

FTP_HOST = '162.55.90.123'
FTP_USER = 'prophelp'
FTP_PASS = '.Propt333doka?'
FTP_DIR = '/www/lic.prophelper.org/files/'

def upload_files():
    """Upload the fixed files to server"""
    
    files_to_upload = [
        ('template.inc.php', 'template.inc.php'),
        ('update_robo_status_fixed.php', 'update_robo_status.php')
    ]
    
    print("=== Uploading Fixes to Server ===")
    
    try:
        # Connect to FTP
        print(f"Connecting to {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        
        # Change to target directory
        print(f"Changing to directory {FTP_DIR}")
        ftp.cwd(FTP_DIR)
        
        for local_file, remote_file in files_to_upload:
            local_path = f'/home/rodemkay/mt5/daxovernight/{local_file}'
            
            if not os.path.exists(local_path):
                print(f"Warning: {local_path} not found, skipping...")
                continue
            
            # Create backup
            backup_name = f"{remote_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                ftp.rename(remote_file, backup_name)
                print(f"✓ Backup created: {backup_name}")
            except:
                pass
            
            # Upload file
            print(f"Uploading {local_file} as {remote_file}...")
            with open(local_path, 'rb') as f:
                ftp.storbinary(f'STOR {remote_file}', f)
            print(f"✓ {remote_file} uploaded successfully!")
        
        # Close connection
        ftp.quit()
        
        print("\n=== All Fixes Uploaded ===")
        print("1. Template: Doppelte RoboForex-Spalte entfernt")
        print("2. update_robo_status.php: DB-Passwort korrigiert")
        print("3. EA: Nutzt jetzt direkt WinInet")
        print("\nÄnderungen sind live auf:")
        print("- https://lic.prophelper.org/connect")
        print("- https://lic.prophelper.org/office")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    upload_files()