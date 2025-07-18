#!/bin/bash
# Railway deployment script

echo "Starting AspireHR on Railway..."

# Set up environment
export FRAPPE_SITE_NAME="aspirehr.up.railway.app"
export ADMIN_PASSWORD="admin"

# Start Redis in background
redis-server &

# Wait for Redis to start
sleep 5

# Initialize if needed
if [ ! -f sites/${FRAPPE_SITE_NAME}/site_config.json ]; then
    echo "Creating new site..."
    bench new-site ${FRAPPE_SITE_NAME} --admin-password=${ADMIN_PASSWORD} --no-mariadb-socket
    bench --site ${FRAPPE_SITE_NAME} install-app aspirehr
fi

# Start the application
echo "Starting AspireHR server..."
bench --site ${FRAPPE_SITE_NAME} serve --port ${PORT:-8000} --host 0.0.0.0
