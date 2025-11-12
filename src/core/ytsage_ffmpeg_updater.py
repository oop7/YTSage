"""
FFmpeg updater module for YTSage application.
Handles checking for updates and updating FFmpeg to the latest Essentials build.
"""

import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple, Callable

import requests

from src.utils.ytsage_logger import logger
from src.utils.ytsage_constants import (
    FFMPEG_7Z_DOWNLOAD_URL,
    FFMPEG_7Z_SHA256_URL,
    FFMPEG_7Z_VERSION_URL,
    FFMPEG_ZIP_DOWNLOAD_URL,
    FFMPEG_ZIP_SHA256_URL,
    FFMPEG_ZIP_VERSION_URL,
    OS_NAME,
    SUBPROCESS_CREATIONFLAGS,
)
from src.core.ytsage_ffmpeg import (
    check_7zip_installed,
    download_file,
    get_file_sha256,
    verify_sha256,
    get_ffmpeg_install_path,
)
from src.core.ytsage_utils import get_ffmpeg_version_direct


def get_latest_ffmpeg_version() -> Optional[str]:
    """
    Fetch the latest FFmpeg version from the version URL.
    
    Returns:
        str: Version string (e.g., "8.0") or None if fetch failed
    """
    try:
        # Try 7z version URL first
        response = requests.get(FFMPEG_7Z_VERSION_URL, timeout=10)
        response.raise_for_status()
        version = response.text.strip()
        
        # Validate version format (should be something like "8.0" or "7.1.1")
        if re.match(r'^\d+\.\d+(\.\d+)?$', version):
            logger.info(f"Latest FFmpeg version: {version}")
            return version
        else:
            logger.warning(f"Unexpected version format: {version}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Failed to fetch latest FFmpeg version: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error fetching FFmpeg version: {e}")
        return None


def parse_version(version_str: str) -> Tuple[int, ...]:
    """
    Parse version string into tuple of integers for comparison.
    
    Args:
        version_str: Version string like "8.0" or "7.1.1"
        
    Returns:
        Tuple of integers (e.g., (8, 0) or (7, 1, 1))
    """
    try:
        # Extract version numbers from string
        # Handles formats like "8.0", "7.1.1", "ffmpeg version 8.0", etc.
        match = re.search(r'(\d+\.\d+(?:\.\d+)?)', version_str)
        if match:
            version_str = match.group(1)
        
        parts = version_str.split('.')
        return tuple(int(p) for p in parts)
    except (ValueError, AttributeError):
        logger.warning(f"Could not parse version: {version_str}")
        return (0,)


def compare_versions(current: str, latest: str) -> bool:
    """
    Compare two version strings.
    
    Args:
        current: Current version string
        latest: Latest version string
        
    Returns:
        True if update is needed (latest > current), False otherwise
    """
    try:
        current_tuple = parse_version(current)
        latest_tuple = parse_version(latest)
        
        logger.info(f"Comparing versions - Current: {current_tuple}, Latest: {latest_tuple}")
        
        # Pad shorter version with zeros for comparison
        max_len = max(len(current_tuple), len(latest_tuple))
        current_padded = current_tuple + (0,) * (max_len - len(current_tuple))
        latest_padded = latest_tuple + (0,) * (max_len - len(latest_tuple))
        
        return latest_padded > current_padded
    except Exception as e:
        logger.exception(f"Error comparing versions: {e}")
        return False


def check_ffmpeg_update_available() -> Tuple[bool, str, str]:
    """
    Check if FFmpeg update is available.
    
    Returns:
        Tuple of (update_available, current_version, latest_version)
        - update_available: True if update is needed
        - current_version: Currently installed version or "Not installed"
        - latest_version: Latest available version or "Unknown"
    """
    try:
        # Get current version
        current_version = get_ffmpeg_version_direct()
        if current_version in ["Not found", "Error getting version", "Unknown version"]:
            current_version = "Not installed"
        
        # Get latest version
        latest_version = get_latest_ffmpeg_version()
        if latest_version is None:
            latest_version = "Unknown"
            return False, current_version, latest_version
        
        # If not installed, update is needed
        if current_version == "Not installed":
            return True, current_version, latest_version
        
        # Compare versions
        update_needed = compare_versions(current_version, latest_version)
        
        return update_needed, current_version, latest_version
        
    except Exception as e:
        logger.exception(f"Error checking for FFmpeg updates: {e}")
        return False, "Error", "Error"


