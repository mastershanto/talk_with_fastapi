#!/usr/bin/env bash
set -euo pipefail

# Builds the Docker image (from repo root) and runs the container
IMAGE_NAME="talk_with_fastapi:latest"
CONTAINER_NAME="talk_with_fastapi"

# Compute paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."

echo "🔨 Building image ${IMAGE_NAME}..."
docker build -t "${IMAGE_NAME}" -f "${SCRIPT_DIR}/Dockerfile" "${PROJECT_ROOT}"

# Remove any existing container with the same name
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Removing existing container ${CONTAINER_NAME}..."
  docker rm -f "${CONTAINER_NAME}" >/dev/null || true
fi

# Run container (you can pass extra docker run args after -- in the command)
# Example: ./run.sh --env-file ../.env -e DATABASE_URL=... 

echo "🚀 Starting container ${CONTAINER_NAME} (port 8000 -> 8000)..."
docker run -d --name "${CONTAINER_NAME}" -p 8000:8000 "$@" "${IMAGE_NAME}"

echo "✅ Container started. Visit http://localhost:8000"
