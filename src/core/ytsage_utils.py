import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pkg_resources
import requests
from packaging import version

from src.core.ytsage_ffmpeg import check_ffmpeg_installed, get_ffmpeg_install_path
from src.utils.ytsage_logger import logger
from src.core.ytsage_yt_dlp import get_yt_dlp_path
from src.utils.ytsage_constants import (
    APP_CONFIG_FILE,
    OS_NAME,
    SUBPROCESS_CREATIONFLAGS,
    USER_HOME_DIR,
    YTDLP_APP_BIN_PATH,
    YTDLP_DOWNLOAD_URL,
)

# Cache for version information to avoid delays
_version_cache = {
    "ytdlp": {"version": None, "path": None, "last_check": 0, "path_mtime": 0},
    "ffmpeg": {"version": None, "path": None, "last_check": 0, "path_mtime": 0},
}

# Cache expiry time in seconds (5 minutes)
CACHE_EXPIRY = 300


def get_file_mtime(filepath) -> float:
    """Get file modification time safely."""
    try:
        if filepath and Path(filepath).exists():
            return Path(filepath).stat().st_mtime
    except Exception:
        pass
    return 0


def should_refresh_cache(tool_name, current_path) -> bool:
    """Determine if cache should be refreshed for a tool."""
    cache = _version_cache.get(tool_name, {})
    current_time = time.time()

    # Always refresh if no cached data
    if not cache.get("version"):
        return True

    # Refresh if path changed
    if cache.get("path") != current_path:
        return True

    # Refresh if file was modified
    current_mtime = get_file_mtime(current_path)
    if current_mtime > cache.get("path_mtime", 0):
        return True

    # Refresh if cache expired
    if current_time - cache.get("last_check", 0) > CACHE_EXPIRY:
        return True

    return False


def update_version_cache(tool_name, version_info, path, force_save=False) -> None:
    """Update the version cache and optionally save to config."""
    current_time = time.time()
    current_mtime = get_file_mtime(path)

    _version_cache[tool_name] = {
        "version": version_info,
        "path": path,
        "last_check": current_time,
        "path_mtime": current_mtime,
    }

    # Save to persistent config
    if force_save:
        save_version_cache_to_config()


def load_version_cache_from_config() -> None:
    """Load cached version info from config file."""
    try:
        config = load_config()
        cached_versions = config.get("cached_versions", {})

        for tool_name, cache_data in cached_versions.items():
            if tool_name in _version_cache:
                _version_cache[tool_name].update(cache_data)
    except Exception as e:
        logger.exception(f"Error loading version cache: {e}")


def save_version_cache_to_config() -> None:
    """Save version cache to config file."""
    try:
        config = load_config()
        config["cached_versions"] = _version_cache.copy()
        save_config(config)
    except Exception as e:
        logger.exception(f"Error saving version cache: {e}")


def get_ytdlp_version_cached() -> str:
    """Get yt-dlp version with caching support."""
    try:
        current_path = get_yt_dlp_path()

        # Check if we need to refresh cache
        if not should_refresh_cache("ytdlp", current_path):
            cached_version = _version_cache["ytdlp"].get("version")
            if cached_version:
                return cached_version

        # Get fresh version info
        version_info = get_ytdlp_version_direct(current_path)

        # Update cache
        update_version_cache("ytdlp", version_info, current_path)

        return version_info
    except Exception as e:
        logger.exception(f"Error getting cached yt-dlp version: {e}")
        return "Error getting version"


def get_ffmpeg_version_cached() -> str:
    """Get FFmpeg version with caching support."""
    try:
        # Try to find ffmpeg path
        current_path = "ffmpeg"  # Default to system PATH

        # Check if we need to refresh cache
        if not should_refresh_cache("ffmpeg", current_path):
            cached_version = _version_cache["ffmpeg"].get("version")
            if cached_version:
                return cached_version

        # Get fresh version info
        version_info = get_ffmpeg_version_direct()

        # Update cache
        update_version_cache("ffmpeg", version_info, current_path)

        return version_info
    except Exception as e:
        logger.exception(f"Error getting cached FFmpeg version: {e}")
        return "Error getting version"


def refresh_version_cache(force=False) -> bool:
    """Manually refresh version cache for both tools."""
    try:
        # Refresh yt-dlp
        current_path = get_yt_dlp_path()
        version_info = get_ytdlp_version_direct(current_path)
        update_version_cache("ytdlp", version_info, current_path, force_save=True)

        # Refresh FFmpeg
        version_info = get_ffmpeg_version_direct()
        update_version_cache("ffmpeg", version_info, "ffmpeg", force_save=True)

        return True
    except Exception as e:
        logger.exception(f"Error refreshing version cache: {e}")
        return False


