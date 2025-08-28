#!/usr/bin/env python3
import ftplib

ftp = ftplib.FTP("162.55.90.123")
ftp.login("prophelp", ".Propt333doka?")
print("Connected to FTP")
print("Current directory:", ftp.pwd())
print("\nListing directories:")
dirs = []
ftp.retrlines('LIST', dirs.append)
for d in dirs[:20]:
    print(d)

# Try to find files directory
print("\nTrying different paths:")
paths = ["/files", "files", "/www/lic.prophelper.org/files", "www/lic.prophelper.org/files"]
for path in paths:
    try:
        ftp.cwd(path)
        print(f"✓ Found: {path}")
        print(f"  Current dir: {ftp.pwd()}")
        break
    except:
        print(f"✗ Not found: {path}")

ftp.quit()