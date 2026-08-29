#!/usr/bin/env bash
# Stamp a secret-free test deployment into a unique /srv directory and inspect it.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ "$(id -u)" -eq 0 ] || {
  echo "smoke_deployment.sh must run with sudo/root" >&2
  exit 1
}

SMOKE_DIR="$(mktemp -d /srv/head-of-ops-smoke.XXXXXX)"
cleanup() {
  case "$SMOKE_DIR" in
    /srv/head-of-ops-smoke.*) rm -rf -- "$SMOKE_DIR" ;;
    *) echo "Refusing to clean unexpected smoke path: $SMOKE_DIR" >&2 ;;
  esac
}
trap cleanup EXIT

PRIVATE_CONFIG="$SMOKE_DIR/.env"
cat > "$PRIVATE_CONFIG" <<EOF
AGENT_NAME=head-of-ops-smoke
BASE_DIR=$SMOKE_DIR
HERMES_PORT=18789
TZ=America/New_York
AGENT_PERSONA=concise
HERMES_MODEL=openai/gpt-5.6-luna
OPENROUTER_API_KEY=placeholder
TELEGRAM_BOT_TOKEN=placeholder
SLACK_BOT_TOKEN=
SLACK_APP_TOKEN=
SLACK_ALLOWED_USERS=
DISCORD_BOT_TOKEN=
BLUEBUBBLES_SERVER_URL=
BLUEBUBBLES_PASSWORD=
GATEWAY_ALLOW_ALL_USERS=false
COMPOSIO_API_KEY=
HERMES_MEM_LIMIT=5g
HERMES_CPUS=3.0
EOF
chmod 600 "$PRIVATE_CONFIG"

"$ROOT/new-agent.sh" "$PRIVATE_CONFIG" >/dev/null

required=(
  "bin/connect-channels.sh"
  "bin/connect-tools.sh"
  "bin/finish-setup.sh"
  "bin/operator-lib.sh"
  "bin/render_config.py"
  "hermes/config.template.yaml"
  "hermes/data/AGENTS.md"
  "hermes/data/SOUL.md"
  "hermes/data/config.yaml"
  "hermes/data/skills/business/operator-onboarding/SKILL.md"
  "hermes/data/skills/business/proposal-builder/SKILL.md"
  "hermes/data/skills/communication/inbox-operator/SKILL.md"
  "hermes/data/skills/communication/slack-operator/SKILL.md"
  "hermes/data/skills/productivity/calendar-operator/SKILL.md"
  "slack-manifest.yml"
  "vault/agent-knowledge/00.Onboarding.md"
  "vault/agent-knowledge/04.Tool Connections.md"
)
for relative in "${required[@]}"; do
  [ -f "$SMOKE_DIR/$relative" ] || {
    echo "Missing deployed file: $relative" >&2
    exit 1
  }
done

[ "$(stat -c '%a' "$SMOKE_DIR/.env")" = "600" ]
[ "$(stat -c '%a' "$SMOKE_DIR/hermes/data/config.yaml")" = "600" ]
[ -L "$SMOKE_DIR/hermes/data/agent-knowledge" ]
grep -q 'jump in and go' "$SMOKE_DIR/hermes/data/AGENTS.md"
grep -q 'enabled: true' "$SMOKE_DIR/hermes/data/config.yaml"
! find "$SMOKE_DIR/hermes/data/skills" -type f -path '*revenue-partner*' | grep -q .
! find "$SMOKE_DIR" -type f -path '*copywriting_retrieval*' | grep -q .

echo "Deployment layout smoke test passed."
