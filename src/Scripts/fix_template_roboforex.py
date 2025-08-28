#!/usr/bin/env python3
"""
Fix template.inc.php - Füge RoboForex-Spalte korrekt hinzu
"""

import ftplib
from datetime import datetime

# FTP Credentials
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_PATH = "/www/lic.prophelper.org/files/"

print("=== RoboForex Column Fix ===\n")

# Download current template
print("Downloading current template...")
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(FTP_PATH)

with open('template_current.inc.php', 'wb') as f:
    ftp.retrbinary('RETR template.inc.php', f.write)
print("✓ Downloaded")

# Read and analyze
with open('template_current.inc.php', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Check if RoboForex column exists
has_roboforex_header = 'RoboForex' in content
has_roboforex_display = 'roboaffiliate' in content

print(f"Has RoboForex header: {has_roboforex_header}")
print(f"Has roboaffiliate code: {has_roboforex_display}")

if not has_roboforex_header or not has_roboforex_display:
    print("\nAdding RoboForex column...")
    
    lines = content.split('\n')
    new_lines = []
    
    # Flags to track what we've added
    header_added = False
    display_added = False
    sort_added = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 1. Add header column after "Del" or before last </tr> in header
        if not header_added and '<th>' in line and '</tr>' in lines[i:i+5]:
            new_lines.append(line)
            # Look for Del column
            if 'Del' in line:
                # Add RoboForex header before Del
                new_lines.append('\t\t<th style="text-align:center;width:80px;">RoboForex</th>')
                header_added = True
                print("✓ Added RoboForex header")
            i += 1
            continue
            
        # 2. Add display logic after registrar display
        if not display_added and "echo '<td class=\"delete\">';" in line:
            # Add RoboForex display before delete button
            new_lines.append('\t\t// RoboForex Partner Status')
            new_lines.append('\t\t$roboStatus = isset($res[\'roboaffiliate\']) ? $res[\'roboaffiliate\'] : \'no\';')
            new_lines.append('\t\tif($roboStatus == \'yes\' || $roboStatus == \'1\' || $roboStatus == 1) {')
            new_lines.append('\t\t\techo \'<td style="text-align:center;color:#00AA00;font-weight:bold;" title="RoboForex Partner">✓</td>\';')
            new_lines.append('\t\t} else {')
            new_lines.append('\t\t\techo \'<td style="text-align:center;color:#AA0000;" title="Not a RoboForex Partner">✗</td>\';')
            new_lines.append('\t\t}')
            display_added = True
            print("✓ Added RoboForex display logic")
            new_lines.append(line)
            i += 1
            continue
            
        # 3. Add sort option
        if not sort_added and '<option value="12">Registrar/Referal</option>' in line:
            new_lines.append(line)
            new_lines.append('\t\t\t<option value="13">RoboForex Status</option>')
            sort_added = True
            print("✓ Added RoboForex sort option")
            i += 1
            continue
            
        # 4. Add ORDER BY clause
        if 'case \'12\': $sql.=" ORDER BY `registrar`"; break;' in line:
            new_lines.append(line)
            new_lines.append('\t\tcase \'13\': $sql.=" ORDER BY `roboaffiliate` DESC"; break;')
            print("✓ Added RoboForex ORDER BY")
            i += 1
            continue
            
        new_lines.append(line)
        i += 1
    
    # Save fixed version
    fixed_content = '\n'.join(new_lines)
    with open('template_fixed_roboforex.inc.php', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    print("\n✓ Fixed template created")
    
    # Backup and upload
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        ftp.rename('template.inc.php', f'template.inc.php.backup_{timestamp}')
        print(f"✓ Backup created: template.inc.php.backup_{timestamp}")
    except:
        pass
    
    # Upload fixed version
    with open('template_fixed_roboforex.inc.php', 'rb') as f:
        ftp.storbinary('STOR template.inc.php', f)
    print("✓ Uploaded fixed template")
else:
    print("\nRoboForex column code exists in template")
    print("Checking for other issues...")
    
    # Look for the actual table structure
    import re
    
    # Find table headers
    headers = re.findall(r'<th[^>]*>([^<]+)</th>', content)
    print(f"\nFound headers: {headers}")
    
    # Check if roboaffiliate is in SELECT
    if 'SELECT' in content:
        select_lines = [l for l in content.split('\n') if 'SELECT' in l.upper()]
        for sl in select_lines[:3]:
            print(f"SELECT: {sl[:100]}...")

ftp.quit()
print("\n✓ Complete! Check https://lic.prophelper.org/connect")