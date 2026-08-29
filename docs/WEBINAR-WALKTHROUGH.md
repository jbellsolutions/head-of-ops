# Webinar Walkthrough

This is the host's run-of-show for taking one first-time participant from a
blank DigitalOcean account to a working hosted Operator.

## Before the webinar

- Use a fresh test account and a fresh bot. Never screen-share a production key.
- Confirm the repository's default branch passes CI.
- Keep one prebuilt Droplet available as a fallback for slow image downloads.
- Put the master prompt from `README.md` in a copyable webinar chat message.
- For a Slack webinar, have a workspace owner present and use a fresh Slack
  app so the permanent Agent-view choice is easy to explain.

## Live sequence

### 1. Set expectations

Say: “You will make the account choices. The setup agent will do every technical
step. We will launch the core operator first, prove it works, then connect
Calendar and proposals.”

### 2. Drop one link and prompt

Share:

`https://github.com/jbellsolutions/head-of-ops`

Have the participant paste the master prompt from `README.md` into Codex or
Claude Code.

### 3. Create the Droplet

The participant signs in and approves the server charge. The setup agent chooses
Ubuntu LTS, the recommended live machine shape, a nearby region, and SSH-key
authentication. It records the host without exposing the private key.

### 4. Connect the model and Slack

For the first healthy reply, connect:

1. OpenRouter.
2. Slack by following [SLACK-SETUP.md](SLACK-SETUP.md) one screen at a time.

Use the included Agent-view manifest, the hidden `xoxb-` and `xapp-` prompts,
and the participant's copied Slack Member ID. Skip Calendar and every other
optional account until Slack answers.

### 5. Prove Slack

The participant sends `hello` in a direct message, `@mentions` Head of Ops once
in an approved channel, then follows up in that thread without another mention.
Test `/help`, `/reload-skills`, and one button. Do not continue until every reply
arrives.

### 6. Connect Calendar

Add the Composio consumer key and Google Calendar connection. Run a read-only
test for the next three events. Do not create a webinar invite as the first test.

### 7. Connect proposals

Use `connect-tools.sh` to authenticate PandaDoc. Create a private draft named
`Connection Test`; confirm it is unsent.

### 8. Personalize the Operator

Let the first reply offer “jump in and go” or guided setup. Choose guided setup
and complete the Operator name, use case, first outcomes, persona, messaging
choice, permission boundary, and first private skill on screen. End with the
final “anything else?” question and the “we're all done” confirmation.

## Fallbacks

- Slow image build: switch to the prebuilt clean Droplet and continue from
  `setup.sh`; explain that the participant's build continues in the background.
- OAuth outage: mark the tool `not_connected`, finish the core bot, and return
  to the connector after the webinar.
- Bad token: replace only that value and re-run `setup.sh`; do not rebuild the
  Droplet from scratch.
- Bot does not reply: use the troubleshooting table and check channel status
  before touching the model configuration.

## Definition of done

The participant leaves with a healthy always-on Operator, private dashboard
access, fully proven Slack behavior, included skills plus owner-review controls,
a read-tested calendar/inbox connection, an unsent proposal draft, and a
private personalized knowledge vault.
