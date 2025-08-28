#!/bin/bash

# Unblock user script for DAX Overnight EA
# This script removes the block for a specific user name

# Database credentials
DB_HOST="localhost"
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

# First, check current status
echo "1. Checking current status..."
echo ""

mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" << EOF
SELECT id, account, full_name, full_name_blocked, serialNo, deactivate_date, last_connect 
FROM lnative 
WHERE full_name = '$USER_NAME';
EOF

echo ""
echo "2. Removing block..."
echo ""

# Remove the block
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" << EOF
UPDATE lnative 
SET full_name_blocked = 0 
WHERE full_name = '$USER_NAME';
EOF

echo ""
echo "3. Verifying changes..."
echo ""

# Verify the change
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" << EOF
SELECT id, account, full_name, full_name_blocked, serialNo 
FROM lnative 
WHERE full_name = '$USER_NAME';
EOF

echo ""
echo "========================================="
echo "Process completed!"
echo "========================================="