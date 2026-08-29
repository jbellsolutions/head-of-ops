# Reviewed Hermes Agent v0.20.6 release. The tag is readable and the digest
# makes every build use the exact same upstream image.
FROM nousresearch/hermes-agent:v2026.8.27@sha256:e0df6adebddf29b91112aefc999d4aaf6846c9eb544faca5672a16a13590ff79

USER root

# Live voice stack.
RUN uv pip install --python /opt/hermes/.venv/bin/python --no-cache \
      faster-whisper==1.2.1 \
      edge-tts==7.2.7

# The browser router source is byte-for-byte identical to the active live copy.
COPY files/local-packages/super-browser /opt/super-browser
RUN uv venv --python /opt/hermes/.venv/bin/python /opt/super-browser/.venv \
    && uv pip install --python /opt/super-browser/.venv/bin/python \
         --require-hashes --no-cache \
         -r /opt/super-browser/requirements-runtime.lock \
    && PLAYWRIGHT_BROWSERS_PATH=/opt/playwright \
         /opt/super-browser/.venv/bin/python -m playwright install --with-deps chromium \
    && chmod +x /opt/super-browser/mcp/super-browser-server

ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright
