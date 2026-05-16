#!/usr/bin/env bash
set -e
echo "🚀 Starting Breach Hunter with Docker..."
# Check if Docker is installed
if ! command -v docker &> /dev/null; then
  echo "❌ Docker is not installed. Please install docker first."
  exit 1
fi
# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
  echo "❌ docker-compose is not installed. Please install it first."
  exit 1
fi
# Run containers
docker-compose -f docker/docker-compose.yml up --build
