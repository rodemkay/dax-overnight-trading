#!/usr/bin/env python3
"""
WWW-Verzeichnisstruktur prüfen
"""

import ftplib

# FTP-Konfiguration
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"

def check_www():
    """Prüft die www-Verzeichnisstruktur"""
    
    print("=" * 60)
    print("WWW Verzeichnisstruktur prüfen")
    print("=" * 60)
    
    try:
        # FTP-Verbindung
        print(f"\n📡 Verbinde zu {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ Verbunden")
        
        # Zu www wechseln
        print("\n📂 Wechsle zu /www...")
        ftp.cwd('/www')
        print("✅ In /www angekommen")
        
        # Inhalt von www anzeigen
        print("\n📁 Inhalt von /www:")
        print("-" * 40)
        items = []
        ftp.retrlines('LIST', items.append)
        
        for item in items:
            print(item)
            
        # Prüfe auf Subdomains
        print("\n" + "-" * 40)
        print("📍 Prüfe auf lic.prophelper.org...")
        
        try:
            ftp.cwd('lic.prophelper.org')
            print("✅ /www/lic.prophelper.org existiert")
            
            # Inhalt anzeigen
            print("\n📁 Inhalt von /www/lic.prophelper.org:")
            print("-" * 40)
            items = []
            ftp.retrlines('LIST', items.append)
            
            for item in items:
                print(item)
                
            # Prüfe ob api-Verzeichnis existiert
            print("\n" + "-" * 40)
            try:
                ftp.cwd('api')
                print("✅ /www/lic.prophelper.org/api existiert")
                
                # Inhalt des api-Verzeichnisses
                print("\n📁 Inhalt von /www/lic.prophelper.org/api:")
                print("-" * 40)
                items = []
                ftp.retrlines('LIST', items.append)
                
                for item in items:
                    print(item)
                    
            except:
                print("⚠️  /www/lic.prophelper.org/api existiert NICHT")
                print("   Versuche api-Verzeichnis zu erstellen...")
                try:
                    ftp.mkd('api')
                    print("✅ /www/lic.prophelper.org/api wurde erstellt")
                except Exception as e:
                    print(f"❌ Konnte api-Verzeichnis nicht erstellen: {e}")
                    
        except Exception as e:
            print(f"❌ /www/lic.prophelper.org existiert nicht: {e}")
            
            # Zeige verfügbare Domains
            print("\n📍 Verfügbare Domains in /www:")
            ftp.cwd('/www')
            items = []
            ftp.retrlines('NLST', items.append)
            for item in items:
                if '.' in item:  # Wahrscheinlich eine Domain
                    print(f"  • {item}")
        
        ftp.quit()
        
        print("\n" + "=" * 60)
        print("✅ WWW-Check abgeschlossen")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        return False

if __name__ == "__main__":
    check_www()
