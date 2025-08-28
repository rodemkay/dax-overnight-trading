#!/usr/bin/env python3
"""
Untersucht die FTP-Server-Struktur und findet das URL-Routing
"""

from ftplib import FTP
import os

# FTP-Zugangsdaten
FTP_HOST = '162.55.90.123'
FTP_USER = 'prophelp'
FTP_PASS = '.Propt333doka?'

def list_directory(ftp, path='/'):
    """Listet alle Dateien und Verzeichnisse in einem Pfad"""
    try:
        ftp.cwd(path)
        items = []
        ftp.retrlines('LIST', items.append)
        return items
    except Exception as e:
        print(f"Fehler beim Auflisten von {path}: {e}")
        return []

def find_htaccess(ftp, start_path='/'):
    """Sucht nach .htaccess Dateien"""
    htaccess_files = []
    
    def search_dir(path):
        items = list_directory(ftp, path)
        for item in items:
            parts = item.split()
            if len(parts) >= 9:
                name = ' '.join(parts[8:])
                if name == '.htaccess':
                    htaccess_files.append(path + '/' + name)
                elif item.startswith('d') and name not in ['.', '..']:
                    # Rekursiv in Unterverzeichnisse
                    new_path = path.rstrip('/') + '/' + name
                    if new_path.count('/') < 4:  # Begrenze Tiefe
                        search_dir(new_path)
    
    search_dir(start_path)
    return htaccess_files

def download_htaccess(ftp, remote_path):
    """Lädt eine .htaccess Datei herunter und zeigt den Inhalt"""
    try:
        content = []
        ftp.retrlines(f'RETR {remote_path}', content.append)
        return '\n'.join(content)
    except Exception as e:
        print(f"Fehler beim Download von {remote_path}: {e}")
        return None

def main():
    print("=== FTP Server-Struktur Analyse ===\n")
    
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"✓ Verbunden mit FTP-Server {FTP_HOST}\n")
        
        # Root-Verzeichnis anzeigen
        print("=== Root-Verzeichnis ===")
        root_items = list_directory(ftp, '/')
        for item in root_items[:10]:  # Zeige nur erste 10
            print(item)
        
        # www Verzeichnis untersuchen
        print("\n=== /www Verzeichnis ===")
        www_items = list_directory(ftp, '/www')
        for item in www_items[:10]:
            print(item)
        
        # lic.prophelper.org Verzeichnis
        print("\n=== /www/lic.prophelper.org Verzeichnis ===")
        lic_items = list_directory(ftp, '/www/lic.prophelper.org')
        for item in lic_items:
            print(item)
        
        # Suche nach .htaccess
        print("\n=== Suche nach .htaccess Dateien ===")
        htaccess_files = find_htaccess(ftp, '/www/lic.prophelper.org')
        
        if htaccess_files:
            print(f"Gefundene .htaccess Dateien:")
            for htfile in htaccess_files:
                print(f"  • {htfile}")
                
            # Lade erste .htaccess
            print(f"\n=== Inhalt von {htaccess_files[0]} ===")
            content = download_htaccess(ftp, htaccess_files[0])
            if content:
                print(content)
        else:
            print("Keine .htaccess Dateien gefunden")
        
        # Prüfe ob es /office und /connect Verzeichnisse gibt
        print("\n=== Prüfe /office und /connect ===")
        for dir_name in ['office', 'connect', 'files']:
            path = f'/www/lic.prophelper.org/{dir_name}'
            items = list_directory(ftp, path)
            if items:
                print(f"\n{path} existiert:")
                for item in items[:5]:
                    print(f"  {item}")
            else:
                print(f"{path} existiert nicht oder ist leer")
        
        ftp.quit()
        
    except Exception as e:
        print(f"✗ Fehler: {e}")

if __name__ == "__main__":
    main()
