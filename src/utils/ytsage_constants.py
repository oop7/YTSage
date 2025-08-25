"""
YTSage application constants.

This module defines centralized constants used across the YTSage application.
By storing shared values in one place, it improves consistency, readability,
and maintainability of the codebase.
"""

import os
import platform
from pathlib import Path

# Assets Constants
ICON_PATH: Path = Path("assets/Icon/icon.png")
SOUND_PATH: Path = Path("assets/sound/notification.mp3")

OS_NAME: str = platform.system()  # Windows ; Darwin ; Linux

USER_HOME_DIR: Path = Path.home()

# OS Specific Constants
if OS_NAME == "Windows":
    # APP_PATH will be from system environment path or fallback to Path.home()
    APP_DIR: Path = Path(os.environ.get("LOCALAPPDATA", USER_HOME_DIR / "AppData" / "Local")) / "YTSage"
    APP_BIN_DIR: Path = APP_DIR / "bin"
    APP_DATA_DIR: Path = APP_DIR / "data"
    APP_LOG_DIR: Path = APP_DIR / "logs"

    YTDLP_DOWNLOAD_URL: str = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"


elif OS_NAME == "Darwin":  # macOS
    APP_DIR: Path = USER_HOME_DIR / "Library" / "Application Support" / "YTSage"
    APP_BIN_DIR: Path = APP_DIR / "bin"
    APP_DATA_DIR: Path = APP_DIR / "data"
    APP_LOG_DIR: Path = APP_DIR / "logs"

    YTDLP_DOWNLOAD_URL: str = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"

else:  # Linux and other UNIX-like
    APP_DIR: Path = USER_HOME_DIR / ".local" / "share" / "YTSage"
    APP_BIN_DIR: Path = APP_DIR / "bin"
    APP_DATA_DIR: Path = APP_DIR / "data"
    APP_LOG_DIR: Path = APP_DIR / "logs"

    YTDLP_DOWNLOAD_URL: str = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"

# ffmpeg download links
FFMPEG_7Z_DOWNLOAD_URL = "https://github.com/GyanD/codexffmpeg/releases/download/7.1.1/ffmpeg-7.1.1-full_build.7z"
FFMPEG_7Z_SHA256_URL = "https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.1.1-full_build.7z.sha256"
FFMPEG_ZIP_DOWNLOAD_URL = "https://github.com/GyanD/codexffmpeg/releases/download/7.1.1/ffmpeg-7.1.1-full_build.zip"

if __name__ == "__main__":
    print(f"OS_NAME: {OS_NAME}")
    print(f"USER_HOME_DIR: {USER_HOME_DIR}")
    print(f"APP_DIR: {APP_DIR}")
    print(f"APP_BIN_DIR: {APP_BIN_DIR}")
    print(f"APP_DATA_DIR: {APP_DATA_DIR}")
    print(f"APP_LOG_DIR: {APP_LOG_DIR}")
    print(f"YTDLP_DOWNLOAD_URL: {YTDLP_DOWNLOAD_URL}")

# moved to src\utils\ytsage_constants.py
# things to change with constant
# sys.platform
# if sys.platform == "win32":
# elif sys.platform == "darwin":
# os.getenv("LOCALAPPDATA")
# Path.home()
# get_ytdlp_install_dir()
# os_name
# self.os_type
# .parent
# icon and audio path
