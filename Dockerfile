# Multi-stage Dockerfile for AspireHR
FROM frappe/frappe:latest as base

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Install AspireHR
RUN bench get-app https://github.com/innopay-suresh/commi.git aspirehr

# Production stage
FROM base as production

# Create new site
RUN bench new-site aspirehr.local --admin-password=admin --no-mariadb-socket

# Install app
RUN bench --site aspirehr.local install-app aspirehr

# Set production configuration
RUN bench --site aspirehr.local set-config developer_mode 0
RUN bench --site aspirehr.local set-config server_script_enabled 1

# Build assets
RUN bench build --app aspirehr

# Expose port
EXPOSE 8000

# Start command
CMD ["bench", "start"]
