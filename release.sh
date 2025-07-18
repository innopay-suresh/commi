#!/bin/bash

# Heroku release script
echo "Running Heroku release tasks..."

# Install frappe-bench
pip install frappe-bench

# Initialize bench
bench init --frappe-branch version-14 frappe-bench --no-procfile --no-backups
cd frappe-bench

# Get AspireHR app
bench get-app https://github.com/innopay-suresh/commi.git aspirehr

# Create site
bench new-site aspirehr.herokuapp.com --admin-password $ADMIN_PASSWORD --db-name $DATABASE_URL

# Install app
bench --site aspirehr.herokuapp.com install-app aspirehr

# Build assets
bench build --app aspirehr

echo "Release tasks completed!"
