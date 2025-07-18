# Simplified Dockerfile for AspireHR
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install yarn
RUN npm install -g yarn

# Install frappe-bench
RUN pip install frappe-bench

# Copy app files
COPY . /app/aspirehr

# Initialize frappe-bench
RUN bench init --skip-redis-config-generation frappe-bench

# Change to bench directory
WORKDIR /app/frappe-bench

# Link the app
RUN ln -s /app/aspirehr apps/aspirehr

# Install dependencies
RUN pip install -e apps/aspirehr

# Set environment variables
ENV PYTHONPATH=/app/frappe-bench
ENV FRAPPE_SITE_NAME=aspirehr.docker

# Expose port
EXPOSE 8000

# Create startup script
RUN echo '#!/bin/bash\n\
if [ ! -f sites/aspirehr.docker/site_config.json ]; then\n\
    bench new-site aspirehr.docker --admin-password=admin --no-mariadb-socket\n\
    bench --site aspirehr.docker install-app aspirehr\n\
fi\n\
bench --site aspirehr.docker serve --port 8000 --host 0.0.0.0' > start.sh

RUN chmod +x start.sh

# Start command
CMD ["./start.sh"]