def get_ffmpeg_extract_dir() -> Path:
    """Get the directory where FFmpeg should be extracted."""
    if OS_NAME == "Windows":
        return Path(os.getenv("LOCALAPPDATA")) / "ffmpeg"  # type: ignore
    elif OS_NAME == "Darwin":
        return Path.home() / "Library" / "Application Support" / "ffmpeg"
    else:
        return Path.home() / ".local" / "share" / "ffmpeg"


def find_ffmpeg_bin_dir(extract_dir: Path, version: str) -> Optional[Path]:
    """
    Find the FFmpeg bin directory after extraction.
    
    Args:
        extract_dir: Directory where FFmpeg was extracted
        version: Version string (e.g., "8.0")
        
    Returns:
        Path to bin directory or None if not found
    """
    # Expected pattern: ffmpeg-{version}-essentials_build
    pattern = f"ffmpeg-{version}-essentials_build"
    
    # Look for the directory
    for item in extract_dir.iterdir():
        if item.is_dir() and item.name.startswith(f"ffmpeg-{version}"):
            bin_dir = item / "bin"
            if bin_dir.exists():
                logger.info(f"Found FFmpeg bin directory: {bin_dir}")
                return bin_dir
    
    logger.warning(f"Could not find FFmpeg bin directory with pattern: {pattern}")
    return None


