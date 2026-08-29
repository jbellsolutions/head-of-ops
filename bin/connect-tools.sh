#!/usr/bin/env bash
# Connect the basic business tools every Operator can use.
set -euo pipefail

# shellcheck disable=SC1091
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/operator-lib.sh"
operator_load_env
operator_init_docker

echo
echo "Connect Calendar, inboxes, documents, proposals, and business apps"
echo "No password or token will be printed by this helper."

while true; do
  cat <<'MENU'

  1. Show connection status
  2. Connect Composio for Calendar, Gmail, Outlook, files, and business apps
  3. Connect PandaDoc proposals
  4. Connect Higgsfield creative tools
  5. Test the browser tool
  6. Finish
MENU
  read -r -p "Choose a number: " choice
  case "$choice" in
    1)
      operator_hermes mcp list
      ;;
    2)
      if [ -z "${COMPOSIO_API_KEY:-}" ]; then
        echo "Open https://app.composio.dev and create a consumer API key."
        key="$(operator_secret "Paste the Composio consumer key")"
        [ -n "$key" ] || operator_fail "the Composio key cannot be blank"
        operator_save_value COMPOSIO_API_KEY "$key"
        operator_refresh
        COMPOSIO_API_KEY=$key
      fi
      cat <<'TEXT'

Composio is installed. In its dashboard, connect only the accounts you want:
Google Calendar, Gmail or Outlook, Drive/Docs/Sheets, Notion, CRM, or others.

First safe tests to send the Operator:
  Read my next three calendar events. Do not change anything.
  List three recent inbox subject lines. Do not send or change anything.
TEXT
      ;;
    3)
      echo "Hermes will show a secure PandaDoc sign-in link."
      operator_hermes mcp login pandadoc
      echo 'Test with: Create a private draft proposal titled "Connection Test". Do not send it.'
      ;;
    4)
      echo "Hermes will show a secure Higgsfield sign-in link."
      operator_hermes mcp login higgsfield
      ;;
    5)
      echo "Testing the local Super Browser route..."
      operator_docker exec "${AGENT_NAME:-head-of-ops}" \
        /opt/super-browser/.venv/bin/python -m super_browser.cli doctor
      ;;
    6)
      echo "Business-tool setup is finished."
      break
      ;;
    *) echo "Choose a number from 1 through 6." ;;
  esac
done
