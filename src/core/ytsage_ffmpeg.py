import hashlib
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import requests

from src.utils.ytsage_logger import logger
from src.utils.ytsage_constants import (
    FFMPEG_7Z_DOWNLOAD_URL,
    FFMPEG_7Z_SHA256_URL,
    FFMPEG_ZIP_DOWNLOAD_URL,
    FFMPEG_ZIP_SHA256_URL,
    OS_NAME,
    SUBPROCESS_CREATIONFLAGS,
)


def check_7zip_installed() -> bool:
    """Check if 7-Zip is installed on Windows."""
    try:
        subprocess.run(["7z", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=SUBPROCESS_CREATIONFLAGS)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def download_file(url, dest_path, progress_callback=None) -> bool:
    """Download a file from URL to destination path with progress indication."""
    try:
        response = requests.get(url, stream=True, timeout=30)  # Added timeout
        response.raise_for_status()  # Check for HTTP errors
        total_size = int(response.headers.get("content-length", 0))

        with open(dest_path, "wb") as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for data in response.iter_content(chunk_size=8192):
                    downloaded += len(data)
                    f.write(data)
                    if progress_callback:
                        progress = int((downloaded / total_size) * 100)
                        progress_callback(f"⚡ Downloading FFmpeg components... {progress}%")
        return True
    except requests.RequestException as e:
        logger.info(f"Download error: {e}")
        return False


def get_file_sha256(file_path) -> str:
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def verify_sha256(file_path, expected_hash_url) -> bool:
    """Verify file SHA-256 hash against expected hash from URL."""
    try:
        # Download the SHA-256 hash
        response = requests.get(expected_hash_url, timeout=10)
        response.raise_for_status()
        expected_hash = response.text.strip().split()[0]  # Get just the hash part

        # Calculate actual hash
        actual_hash = get_file_sha256(file_path)

        # Compare hashes
        if actual_hash.lower() == expected_hash.lower():
            logger.info("SHA-256 verification successful!")
            return True
        else:
            logger.error(f"SHA-256 verification failed!")
            logger.info(f"Expected: {expected_hash}")
            logger.info(f"Actual:   {actual_hash}")
            return False
    except Exception as e:
        logger.info(f"⚠️ SHA-256 verification error: {e}")
        return False


def get_ffmpeg_install_path() -> Path:
    """
    Get the FFmpeg installation path.
    For Windows, tries to find the latest essentials build dynamically.
    """
    if OS_NAME == "Windows":
        ffmpeg_base = Path(os.getenv("LOCALAPPDATA")) / "ffmpeg"  # type: ignore
        
        # If the directory exists, look for any ffmpeg-*-essentials_build folder
        if ffmpeg_base.exists():
            # Find all directories matching the pattern
            essentials_dirs = list(ffmpeg_base.glob("ffmpeg-*-essentials_build"))
            if essentials_dirs:
                # Sort by name (which includes version) and take the latest
                latest_dir = sorted(essentials_dirs, reverse=True)[0]
                bin_dir = latest_dir / "bin"
                if bin_dir.exists():
                    return bin_dir
        
        # Fallback: return default path (even if it doesn't exist yet)
        return ffmpeg_base / "ffmpeg-essentials_build" / "bin"

    elif OS_NAME == "Darwin":
        paths = ["/usr/local/bin", "/opt/homebrew/bin", "/usr/bin"]
        for path in paths:
            if Path(path).joinpath("ffmpeg").exists():
                return Path(path)
        return Path("/usr/local/bin")  # Default Homebrew path
    else:
        return Path("/usr/bin")  # Standard Linux path



def get_ffmpeg_path() -> str | Path:
    """
    Get the FFmpeg executable path, either from PATH or installation directory.
    Returns:
        str: Path to FFmpeg executable or 'ffmpeg' if found in PATH but path unknown
    """
    try:
        # First try to find ffmpeg in PATH using 'where' on Windows or 'which' on Unix
        if OS_NAME == "Windows":
            # On Windows, use 'where' command and hide console window
            # Extra logic moved to src\utils\ytsage_constants.py

            result = subprocess.run(
                ["where", "ffmpeg"],
                capture_output=True,
                text=True,
                check=False,
                creationflags=SUBPROCESS_CREATIONFLAGS,
            )
            if result.returncode == 0 and result.stdout.strip():
                ffmpeg_path = result.stdout.strip().split("\n")[0]
                return ffmpeg_path
        else:
            # On Unix systems, use 'which' command
            result = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True, check=False)
            if result.returncode == 0 and result.stdout.strip():
                ffmpeg_path = result.stdout.strip()
                return ffmpeg_path
    except Exception as e:
        logger.exception(f"Error finding ffmpeg in PATH: {e}")

    # If not found in PATH, check the installation directory
    ffmpeg_install_path = get_ffmpeg_install_path()
    if OS_NAME == "Windows":
        ffmpeg_exe = Path(ffmpeg_install_path).joinpath("ffmpeg.exe")
    else:
        ffmpeg_exe = Path(ffmpeg_install_path).joinpath("ffmpeg")

    if ffmpeg_exe.exists():
        return ffmpeg_exe

    # Return command name as fallback
    return "ffmpeg"


