# Head of Ops

Give one GitHub link to Claude or Codex. It builds a private, always-on AI
operator in the cloud, connects the owner's preferred messaging apps, and then
walks the owner through persona, business use case, tools, and skills.

No prewritten agency persona or proprietary operating playbook is included.
Every owner gets the full basic operator and creates their private business
context and custom skills on their own VPS.

## The drag-and-drop setup

Copy this whole message into Claude Code, Codex, or another computer-using
coding agent:

```text
Build and host my private Head of Ops from this repository:
https://github.com/jbellsolutions/head-of-ops

Read START-HERE.md first and do every technical step for me. Use a fresh Ubuntu
VPS on DigitalOcean unless I choose another provider. Operate the browser and
terminal yourself. Explain one screen at a time in plain English and ask me for
only one private value or account decision at a time. Never repeat, expose, or
commit a key after I provide it.

Install the Operator with setup.sh, prove the container is healthy, and prove a
real message works. Start with Telegram for the fastest setup unless I choose
Slack. If I choose Slack, follow docs/SLACK-SETUP.md and use the included
current Agent-view slack-manifest.yml. Authorize my exact Slack Member ID. After launch,
offer Calendar and inboxes through Composio, proposals through PandaDoc, and
Slack, Telegram, iMessage/BlueBubbles, WhatsApp, Discord, or the private browser
dashboard as messaging choices.

Do not add proprietary agency skills or copy another person's private data.
When the Operator replies for the first time, let it offer quick start or a
one-question-at-a-time guided setup for its name, persona, business use case,
permissions, tools, priorities, and private custom skills. Finish only after
scripts/verify.sh passes, the hosted Operator answers a real message, and you
give me its status, private dashboard instructions, and next safe test.
```

That is the main installation method. The owner approves account sign-ins and
charges; the setup agent handles the technical work.

## What the owner gets

| Area | Included |
|---|---|
| Hosted brain | Digest-pinned Hermes Agent 0.20.6 on a private Ubuntu VPS |
| Messaging | Telegram, Slack, Discord, WhatsApp, iMessage via BlueBubbles, private dashboard |
| Calendar and inboxes | Google Calendar, Gmail, Outlook, and other apps through Composio |
| Proposals | Private document drafting plus PandaDoc connection |
| Documents | Markdown, DOCX, PDF, spreadsheets, presentations, Drive/Docs/Sheets |
| Browser work | Local Playwright and ten Super Browser provider routes |
| Creative work | Images, vision, voice, and optional Higgsfield |
| Operations | Memory, tasks, schedules, files, code, terminal, and sub-agents |
| Private customization | First-run persona, business context, priorities, and owner-specific skills |

The connection is included even when an optional account is not connected yet.
The finish menu can add it later without rebuilding the server.

## What happens, step by step

1. The setup agent creates or connects to a fresh Ubuntu VPS.
2. It clones this repository and runs `./setup.sh`.
3. The installer asks for an Operator name, timezone, OpenRouter key, and either
   Telegram or Slack. Slack also requires the owner's Member ID. Every secret
   entry is hidden.
4. It builds the exact hosted runtime, starts it, and waits for a healthy result.
5. The finish menu offers business apps, more messaging apps, a complete Slack
   manifest, and optional computer-control guidance.
6. The owner sends `hello`.
7. The Operator replies:

   > Your Operator is online. Do you want to jump in and go, or personalize it
   > with me first?

8. Guided setup asks one question at a time, creates only the private skills
   that owner needs, asks one final “anything else?” question, then says:

   > All right — we're all done. I'm ready whenever you are.

## Slack

The ready-to-paste current manifest is [slack-manifest.yml](slack-manifest.yml).
It includes Socket Mode, Slack Agent view, message/file/channel permissions,
events, buttons, and the current 50 native Hermes commands. After the Operator
is running, its finish menu generates the exact runtime manifest at:

`/srv/<operator>/hermes/data/slack-manifest.json`

The Slack app can see only channels it is allowed to access. Invite it only to
the channels the owner wants the Operator to use. Hermes also requires
`SLACK_ALLOWED_USERS`, so the installer collects the authorized owner's Member
ID. Follow [the screen-by-screen Slack guide](docs/SLACK-SETUP.md).

## Calendar, inboxes, and proposals

- Composio is the front door for Calendar, Gmail, Outlook, Drive, Docs, Sheets,
  Notion, CRM, and other connected apps.
- PandaDoc is the proposal front door.
- The first tests are read-only Calendar/inbox checks and an unsent private
  proposal draft.
- Sends, event changes, proposal sends, publishes, purchases, and account
  changes require approval for the exact action and a destination read-back.

## Manual server command

A setup agent normally runs this. On a fresh Ubuntu VPS it is:

```bash
git clone https://github.com/jbellsolutions/head-of-ops.git
cd head-of-ops
./setup.sh
```

Detailed beginner instructions are in [START-HERE.md](START-HERE.md). The live
tool ledger is in [docs/LIVE-PARITY.md](docs/LIVE-PARITY.md), and the full tool
map is in [docs/TOOLS.md](docs/TOOLS.md). See [docs/SKILLS.md](docs/SKILLS.md)
for installed and optional skills and [docs/UPDATES.md](docs/UPDATES.md) for the
reviewed update process.

## Public/private boundary

This repository contains generic source code, blank knowledge templates, and
basic operator skills only. It does not contain private conversations, customer
files, account IDs, OAuth sessions, browser profiles, credentials, proprietary
agency playbooks, or another owner's persona.

Private data stays under `/srv/<operator>` on that owner's VPS. The dashboard
binds to localhost and opens through an SSH tunnel or an approved private
network. Read [SECURITY.md](SECURITY.md) before publishing a fork.

MIT licensed. Hermes Agent is maintained by Nous Research. This repository is
not affiliated with DigitalOcean, Nous Research, OpenRouter, Composio, Slack,
PandaDoc, or BlueBubbles.
