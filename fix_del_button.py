#!/usr/bin/env python3
"""
Fix Del-Button der fälschlicherweise entfernt wurde
"""

import ftplib
from datetime import datetime

# FTP Credentials
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_PATH = "/www/lic.prophelper.org/files/"

print("=== Fix Del Button ===\n")

# Connect to FTP
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(FTP_PATH)

# Get backup before our changes
print("Looking for original backup...")
files = []
ftp.retrlines('LIST', files.append)

# Find a backup from before our changes
backup_files = [f for f in files if 'template.inc.php.backup_2025' in f and '1642' not in f and '1643' not in f]
if backup_files:
    backup_name = backup_files[-1].split()[-1]
    print(f"Using backup: {backup_name}")
    
    # Download original backup
    with open('template_original.inc.php', 'wb') as f:
        ftp.retrbinary(f'RETR {backup_name}', f.write)
else:
    print("No suitable backup found")
    
# Download current broken version
with open('template_current.inc.php', 'wb') as f:
    ftp.retrbinary('RETR template.inc.php', f.write)
print("✓ Downloaded current template")

# Read both files
with open('template_original.inc.php', 'r', encoding='utf-8', errors='ignore') as f:
    original_lines = f.readlines()

with open('template_current.inc.php', 'r', encoding='utf-8', errors='ignore') as f:
    current_lines = f.readlines()

# Find the Del button code in original
del_button_code = None
for i, line in enumerate(original_lines):
    if '<button type="submit" class="del_id"' in line:
        # Get the complete form block
        start = i - 5
        end = i + 2
        del_button_code = original_lines[start:end]
        print(f"Found Del button code at line {i+1}")
        break

# Now fix the current template
new_lines = []
roboforex_added = False

for i, line in enumerate(current_lines):
    # Keep the line
    new_lines.append(line)
    
    # After RoboForex display, ensure Del button exists
    if not roboforex_added and ('✗</span></td>' in line or '✓</span></td>' in line) and i < 350:
        roboforex_added = True
        # Check if next line has Del button
        if i+1 < len(current_lines) and '<td class="delete">' not in current_lines[i+1]:
            print(f"Adding Del button after RoboForex at line {i+1}")
            new_lines.append('\t\t<td class="delete">\n')
            new_lines.append('\t\t<form action="files/update.php" method="POST" class="del_form">\n')
            new_lines.append('\t\t<input type="hidden" name="update" value="9">\n')
            new_lines.append('\t\t<input type="hidden" name="field" value="del">\n')
            new_lines.append('\t\t<input type="hidden" name="id" value="\'.$ID.\'">\n')
            new_lines.append('\t\t<button type="submit" class="del_id" value=""></button>\n')
            new_lines.append('\t\t</form>\n')
            new_lines.append('\t\t</td>\n')

# Save fixed version
with open('template_fixed_del.inc.php', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("✓ Fixed template saved")

# Backup and upload
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
ftp.rename('template.inc.php', f'template.inc.php.broken_del_{timestamp}')
print(f"✓ Backup: template.inc.php.broken_del_{timestamp}")

# Upload fixed version
with open('template_fixed_del.inc.php', 'rb') as f:
    ftp.storbinary('STOR template.inc.php', f)
print("✓ Uploaded fixed template")

ftp.quit()
print("\n✓ Done! Del button should now work correctly")