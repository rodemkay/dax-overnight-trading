#!/usr/bin/env python3
"""
Master Script für RoboForex Integration
Führt alle notwendigen Schritte aus
"""

import os
import sys
import subprocess
from datetime import datetime

def run_command(command, description):
    """Führe einen Befehl aus und zeige Status"""
    print(f"\n{'='*60}")
    print(f"Executing: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ {description} - SUCCESS")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"✗ {description} - FAILED")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║        RoboForex Integration Master Script                  ║
    ║                                                              ║
    ║  Dieses Script führt alle Komponenten der RoboForex         ║
    ║  Integration aus:                                           ║
    ║                                                              ║
    ║  1. Template.inc.php Syntax-Fix und Upload                  ║
    ║  2. update_robo_status.php Upload                           ║
    ║  3. RoboForex API Connection Test                           ║
    ║  4. MySQL Account Liste                                     ║
    ║  5. RoboAffiliate Status Update                             ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    steps = [
        {
            'name': 'Fix und Upload template.inc.php',
            'script': 'fix_and_upload_template.py',
            'required': True
        },
        {
            'name': 'Upload update_robo_status.php',
            'script': 'upload_robo_update_script.py',
            'required': True
        },
        {
            'name': 'Test RoboForex API Connection',
            'script': 'test_roboforex_connection.py',
            'required': False
        },
        {
            'name': 'List MySQL Accounts',
            'script': 'mysql_list_accounts.py',
            'required': False
        },
        {
            'name': 'Update RoboAffiliate Status',
            'script': 'update_roboaffiliate.py --limit 5',
            'required': False
        }
    ]
    
    print("\nAvailable Steps:")
    for i, step in enumerate(steps, 1):
        req = " [REQUIRED]" if step['required'] else ""
        print(f"{i}. {step['name']}{req}")
    
    response = input("\nSelect option:\n1) Run all steps\n2) Run required only\n3) Select individual steps\n4) Exit\n\nChoice (1-4): ")
    
    if response == '1':
        # Run all steps
        for step in steps:
            if not run_command(f"python {step['script']}", step['name']):
                if step['required']:
                    print(f"\n✗ Required step failed: {step['name']}")
                    print("Stopping execution.")
                    return
    
    elif response == '2':
        # Run required only
        for step in steps:
            if step['required']:
                if not run_command(f"python {step['script']}", step['name']):
                    print(f"\n✗ Required step failed: {step['name']}")
                    print("Stopping execution.")
                    return
    
    elif response == '3':
        # Select individual
        selections = input("Enter step numbers separated by comma (e.g., 1,3,5): ")
        selected = [int(x.strip())-1 for x in selections.split(',') if x.strip().isdigit()]
        
        for idx in selected:
            if 0 <= idx < len(steps):
                step = steps[idx]
                run_command(f"python {step['script']}", step['name'])
    
    elif response == '4':
        print("Exiting...")
        return
    
    print("\n" + "="*60)
    print("INTEGRATION COMPLETE!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Test the system at https://lic.prophelper.org/connect")
    print("2. Check RoboForex column is displayed correctly")
    print("3. Run the EA (don_gpt.mq5) to test status updates")
    print("4. Monitor the robo_updates.log file on the server")
    
    print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # Check if all required scripts exist
    required_scripts = [
        'fix_and_upload_template.py',
        'upload_robo_update_script.py',
        'test_roboforex_connection.py',
        'mysql_list_accounts.py',
        'update_roboaffiliate.py'
    ]
    
    missing = []
    for script in required_scripts:
        if not os.path.exists(script):
            missing.append(script)
    
    if missing:
        print("✗ Missing required scripts:")
        for m in missing:
            print(f"  - {m}")
        print("\nPlease ensure all scripts are in the current directory.")
        sys.exit(1)
    
    main()