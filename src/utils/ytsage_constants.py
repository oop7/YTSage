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
import sys
from pathlib import Path

# Handle resource paths for both development and installed package
def get_asset_path(asset_relative_path: str) -> Path:
    """
    Get the absolute path to an asset file, works both in development and installed package.
    
    Args:
        asset_relative_path: Relative path to the asset (e.g., "assets/Icon/icon.png")
    
    Returns:
        Path: Absolute path to the asset file
    """
    # Check if running as a frozen executable (PyInstaller, cx_Freeze, etc.)
    if getattr(sys, "frozen", False):
        # Running as a frozen executable
        # Try sys._MEIPASS first (PyInstaller)
        if hasattr(sys, "_MEIPASS"):
            asset_path = Path(sys._MEIPASS) / asset_relative_path
            if asset_path.exists():
                return asset_path
        
        # For cx_Freeze, assets are typically in lib/ directory next to the executable
        executable_dir = Path(sys.executable).parent
        
        # Try with lib/ prefix (cx_Freeze standard structure)
        asset_path = executable_dir / "lib" / asset_relative_path
        if asset_path.exists():
            return asset_path
        
        # Try directly in executable directory
        asset_path = executable_dir / asset_relative_path
        if asset_path.exists():
            return asset_path
    
    # Not frozen - try importlib.resources for installed packages
    try:
        # Use importlib.resources (standard in Python 3.9+)
        import importlib.resources as resources
        try:
            # Navigate to the package root and then to the asset
            package_path = resources.files('ytsage')
            asset_path = package_path / asset_relative_path
            if asset_path.is_file():
                return Path(str(asset_path))
        except (ImportError, AttributeError, FileNotFoundError):
            pass
            
    except Exception:
        pass
    
    # Fallback to relative path (for development environment)
    current_file = Path(__file__)
    # Go up from src/utils to ytsage root, then to asset
    ytsage_root = current_file.parent.parent.parent
    asset_path = ytsage_root / asset_relative_path
    
    return asset_path

# Assets Constants
ICON_PATH: Path = get_asset_path("assets/Icon/icon.png")
SOUND_PATH: Path = get_asset_path("assets/sound/notification.mp3")

OS_NAME: str = platform.system()  # Windows ; Darwin ; Linux

IS_FROZEN = getattr(sys, "frozen", False)
USER_HOME_DIR: Path = Path.home()

# OS Specific Constants
if OS_NAME == "Windows":
    OS_FULL_NAME: str = f"{OS_NAME} {platform.release()}"

    # Always use user data directory for app data, logs, config, and binaries
    # Even when frozen, we don't want to create these folders next to the executable
    APP_DIR: Path = Path(os.environ.get("LOCALAPPDATA", USER_HOME_DIR / "AppData" / "Local")) / "YTSage"
    APP_BIN_DIR: Path = APP_DIR / "bin"
    APP_DATA_DIR: Path = APP_DIR / "data"
    APP_LOG_DIR: Path = APP_DIR / "logs"
    APP_CONFIG_FILE: Path = APP_DATA_DIR / "ytsage_config.json"
    APP_HISTORY_FILE: Path = APP_DATA_DIR / "ytsage_history.json"
    APP_THUMBNAILS_DIR: Path = APP_DATA_DIR / "thumbnails"

    YTDLP_DOWNLOAD_URL: str = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
    YTDLP_APP_BIN_PATH: Path = APP_BIN_DIR / "yt-dlp.exe"

    SUBPROCESS_CREATIONFLAGS: int = subprocess.CREATE_NO_WINDOW

elif OS_NAME == "Darwin":  # macOS
    _mac_version = platform.mac_ver()[0]
    OS_FULL_NAME: str = f"macOS {_mac_version}" if _mac_version else "macOS"

    # Always use user data directory for app data, logs, config, and binaries
    # Even when frozen, we don't want to create these folders next to the executable
    APP_DIR: Path = USER_HOME_DIR / "Library" / "Application Support" / "YTSage"
    APP_BIN_DIR: Path = APP_DIR / "bin"
    APP_DATA_DIR: Path = APP_DIR / "data"
    APP_LOG_DIR: Path = APP_DIR / "logs"
    APP_CONFIG_FILE: Path = APP_DATA_DIR / "ytsage_config.json"
    APP_HISTORY_FILE: Path = APP_DATA_DIR / "ytsage_history.json"
    APP_THUMBNAILS_DIR: Path = APP_DATA_DIR / "thumbnails"

    YTDLP_DOWNLOAD_URL: str = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
    YTDLP_APP_BIN_PATH: Path = APP_BIN_DIR / "yt-dlp"

    SUBPROCESS_CREATIONFLAGS: int = 0


