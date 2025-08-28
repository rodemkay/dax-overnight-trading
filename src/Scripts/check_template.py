#!/usr/bin/env python3
import ftplib

# Download current template
ftp = ftplib.FTP("162.55.90.123")
ftp.login("prophelp", ".Propt333doka?")
ftp.cwd("/www/lic.prophelper.org/files/")

with open('template_broken.inc.php', 'wb') as f:
    ftp.retrbinary('RETR template.inc.php', f.write)
    
ftp.quit()
print("Downloaded broken template")

# Check the file
with open('template_broken.inc.php', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
    
print(f"Total lines: {len(lines)}")
print("\nLast 20 lines:")
for i, line in enumerate(lines[-20:], start=len(lines)-19):
    print(f"{i}: {line.rstrip()}")

# Check for missing closing brackets
open_brackets = 0
for i, line in enumerate(lines, 1):
    open_brackets += line.count('{') - line.count('}')
    
print(f"\nUnclosed brackets: {open_brackets}")

# Find problematic areas around line 334
print("\nLines around 330-340:")
for i in range(329, min(340, len(lines))):
    print(f"{i+1}: {lines[i].rstrip()}")