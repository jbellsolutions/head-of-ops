# Live Operator Parity Ledger

Audit date: 2026-08-28.

Source inspected: the active `single-brain` DigitalOcean host and its running
containers, not the stale deployment README.

## Runtime copied

| Live item | Repository equivalent |
|---|---|
| Hermes Agent v0.20.0, upstream `91937a6d` | digest-pinned base in `hermes-image/Dockerfile` |
| Voice additions `faster-whisper 1.2.1`, `edge-tts 7.2.7` | same pinned packages in the image |
| Dashboard on 9119, gateway foreground | `bin/start-hermes.sh` |
| s6-overlay entrypoint dispatch and ownership fix | `bin/init-chown.sh` |
| Persistent `/opt/data`, vault, logs, read-only Docker socket | `compose.yml` |
| Multi-channel gateway | Slack, Telegram, Discord, WhatsApp, and BlueBubbles/iMessage routes |
| Obsidian/Notion 60-second mirror | optional `sync` profile |
| Watchdog and restart policy | `bin/watchdog.sh` + Compose |

## Tool front doors copied

- Super Browser — the exact live Python source, local Playwright, and the same
  optional hosted-provider routes and direct package versions.
- Composio — Calendar, Gmail, Google workspace, Notion, CRM, and other apps.
- Higgsfield — creative media MCP.
- PandaDoc — proposal MCP.

Every supported messaging route receives the broad core toolset: browser, code
execution, computer use, cron, delegation, files, image generation, kanban,
memory, session search, skills, terminal, tasks, text-to-speech, vision, and web.

## Intentionally not copied

- API keys, passwords, OAuth sessions, bot tokens, cookies, and SSH keys.
- Personal Slack, Telegram, Notion, tailnet, and A2A account IDs.
- Conversations, candidate resumes, lead lists, customer files, generated work,
  browser profiles, cron history, and private memories.
- Proprietary agency playbooks, internal offer methods, private source archives,
  and any other owner's persona or custom skills.
- The live server's archived OpenClaw runtime and package caches.
- Machine-specific IP addresses and internal agent URLs.

Those omissions are the difference between a safe operational replica and a
credential/data breach. Each owner supplies private values during setup.

## Public Operator additions

The public package adds a neutral SOUL, blank knowledge templates, a first-run
guided interview, generic Calendar/inbox/Slack/document/proposal skills, a Slack
manifest, and post-launch connection menus. Owner-specific persona and skills
are created privately on that owner's VPS and never added to this repository.
