import os
import sys
import subprocess
import requests
import shutil
import tempfile
from pathlib import Path
from PySide6.QtGui import QIcon

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
        print(f"Download error: {str(e)}")
        return False

def get_ffmpeg_install_path():
    """Get the FFmpeg installation path."""
    if sys.platform == 'win32':
        return os.path.join(os.getenv('LOCALAPPDATA'), 'ffmpeg', 'ffmpeg-7.1-full_build', 'bin')
    elif sys.platform == 'darwin':
        paths = ['/usr/local/bin', '/opt/homebrew/bin', '/usr/bin']
        for path in paths:
            if os.path.exists(os.path.join(path, 'ffmpeg')):
                return path
        return '/usr/local/bin'  # Default Homebrew path
    else:
        return '/usr/bin'  # Standard Linux path

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
        print(f"FFmpeg check error: {str(e)}")
        return False

def install_ffmpeg_windows():
    """Install FFmpeg on Windows using either 7z or zip method."""
    ffmpeg_path = get_ffmpeg_install_path()
    
    # Check if already installed
    if check_ffmpeg_installed():
        print("✨ FFmpeg is already installed!")
        return True
        
    try:
        # Define variables
        ffmpeg_url = "https://github.com/GyanD/codexffmpeg/releases/download/7.1/ffmpeg-7.1-full_build.7z"
        zip_url = "https://github.com/GyanD/codexffmpeg/releases/download/7.1/ffmpeg-7.1-full_build.zip"
        extract_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'ffmpeg')
        full_build_dir = os.path.join(extract_dir, 'ffmpeg-7.1-full_build')
        bin_dir = os.path.join(full_build_dir, 'bin')

        # Create extraction directory if it doesn't exist
        os.makedirs(extract_dir, exist_ok=True)

        # Choose installation method based on 7-Zip availability
        use_7zip = check_7zip_installed()
        temp_file = tempfile.NamedTemporaryFile(delete=False, 
                                              suffix='.7z' if use_7zip else '.zip').name

        # Download with progress callback
        if not download_file(ffmpeg_url if use_7zip else zip_url, temp_file, 
                           progress_callback=lambda msg: print(msg)):
            raise Exception("Failed to download FFmpeg")

        print("🔧 Extracting FFmpeg components...")
        try:
            if use_7zip:
                # Extract using 7-Zip
                subprocess.run(['7z', 'x', temp_file, f'-o{extract_dir}', '-y'],
                             creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                             timeout=300)  # 5-minute timeout
            else:
                # Extract using built-in Windows tools
                import zipfile
                with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
        except Exception as e:
            raise Exception(f"Extraction failed: {str(e)}")

        print("⚙️ Configuring system paths...")
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

        print("✨ FFmpeg installation completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Error installing FFmpeg: {str(e)}")
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
            print("Installing Homebrew...")
            brew_install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            subprocess.run(brew_install_cmd, shell=True, check=True, timeout=300)

        # Install FFmpeg
        print("Installing FFmpeg...")
        subprocess.run(['brew', 'install', 'ffmpeg'], check=True, timeout=300)
        
        # Verify installation
        if not check_ffmpeg_installed():
            raise Exception("FFmpeg installation verification failed")
            
        return True

    except Exception as e:
        print(f"Error installing FFmpeg: {str(e)}")
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
        print(f"Error installing FFmpeg: {str(e)}")
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
        print(f"Unsupported operating system: {sys.platform}")
        return False 