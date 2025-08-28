#!/usr/bin/env python3
import ftplib

# Upload fixed update_robo_status.php
ftp = ftplib.FTP("162.55.90.123")
ftp.login("prophelp", ".Propt333doka?")
ftp.cwd("/www/lic.prophelper.org/files/")

with open('update_robo_status.php', 'rb') as f:
    ftp.storbinary('STOR update_robo_status.php', f)
    
print("✓ Uploaded fixed update_robo_status.php with localhost MySQL connection")
ftp.quit()