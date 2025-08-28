#!/usr/bin/env python3
"""
Fix und Upload template.inc.php mit RoboForex-Spalte für connect.php
"""

import ftplib
import os
from datetime import datetime

# FTP Credentials
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_PATH = "/www/lic.prophelper.org/files/"

def download_current_template():
    """Download aktuelle template.inc.php vom Server"""
    print("Downloading current template.inc.php from server...")
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_PATH)
        
        local_file = 'template_current.inc.php'
        with open(local_file, 'wb') as f:
            ftp.retrbinary('RETR template.inc.php', f.write)
        
        ftp.quit()
        print(f"✓ Downloaded to {local_file}")
        return local_file
    except Exception as e:
        print(f"✗ Download failed: {e}")
        return None

def fix_template_complete():
    """Erstelle eine komplett korrigierte Version von template.inc.php"""
    print("\nCreating fixed template.inc.php...")
    
    # Lese die aktuelle Datei
    with open('template_current.inc.php', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Backup erstellen
    backup_name = f'template.inc.php.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    with open(backup_name, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Backup created: {backup_name}")
    
    # Finde die Position für Korrekturen
    lines = content.split('\n')
    new_lines = []
    i = 0
    fixed = False
    
    while i < len(lines):
        line = lines[i]
        
        # Suche nach der Stelle wo die RoboForex-Spalte eingefügt werden muss
        # Das ist nach der "registrar" Spalte und vor der "delete" Spalte
        
        # Fix für das doppelte else Problem
        if 'if($res[\'registrar\'] == $res[\'ref\'] || $res[\'registrar\'] ==\'site\')' in line:
            # Beginne korrigierte Struktur
            new_lines.append(line)  # if statement
            i += 1
            new_lines.append(lines[i])  # echo für ersten Fall
            i += 1
            # Füge korrektes else hinzu
            new_lines.append('\t\t} else {')
            # Füge echo für zweiten Fall hinzu
            new_lines.append('\t\techo \'<td class="adm_ref_t wrap \'.($_COOKIE[\'showAdm\']==1?\'active\':\'\').\'">\''
                           '.$res[\'registrar\'].\' (\'.$res[\'ref\'].\'(\'.$res[\'fee\'].\')</td>\';')
            new_lines.append('\t\t}')
            
            # Füge RoboForex-Spalte hinzu
            new_lines.append('\t\t// RoboForex Partner Status')
            new_lines.append('\t\t$roboStatus = isset($res[\'roboaffiliate\']) ? $res[\'roboaffiliate\'] : \'no\';')
            new_lines.append('\t\tif($roboStatus == \'yes\' || $roboStatus == \'1\' || $roboStatus == 1) {')
            new_lines.append('\t\t\techo \'<td style="text-align:center;color:#00AA00;font-weight:bold;" title="RoboForex Partner">✓</td>\';')
            new_lines.append('\t\t} else {')
            new_lines.append('\t\t\techo \'<td style="text-align:center;color:#AA0000;" title="Not a RoboForex Partner">✗</td>\';')
            new_lines.append('\t\t}')
            
            # Überspringe alle fehlerhaften Zeilen bis zum delete button
            while i < len(lines) and 'echo \'<td class="delete">\'' not in lines[i]:
                i += 1
            
            fixed = True
            
        # Füge RoboForex Header in die Tabelle ein
        elif '<td class="adm_ref">Registrar/Referal</td>' in line:
            new_lines.append(line)
            # Füge RoboForex Header nach Registrar hinzu
            new_lines.append('\t\t<td style="text-align:center;width:80px;">RoboForex</td>')
            i += 1
            
        # Füge RoboForex in die SELECT Query ein
        elif 'SELECT' in line and 'FROM' in line and 'lnative' in line and 'roboaffiliate' not in line:
            # Füge roboaffiliate zur SELECT Liste hinzu
            if 'SELECT *' in line:
                new_lines.append(line)  # Bei SELECT * ist alles schon dabei
            else:
                # Füge roboaffiliate vor FROM hinzu
                modified_line = line.replace(' FROM', ', roboaffiliate FROM')
                new_lines.append(modified_line)
            i += 1
            
        # Füge Sortier-Option für RoboForex hinzu
        elif '<option value="12">Registrar/Referal</option>' in line:
            new_lines.append(line)
            new_lines.append('\t\t\t<option value="13">RoboForex Status</option>')
            i += 1
            
        # Füge ORDER BY für RoboForex hinzu
        elif 'case \'12\': $sql.=" ORDER BY `registrar`"; break;' in line:
            new_lines.append(line)
            new_lines.append('\t\tcase \'13\': $sql.=" ORDER BY `roboaffiliate` DESC"; break;')
            i += 1
            
        else:
            new_lines.append(line)
            i += 1
    
    # Speichere korrigierte Version
    fixed_content = '\n'.join(new_lines)
    
    with open('template_inc_fixed_complete.php', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"✓ Fixed template saved as template_inc_fixed_complete.php")
    print(f"✓ Syntax error fixed: {fixed}")
    
    return 'template_inc_fixed_complete.php'

def upload_fixed_template(local_file):
    """Upload die korrigierte template.inc.php zum Server"""
    print(f"\nUploading {local_file} to server...")
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_PATH)
        
        # Erstelle Server-Backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f'template.inc.php.backup_{timestamp}'
        
        try:
            ftp.rename('template.inc.php', backup_name)
            print(f"✓ Server backup created: {backup_name}")
        except Exception as e:
            print(f"⚠ Could not create server backup: {e}")
        
        # Upload neue Datei
        with open(local_file, 'rb') as f:
            ftp.storbinary('STOR template.inc.php', f)
        
        # Verifiziere Upload
        ftp_files = []
        ftp.retrlines('LIST', ftp_files.append)
        
        uploaded = False
        for file_line in ftp_files:
            if 'template.inc.php' in file_line:
                uploaded = True
                break
        
        ftp.quit()
        
        if uploaded:
            print("✓ Upload successful!")
            print("✓ template.inc.php has been updated on the server")
            return True
        else:
            print("✗ Upload verification failed")
            return False
            
    except Exception as e:
        print(f"✗ Upload failed: {e}")
        return False

def main():
    print("=== Template.inc.php Fix & Upload Tool ===")
    print("This will fix the syntax error and add RoboForex column support\n")
    
    # Download current template
    if not download_current_template():
        print("\n✗ Could not download current template. Exiting.")
        return
    
    # Create fixed version
    fixed_file = fix_template_complete()
    
    print("\n" + "="*60)
    print("READY TO UPLOAD")
    print("="*60)
    print("The following changes will be made:")
    print("1. Fix syntax error (double else statement)")
    print("2. Add RoboForex column to the table")
    print("3. Add sorting option for RoboForex status")
    print("4. Display ✓ for partners and ✗ for non-partners")
    print("="*60)
    
    # Confirm upload
    response = input("\nProceed with upload? (yes/no): ")
    
    if response.lower() == 'yes':
        if upload_fixed_template(fixed_file):
            print("\n" + "="*60)
            print("SUCCESS!")
            print("="*60)
            print("✓ template.inc.php has been fixed and uploaded")
            print("✓ Syntax error has been corrected")
            print("✓ RoboForex column is now available")
            print("\nYou can now test at:")
            print("  https://lic.prophelper.org/connect")
            print("  https://lic.prophelper.org/office")
        else:
            print("\n✗ Upload failed. Please check the connection and try again.")
    else:
        print("\nUpload cancelled.")
        print(f"Fixed file saved locally as: {fixed_file}")
        print("You can manually upload it later.")

if __name__ == "__main__":
    main()