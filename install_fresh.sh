#!/bin/bash

# AspireHR Fresh Installation Script
set -e

echo "Starting AspireHR Fresh Installation..."

# Configuration
SITE_NAME="aspirehr.local"
ADMIN_PASSWORD="admin"
DB_ROOT_PASSWORD="root"

# Step 1: Start services
echo "Starting required services..."
sudo systemctl start mariadb
sudo systemctl start redis-server

# Step 2: Create new site
echo "Creating new site..."
cd /home/aspirehr/AspireHR/frappe-bench
bench new-site $SITE_NAME --admin-password $ADMIN_PASSWORD --mariadb-root-password $DB_ROOT_PASSWORD

# Step 3: Get app
echo "Getting AspireHR app..."
bench get-app https://github.com/innopay-suresh/commi.git
mv apps/commi apps/aspirehr

# Step 4: Install app
echo "Installing AspireHR..."
bench --site $SITE_NAME install-app aspirehr

# Step 5: Start development server
echo "Starting development server..."
bench --site $SITE_NAME serve --port 8000

echo "AspireHR installation completed!"
echo "Access your site at: http://localhost:8000"
echo "Username: Administrator"
echo "Password: $ADMIN_PASSWORD"
