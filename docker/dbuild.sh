#!/usr/bin/env bash
set -euo pipefail

# Build the docker image for this project.
# Usage:
#   ./dbuild.sh             # default build
#   ./dbuild.sh --no-cache  # build without cache
#   ./dbuild.sh --help
#   ./dbuild.sh -- -e KEY=VAL   # pass extra docker build/run args after --

IMAGE_NAME="talk_with_fastapi:latest"
DOCKERFILE_PATH="docker/Dockerfile"
CONTEXT_DIR="."
NO_CACHE=false
EXTRA=()

usage() {
  cat <<EOF
Usage: $0 [--no-cache] [--] [extra-docker-args]

Builds the Docker image: ${IMAGE_NAME}
Options:
  --no-cache    Disable Docker build cache
  --help        Show this help

Any arguments after -- are appended to the docker build command.
EOF
  exit 1
}

# Parse simple flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-cache) NO_CACHE=true; shift ;;
    --help) usage ;;
    --) shift; EXTRA=("$@") ; break ;;
    *) EXTRA+=("$1"); shift ;;
  esac
done

if [ ! -f "${DOCKERFILE_PATH}" ]; then
  echo "❌ Dockerfile not found at ${DOCKERFILE_PATH}. Aborting."
  exit 1
fi

echo "🔨 Building image ${IMAGE_NAME} from ${DOCKERFILE_PATH}"
CMD=(docker build -t "${IMAGE_NAME}" -f "${DOCKERFILE_PATH}" "${CONTEXT_DIR}")
if $NO_CACHE; then
  CMD+=(--no-cache)
fi
if [ ${#EXTRA[@]} -gt 0 ]; then
  CMD+=("${EXTRA[@]}")
fi

# Show and run
echo "+ ${CMD[*]}"
"${CMD[@]}"

echo "✅ Docker image ${IMAGE_NAME} built successfully."
