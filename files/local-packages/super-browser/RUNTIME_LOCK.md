# Super Browser Runtime

The core MCP and browser dependency graph comes from the committed,
hash-verified `requirements-runtime.lock`. The image then pins the four direct
package versions used by the live operator:

- `mcp==1.28.0`
- `playwright==1.60.0`
- `browserbase==1.13.0`
- `browser-use-sdk==3.8.4`

The image installs Playwright Chromium during the build. Super Browser source
is loaded from `/opt/super-browser/src` through `PYTHONPATH`, matching the live
MCP launch pattern. Change package versions only through a reviewed image
rebuild; do not install replacements inside a running operator.
