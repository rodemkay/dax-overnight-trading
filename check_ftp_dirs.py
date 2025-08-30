#!/usr/bin/env python3
"""
FTP Verzeichnisse prüfen
"""

import ftplib

# FTP-Zugangsdaten
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"

def check_directories():
    """Verfügbare Verzeichnisse anzeigen"""
    try:
        print(f"📡 Verbinde mit FTP-Server {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ FTP-Verbindung hergestellt\n")
        
        print("📂 Verfügbare Verzeichnisse:")
        print("-" * 40)
        
        # Root-Verzeichnis anzeigen
        dirs = []
        files = []
        
        def parse_line(line):
            parts = line.split()
            if parts[0].startswith('d'):
                dirs.append(parts[-1])
            else:
                files.append(parts[-1])
        
        ftp.retrlines('LIST', parse_line)
        
        print("\nVerzeichnisse:")
        for d in sorted(dirs):
            print(f"  📁 {d}")
            
        print("\nDateien im Root:")
        for f in sorted(files)[:10]:  # Nur erste 10 Dateien
            print(f"  📄 {f}")
            
        # Prüfe ob files Verzeichnis existiert
        print("\n" + "=" * 40)
        print("Suche 'files' Verzeichnis...")
        
        try:
            ftp.cwd('files')
            print("✅ /files gefunden!")
            
            # Zeige Inhalt
            print("\nInhalt von /files:")
            files_content = []
            ftp.retrlines('LIST', lambda x: files_content.append(x))
            for line in files_content[:5]:
                print(f"  {line}")
                
            # Zurück zum Root
            ftp.cwd('/')
        except:
            print("❌ /files nicht gefunden")
            
        # Prüfe ob public_html existiert
        try:
            ftp.cwd('public_html')
            print("\n✅ /public_html gefunden!")
            
            # Prüfe ob files darin ist
            try:
                ftp.cwd('files')
                print("✅ /public_html/files gefunden!")
            except:
                print("❌ /public_html/files nicht gefunden")
        except:
            print("❌ /public_html nicht gefunden")
            
        ftp.quit()
        
    except Exception as e:
        print(f"❌ Fehler: {e}")

if __name__ == "__main__":
    check_directories()