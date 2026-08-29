#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "Checking shell scripts..."
while IFS= read -r script; do
  bash -n "$script"
done < <(find . -type f -name '*.sh' -not -path './.git/*' | sort)

echo "Checking Python files..."
python3 -m compileall -q \
  scripts \
  tests \
  sync

echo "Running repository tests..."
python3 -m unittest discover -s tests -v

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  echo "Checking Compose configuration..."
  OPENROUTER_API_KEY=placeholder \
  BASE_DIR=/srv/head-of-ops \
  AGENT_NAME=head-of-ops \
    docker compose -f compose.yml config --quiet
fi

echo "Verification passed."
