#!/usr/bin/env python3
"""
Upload der aktualisierten API mit Affiliate-Support
"""

import ftplib
import os
import sys
from datetime import datetime

# FTP-Konfiguration
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
REMOTE_DIR = "/www/lic.prophelper.org/api"

def upload_file():
    """Lädt die aktualisierte db_api.php auf den Server"""
    
    print("=" * 60)
    print("API Upload mit Affiliate-Support")
    print("=" * 60)
    
    local_file = "db_api_fixed.php"
    remote_file = "db_api.php"
    
    if not os.path.exists(local_file):
        print(f"❌ Datei {local_file} nicht gefunden!")
        return False
    
    try:
        # FTP-Verbindung
        print(f"\n📡 Verbinde zu {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ Verbunden")
        
        # Zum API-Verzeichnis wechseln
        ftp.cwd(REMOTE_DIR)
        print(f"📂 Arbeitsverzeichnis: {REMOTE_DIR}")
        
        # Backup der alten Datei
        backup_name = f"db_api_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.php"
        try:
            ftp.rename(remote_file, backup_name)
            print(f"💾 Backup erstellt: {backup_name}")
        except:
            print("⚠️  Keine existierende Datei zum Backup gefunden")
        
        # Neue Datei hochladen
        print(f"\n📤 Lade {local_file} als {remote_file} hoch...")
        with open(local_file, 'rb') as file:
            ftp.storbinary(f'STOR {remote_file}', file)
        
        # Dateigröße prüfen
        size = ftp.size(remote_file)
        print(f"✅ Upload erfolgreich! Größe: {size} bytes")
        
        # Rechte setzen
        try:
            ftp.sendcmd(f'SITE CHMOD 644 {remote_file}')
            print("✅ Dateirechte gesetzt (644)")
        except:
            print("⚠️  Konnte Dateirechte nicht setzen")
        
        ftp.quit()
        
        print("\n" + "=" * 60)
        print("✅ API mit Affiliate-Support erfolgreich hochgeladen!")
        print("=" * 60)
        print("\nDie API unterstützt jetzt folgende neue Actions:")
        print("  • get_all - Alle Datensätze abrufen")
        print("  • get_account - Einzelnes Konto abrufen")
        print("  • update_affiliate - Affiliate-Status aktualisieren")
        print("\nURL: https://lic.prophelper.org/api/db_api.php")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Upload: {str(e)}")
        return False

if __name__ == "__main__":
    if upload_file():
        sys.exit(0)
    else:
        sys.exit(1)
