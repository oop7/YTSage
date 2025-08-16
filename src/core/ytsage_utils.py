import sys
import os
import json
import time
from pathlib import Path
import subprocess
import tempfile
import shutil
import pkg_resources
from packaging import version
import requests
from .ytsage_logging import logger
from .ytsage_ffmpeg import check_ffmpeg_installed, get_ffmpeg_install_path, get_ffmpeg_path
from .ytsage_yt_dlp import get_yt_dlp_path  # Import the new function to avoid import errors

# Cache for version information to avoid delays
_version_cache = {
    'ytdlp': {'version': None, 'path': None, 'last_check': 0, 'path_mtime': 0},
    'ffmpeg': {'version': None, 'path': None, 'last_check': 0, 'path_mtime': 0}
}

# Cache expiry time in seconds (5 minutes)
CACHE_EXPIRY = 300

def get_file_mtime(filepath):
    """Get file modification time safely."""
    try:
        if filepath and os.path.exists(filepath):
            return os.path.getmtime(filepath)
    except Exception:
        pass
    return 0

def should_refresh_cache(tool_name, current_path):
    """Determine if cache should be refreshed for a tool."""
    cache = _version_cache.get(tool_name, {})
    current_time = time.time()
    
    # Always refresh if no cached data
    if not cache.get('version'):
        return True
    
    # Refresh if path changed
    if cache.get('path') != current_path:
        return True
    
    # Refresh if file was modified
    current_mtime = get_file_mtime(current_path)
    if current_mtime > cache.get('path_mtime', 0):
        return True
    
    # Refresh if cache expired
    if current_time - cache.get('last_check', 0) > CACHE_EXPIRY:
        return True
    
    return False

def update_version_cache(tool_name, version_info, path, force_save=False):
    """Update the version cache and optionally save to config."""
    current_time = time.time()
    current_mtime = get_file_mtime(path)
    
    _version_cache[tool_name] = {
        'version': version_info,
        'path': path,
        'last_check': current_time,
        'path_mtime': current_mtime
    }
    
    # Save to persistent config
    if force_save:
        save_version_cache_to_config()

def load_version_cache_from_config():
    """Load cached version info from config file."""
    try:
        config = load_config()
        cached_versions = config.get('cached_versions', {})
        
        for tool_name, cache_data in cached_versions.items():
            if tool_name in _version_cache:
                _version_cache[tool_name].update(cache_data)
    except Exception as e:
        logger.error(f"Error loading version cache: {e}")

def save_version_cache_to_config():
    """Save version cache to config file."""
    try:
        config = load_config()
        config['cached_versions'] = _version_cache.copy()
        save_config(config)
    except Exception as e:
        logger.error(f"Error saving version cache: {e}")

def get_ytdlp_version_cached():
    """Get yt-dlp version with caching support."""
    try:
        current_path = get_yt_dlp_path()
        
        # Check if we need to refresh cache
        if not should_refresh_cache('ytdlp', current_path):
            cached_version = _version_cache['ytdlp'].get('version')
            if cached_version:
                return cached_version
        
        # Get fresh version info
        version_info = get_ytdlp_version_direct(current_path)
        
        # Update cache
        update_version_cache('ytdlp', version_info, current_path)
        
        return version_info
    except Exception as e:
        logger.error(f"Error getting cached yt-dlp version: {e}")
        return "Error getting version"

def get_ffmpeg_version_cached():
    """Get FFmpeg version with caching support."""
    try:
        # Try to find ffmpeg path
        current_path = "ffmpeg"  # Default to system PATH
        
        # Check if we need to refresh cache
        if not should_refresh_cache('ffmpeg', current_path):
            cached_version = _version_cache['ffmpeg'].get('version')
            if cached_version:
                return cached_version
        
        # Get fresh version info
        version_info = get_ffmpeg_version_direct()
        
        # Update cache
        update_version_cache('ffmpeg', version_info, current_path)
        
        return version_info
    except Exception as e:
        logger.error(f"Error getting cached FFmpeg version: {e}")
        return "Error getting version"

