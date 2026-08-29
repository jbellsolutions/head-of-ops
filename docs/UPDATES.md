# Runtime and Update Guide

## Current reviewed runtime

Head of Ops is pinned to:

```text
Hermes Agent v0.20.6
release tag: v2026.8.27
image: nousresearch/hermes-agent:v2026.8.27
digest: sha256:e0df6adebddf29b91112aefc999d4aaf6846c9eb544faca5672a16a13590ff79
```

Release reference: [Hermes Agent v0.20.6](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.27).

The tag makes the version readable; the digest prevents a different image from
silently appearing under the same tag. Production never follows `latest`.

## What this refresh adds

The current runtime brings the newer Hermes Agent-view Slack experience,
clarify buttons, current slash-command generation, lean context-tail handling,
skill write approvals and auditing, multi-query tool search, managed remote MCP
catalog improvements, stronger update coordination, durable cron incidents,
optional OS-keychain secret encryption, and current browser/remote-host tooling.

Head of Ops keeps its existing operator identity, knowledge vault, Calendar,
inbox, document, proposal, Super Browser, messaging, memory, scheduling, and
approval design on top of that runtime.

## Update an installed Operator

From the repository checkout on the server, run:

```bash
./update.sh /srv/<operator>/.env
```

The update helper:

1. accepts only a fast-forward repository update;
2. runs the repository verification;
3. refreshes public runtime files without replacing private memory or existing
   skills;
4. rebuilds from the reviewed image digest;
5. restarts and waits for a healthy result;
6. regenerates the current Slack Agent-view manifest; and
7. checks and audits installed skills.

It deliberately does not force-update owner-customized skills. Review available
Hub updates with `hermes skills update` after reading the proposed changes.

Afterward, apply the generated Slack manifest and rerun the three message tests
in [SLACK-SETUP.md](SLACK-SETUP.md).

## Reviewing a future Hermes release

Before changing the runtime pin:

1. Read the official release notes and migration notes.
2. Record the exact release tag and multi-architecture digest.
3. Update both the Dockerfile pin and the public version label.
4. Regenerate `slack-manifest.yml` with that exact release and `--agent-view`.
5. Run `scripts/verify.sh` and the fresh-deployment smoke test.
6. Build the full image and prove its Hermes version and manifest.
7. Prove a Slack DM, channel thread, follow-up, button, skill, and restart on a
   non-production Operator before updating a live owner.
