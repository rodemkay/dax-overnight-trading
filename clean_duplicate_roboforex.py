#!/usr/bin/env python3
"""
Entferne doppelte RoboForex-Spalte
"""

import ftplib
from datetime import datetime

# FTP Credentials
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_PATH = "/www/lic.prophelper.org/files/"

print("=== Clean Duplicate RoboForex Column ===\n")

# Connect to FTP
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(FTP_PATH)

# Download current template
print("Downloading template.inc.php...")
with open('template_to_clean.inc.php', 'wb') as f:
    ftp.retrbinary('RETR template.inc.php', f.write)
print("✓ Downloaded")

# Read template
with open('template_to_clean.inc.php', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Remove duplicate RoboForex display
new_lines = []
skip_next = 0
robo_count = 0

for i, line in enumerate(lines):
    if skip_next > 0:
        skip_next -= 1
        continue
    
    # Check for duplicate RoboForex display
    if 'RoboForex Partner Status' in line and robo_count > 0:
        # Skip the next 6 lines (the duplicate display code)
        print(f"Removing duplicate RoboForex code at line {i+1}")
        skip_next = 6
        continue
    elif 'RoboForex Partner Status' in line:
        robo_count += 1
    
    # Check for duplicate table cell
    if i > 320 and i < 340:
        if '<td style="text-align:center;color:#00AA00;font-weight:bold;" title="RoboForex Partner">✓</td>' in line:
            # This is the old style, skip it
            print(f"Removing old style RoboForex cell at line {i+1}")
            continue
        elif '<td style="text-align:center;color:#AA0000;" title="Not a RoboForex Partner">✗</td>' in line:
            # This is the old style, skip it
            print(f"Removing old style RoboForex cell at line {i+1}")
            continue
    
    new_lines.append(line)

# Save cleaned version
with open('template_cleaned.inc.php', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("\n✓ Cleaned template saved")

# Backup and upload
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
try:
    ftp.rename('template.inc.php', f'template.inc.php.before_clean_{timestamp}')
    print(f"✓ Server backup: template.inc.php.before_clean_{timestamp}")
except:
    pass

# Upload cleaned version
with open('template_cleaned.inc.php', 'rb') as f:
    ftp.storbinary('STOR template.inc.php', f)
print("✓ Uploaded cleaned template")

ftp.quit()
print("\n✓ Done! Duplicate RoboForex columns removed")