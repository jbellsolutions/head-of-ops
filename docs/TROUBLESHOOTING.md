# Troubleshooting

Re-run `setup.sh` after correcting a token or optional connection. It refreshes
the declared configuration and keeps a local backup of the previous file.
Use `/srv/<operator>/bin/finish-setup.sh` to add channels or tools later.

## Fast status

From the deployed operator folder:

```bash
docker compose ps
docker compose logs --tail=100 hermes
docker exec "$AGENT_NAME" /opt/hermes/.venv/bin/hermes gateway status
docker exec "$AGENT_NAME" /opt/hermes/.venv/bin/hermes mcp list
```

## Symptom → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Setup says OpenRouter is missing | The required model key was blank | Re-run `setup.sh` and paste a current OpenRouter key |
| Container keeps restarting | An enabled channel has a missing or invalid token | Re-run setup with a valid Telegram token, or both Slack tokens |
| Telegram does not answer | Bot token is wrong, another process is polling it, or pairing is incomplete | Check gateway logs, stop the other bot process, and complete pairing |
| Slack ignores every message | `SLACK_ALLOWED_USERS` is blank or contains a display name instead of a Member ID | Copy the owner's Member ID from the Slack profile menu, save it with `connect-channels.sh`, and restart |
| Slack DMs work but channel mentions do not | The bot is not a member of that Slack channel | Invite the bot to the channel |
| Slack app is missing commands or scopes | The current manifest was not applied or the app was not reinstalled | Apply `/srv/<operator>/hermes/data/slack-manifest.json`, save, and reinstall when Slack prompts |
| iMessage does not connect | BlueBubbles is not reachable from the VPS or its password changed | Verify the BlueBubbles server URL privately, reconnect it, and complete DM pairing |
| WhatsApp pairing expired | The QR setup was not completed in time | Run `finish-setup.sh`, choose messaging, and start a fresh WhatsApp QR |
| Dashboard is blank | The ownership/TUI workaround was removed | Restore `HOME`, `HERMES_TUI_DIR`, and `bin/init-chown.sh` from this repo |
| Dashboard URL does not open | It is private by design | Start the SSH tunnel shown by setup, then open localhost |
| History disappears after a rebuild | The `/opt/data` bind mount was removed or a new base directory was used | Restore the data mount and the original `BASE_DIR`; never use `docker compose down -v` |
| Calendar tools are missing | Composio key was skipped when the private config was rendered | Add the key by re-running setup, restart, then connect Google Calendar in Composio |
| Calendar exists but reads fail | The Google account is not connected or scope expired | Reconnect only Google Calendar in Composio and run the read-only test |
| PandaDoc login fails | OAuth session expired or the remote MCP is unavailable | Re-run `connect-tools.sh`, choose PandaDoc, and use the new sign-in link |
| First reply skips personalization | The onboarding file is already marked complete or was owner-edited | Ask the Operator to run the `operator-onboarding` skill again |
| A proposed skill change is not active | Skill write approval staged it for owner review | Use `!skills pending`, inspect the diff, then approve or reject the exact change |
| Super Browser does not start | Image build or Playwright install failed | Rebuild with `docker compose build --no-cache hermes` and inspect the first failing package line |
| Container is alive but unhealthy | Gateway is wedged | Let the watchdog restart it after repeated failures, then inspect logs |

## Important recovery rules

- Do not delete `/srv/<operator>/hermes/data` or `/srv/<operator>/vault`.
- Do not copy a production `.env` into GitHub or a support message.
- Do not retry an ambiguous email, proposal, calendar, campaign, or CRM write;
  read the destination first.
- Before an image or configuration upgrade, back up the two durable folders.

## Backup

```bash
cd /srv/<operator>
docker compose stop
tar -czf /srv/<operator>-backup.tgz hermes/data vault .env
docker compose start
```

The archive contains secrets and customer data. Keep it private and encrypted.