def refresh_version_cache(force=False):
    """Manually refresh version cache for both tools."""
    try:
        # Refresh yt-dlp
        current_path = get_yt_dlp_path()
        version_info = get_ytdlp_version_direct(current_path)
        update_version_cache('ytdlp', version_info, current_path, force_save=True)
        
        # Refresh FFmpeg
        version_info = get_ffmpeg_version_direct()
        update_version_cache('ffmpeg', version_info, "ffmpeg", force_save=True)
        
        return True
    except Exception as e:
        logger.error(f"Error refreshing version cache: {e}")
        return False

def get_ytdlp_version():
    """Get the version of yt-dlp (uses cached version for performance)."""
    return get_ytdlp_version_cached()

def get_ffmpeg_version():
    """Get the version of FFmpeg (uses cached version for performance)."""
    return get_ffmpeg_version_cached()

def get_ytdlp_version_direct(yt_dlp_path=None):
    """Get yt-dlp version directly without caching."""
    try:
        if yt_dlp_path is None:
            yt_dlp_path = get_yt_dlp_path()
        
        if not yt_dlp_path or yt_dlp_path == "yt-dlp":
            return "Not found"
        
        # Create startupinfo to hide console on Windows
        startupinfo = None
        if sys.platform == 'win32' and hasattr(subprocess, 'STARTUPINFO'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
        
        result = subprocess.run(
            [yt_dlp_path, '--version'],
            capture_output=True,
            text=True,
            timeout=10,
            startupinfo=startupinfo
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "Error getting version"
    except Exception as e:
        logger.error(f"Error getting yt-dlp version: {e}")
        return "Error getting version"

def get_ffmpeg_version_direct():
    """Get FFmpeg version directly without caching."""
    try:
        # Create startupinfo to hide console on Windows
        startupinfo = None
        if sys.platform == 'win32' and hasattr(subprocess, 'STARTUPINFO'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
        
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=10,
            startupinfo=startupinfo
        )
        
        if result.returncode == 0:
            # Parse the first line to get version info
            lines = result.stdout.split('\n')
            if lines:
                first_line = lines[0]
                # Extract version from something like "ffmpeg version 4.4.2 Copyright..."
                if 'version' in first_line:
                    parts = first_line.split()
                    for i, part in enumerate(parts):
                        if part == 'version' and i + 1 < len(parts):
                            return parts[i + 1]
                return first_line.strip()
            return "Unknown version"
        else:
            return "Not found"
    except FileNotFoundError:
        # If ffmpeg is not in PATH, try the installation directory
        try:
            ffmpeg_path = get_ffmpeg_install_path()
            if sys.platform == 'win32':
                ffmpeg_exe = os.path.join(ffmpeg_path, 'ffmpeg.exe')
            else:
                ffmpeg_exe = os.path.join(ffmpeg_path, 'ffmpeg')
            
            if os.path.exists(ffmpeg_exe):
                result = subprocess.run(
                    [ffmpeg_exe, '-version'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    startupinfo=startupinfo
                )
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    if lines:
                        first_line = lines[0]
                        if 'version' in first_line:
                            parts = first_line.split()
                            for i, part in enumerate(parts):
                                if part == 'version' and i + 1 < len(parts):
                                    return parts[i + 1]
                        return first_line.strip()
                    return "Unknown version"
            return "Not found"
        except Exception as e:
            logger.error(f"Error getting FFmpeg version from install path: {e}")
            return "Not found"
    except Exception as e:
        logger.error(f"Error getting FFmpeg version: {e}")
        return "Error getting version"

def get_app_data_dir():
    """Get the OS-specific application data directory."""
    if sys.platform == 'win32':
        # Windows: %LOCALAPPDATA%\YTSage\data\
        return Path(os.environ.get('LOCALAPPDATA', '')) / 'YTSage' / 'data'
    elif sys.platform == 'darwin':
        # macOS: ~/Library/Application Support/YTSage/data/
        return Path.home() / 'Library' / 'Application Support' / 'YTSage' / 'data'
    else:
        # Linux: ~/.local/share/YTSage/data/
        return Path.home() / '.local' / 'share' / 'YTSage' / 'data'

def get_config_file_path():
    """Get the path to the main configuration file."""
    return get_app_data_dir() / 'ytsage_config.json'

def ensure_app_data_dir():
    """Ensure the application data directory exists."""
    data_dir = get_app_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def load_config():
    """Load the application configuration from file."""
    config_file = get_config_file_path()
    default_config = {
        'download_path': str(Path.home() / 'Downloads'),
        'speed_limit_value': None,
        'speed_limit_unit_index': 0,
        'cookie_file_path': None,
        'last_used_cookie_file': None,
        'auto_update_ytdlp': True,  # Enable auto-update by default
        'auto_update_frequency': 'daily',  # daily, weekly, or startup
        'last_update_check': 0,  # timestamp of last check
        'cached_versions': {
            'ytdlp': {'version': None, 'path': None, 'last_check': 0, 'path_mtime': 0},
            'ffmpeg': {'version': None, 'path': None, 'last_check': 0, 'path_mtime': 0}
        }
    }
    
    try:
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
    except (json.JSONDecodeError, UnicodeError, Exception) as e:
        logger.error(f"Error reading config file: {e}")
        # If config file is corrupted, create a new one with defaults
        save_config(default_config)
    
    return default_config

def save_config(config):
    """Save the application configuration to file."""
    config_file = get_config_file_path()
    try:
        # Ensure the config directory exists
        ensure_app_data_dir()
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible with enhanced error handling."""
    try:
        # Use the enhanced FFmpeg check from ytsage_ffmpeg
        if check_ffmpeg_installed():
            return True
            
        # For Windows, try to add the FFmpeg path to environment
        if sys.platform == 'win32':
            ffmpeg_path = get_ffmpeg_install_path()
            if os.path.exists(os.path.join(ffmpeg_path, 'ffmpeg.exe')):
                try:
                    # Add to current session PATH
                    os.environ['PATH'] = f"{ffmpeg_path}{os.pathsep}{os.environ.get('PATH', '')}"
                    return True
                except Exception as e:
                    logger.error(f"Error updating PATH: {e}")
                    return False
                
        # For macOS, check common paths
        elif sys.platform == 'darwin':
            common_paths = [
                '/usr/local/bin/ffmpeg',
                '/opt/homebrew/bin/ffmpeg',
                '/usr/bin/ffmpeg'
            ]
            for path in common_paths:
                if os.path.exists(path):
                    try:
                        ffmpeg_dir = os.path.dirname(path)
                        os.environ['PATH'] = f"{ffmpeg_dir}{os.pathsep}{os.environ.get('PATH', '')}"
                        return True
                    except Exception as e:
                        logger.error(f"Error updating PATH: {e}")
                        continue
                    
        return False
        
    except Exception as e:
        logger.error(f"Error checking FFmpeg: {e}")
        return False

def load_saved_path(main_window_instance):
    """Load saved download path with enhanced error handling."""
    config_file = get_config_file_path()
    try:
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    saved_path = config.get('download_path', '')
                    if os.path.exists(saved_path) and os.access(saved_path, os.W_OK):
                        main_window_instance.last_path = saved_path
                        return
            except (json.JSONDecodeError, UnicodeError) as e:
                logger.error(f"Error reading config file: {e}")
                # If config file is corrupted, try to remove it
                try:
                    os.remove(config_file)
                except Exception:
                    pass
                
        # Fallback to Downloads folder
        downloads_path = str(Path.home() / 'Downloads')
        if os.path.exists(downloads_path) and os.access(downloads_path, os.W_OK):
            main_window_instance.last_path = downloads_path
        else:
            # Final fallback to temp directory if Downloads is not accessible
            main_window_instance.last_path = tempfile.gettempdir()
            
    except Exception as e:
        logger.error(f"Error loading saved settings: {e}")
        main_window_instance.last_path = tempfile.gettempdir()

def save_path(main_window_instance, path):
    """Save download path with enhanced error handling."""
    config_file = get_config_file_path()
    try:
        # Verify the path is valid and writable
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                logger.error(f"Error creating directory: {e}")
                return False
                
        if not os.access(path, os.W_OK):
            logger.info("Path is not writable")
            return False
            
        # Ensure the config directory exists
        ensure_app_data_dir()
            
        # Save the config
        config = {'download_path': path}
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False)
        return True
        
    except Exception as e:
        logger.error(f"Error saving settings: {e}")
        return False

def update_yt_dlp():
    """Check for yt-dlp updates and update if a newer version is available."""
    try:
        # Get the yt-dlp path
        yt_dlp_path = get_yt_dlp_path()
        
        # Create startupinfo to hide console on Windows
        startupinfo = None
        if sys.platform == 'win32' and hasattr(subprocess, 'STARTUPINFO'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
            
        # For binaries downloaded with our app, use direct binary update approach
        if os.path.dirname(yt_dlp_path) in [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'YTSage', 'bin'),
            os.path.expanduser(os.path.join('~', 'Library', 'Application Support', 'YTSage', 'bin')),
            os.path.expanduser(os.path.join('~', '.local', 'share', 'YTSage', 'bin'))
        ]:
            # We're using a binary installed by our app, update directly
            logger.info(f"Updating yt-dlp binary at {yt_dlp_path}")
            
            # Determine the URL based on OS
            if sys.platform == 'win32':
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
            elif sys.platform == 'darwin':
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
            else:
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
                
            # Download the latest version
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    # Create a temporary file
                    temp_file = f"{yt_dlp_path}.new"
                    
                    with open(temp_file, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    # Make executable on Unix systems
                    if sys.platform != 'win32':
                        os.chmod(temp_file, 0o755)
                    
                    # Replace the old file with the new one
                    try:
                        # On Windows, we need to remove the old file first
                        if sys.platform == 'win32' and os.path.exists(yt_dlp_path):
                            os.remove(yt_dlp_path)
                        
                        os.rename(temp_file, yt_dlp_path)
                        logger.info("yt-dlp binary successfully updated")
                        return True
                    except Exception as e:
                        logger.error(f"Error replacing yt-dlp binary: {e}")
                        return False
                else:
                    logger.info(f"Failed to download latest yt-dlp: HTTP {response.status_code}")
                    return False
            except Exception as e:
                logger.error(f"Error downloading yt-dlp update: {e}")
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
                            [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                            capture_output=True,
                            text=True,
                            check=False,
                            startupinfo=startupinfo
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
                logger.error(f"Error checking for yt-dlp updates: {e}")
    except Exception as e:
        logger.info(f"Unexpected error during yt-dlp update: {e}")
    
    return False


def should_check_for_auto_update():
    """Check if auto-update should be performed based on user settings."""
    try:
        config = load_config()
        
        # Check if auto-update is enabled
        if not config.get('auto_update_ytdlp', False):
            return False
        
        frequency = config.get('auto_update_frequency', 'daily')
        last_check = config.get('last_update_check', 0)
        current_time = time.time()
        
        # Calculate time since last check
        time_diff = current_time - last_check
        
        if frequency == 'startup':
            # Always check on startup if we haven't checked in the last hour
            return time_diff > 3600  # 1 hour
        elif frequency == 'daily':
            return time_diff > 86400  # 24 hours
        elif frequency == 'weekly':
            return time_diff > 604800  # 7 days
        
        return False
    except Exception as e:
        logger.error(f"Error checking auto-update schedule: {e}")
        return False


def check_and_update_ytdlp_auto():
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
            current_version = current_version.replace('_', '.')
            latest_version = latest_version.replace('_', '.')
            
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
                    config['last_update_check'] = time.time()
                    save_config(config)
                    return True
                else:
                    logger.info("Auto-update failed")
                    return False
            else:
                logger.info("yt-dlp is already up to date")
                # Still update the timestamp even if no update was needed
                config = load_config()
                config['last_update_check'] = time.time()
                save_config(config)
                return True
                
        except requests.RequestException as e:
            logger.info(f"Network error during auto-update check: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during auto-update check: {e}")
            return False
            
    except Exception as e:
        logger.info(f"Critical error in auto-update: {e}")
        return False


def get_auto_update_settings():
    """Get current auto-update settings from config."""
    config = load_config()
    return {
        'enabled': config.get('auto_update_ytdlp', True),
        'frequency': config.get('auto_update_frequency', 'daily'),
        'last_check': config.get('last_update_check', 0)
    }


def update_auto_update_settings(enabled, frequency):
    """Update auto-update settings in config."""
    try:
        config = load_config()
        config['auto_update_ytdlp'] = enabled
        config['auto_update_frequency'] = frequency
        save_config(config)
        return True
    except Exception as e:
        logger.error(f"Error updating auto-update settings: {e}")
        return False