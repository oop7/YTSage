import json
import os
import subprocess
import sys
import tempfile
import time
from importlib.metadata import PackageNotFoundError
from pathlib import Path
from typing import Any, Dict, Optional, Union

import requests
from packaging import version

from src.core.ytsage_ffmpeg import check_ffmpeg_installed, get_ffmpeg_install_path
from src.core.ytsage_yt_dlp import get_yt_dlp_path
from src.utils.ytsage_constants import (
    APP_CONFIG_FILE,
    OS_NAME,
    SUBPROCESS_CREATIONFLAGS,
    USER_HOME_DIR,
    YTDLP_APP_BIN_PATH,
    YTDLP_DOWNLOAD_URL,
)
from src.utils.ytsage_localization import _
from src.utils.ytsage_logger import logger

try:
    from importlib.metadata import PackageNotFoundError as ImportlibPackageNotFoundError
    from importlib.metadata import version as importlib_version

    def get_version(package_name: str) -> str:
        return importlib_version(package_name)

    PackageNotFoundError = ImportlibPackageNotFoundError
except ImportError:
    # Fallback for older Python versions
    import pkg_resources

    def get_version(package_name: str) -> str:
        return pkg_resources.get_distribution(package_name).version

    PackageNotFoundError = pkg_resources.DistributionNotFound


# Cache for version information to avoid delays
_version_cache: Dict[str, Dict[str, Any]] = {
    "ytdlp": {"version": None, "path": None, "last_check": 0, "path_mtime": 0},
    "ffmpeg": {"version": None, "path": None, "last_check": 0, "path_mtime": 0},
    "deno": {"version": None, "path": None, "last_check": 0, "path_mtime": 0},
}

# Cache expiry time in seconds (5 minutes)
CACHE_EXPIRY: int = 300


def get_file_mtime(filepath: Optional[Union[str, Path]]) -> float:
    """Get file modification time safely."""
    try:
        if filepath and Path(filepath).exists():
            return Path(filepath).stat().st_mtime
    except Exception:
        pass
    return 0.0


def should_refresh_cache(tool_name: str, current_path: Optional[str]) -> bool:
    """Determine if cache should be refreshed for a tool."""
    cache: Dict[str, Any] = _version_cache.get(tool_name, {})
    current_time: float = time.time()

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


def update_version_cache(tool_name: str, version_info: str, path: Optional[str], force_save: bool = False) -> None:
    """Update the version cache and optionally save to config."""
    current_time: float = time.time()
    current_mtime: float = get_file_mtime(path)

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


def get_deno_version_cached() -> str:
    """Get Deno version with caching support."""
    try:
        from src.core.ytsage_deno import get_deno_path
        
        current_path = get_deno_path()

        # Check if we need to refresh cache
        if not should_refresh_cache("deno", current_path):
            cached_version = _version_cache["deno"].get("version")
            if cached_version:
                return cached_version

        # Get fresh version info
        from src.core.ytsage_deno import get_deno_version_direct
        version_info = get_deno_version_direct(current_path)

        # Update cache
        update_version_cache("deno", version_info, current_path)

        return version_info
    except Exception as e:
        logger.exception(f"Error getting cached Deno version: {e}")
        return "Error getting version"


def refresh_version_cache(force=False) -> bool:
    """Manually refresh version cache for all tools."""
    try:
        # Refresh yt-dlp
        current_path = get_yt_dlp_path()
        version_info = get_ytdlp_version_direct(current_path)
        update_version_cache("ytdlp", version_info, current_path, force_save=True)

        # Refresh FFmpeg
        version_info = get_ffmpeg_version_direct()
        update_version_cache("ffmpeg", version_info, "ffmpeg", force_save=True)

        # Refresh Deno
        from src.core.ytsage_deno import get_deno_path, get_deno_version_direct
        deno_path = get_deno_path()
        version_info = get_deno_version_direct(deno_path)
        update_version_cache("deno", version_info, deno_path, force_save=True)

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


