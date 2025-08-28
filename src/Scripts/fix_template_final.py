#!/usr/bin/env python3
"""
Final fix for template.inc.php - behebe alle Syntax-Fehler
"""

import ftplib
from datetime import datetime

# FTP Credentials
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_PATH = "/www/lic.prophelper.org/files/"

print("=== Final Template Fix ===\n")

# Download broken template
print("Downloading broken template...")
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(FTP_PATH)

# Backup current broken version
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
try:
    ftp.rename('template.inc.php', f'template.inc.php.broken_{timestamp}')
    print(f"✓ Backup created: template.inc.php.broken_{timestamp}")
except:
    pass

# Get original clean template from backup
files = []
ftp.retrlines('LIST', files.append)
backup_files = [f for f in files if 'template.inc.php.backup_2025' in f and 'broken' not in f]

if backup_files:
    # Use most recent good backup
    backup_name = backup_files[0].split()[-1]
    print(f"Using backup: {backup_name}")
    
    with open('template_clean.inc.php', 'wb') as f:
        ftp.retrbinary(f'RETR {backup_name}', f.write)
else:
    print("No clean backup found, downloading original from LicProphelper")
    # Use local copy
    import shutil
    shutil.copy('/home/rodemkay/mt5/daxovernight/LicProphelper/files/template.inc.php', 
                'template_clean.inc.php')

print("Creating fixed version...")

# Read clean template
with open('template_clean.inc.php', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Apply fixes properly
lines = content.split('\n')
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Add RoboForex header after Registrar column
    if '<td class="adm_ref">Registrar/Referal</td>' in line:
        new_lines.append(line)
        new_lines.append('\t\t<td style="text-align:center;width:80px;">RoboForex</td>')
        i += 1
        continue
    
    # Fix the registrar/roboforex display section
    if "if(\$res['registrar'] == \$res['ref'] || \$res['registrar'] =='site')" in line:
        # Add complete if-else structure with RoboForex column
        new_lines.append(line)  # if line
        i += 1
        new_lines.append(lines[i])  # first echo
        i += 1
        new_lines.append('\t\t} else {')
        new_lines.append('\t\techo \'<td class="adm_ref_t wrap \'.($_COOKIE[\'showAdm\']==1?\'active\':\'\').\'">\''
                        '.$res[\'registrar\'].\' (\'.$res[\'ref\'].\'(\'.$res[\'fee\'].\')</td>\';')
        new_lines.append('\t\t}')
        
        # Add RoboForex column
        new_lines.append('\t\t// RoboForex Partner Status')
        new_lines.append('\t\t$roboStatus = isset($res[\'roboaffiliate\']) ? $res[\'roboaffiliate\'] : \'no\';')
        new_lines.append('\t\tif($roboStatus == \'yes\' || $roboStatus == \'1\' || $roboStatus == 1) {')
        new_lines.append('\t\t\techo \'<td style="text-align:center;color:#00AA00;font-weight:bold;" title="RoboForex Partner">✓</td>\';')
        new_lines.append('\t\t} else {')
        new_lines.append('\t\t\techo \'<td style="text-align:center;color:#AA0000;" title="Not a RoboForex Partner">✗</td>\';')
        new_lines.append('\t\t}')
        
        # Skip original problematic lines
        while i < len(lines) and 'echo \'<td class="delete">\'' not in lines[i]:
            i += 1
        continue
    
    # Add sorting option for RoboForex
    if '<option value="12">Registrar/Referal</option>' in line:
        new_lines.append(line)
        new_lines.append('\t\t\t<option value="13">RoboForex Status</option>')
        i += 1
        continue
    
    # Add ORDER BY for RoboForex
    if 'case \'12\': $sql.=" ORDER BY `registrar`"; break;' in line:
        new_lines.append(line)
        new_lines.append('\t\tcase \'13\': $sql.=" ORDER BY `roboaffiliate` DESC"; break;')
        i += 1
        continue
    
    # Handle the search results section (around line 520)
    if i > 515 and "if(\$res['registrar'] == \$res['ref'] || \$res['registrar'] =='site')" in line:
        # Fix search results section
        new_lines.append(line)  # if line
        i += 1
        new_lines.append(lines[i])  # first SESSION append
        i += 1
        new_lines.append('\t\t} else {')
        new_lines.append('\t\t$_SESSION[\'search\'][$z-1].= \'<td class="adm_ref_t wrap \'.($_COOKIE[\'showAdm\']==1?\'active\':\'\').\'">\''
                        '.$res[\'registrar\'].\' (\'.$res[\'ref\'].\'(\'.$res[\'fee\'].\')</td>\';')
        new_lines.append('\t\t}')
        
        # Add RoboForex for search results
        new_lines.append('\t\t// RoboForex Partner Status')
        new_lines.append('\t\t$roboStatus = isset($res[\'roboaffiliate\']) ? $res[\'roboaffiliate\'] : \'no\';')
        new_lines.append('\t\tif($roboStatus == \'yes\' || $roboStatus == \'1\' || $roboStatus == 1) {')
        new_lines.append('\t\t\t$_SESSION[\'search\'][$z-1].= \'<td style="text-align:center;color:#00AA00;font-weight:bold;" title="RoboForex Partner">✓</td>\';')
        new_lines.append('\t\t} else {')
        new_lines.append('\t\t\t$_SESSION[\'search\'][$z-1].= \'<td style="text-align:center;color:#AA0000;" title="Not a RoboForex Partner">✗</td>\';')
        new_lines.append('\t\t}')
        
        # Skip problematic lines
        while i < len(lines) and not lines[i].strip().startswith('$_SESSION[\'search\'][$z-1].= \'<td class="delete"'):
            i += 1
        continue
    
    new_lines.append(line)
    i += 1

# Ensure file is properly closed
if not new_lines[-1].strip().endswith('}'):
    # Add missing closing brackets if needed
    new_lines.append('}')
    new_lines.append('}')
    new_lines.append('}')

# Save fixed version
fixed_content = '\n'.join(new_lines)
with open('template_fixed_final.inc.php', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✓ Fixed template created")

# Upload fixed version
print("Uploading fixed template...")
with open('template_fixed_final.inc.php', 'rb') as f:
    ftp.storbinary('STOR template.inc.php', f)

ftp.quit()
print("✓ Upload complete!")
print("\nThe template.inc.php has been fixed and uploaded.")
print("Test at: https://lic.prophelper.org/connect")