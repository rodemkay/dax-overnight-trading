#!/usr/bin/env python3
"""Upload fixed template.inc.php to server"""

import ftplib
import os
from datetime import datetime

FTP_HOST = '162.55.90.123'
FTP_USER = 'prophelp'
FTP_PASS = '.Propt333doka?'
FTP_DIR = '/www/lic.prophelper.org/files/'

def upload_template():
    """Upload the fixed template to server"""
    
    local_file = '/home/rodemkay/mt5/daxovernight/template.inc.php'
    
    print("=== Uploading Fixed Template ===")
    
    # Check if file exists
    if not os.path.exists(local_file):
        print(f"Error: {local_file} not found!")
        return False
    
    try:
        # Connect to FTP
        print(f"Connecting to {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        
        # Change to target directory
        print(f"Changing to directory {FTP_DIR}")
        ftp.cwd(FTP_DIR)
        
        # Create backup on server
        backup_name = f"template.inc.php.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"Creating backup: {backup_name}")
        try:
            ftp.rename('template.inc.php', backup_name)
            print(f"✓ Backup created: {backup_name}")
        except:
            print("Note: Could not create backup (file might not exist)")
        
        # Upload new file
        print("Uploading fixed template.inc.php...")
        with open(local_file, 'rb') as f:
            ftp.storbinary('STOR template.inc.php', f)
        
        print("✓ Upload successful!")
        
        # Close connection
        ftp.quit()
        
        print("\n=== Upload Complete ===")
        print("The fixed template with RoboForex header is now live!")
        print("Check: https://lic.prophelper.org/connect")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    upload_template()