def get_deno_version() -> str:
    """Get the version of Deno (uses cached version for performance)."""
    return get_deno_version_cached()


def get_ytdlp_version_direct(yt_dlp_path: Optional[str] = None) -> str:
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


def load_config() -> Dict[str, Any]:
    """Load the application configuration from file."""
    default_config: Dict[str, Any] = {
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


def save_config(config: Dict[str, Any]) -> bool:
    """Save the application configuration to file."""
    try:
        # Convert any Path objects to strings for JSON serialization
        def _convert_path(obj):
            if isinstance(obj, Path):
                return str(obj)
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

        with open(APP_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2, default=_convert_path)
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


def load_saved_path(main_window_instance: Any) -> None:
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


def save_path(main_window_instance: Any, path: Union[str, Path]) -> bool:
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
        yt_dlp_path: Path = get_yt_dlp_path()

        # Extra logic moved to src\utils\ytsage_constants.py

        # For binaries downloaded with our app, use direct binary update approach
        # Check if this is an app-managed binary by comparing paths safely
        is_app_managed: bool = False
        try:
            # Only compare if both files exist
            if yt_dlp_path.exists() and YTDLP_APP_BIN_PATH.exists():
                is_app_managed = yt_dlp_path.samefile(YTDLP_APP_BIN_PATH)
            elif str(yt_dlp_path) == str(YTDLP_APP_BIN_PATH):
                # If paths are identical as strings, consider it app-managed
                is_app_managed = True
            else:
                # If app binary doesn't exist, this is definitely not app-managed
                is_app_managed = False
        except (OSError, IOError) as e:
            logger.debug(f"Error comparing paths in update_yt_dlp: {e}")
            is_app_managed = False

        if is_app_managed:
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
                current_version = get_version("yt-dlp")
                logger.info(f"Current yt-dlp version: {current_version}")
            except PackageNotFoundError:
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

        frequency: str = config.get("auto_update_frequency", "daily")
        last_check: float = config.get("last_update_check", 0)
        current_time: float = time.time()

        # Calculate time since last check
        time_diff: float = current_time - last_check

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
            if version.parse(latest_version) > version.parse(current_version):
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


def get_auto_update_settings() -> Dict[str, Any]:
    """Get current auto-update settings from config."""
    from src.utils.ytsage_config_manager import ConfigManager
    
    enabled: Optional[bool] = ConfigManager.get("auto_update_ytdlp")
    frequency: Optional[str] = ConfigManager.get("auto_update_frequency")
    last_check: Optional[float] = ConfigManager.get("last_update_check")
    
    return {
        "enabled": enabled if enabled is not None else True,
        "frequency": frequency if frequency is not None else "daily",
        "last_check": last_check if last_check is not None else 0,
    }


def update_auto_update_settings(enabled: bool, frequency: str) -> bool:
    """Update auto-update settings in config."""
    try:
        from src.utils.ytsage_config_manager import ConfigManager
        
        ConfigManager.set("auto_update_ytdlp", enabled)
        ConfigManager.set("auto_update_frequency", frequency)
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
    error_str = error_message.lower()

    # Private video errors
    if any(keyword in error_str for keyword in ["private video", "login_required", "sign in if you"]):
        return _("ytdlp_errors.private_video")

    # Age-restricted content
    if any(keyword in error_str for keyword in ["age restricted", "age-restricted", "confirm your age"]):
        return _("ytdlp_errors.age_restricted")

    # Geo-blocked content
    if any(
        keyword in error_str
        for keyword in [
            "not available in your country",
            "geo-blocked",
            "video is not available",
            "not made this video available in your country",
        ]
    ):
        return _("ytdlp_errors.geo_blocked")

    # Removed/deleted videos
    if any(keyword in error_str for keyword in ["video unavailable", "this video has been removed", "video does not exist"]):
        return _("ytdlp_errors.video_unavailable")

    # Live stream errors
    if any(keyword in error_str for keyword in ["live stream", "livestream", "is live"]):
        return _("ytdlp_errors.live_stream")

    # Playlist errors
    if any(keyword in error_str for keyword in ["playlist", "no entries"]):
        return _("ytdlp_errors.playlist_error")

    # Network/connection errors
    if any(keyword in error_str for keyword in ["network error", "connection", "timeout", "unable to download"]):
        return _("ytdlp_errors.network_error")

    # Invalid URL
    if any(keyword in error_str for keyword in ["invalid url", "unsupported url", "no video found"]):
        return _("ytdlp_errors.invalid_url")

    # YouTube premium content
    if any(keyword in error_str for keyword in ["youtube premium", "premium", "members only"]):
        return _("ytdlp_errors.premium_content")

    # Copyright/DMCA
    if any(keyword in error_str for keyword in ["copyright", "dmca", "blocked"]):
        return _("ytdlp_errors.copyright_blocked")

    # Extraction errors (could be temporary)
    if any(keyword in error_str for keyword in ["unable to extract", "extraction failed"]):
        return _("ytdlp_errors.extraction_failed")

    # Generic fallback with the original error for debugging
    return _("ytdlp_errors.generic_error", error=error_message)


def validate_video_url(url: str) -> tuple[bool, str]:
    """
    Validate a video URL for supported platforms.
    
    Args:
        url: The URL string to validate
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
        - is_valid: True if URL is valid, False otherwise
        - error_message: Empty string if valid, error description if invalid
        
    Example:
        >>> is_valid, error = validate_video_url("https://youtube.com/watch?v=xxx")
        >>> if not is_valid:
        ...     print(error)
    """
    from urllib.parse import urlparse
    
    # Check if URL is empty
    if not url or not url.strip():
        return False, _("url_validation.empty_url")
    
    url = url.strip()
    
    # Check basic URL structure
    try:
        parsed = urlparse(url)
    except Exception as e:
        logger.debug(f"URL parsing error: {e}")
        return False, _("url_validation.invalid_format")
    
    # Check if scheme is http or https
    if parsed.scheme not in ['http', 'https']:
        return False, _("url_validation.invalid_scheme")
    
    # Check if netloc (domain) exists
    if not parsed.netloc:
        return False, _("url_validation.missing_domain")
    
    # YTSage focuses on YouTube and YouTube Music only
    # Supported YouTube domains
    youtube_domains = [
        'youtube.com',
        'www.youtube.com',
        'youtu.be',
        'm.youtube.com',
        'music.youtube.com',  # YouTube Music
        'gaming.youtube.com',  # YouTube Gaming (redirects to main)
    ]
    
    # Check if domain is YouTube
    netloc_lower = parsed.netloc.lower()
    is_youtube = any(
        netloc_lower == domain or netloc_lower.endswith('.' + domain)
        for domain in youtube_domains
    )
    
    if not is_youtube:
        return False, _("url_validation.unsupported_platform", domain=parsed.netloc)
    
    # Optional: Validate YouTube URL patterns
    # Common YouTube URL patterns:
    # - /watch?v=VIDEO_ID
    # - /playlist?list=PLAYLIST_ID
    # - /shorts/VIDEO_ID
    # - youtu.be/VIDEO_ID
    valid_patterns = [
        '/watch',
        '/playlist',
        '/shorts/',
        '/live/',
        '/channel/',
        '/c/',
        '/user/',
        '@',  # New handle format
    ]
    
    # For youtu.be, the path itself is the video ID
    if 'youtu.be' in netloc_lower:
        if not parsed.path or parsed.path == '/':
            return False, _("url_validation.invalid_youtu_be")
        return True, ""
    
    # For youtube.com domains, check for valid patterns
    if any(pattern in url.lower() for pattern in valid_patterns):
        return True, ""
    
    # If it's a YouTube domain but doesn't match known patterns, still allow it
    # (yt-dlp might support formats we don't know about)
    logger.info(f"YouTube URL doesn't match known patterns but allowing: {url}")
    return True, ""

