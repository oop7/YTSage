import os
import sys
import subprocess
import requests
import shutil
import tempfile
import hashlib
from pathlib import Path
from PySide6.QtGui import QIcon
from .ytsage_logging import logger

def check_7zip_installed():
    """Check if 7-Zip is installed on Windows."""
    try:
        subprocess.run(['7z', '--help'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE,
                      creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def download_file(url, dest_path, progress_callback=None):
    """Download a file from URL to destination path with progress indication."""
    try:
        response = requests.get(url, stream=True, timeout=30)  # Added timeout
        response.raise_for_status()  # Check for HTTP errors
        total_size = int(response.headers.get('content-length', 0))
        
        with open(dest_path, 'wb') as f:
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
        logger.info(f"Download error: {str(e)}")
        return False

def get_file_sha256(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def verify_sha256(file_path, expected_hash_url):
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
        logger.info(f"⚠️ SHA-256 verification error: {str(e)}")
        return False

def get_ffmpeg_install_path():
    """Get the FFmpeg installation path."""
    if sys.platform == 'win32':
        return os.path.join(os.getenv('LOCALAPPDATA'), 'ffmpeg', 'ffmpeg-7.1.1-full_build', 'bin')
    elif sys.platform == 'darwin':
        paths = ['/usr/local/bin', '/opt/homebrew/bin', '/usr/bin']
        for path in paths:
            if os.path.exists(os.path.join(path, 'ffmpeg')):
                return path
        return '/usr/local/bin'  # Default Homebrew path
    else:
        return '/usr/bin'  # Standard Linux path

def get_ffmpeg_path():
    """
    Get the FFmpeg executable path, either from PATH or installation directory.
    Returns:
        str: Path to FFmpeg executable or 'ffmpeg' if found in PATH but path unknown
    """
    try:
        # First try to find ffmpeg in PATH using 'where' on Windows or 'which' on Unix
        if sys.platform == 'win32':
            # On Windows, use 'where' command and hide console window
            startupinfo = None
            if hasattr(subprocess, 'STARTUPINFO'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # SW_HIDE
            
            result = subprocess.run(
                ['where', 'ffmpeg'], 
                capture_output=True, 
                text=True, 
                check=False,
                startupinfo=startupinfo
            )
            if result.returncode == 0 and result.stdout.strip():
                ffmpeg_path = result.stdout.strip().split('\n')[0]
                return ffmpeg_path
        else:
            # On Unix systems, use 'which' command
            result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True, check=False)
            if result.returncode == 0 and result.stdout.strip():
                ffmpeg_path = result.stdout.strip()
                return ffmpeg_path
    except Exception as e:
        logger.error(f"Error finding ffmpeg in PATH: {e}")
    
    # If not found in PATH, check the installation directory
    ffmpeg_install_path = get_ffmpeg_install_path()
    if sys.platform == 'win32':
        ffmpeg_exe = os.path.join(ffmpeg_install_path, 'ffmpeg.exe')
    else:
        ffmpeg_exe = os.path.join(ffmpeg_install_path, 'ffmpeg')
        
    if os.path.exists(ffmpeg_exe):
        return ffmpeg_exe
    
    # Return command name as fallback
    return "ffmpeg"

def check_ffmpeg_installed():
    """Check if FFmpeg is installed and accessible."""
    try:
        # First try the PATH
        result = subprocess.run(['ffmpeg', '-version'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             check=True,
                             creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                             timeout=5)  # Added timeout
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        # If not in PATH, check the installation directory
        ffmpeg_path = get_ffmpeg_install_path()
        if sys.platform == 'win32':
            ffmpeg_exe = os.path.join(ffmpeg_path, 'ffmpeg.exe')
        else:
            ffmpeg_exe = os.path.join(ffmpeg_path, 'ffmpeg')
            
        if os.path.exists(ffmpeg_exe):
            # Add to PATH if found
            os.environ['PATH'] = f"{ffmpeg_path}{os.pathsep}{os.environ.get('PATH', '')}"
            return True
        return False
    except Exception as e:
        logger.info(f"FFmpeg check error: {str(e)}")
        return False

def install_ffmpeg_windows():
    """Install FFmpeg on Windows using 7z method primarily, with zip as fallback."""
    ffmpeg_path = get_ffmpeg_install_path()
    
    # Check if already installed
    if check_ffmpeg_installed():
        logger.info("FFmpeg is already installed!")
        return True
        
    try:
        # Define variables - prioritize 7z version
        ffmpeg_7z_url = "https://github.com/GyanD/codexffmpeg/releases/download/7.1.1/ffmpeg-7.1.1-full_build.7z"
        ffmpeg_zip_url = "https://github.com/GyanD/codexffmpeg/releases/download/7.1.1/ffmpeg-7.1.1-full_build.zip"
        sha256_url = "https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.1.1-full_build.7z.sha256"
        extract_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'ffmpeg')
        full_build_dir = os.path.join(extract_dir, 'ffmpeg-7.1.1-full_build')
        bin_dir = os.path.join(full_build_dir, 'bin')

        # Create extraction directory if it doesn't exist
        os.makedirs(extract_dir, exist_ok=True)

        # Try 7z method first (smaller size)
        use_7zip = check_7zip_installed()
        if use_7zip:
            logger.info("Using 7-Zip method (smaller download size)...")
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.7z').name
            
            # Download 7z file
            if not download_file(ffmpeg_7z_url, temp_file, 
                               progress_callback=lambda msg: logger.debug(msg)):
                logger.error("Failed to download 7z file, trying zip fallback...")
                use_7zip = False
            else:
                # Verify SHA-256 hash for 7z file
                if verify_sha256(temp_file, sha256_url):
                    logger.info("Extracting FFmpeg components from 7z archive...")
                    try:
                        subprocess.run(['7z', 'x', temp_file, f'-o{extract_dir}', '-y'],
                                     creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                                     timeout=300)  # 5-minute timeout
                    except Exception as e:
                        logger.error(f"7z extraction failed: {str(e)}, trying zip fallback...")
                        use_7zip = False
                else:
                    logger.error("SHA-256 verification failed for 7z file, trying zip fallback...")
                    use_7zip = False
        
        # Fallback to zip method if 7z failed or not available
        if not use_7zip:
            logger.info("Using ZIP method as fallback...")
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip').name
            
            # Download zip file
            if not download_file(ffmpeg_zip_url, temp_file, 
                               progress_callback=lambda msg: logger.debug(msg)):
                raise Exception("Failed to download FFmpeg (both 7z and zip methods failed)")

            logger.info("Extracting FFmpeg components from zip archive...")
            try:
                import zipfile
                with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
            except Exception as e:
                raise Exception(f"Extraction failed: {str(e)}")

        logger.info("Configuring system paths...")
        # Add to System Path
        user_path = os.environ.get('PATH', '')
        if bin_dir not in user_path:
            subprocess.run(['setx', 'PATH', f"{user_path};{bin_dir}"], 
                         creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            os.environ['PATH'] = f"{user_path};{bin_dir}"

        # Clean up
        try:
            os.unlink(temp_file)
        except Exception:
            pass  # Ignore cleanup errors

        # Verify installation
        if not check_ffmpeg_installed():
            raise Exception("FFmpeg installation verification failed")

        logger.info("FFmpeg installation completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Error installing FFmpeg: {str(e)}")
        return False

def install_ffmpeg_macos():
    """Install FFmpeg on macOS using Homebrew."""
    try:
        # Check if Homebrew is installed
        try:
            subprocess.run(['brew', '--version'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, 
                         check=True,
                         timeout=5)
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.info("Installing Homebrew...")
            brew_install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            subprocess.run(brew_install_cmd, shell=True, check=True, timeout=300)

        # Install FFmpeg
        logger.info("Installing FFmpeg...")
        subprocess.run(['brew', 'install', 'ffmpeg'], check=True, timeout=300)
        
        # Verify installation
        if not check_ffmpeg_installed():
            raise Exception("FFmpeg installation verification failed")
            
        return True

    except Exception as e:
        logger.error(f"Error installing FFmpeg: {str(e)}")
        return False

def install_ffmpeg_linux():
    """Install FFmpeg on Linux using appropriate package manager."""
    try:
        # Detect the package manager
        if shutil.which('apt'):
            # Debian/Ubuntu
            subprocess.run(['sudo', 'apt', 'update'], check=True, timeout=60)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'ffmpeg'], check=True, timeout=300)
        elif shutil.which('dnf'):
            # Fedora
            subprocess.run(['sudo', 'dnf', 'install', '-y', 'ffmpeg'], check=True, timeout=300)
        elif shutil.which('pacman'):
            # Arch Linux
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg'], check=True, timeout=300)
        elif shutil.which('snap'):
            # Universal snap package
            subprocess.run(['sudo', 'snap', 'install', 'ffmpeg'], check=True, timeout=300)
        else:
            raise Exception("No supported package manager found")
        
        # Verify installation
        if not check_ffmpeg_installed():
            raise Exception("FFmpeg installation verification failed")
            
        return True

    except Exception as e:
        logger.error(f"Error installing FFmpeg: {str(e)}")
        return False

def auto_install_ffmpeg():
    """Automatically install FFmpeg based on the operating system."""
    if sys.platform == 'win32':
        return install_ffmpeg_windows()
    elif sys.platform == 'darwin':
        return install_ffmpeg_macos()
    elif sys.platform.startswith('linux'):
        return install_ffmpeg_linux()
    else:
        logger.info(f"Unsupported operating system: {sys.platform}")
        return False 