def get_ytdlp_version() -> str:
    """Get the version of yt-dlp (uses cached version for performance)."""
    return get_ytdlp_version_cached()


def get_ffmpeg_version() -> str:
    """Get the version of FFmpeg (uses cached version for performance)."""
    return get_ffmpeg_version_cached()


def get_ytdlp_version_direct(yt_dlp_path=None) -> str:
    """Get yt-dlp version directly without caching."""
    try:
        if yt_dlp_path is None:
            yt_dlp_path = get_yt_dlp_path()

        if not yt_dlp_path or yt_dlp_path == "yt-dlp":
            return "Not found"

        # Extra logic moved to src\utils\ytsage_constants.py
        result = subprocess.run(
            [yt_dlp_path, "--version"], capture_output=True, text=True, timeout=10, creationflags=SUBPROCESS_CREATIONFLAGS
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "Error getting version"
    except Exception as e:
        logger.exception(f"Error getting yt-dlp version: {e}")
        return "Error getting version"


def get_ffmpeg_version_direct() -> str:
    """Get FFmpeg version directly without caching."""
    try:
        # Extra logic moved to src\utils\ytsage_constants.py
        result = subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, timeout=10, creationflags=SUBPROCESS_CREATIONFLAGS
        )

        if result.returncode == 0:
            # Parse the first line to get version info
            lines = result.stdout.split("\n")
            if lines:
                first_line = lines[0]
                # Extract version from something like "ffmpeg version 4.4.2 Copyright..."
                if "version" in first_line:
                    parts = first_line.split()
                    for i, part in enumerate(parts):
                        if part == "version" and i + 1 < len(parts):
                            return parts[i + 1]
                return first_line.strip()
            return "Unknown version"
        else:
            return "Not found"
    except FileNotFoundError:
        # If ffmpeg is not in PATH, try the installation directory
        try:
            ffmpeg_path = get_ffmpeg_install_path()
            if OS_NAME == "Windows":
                ffmpeg_exe = Path(ffmpeg_path).joinpath("ffmpeg.exe")
            else:
                ffmpeg_exe = Path(ffmpeg_path).joinpath("ffmpeg")

            if ffmpeg_exe.exists():
                result = subprocess.run(
                    [ffmpeg_exe, "-version"], capture_output=True, text=True, timeout=10, creationflags=SUBPROCESS_CREATIONFLAGS
                )

                if result.returncode == 0:
                    lines = result.stdout.split("\n")
                    if lines:
                        first_line = lines[0]
                        if "version" in first_line:
                            parts = first_line.split()
                            for i, part in enumerate(parts):
                                if part == "version" and i + 1 < len(parts):
                                    return parts[i + 1]
                        return first_line.strip()
                    return "Unknown version"
            return "Not found"
        except Exception as e:
            logger.exception(f"Error getting FFmpeg version from install path: {e}")
            return "Not found"
    except Exception as e:
        logger.exception(f"Error getting FFmpeg version: {e}")
        return "Error getting version"


# get_app_data_dir() moved to src\utils\ytsage_constants.py
# get_config_file_path() moved to src\utils\ytsage_constants.py
# ensure_app_data_dir() moved to src\utils\ytsage_constants.py


