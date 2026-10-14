# YTSage Self-Hosted (Docker)

Run **YTSage** in a Docker container and access the full desktop application directly through any modern web browser via WebRTC/HTML5, without needing to install Python, Qt, or desktop dependencies on your host.

Powered by [LinuxServer.io's KasmVNC base image](https://github.com/linuxserver/docker-baseimage-kasmvnc).

---

## 🚀 Quick Start with Docker Compose

The simplest way to run YTSage self-hosted:

1. Clone or download the repository:
   ```bash
   git clone https://github.com/oop7/YTSage.git
   cd YTSage
   ```

2. Start the container:
   ```bash
   docker compose up -d
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```
   *(or `https://localhost:3001` for HTTPS)*

---

## 🐳 Docker CLI

You can also build and run the container directly with Docker CLI:

### Build Image
```bash
docker build -t ytsage:latest -f docker/Dockerfile .
```

### Run Container
```bash
docker run -d \
  --name=ytsage \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -e TITLE=YTSage \
  -p 3000:3000 \
  -p 3001:3001 \
  -v /path/to/config:/config \
  -v /path/to/downloads:/downloads \
  --restart unless-stopped \
  ytsage:latest
```

---

## ⚙️ Configuration & Environment Variables

| Parameter | Function | Default |
|---|---|---|
| `-p 3000:3000` | HTTP Web GUI | `3000` |
| `-p 3001:3001` | HTTPS Web GUI | `3001` |
| `-e PUID=1000` | User ID for volume write permissions | `1000` |
| `-e PGID=1000` | Group ID for volume write permissions | `1000` |
| `-e TZ=Etc/UTC` | Timezone | `Etc/UTC` |
| `-e TITLE=YTSage` | Web page title | `YTSage` |
| `-v /config` | Persistent app data, settings, history, and binaries | `./config` |
| `-v /downloads` | Default destination folder for downloaded media | `./downloads` |

---

## 🌟 Highlights

- **Native Desktop GUI in Browser**: Seamless HTML5/WebRTC streaming powered by KasmVNC with high frame rates, low latency, and clipboard synchronization.
- **Batteries Included**: FFmpeg, pre-fetched yt-dlp, and Deno are configured automatically.
- **Persistent Storage**: All downloaded files save directly to your mounted `/downloads` directory, while history and settings persist in `/config`.
- **NAS & Homelab Friendly**: Built-in support for `PUID` and `PGID` ensures downloaded files have the correct ownership for Synology, Unraid, TrueNAS, CasaOS, and Linux servers.

## Download location in Docker

The application runs as a desktop application inside the container and is streamed to your browser by KasmVNC. Downloads are saved to `/downloads`, which is the host directory mounted by the Compose file as `./downloads`. They therefore appear on the Docker host, not in the browser client's normal Downloads folder.

The folder button opens the mounted downloads directory in the container desktop. To get a file onto a separate client device, copy it from the host's `downloads` directory or use a file-sharing service provided by your host/NAS.