def check_ffmpeg_installed() -> bool:
    """Check if FFmpeg is installed and accessible."""
    try:
        # First try the PATH
        result = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            creationflags=SUBPROCESS_CREATIONFLAGS,
            timeout=5,
        )  # Added timeout
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        # If not in PATH, check the installation directory
        ffmpeg_path = get_ffmpeg_install_path()
        if OS_NAME == "Windows":
            ffmpeg_exe = Path(ffmpeg_path).joinpath("ffmpeg.exe")
        else:
            ffmpeg_exe = Path(ffmpeg_path).joinpath("ffmpeg")

        if ffmpeg_exe.exists():
            # Add to PATH if found
            os.environ["PATH"] = f"{ffmpeg_path}{os.pathsep}{os.environ.get('PATH', '')}"
            return True
        return False
    except Exception as e:
        logger.info(f"FFmpeg check error: {e}")
        return False


def install_ffmpeg_windows(progress_callback=None) -> bool:
    """Install FFmpeg on Windows using essentials build with 7z method primarily, with zip as fallback."""
    # Check if already installed
    if check_ffmpeg_installed():
        logger.info("FFmpeg is already installed!")
        if progress_callback:
            progress_callback("✅ FFmpeg is already installed!")
        return True

    try:
        # Define variables for essentials build
        extract_dir = Path(os.getenv("LOCALAPPDATA")) / "ffmpeg"  # type: ignore
        
        # Create extraction directory if it doesn't exist
        extract_dir.mkdir(exist_ok=True)

        # Try 7z method first (smaller size)
        use_7zip = check_7zip_installed()
        success = False
        
        if use_7zip:
            logger.info("Using 7-Zip method (smaller download size)...")
            if progress_callback:
                progress_callback("⚡ Using 7-Zip method...")
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".7z").name

            # Download 7z file
            if progress_callback:
                progress_callback("⬇ Downloading FFmpeg (7z)...")
            if download_file(
                FFMPEG_7Z_DOWNLOAD_URL,
                temp_file,
                progress_callback=progress_callback,
            ):
                # Verify SHA-256 hash for 7z file
                if progress_callback:
                    progress_callback("🔐 Verifying download integrity...")
                if verify_sha256(temp_file, FFMPEG_7Z_SHA256_URL):
                    logger.info("Extracting FFmpeg components from 7z archive...")
                    if progress_callback:
                        progress_callback("⚙ Extracting FFmpeg...")
                    try:
                        subprocess.run(
                            ["7z", "x", temp_file, f"-o{extract_dir}", "-y"],
                            creationflags=SUBPROCESS_CREATIONFLAGS,
                            timeout=300,
                            check=True,
                        )
                        success = True
                    except Exception as e:
                        logger.exception(f"7z extraction failed: {e}, trying zip fallback...")
                        if progress_callback:
                            progress_callback("❌ 7z extraction failed, trying zip fallback...")
                else:
                    logger.error("SHA-256 verification failed for 7z file, trying zip fallback...")
                    if progress_callback:
                        progress_callback("❌ SHA-256 verification failed, trying zip fallback...")
            
            # Clean up temp file
            try:
                Path(temp_file).unlink(missing_ok=True)
            except Exception:
                pass

        # Fallback to zip method if 7z failed or not available
        if not success:
            logger.info("Using ZIP method as fallback...")
            if progress_callback:
                progress_callback("📦 Using ZIP method...")
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip").name

            # Download zip file
            if progress_callback:
                progress_callback("⬇ Downloading FFmpeg (zip)...")
            if not download_file(
                FFMPEG_ZIP_DOWNLOAD_URL,
                temp_file,
                progress_callback=progress_callback,
            ):
                logger.error("Failed to download FFmpeg (both 7z and zip methods failed)")
                if progress_callback:
                    progress_callback("❌ Failed to download FFmpeg")
                return False

            # Verify SHA-256 hash for zip
            if progress_callback:
                progress_callback("🔐 Verifying download integrity...")
            if not verify_sha256(temp_file, FFMPEG_ZIP_SHA256_URL):
                logger.warning("SHA-256 verification failed for zip file, proceeding anyway...")
                if progress_callback:
                    progress_callback("⚠️ SHA-256 verification failed, proceeding anyway...")

            logger.info("Extracting FFmpeg components from zip archive...")
            if progress_callback:
                progress_callback("⚙ Extracting FFmpeg...")
            try:
                import zipfile
                with zipfile.ZipFile(temp_file, "r") as zip_ref:
                    zip_ref.extractall(extract_dir)
                success = True
            except Exception as e:
                logger.exception(f"Extraction failed: {e}")
                if progress_callback:
                    progress_callback(f"❌ Extraction failed: {e}")
                return False
            finally:
                # Clean up temp file
                try:
                    Path(temp_file).unlink(missing_ok=True)
                except Exception:
                    pass

        if not success:
            logger.error("Both 7z and zip methods failed")
            if progress_callback:
                progress_callback("❌ Installation failed")
            return False

        # Find the bin directory in the extracted essentials build
        logger.info("Locating FFmpeg binaries...")
        if progress_callback:
            progress_callback("🔍 Locating FFmpeg binaries...")
        
        bin_dir = None
        # Look for any directory matching ffmpeg-*-essentials_build pattern
        for item in extract_dir.iterdir():
            if item.is_dir() and "essentials_build" in item.name.lower():
                potential_bin = item / "bin"
                if potential_bin.exists():
                    bin_dir = potential_bin
                    logger.info(f"Found FFmpeg bin directory: {bin_dir}")
                    break
        
        if not bin_dir:
            logger.error("Could not locate FFmpeg bin directory")
            if progress_callback:
                progress_callback("❌ Could not locate FFmpeg bin directory")
            return False

        logger.info("Configuring system paths...")
        if progress_callback:
            progress_callback("🔧 Configuring system paths...")
        
        # Add to System Path
        user_path = os.environ.get("PATH", "")
        path_parts = user_path.split(os.pathsep)
        
        # Remove old FFmpeg paths and add new one
        cleaned_paths = [p for p in path_parts if "ffmpeg" not in p.lower() or str(bin_dir) in p]
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
        if progress_callback:
            progress_callback("✅ Verifying installation...")
        if not check_ffmpeg_installed():
            logger.error("FFmpeg installation verification failed")
            if progress_callback:
                progress_callback("⚠️ Installation completed but verification failed")
            return True  # Still return True as files were extracted

        logger.info("FFmpeg installation completed successfully!")
        if progress_callback:
            progress_callback("✅ FFmpeg installation completed successfully!")
        return True

    except Exception as e:
        logger.exception(f"Error installing FFmpeg: {e}")
        if progress_callback:
            progress_callback(f"❌ Error installing FFmpeg: {e}")
        return False


