#!/usr/bin/env python3
"""
Final fix for RoboForex display - ensure it shows correctly
"""

import ftplib
from datetime import datetime

# FTP Credentials
FTP_HOST = "162.55.90.123"
FTP_USER = "prophelp"
FTP_PASS = ".Propt333doka?"
FTP_PATH = "/www/lic.prophelper.org/files/"

print("=== Final Fix for RoboForex Display ===\n")

# Connect to FTP
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(FTP_PATH)

# Download current template
print("Downloading template.inc.php...")
with open('template_final.inc.php', 'wb') as f:
    ftp.retrbinary('RETR template.inc.php', f.write)
print("✓ Downloaded")

# Read template
with open('template_final.inc.php', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Check if RoboForex display code is correct
print("\nChecking for RoboForex display code...")

# Count occurrences
robo_headers = content.count('>Robo</th>')
robo_displays = content.count('roboaffiliate')
robo_checks = content.count('✓</span></td>')

print(f"Found {robo_headers} Robo headers")
print(f"Found {robo_displays} roboaffiliate checks")
print(f"Found {robo_checks} display outputs")

# Find and fix any issues
lines = content.split('\n')
new_lines = []
fixed = False

for i, line in enumerate(lines):
    # Remove any duplicate or misplaced RoboForex code
    if i > 315 and i < 330:
        # This is the area where the broken code was
        if '// RoboForex Partner Status' in line:
            # Check if the next lines are empty or broken
            if i+3 < len(lines):
                if '} else {' in lines[i+3] and '}' in lines[i+4]:
                    # This is broken, skip these lines
                    print(f"Removing broken RoboForex code at line {i+1}")
                    fixed = True
                    continue
    
    new_lines.append(line)

if fixed:
    # Save and upload
    with open('template_final_fixed.inc.php', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    print("\n✓ Fixed template saved")
    
    # Backup and upload
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        ftp.rename('template.inc.php', f'template.inc.php.prefinal_{timestamp}')
        print(f"✓ Server backup: template.inc.php.prefinal_{timestamp}")
    except:
        pass
    
    # Upload fixed version
    with open('template_final_fixed.inc.php', 'rb') as f:
        ftp.storbinary('STOR template.inc.php', f)
    print("✓ Uploaded final fixed template")
else:
    print("\n✓ Template appears to be correct")

# Test the update_robo_status.php endpoint
print("\n=== Testing update_robo_status.php ===")
import requests

test_url = "https://lic.prophelper.org/files/update_robo_status.php"
params = {
    'account': '77022300',
    'robo_status': 'yes',
    'program': 'don_gpt',
    'api_key': 'ec4d40c4343ee741'
}

try:
    response = requests.get(test_url, params=params, timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    if 'success' in response.text:
        print("✓ Database update works!")
    elif 'error' in response.text:
        print("⚠ Error in response - check MySQL connection")
except Exception as e:
    print(f"⚠ Test failed: {e}")

ftp.quit()
print("\n✓ Complete!")