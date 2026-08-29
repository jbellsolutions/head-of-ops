# Skills: Included, Private, and Current

Hermes skills are reusable procedures. Memory remembers durable facts about an
owner; a skill explains how to perform a repeatable workflow.

Official reference: [Hermes Skills Hub](https://hermes-agent.nousresearch.com/docs/skills).

## Included with Head of Ops

Every installation starts with generic, owner-safe procedures for:

- first-run operator onboarding;
- Calendar work;
- inbox work;
- Slack operations;
- business documents; and
- proposal drafting and PandaDoc handoff.

It also includes the Super Browser planner, orchestrator, verifier, publishing
safety guard, and provider specialist skills already shipped in this
repository. The current Hermes image contributes its complete bundled catalog
for research, documents, development, browsing, planning, creative work, and
agent operations.

Existing owner-created skills under `/srv/<operator>/hermes/data/skills` are
preserved during setup reruns and runtime updates.

## Use a skill in Slack

The reliable Slack form is an exclamation mark followed by the skill name:

```text
!calendar-operator show my next three events; do not change anything
!proposal-builder draft a private proposal; do not send it
!operator-onboarding continue my setup
/reload-skills
```

Hermes also loads a skill naturally when the owner's request matches its
description. Slack caps every app at 50 native slash commands, so not every
installed skill appears in Slack's slash-command picker.

## See, search, and install optional skills

On the private server:

```bash
docker exec -it -u hermes head-of-ops /opt/hermes/.venv/bin/hermes skills list
docker exec -it -u hermes head-of-ops /opt/hermes/.venv/bin/hermes skills browse --source official
docker exec -it -u hermes head-of-ops /opt/hermes/.venv/bin/hermes skills search calendar
docker exec -it -u hermes head-of-ops /opt/hermes/.venv/bin/hermes skills inspect official/security/1password
docker exec -it -u hermes head-of-ops /opt/hermes/.venv/bin/hermes skills install official/security/1password
```

Replace `head-of-ops` with the chosen Operator name. Inspect a skill before
installing it. Prefer the official catalog; community skills are scanned but
still require human judgment.

## Owner approval is enabled

This repository turns on `skills.write_approval` and the agent-created-skill
scanner. Head of Ops may propose a new or improved private procedure, but the
change is staged until the owner approves it:

```text
!skills pending
!skills diff <id>
!skills approve <id>
!skills reject <id>
!skills approval on
```

The same review works in the dashboard or CLI. A full diff is easiest to read
there. Pending changes survive a restart.

## Check and update safely

```bash
docker exec -u hermes head-of-ops /opt/hermes/.venv/bin/hermes skills check
docker exec -u hermes head-of-ops /opt/hermes/.venv/bin/hermes skills audit
docker exec -it -u hermes head-of-ops /opt/hermes/.venv/bin/hermes skills update
```

`skills update` updates Hub-installed skills when a reviewed version is
available. Locally edited skills are skipped unless `--force` is used. Do not
force-update an owner-customized procedure without first reading the diff and
keeping a backup.
