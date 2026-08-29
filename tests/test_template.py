from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TemplateTests(unittest.TestCase):
    def test_required_beginner_and_runtime_files_exist(self) -> None:
        required = [
            "README.md",
            "START-HERE.md",
            "setup.sh",
            "update.sh",
            "new-agent.sh",
            "compose.yml",
            "hermes-image/Dockerfile",
            "hermes/config.template.yaml",
            "bin/connect-tools.sh",
            "bin/connect-channels.sh",
            "bin/finish-setup.sh",
            "bin/operator-lib.sh",
            "slack-manifest.yml",
            "tests/smoke_deployment.sh",
            "files/SOUL.md",
            "files/AGENTS.md",
            "files/agent-knowledge/00.Onboarding.md",
            "files/skills/business/operator-onboarding/SKILL.md",
            "files/skills/business/proposal-builder/SKILL.md",
            "files/skills/communication/inbox-operator/SKILL.md",
            "files/skills/communication/slack-operator/SKILL.md",
            "files/skills/productivity/calendar-operator/SKILL.md",
            "docs/WEBINAR-WALKTHROUGH.md",
            "docs/LIVE-PARITY.md",
            "docs/SLACK-SETUP.md",
            "docs/SKILLS.md",
            "docs/UPDATES.md",
        ]
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_live_image_is_digest_pinned(self) -> None:
        dockerfile = (ROOT / "hermes-image/Dockerfile").read_text()
        self.assertIn(
            "nousresearch/hermes-agent:v2026.8.27@sha256:e0df6adebddf29b91112aefc999d4aaf6846c9eb544faca5672a16a13590ff79",
            dockerfile,
        )
        self.assertNotIn(":latest", dockerfile)

    def test_super_browser_source_matches_live_audit(self) -> None:
        source_root = ROOT / "files/local-packages/super-browser/src"
        source_files = sorted(source_root.rglob("*.py"))
        digest = hashlib.sha256()
        for path in source_files:
            digest.update(path.relative_to(source_root).as_posix().encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
        self.assertEqual(21, len(source_files))
        self.assertEqual(
            "7fad2facb6ba04f6f33c533aa3c5c36cd35afe27af50ef76e64587d292e12522",
            digest.hexdigest(),
        )

    def test_super_browser_runtime_lock_is_exact_and_hashed(self) -> None:
        lock = (ROOT / "files/local-packages/super-browser/requirements-runtime.lock").read_text()
        for requirement in ("playwright==1.60.0", "browserbase==1.13.0", "browser-use-sdk==3.8.4"):
            self.assertIn(requirement, lock)
        requirement_lines = [
            line.strip().removesuffix("\\").strip()
            for line in lock.splitlines()
            if line and not line[0].isspace() and not line.startswith("#")
        ]
        self.assertGreater(len(requirement_lines), 10)
        for requirement in requirement_lines:
            self.assertIn("==", requirement)
        self.assertGreaterEqual(lock.count("--hash=sha256:"), len(requirement_lines))
        dockerfile = (ROOT / "hermes-image/Dockerfile").read_text()
        self.assertIn("uv pip install --no-config", dockerfile)

    def test_public_tree_contains_no_live_identifiers_or_secret_shapes(self) -> None:
        forbidden_literals = [
            "104.236.11.200",
            "100.117.225.14",
            "T01D6BZEGA0",
            "U01D077J78S",
            "1264488761",
        ]
        secret_patterns = [
            re.compile(r"gh[opsu]_[A-Za-z0-9]{20,}"),
            re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
            re.compile(r"xox[baprs]-[A-Za-z0-9-]{12,}"),
            re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
            re.compile(r"sk-(?:live|test)?[_-]?[A-Za-z0-9]{20,}"),
        ]
        tracked = subprocess.check_output(
            ["git", "ls-files", "-z"], cwd=ROOT
        ).split(b"\0")
        violations: list[str] = []
        for raw in tracked:
            if not raw:
                continue
            path = ROOT / raw.decode()
            if path == Path(__file__).resolve():
                continue
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            for literal in forbidden_literals:
                if literal in text:
                    violations.append(f"{path.relative_to(ROOT)} contains {literal}")
            for pattern in secret_patterns:
                if pattern.search(text):
                    violations.append(f"{path.relative_to(ROOT)} matches {pattern.pattern}")
        self.assertEqual([], violations)

    def test_minimal_config_render_has_core_tools_only(self) -> None:
        env = {
            **os.environ,
            "HERMES_MODEL": "openai/gpt-5.6-luna",
            "AGENT_PERSONA": "concise",
            "TELEGRAM_BOT_TOKEN": "placeholder",
        }
        for name in (
            "FIREWORKS_API_KEY",
            "DEEPSEEK_API_KEY",
            "TOGETHER_API_KEY",
            "COMPOSIO_API_KEY",
            "TELEGRAM_HOME_CHANNEL",
            "SLACK_HOME_CHANNEL",
            "SLACK_BOT_TOKEN",
            "SLACK_APP_TOKEN",
            "DISCORD_BOT_TOKEN",
            "BLUEBUBBLES_SERVER_URL",
            "BLUEBUBBLES_PASSWORD",
        ):
            env.pop(name, None)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "config.yaml"
            subprocess.run(
                [
                    "python3",
                    str(ROOT / "scripts/render_config.py"),
                    str(ROOT / "hermes/config.template.yaml"),
                    str(output),
                ],
                env=env,
                check=True,
            )
            text = output.read_text()
        self.assertIn("telegram:\n    enabled: true", text)
        self.assertIn("slack:\n    enabled: false", text)
        self.assertIn("discord:\n    enabled: false", text)
        self.assertIn("bluebubbles:\n    enabled: false", text)
        self.assertIn("super-browser:", text)
        self.assertIn("pandadoc:", text)
        self.assertIn("higgsfield:", text)
        self.assertNotIn("copywriting_retrieval:", text)
        self.assertNotIn("composio:", text)
        self.assertIn("fallback_providers: []", text)
        self.assertIn("tail_mode: lean", text)
        self.assertIn("write_approval: true", text)
        self.assertIn("guard_agent_created: true", text)
        self.assertNotIn("__", text)

    def test_full_config_render_adds_calendar_and_fallbacks(self) -> None:
        env = {
            **os.environ,
            "HERMES_MODEL": "openai/gpt-5.6-luna",
            "AGENT_PERSONA": "concise",
            "SLACK_BOT_TOKEN": "placeholder",
            "SLACK_APP_TOKEN": "placeholder",
            "DISCORD_BOT_TOKEN": "placeholder",
            "BLUEBUBBLES_SERVER_URL": "https://bluebubbles.example.test",
            "BLUEBUBBLES_PASSWORD": "placeholder",
            "COMPOSIO_API_KEY": "value-with-special-&-characters",
            "FIREWORKS_API_KEY": "placeholder",
            "DEEPSEEK_API_KEY": "placeholder",
            "TOGETHER_API_KEY": "placeholder",
            "TELEGRAM_HOME_CHANNEL": "123",
        }
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "config.yaml"
            subprocess.run(
                [
                    "python3",
                    str(ROOT / "scripts/render_config.py"),
                    str(ROOT / "hermes/config.template.yaml"),
                    str(output),
                ],
                env=env,
                check=True,
            )
            text = output.read_text()
        self.assertIn("composio:", text)
        self.assertIn('"value-with-special-&-characters"', text)
        self.assertIn("api.fireworks.ai", text)
        self.assertIn("api.deepseek.com", text)
        self.assertIn("api.together.xyz", text)
        self.assertIn("discord:\n    enabled: true", text)
        self.assertIn("bluebubbles:\n    enabled: true", text)
        self.assertNotIn("__", text)

    def test_skill_frontmatter_is_present(self) -> None:
        skill_paths = sorted((ROOT / "files/skills").rglob("SKILL.md"))
        self.assertGreaterEqual(len(skill_paths), 6)
        for path in skill_paths:
            text = path.read_text()
            self.assertTrue(text.startswith("---\n"), path)
            self.assertRegex(text, r"(?m)^name: [a-z0-9-]+$")
            self.assertRegex(text, r"(?m)^description: .+$")

    def test_public_seed_is_generic_and_first_run_is_enforced(self) -> None:
        seed_paths = [ROOT / "files/SOUL.md", ROOT / "files/AGENTS.md"]
        seed_paths.extend((ROOT / "files/agent-knowledge").rglob("*.md"))
        seed_paths.extend((ROOT / "files/skills").rglob("*.md"))
        seed = "\n".join(path.read_text() for path in seed_paths)
        for proprietary_marker in (
            "Money Desk",
            "SpeakerAgent",
            "aiintegraterz.com/revenue-partner",
            "kdvm_kRZk8A",
        ):
            self.assertNotIn(proprietary_marker, seed)
        self.assertIn("jump in and go", seed.lower())
        self.assertIn("All right — we're all done", seed)
        self.assertFalse(
            any(
                path.is_file()
                for path in (ROOT / "files/skills/go-to-market/revenue-partner").rglob("*")
            )
        )

    def test_slack_manifest_and_finish_menu_cover_onboarding(self) -> None:
        manifest = (ROOT / "slack-manifest.yml").read_text()
        for required in (
            "socket_mode_enabled: true",
            "agent_view:",
            "assistant:write",
            "app_context_changed",
            "app_home_opened",
            "app_mentions:read",
            "channels:history",
            "chat:write",
            "files:read",
            "message.im",
            "message.channels",
            "command: /hermes",
            "command: /reload-skills",
        ):
            self.assertIn(required, manifest)
        self.assertEqual(50, manifest.count("  - command:"))
        finish = (ROOT / "bin/finish-setup.sh").read_text()
        self.assertIn("iMessage", finish)
        self.assertIn("Calendar", finish)
        self.assertIn("All right — we're all done", finish)

    def test_head_of_ops_brand_and_install_links(self) -> None:
        readme = (ROOT / "README.md").read_text()
        start_here = (ROOT / "START-HERE.md").read_text()
        provisioner = (ROOT / "provision-vps.sh").read_text()
        manifest = (ROOT / "slack-manifest.yml").read_text()
        self.assertTrue(readme.startswith("# Head of Ops\n"))
        self.assertIn("https://github.com/jbellsolutions/head-of-ops", readme)
        self.assertIn("https://github.com/jbellsolutions/head-of-ops.git", start_here)
        self.assertIn("https://github.com/jbellsolutions/head-of-ops.git", provisioner)
        self.assertIn("name: Head of Ops", manifest)
        for text in (readme, start_here, provisioner):
            self.assertNotIn("jbellsolutions/revenue-partner-agent", text)

    def test_slack_is_owner_allowlisted_and_current(self) -> None:
        setup = (ROOT / "setup.sh").read_text()
        channels = (ROOT / "bin/connect-channels.sh").read_text()
        compose = (ROOT / "compose.yml").read_text()
        config = (ROOT / "agent.example.env").read_text()
        for text in (setup, channels):
            self.assertIn("Slack Member ID", text)
            self.assertIn("SLACK_ALLOWED_USERS", text)
        operator_lib = (ROOT / "bin/operator-lib.sh").read_text()
        self.assertIn("--agent-view", setup)
        self.assertIn("--agent-view", operator_lib)
        self.assertIn("SLACK_ALLOWED_USERS: ${SLACK_ALLOWED_USERS:-}", compose)
        self.assertIn("SLACK_ALLOWED_USERS=", config)
        self.assertNotIn("--no-assistant", setup + operator_lib)

    def test_deployed_copy_contains_post_launch_setup_assets(self) -> None:
        installer = (ROOT / "new-agent.sh").read_text()
        for asset in (
            "connect-channels.sh",
            "connect-tools.sh",
            "finish-setup.sh",
            "operator-lib.sh",
            "render_config.py",
            "slack-manifest.yml",
        ):
            self.assertIn(asset, installer)


if __name__ == "__main__":
    unittest.main()
