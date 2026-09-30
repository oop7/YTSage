#!/usr/bin/env bash

chmod 755 /defaults 2>/dev/null || true
chmod +x /defaults/startwm.sh 2>/dev/null || true
rm -f /tmp/.X1-lock /tmp/.X11-unix/X1 2>/dev/null || true

# Ensure downloads directory exists and has permissive permissions
mkdir -p /downloads
chmod 777 /downloads 2>/dev/null || true

# Ensure user directories exist
mkdir -p /config/.config/openbox
mkdir -p /config/.local/share/YTSage/bin
mkdir -p /config/.local/share/YTSage/data

# Seed yt-dlp binary if not present in user config bin directory
if [ ! -f /config/.local/share/YTSage/bin/yt-dlp ] && [ -f /defaults/bin/yt-dlp ]; then
    cp /defaults/bin/yt-dlp /config/.local/share/YTSage/bin/yt-dlp
    chmod +x /config/.local/share/YTSage/bin/yt-dlp
fi

# Seed deno binary if not present in user config bin directory
if [ ! -f /config/.local/share/YTSage/bin/deno ] && [ -f /defaults/bin/deno ]; then
    cp /defaults/bin/deno /config/.local/share/YTSage/bin/deno
    chmod +x /config/.local/share/YTSage/bin/deno
fi

# Link /config/Downloads to /downloads so file dialogs map directly to mounted downloads volume
ln -sfn /downloads /config/Downloads

# Always ensure autostart script is installed
cp /defaults/autostart /config/.config/openbox/autostart
chmod +x /config/.config/openbox/autostart

# Ensure Openbox rc.xml exists
if [ ! -f /config/.config/openbox/rc.xml ]; then
    if [ -f /defaults/rc.xml ]; then
        cp /defaults/rc.xml /config/.config/openbox/rc.xml
    elif [ -f /etc/xdg/openbox/rc.xml ]; then
        cp /etc/xdg/openbox/rc.xml /config/.config/openbox/rc.xml
    fi
fi

# Set ownership to abc user for config directory
chown -R abc:abc /config 2>/dev/null || true