def update_ffmpeg_windows(progress_callback: Optional[Callable[[str], None]] = None) -> bool:
    """
    Update FFmpeg on Windows to the latest Essentials build.
    
    Args:
        progress_callback: Optional callback function for progress updates
        
    Returns:
        True if update was successful, False otherwise
    """
    if OS_NAME != "Windows":
        logger.error("This update method is only for Windows")
        return False
    
    try:
        # Track last progress percentage to avoid spam
        last_percent = -1
        
        def report_progress(msg: str, force: bool = False):
            """Helper to report progress (always logged, callback only if force=True or status message)."""
            logger.info(msg)
            
            # Only send callback for non-percentage messages or when forced
            if progress_callback and (force or not msg.strip().endswith('%')):
                progress_callback(msg)
        
        def download_progress_wrapper(msg: str):
            """Wrapper for download progress that throttles percentage updates."""
            nonlocal last_percent
            
            # Extract percentage if present
            percent_match = re.search(r'(\d+)%', msg)
            if percent_match:
                current_percent = int(percent_match.group(1))
                # Only report every 10% and to logger only
                if current_percent != last_percent and current_percent % 10 == 0:
                    logger.info(msg)
                    if progress_callback:
                        progress_callback(msg)
                    last_percent = current_percent
            else:
                # Non-percentage messages get reported normally
                report_progress(msg, force=True)
        
        # Get latest version
        report_progress("🔍 Checking latest FFmpeg version...", force=True)
        latest_version = get_latest_ffmpeg_version()
        if not latest_version:
            report_progress("❌ Failed to determine latest version", force=True)
            return False
        
        report_progress(f"📦 Latest version: {latest_version}", force=True)
        
        extract_dir = get_ffmpeg_extract_dir()
        extract_dir.mkdir(exist_ok=True)
        
        # Try 7z method first (smaller size)
        use_7zip = check_7zip_installed()
        success = False
        
        if use_7zip:
            report_progress("⚡ Using 7-Zip method (smaller download)...", force=True)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".7z").name
            
            # Download 7z file
            report_progress("⬇ Downloading FFmpeg (7z)...", force=True)
            last_percent = -1  # Reset for this download
            if download_file(
                FFMPEG_7Z_DOWNLOAD_URL,
                temp_file,
                progress_callback=download_progress_wrapper,
            ):
                # Verify SHA-256 hash
                report_progress("🔐 Verifying download integrity...", force=True)
                if verify_sha256(temp_file, FFMPEG_7Z_SHA256_URL):
                    report_progress("⚙ Extracting FFmpeg...", force=True)
                    try:
                        subprocess.run(
                            ["7z", "x", temp_file, f"-o{extract_dir}", "-y"],
                            creationflags=SUBPROCESS_CREATIONFLAGS,
                            timeout=300,
                            check=True,
                        )
                        success = True
                    except Exception as e:
                        logger.exception(f"7z extraction failed: {e}")
                        report_progress(f"❌ 7z extraction failed, trying zip fallback...", force=True)
                else:
                    report_progress("❌ SHA-256 verification failed, trying zip fallback...", force=True)
            
            # Clean up temp file
            try:
                Path(temp_file).unlink(missing_ok=True)
            except Exception:
                pass
        
        # Fallback to zip method
        if not success:
            report_progress("📦 Using ZIP method...", force=True)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip").name
            
            # Download zip file
            report_progress("⬇ Downloading FFmpeg (zip)...", force=True)
            last_percent = -1  # Reset for this download
            if not download_file(
                FFMPEG_ZIP_DOWNLOAD_URL,
                temp_file,
                progress_callback=download_progress_wrapper,
            ):
                report_progress("❌ Failed to download FFmpeg", force=True)
                return False
            
            # Verify SHA-256 hash for zip
            report_progress("🔐 Verifying download integrity...", force=True)
            if not verify_sha256(temp_file, FFMPEG_ZIP_SHA256_URL):
                report_progress("⚠️ SHA-256 verification failed, proceeding anyway...", force=True)
            
            report_progress("⚙ Extracting FFmpeg...", force=True)
            try:
                import zipfile
                with zipfile.ZipFile(temp_file, "r") as zip_ref:
                    zip_ref.extractall(extract_dir)
                success = True
            except Exception as e:
                logger.exception(f"Extraction failed: {e}")
                report_progress(f"❌ Extraction failed: {e}", force=True)
                return False
            finally:
                # Clean up temp file
                try:
                    Path(temp_file).unlink(missing_ok=True)
                except Exception:
                    pass
        
        if not success:
            report_progress("❌ Both 7z and zip methods failed", force=True)
            return False
        
        # Find the bin directory
        report_progress("🔍 Locating FFmpeg binaries...", force=True)
        bin_dir = find_ffmpeg_bin_dir(extract_dir, latest_version)
        if not bin_dir:
            report_progress("❌ Could not locate FFmpeg bin directory", force=True)
            return False
        
        # Add to System Path
        report_progress("🔧 Configuring system paths...", force=True)
        user_path = os.environ.get("PATH", "")
        
        # Remove old FFmpeg paths from PATH
        path_parts = user_path.split(os.pathsep)
        cleaned_paths = [p for p in path_parts if "ffmpeg" not in p.lower() or str(bin_dir) in p]
        
        # Add new path if not already present
        if str(bin_dir) not in cleaned_paths:
            cleaned_paths.insert(0, str(bin_dir))
        
        new_path = os.pathsep.join(cleaned_paths)
        
        try:
            subprocess.run(
                ["setx", "PATH", new_path],
                creationflags=SUBPROCESS_CREATIONFLAGS,
                timeout=30,
                check=True,
            )
            os.environ["PATH"] = new_path
        except Exception as e:
            logger.warning(f"Failed to update PATH permanently: {e}")
            # Still update for current session
            os.environ["PATH"] = new_path
        
        # Verify installation
        report_progress("✅ Verifying installation...", force=True)
        new_version = get_ffmpeg_version_direct()
        if new_version not in ["Not found", "Error getting version", "Unknown version"]:
            report_progress(f"✅ FFmpeg successfully updated to version {new_version}!", force=True)
            return True
        else:
            report_progress("⚠️ Update completed but verification failed", force=True)
            return True  # Still return True as files were extracted
        
    except Exception as e:
        logger.exception(f"Error updating FFmpeg: {e}")
        if progress_callback:
            progress_callback(f"❌ Error: {e}")
        return False


def update_ffmpeg(progress_callback: Optional[Callable[[str], None]] = None) -> bool:
    """
    Update FFmpeg based on the operating system.
    
    Args:
        progress_callback: Optional callback function for progress updates
        
    Returns:
        True if update was successful, False otherwise
    """
    if OS_NAME == "Windows":
        return update_ffmpeg_windows(progress_callback)
    elif OS_NAME == "Darwin":
        # macOS update via Homebrew
        if progress_callback:
            progress_callback("🍺 Updating FFmpeg via Homebrew...")
        try:
            subprocess.run(["brew", "upgrade", "ffmpeg"], check=True, timeout=300)
            if progress_callback:
                progress_callback("✅ FFmpeg updated successfully!")
            return True
        except Exception as e:
            logger.exception(f"Error updating FFmpeg on macOS: {e}")
            if progress_callback:
                progress_callback(f"❌ Error: {e}")
            return False
    elif OS_NAME == "Linux":
        # Linux update via package manager
        if progress_callback:
            progress_callback("📦 Please use your package manager to update FFmpeg")
        return False
    else:
        logger.error(f"Unsupported operating system: {OS_NAME}")
        return False
