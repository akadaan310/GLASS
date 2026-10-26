#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
PORT="${1:-8765}"
case "$PORT" in ''|*[!0-9]*) echo 'Enter a numeric TCP port' >&2; exit 2;; esac
exec python3 server.py --host 127.0.0.1 --port "$PORT"
