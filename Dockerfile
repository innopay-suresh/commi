# Simplified Dockerfile for AspireHR
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    curl \
    build-essential \
    mariadb-client \
    redis-server \
    nodejs \
    npm \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Install yarn
RUN npm install -g yarn

# Create frappe user
RUN useradd -m -s /bin/bash frappe \
    && echo "frappe ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch to frappe user
USER frappe
WORKDIR /home/frappe

# Add .local/bin to PATH
ENV PATH="/home/frappe/.local/bin:${PATH}"

# Install frappe-bench
RUN pip3 install frappe-bench

# Copy app files
COPY --chown=frappe:frappe . /home/frappe/aspirehr

# Initialize frappe-bench with minimal setup
RUN /home/frappe/.local/bin/bench init --skip-redis-config-generation --no-procfile --skip-assets frappe-bench

# Change to bench directory
WORKDIR /home/frappe/frappe-bench

# Link the app
RUN ln -s /home/frappe/aspirehr apps/aspirehr

# Install app dependencies
RUN ./env/bin/pip install -e apps/aspirehr

# Create a simple startup script
RUN echo '#!/bin/bash\n\
export PATH="/home/frappe/.local/bin:$PATH"\n\
redis-server &\n\
sleep 5\n\
if [ ! -f sites/aspirehr.docker/site_config.json ]; then\n\
    bench new-site aspirehr.docker --admin-password=admin --no-mariadb-socket\n\
    bench --site aspirehr.docker install-app aspirehr\n\
fi\n\
bench --site aspirehr.docker serve --port 8000 --host 0.0.0.0' > start.sh

RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Start command
CMD ["./start.sh"]