>>>>>>> 1a2040f (- add: ytsage_constants.py file for one place to store all constants.)
def load_config() -> dict:
    """Load the application configuration from file."""
    default_config = {
        "download_path": str(USER_HOME_DIR / "Downloads"),
        "speed_limit_value": None,
        "speed_limit_unit_index": 0,
        "cookie_file_path": None,
        "last_used_cookie_file": None,
        "auto_update_ytdlp": True,  # Enable auto-update by default
        "auto_update_frequency": "daily",  # daily, weekly, or startup
        "last_update_check": 0,  # timestamp of last check
        "cached_versions": {
            "ytdlp": {"version": None, "path": None, "last_check": 0, "path_mtime": 0},
            "ffmpeg": {"version": None, "path": None, "last_check": 0, "path_mtime": 0},
        },
    }

    try:
        if APP_CONFIG_FILE.exists():
            with open(APP_CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
    except (json.JSONDecodeError, UnicodeError, Exception) as e:
        logger.exception(f"Error reading config file: {e}")
        # If config file is corrupted, create a new one with defaults
        save_config(default_config)

    return default_config


def save_config(config) -> bool:
    """Save the application configuration to file."""
    try:
        with open(APP_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.exception(f"Error saving config: {e}")
        return False


def check_ffmpeg() -> bool:
    """Check if FFmpeg is installed and accessible with enhanced error handling."""
    try:
        # Use the enhanced FFmpeg check from ytsage_ffmpeg
        if check_ffmpeg_installed():
            return True

        # For Windows, try to add the FFmpeg path to environment
        if OS_NAME == "Windows":
            ffmpeg_path = get_ffmpeg_install_path()
            if ffmpeg_path.joinpath("ffmpeg.exe").exists():
                try:
                    # Add to current session PATH
                    os.environ["PATH"] = f"{ffmpeg_path}{os.pathsep}{os.environ.get('PATH', '')}"
                    return True
                except Exception as e:
                    logger.exception(f"Error updating PATH: {e}")
                    return False

        # For macOS, check common paths
        elif OS_NAME == "Darwin":
            common_paths = [
                "/usr/local/bin/ffmpeg",
                "/opt/homebrew/bin/ffmpeg",
                "/usr/bin/ffmpeg",
            ]
            for path in common_paths:
                if Path(path).exists():
                    try:
                        ffmpeg_dir = Path(path).parent
                        os.environ["PATH"] = f"{ffmpeg_dir}{os.pathsep}{os.environ.get('PATH', '')}"
                        return True
                    except Exception as e:
                        logger.exception(f"Error updating PATH: {e}")
                        continue

        return False

    except Exception as e:
        logger.exception(f"Error checking FFmpeg: {e}")
        return False


def load_saved_path(main_window_instance) -> None:
    """Load saved download path with enhanced error handling."""
    try:
        if APP_CONFIG_FILE.exists():
            try:
                with open(APP_CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    saved_path = config.get("download_path", "")
                    if Path(saved_path).exists() and os.access(saved_path, os.W_OK):
                        main_window_instance.last_path = saved_path
                        return
            except (json.JSONDecodeError, UnicodeError) as e:
                logger.exception(f"Error reading config file: {e}")
                # If config file is corrupted, try to remove it
                try:
                    APP_CONFIG_FILE.unlink(missing_ok=True)
                except Exception:
                    pass

        # Fallback to Downloads folder
        downloads_path = USER_HOME_DIR / "Downloads"
        if downloads_path.exists() and os.access(downloads_path, os.W_OK):
            main_window_instance.last_path = downloads_path
        else:
            # Final fallback to temp directory if Downloads is not accessible
            main_window_instance.last_path = tempfile.gettempdir()

    except Exception as e:
        logger.exception(f"Error loading saved settings: {e}")
        main_window_instance.last_path = tempfile.gettempdir()


def save_path(main_window_instance, path) -> bool:
    """Save download path with enhanced error handling."""
    try:
        # Verify the path is valid and writable
        if not Path(path).exists():
            try:
                Path(path).mkdir(exist_ok=True)
            except Exception as e:
                logger.exception(f"Error creating directory: {e}")
                return False

        if not os.access(path, os.W_OK):
            logger.info("Path is not writable")
            return False

        # Save the config
        config = {"download_path": path}
        with open(APP_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False)
        return True

    except Exception as e:
        logger.exception(f"Error saving settings: {e}")
        return False


def update_yt_dlp() -> bool:
    """Check for yt-dlp updates and update if a newer version is available."""
    try:
        # Get the yt-dlp path
        yt_dlp_path = get_yt_dlp_path()

        # Extra logic moved to src\utils\ytsage_constants.py

        # For binaries downloaded with our app, use direct binary update approach
        if yt_dlp_path.samefile(YTDLP_APP_BIN_PATH):
            # We're using a binary installed by our app, update directly
            logger.info(f"Updating yt-dlp binary at {yt_dlp_path}")

            # Determine the URL based on OS
            # Extra logic moved to src\utils\ytsage_constants.py

            # Download the latest version
            try:
                response = requests.get(YTDLP_DOWNLOAD_URL, stream=True)
                if response.status_code == 200:
                    # Create a temporary file
                    temp_file = f"{yt_dlp_path}.new"

                    with open(temp_file, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    # Make executable on Unix systems
                    if OS_NAME != "Windows":
                        os.chmod(temp_file, 0o755)

                    # Replace the old file with the new one
                    try:
                        # On Windows, we need to remove the old file first
                        if OS_NAME == "Windows" and yt_dlp_path.exists():
                            yt_dlp_path.unlink(missing_ok=True)

                        Path(temp_file).rename(yt_dlp_path)
                        logger.info("yt-dlp binary successfully updated")
                        return True
                    except Exception as e:
                        logger.exception(f"Error replacing yt-dlp binary: {e}")
                        return False
                else:
                    logger.info(f"Failed to download latest yt-dlp: HTTP {response.status_code}")
                    return False
            except Exception as e:
                logger.exception(f"Error downloading yt-dlp update: {e}")
                return False
        else:
            # We're using a system-installed yt-dlp, use pip to update
            logger.info("Using pip to update yt-dlp")

            # Get current version
            try:
                current_version = pkg_resources.get_distribution("yt-dlp").version
                logger.info(f"Current yt-dlp version: {current_version}")
            except pkg_resources.DistributionNotFound:
                logger.info("yt-dlp not installed via pip, attempting update anyway")
                current_version = "0.0.0"  # Assume very old version to force update

            # Get the latest version from PyPI JSON API
            try:
                response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    latest_version = data["info"]["version"]
                    logger.info(f"Latest available yt-dlp version: {latest_version}")

                    # Compare versions and update if needed
                    if version.parse(latest_version) > version.parse(current_version):
                        logger.info(f"Updating yt-dlp from {current_version} to {latest_version}...")
                        update_result = subprocess.run(
                            [
                                sys.executable,
                                "-m",
                                "pip",
                                "install",
                                "--upgrade",
                                "yt-dlp",
                            ],
                            capture_output=True,
                            text=True,
                            check=False,
                            creationflags=SUBPROCESS_CREATIONFLAGS,
                        )
                        if update_result.returncode == 0:
                            logger.info("yt-dlp successfully updated")
                            return True
                        else:
                            logger.error(f"Error updating yt-dlp: {update_result.stderr}")
                    else:
                        logger.info("yt-dlp is already up to date")
                        return True
                else:
                    logger.info(f"Failed to get latest version info: HTTP {response.status_code}")
            except Exception as e:
                logger.exception(f"Error checking for yt-dlp updates: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error during yt-dlp update: {e}")

    return False


def should_check_for_auto_update() -> bool:
    """Check if auto-update should be performed based on user settings."""
    try:
        config = load_config()

        # Check if auto-update is enabled
        if not config.get("auto_update_ytdlp", False):
            return False

        frequency = config.get("auto_update_frequency", "daily")
        last_check = config.get("last_update_check", 0)
        current_time = time.time()

        # Calculate time since last check
        time_diff = current_time - last_check

        if frequency == "startup":
            # Always check on startup if we haven't checked in the last hour
            return time_diff > 3600  # 1 hour
        elif frequency == "daily":
            return time_diff > 86400  # 24 hours
        elif frequency == "weekly":
            return time_diff > 604800  # 7 days

        return False
    except Exception as e:
        logger.exception(f"Error checking auto-update schedule: {e}")
        return False


def check_and_update_ytdlp_auto() -> bool:
    """Perform automatic yt-dlp update check and update if needed."""
    try:
        logger.info("Performing automatic yt-dlp update check...")

        # Get current version
        current_version = get_ytdlp_version()
        if "Error" in current_version:
            logger.info("Could not determine current yt-dlp version, skipping auto-update")
            return False

        # Get latest version from PyPI
        try:
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
            response.raise_for_status()
            latest_version = response.json()["info"]["version"]

            # Clean up version strings
            current_version = current_version.replace("_", ".")
            latest_version = latest_version.replace("_", ".")

            logger.info(f"Current yt-dlp version: {current_version}")
            logger.info(f"Latest yt-dlp version: {latest_version}")

            # Compare versions
            from packaging import version as version_parser

            if version_parser.parse(latest_version) > version_parser.parse(current_version):
                logger.info(f"Auto-updating yt-dlp from {current_version} to {latest_version}...")

                # Perform the update
                if update_yt_dlp():
                    logger.info("Auto-update completed successfully!")
                    # Update the last check timestamp
                    config = load_config()
                    config["last_update_check"] = time.time()
                    save_config(config)
                    return True
                else:
                    logger.info("Auto-update failed")
                    return False
            else:
                logger.info("yt-dlp is already up to date")
                # Still update the timestamp even if no update was needed
                config = load_config()
                config["last_update_check"] = time.time()
                save_config(config)
                return True

        except requests.RequestException as e:
            logger.info(f"Network error during auto-update check: {e}")
            return False
        except Exception as e:
            logger.exception(f"Error during auto-update check: {e}")
            return False

    except Exception as e:
        logger.critical(f"Critical error in auto-update: {e}", exc_info=True)
        return False


def get_auto_update_settings() -> dict:
    """Get current auto-update settings from config."""
    config = load_config()
    return {
        "enabled": config.get("auto_update_ytdlp", True),
        "frequency": config.get("auto_update_frequency", "daily"),
        "last_check": config.get("last_update_check", 0),
    }


def update_auto_update_settings(enabled, frequency) -> bool:
    """Update auto-update settings in config."""
    try:
        config = load_config()
        config["auto_update_ytdlp"] = enabled
        config["auto_update_frequency"] = frequency
        save_config(config)
        return True
    except Exception as e:
        logger.exception(f"Error updating auto-update settings: {e}")
        return False


def parse_yt_dlp_error(error_message: str) -> str:
    """
    Parse yt-dlp error messages and return user-friendly error messages.
    
    Args:
        error_message: The raw error message from yt-dlp
        
    Returns:
        str: A user-friendly error message with actionable advice
    """
    error_str = str(error_message).lower()
    
    # Private video errors
    if any(keyword in error_str for keyword in ['private video', 'login_required', 'sign in if you']):
        return ("This is a private video. You can download it by logging into your account using cookies.\n"
                "Go to 'Custom Options' → 'Login with Cookies' → 'Extract cookies from browser' to authenticate.")
    
    # Age-restricted content
    if any(keyword in error_str for keyword in ['age restricted', 'age-restricted', 'confirm your age']):
        return ("This video is age-restricted. You need to be logged in to access it.\n"
                "Use 'Custom Options' → 'Login with Cookies' to authenticate with your account.")
    
    # Geo-blocked content
    if any(keyword in error_str for keyword in ['not available in your country', 'geo-blocked', 'video is not available', 'not made this video available in your country']):
        return ("This video is not available in your region (geo-blocked).\n"
                "You may need to use a VPN or the video might be restricted in your country.")
    
    # Removed/deleted videos
    if any(keyword in error_str for keyword in ['video unavailable', 'this video has been removed', 'video does not exist']):
        return ("This video has been removed or is no longer available.\n"
                "The video may have been deleted by the uploader or removed due to policy violations.")
    
    # Live stream errors
    if any(keyword in error_str for keyword in ['live stream', 'livestream', 'is live']):
        return ("This is a live stream that cannot be downloaded while active.\n"
                "Wait for the stream to end, then try downloading the archived version.")
    
    # Playlist errors
    if any(keyword in error_str for keyword in ['playlist', 'no entries']):
        return ("Unable to access this playlist. It may be private, deleted, or empty.\n"
                "Check if the playlist exists and is publicly accessible.")
    
    # Network/connection errors
    if any(keyword in error_str for keyword in ['network error', 'connection', 'timeout', 'unable to download']):
        return ("Network connection error. Please check your internet connection and try again.\n"
                "If the problem persists, the video server might be temporarily unavailable.")
    
    # Invalid URL
    if any(keyword in error_str for keyword in ['invalid url', 'unsupported url', 'no video found']):
        return ("Invalid or unsupported URL. Please check the link and try again.\n"
                "Make sure you're using a valid YouTube, Vimeo, or other supported platform URL.")
    
    # YouTube premium content
    if any(keyword in error_str for keyword in ['youtube premium', 'premium', 'members only']):
        return ("This content requires YouTube Premium or channel membership.\n"
                "You need to be logged in with an account that has access to this content.")
    
    # Copyright/DMCA
    if any(keyword in error_str for keyword in ['copyright', 'dmca', 'blocked']):
        return ("This video is blocked due to copyright claims.\n"
                "The content owner has restricted access to this video.")
    
    # Extraction errors (could be temporary)
    if any(keyword in error_str for keyword in ['unable to extract', 'extraction failed']):
        return ("Failed to extract video information. This might be a temporary issue.\n"
                "Please try again in a few minutes, or check if the video link is correct.")
    
    # Generic fallback with the original error for debugging
    return (f"Could not extract video information. Please check your link.\n"
            f"Technical details: {error_message}")
