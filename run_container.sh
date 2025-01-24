#!/bin/bash

# Prompt user for SMTP details
read -p "Enter SMTP Server: " SMTP_SERVER
read -p "Enter SMTP Port (default: 587): " SMTP_PORT
SMTP_PORT=${SMTP_PORT:-587}
read -p "Enter SMTP User (email): " SMTP_USER
read -sp "Enter SMTP Password: " SMTP_PASSWORD
echo ""

# Run Docker container with provided credentials
docker run -d -p 8000:8000 \
    -e SMTP_SERVER="$SMTP_SERVER" \
    -e SMTP_PORT="$SMTP_PORT" \
    -e SMTP_USER="$SMTP_USER" \
    -e SMTP_PASSWORD="$SMTP_PASSWORD" \
    --name bulk-email-app bulk-email-app