else:  # Linux and other UNIX-like
    OS_FULL_NAME: str = f"{OS_NAME} {platform.release()}"

    # Always use user data directory for app data, logs, config, and binaries
    # Even when frozen, we don't want to create these folders next to the executable
    APP_DIR: Path = USER_HOME_DIR / ".local" / "share" / "YTSage"
    APP_BIN_DIR: Path = APP_DIR / "bin"
    APP_DATA_DIR: Path = APP_DIR / "data"
    APP_LOG_DIR: Path = APP_DIR / "logs"
    APP_CONFIG_FILE: Path = APP_DATA_DIR / "ytsage_config.json"
    APP_HISTORY_FILE: Path = APP_DATA_DIR / "ytsage_history.json"
    APP_THUMBNAILS_DIR: Path = APP_DATA_DIR / "thumbnails"

    YTDLP_DOWNLOAD_URL: str = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
    
    # Check for environment variable override (critical for Flatpak support)
    _ytdlp_env_path = os.environ.get("YTDLP_APP_BIN_PATH")
    if _ytdlp_env_path:
        YTDLP_APP_BIN_PATH: Path = Path(_ytdlp_env_path)
    else:
        YTDLP_APP_BIN_PATH: Path = APP_BIN_DIR / "yt-dlp"

    SUBPROCESS_CREATIONFLAGS: int = 0

# Documentation URLs
YTDLP_DOCS_URL: str = "https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#usage-and-options"

# yt-dlp SHA256 checksums URL
YTDLP_SHA256_URL: str = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/SHA2-256SUMS"

# Deno download URLs and paths
if OS_NAME == "Windows":
    DENO_DOWNLOAD_URL: str = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-pc-windows-msvc.zip"
    DENO_SHA256_URL: str = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-pc-windows-msvc.zip.sha256sum"
    DENO_APP_BIN_PATH: Path = APP_BIN_DIR / "deno.exe"
elif OS_NAME == "Darwin":  # macOS
    DENO_DOWNLOAD_URL: str = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-apple-darwin.zip"
    DENO_SHA256_URL: str = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-apple-darwin.zip.sha256sum"
    DENO_APP_BIN_PATH: Path = APP_BIN_DIR / "deno"
else:  # Linux
    DENO_DOWNLOAD_URL: str = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-unknown-linux-gnu.zip"
    DENO_SHA256_URL: str = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-unknown-linux-gnu.zip.sha256sum"
    
    # Check for environment variable override (critical for Flatpak support)
    _deno_env_path = os.environ.get("DENO_APP_BIN_PATH")
    if _deno_env_path:
        DENO_APP_BIN_PATH: Path = Path(_deno_env_path)
    else:
        DENO_APP_BIN_PATH: Path = APP_BIN_DIR / "deno"

# FFmpeg download links (Essentials build - always latest version)
FFMPEG_7Z_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z"
FFMPEG_ZIP_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_7Z_SHA256_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z.sha256"
FFMPEG_ZIP_SHA256_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip.sha256"
FFMPEG_7Z_VERSION_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z.ver"
FFMPEG_ZIP_VERSION_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip.ver"

# =============================================================================
# File Extension Constants
# =============================================================================
# Centralized file extension definitions to avoid duplication across modules
# Use these constants for file type detection throughout the application

# Video file extensions (container formats that typically contain video)
VIDEO_EXTENSIONS: frozenset[str] = frozenset({
    ".mp4", ".webm", ".mkv", ".avi", ".mov", ".flv"
})

# Audio file extensions (audio-only formats)
AUDIO_EXTENSIONS: frozenset[str] = frozenset({
    ".mp3", ".m4a", ".aac", ".wav", ".ogg", ".opus", ".flac"
})

# Subtitle file extensions
SUBTITLE_EXTENSIONS: frozenset[str] = frozenset({
    ".vtt", ".srt", ".ass", ".ssa"
})

# Combined video and audio extensions (for file search operations)
MEDIA_EXTENSIONS: frozenset[str] = VIDEO_EXTENSIONS | AUDIO_EXTENSIONS

if __name__ == "__main__":
    # If this file is run directly, print directory information; if imported, create the necessary directories for the application.
    # for debug, to check os specific variable which can be different based on os.
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
        "SUBPROCESS_CREATIONFLAGS": SUBPROCESS_CREATIONFLAGS,
    }
    for key, value in info.items():
        print(f"{key}: {value}")
else:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    APP_BIN_DIR.mkdir(parents=True, exist_ok=True)
    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    APP_LOG_DIR.mkdir(parents=True, exist_ok=True)
    APP_THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Ensure custom yt-dlp directory exists if set
    if OS_NAME not in ["Windows", "Darwin"]:
        # Ensure parent directories exist for custom paths
        if "YTDLP_APP_BIN_PATH" in globals():
            YTDLP_APP_BIN_PATH.parent.mkdir(parents=True, exist_ok=True)
        if "DENO_APP_BIN_PATH" in globals():
            DENO_APP_BIN_PATH.parent.mkdir(parents=True, exist_ok=True)
