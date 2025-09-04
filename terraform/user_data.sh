#!/bin/bash

# Update system
apt-get update
apt-get upgrade -y

# Install Docker
apt-get install -y docker.io

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create app directory
mkdir -p /app
cd /app

# Create docker-compose.yml
cat <<EOF > docker-compose.yml
version: '3.8'

services:
  backend:
    image: karimaji143/backend:latest
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydatabase
    depends_on:
      - db

  frontend:
    image: karimaji143/frontend:latest
    ports:
      - "80:80"
    environment:
      - BACKEND_URL=http://localhost:5000/api/data
    depends_on:
      - backend

  logger:
    image: karimaji143/logger:latest

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydatabase
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
EOF

# Start the application
docker-compose up -d