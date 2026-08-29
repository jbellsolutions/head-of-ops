# Tools and Connections

The repository ships the same broad tool surface as the live operator. A tool is
usable only after its own connection or read-only test succeeds.

## Ready on first launch

| Capability | What it does | Account needed |
|---|---|---|
| Web | Search, retrieve, and cite public information | no extra account |
| Super Browser / Playwright | Browser research and structured automation | no extra account for local Playwright |
| Files and code | Create documents, analyze files, run scripts | no extra account |
| Images and vision | Generate and inspect images | model/provider dependent |
| Voice | Transcribe voice and speak replies | local STT + Edge TTS included |
| Memory and sessions | Remember context and search prior work | no extra account |
| Tasks and schedules | Kanban, plans, and guarded cron jobs | no extra account |
| Delegation | Up to three child agents with inherited tools | model key |
| Business documents | Private Markdown, DOCX, PDF, sheets, and presentations | no extra account |

## Connected after launch

| Capability | Connection | First safe test |
|---|---|---|
| Google Calendar | Composio | read the next three events |
| Gmail | Composio | list unread message subjects; do not send |
| Outlook | Composio | list three recent message subjects; do not send |
| Drive, Docs, Sheets | Composio | list a small folder or create a private test draft |
| CRM | Composio | read one record; do not modify |
| Proposals | PandaDoc MCP | create a private unsent draft |
| Creative video/media | Higgsfield MCP | list capabilities or make a private test asset |
| Hosted browser sessions | Browser Use, Browserbase, Airtop, Hyperbrowser, Steel, Orgo, Browserless, Decodo, Rtrvr | provider readiness check |
| Lead/data actors | Apify | account/status check with no paid run |
| Cold email | Instantly or SmartLead | read campaign status; do not launch |
| Booking links | Cal.com | read current booking configuration |
| Calls | Retell | read agent status; do not place a call |
| Memory mirror | Notion | create the five private databases and run one sync |

## Messaging choices

| Channel | Connection | First safe test |
|---|---|---|
| Telegram | BotFather bot token | send and receive `hello` |
| Slack | Agent-view manifest + Socket Mode tokens + owner Member ID | DM `hello`, then test an `@mention` and thread follow-up |
| iMessage | BlueBubbles server on an owner-controlled Mac | complete DM pairing and send `hello` |
| WhatsApp | Hermes QR pairing | send and receive `hello` |
| Discord | Discord bot token | answer in one approved server/channel |
| Browser dashboard | private SSH tunnel | open Chat and send `hello` |

## Calendar rule

Reading availability is allowed. Creating, moving, cancelling, or inviting is an
external write and needs approval for the exact event details. The operator must
read the event back after the write.

## Proposal rule

Local drafting and a private PandaDoc draft are allowed. Sending, requesting a
signature, changing recipients, or changing commercial terms needs approval for
the exact document and recipients. The operator must read back the document ID,
status, and recipients after sending.

## Connection status

The durable checklist is:

`/opt/data/agent-knowledge/04.Tool Connections.md`

The presence of a key is not proof. Mark a connection verified only after the
least-privileged safe test succeeds.

The full included-skill list, Slack invocation examples, owner-review flow, and
safe Hub update commands are in [SKILLS.md](SKILLS.md).
