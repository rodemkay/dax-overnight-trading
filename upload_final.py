#!/usr/bin/env python3
"""
Upload der finalen modifizierten template.inc.php zum FTP-Server
Mit Backup-Erstellung und Bestätigung
"""

from ftplib import FTP
import os
from datetime import datetime

# FTP-Zugangsdaten
FTP_HOST = '162.55.90.123'
FTP_USER = 'prophelp'
FTP_PASS = '.Propt333doka?'

def create_backup(ftp):
    """Erstellt ein Backup der existierenden Datei"""
    try:
        remote_file = '/www/lic.prophelper.org/files/template.inc.php'
        backup_name = f'/www/lic.prophelper.org/files/template.inc.php.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        
        # Erstelle Backup durch Kopieren
        ftp.rename(remote_file, backup_name)
        print(f"✓ Backup erstellt: {backup_name}")
        return backup_name
    except Exception as e:
        print(f"⚠ Backup fehlgeschlagen: {e}")
        return None

def restore_backup(ftp, backup_name):
    """Stellt das Backup wieder her"""
    try:
        remote_file = '/www/lic.prophelper.org/files/template.inc.php'
        ftp.rename(backup_name, remote_file)
        print(f"✓ Backup wiederhergestellt")
        return True
    except Exception as e:
        print(f"✗ Wiederherstellung fehlgeschlagen: {e}")
        return False

def upload_file(local_path):
    """Upload der modifizierten Datei zum FTP-Server"""
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"✓ Verbunden mit FTP-Server {FTP_HOST}")
        
        remote_file = '/www/lic.prophelper.org/files/template.inc.php'
        
        # Backup erstellen
        print(f"\nErstelle Backup...")
        backup_name = create_backup(ftp)
        
        if not backup_name:
            print("✗ Abbruch: Kein Backup möglich")
            ftp.quit()
            return False
        
        # Neue Datei hochladen
        print(f"\nLade modifizierte Datei hoch...")
        with open(local_path, 'rb') as local_file:
            ftp.storbinary(f'STOR {remote_file}', local_file)
        
        # Dateigröße prüfen
        local_size = os.path.getsize(local_path)
        remote_size = ftp.size(remote_file)
        
        print(f"✓ Upload erfolgreich")
        print(f"  Lokale Größe:  {local_size:,} bytes")
        print(f"  Remote Größe:  {remote_size:,} bytes")
        
        if abs(local_size - remote_size) > 100:
            print("⚠ WARNUNG: Dateigrößen unterscheiden sich stark!")
            print("Möchten Sie das Backup wiederherstellen? (j/n): ", end="")
            if input().lower() == 'j':
                restore_backup(ftp, backup_name)
        
        ftp.quit()
        return True
        
    except Exception as e:
        print(f"✗ Fehler beim Upload: {e}")
        return False

def verify_changes(local_path):
    """Zeigt die wichtigsten Änderungen"""
    print("\n=== ÜBERPRÜFUNG DER ÄNDERUNGEN ===")
    
    with open(local_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ('SELECT mit roboaffiliate', 'SELECT full_name,program,test,ip,serialNo,roboaffiliate'),
        ('Sort-Option RoboForex', '<option value="13"'),
        ('Sort-Query roboaffiliate', 'ORDER BY `roboaffiliate`'),
        ('Header RoboForex', '<th>RoboForex</th>'),
        ('Account mit accountLogin', 'accountLogin'),
        ('RoboForex Status Check', '✓</td>'),
    ]
    
    for name, search in checks:
        if search in content:
            print(f"✓ {name}")
        else:
            print(f"✗ {name} FEHLT!")
    
    print(f"\nDateigröße: {os.path.getsize(local_path):,} bytes")
    lines = content.count('\n')
    print(f"Zeilen: {lines}")

if __name__ == "__main__":
    print("=== FTP Upload: Modifizierte template.inc.php ===\n")
    
    local_file = 's:\\mt5\\daxovernight\\template_inc_complete.php'
    
    # Prüfen ob Datei existiert
    if not os.path.exists(local_file):
        print(f"✗ Datei nicht gefunden: {local_file}")
        exit(1)
    
    # Änderungen verifizieren
    verify_changes(local_file)
    
    # Benutzer fragen
    print("\n" + "="*50)
    print("WICHTIG: Diese Aktion wird die template.inc.php")
    print("auf dem Live-Server ersetzen!")
    print("="*50)
    print("\nFolgende Änderungen werden hochgeladen:")
    print("• RoboForex Partner-Spalte in der Benutzertabelle")
    print("• Sortierung nach RoboForex-Status")
    print("• Account-Anzeige mit accountLogin")
    print("• Status-Anzeige als ✓ (Partner) oder ✗ (kein Partner)")
    
    print("\nMöchten Sie fortfahren? (j/n): ", end="")
    
    if input().lower() == 'j':
        print("\nStarte Upload...")
        if upload_file(local_file):
            print("\n" + "="*50)
            print("✓ ERFOLGREICH HOCHGELADEN!")
            print("="*50)
            print("\nDie Änderungen sind jetzt live auf:")
            print("• https://lic.prophelper.org/files/office.php")
            print("• https://lic.prophelper.org/files/metatrader.php")
            print("\nBitte testen Sie die neue RoboForex-Spalte!")
        else:
            print("\n✗ Upload fehlgeschlagen!")
    else:
        print("\nAbgebrochen.")
