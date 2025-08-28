#!/usr/bin/env python3
"""
Füge RoboForex-Spalte in template.inc.php ein
"""

import ftplib
from datetime import datetime

# FTP Credentials
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_PATH = "/www/lic.prophelper.org/files/"

print("=== Adding RoboForex Column to Template ===\n")

# Connect to FTP
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(FTP_PATH)

# Download current template
print("Downloading template.inc.php...")
with open('template.inc.php', 'wb') as f:
    ftp.retrbinary('RETR template.inc.php', f.write)
print("✓ Downloaded")

# Read template
with open('template.inc.php', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Find and modify
new_lines = []
header_modified = False
display_modified = False
search_header_modified = False
search_display_modified = False

for i, line in enumerate(lines):
    # 1. Add header column BEFORE Del column in main table (around line 205)
    if i > 200 and i < 210 and '<th>Del</th>' in line and not header_modified:
        # Add RoboForex header before Del
        new_lines.append('\t<th style="text-align:center;">RoboForex</th>\n')
        new_lines.append(line)
        header_modified = True
        print(f"✓ Added RoboForex header at line {i+1}")
        continue
    
    # 2. Add display code BEFORE delete button (around line 330)
    if i > 325 and i < 335 and "echo '<td class=\"delete\">';" in line and not display_modified:
        # Add RoboForex display
        new_lines.append('\t\t// RoboForex Partner Status\n')
        new_lines.append('\t\t$roboStatus = isset($res[\'roboaffiliate\']) ? $res[\'roboaffiliate\'] : \'no\';\n')
        new_lines.append('\t\tif($roboStatus == \'yes\' || $roboStatus == \'1\' || $roboStatus == 1) {\n')
        new_lines.append('\t\t\techo \'<td style="text-align:center;"><span style="color:#00AA00;font-weight:bold;" title="RoboForex Partner">✓</span></td>\';\n')
        new_lines.append('\t\t} else {\n')
        new_lines.append('\t\t\techo \'<td style="text-align:center;"><span style="color:#AA0000;" title="Not a Partner">✗</span></td>\';\n')
        new_lines.append('\t\t}\n')
        new_lines.append(line)
        display_modified = True
        print(f"✓ Added RoboForex display at line {i+1}")
        continue
    
    # 3. Add header in search results table (around line 579)
    if i > 575 and i < 585 and '<th>Del</th>' in line and not search_header_modified:
        # Add RoboForex header before Del in search results
        new_lines.append('\t<th style="text-align:center;">RoboForex</th>\n')
        new_lines.append(line)
        search_header_modified = True
        print(f"✓ Added RoboForex header in search at line {i+1}")
        continue
    
    # 4. Add display in search results (around line 525)
    if i > 520 and i < 530 and "$_SESSION['search'][\$z-1].= '<td class=\"delete\">';" in line and not search_display_modified:
        # Add RoboForex display for search results
        new_lines.append('\t\t// RoboForex Partner Status\n')
        new_lines.append('\t\t$roboStatus = isset($res[\'roboaffiliate\']) ? $res[\'roboaffiliate\'] : \'no\';\n')
        new_lines.append('\t\tif($roboStatus == \'yes\' || $roboStatus == \'1\' || $roboStatus == 1) {\n')
        new_lines.append('\t\t\t$_SESSION[\'search\'][$z-1].= \'<td style="text-align:center;"><span style="color:#00AA00;font-weight:bold;" title="RoboForex Partner">✓</span></td>\';\n')
        new_lines.append('\t\t} else {\n')
        new_lines.append('\t\t\t$_SESSION[\'search\'][$z-1].= \'<td style="text-align:center;"><span style="color:#AA0000;" title="Not a Partner">✗</span></td>\';\n')
        new_lines.append('\t\t}\n')
        new_lines.append(line)
        search_display_modified = True
        print(f"✓ Added RoboForex display in search at line {i+1}")
        continue
    
    # Keep original line
    new_lines.append(line)

# Check what was modified
print(f"\nModifications:")
print(f"- Main header: {header_modified}")
print(f"- Main display: {display_modified}")
print(f"- Search header: {search_header_modified}")
print(f"- Search display: {search_display_modified}")

if header_modified or display_modified:
    # Save modified version
    with open('template_with_roboforex.inc.php', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("\n✓ Modified template saved")
    
    # Backup current on server
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        ftp.rename('template.inc.php', f'template.inc.php.backup_{timestamp}')
        print(f"✓ Server backup: template.inc.php.backup_{timestamp}")
    except:
        pass
    
    # Upload modified version
    with open('template_with_roboforex.inc.php', 'rb') as f:
        ftp.storbinary('STOR template.inc.php', f)
    print("✓ Uploaded modified template")
else:
    print("\n⚠ No modifications made - column may already exist")

ftp.quit()
print("\n✓ Done! Check https://lic.prophelper.org/connect")