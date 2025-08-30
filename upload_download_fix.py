#!/usr/bin/env python3
"""
Upload korrigierte download.php
"""

import ftplib
import os

# FTP-Zugangsdaten
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_DIR = "/www/lic.prophelper.org"

def upload_file():
    """Korrigierte download.php hochladen"""
    try:
        print("=" * 60)
        print("DOWNLOAD.PHP FIX UPLOAD")
        print("=" * 60)
        
        print(f"\n📡 Verbinde mit FTP-Server {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ FTP-Verbindung hergestellt")
        
        # In Verzeichnis wechseln
        ftp.cwd(FTP_DIR)
        print(f"📂 Verzeichnis: {FTP_DIR}")
        
        # Datei hochladen
        local_file = "/home/rodemkay/mt5/daxovernight/download.php"
        remote_file = "download.php"
        
        print(f"📤 Lade {remote_file} hoch...")
        with open(local_file, 'rb') as f:
            ftp.storbinary(f'STOR {remote_file}', f)
        
        print(f"✅ {remote_file} erfolgreich hochgeladen!")
        
        # Berechtigungen setzen
        try:
            ftp.sendcmd(f'SITE CHMOD 644 {remote_file}')
            print(f"🔒 Berechtigungen gesetzt: 644")
        except:
            print(f"⚠️  Konnte Berechtigungen nicht setzen (nicht kritisch)")
        
        ftp.quit()
        
        print("\n" + "=" * 60)
        print("✅ ERFOLGREICH!")
        print("=" * 60)
        print("\n📋 Behobener Fehler:")
        print("- Notice: Undefined offset: 2 in line 108")
        print("\n✨ Lösung:")
        print("- Array-Zugriff mit isset() geprüft")
        print("- Verhindert Fehler bei fehlenden Array-Elementen")
        print("\n🌐 URL: https://lic.prophelper.org/download.php")
        print("✅ Der Fehler sollte jetzt behoben sein!")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    upload_file()