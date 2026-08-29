# Start Here: From One Link to Head of Ops

This guide is written for someone setting up a cloud computer for the first
time. You do not need to know terminal commands. Give the repository link and
the master prompt from the README to Claude Code or Codex; the setup agent does
the browser and server work while you approve accounts and enter private values.

## Before starting

Have access to:

- A cloud account. DigitalOcean is the recommended walkthrough.
- An OpenRouter account with billing enabled.
- Telegram, or permission to create a Slack app.

Calendar, inboxes, proposals, iMessage, WhatsApp, Discord, and other apps are
connected after the first healthy reply, so none of them can block the launch.

## 1. Create the private cloud computer

The setup agent opens DigitalOcean and chooses **Create → Droplets**:

- Image: current Ubuntu LTS.
- Size: 4 vCPU and 8 GB RAM is the comfortable proven shape.
- Region: closest practical region to the owner.
- Authentication: SSH key.
- Hostname: `operator` is fine.

You approve the server charge. The setup agent waits for the Droplet to become
active and connects by SSH. The private dashboard does not need a public port.

## 2. Install the Operator

The setup agent runs:

```bash
git clone https://github.com/jbellsolutions/head-of-ops.git
cd head-of-ops
./setup.sh
```

The installer asks one thing at a time:

1. What to call the Operator.
2. The owner's timezone.
3. A private OpenRouter key.
4. Telegram, Slack, or both.
5. An optional Composio key.

Choose Telegram for the shortest first setup. Open `@BotFather`, create a bot,
and paste its token into the hidden prompt.

For Slack, the setup agent follows [the screen-by-screen Slack guide](docs/SLACK-SETUP.md),
opens [slack-manifest.yml](slack-manifest.yml), goes to
[Slack Apps](https://api.slack.com/apps), chooses **Create New App → From an app
manifest**, selects the workspace, pastes the manifest, and creates the app.
The current manifest uses Slack Agent view; Slack cannot change that app back
to the older messages interface after it is applied. The setup agent then:

1. Installs the app to the workspace and copies the `xoxb-` Bot Token.
2. Opens **Basic Information → App-Level Tokens**.
3. Creates an `xapp-` token with `connections:write`.
4. Copies the owner's Slack Member ID from the owner's profile menu.
5. Pastes both tokens only into hidden installer prompts and enters the Member
   ID in the owner allowlist prompt.
6. Invites the app only to channels the Operator may read.

Secrets are stored only in `/srv/<operator>/.env` with private file permissions.

## 3. Wait for the proof

The build can take several minutes. The installer waits and stops with a useful
error if the service never becomes healthy. Success shows a running `healthy`
Operator and the private dashboard tunnel command.

The setup agent must run `scripts/verify.sh` and keep working until it passes.

## 4. Finish the useful connections

At the end, the installer offers a menu:

1. Calendar, inboxes, documents, and proposals.
2. Slack, Telegram, iMessage, WhatsApp, or Discord.
3. The complete Slack slash-command manifest.
4. Optional computer control.
5. All done.

### Calendar and inboxes

Composio connects Google Calendar, Gmail, Outlook, Drive, Docs, Sheets, Notion,
CRM, and many other business apps. Connect only the intended account and scopes.
Test with:

```text
Read my next three calendar events. Do not change anything.
List three recent inbox subject lines. Do not send or change anything.
```

### Proposals

Choose PandaDoc in the business-tools menu, follow its secure sign-in link, and
test with:

```text
Create a private draft proposal titled "Connection Test". Do not send it.
```

### iMessage and other messaging apps

The messaging menu asks where else the owner wants to talk to the Operator:

- iMessage uses a BlueBubbles server running on a Mac over an approved private
  network such as Tailscale; do not expose its port without authentication.
- WhatsApp uses Hermes' QR pairing flow.
- Discord uses a bot token.
- Slack uses the included manifest and two Socket Mode tokens.
- The browser dashboard is always available privately.

Do not enable remote control of the owner's Mac, browser profile, files, or
desktop merely because the Operator runs remotely. That is a separate optional
permission and should be added only for a specific use case.

## 5. Send the first message

Send:

```text
hello
```

The first reply offers:

```text
Your Operator is online. Do you want to jump in and go, or personalize it with
me first?

1. Jump in and use it now
2. Personalize it with a short guided setup
```

Guided setup asks one question at a time about the Operator's name, the owner's
use case, first outcomes, recurring jobs, preferred persona, messaging apps,
business tools, permissions, and needed skills. It writes these only to that
owner's VPS.

Before finishing, it asks:

```text
Any last skills or anything else you want me to think through before I finish?
```

When the owner is satisfied, it says:

```text
All right — we're all done. I'm ready whenever you are.
```

## The finish line

Setup is complete only when:

- The hosted container is healthy after a restart.
- A real message gets a real answer.
- The dashboard is private and reachable through the shown tunnel.
- The owner has chosen quick start or completed guided personalization.
- Requested Calendar/inbox/proposal connections pass their safe tests.
- The chosen messaging channels work.
- Slack passes a DM, an `@mention` in a channel, and a follow-up in that thread.
- Included skills load, and agent-authored skill changes wait for owner review.
- `scripts/verify.sh` passes.
- No key, customer data, proprietary skill, or private account ID is in git.

If anything fails, keep the server and re-run the relevant menu. Do not delete
the private `/srv/<operator>/hermes/data` or `/srv/<operator>/vault` folders.
Use [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for symptom-based fixes.
