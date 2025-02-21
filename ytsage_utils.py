import sys
import os
import json
from pathlib import Path
import subprocess

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def get_yt_dlp_path():
    """Get the appropriate yt-dlp path based on platform and deployment method"""
    try:
        if getattr(sys, 'frozen', False):
            if sys.platform == 'darwin':
                # For macOS .app bundle
                if 'Contents/MacOS' in sys.executable:
                    # Inside .app bundle
                    return os.path.join(os.path.dirname(sys.executable), 'yt-dlp')
                else:
                    # Fallback to user's home directory for macOS
                    base_path = os.path.expanduser('~/Library/Application Support/YTSage')
                    os.makedirs(base_path, exist_ok=True)
                    return os.path.join(base_path, 'yt-dlp')
            elif sys.platform == 'win32':
                # For Windows executable
                app_data = os.getenv('APPDATA')
                if app_data:
                    base_path = os.path.join(app_data, 'YTSage')
                else:
                    base_path = os.path.dirname(sys.executable)
                os.makedirs(base_path, exist_ok=True)
                return os.path.join(base_path, 'yt-dlp.exe')
            else:
                # For Linux AppImage or binary
                if 'APPIMAGE' in os.environ:
                    # Inside AppImage
                    xdg_data = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
                    base_path = os.path.join(xdg_data, 'YTSage')
                else:
                    base_path = os.path.dirname(sys.executable)
                os.makedirs(base_path, exist_ok=True)
                return os.path.join(base_path, 'yt-dlp')
        else:
            # For development/script mode
            return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'yt-dlp.exe' if sys.platform == 'win32' else 'yt-dlp')
    except Exception as e:
        print(f"Error determining yt-dlp path: {e}")
        # Fallback to current directory
        return os.path.join(os.getcwd(), 'yt-dlp.exe' if sys.platform == 'win32' else 'yt-dlp')

def load_saved_path(main_window_instance): # Pass the main window instance
    config_file = main_window_instance.config_file # Access config_file via instance
    try:
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
                saved_path = config.get('download_path', '')
                if os.path.exists(saved_path):
                    main_window_instance.last_path = saved_path # Access last_path via instance
                else:
                    main_window_instance.last_path = str(Path.home() / 'Downloads')
        else:
            main_window_instance.last_path = str(Path.home() / 'Downloads')
    except Exception as e:
        print(f"Error loading saved settings: {e}")
        main_window_instance.last_path = str(Path.home() / 'Downloads')

def save_path(main_window_instance, path): # Pass main window instance
    config_file = main_window_instance.config_file # Access config_file via instance
    try:
        config = {
            'download_path': path
        }
        with open(config_file, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving settings: {e}")