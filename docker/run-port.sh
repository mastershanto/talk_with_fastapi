m#!/usr/bin/env bash
set -euo pipefail

# Run the talk_with_fastapi container but allow overriding the HOST port.
# Usage:
#   ./run-port.sh           -> uses host port 8000
#   ./run-port.sh 8555      -> maps host 8555 -> container 8000
#   ./run-port.sh 8555 --env-file ../.env -e KEY=VAL  -> pass extra docker run args after the port

IMAGE_NAME="talk_with_fastapi:latest"
CONTAINER_NAME="talk_with_fastapi"

HOST_PORT="${1:-8000}"
shift  || true
EXTRA_ARGS=("$@")

# Build image (no-op if up-to-date)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."

echo "🔨 Building image ${IMAGE_NAME} (if needed)..."
docker build -t "${IMAGE_NAME}" -f "${SCRIPT_DIR}/Dockerfile" "${PROJECT_ROOT}"

# Remove existing container with same name
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Removing existing container ${CONTAINER_NAME}..."
  docker rm -f "${CONTAINER_NAME}" >/dev/null || true
fi

# Run container with dynamic host port
echo "🚀 Starting container ${CONTAINER_NAME} (host:${HOST_PORT} -> container:8000)"
if [ ${#EXTRA_ARGS[@]} -gt 0 ]; then
  docker run -d --name "${CONTAINER_NAME}" -p "${HOST_PORT}:8000" "${EXTRA_ARGS[@]}" "${IMAGE_NAME}"
else
  docker run -d --name "${CONTAINER_NAME}" -p "${HOST_PORT}:8000" "${IMAGE_NAME}"
fi

echo "✅ Container started. Open http://localhost:${HOST_PORT}/docs"
