#!/usr/bin/env bash
# Prepare a fresh Ubuntu server, clone the repository, and hand off to setup.sh.
set -euo pipefail

REPOSITORY="${HEAD_OF_OPS_REPO:-https://github.com/jbellsolutions/head-of-ops.git}"
DESTINATION="${HEAD_OF_OPS_DEST:-$HOME/head-of-ops}"

if [ "$(id -u)" -eq 0 ]; then
  ELEVATE=()
else
  ELEVATE=(sudo)
fi

if ! command -v git >/dev/null 2>&1; then
  "${ELEVATE[@]}" apt-get update -qq
  "${ELEVATE[@]}" apt-get install -y -qq git ca-certificates
fi

if [ -d "$DESTINATION/.git" ]; then
  git -C "$DESTINATION" pull --ff-only
else
  git clone "$REPOSITORY" "$DESTINATION"
fi

echo
echo "The setup files are ready at $DESTINATION."
echo "Run:"
echo "  cd $DESTINATION && ./setup.sh"
