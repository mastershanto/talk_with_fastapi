#!/usr/bin/env bash
set -euo pipefail

# Remove Docker images safely.
# Usage:
#   ./drmi.sh IMAGE_NAME [IMAGE_NAME2 ...]
#   ./drmi.sh --dangling
#   ./drmi.sh --all [--yes]
#   ./drmi.sh --help

DEFAULT_IMAGE="talk_with_fastapi:latest"

usage() {
  cat <<EOF
Usage: $0 [OPTIONS] [IMAGE...]

Options:
  --dangling      Remove dangling images only
  --all           Remove all local images (DANGEROUS)
  --yes           Skip confirmation prompt
  --help          Show this help

If no IMAGE is provided, the script will attempt to remove '${DEFAULT_IMAGE}' (if present).
EOF
  exit 1
}

if [ "$#" -eq 0 ]; then
  IMAGES=("${DEFAULT_IMAGE}")
fi

ALL=false
DANGLING=false
ASSUME_YES=false
POSITIONS=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    --all) ALL=true; shift ;;
    --dangling) DANGLING=true; shift ;;
    --yes) ASSUME_YES=true; shift ;;
    --help) usage ;;
    --*) echo "Unknown option: $1" >&2; usage ;;
    *) POSITIONS+=("$1"); shift ;;
  esac
done

if [ ${#POSITIONS[@]} -gt 0 ]; then
  IMAGES=("${POSITIONS[@]}")
fi

# Determine image IDs to remove
IMAGE_IDS=()

if $ALL; then
  mapfile -t IMAGE_IDS < <(docker images -q)
elif $DANGLING; then
  mapfile -t IMAGE_IDS < <(docker images -f dangling=true -q)
else
  for img in "${IMAGES[@]}"; do
    # Support image name or ID
    ids=$(docker images -q "$img" || true)
    if [ -n "$ids" ]; then
      while IFS= read -r id; do IMAGE_IDS+=("$id"); done <<<"$ids"
    fi
  done
fi

# Unique IDs
if [ ${#IMAGE_IDS[@]} -eq 0 ]; then
  echo "No matching images found. Nothing to do."
  exit 0
fi

# Show summary
echo "Images to be removed (count=${#IMAGE_IDS[@]}):"
for id in "${IMAGE_IDS[@]}"; do
  docker images --no-trunc --format "{{.Repository}}:{{.Tag}}\t{{.ID}}\t{{.Size}}" | grep "$id" || true
done

if ! $ASSUME_YES; then
  read -rp "Proceed to remove these images? (y/N): " ans
  case "$ans" in
    [Yy]*) ;;
    *) echo "Aborted."; exit 1 ;;
  esac
fi

# Remove images
for id in "${IMAGE_IDS[@]}"; do
  echo "Removing image $id..."
  docker rmi -f "$id" || echo "Failed to remove $id (it may be in use)."
done

echo "✅ Done."