def install_ffmpeg_macos() -> bool:
    """Install FFmpeg on macOS using Homebrew."""
    try:
        # Check if Homebrew is installed
        try:
            subprocess.run(
                ["brew", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                timeout=5,
            )
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.info("Installing Homebrew...")
            brew_install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            subprocess.run(brew_install_cmd, shell=True, check=True, timeout=300)

        # Install FFmpeg
        logger.info("Installing FFmpeg...")
        subprocess.run(["brew", "install", "ffmpeg"], check=True, timeout=300)

        # Verify installation
        if not check_ffmpeg_installed():
            logger.error("FFmpeg installation verification failed")
            return False

        return True

    except Exception as e:
        logger.exception(f"Error installing FFmpeg: {e}")
        return False


def install_ffmpeg_linux() -> bool:
    """Install FFmpeg on Linux using appropriate package manager."""
    try:
        # Detect the package manager
        if shutil.which("apt"):
            # Debian/Ubuntu
            subprocess.run(["sudo", "apt", "update"], check=True, timeout=60)
            subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True, timeout=300)
        elif shutil.which("dnf"):
            # Fedora
            subprocess.run(["sudo", "dnf", "install", "-y", "ffmpeg"], check=True, timeout=300)
        elif shutil.which("pacman"):
            # Arch Linux
            subprocess.run(
                ["sudo", "pacman", "-S", "--noconfirm", "ffmpeg"],
                check=True,
                timeout=300,
            )
        elif shutil.which("snap"):
            # Universal snap package
            subprocess.run(["sudo", "snap", "install", "ffmpeg"], check=True, timeout=300)
        else:
            logger.error("No supported package manager found")
            return False

        # Verify installation
        if not check_ffmpeg_installed():
            logger.error("FFmpeg installation verification failed")
            return False

        return True

    except Exception as e:
        logger.exception(f"Error installing FFmpeg: {e}")
        return False


def auto_install_ffmpeg(progress_callback=None) -> bool:
    """Automatically install FFmpeg based on the operating system."""
    if OS_NAME == "Windows":
        return install_ffmpeg_windows(progress_callback=progress_callback)
    elif OS_NAME == "Darwin":
        return install_ffmpeg_macos()
    elif OS_NAME == "Linux":
        return install_ffmpeg_linux()
    else:
        logger.info(f"Unsupported operating system: {OS_NAME}")
        if progress_callback:
            progress_callback(f"❌ Unsupported operating system: {OS_NAME}")
        return False
