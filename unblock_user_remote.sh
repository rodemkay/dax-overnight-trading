#!/bin/bash

# Unblock user script for DAX Overnight EA
# Run this script ON THE SERVER (162.55.90.123)

# Database credentials
DB_NAME="prophelp_users_1"
DB_USER="prophelp_adm"
DB_PASS="mW0uG1pG9b"

# User to unblock
USER_NAME="Marco Dittmer Schaff"

echo "========================================="
echo "DAX Overnight EA - User Unblock Script"
echo "========================================="
echo ""
echo "This script will unblock user: $USER_NAME"
echo ""

# Create SQL commands file
cat > /tmp/unblock_commands.sql << EOF
-- Show current status
SELECT '=== CURRENT STATUS ===' as Info;
SELECT id, account, full_name, full_name_blocked, serialNo, 
       DATE_FORMAT(FROM_UNIXTIME(deactivate_date), '%Y-%m-%d %H:%i:%s') as deactivate_date,
       DATE_FORMAT(FROM_UNIXTIME(last_connect), '%Y-%m-%d %H:%i:%s') as last_connect
FROM lnative 
WHERE full_name = '$USER_NAME';

-- Remove the block
SELECT '=== REMOVING BLOCK ===' as Info;
UPDATE lnative 
SET full_name_blocked = 0 
WHERE full_name = '$USER_NAME';

-- Show updated status
SELECT '=== UPDATED STATUS ===' as Info;
SELECT id, account, full_name, full_name_blocked, serialNo 
FROM lnative 
WHERE full_name = '$USER_NAME';
EOF

# Execute SQL commands
mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < /tmp/unblock_commands.sql

# Clean up
rm -f /tmp/unblock_commands.sql

echo ""
echo "========================================="
echo "Process completed!"
echo "If full_name_blocked now shows 0, the user is unblocked."
echo "========================================="