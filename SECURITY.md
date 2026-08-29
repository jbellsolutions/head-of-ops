# Security

## Public repository boundary

This repository must contain zero live credentials and zero customer data.
Commit only templates, seeded instructions, and code.

Never commit:

- `agent.env`, `.env`, or a rendered `hermes/data/config.yaml`.
- API keys, bot tokens, OAuth sessions, cookies, SSH keys, or webhook secrets.
- Lead lists, resumes, conversations, proposals, call notes, or browser profiles.
- Personal Slack, Telegram, Discord, WhatsApp, iMessage, Notion, tailnet,
  calendar, or A2A identifiers.
- Proprietary agency playbooks or another owner's persona and private skills.

The safe copy intentionally excludes all of those from the live VPS.

## Where private values live

- `/srv/<operator>/.env` — owner-provided keys; mode 600.
- `/srv/<operator>/hermes/data/config.yaml` — rendered config and the Composio
  consumer header; mode 600.
- `/srv/<operator>/hermes/data/` — sessions, authentication, memory, and work.
- `/srv/<operator>/vault/` — durable business knowledge and mirrored history.

These paths are host-mounted runtime state and are ignored by git.

## Network boundary

The dashboard binds to `127.0.0.1`. Reach it through an SSH tunnel or a private
Tailscale network. Do not publish port 18789 directly to the internet.

Keep `GATEWAY_ALLOW_ALL_USERS=false` unless a public bot is intentional. Use
channel pairing, invite the Slack app only to intended channels, and keep
provider scopes as narrow as practical.

## External actions

Research and local drafts can run autonomously. Sending, publishing, scheduling,
proposals, CRM mutation, campaign activation, purchases, and permission changes
require explicit approval for the exact action. Verify every external write.

## Before pushing a fork

Run:

```bash
./scripts/verify.sh
git status --short
```

Review every staged file. A green scan cannot decide whether ordinary-looking
business data is private.

## If a secret is exposed

1. Revoke or rotate it at the provider immediately.
2. Replace it in the private server `.env`.
3. Re-run `setup.sh` and restart the operator.
4. Remove it from git history; deleting the current line is not enough.
5. Review provider audit logs for unexpected use.

Report security issues privately to the repository owner instead of opening a
public issue with sensitive details.
