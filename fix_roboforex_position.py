#!/usr/bin/env python3
"""
Fix RoboForex column position and display
- Move after Account column
- Rename to "Robo"
- Fix empty display issue
"""

import ftplib
from datetime import datetime

# FTP Credentials
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_PATH = "/www/lic.prophelper.org/files/"

print("=== Fix RoboForex Column Position and Display ===\n")

# Connect to FTP
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(FTP_PATH)

# Download current template
print("Downloading template.inc.php...")
with open('template_current.inc.php', 'wb') as f:
    ftp.retrbinary('RETR template.inc.php', f.write)
print("✓ Downloaded")

# Read template
with open('template_current.inc.php', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # 1. Remove old RoboForex header from wrong position
    if '<th style="text-align:center;">RoboForex</th>' in line:
        print(f"Removing old RoboForex header at line {i+1}")
        i += 1
        continue
    
    # 2. Add new Robo header after Account column
    if '<th class="account">Account</th>' in line:
        new_lines.append(line)
        new_lines.append('\t<th style="text-align:center;width:50px;">Robo</th>\n')
        print(f"Added Robo header after Account at line {i+1}")
        i += 1
        continue
    
    # 3. Fix the display code - find the empty if/else blocks
    if i > 320 and i < 330:
        if line.strip() == '// RoboForex Partner Status':
            # Found the RoboForex display section
            new_lines.append(line)  # Keep comment
            i += 1
            
            # Add proper display code
            new_lines.append('\t\t$roboStatus = isset($res[\'roboaffiliate\']) ? $res[\'roboaffiliate\'] : \'no\';\n')
            new_lines.append('\t\tif($roboStatus == \'yes\' || $roboStatus == \'1\' || $roboStatus == 1) {\n')
            new_lines.append('\t\t\techo \'<td style="text-align:center;"><span style="color:#00AA00;font-weight:bold;" title="Partner">✓</span></td>\';\n')
            new_lines.append('\t\t} else {\n')
            new_lines.append('\t\t\techo \'<td style="text-align:center;"><span style="color:#AA0000;" title="No Partner">✗</span></td>\';\n')
            new_lines.append('\t\t}\n')
            
            # Skip the old empty if/else blocks
            while i < len(lines):
                if '} else {' in lines[i]:
                    i += 1
                    if '}' in lines[i]:
                        i += 1
                        break
                i += 1
            continue
    
    # 4. Move display to after account column (around line 285)
    if '<td class="account"><span class="cacc">' in line and '$res[\'account\']' in line:
        new_lines.append(line)
        # Add RoboForex display right after account
        new_lines.append('\t\t// RoboForex Status\n')
        new_lines.append('\t\t$roboStatus = isset($res[\'roboaffiliate\']) ? $res[\'roboaffiliate\'] : \'no\';\n')
        new_lines.append('\t\tif($roboStatus == \'yes\' || $roboStatus == \'1\' || $roboStatus == 1) {\n')
        new_lines.append('\t\t\techo \'<td style="text-align:center;"><span style="color:#00AA00;font-weight:bold;" title="Partner">✓</span></td>\';\n')
        new_lines.append('\t\t} else {\n')
        new_lines.append('\t\t\techo \'<td style="text-align:center;"><span style="color:#AA0000;" title="No Partner">✗</span></td>\';\n')
        new_lines.append('\t\t}\n')
        print(f"Added RoboForex display after account at line {i+1}")
        i += 1
        continue
    
    # 5. Also fix for search results section (around line 482)
    if i > 480 and i < 490 and '$_SESSION[\'search\'][$z-1].= \'<td class="account">' in line:
        new_lines.append(line)
        # Add RoboForex for search results
        new_lines.append('\t\t// RoboForex Status\n')
        new_lines.append('\t\t$roboStatus = isset($res[\'roboaffiliate\']) ? $res[\'roboaffiliate\'] : \'no\';\n')
        new_lines.append('\t\tif($roboStatus == \'yes\' || $roboStatus == \'1\' || $roboStatus == 1) {\n')
        new_lines.append('\t\t\t$_SESSION[\'search\'][$z-1].= \'<td style="text-align:center;"><span style="color:#00AA00;font-weight:bold;" title="Partner">✓</span></td>\';\n')
        new_lines.append('\t\t} else {\n')
        new_lines.append('\t\t\t$_SESSION[\'search\'][$z-1].= \'<td style="text-align:center;"><span style="color:#AA0000;" title="No Partner">✗</span></td>\';\n')
        new_lines.append('\t\t}\n')
        print(f"Added RoboForex display for search at line {i+1}")
        i += 1
        continue
    
    # 6. Fix search results header (around line 571)
    if i > 570 and i < 580 and '<th class="account">Account</th>' in line:
        new_lines.append(line)
        new_lines.append('\t<th style="text-align:center;width:50px;">Robo</th>\n')
        print(f"Added Robo header in search at line {i+1}")
        i += 1
        continue
    
    # Keep all other lines
    new_lines.append(line)
    i += 1

# Save fixed version
with open('template_fixed_robo.inc.php', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("\n✓ Fixed template saved")

# Backup and upload
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
try:
    ftp.rename('template.inc.php', f'template.inc.php.backup_{timestamp}')
    print(f"✓ Server backup: template.inc.php.backup_{timestamp}")
except:
    pass

# Upload fixed version
with open('template_fixed_robo.inc.php', 'rb') as f:
    ftp.storbinary('STOR template.inc.php', f)
print("✓ Uploaded fixed template")

ftp.quit()
print("\n✓ Done! RoboForex column moved after Account and renamed to 'Robo'")