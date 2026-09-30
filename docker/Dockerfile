FROM ghcr.io/linuxserver/baseimage-kasmvnc:debianbookworm

LABEL maintainer="oop7"
LABEL org.opencontainers.image.title="YTSage Web"
LABEL org.opencontainers.image.description="Self-hosted Web GUI for YTSage YouTube Downloader"
LABEL org.opencontainers.image.source="https://github.com/oop7/YTSage"

ENV TITLE="YTSage" \
    YTSAGE_DOWNLOAD_PATH="/downloads" \
    YTSAGE_DOWNLOAD_DIR="/downloads" \
    VIRTUAL_ENV="/opt/venv" \
    PATH="/opt/venv/bin:/lsiopy/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    curl \
    ca-certificates \
    unzip \
    pcmanfm \
    fonts-noto-color-emoji \
    fonts-dejavu-core \
    libgl1 \
    libegl1 \
    libglib2.0-0 \
    libfontconfig1 \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    libxcb1 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxrender1 \
    libxi6 \
    libxext6 \
    libasound2 \
    libpulse0 \
    libpipewire-0.3-0 \
    && rm -rf /var/lib/apt/lists/*

# Pre-fetch yt-dlp and deno so first container start has tools ready
RUN mkdir -p /defaults/bin && \
    curl -fsSL https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /defaults/bin/yt-dlp && \
    chmod +x /defaults/bin/yt-dlp && \
    curl -fsSL https://github.com/denoland/deno/releases/latest/download/deno-x86_64-unknown-linux-gnu.zip -o /tmp/deno.zip && \
    unzip -q /tmp/deno.zip -d /defaults/bin && \
    chmod +x /defaults/bin/deno && \
    rm -f /tmp/deno.zip

# Create Python virtual environment
RUN python3 -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/pip install --no-cache-dir --upgrade pip wheel setuptools

WORKDIR /app
COPY pyproject.toml README.md MANIFEST.in ./
COPY ytsage ./ytsage
COPY branding ./branding

# Install YTSage into virtual environment
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir .

# Copy docker root overlay files
COPY docker/root/ /

RUN chmod 755 /defaults \
    && chmod +x /defaults/startwm.sh /defaults/autostart \
    && chmod +x /custom-cont-init.d/10-ytsage-setup.sh \
    && sed -i 's/\r$//' /etc/s6-overlay/s6-rc.d/svc-de/run \
    && chmod +x /etc/s6-overlay/s6-rc.d/svc-de/run \
    && sed -i "/^socket.on('audio', processAudio);$/a window.addEventListener('load', function () { audio(); });" /kclient/public/js/kclient.js \
    && sed -i "/case 'control_open':/i\\      case 'enable_audio':\n        if (player.audioCtx) { player.audioCtx.resume(); }\n        break;" /kclient/public/js/kclient.js

EXPOSE 3000 3001
VOLUME ["/config", "/downloads"]
