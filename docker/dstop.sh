#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="talk_with_fastapi"
IMAGE_NAME="talk_with_fastapi:latest"

# Stop container if running
if docker ps -q -f name="^/${CONTAINER_NAME}$" | grep -q .; then
  echo "Stopping container ${CONTAINER_NAME}..."
  docker stop "${CONTAINER_NAME}" >/dev/null || true
else
  echo "No running container named ${CONTAINER_NAME} found."
fi

# Remove container if exists
if docker ps -a -q -f name="^/${CONTAINER_NAME}$" | grep -q .; then
  echo "Removing container ${CONTAINER_NAME}..."
  docker rm -f "${CONTAINER_NAME}" >/dev/null || true
fi

# If user passed --rmi, remove the image too
if [ "${1:-}" = "--rmi" ]; then
  if docker images -q "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "Removing image ${IMAGE_NAME}..."
    docker rmi "${IMAGE_NAME}" || echo "Image removal failed or image in use."
  else
    echo "Image ${IMAGE_NAME} not present."
  fi
fi

echo "✅ Stopped/removed docker resources for ${CONTAINER_NAME}."
