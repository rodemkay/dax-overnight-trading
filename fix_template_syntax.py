#!/usr/bin/env python3
"""
Fix template.inc.php Syntax-Fehler und implementiere RoboForex-Spalte
"""

import ftplib
import os
from datetime import datetime

# FTP Credentials
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_PATH = "/www/lic.prophelper.org/files/"

def download_file():
    """Download template.inc.php vom FTP Server"""
    print("Downloading template.inc.php...")
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_PATH)
        
        local_file = 'template.inc.php'
        with open(local_file, 'wb') as f:
            ftp.retrbinary('RETR template.inc.php', f.write)
        
        ftp.quit()
        print(f"✓ Downloaded to {local_file}")
        return local_file
    except Exception as e:
        print(f"✗ Download failed: {e}")
        return None

def fix_template():
    """Korrigiere den Syntax-Fehler und füge RoboForex-Spalte hinzu"""
    print("\nFixing template.inc.php...")
    
    with open('template.inc.php', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Backup erstellen
    backup_name = f'template.inc.php.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    with open(backup_name, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"✓ Backup created: {backup_name}")
    
    # Finde und korrigiere den Fehler
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Suche nach dem problematischen Bereich (um Zeile 320-340)
        if i >= 315 and i <= 340:
            # Prüfe auf das doppelte else Problem
            if 'if($res[\'registrar\'] == $res[\'ref\'] || $res[\'registrar\'] ==\'site\')' in line:
                # Beginne die korrekte Struktur
                fixed_lines.append(line)
                i += 1
                # Füge den ersten echo hinzu
                fixed_lines.append(lines[i])  # echo '<td class="adm_ref_t...
                i += 1
                # Füge das korrekte else hinzu
                fixed_lines.append('\t\t} else {\n')
                # Füge den zweiten echo hinzu
                fixed_lines.append('\t\techo \'<td class="adm_ref_t wrap \'.($_COOKIE[\'showAdm\']==1?\'active\':\'\').\'">\''
                                 '.$res[\'registrar\'].\' (\'.$res[\'ref\'].\'(\'.$res[\'fee\'].\')</td>\';\n')
                fixed_lines.append('\t\t}\n')
                
                # Füge RoboForex-Spalte für connect.php hinzu
                fixed_lines.append('\t\t// RoboForex Partner Status\n')
                fixed_lines.append('\t\t$roboStatus = isset($res[\'roboaffiliate\']) ? $res[\'roboaffiliate\'] : \'no\';\n')
                fixed_lines.append('\t\tif($roboStatus == \'yes\' || $roboStatus == \'1\' || $roboStatus == 1) {\n')
                fixed_lines.append('\t\t\techo \'<td style="text-align:center;color:#00AA00;font-weight:bold;">✓</td>\';\n')
                fixed_lines.append('\t\t} else {\n')
                fixed_lines.append('\t\t\techo \'<td style="text-align:center;color:#AA0000;">✗</td>\';\n')
                fixed_lines.append('\t\t}\n')
                
                # Überspringe die fehlerhaften Zeilen im Original
                while i < len(lines):
                    if 'echo \'<td class="delete">\'' in lines[i]:
                        break
                    i += 1
            else:
                fixed_lines.append(line)
                i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    # Speichere die korrigierte Version
    with open('template_inc_fixed.php', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("✓ Fixed template saved as template_inc_fixed.php")
    return 'template_inc_fixed.php'

def upload_file(local_file):
    """Upload korrigierte Datei zum FTP Server"""
    print(f"\nUploading {local_file} to server...")
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_PATH)
        
        # Backup auf Server erstellen
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        try:
            ftp.rename('template.inc.php', f'template.inc.php.backup_{timestamp}')
            print(f"✓ Server backup created: template.inc.php.backup_{timestamp}")
        except:
            pass
        
        # Upload neue Datei
        with open(local_file, 'rb') as f:
            ftp.storbinary('STOR template.inc.php', f)
        
        ftp.quit()
        print("✓ Upload successful!")
        return True
    except Exception as e:
        print(f"✗ Upload failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Template.inc.php Syntax Fix ===\n")
    
    # Download original
    if download_file():
        # Fix syntax error
        fixed_file = fix_template()
        
        # Ask for confirmation before upload
        print("\n" + "="*50)
        print("Ready to upload fixed template.inc.php")
        print("This will:")
        print("1. Create backup on server")
        print("2. Replace template.inc.php with fixed version")
        print("3. Add RoboForex column support")
        print("="*50)
        
        response = input("\nProceed with upload? (yes/no): ")
        if response.lower() == 'yes':
            if upload_file(fixed_file):
                print("\n✓ Template.inc.php successfully fixed and uploaded!")
                print("✓ RoboForex column is now available in connect.php")
            else:
                print("\n✗ Upload failed. Please check connection and try again.")
        else:
            print("\nUpload cancelled. Fixed file saved locally as template_inc_fixed.php")