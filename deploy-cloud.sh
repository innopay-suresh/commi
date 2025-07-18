#!/bin/bash

# AspireHR Cloud Deployment Script
# For Ubuntu 20.04/22.04 on AWS/Digital Ocean/Google Cloud

set -e

echo "🚀 Starting AspireHR Cloud Deployment..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-dev python3-pip python3-venv
sudo apt install -y git curl build-essential
sudo apt install -y mariadb-server mariadb-client
sudo apt install -y redis-server
sudo apt install -y nodejs npm
sudo apt install -y nginx

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install yarn
sudo npm install -g yarn

# Setup MariaDB
sudo mysql_secure_installation

# Create database user
sudo mysql -u root -p << EOF
CREATE DATABASE aspirehr_db;
CREATE USER 'aspirehr_user'@'localhost' IDENTIFIED BY 'aspirehr_password';
GRANT ALL PRIVILEGES ON aspirehr_db.* TO 'aspirehr_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF

# Create frappe user
sudo adduser --disabled-password --gecos "" frappe
sudo usermod -aG sudo frappe

# Switch to frappe user
sudo -u frappe bash << 'EOF'
cd /home/frappe

# Install bench
pip3 install frappe-bench

# Create bench
bench init --frappe-branch version-14 frappe-bench
cd frappe-bench

# Get AspireHR app
bench get-app https://github.com/innopay-suresh/commi.git aspirehr

# Create site
bench new-site aspirehr.cloud --admin-password Admin@123 --mariadb-root-password [ROOT_PASSWORD]

# Install app
bench --site aspirehr.cloud install-app aspirehr

# Setup production
sudo bench setup production frappe --yes

# Setup SSL (optional)
sudo bench setup lets-encrypt aspirehr.cloud

EOF

# Configure Nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# Configure firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable

echo "✅ AspireHR Cloud Deployment Complete!"
echo "🌐 Access your site at: https://aspirehr.cloud"
echo "👤 Username: Administrator"
echo "🔑 Password: Admin@123"
