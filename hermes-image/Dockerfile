# Exact Hermes release and digest running on the live Single Brain operator.
FROM nousresearch/hermes-agent@sha256:248024e18a05b0ee2d600a81538b1a3fd60653afa699814f68c2bdd928c19b47

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
    && uv pip install --python /opt/super-browser/.venv/bin/python --no-cache \
         mcp==1.28.0 \
         playwright==1.60.0 \
         browserbase==1.13.0 \
         browser-use-sdk==3.8.4 \
    && PLAYWRIGHT_BROWSERS_PATH=/opt/playwright \
         /opt/super-browser/.venv/bin/python -m playwright install --with-deps chromium \
    && chmod +x /opt/super-browser/mcp/super-browser-server

ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright
