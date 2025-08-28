#!/usr/bin/env python3
"""
Complete fix for Robo column - add headers and ensure display works
"""

import ftplib
from datetime import datetime

# FTP Credentials
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_PATH = "/www/lic.prophelper.org/files/"

print("=== Complete Robo Column Fix ===\n")

# Connect to FTP
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(FTP_PATH)

# Download current template
with open('template.inc.php', 'wb') as f:
    ftp.retrbinary('RETR template.inc.php', f.write)
print("✓ Downloaded template")

# Read template
with open('template.inc.php', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

new_lines = []
header_added = False
search_header_added = False

for i, line in enumerate(lines):
    # 1. Add Robo header after Account in main table (around line 183)
    if not header_added and '<th class="account">Account</th>' in line:
        new_lines.append(line)
        new_lines.append('\t<th style="text-align:center;width:50px;">Robo</th>\n')
        header_added = True
        print(f"Added Robo header after Account at line {i+1}")
        continue
    
    # 2. Add Robo header in search results (around line 571)
    if not search_header_added and i > 560 and '<th class="account">Account</th>' in line:
        new_lines.append(line)
        new_lines.append('\t<th style="text-align:center;width:50px;">Robo</th>\n')
        search_header_added = True
        print(f"Added Robo header in search at line {i+1}")
        continue
    
    # 3. Remove old RoboForex headers from wrong position
    if '<th style="text-align:center;">RoboForex</th>' in line:
        print(f"Removing old RoboForex header at line {i+1}")
        continue
    
    new_lines.append(line)

# Save fixed version
with open('template_complete.inc.php', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("\n✓ Fixed template saved")

# Backup and upload
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
try:
    ftp.rename('template.inc.php', f'template.inc.php.before_complete_{timestamp}')
    print(f"✓ Backup: template.inc.php.before_complete_{timestamp}")
except:
    pass

# Upload
with open('template_complete.inc.php', 'rb') as f:
    ftp.storbinary('STOR template.inc.php', f)
print("✓ Uploaded complete template")

ftp.quit()
print("\n✓ Done! Robo column should now appear after Account column")