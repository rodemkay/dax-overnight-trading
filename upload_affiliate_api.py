"""
Upload-Script für die erweiterte API mit Affiliate-Status Support
"""

import ftplib
import os
from pathlib import Path

def upload_file_to_ftp():
    """Lädt die erweiterte API auf den Server"""
    
    # FTP-Konfiguration
    FTP_HOST = "lic.prophelper.org"
    FTP_USER = "u97859420"
    FTP_PASS = "g5!PowR%L7&d"
    
    # Datei-Pfade
    local_file = "db_api_with_affiliate.php"
    remote_path = "/api/db_api.php"  # Überschreibt die alte API
    
    print("=" * 70)
    print("📤 UPLOAD ERWEITERTE API MIT AFFILIATE-STATUS")
    print("=" * 70)
    
    try:
        # Verbindung aufbauen
        print(f"\n1️⃣ Verbinde zu {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ FTP-Verbindung hergestellt")
        
        # In API-Verzeichnis wechseln
        print("\n2️⃣ Wechsle ins API-Verzeichnis...")
        ftp.cwd('/api')
        print(f"✅ Aktuelles Verzeichnis: {ftp.pwd()}")
        
        # Datei hochladen
        print(f"\n3️⃣ Lade {local_file} hoch...")
        with open(local_file, 'rb') as file:
            ftp.storbinary(f'STOR db_api.php', file)
        print(f"✅ Datei erfolgreich als db_api.php hochgeladen")
        
        # Rechte setzen
        print("\n4️⃣ Setze Dateirechte...")
        try:
            ftp.sendcmd('SITE CHMOD 644 db_api.php')
            print("✅ Rechte auf 644 gesetzt")
        except:
            print("⚠️ Konnte Rechte nicht setzen (möglicherweise nicht unterstützt)")
        
        # Verifikation
        print("\n5️⃣ Verifiziere Upload...")
        files = []
        ftp.retrlines('LIST', files.append)
        
        for file_info in files:
            if 'db_api.php' in file_info:
                print(f"✅ Gefunden: {file_info}")
                break
        
        # Verbindung schließen
        ftp.quit()
        
        print("\n" + "=" * 70)
        print("✅ UPLOAD ERFOLGREICH ABGESCHLOSSEN!")
        print("=" * 70)
        print("\n📍 API-URL: https://lic.prophelper.org/api/db_api.php")
        print("🔑 Token: 250277100311270613")
        print("\n✨ Neue Features:")
        print("   • update_affiliate_status - Affiliate-Status aktualisieren")
        print("   • get_affiliate_status - Affiliate-Status abrufen")
        print("   • get_all_affiliate_status - Alle Accounts mit Status abrufen")
        print("\n💡 Die API erstellt automatisch die affiliate_status Spalte wenn nötig.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Fehler beim Upload: {e}")
        return False

if __name__ == "__main__":
    success = upload_file_to_ftp()
    
    if success:
        print("\n📋 Nächste Schritte:")
        print("1. Webseite erstellen für Status-Anzeige")
        print("2. MQL5 Code erweitern")
        print("3. End-to-End Test durchführen")
