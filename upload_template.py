#!/usr/bin/env python3
"""
Upload der modifizierten template.inc.php zum FTP-Server
"""

from ftplib import FTP
import os
from datetime import datetime

# FTP-Zugangsdaten
FTP_HOST = '162.55.90.123'
FTP_USER = 'prophelp'
FTP_PASS = '.Propt333doka?'

def create_backup(ftp, remote_path):
    """Erstellt ein Backup der existierenden Datei"""
    try:
        # Backup-Name mit Zeitstempel
        backup_name = remote_path + '.backup_' + datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Existierende Datei umbenennen
        ftp.rename(remote_path, backup_name)
        print(f"✓ Backup erstellt: {backup_name}")
        return True
    except Exception as e:
        print(f"⚠ Backup fehlgeschlagen: {e}")
        return False

def upload_file(local_path, remote_path):
    """Upload einer Datei zum FTP-Server"""
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"✓ Verbunden mit FTP-Server {FTP_HOST}")
        
        # Backup erstellen
        print(f"\nErstelle Backup von {remote_path}...")
        create_backup(ftp, remote_path)
        
        # Neue Datei hochladen
        print(f"\nLade neue Datei hoch...")
        with open(local_path, 'rb') as local_file:
            ftp.storbinary(f'STOR {remote_path}', local_file)
        print(f"✓ Hochgeladen: {local_path} → {remote_path}")
        
        # Dateigröße prüfen
        size = ftp.size(remote_path)
        print(f"✓ Dateigröße auf Server: {size} bytes")
        
        ftp.quit()
        return True
    except Exception as e:
        print(f"✗ Fehler: {e}")
        return False

def check_file(remote_path):
    """Prüft ob die Datei auf dem Server existiert"""
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        
        size = ftp.size(remote_path)
        print(f"✓ Datei existiert: {remote_path} ({size} bytes)")
        
        ftp.quit()
        return True
    except:
        print(f"✗ Datei nicht gefunden: {remote_path}")
        return False

# Hauptprogramm
if __name__ == "__main__":
    print("=== FTP Upload: template.inc.php ===")
    
    # Lokale und remote Pfade
    local_file = 's:\\mt5\\daxovernight\\template.inc.php'  # Original
    modified_file = 's:\\mt5\\daxovernight\\template_inc_modified.php'
    remote_file = '/www/lic.prophelper.org/files/template.inc.php'
    
    # Prüfen ob lokale Dateien existieren
    if not os.path.exists(local_file):
        print(f"✗ Lokale Datei nicht gefunden: {local_file}")
        exit(1)
    
    print(f"\nLokale Original-Datei: {os.path.getsize(local_file)} bytes")
    
    if os.path.exists(modified_file):
        print(f"Modifizierte Datei vorhanden: {os.path.getsize(modified_file)} bytes")
    
    # Prüfen ob Datei auf Server existiert
    print(f"\nPrüfe Server-Status...")
    check_file(remote_file)
    
    # Benutzer fragen
    print("\n" + "="*50)
    print("WARNUNG: Die modifizierte Datei ist noch nicht vollständig!")
    print("Sie wurde bei Zeile 307 abgeschnitten.")
    print("Die Original-Datei hat 748 Zeilen.")
    print("="*50)
    print("\nMöchten Sie:")
    print("1. Die vollständige modifizierte Datei erstellen")
    print("2. Nur die Änderungen anzeigen")
    print("3. Abbrechen")
    
    choice = input("\nIhre Wahl (1-3): ")
    
    if choice == '1':
        print("\nErstelle vollständige modifizierte Datei...")
        # Hier würde die vollständige Datei erstellt werden
        print("✓ Datei wird vorbereitet...")
    elif choice == '2':
        print("\n=== ÄNDERUNGEN ===")
        print("1. SQL Query erweitert: SELECT ... roboaffiliate")
        print("2. Sort-Option hinzugefügt: value=13 'RoboForex Partner'")
        print("3. Sort-Query hinzugefügt: ORDER BY roboaffiliate")
        print("4. Tabellen-Header erweitert: <th>RoboForex</th>")
        print("5. Neue Spalte mit Status-Anzeige (✓/✗)")
        print("6. Account-Anzeige nutzt jetzt accountLogin wenn vorhanden")
    else:
        print("Abgebrochen.")
