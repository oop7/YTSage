import sys
import os
import json
from pathlib import Path
import subprocess
import tempfile
import shutil
from ytsage_ffmpeg import check_ffmpeg_installed, get_ffmpeg_install_path

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
                    print(f"Error updating PATH: {e}")
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
                        print(f"Error updating PATH: {e}")
                        continue
                    
        return False
        
    except Exception as e:
        print(f"Error checking FFmpeg: {e}")
        return False

def get_yt_dlp_path():
    """Get the yt-dlp command or path, prioritizing the system PATH."""
    try:
        # Use shutil.which to find yt-dlp in the system's PATH
        yt_dlp_executable = shutil.which('yt-dlp')
        
        if yt_dlp_executable:
            print(f"Found yt-dlp executable in PATH: {yt_dlp_executable}")
            return yt_dlp_executable
        else:
            # If not found in PATH, assume 'yt-dlp' is the command name
            print("yt-dlp not found in PATH. Will attempt to use 'yt-dlp' as the command.")
            return 'yt-dlp'
            
    except Exception as e:
        print(f"Error finding yt-dlp path: {e}")
        # Fallback to the command name on any error
        print("An error occurred during yt-dlp path detection. Falling back to command 'yt-dlp'.")
        return 'yt-dlp'

def load_saved_path(main_window_instance):
    """Load saved download path with enhanced error handling."""
    config_file = main_window_instance.config_file
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
                print(f"Error reading config file: {e}")
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
        print(f"Error loading saved settings: {e}")
        main_window_instance.last_path = tempfile.gettempdir()

def save_path(main_window_instance, path):
    """Save download path with enhanced error handling."""
    config_file = main_window_instance.config_file
    try:
        # Verify the path is valid and writable
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                print(f"Error creating directory: {e}")
                return False
                
        if not os.access(path, os.W_OK):
            print("Path is not writable")
            return False
            
        # Create config directory if it doesn't exist
        config_dir = config_file.parent
        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)
            
        # Save the config
        config = {'download_path': path}
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False)
        return True
        
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False