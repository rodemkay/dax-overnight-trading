#!/usr/bin/env python3
"""
WWW Verzeichnis prüfen
"""

import ftplib

# FTP-Zugangsdaten
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"

def check_www():
    """WWW Verzeichnis prüfen"""
    try:
        print(f"📡 Verbinde mit FTP-Server {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ FTP-Verbindung hergestellt\n")
        
        # In www wechseln
        ftp.cwd('www')
        print("📂 Inhalt von /www:")
        print("-" * 40)
        
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
            
        # Prüfe ob lic.prophelper.org existiert
        if 'lic.prophelper.org' in dirs:
            print("\n✅ lic.prophelper.org gefunden!")
            ftp.cwd('lic.prophelper.org')
            
            print("\n📂 Inhalt von /www/lic.prophelper.org:")
            dirs2 = []
            files2 = []
            
            ftp.retrlines('LIST', lambda x: parse_line2(x, dirs2, files2))
            
            def parse_line2(line, d, f):
                parts = line.split()
                if parts[0].startswith('d'):
                    d.append(parts[-1])
                else:
                    f.append(parts[-1])
            
            # Zeige Unterverzeichnisse
            subdirs = []
            ftp.retrlines('LIST', lambda x: subdirs.append(x.split()[-1] if x.startswith('d') else None))
            subdirs = [d for d in subdirs if d]
            
            print("Unterverzeichnisse:")
            for d in subdirs[:10]:
                print(f"  📁 {d}")
                
            # Prüfe ob files existiert
            try:
                ftp.cwd('files')
                print("\n✅ /www/lic.prophelper.org/files gefunden!")
                
                # Zeige PHP-Dateien
                print("\nPHP-Dateien in files:")
                php_files = []
                ftp.retrlines('LIST *.php', lambda x: php_files.append(x.split()[-1]))
                for f in php_files[:10]:
                    print(f"  📄 {f}")
                    
            except:
                print("❌ files Verzeichnis nicht gefunden")
        
        ftp.quit()
        
    except Exception as e:
        print(f"❌ Fehler: {e}")

if __name__ == "__main__":
    check_www()