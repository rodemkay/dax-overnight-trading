#!/usr/bin/env python3
"""
Upload verbesserte Testzeitraum-Meldungen zum Server
"""

import ftplib
import os
from pathlib import Path

# FTP-Zugangsdaten
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_DIR = "/www/lic.prophelper.org/files"

def upload_file(local_file, remote_name):
    """Datei per FTP hochladen"""
    try:
        # Verbindung herstellen
        print(f"\n📡 Verbinde mit FTP-Server {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ FTP-Verbindung hergestellt")
        
        # In Zielverzeichnis wechseln
        ftp.cwd(FTP_DIR)
        print(f"📂 Verzeichnis gewechselt zu: {FTP_DIR}")
        
        # Datei hochladen
        with open(local_file, 'rb') as f:
            print(f"📤 Lade {remote_name} hoch...")
            ftp.storbinary(f'STOR {remote_name}', f)
            print(f"✅ {remote_name} erfolgreich hochgeladen!")
        
        # Berechtigungen setzen
        try:
            ftp.sendcmd(f'SITE CHMOD 644 {remote_name}')
            print(f"🔒 Berechtigungen für {remote_name} gesetzt: 644")
        except:
            print(f"⚠️  Konnte Berechtigungen nicht setzen (nicht kritisch)")
        
        ftp.quit()
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Upload: {e}")
        return False

def main():
    print("=" * 60)
    print("TESTZEITRAUM-MELDUNGEN VERBESSERN")
    print("=" * 60)
    
    # Datei zum Upload
    local_file = "/home/rodemkay/mt5/daxovernight/metatrader_patched.php"
    
    if not os.path.exists(local_file):
        print(f"❌ Datei nicht gefunden: {local_file}")
        return
    
    print(f"\n📁 Lokale Datei: {local_file}")
    print(f"🎯 Ziel: {FTP_HOST}:{FTP_DIR}/metatrader.php")
    
    # Auto-Upload ohne Abfrage (für automatische Ausführung)
    print("\n⚠️  ACHTUNG: Dies wird die Live-Datei auf dem Server überschreiben!")
    print("🚀 Auto-Upload aktiviert...")
    
    # Upload durchführen
    if upload_file(local_file, "metatrader.php"):
        print("\n" + "=" * 60)
        print("✅ ERFOLGREICH HOCHGELADEN!")
        print("=" * 60)
        print("\n📋 Neue Testzeitraum-Meldung:")
        print("-" * 60)
        print("TESTZEITRAUM ABGELAUFEN für [Account-Name]")
        print("WICHTIG: Der kostenlose Testzeitraum kann nur EINMAL")
        print("pro Account-Name in Anspruch genommen werden.")
        print("\nOptionen:")
        print("1) RoboForex Partner werden unter forexsignale.trade/broker")
        print("   (Code: qnyj) für unbegrenzte Nutzung")
        print("2) Server-Lizenz erwerben")
        print("-" * 60)
        print("\n✅ Die Änderung ist sofort aktiv!")
    else:
        print("\n❌ Upload fehlgeschlagen!")

if __name__ == "__main__":
    main()