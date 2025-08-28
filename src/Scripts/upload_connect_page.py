#!/usr/bin/env python3
"""
Upload der Connect-Seite
"""

import ftplib
import os
import sys
from datetime import datetime

# FTP-Konfiguration
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
REMOTE_DIR = "/www/lic.prophelper.org"

def upload_file():
    """Lädt die connect.html auf den Server"""
    
    print("=" * 60)
    print("Connect-Seite Upload")
    print("=" * 60)
    
    local_file = "connect.html"
    remote_file = "connect.html"
    
    if not os.path.exists(local_file):
        print(f"❌ Datei {local_file} nicht gefunden!")
        return False
    
    try:
        # FTP-Verbindung
        print(f"\n📡 Verbinde zu {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ Verbunden")
        
        # Zum Hauptverzeichnis wechseln
        ftp.cwd(REMOTE_DIR)
        print(f"📂 Arbeitsverzeichnis: {REMOTE_DIR}")
        
        # Neue Datei hochladen
        print(f"\n📤 Lade {local_file} hoch...")
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
        print("✅ Connect-Seite erfolgreich hochgeladen!")
        print("=" * 60)
        print("\n🌐 Die Seite ist jetzt verfügbar unter:")
        print("   https://lic.prophelper.org/connect.html")
        print("\nFunktionen:")
        print("  • Zeigt alle Accounts mit Status")
        print("  • Zeigt RoboForex Affiliate-Status")
        print("  • Auto-Refresh alle 30 Sekunden")
        print("  • Statistik-Dashboard")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Upload: {str(e)}")
        return False

if __name__ == "__main__":
    if upload_file():
        sys.exit(0)
    else:
        sys.exit(1)
