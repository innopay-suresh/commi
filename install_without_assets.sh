#!/bin/bash

# Alternative installation script for AspireHR
# This script skips the asset building step which is causing issues

echo "Installing AspireHR without asset building..."

# Install the Python package only
cd /home/aspirehr/AspireHR/frappe-bench
source env/bin/activate
pip install -e ./apps/aspirehr --no-deps

# Install the app in Frappe without building assets
bench --site all install-app aspirehr --skip-assets

# Migrate the database
bench --site all migrate

echo "AspireHR installed successfully!"
echo "You can build assets later with: bench build --app aspirehr"
