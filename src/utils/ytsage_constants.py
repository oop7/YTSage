"""
This module defines centralized constants used across the YTSage application.
By storing shared values in one place, it improves consistency, readability,
and maintainability of the codebase.

Constants include:
- Asset paths for icons and notification sounds.
- OS detection and platform-specific directory paths for application data, binaries, logs, and configuration.
- Download URLs for yt-dlp and ffmpeg binaries.
- SUBPROCESS_CREATIONFLAGS: Used to specify subprocess creation flags (e.g., subprocess.CREATE_NO_WINDOW on Windows to hide the console window).
Directories are automatically created when the module is imported, ensuring the required structure exists for the application.
YTSage application constants.

"""

import os
import platform
import subprocess
from pathlib import Path

# Assets Constants
ICON_PATH: Path = Path("assets/Icon/icon.png")
SOUND_PATH: Path = Path("assets/sound/notification.mp3")

OS_NAME: str = platform.system()  # Windows ; Darwin ; Linux

USER_HOME_DIR: Path = Path.home()

# OS Specific Constants
if OS_NAME == "Windows":
    OS_FULL_NAME: str = f"{OS_NAME} {platform.release()}"

    # APP_PATH will be from system environment path or fallback to Path.home()
    APP_DIR: Path = Path(os.environ.get("LOCALAPPDATA", USER_HOME_DIR / "AppData" / "Local")) / "YTSage"
    APP_BIN_DIR: Path = APP_DIR / "bin"
    APP_DATA_DIR: Path = APP_DIR / "data"
    APP_LOG_DIR: Path = APP_DIR / "logs"
    APP_CONFIG_FILE: Path = APP_DATA_DIR / "ytsage_config.json"

    YTDLP_DOWNLOAD_URL: str = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
    YTDLP_APP_BIN_PATH: Path = APP_BIN_DIR / "yt-dlp.exe"
    
    # Documentation URLs
    YTDLP_DOCS_URL: str = "https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#usage-and-options"

    SUBPROCESS_CREATIONFLAGS: int = subprocess.CREATE_NO_WINDOW

elif OS_NAME == "Darwin":  # macOS
    _mac_version = platform.mac_ver()[0]
    OS_FULL_NAME: str = f"macOS {_mac_version}" if _mac_version else "macOS"

    APP_DIR: Path = USER_HOME_DIR / "Library" / "Application Support" / "YTSage"
    APP_BIN_DIR: Path = APP_DIR / "bin"
    APP_DATA_DIR: Path = APP_DIR / "data"
    APP_LOG_DIR: Path = APP_DIR / "logs"
    APP_CONFIG_FILE: Path = APP_DATA_DIR / "ytsage_config.json"

    YTDLP_DOWNLOAD_URL: str = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
    YTDLP_APP_BIN_PATH: Path = APP_BIN_DIR / "yt-dlp"
    
    # Documentation URLs
    YTDLP_DOCS_URL: str = "https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#usage-and-options"

    SUBPROCESS_CREATIONFLAGS: int = 0


else:  # Linux and other UNIX-like
    OS_FULL_NAME: str = f"{OS_NAME} {platform.release()}"

    APP_DIR: Path = USER_HOME_DIR / ".local" / "share" / "YTSage"
    APP_BIN_DIR: Path = APP_DIR / "bin"
    APP_DATA_DIR: Path = APP_DIR / "data"
    APP_LOG_DIR: Path = APP_DIR / "logs"
    APP_CONFIG_FILE: Path = APP_DATA_DIR / "ytsage_config.json"

    YTDLP_DOWNLOAD_URL: str = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
    YTDLP_APP_BIN_PATH: Path = APP_BIN_DIR / "yt-dlp"
    
    # Documentation URLs
    YTDLP_DOCS_URL: str = "https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#usage-and-options"

    SUBPROCESS_CREATIONFLAGS: int = 0


# ffmpeg download links
FFMPEG_7Z_DOWNLOAD_URL = "https://github.com/GyanD/codexffmpeg/releases/download/7.1.1/ffmpeg-7.1.1-full_build.7z"
FFMPEG_7Z_SHA256_URL = "https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.1.1-full_build.7z.sha256"
FFMPEG_ZIP_DOWNLOAD_URL = "https://github.com/GyanD/codexffmpeg/releases/download/7.1.1/ffmpeg-7.1.1-full_build.zip"

if __name__ == "__main__":
    # If this file is run directly, print directory information; if imported, create the necessary directories for the application.
    info = {
        "OS_NAME": OS_NAME,
        "OS_FULL_NAME": OS_FULL_NAME,
        "USER_HOME_DIR": str(USER_HOME_DIR),
        "APP_DIR": str(APP_DIR),
        "APP_BIN_DIR": str(APP_BIN_DIR),
        "APP_DATA_DIR": str(APP_DATA_DIR),
        "APP_LOG_DIR": str(APP_LOG_DIR),
        "APP_CONFIG_FILE": str(APP_CONFIG_FILE),
        "YTDLP_DOWNLOAD_URL": YTDLP_DOWNLOAD_URL,
        "YTDLP_APP_BIN_PATH": YTDLP_APP_BIN_PATH,
        "YTDLP_DOCS_URL": YTDLP_DOCS_URL,
        "SUBPROCESS_CREATIONFLAGS": SUBPROCESS_CREATIONFLAGS,
    }
    for key, value in info.items():
        print(f"{key}: {value}")
else:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    APP_BIN_DIR.mkdir(parents=True, exist_ok=True)
    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    APP_LOG_DIR.mkdir(parents=True, exist_ok=True)
