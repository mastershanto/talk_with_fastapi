#!/bin/bash
set -e

# Stop FastAPI (uvicorn) processes gracefully, then force-kill any that remain
echo "Stopping FastAPI (uvicorn) processes..."

# Try pkill (sends SIGTERM)
if pgrep -f uvicorn >/dev/null 2>&1; then
  pkill -f uvicorn && echo "Sent SIGTERM to uvicorn processes."
else
  echo "No uvicorn processes found via pgrep."
fi

# Also ensure nothing is listening on port 8000 (force kill)
PORT=8000
if command -v lsof >/dev/null 2>&1; then
  if lsof -ti tcp:${PORT} >/dev/null 2>&1; then
    lsof -ti tcp:${PORT} | xargs -r kill -9 && echo "Killed processes listening on port ${PORT}."
  else
    echo "No process listening on port ${PORT}."
  fi
else
  echo "lsof not available — skipping port check."
fi

echo "Done."
