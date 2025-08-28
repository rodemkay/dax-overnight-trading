"""
Upload und Test des simple_test.php Scripts
"""

import ftplib
import requests
import json

def upload_and_test():
    """Lädt simple_test.php hoch und testet es"""
    
    print("=" * 60)
    print("UPLOAD & TEST SIMPLE PHP")
    print("=" * 60)
    
    # FTP Upload
    print("\n1. FTP Upload...")
    FTP_HOST = "162.55.90.123"
    FTP_USER = "prophelp"
    FTP_PASS = ".Propt333doka?"
    FTP_PATH = "/www/lic.prophelper.org/api/"
    
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_PATH)
        
        with open('r:/mt5/daxovernight/simple_test.php', 'rb') as file:
            ftp.storbinary('STOR simple_test.php', file)
        
        print("✅ simple_test.php hochgeladen")
        ftp.quit()
        
    except Exception as e:
        print(f"❌ FTP-Fehler: {e}")
        return
    
    # Test ohne Token
    print("\n2. Test ohne Token:")
    print("-" * 40)
    url = "https://lic.prophelper.org/api/simple_test.php"
    
    try:
        response = requests.post(url, json={})
        print(response.text)
    except Exception as e:
        print(f"Fehler: {e}")
    
    # Test mit Token
    print("\n3. Test mit Token:")
    print("-" * 40)
    
    try:
        data = {'token': '250277100311270613'}
        response = requests.post(url, json=data)
        print(response.text)
    except Exception as e:
        print(f"Fehler: {e}")
    
    print("\n" + "=" * 60)
    print("TEST ABGESCHLOSSEN")
    print("=" * 60)

if __name__ == "__main__":
    upload_and_test()
