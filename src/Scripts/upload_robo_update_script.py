#!/usr/bin/env python3
"""
Upload update_robo_status.php zum Server
"""

import ftplib
from datetime import datetime

# FTP Credentials
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_PATH = "/www/lic.prophelper.org/files/"

def upload_php_script():
    """Upload update_robo_status.php zum Server"""
    print("=== Upload RoboForex Update Script ===\n")
    
    try:
        # Verbinde zum FTP Server
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_PATH)
        print(f"✓ Connected to FTP server")
        print(f"✓ Changed to directory: {FTP_PATH}")
        
        # Upload PHP Script
        local_file = 'update_robo_status.php'
        remote_file = 'update_robo_status.php'
        
        with open(local_file, 'rb') as f:
            ftp.storbinary(f'STOR {remote_file}', f)
        
        print(f"✓ Uploaded {local_file} successfully")
        
        # Setze Berechtigungen (644)
        try:
            ftp.voidcmd(f'SITE CHMOD 644 {remote_file}')
            print(f"✓ Set permissions to 644")
        except:
            print("⚠ Could not set permissions (may not be supported)")
        
        # Verifiziere Upload
        files = []
        ftp.retrlines('LIST', files.append)
        
        uploaded = False
        for file_line in files:
            if 'update_robo_status.php' in file_line:
                uploaded = True
                print(f"✓ Verified: {file_line}")
                break
        
        if not uploaded:
            print("⚠ File not found in directory listing")
        
        ftp.quit()
        print("\n✓ Upload complete!")
        print(f"✓ Script available at: https://{FTP_HOST.replace('162.55.90.123', 'lic.prophelper.org')}/files/update_robo_status.php")
        
        return True
        
    except Exception as e:
        print(f"✗ Upload failed: {e}")
        return False

def test_script():
    """Test das hochgeladene Script"""
    print("\n=== Testing Script ===\n")
    
    import requests
    
    test_url = "https://lic.prophelper.org/files/update_robo_status.php"
    
    # Test mit GET Request
    params = {
        'account': '12345678',
        'robo_status': 'no',
        'program': 'test',
        'api_key': 'ec4d40c4343ee741'
    }
    
    try:
        response = requests.get(test_url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            if 'success' in response.text or 'not found' in response.text:
                print("✓ Script is working correctly")
            elif 'error' in response.text:
                print("⚠ Script returned an error (expected for test account)")
            else:
                print("⚠ Unexpected response")
        else:
            print(f"✗ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Test failed: {e}")

if __name__ == "__main__":
    print("This script will upload update_robo_status.php to the server")
    print("The PHP script will be used by the EA to update RoboForex status\n")
    
    response = input("Proceed with upload? (yes/no): ")
    
    if response.lower() == 'yes':
        if upload_php_script():
            print("\n" + "="*50)
            print("SUCCESS!")
            print("="*50)
            print("The update_robo_status.php script has been uploaded.")
            print("The EA can now update the RoboForex status in the database.")
            
            test_response = input("\nTest the script? (yes/no): ")
            if test_response.lower() == 'yes':
                test_script()
    else:
        print("Upload cancelled.")