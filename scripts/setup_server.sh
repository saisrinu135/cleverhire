#!/bin/bash

# Server Setup Script for CleverHire
# Supports Ubuntu 20.04/22.04 LTS

set -e  # Exit on error

echo "Starting server setup..."

# 1. Update and Upgrade System
echo "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Docker and Docker Compose
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    sudo apt-get install -y ca-certificates curl gnupg lsb-release

    # Add Docker's official GPG key
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    # Set up the repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
else
    echo "Docker already installed."
fi

# 3. Add User to Docker Group (Permissions)
# This allows running 'docker' without 'sudo'
echo "Adding user '$USER' to docker group..."
sudo usermod -aG docker $USER
echo "You may need to log out and log back in for group changes to take effect."

# 4. Firewall Setup (UFW)
echo "Configuring Firewall (UFW)..."

# Default strict policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow Essential Ports
sudo ufw allow 22/tcp comment 'SSH'
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'

# Allow backend port (Optional - Uncomment if debugging directly)
# sudo ufw allow 8000/tcp comment 'Django Backend'

echo "Enabling UFW..."
# Non-interactive enable
echo "y" | sudo ufw enable

echo "------------------------------------------------"
echo "Setup Complete!"
echo "1. Please log out and log back in to use Docker."
echo "2. Clone your repo or pull changes."
echo "3. Run 'docker compose up -d' to start the app."
echo "------------------------------------------------"
