import sys
import os
import webbrowser
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QProgressBar, QLabel, QFileDialog,
                            QHeaderView, QStyle, QStyleFactory, QComboBox, QTextEdit, QDialog, QPlainTextEdit, QCheckBox, QButtonGroup, QListWidget,
                            QListWidgetItem, QDialogButtonBox, QScrollArea, QGroupBox, QTabWidget, QRadioButton, QMessageBox)
from PySide6.QtCore import Qt, Signal, QObject, QThread, QProcess, QTimer
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime
import json
from pathlib import Path
from packaging import version
import subprocess
import re
try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    print("Warning: yt-dlp not available at startup, will be downloaded at runtime")
import time  # Add time import for cache timestamps
from ytsage_ffmpeg import auto_install_ffmpeg, check_ffmpeg_installed
from ytsage_yt_dlp import get_yt_dlp_path

from ytsage_utils import check_ffmpeg, load_saved_path, save_path, get_ytdlp_version, get_ffmpeg_version, refresh_version_cache, _version_cache # Import utility functions


class LogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('yt-dlp Log')
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout(self)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: Consolas, monospace;
                font-size: 12px;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
            }
        """)

        layout.addWidget(self.log_text)

    def append_log(self, message):
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

class CustomCommandDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle('Custom yt-dlp Command')
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)

        # Help text
        help_text = QLabel(
            "Enter custom yt-dlp commands below. The URL will be automatically appended.\n"
            "Example: --extract-audio --audio-format mp3 --audio-quality 0\n"
            "Note: Download path and output template will be preserved."
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #999999; padding: 10px;")
        layout.addWidget(help_text)

        # Command input
        self.command_input = QPlainTextEdit()
        self.command_input.setPlaceholderText("Enter yt-dlp arguments...")
        self.command_input.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1d1e22;
                color: #ffffff;
                border: 2px solid #1d1e22;
                border-radius: 4px;
                padding: 8px;
                font-family: Consolas, monospace;
            }
        """)
        layout.addWidget(self.command_input)

        # Add SponsorBlock checkbox
        self.sponsorblock_checkbox = QCheckBox("Remove Sponsor Segments")
        self.sponsorblock_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 20px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #1d1e22;
                border-radius: 9px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
                border-radius: 9px;
            }
        """)
        layout.insertWidget(layout.indexOf(self.command_input), self.sponsorblock_checkbox)

        # Buttons
        button_layout = QHBoxLayout()

        self.run_btn = QPushButton("Run Command")
        self.run_btn.clicked.connect(self.run_custom_command)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)

        button_layout.addWidget(self.run_btn)
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background-color: #1d1e22;
                color: #ffffff;
                border: 2px solid #1d1e22;
                border-radius: 4px;
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.log_output)

        self.setStyleSheet("""
            QDialog {
                background-color: #15181b;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
        """)

    def run_custom_command(self):
        url = self.parent.url_input.text().strip()
        if not url:
            self.log_output.append("Error: No URL provided")
            return

        command = self.command_input.toPlainText().strip()
        path = self.parent.path_input.text().strip()

        self.log_output.clear()
        self.log_output.append(f"Running command with URL: {url}")
        self.run_btn.setEnabled(False)

        # Start command in thread
        import threading
        threading.Thread(target=self._run_command_thread,
                        args=(command, url, path),
                        daemon=True).start()

    def _run_command_thread(self, command, url, path):
        try:
            class CommandLogger:
                def debug(self, msg):
                    self.dialog.log_output.append(msg)
                def warning(self, msg):
                    self.dialog.log_output.append(f"Warning: {msg}")
                def error(self, msg):
                    self.dialog.log_output.append(f"Error: {msg}")
                def __init__(self, dialog):
                    self.dialog = dialog

            # Split command into arguments
            args = command.split()

            # Base options
            ydl_opts = {
                'logger': CommandLogger(self),
                'paths': {'home': path},
                'debug_printout': True,
                'postprocessors': []
            }

            # Add SponsorBlock options if enabled
            if self.sponsorblock_checkbox.isChecked():
                ydl_opts['postprocessors'].extend([{
                    'key': 'SponsorBlock',
                    'categories': ['sponsor', 'selfpromo', 'interaction'],
                    'api': 'https://sponsor.ajay.app'
                }, {
                    'key': 'ModifyChapters',
                    'remove_sponsor_segments': ['sponsor', 'selfpromo', 'interaction'],
                    'sponsorblock_chapter_title': '[SponsorBlock]: %(category_names)l',
                    'force_keyframes': True
                }])

            # Add custom arguments
            for i in range(0, len(args), 2):
                if i + 1 < len(args):
                    key = args[i].lstrip('-').replace('-', '_')
                    value = args[i + 1]
                    try:
                        # Try to convert to appropriate type
                        if value.lower() in ('true', 'false'):
                            value = value.lower() == 'true'
                        elif value.isdigit():
                            value = int(value)
                        ydl_opts[key] = value
                    except:
                        ydl_opts[key] = value

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.log_output.append("Command completed successfully")

        except Exception as e:
            self.log_output.append(f"Error: {str(e)}")
        finally:
            self.run_btn.setEnabled(True)

class FFmpegInstallThread(QThread):
    finished = Signal(bool)
    progress = Signal(str)

    def run(self):
        # Redirect stdout to capture progress messages
        import sys
        from io import StringIO
        import contextlib

        output = StringIO()
        with contextlib.redirect_stdout(output):
            success = auto_install_ffmpeg()
            
        # Process captured output and emit progress signals
        for line in output.getvalue().splitlines():
            self.progress.emit(line)
            
        self.finished.emit(success)

class FFmpegCheckDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Installing FFmpeg')
        self.setMinimumWidth(450)
        self.setMinimumHeight(250)
        
        # Set the window icon to match the main app
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Header with icon
        header_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown).pixmap(32, 32))
        header_layout.addWidget(icon_label)
        
        header_text = QLabel("FFmpeg Installation")
        header_text.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(header_text)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Message
        self.message_label = QLabel(
            "🎥 YTSage needs FFmpeg to process videos.\n"
            "Let's set it up for you automatically!"
        )
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.message_label)

        # Progress label with cool emojis
        self.progress_label = QLabel("")
        self.progress_label.setWordWrap(True)
        self.progress_label.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)
        self.progress_label.hide()
        layout.addWidget(self.progress_label)

        # Buttons container
        button_layout = QHBoxLayout()
        
        # Install button
        self.install_btn = QPushButton("Install FFmpeg")
        self.install_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
        self.install_btn.clicked.connect(self.start_installation)
        button_layout.addWidget(self.install_btn)

        # Manual install button
        self.manual_btn = QPushButton("Manual Guide")
        self.manual_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogHelpButton))
        self.manual_btn.clicked.connect(lambda: webbrowser.open('https://github.com/oop7/ffmpeg-install-guide'))
        button_layout.addWidget(self.manual_btn)

        # Close button
        self.close_btn = QPushButton("Close")
        self.close_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton))
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)

        # Style the dialog
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #3d3d3d;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                margin: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:disabled {
                background-color: #2d2d2d;
                color: #666666;
            }
        """)

        # Initialize installation thread
        self.install_thread = None

    def start_installation(self):
        self.install_btn.setEnabled(False)
        self.manual_btn.setEnabled(False)
        self.close_btn.setEnabled(False)
        
        # Check if FFmpeg is already installed
        if check_ffmpeg_installed():
            self.message_label.setText("🎉 FFmpeg is already installed!")
            self.progress_label.setText("✅ You can close this dialog and continue using YTSage.")
            self.install_btn.hide()
            self.manual_btn.hide()
            self.close_btn.setEnabled(True)
            return
            
        self.message_label.setText("🚀 Installing FFmpeg... Hold tight!")
        self.progress_label.show()

        self.install_thread = FFmpegInstallThread()
        self.install_thread.finished.connect(self.installation_finished)
        self.install_thread.progress.connect(self.update_progress)
        self.install_thread.start()

    def update_progress(self, message):
        self.progress_label.setText(message)

    def installation_finished(self, success):
        if success:
            self.message_label.setText("🎉 FFmpeg has been installed successfully!")
            self.progress_label.setText("✅ You're all set! You can now close this dialog and continue using YTSage.")
            self.install_btn.hide()
            self.manual_btn.hide()
        else:
            self.message_label.setText("❌ Oops! FFmpeg installation encountered an issue.")
            self.progress_label.setText("💡 Try using the manual installation guide instead.")
            self.install_btn.setEnabled(True)
            self.manual_btn.setEnabled(True)
        
        self.close_btn.setEnabled(True)

class VersionCheckThread(QThread):
    finished = Signal(str, str, str) # current_version, latest_version, error_message
    
    def run(self):
        current_version = ""
        latest_version = ""
        error_message = ""
        
        try:
            # Get the yt-dlp executable path using the new module
            yt_dlp_path = get_yt_dlp_path()
            
            # Get current version with timeout
            try:
                result = subprocess.run([yt_dlp_path, '--version'], 
                                     capture_output=True, 
                                     text=True,
                                     timeout=30,  # 30 second timeout
                                     startupinfo=None if sys.platform != 'win32' else subprocess.STARTUPINFO(dwFlags=subprocess.STARTF_USESHOWWINDOW, wShowWindow=subprocess.SW_HIDE), # Hide console window on Windows
                                     creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0) # Hide console window on Windows
                if result.returncode == 0:
                    current_version = result.stdout.strip()
                else: # Try fallback if command failed
                    if YT_DLP_AVAILABLE:
                        current_version = yt_dlp.version.__version__
                    else:
                        error_message = "yt-dlp not available."
                        self.finished.emit(current_version, latest_version, error_message)
                        return
            except subprocess.TimeoutExpired:
                # Try fallback if timeout
                if YT_DLP_AVAILABLE:
                    current_version = yt_dlp.version.__version__
                else:
                    error_message = "yt-dlp version check timed out and package not found."
                    self.finished.emit(current_version, latest_version, error_message)
                    return
            except Exception:
                 # Fallback to importing yt_dlp package directly if subprocess fails
                if YT_DLP_AVAILABLE:
                    current_version = yt_dlp.version.__version__
                else:
                     error_message = "yt-dlp not found or accessible."
                     self.finished.emit(current_version, latest_version, error_message)
                     return


            # Get latest version from PyPI
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10) # Add timeout
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            latest_version = response.json()["info"]["version"]
            
            # Clean up version strings
            current_version = current_version.replace('_', '.')
            latest_version = latest_version.replace('_', '.')

        except requests.RequestException as e:
            error_message = f"Network error checking PyPI: {e}"
        except Exception as e:
            error_message = f"Error checking version: {e}"
            
        self.finished.emit(current_version, latest_version, error_message)


class UpdateThread(QThread):
    update_status = Signal(str) # For status messages
    update_progress = Signal(int) # For progress percentage (0-100)
    update_finished = Signal(bool, str) # success (bool), message/error (str)
    
    def run(self):
        error_message = ""
        success = False
        try:
            import requests
            import subprocess
            import pkg_resources
            from packaging import version
            import os
            import sys
            import shutil
            from ytsage_yt_dlp import get_yt_dlp_path
            
            self.update_status.emit("🔍 Checking current installation...")
            self.update_progress.emit(10)
            
            # Get the yt-dlp path
            try:
                yt_dlp_path = get_yt_dlp_path()
                self.update_status.emit(f"📍 Found yt-dlp at: {os.path.basename(yt_dlp_path)}")
            except Exception as e:
                self.update_status.emit(f"❌ Error getting yt-dlp path: {e}")
                self.update_finished.emit(False, f"❌ Error getting yt-dlp path: {e}")
                return
            
            # Create startupinfo to hide console on Windows
            startupinfo = None
            if sys.platform == 'win32' and hasattr(subprocess, 'STARTUPINFO'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # SW_HIDE
            
            self.update_progress.emit(20)
            
            # Check if we're using an app-managed binary or system installation
            app_managed_dirs = [
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'YTSage', 'bin'),
                os.path.expanduser(os.path.join('~', 'Library', 'Application Support', 'YTSage', 'bin')),
                os.path.expanduser(os.path.join('~', '.local', 'share', 'YTSage', 'bin'))
            ]
            
            is_app_managed = any(os.path.dirname(yt_dlp_path) == dir_path for dir_path in app_managed_dirs)
            
            if is_app_managed:
                self.update_status.emit("📦 Updating app-managed yt-dlp binary...")
                success = self._update_binary(yt_dlp_path)
            else:
                self.update_status.emit("🐍 Updating system yt-dlp via pip...")
                success = self._update_via_pip(startupinfo)
            
            if success:
                self.update_progress.emit(100)
                error_message = "✅ yt-dlp has been successfully updated!"
            else:
                error_message = "❌ Failed to update yt-dlp. Please try again or check your internet connection."
                
        except requests.RequestException as e:
            error_message = f"❌ Network error during update: {str(e)}"
            self.update_status.emit(error_message)
            success = False
        except Exception as e:
            error_message = f"❌ Update failed: {str(e)}"
            self.update_status.emit(error_message)
            success = False
            
        self.update_finished.emit(success, error_message)
    
    def _update_binary(self, yt_dlp_path):
        """Update yt-dlp binary directly from GitHub releases."""
        try:
            self.update_status.emit("🌐 Determining download URL...")
            self.update_progress.emit(30)
            
            # Determine the URL based on OS
            if sys.platform == 'win32':
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
            elif sys.platform == 'darwin':
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
            else:
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
            
            self.update_status.emit("⬇️ Downloading latest yt-dlp binary...")
            self.update_progress.emit(40)
            
            # Download with progress tracking and timeout
            response = requests.get(url, stream=True, timeout=30)
            if response.status_code != 200:
                self.update_status.emit(f"❌ Download failed: HTTP {response.status_code}")
                return False
            
            total_size = int(response.headers.get('content-length', 0))
            temp_file = f"{yt_dlp_path}.new"
            downloaded = 0
            
            self.update_status.emit("💾 Downloading and saving binary...")
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Update progress (40-80% for download)
                        if total_size > 0:
                            progress = 40 + int((downloaded / total_size) * 40)
                            self.update_progress.emit(progress)
            
            self.update_status.emit("🔧 Installing updated binary...")
            self.update_progress.emit(85)
            
            # Make executable on Unix systems
            if sys.platform != 'win32':
                os.chmod(temp_file, 0o755)
            
            # Replace the old file with the new one
            try:
                # On Windows, we need to remove the old file first
                if sys.platform == 'win32' and os.path.exists(yt_dlp_path):
                    os.remove(yt_dlp_path)
                
                os.rename(temp_file, yt_dlp_path)
                self.update_status.emit("✅ Binary successfully updated!")
                self.update_progress.emit(95)
                return True
                
            except Exception as e:
                self.update_status.emit(f"❌ Error installing binary: {e}")
                # Clean up temp file if it exists
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                return False
                
        except requests.RequestException as e:
            self.update_status.emit(f"❌ Network error: {e}")
            return False
        except Exception as e:
            self.update_status.emit(f"❌ Binary update failed: {e}")
            return False
    
    def _update_via_pip(self, startupinfo):
        """Update yt-dlp via pip."""
        try:
            import pkg_resources
            
            self.update_status.emit("🔍 Checking current pip installation...")
            self.update_progress.emit(30)
            
            # Get current version
            try:
                current_version = pkg_resources.get_distribution("yt-dlp").version
                self.update_status.emit(f"📋 Current version: {current_version}")
            except pkg_resources.DistributionNotFound:
                self.update_status.emit("⚠️ yt-dlp not found via pip, attempting installation...")
                current_version = "0.0.0"
                
            self.update_progress.emit(40)
            
            # Get the latest version from PyPI
            self.update_status.emit("🌐 Checking for latest version...")
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
            
            if response.status_code != 200:
                self.update_status.emit("❌ Failed to check for updates")
                return False
                
            data = response.json()
            latest_version = data["info"]["version"]
            self.update_status.emit(f"🆕 Latest version: {latest_version}")
            self.update_progress.emit(50)
            
            # Compare versions
            from packaging import version
            if version.parse(latest_version) > version.parse(current_version):
                self.update_status.emit(f"⬆️ Updating from {current_version} to {latest_version}...")
                self.update_progress.emit(60)
                
                try:
                    # Run pip update with timeout
                    self.update_status.emit("📦 Running pip install --upgrade...")
                    update_result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=300,  # 5 minute timeout for pip install
                        startupinfo=startupinfo
                    )
                    
                    self.update_progress.emit(85)
                    
                    if update_result.returncode == 0:
                        self.update_status.emit("✅ Pip update completed successfully!")
                        self.update_progress.emit(95)
                        return True
                    else:
                        self.update_status.emit(f"❌ Pip update failed: {update_result.stderr}")
                        return False
                        
                except subprocess.TimeoutExpired:
                    self.update_status.emit("❌ Pip update timed out after 5 minutes")
                    return False
                except Exception as e:
                    self.update_status.emit(f"❌ Error during pip update: {e}")
                    return False
            else:
                self.update_status.emit("✅ yt-dlp is already up to date!")
                self.update_progress.emit(95)
                return True
                
        except Exception as e:
            self.update_status.emit(f"❌ Pip update failed: {e}")
            return False


class YTDLPUpdateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update yt-dlp")
        self.setMinimumWidth(450)
        self.setMinimumHeight(200)
        self._closing = False  # Flag to track if dialog is closing
        
        layout = QVBoxLayout(self)
        
        # Status label
        self.status_label = QLabel("Checking for updates...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(60)
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()  # Hide initially
        layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.perform_update)
        self.update_btn.setEnabled(False)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)
        
        # Style
        self.setStyleSheet("""
            QDialog {
                background-color: #15181b;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
                padding: 10px;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QProgressBar {
                border: 2px solid #1d1e22;
                border-radius: 6px;
                text-align: center;
                color: white;
                background-color: #1d1e22;
                height: 30px;
                font-weight: bold;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #e60000, stop: 0.5 #ff3333, stop: 1 #c90000);
                border-radius: 4px;
                margin: 1px;
            }
        """)
        
        # Start version check in background
        self.check_version()
    
    def check_version(self):
        self.status_label.setText("Checking for updates...")
        self.update_btn.setEnabled(False)
        self.version_check_thread = VersionCheckThread()
        self.version_check_thread.finished.connect(self.on_version_check_finished)
        self.version_check_thread.start()

    def on_version_check_finished(self, current_version, latest_version, error_message):
        # Check if dialog is closing to avoid unnecessary updates
        if hasattr(self, '_closing') and self._closing:
            return
            
        if error_message:
            self.status_label.setText(error_message)
            self.update_btn.setEnabled(False)
            return

        if not current_version or not latest_version:
             self.status_label.setText("Could not determine versions.")
             self.update_btn.setEnabled(False)
             return

        try:
            # Compare versions
            current_ver = version.parse(current_version)
            latest_ver = version.parse(latest_version)
            
            if current_ver < latest_ver:
                self.status_label.setText(f"Update available!\nCurrent version: {current_version}\nLatest version: {latest_version}")
                self.update_btn.setEnabled(True)
            else:
                self.status_label.setText(f"yt-dlp is up to date (version {current_version})")
                self.update_btn.setEnabled(False)
        except version.InvalidVersion:
            # If version parsing fails, do a simple string comparison
            if current_version != latest_version:
                self.status_label.setText(f"Update available! (Comparison failed)\nCurrent: {current_version}\nLatest: {latest_version}")
                self.update_btn.setEnabled(True)
            else:
                self.status_label.setText(f"yt-dlp is up to date (version {current_version})")
                self.update_btn.setEnabled(False)
        except Exception as e: # Catch any other unexpected errors during comparison
             self.status_label.setText(f"Error comparing versions: {e}")
             self.update_btn.setEnabled(False)

    def perform_update(self):
        # Immediate visual feedback
        self.update_btn.setEnabled(False)
        self.close_btn.setEnabled(False)
        self.update_btn.setText("Updating...")
        self.status_label.setText("🚀 Initializing update process...")
        
        # Show progress bar immediately
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        
        # Start the update thread immediately without processEvents()
        # The QTimer delay was unnecessary and could cause issues
        self._start_update_thread()
    
    def _start_update_thread(self):
        """Start the actual update thread after giving immediate feedback."""
        # Create and start the update thread
        self.update_thread = UpdateThread()
        self.update_thread.update_status.connect(self.on_update_status)
        self.update_thread.update_progress.connect(self.on_update_progress)
        self.update_thread.update_finished.connect(self.on_update_finished)
        self.update_thread.start()

    def on_update_status(self, message):
        """Slot to receive status messages from UpdateThread."""
        if not (hasattr(self, '_closing') and self._closing):
            self.status_label.setText(message)

    def on_update_progress(self, progress):
        """Slot to receive progress updates from UpdateThread."""
        if not (hasattr(self, '_closing') and self._closing):
            self.progress_bar.setValue(progress)

    def on_update_finished(self, success, message):
        """Slot called when the UpdateThread finishes."""
        # Check if dialog is closing to avoid unnecessary updates
        if hasattr(self, '_closing') and self._closing:
            return
            
        self.progress_bar.setValue(100)
        self.status_label.setText(message)
        self.close_btn.setEnabled(True)
        self.update_btn.setText("Update")  # Reset button text
        
        if success:
            # Show success briefly then auto-check version
            QTimer.singleShot(2000, self.check_version)  # Wait 2 seconds then refresh
        else:
            # Re-enable update button on failure after a short delay
            QTimer.singleShot(3000, lambda: self.update_btn.setEnabled(True) if not (hasattr(self, '_closing') and self._closing) else None)

    def closeEvent(self, event):
        """Ensure threads are terminated if the dialog is closed prematurely."""
        # Set a flag to indicate dialog is closing
        self._closing = True
        
        if hasattr(self, 'version_check_thread') and self.version_check_thread.isRunning():
            self.version_check_thread.quit()
            if not self.version_check_thread.wait(3000):  # Wait up to 3 seconds
                self.version_check_thread.terminate()
                
        if hasattr(self, 'update_thread') and self.update_thread.isRunning():
            self.update_thread.quit()
            if not self.update_thread.wait(5000):  # Wait up to 5 seconds for update to finish
                self.update_thread.terminate()
                
        super().closeEvent(event)

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent # Store parent to access version etc.
        self.setWindowTitle("About YTSage")
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title and Version
        title_label = QLabel("<h2 style='color: #c90000;'>YTSage</h2>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel(f"Version: {getattr(self.parent, 'version', 'N/A')}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #cccccc;")
        layout.addWidget(version_label)

        # Description
        description_label = QLabel("A simple GUI frontend for the powerful yt-dlp video downloader.")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("color: #ffffff; padding-top: 10px;")
        layout.addWidget(description_label)

        # Separator
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #1d1e22;")
        layout.addWidget(separator)

        # Information Section
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)

        # Author
        author_label = QLabel("Created by: <a href='https://github.com/oop7/' style='color: #c90000; text-decoration: none;'>oop7</a>")
        author_label.setOpenExternalLinks(True)
        info_layout.addWidget(author_label)

        # GitHub Repo
        repo_label = QLabel("GitHub: <a href='https://github.com/oop7/YTSage/' style='color: #c90000; text-decoration: none;'>github.com/oop7/YTSage</a>")
        repo_label.setOpenExternalLinks(True)
        info_layout.addWidget(repo_label)

        # Create version info container with refresh button
        version_container = QVBoxLayout()
        
        # Header with refresh button
        header_layout = QHBoxLayout()
        header_label = QLabel("<b>System Information</b>")
        header_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 4px 12px;
                background-color: #3d3d3d;
                border: 1px solid #555555;
                border-radius: 4px;
                color: white;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_version_info)
        header_layout.addWidget(self.refresh_btn)
        
        version_container.addLayout(header_layout)

        # Version information labels (stored as instance variables for updating)
        self.version_info_layout = QVBoxLayout()
        version_container.addLayout(self.version_info_layout)
        
        # Populate version information
        self.update_version_info()
        
        info_layout.addLayout(version_container)
        layout.addLayout(info_layout)

        # Close Button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        # Center the button box
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button_box)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Apply overall styling
        self.setStyleSheet("""
            QDialog { background-color: #15181b; color: #ffffff; }
            QLabel { color: #cccccc; }
            QPushButton {
                padding: 8px 25px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #a50000; }
        """)

    def update_version_info(self):
        """Update the version information display."""
        # Clear existing labels
        for i in reversed(range(self.version_info_layout.count())):
            child = self.version_info_layout.itemAt(i).widget()
            if child:
                child.deleteLater()

        # yt-dlp path and version
        yt_dlp_path = get_yt_dlp_path()
        yt_dlp_path_text = yt_dlp_path if yt_dlp_path else 'yt-dlp not found in PATH'
        yt_dlp_version = get_ytdlp_version()
        
        yt_dlp_label = QLabel(f"<b>yt-dlp Path:</b> {yt_dlp_path_text}")
        yt_dlp_label.setWordWrap(True)
        self.version_info_layout.addWidget(yt_dlp_label)
        
        # Add cache status for yt-dlp
        ytdlp_cache = _version_cache.get('ytdlp', {})
        last_check = ytdlp_cache.get('last_check', 0)
        cache_status = ""
        if last_check > 0:
            import time
            from datetime import datetime
            cache_time = datetime.fromtimestamp(last_check).strftime("%H:%M:%S")
            cache_status = f" <span style='color: #999999; font-size: 10px;'>(checked at {cache_time})</span>"
        
        yt_dlp_version_label = QLabel(f"<b>yt-dlp Version:</b> {yt_dlp_version}{cache_status}")
        yt_dlp_version_label.setWordWrap(True)
        self.version_info_layout.addWidget(yt_dlp_version_label)

        # FFmpeg Status and Version
        ffmpeg_found = check_ffmpeg()
        ffmpeg_status_text = "<span style='color: #00ff00;'>Detected</span>" if ffmpeg_found else "<span style='color: #ff5555;'>Not Detected</span>"
        ffmpeg_version = get_ffmpeg_version() if ffmpeg_found else "Not Available"
        
        ffmpeg_label = QLabel(f"<b>FFmpeg Status:</b> {ffmpeg_status_text}")
        self.version_info_layout.addWidget(ffmpeg_label)
        
        # Add cache status for FFmpeg
        ffmpeg_cache = _version_cache.get('ffmpeg', {})
        last_check = ffmpeg_cache.get('last_check', 0)
        cache_status = ""
        if last_check > 0 and ffmpeg_found:
            import time
            from datetime import datetime
            cache_time = datetime.fromtimestamp(last_check).strftime("%H:%M:%S")
            cache_status = f" <span style='color: #999999; font-size: 10px;'>(checked at {cache_time})</span>"
        
        ffmpeg_version_label = QLabel(f"<b>FFmpeg Version:</b> {ffmpeg_version}{cache_status}")
        ffmpeg_version_label.setWordWrap(True)
        self.version_info_layout.addWidget(ffmpeg_version_label)

    def refresh_version_info(self):
        """Refresh version information manually."""
        self.refresh_btn.setText("Refreshing...")
        self.refresh_btn.setEnabled(False)
        
        # Perform refresh in a separate thread to avoid blocking UI
        from PySide6.QtCore import QThread, Signal
        
        class RefreshThread(QThread):
            finished = Signal(bool)
            
            def run(self):
                success = refresh_version_cache(force=True)
                self.finished.emit(success)
        
        self.refresh_thread = RefreshThread()
        self.refresh_thread.finished.connect(self.on_refresh_finished)
        self.refresh_thread.start()
    
    def on_refresh_finished(self, success):
        """Handle refresh completion."""
        self.refresh_btn.setText("Refresh")
        self.refresh_btn.setEnabled(True)
        
        if success:
            self.update_version_info()
        else:
            # Show error message with proper styling
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Refresh Failed")
            msg_box.setText("Failed to refresh version information.")
            msg_box.setWindowIcon(self.windowIcon())
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #15181b;
                    color: #ffffff;
                }
                QMessageBox QLabel {
                    color: #ffffff;
                }
                QMessageBox QPushButton {
                    padding: 8px 15px;
                    background-color: #c90000;
                    border: none;
                    border-radius: 4px;
                    color: white;
                    font-weight: bold;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #a50000;
                }
            """)
            msg_box.exec()

# --- New Subtitle Selection Dialog ---
class SubtitleSelectionDialog(QDialog):
    def __init__(self, available_manual, available_auto, previously_selected, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Subtitles")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        self.available_manual = available_manual
        self.available_auto = available_auto
        self.previously_selected = set(previously_selected) # Use a set for quick lookups
        self.selected_subtitles = list(previously_selected) # Initialize with previous selection

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Filter input
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter languages (e.g., en, es)...")
        self.filter_input.textChanged.connect(self.filter_list)
        self.filter_input.setStyleSheet("""
            QLineEdit {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
                min-height: 30px;
                color: white;
            }
            QLineEdit:focus {
                border-color: #ff0000;
            }
        """)
        layout.addWidget(self.filter_input)

        # Scroll Area for the list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }") # Remove border around scroll area
        layout.addWidget(scroll_area)

        # Container widget for list items (needed for scroll area)
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(2) # Compact spacing
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Align items to top
        scroll_area.setWidget(self.list_container)

        # Populate the list initially
        self.populate_list()

        # OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Style the buttons
        for button in button_box.buttons():
             button.setStyleSheet("""
                 QPushButton {
                     background-color: #363636;
                     border: 2px solid #3d3d3d;
                     border-radius: 4px;
                     padding: 5px 15px; /* Adjust padding */
                     min-height: 30px; /* Ensure consistent height */
                     color: white;
                 }
                 QPushButton:hover {
                     background-color: #444444;
                 }
                 QPushButton:pressed {
                     background-color: #555555;
                 }
             """)
             # Style the OK button specifically if needed
             if button_box.buttonRole(button) == QDialogButtonBox.ButtonRole.AcceptRole:
                 button.setStyleSheet(button.styleSheet() + "QPushButton { background-color: #ff0000; border-color: #cc0000; } QPushButton:hover { background-color: #cc0000; }")


        layout.addWidget(button_box)

    def populate_list(self, filter_text=""):
        # Clear existing checkboxes from layout
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        filter_text = filter_text.lower()
        combined_subs = {}

        # Add manual subs
        for lang_code, sub_info in self.available_manual.items():
             if not filter_text or filter_text in lang_code.lower():
                 combined_subs[lang_code] = f"{lang_code} - Manual"

        # Add auto subs (only if no manual exists and matches filter)
        for lang_code, sub_info in self.available_auto.items():
            if lang_code not in combined_subs: # Don't overwrite manual
                 if not filter_text or filter_text in lang_code.lower():
                     combined_subs[lang_code] = f"{lang_code} - Auto-generated"

        if not combined_subs:
            no_subs_label = QLabel("No subtitles available" + (f" matching '{filter_text}'" if filter_text else ""))
            no_subs_label.setStyleSheet("color: #aaaaaa; padding: 10px;")
            self.list_layout.addWidget(no_subs_label)
            return

        # Sort by language code
        sorted_lang_codes = sorted(combined_subs.keys())

        for lang_code in sorted_lang_codes:
            item_text = combined_subs[lang_code]
            checkbox = QCheckBox(item_text)
            checkbox.setProperty("subtitle_id", item_text) # Store the identifier
            checkbox.setChecked(item_text in self.previously_selected) # Check if previously selected
            checkbox.stateChanged.connect(self.update_selection)
            checkbox.setStyleSheet("""
                 QCheckBox {
                     color: #ffffff;
                     padding: 5px;
                 }
                 QCheckBox::indicator {
                     width: 18px;
                     height: 18px;
                     border-radius: 4px; /* Square checkboxes */
                 }
                 QCheckBox::indicator:unchecked {
                     border: 2px solid #666666;
                     background: #2b2b2b;
                 }
                 QCheckBox::indicator:checked {
                     border: 2px solid #ff0000;
                     background: #ff0000;
                 }
             """)
            self.list_layout.addWidget(checkbox)

        self.list_layout.addStretch() # Pushes items up if list is short

    def filter_list(self):
        self.populate_list(self.filter_input.text())

    def update_selection(self, state):
        sender = self.sender()
        subtitle_id = sender.property("subtitle_id")
        if state == Qt.CheckState.Checked.value:
            if subtitle_id not in self.previously_selected:
                self.previously_selected.add(subtitle_id)
        else:
            if subtitle_id in self.previously_selected:
                self.previously_selected.remove(subtitle_id)

    def get_selected_subtitles(self):
        # Return the final set as a list
        return list(self.previously_selected)

    def accept(self):
        # Update the final list before closing
        self.selected_subtitles = self.get_selected_subtitles()
        super().accept()

# --- End Subtitle Selection Dialog ---


# --- Playlist Video Selection Dialog ---

class PlaylistSelectionDialog(QDialog):
    def __init__(self, playlist_entries, previously_selected_string, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Playlist Videos")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400) # Allow more vertical space

        self.playlist_entries = playlist_entries
        self.checkboxes = []

        # Main layout
        main_layout = QVBoxLayout(self)

        # Top buttons (Select/Deselect All)
        button_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        deselect_all_btn = QPushButton("Deselect All")
        select_all_btn.clicked.connect(self._select_all)
        deselect_all_btn.clicked.connect(self._deselect_all)
        # Style the buttons to match the subtitle dialog
        select_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px 15px;
                min-height: 30px;
                color: white;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        deselect_all_btn.setStyleSheet(select_all_btn.styleSheet())
        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(deselect_all_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Scrollable area for checkboxes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }") # Remove border around scroll area
        scroll_widget = QWidget()
        self.list_layout = QVBoxLayout(scroll_widget) # Layout for checkboxes
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(2) # Compact spacing
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Align items to top
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # Populate checkboxes
        self._populate_list(previously_selected_string)

        # Dialog buttons (OK/Cancel)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Style the buttons to match subtitle dialog
        for button in button_box.buttons():
            button.setStyleSheet("""
                QPushButton {
                    background-color: #363636;
                    border: 2px solid #3d3d3d;
                    border-radius: 4px;
                    padding: 5px 15px;
                    min-height: 30px;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
                QPushButton:pressed {
                    background-color: #555555;
                }
            """)
            # Style the OK button specifically if needed
            if button_box.buttonRole(button) == QDialogButtonBox.ButtonRole.AcceptRole:
                button.setStyleSheet(button.styleSheet() + "QPushButton { background-color: #ff0000; border-color: #cc0000; } QPushButton:hover { background-color: #cc0000; }")
        
        main_layout.addWidget(button_box)

        # Apply styling to match subtitle dialog
        self.setStyleSheet("""
            QDialog { background-color: #15181b; }
            QCheckBox {
                color: #ffffff;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #2b2b2b;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #ff0000;
                background: #ff0000;
            }
            QWidget { background-color: #15181b; }
        """)

    def _parse_selection_string(self, selection_string):
        """Parses a yt-dlp playlist selection string (e.g., '1-3,5,7-9') into a set of 1-based indices."""
        selected_indices = set()
        if not selection_string:
            # If no previous selection, assume all are selected initially
            return set(range(1, len(self.playlist_entries) + 1))
        
        parts = selection_string.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    if start <= end:
                        selected_indices.update(range(start, end + 1))
                except ValueError:
                    pass # Ignore invalid ranges
            else:
                try:
                    selected_indices.add(int(part))
                except ValueError:
                    pass # Ignore invalid numbers
        return selected_indices

    def _populate_list(self, previously_selected_string):
        """Populates the scroll area with checkboxes for each video."""
        selected_indices = self._parse_selection_string(previously_selected_string)
        
        # Clear existing checkboxes if any (e.g., if repopulating)
        while self.list_layout.count():
            child = self.list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.checkboxes.clear()

        for index, entry in enumerate(self.playlist_entries):
            if not entry: continue # Skip None entries if yt-dlp returns them

            video_index = index + 1 # yt-dlp uses 1-based indexing
            title = entry.get('title', f'Video {video_index}')
            # Shorten title if too long
            display_title = (title[:70] + '...') if len(title) > 73 else title
            
            checkbox = QCheckBox(f"{video_index}. {display_title}")
            checkbox.setChecked(video_index in selected_indices)
            checkbox.setProperty("video_index", video_index) # Store index
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: #ffffff;
                    padding: 5px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 4px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #666666;
                    background: #2b2b2b;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #ff0000;
                    background: #ff0000;
                }
            """)
            self.list_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)
        self.list_layout.addStretch() # Push checkboxes to the top

    def _select_all(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

    def _deselect_all(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def _condense_indices(self, indices):
        """Condenses a list of 1-based indices into a yt-dlp selection string."""
        if not indices:
            return ""
        indices = sorted(list(set(indices)))
        if not indices: # Check again after sorting/set conversion
            return ""
            
        ranges = []
        start = indices[0]
        end = indices[0]
        for i in range(1, len(indices)):
            if indices[i] == end + 1:
                end = indices[i]
            else:
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}-{end}")
                start = indices[i]
                end = indices[i]
        # Add the last range
        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{end}")
        return ",".join(ranges)

    def get_selected_items_string(self):
        """Returns the selection string based on checked boxes."""
        selected_indices = [
            cb.property("video_index") for cb in self.checkboxes if cb.isChecked()
        ]
        
        # Check if all items are selected
        if len(selected_indices) == len(self.playlist_entries):
             return None # yt-dlp default is all items, so return None or empty string

        return self._condense_indices(selected_indices)

    # Optional: Override accept to ensure the string is generated, although not strictly necessary
    # def accept(self):
    #     self._selected_string = self.get_selected_items_string()
    #     super().accept()

# --- End Playlist Video Selection Dialog ---

class CookieLoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Login with Cookies')
        self.setMinimumSize(400, 150)

        layout = QVBoxLayout(self)

        help_text = QLabel(
            "Select the Netscape-format cookies file for logging in.\n"
            "This allows downloading of private videos and premium quality audio."
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #999999; padding: 10px;")
        layout.addWidget(help_text)

        # File path input and browse button
        path_layout = QHBoxLayout()
        self.cookie_path_input = QLineEdit()
        self.cookie_path_input.setPlaceholderText("Path to cookies file (Netscape format)")
        path_layout.addWidget(self.cookie_path_input)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_cookie_file)
        path_layout.addWidget(self.browse_button)

        layout.addLayout(path_layout)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def browse_cookie_file(self):
        # Open file dialog to select cookie file
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Cookies files (*.txt *.lwp)") # Assuming common cookie file extensions
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.cookie_path_input.setText(selected_files[0])

    def get_cookie_file_path(self):
        # Return the selected cookie file path
        return self.cookie_path_input.text()

# === Renamed Dialog: Download Settings ===
class DownloadSettingsDialog(QDialog): # Renamed class
    def __init__(self, current_path, current_limit, current_unit_index, parent=None): # Added limit params
        super().__init__(parent)
        self.setWindowTitle("Download Settings") # Renamed window
        self.setMinimumWidth(450)
        self.setMinimumHeight(400)
        self.current_path = current_path
        self.current_limit = current_limit if current_limit is not None else "" # Handle None
        self.current_unit_index = current_unit_index

        # Apply main app styling
        self.setStyleSheet("""
            QDialog {
                background-color: #15181b;
                color: #ffffff;
            }
            QWidget {
                background-color: #15181b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #1b2021;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                background-color: #15181b;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
                color: #ffffff;
                selection-background-color: #c90000;
                selection-color: #ffffff;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QPushButton:pressed {
                background-color: #800000;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
            QCheckBox {
                spacing: 5px;
                color: #ffffff;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #15181b;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
            }
            QRadioButton {
                spacing: 5px;
                color: #ffffff;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #666666;
                background: #15181b;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
            }
            QComboBox {
                padding: 5px;
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
                color: #ffffff;
                min-height: 20px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #15181b;
                color: #ffffff;
                selection-background-color: #c90000;
                selection-color: #ffffff;
            }
        """)

        layout = QVBoxLayout(self)

        # --- Download Path Section ---
        path_group_box = QGroupBox("Download Path")
        path_layout = QVBoxLayout()

        self.path_display = QLabel(self.current_path)
        self.path_display.setWordWrap(True)
        self.path_display.setStyleSheet("QLabel { color: #ffffff; padding: 5px; border: 1px solid #1b2021; border-radius: 4px; background-color: #1b2021; }")
        path_layout.addWidget(self.path_display)

        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_new_path)
        path_layout.addWidget(browse_button)

        path_group_box.setLayout(path_layout)
        layout.addWidget(path_group_box)
        # --- End Path Section ---

        # --- Speed Limit Section ---
        speed_group_box = QGroupBox("Speed Limit")
        speed_layout = QHBoxLayout()

        self.speed_limit_input = QLineEdit(str(self.current_limit)) # Set initial value
        self.speed_limit_input.setPlaceholderText("None")
        speed_layout.addWidget(self.speed_limit_input)

        self.speed_limit_unit = QComboBox()
        self.speed_limit_unit.addItems(["KB/s", "MB/s"])
        self.speed_limit_unit.setCurrentIndex(self.current_unit_index) # Set initial unit
        speed_layout.addWidget(self.speed_limit_unit)

        speed_group_box.setLayout(speed_layout)
        layout.addWidget(speed_group_box)
        # --- End Speed Limit Section ---

        # --- Auto-Update yt-dlp Section ---
        auto_update_group_box = QGroupBox("Auto-Update yt-dlp")
        auto_update_layout = QVBoxLayout()

        # Load current auto-update settings
        from ytsage_utils import get_auto_update_settings
        auto_settings = get_auto_update_settings()

        # Enable/Disable auto-update checkbox
        self.auto_update_enabled = QCheckBox("Enable automatic yt-dlp updates")
        self.auto_update_enabled.setChecked(auto_settings['enabled'])
        auto_update_layout.addWidget(self.auto_update_enabled)

        # Frequency options
        frequency_label = QLabel("Update frequency:")
        frequency_label.setStyleSheet("color: #ffffff; margin-top: 10px;")
        auto_update_layout.addWidget(frequency_label)

        self.startup_radio = QRadioButton("Check on every startup (minimum 1 hour between checks)")
        self.daily_radio = QRadioButton("Check daily")
        self.weekly_radio = QRadioButton("Check weekly")

        # Set current selection based on saved settings
        current_frequency = auto_settings['frequency']
        if current_frequency == 'startup':
            self.startup_radio.setChecked(True)
        elif current_frequency == 'daily':
            self.daily_radio.setChecked(True)
        else:  # weekly
            self.weekly_radio.setChecked(True)

        auto_update_layout.addWidget(self.startup_radio)
        auto_update_layout.addWidget(self.daily_radio)
        auto_update_layout.addWidget(self.weekly_radio)

        # Test update button
        test_update_layout = QHBoxLayout()
        test_update_button = QPushButton("Check for Updates Now")
        test_update_button.clicked.connect(self.test_update_check)
        test_update_layout.addWidget(test_update_button)
        test_update_layout.addStretch()
        auto_update_layout.addLayout(test_update_layout)

        auto_update_group_box.setLayout(auto_update_layout)
        layout.addWidget(auto_update_group_box)
        # --- End Auto-Update Section ---

        # Dialog buttons (OK/Cancel)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def browse_new_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "Select Download Directory", self.current_path)
        if new_path:
            self.current_path = new_path
            self.path_display.setText(self.current_path)

    def get_selected_path(self):
        """Returns the confirmed path after the dialog is accepted."""
        return self.current_path

    def get_selected_speed_limit(self):
        """Returns the entered speed limit value (as string or None)."""
        limit_str = self.speed_limit_input.text().strip()
        if not limit_str:
            return None
        # Optional: Add validation to ensure it's a number
        try:
            float(limit_str) # Check if convertible to float
            return limit_str
        except ValueError:
            # Handle error? Or just return None? Returning None for simplicity.
            print("Invalid speed limit input in dialog")
            return None # Or raise an error / show message

    def get_selected_unit_index(self):
        """Returns the index of the selected speed limit unit."""
        return self.speed_limit_unit.currentIndex()

    def _create_styled_message_box(self, icon, title, text):
        """Create a styled QMessageBox that matches the app theme."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setWindowIcon(self.windowIcon())
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #15181b;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QMessageBox QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #a50000;
            }
            QMessageBox QPushButton:pressed {
                background-color: #800000;
            }
        """)
        return msg_box

    def test_update_check(self):
        """Test the update check functionality."""
        try:
            from ytsage_utils import get_ytdlp_version
            import requests
            
            # Get current version
            current_version = get_ytdlp_version()
            if "Error" in current_version:
                msg_box = self._create_styled_message_box(
                    QMessageBox.Warning,
                    "Update Check",
                    "Could not determine current yt-dlp version."
                )
                msg_box.exec()
                return
            
            # Get latest version from PyPI
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
            response.raise_for_status()
            latest_version = response.json()["info"]["version"]
            
            # Clean up version strings
            current_version = current_version.replace('_', '.')
            latest_version = latest_version.replace('_', '.')
            
            from packaging import version as version_parser
            if version_parser.parse(latest_version) > version_parser.parse(current_version):
                msg_box = self._create_styled_message_box(
                    QMessageBox.Information,
                    "Update Check",
                    f"Update available!\n\nCurrent: {current_version}\nLatest: {latest_version}\n\nUse the 'Update yt-dlp' button in the main window to update."
                )
                msg_box.exec()
            else:
                msg_box = self._create_styled_message_box(
                    QMessageBox.Information,
                    "Update Check",
                    f"yt-dlp is up to date!\n\nCurrent version: {current_version}"
                )
                msg_box.exec()
        except Exception as e:
            msg_box = self._create_styled_message_box(
                QMessageBox.Warning,
                "Update Check",
                f"Error checking for updates: {str(e)}"
            )
            msg_box.exec()

    def get_auto_update_settings(self):
        """Returns the auto-update settings from the dialog."""
        enabled = self.auto_update_enabled.isChecked()
        
        if self.startup_radio.isChecked():
            frequency = 'startup'
        elif self.daily_radio.isChecked():
            frequency = 'daily'
        else:  # weekly_radio is checked
            frequency = 'weekly'
            
        return enabled, frequency

    def accept(self):
        """Override accept to save auto-update settings."""
        try:
            # Save auto-update settings
            enabled, frequency = self.get_auto_update_settings()
            from ytsage_utils import update_auto_update_settings
            
            if update_auto_update_settings(enabled, frequency):
                QMessageBox.information(self, "Settings Saved",
                                      "Auto-update settings have been saved successfully!")
            else:
                QMessageBox.warning(self, "Error",
                                  "Failed to save auto-update settings.")
        except Exception as e:
            QMessageBox.critical(self, "Error",
                               f"Error saving auto-update settings: {str(e)}")
        
        # Call the parent accept method to close the dialog
        super().accept()

# === New CustomOptions Dialog combining Cookies and Custom Commands ===
class CustomOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle('Custom Options')
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout(self)
        
        # Create tab widget to organize content
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # === Cookies Tab ===
        cookies_tab = QWidget()
        cookies_layout = QVBoxLayout(cookies_tab)
        
        # Help text
        help_text = QLabel(
            "Select the Netscape-format cookies file for logging in.\n"
            "This allows downloading of private videos and premium quality audio."
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #999999; padding: 10px;")
        cookies_layout.addWidget(help_text)

        # File path input and browse button
        path_layout = QHBoxLayout()
        self.cookie_path_input = QLineEdit()
        self.cookie_path_input.setPlaceholderText("Path to cookies file (Netscape format)")
        if hasattr(parent, 'cookie_file_path') and parent.cookie_file_path:
            self.cookie_path_input.setText(parent.cookie_file_path)
        path_layout.addWidget(self.cookie_path_input)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_cookie_file)
        path_layout.addWidget(self.browse_button)
        cookies_layout.addLayout(path_layout)  # Add the horizontal layout to cookies layout
        
        # Status indicator for cookies
        self.cookie_status = QLabel("")
        self.cookie_status.setStyleSheet("color: #999999; font-style: italic;")
        cookies_layout.addWidget(self.cookie_status)
        
        cookies_layout.addStretch()
        
        # === Custom Command Tab ===
        command_tab = QWidget()
        command_layout = QVBoxLayout(command_tab)
        
        # Help text
        cmd_help_text = QLabel(
            "Enter custom yt-dlp commands below. The URL will be automatically appended.\n"
            "Example: --extract-audio --audio-format mp3 --audio-quality 0\n"
            "Note: Download path and output template will be preserved."
        )
        cmd_help_text.setWordWrap(True)
        cmd_help_text.setStyleSheet("color: #999999; padding: 10px;")
        command_layout.addWidget(cmd_help_text)

        # Add SponsorBlock checkbox
        self.sponsorblock_checkbox = QCheckBox("Remove Sponsor Segments")
        self.sponsorblock_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 0px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #1d1e22;
                border-radius: 9px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
                border-radius: 9px;
            }
        """)
        command_layout.addWidget(self.sponsorblock_checkbox)

        # Command input
        self.command_input = QPlainTextEdit()
        self.command_input.setPlaceholderText("Enter yt-dlp arguments...")
        self.command_input.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1d1e22;
                color: #ffffff;
                border: 2px solid #1d1e22;
                border-radius: 4px;
                padding: 8px;
                font-family: Consolas, monospace;
            }
        """)
        command_layout.addWidget(self.command_input)

        # Run command button
        self.run_btn = QPushButton("Run Command")
        self.run_btn.clicked.connect(self.run_custom_command)
        command_layout.addWidget(self.run_btn)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background-color: #1d1e22;
                color: #ffffff;
                border: 2px solid #1d1e22;
                border-radius: 4px;
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        command_layout.addWidget(self.log_output)
        
        # Add tabs to the tab widget
        self.tab_widget.addTab(cookies_tab, "Login with Cookies")
        self.tab_widget.addTab(command_tab, "Custom Command")
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Apply global styles
        self.setStyleSheet("""
            QDialog {
                background-color: #15181b;
            }
            QTabWidget::pane { 
                border: 1px solid #3d3d3d;
                background-color: #15181b;
            }
            QTabBar::tab {
                background-color: #1d1e22;
                color: #ffffff;
                padding: 8px 12px;
                border: 1px solid #3d3d3d;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #c90000;
            }
            QTabBar::tab:hover:!selected {
                background-color: #2a2d36;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
                color: #ffffff;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
        """)

    def browse_cookie_file(self):
        # Open file dialog to select cookie file
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Cookies files (*.txt *.lwp)") # Assuming common cookie file extensions
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.cookie_path_input.setText(selected_files[0])
                self.cookie_status.setText("Cookie file selected - Click OK to apply")
                self.cookie_status.setStyleSheet("color: #00cc00; font-style: italic;")

    def get_cookie_file_path(self):
        # Return the selected cookie file path if it's not empty
        path = self.cookie_path_input.text().strip()
        if path and os.path.exists(path):
            return path
        return None

    def run_custom_command(self):
        url = self.parent.url_input.text().strip()
        if not url:
            self.log_output.append("Error: No URL provided")
            return

        command = self.command_input.toPlainText().strip()
        
        # Get download path from parent
        path = self.parent.last_path

        self.log_output.clear()
        self.log_output.append(f"Running command with URL: {url}")
        self.run_btn.setEnabled(False)

        # Start command in thread
        import threading
        threading.Thread(target=self._run_command_thread,
                        args=(command, url, path),
                        daemon=True).start()

    def _run_command_thread(self, command, url, path):
        try:
            class CommandLogger:
                def debug(self, msg):
                    from PySide6.QtCore import QMetaObject, Qt, Q_ARG
                    QMetaObject.invokeMethod(
                        self.dialog.log_output, "append", Qt.ConnectionType.QueuedConnection,
                        Q_ARG(str, msg)
                    )
                def warning(self, msg):
                    from PySide6.QtCore import QMetaObject, Qt, Q_ARG
                    QMetaObject.invokeMethod(
                        self.dialog.log_output, "append", Qt.ConnectionType.QueuedConnection,
                        Q_ARG(str, f"Warning: {msg}")
                    )
                def error(self, msg):
                    from PySide6.QtCore import QMetaObject, Qt, Q_ARG
                    QMetaObject.invokeMethod(
                        self.dialog.log_output, "append", Qt.ConnectionType.QueuedConnection,
                        Q_ARG(str, f"Error: {msg}")
                    )
                def __init__(self, dialog):
                    self.dialog = dialog

            # Split command into arguments
            args = command.split()

            # Base options
            ydl_opts = {
                'logger': CommandLogger(self),
                'paths': {'home': path},
                'debug_printout': True,
                'postprocessors': []
            }

            # Add SponsorBlock if selected
            if self.sponsorblock_checkbox.isChecked():
                ydl_opts['postprocessors'].append({
                    'key': 'SponsorBlock',
                    'categories': ['sponsor', 'intro', 'outro', 'selfpromo', 'preview', 'filler']
                })

            # Parse additional options
            yt_dlp_path = get_yt_dlp_path()
            base_cmd = [yt_dlp_path] + args + [url]

            # Show the full command
            from PySide6.QtCore import QMetaObject, Qt, Q_ARG
            QMetaObject.invokeMethod(
                self.log_output, "append", Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, f"Full command: {' '.join(base_cmd)}")
            )

            # Run the command
            proc = subprocess.Popen(
                base_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            # Stream output
            for line in proc.stdout:
                QMetaObject.invokeMethod(
                    self.log_output, "append", Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, line.rstrip())
                )

            ret = proc.wait()
            if ret != 0:
                QMetaObject.invokeMethod(
                    self.log_output, "append", Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, f"Command exited with code {ret}")
                )
            else:
                QMetaObject.invokeMethod(
                    self.log_output, "append", Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, "Command completed successfully")
                )
        except Exception as e:
            from PySide6.QtCore import QMetaObject, Qt, Q_ARG
            QMetaObject.invokeMethod(
                self.log_output, "append", Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, f"Error: {str(e)}")
            )
        finally:
            # Re-enable the run button
            QMetaObject.invokeMethod(
                self.run_btn, "setEnabled", Qt.ConnectionType.QueuedConnection,
                Q_ARG(bool, True)
            )

# === Time Range Selection Dialog ===
class TimeRangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle('Download Video Section')
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Help text explaining the feature
        help_text = QLabel(
            "Download only specific parts of a video by specifying time ranges.\n"
            "Use HH:MM:SS format or seconds. Leave start or end empty to download from beginning or to end."
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #999999; padding: 10px;")
        layout.addWidget(help_text)
        
        # Time range section
        time_group = QGroupBox("Time Range")
        time_layout = QVBoxLayout()
        
        # Start time row
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Start Time:"))
        self.start_time_input = QLineEdit()
        self.start_time_input.setPlaceholderText("00:00:00 (or leave empty for start)")
        start_layout.addWidget(self.start_time_input)
        time_layout.addLayout(start_layout)
        
        # End time row
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("End Time:"))
        self.end_time_input = QLineEdit()
        self.end_time_input.setPlaceholderText("00:10:00 (or leave empty for end)")
        end_layout.addWidget(self.end_time_input)
        time_layout.addLayout(end_layout)
        
        time_group.setLayout(time_layout)
        layout.addWidget(time_group)
        
        # Force keyframes option
        self.force_keyframes = QCheckBox("Force keyframes at cuts (better accuracy, slower)")
        self.force_keyframes.setChecked(True)
        self.force_keyframes.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #1d1e22;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.force_keyframes)
        
        # Format preview
        preview_group = QGroupBox("Command Preview")
        preview_layout = QVBoxLayout()
        self.preview_label = QLabel("--download-sections \"*-\"")
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #1d1e22;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
                font-family: Consolas, monospace;
            }
        """)
        preview_layout.addWidget(self.preview_label)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # Connect signals for live preview updates
        self.start_time_input.textChanged.connect(self.update_preview)
        self.end_time_input.textChanged.connect(self.update_preview)
        self.force_keyframes.stateChanged.connect(self.update_preview)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Apply styling
        self.setStyleSheet("""
            QDialog {
                background-color: #15181b;
            }
            QGroupBox {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 1.5ex;
                color: #ffffff;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
                color: #ffffff;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
        """)
        
        # Initialize preview
        self.update_preview()
    
    def update_preview(self):
        start = self.start_time_input.text().strip()
        end = self.end_time_input.text().strip()
        
        if start and end:
            time_range = f"*{start}-{end}"
        elif start:
            time_range = f"*{start}-"
        elif end:
            time_range = f"*-{end}"
        else:
            time_range = "*-"  # Full video
            
        preview = f"--download-sections \"{time_range}\""
        if self.force_keyframes.isChecked():
            preview += " --force-keyframes-at-cuts"
            
        self.preview_label.setText(preview)
    
    def get_download_sections(self):
        """Returns the download sections command arguments or None if no selection made"""
        start = self.start_time_input.text().strip()
        end = self.end_time_input.text().strip()
        
        if not start and not end:
            return None  # No selection made
            
        if start and end:
            time_range = f"*{start}-{end}"
        elif start:
            time_range = f"*{start}-"
        elif end:
            time_range = f"*-{end}"
        else:
            return None  # Shouldn't happen but just in case
            
        return time_range
        
    def get_force_keyframes(self):
        """Returns whether to force keyframes at cuts"""
        return self.force_keyframes.isChecked()

# === Auto-Update Settings Dialog ===

class AutoUpdateSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Auto-Update Settings")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        # Set the window icon to match the main app
        if parent:
            self.setWindowIcon(parent.windowIcon())
        
        self.init_ui()
        self.load_current_settings()
        self.apply_styling()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("<h2>🔄 Auto-Update Settings</h2>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Configure automatic updates for yt-dlp to ensure you always have the latest features and bug fixes.")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #cccccc; margin: 10px; font-size: 11px;")
        layout.addWidget(desc_label)
        
        # Enable/Disable auto-update
        self.enable_checkbox = QCheckBox("Enable automatic yt-dlp updates")
        self.enable_checkbox.setChecked(True)  # Default enabled
        self.enable_checkbox.toggled.connect(self.on_enable_toggled)
        layout.addWidget(self.enable_checkbox)
        
        # Frequency options
        frequency_group = QGroupBox("Update Frequency")
        frequency_layout = QVBoxLayout()
        
        self.frequency_group = QButtonGroup(self)
        
        self.startup_radio = QRadioButton("Check on every startup (minimum 1 hour between checks)")
        self.daily_radio = QRadioButton("Check daily")
        self.weekly_radio = QRadioButton("Check weekly")
        
        self.daily_radio.setChecked(True)  # Default to daily
        
        self.frequency_group.addButton(self.startup_radio, 0)
        self.frequency_group.addButton(self.daily_radio, 1)
        self.frequency_group.addButton(self.weekly_radio, 2)
        
        frequency_layout.addWidget(self.startup_radio)
        frequency_layout.addWidget(self.daily_radio)
        frequency_layout.addWidget(self.weekly_radio)
        frequency_group.setLayout(frequency_layout)
        
        layout.addWidget(frequency_group)
        
        # Current status
        status_group = QGroupBox("Current Status")
        status_layout = QVBoxLayout()
        
        self.current_version_label = QLabel("Current yt-dlp version: Checking...")
        self.last_check_label = QLabel("Last update check: Never")
        self.next_check_label = QLabel("Next check: Based on settings")
        
        status_layout.addWidget(self.current_version_label)
        status_layout.addWidget(self.last_check_label)
        status_layout.addWidget(self.next_check_label)
        status_group.setLayout(status_layout)
        
        layout.addWidget(status_group)
        
        # Manual check button
        self.manual_check_btn = QPushButton("🔍 Check for Updates Now")
        self.manual_check_btn.clicked.connect(self.manual_check)
        layout.addWidget(self.manual_check_btn)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
    def apply_styling(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #15181b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #1b2021;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                background-color: #15181b;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QCheckBox, QRadioButton {
                color: #ffffff;
                spacing: 5px;
                margin: 5px;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                border: 2px solid #666666;
                background: #15181b;
            }
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                margin: 5px;
                min-width: 100px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QPushButton:pressed {
                background-color: #800000;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
        """)
        
    def load_current_settings(self):
        """Load current auto-update settings from config."""
        try:
            from ytsage_utils import get_auto_update_settings, get_ytdlp_version
            import time
            from datetime import datetime
            
            settings = get_auto_update_settings()
            
            # Set checkbox
            self.enable_checkbox.setChecked(settings['enabled'])
            
            # Set frequency
            frequency = settings['frequency']
            if frequency == 'startup':
                self.startup_radio.setChecked(True)
            elif frequency == 'weekly':
                self.weekly_radio.setChecked(True)
            else:  # daily
                self.daily_radio.setChecked(True)

            # Update status labels
            current_version = get_ytdlp_version()
            self.current_version_label.setText(f"Current yt-dlp version: {current_version}")
            
            last_check = settings['last_check']
            if last_check > 0:
                last_check_time = datetime.fromtimestamp(last_check).strftime("%Y-%m-%d %H:%M:%S")
                self.last_check_label.setText(f"Last update check: {last_check_time}")
            else:
                self.last_check_label.setText("Last update check: Never")
            
            # Calculate next check time
            self.update_next_check_label()
            
            # Update UI state
            self.on_enable_toggled(settings['enabled'])
            
        except Exception as e:
            print(f"Error loading auto-update settings: {e}")
            
    def update_next_check_label(self):
        """Update the next check label based on current settings."""
        try:
            if not self.enable_checkbox.isChecked():
                self.next_check_label.setText("Next check: Disabled")
                return
                
            from ytsage_utils import get_auto_update_settings
            import time
            from datetime import datetime, timedelta
            
            settings = get_auto_update_settings()
            last_check = settings['last_check']
            frequency = self.get_selected_frequency()
            
            if last_check == 0:
                self.next_check_label.setText("Next check: On next startup")
                return
            
            next_check_time = last_check
            if frequency == 'startup':
                next_check_time += 3600  # 1 hour
            elif frequency == 'daily':
                next_check_time += 86400  # 24 hours  
            elif frequency == 'weekly':
                next_check_time += 604800  # 7 days
                
            current_time = time.time()
            if next_check_time <= current_time:
                self.next_check_label.setText("Next check: Now (overdue)")
            else:
                next_check_datetime = datetime.fromtimestamp(next_check_time)
                self.next_check_label.setText(f"Next check: {next_check_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
                
        except Exception as e:
            self.next_check_label.setText("Next check: Error calculating")
            print(f"Error calculating next check time: {e}")
    
    def on_enable_toggled(self, enabled):
        """Handle enable/disable checkbox toggle."""
        # Enable/disable frequency options
        for i in range(self.frequency_group.buttons().__len__()):
            self.frequency_group.button(i).setEnabled(enabled)
            
        self.update_next_check_label()
        
    def get_selected_frequency(self):
        """Get the selected frequency setting."""
        if self.startup_radio.isChecked():
            return 'startup'
        elif self.weekly_radio.isChecked():
            return 'weekly'
        else:
            return 'daily'
    
    def manual_check(self):
        """Perform a manual update check."""
        self.manual_check_btn.setEnabled(False)
        self.manual_check_btn.setText("🔄 Checking...")
        
        # Force an immediate update check
        def check_in_thread():
            try:
                from ytsage_utils import check_and_update_ytdlp_auto
                result = check_and_update_ytdlp_auto()
                
                # Update UI in main thread
                QTimer.singleShot(0, lambda: self.manual_check_finished(result))
            except Exception as e:
                print(f"Error during manual check: {e}")
                QTimer.singleShot(0, lambda: self.manual_check_finished(False))
        
        # Run in separate thread to avoid blocking UI
        import threading
        threading.Thread(target=check_in_thread, daemon=True).start()
        
    def _create_styled_message_box(self, icon, title, text):
        """Create a styled QMessageBox that matches the app theme."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setWindowIcon(self.windowIcon())
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #15181b;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QMessageBox QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #a50000;
            }
            QMessageBox QPushButton:pressed {
                background-color: #800000;
            }
        """)
        return msg_box
        
    def manual_check_finished(self, success):
        """Handle completion of manual update check."""
        self.manual_check_btn.setEnabled(True)
        self.manual_check_btn.setText("🔍 Check for Updates Now")
        
        if success:
            msg_box = self._create_styled_message_box(
                QMessageBox.Information, 
                "Update Check",
                "✅ Update check completed successfully!\nCheck the console for details."
            )
            msg_box.exec()
        else:
            msg_box = self._create_styled_message_box(
                QMessageBox.Warning,
                "Update Check", 
                "❌ Update check failed.\nCheck the console for error details."
            )
            msg_box.exec()
        
        # Refresh the current settings display
        self.load_current_settings()
        
    def save_settings(self):
        """Save the auto-update settings."""
        try:
            from ytsage_utils import update_auto_update_settings
            
            enabled = self.enable_checkbox.isChecked()
            frequency = self.get_selected_frequency()
            
            if update_auto_update_settings(enabled, frequency):
                msg_box = self._create_styled_message_box(
                    QMessageBox.Information,
                    "Settings Saved",
                    "✅ Auto-update settings have been saved successfully!"
                )
                msg_box.exec()
                self.accept()
            else:
                msg_box = self._create_styled_message_box(
                    QMessageBox.Warning,
                    "Error",
                    "❌ Failed to save auto-update settings.\nPlease try again."
                )
                msg_box.exec()
        except Exception as e:
            print(f"Error saving auto-update settings: {e}")
            msg_box = self._create_styled_message_box(
                QMessageBox.Critical,
                "Error",
                f"❌ Error saving settings: {str(e)}"
            )
            msg_box.exec()

# --- New AutoUpdateThread class ---
class AutoUpdateThread(QThread):
    """Thread for performing automatic background updates without UI feedback."""
    update_finished = Signal(bool, str)  # success (bool), message (str)
    
    def run(self):
        """Perform automatic yt-dlp update check and update if needed."""
        try:
            print("AutoUpdateThread: Performing automatic yt-dlp update check...")
            
            # Import required modules
            import requests
            import time
            from packaging import version as version_parser
            from ytsage_utils import get_ytdlp_version, load_config, save_config
            from ytsage_yt_dlp import get_yt_dlp_path
            
            # Get current version
            current_version = get_ytdlp_version()
            if "Error" in current_version:
                print("AutoUpdateThread: Could not determine current yt-dlp version, skipping auto-update")
                self.update_finished.emit(False, "Could not determine current yt-dlp version")
                return
            
            # Get latest version from PyPI
            try:
                response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
                response.raise_for_status()
                latest_version = response.json()["info"]["version"]
                
                # Clean up version strings
                current_version = current_version.replace('_', '.')
                latest_version = latest_version.replace('_', '.')
                
                print(f"AutoUpdateThread: Current yt-dlp version: {current_version}")
                print(f"AutoUpdateThread: Latest yt-dlp version: {latest_version}")
                
                # Compare versions
                if version_parser.parse(latest_version) > version_parser.parse(current_version):
                    print(f"AutoUpdateThread: Auto-updating yt-dlp from {current_version} to {latest_version}...")
                    
                    # Perform the update using the same logic as the manual update
                    success = self._perform_update()
                    
                    if success:
                        print("AutoUpdateThread: Auto-update completed successfully!")
                        # Update the last check timestamp
                        config = load_config()
                        config['last_update_check'] = time.time()
                        save_config(config)
                        self.update_finished.emit(True, f"Successfully updated yt-dlp from {current_version} to {latest_version}")
                    else:
                        print("AutoUpdateThread: Auto-update failed")
                        self.update_finished.emit(False, "Auto-update failed")
                else:
                    print("AutoUpdateThread: yt-dlp is already up to date")
                    # Still update the timestamp even if no update was needed
                    config = load_config()
                    config['last_update_check'] = time.time()
                    save_config(config)
                    self.update_finished.emit(True, f"yt-dlp is already up to date (version {current_version})")
                    
            except requests.RequestException as e:
                print(f"AutoUpdateThread: Network error during auto-update check: {e}")
                self.update_finished.emit(False, f"Network error: {e}")
            except Exception as e:
                print(f"AutoUpdateThread: Error during auto-update check: {e}")
                self.update_finished.emit(False, f"Update check error: {e}")
                
        except Exception as e:
            print(f"AutoUpdateThread: Critical error in auto-update: {e}")
            self.update_finished.emit(False, f"Critical error: {e}")
    
    def _perform_update(self):
        """Perform the actual update using similar logic to UpdateThread but without UI feedback."""
        try:
            import os
            import sys
            import requests
            import subprocess
            from ytsage_yt_dlp import get_yt_dlp_path
            
            # Get the yt-dlp path
            yt_dlp_path = get_yt_dlp_path()
            
            # Check if we're using an app-managed binary or system installation
            app_managed_dirs = [
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'YTSage', 'bin'),
                os.path.expanduser(os.path.join('~', 'Library', 'Application Support', 'YTSage', 'bin')),
                os.path.expanduser(os.path.join('~', '.local', 'share', 'YTSage', 'bin'))
            ]
            
            is_app_managed = any(os.path.dirname(yt_dlp_path) == dir_path for dir_path in app_managed_dirs)
            
            if is_app_managed:
                print("AutoUpdateThread: Updating app-managed yt-dlp binary...")
                return self._update_binary(yt_dlp_path)
            else:
                print("AutoUpdateThread: Updating system yt-dlp via pip...")
                return self._update_via_pip()
                
        except Exception as e:
            print(f"AutoUpdateThread: Error in _perform_update: {e}")
            return False
    
    def _update_binary(self, yt_dlp_path):
        """Update yt-dlp binary directly from GitHub releases (silent version)."""
        try:
            import os
            import sys
            import requests
            
            # Determine the URL based on OS
            if sys.platform == 'win32':
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
            elif sys.platform == 'darwin':
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
            else:
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
            
            print("AutoUpdateThread: Downloading latest yt-dlp binary...")
            
            # Download without progress tracking (silent)
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                print(f"AutoUpdateThread: Download failed: HTTP {response.status_code}")
                return False
            
            temp_file = f"{yt_dlp_path}.new"
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print("AutoUpdateThread: Installing updated binary...")
            
            # Make executable on Unix systems
            if sys.platform != 'win32':
                os.chmod(temp_file, 0o755)
            
            # Replace the old file with the new one
            try:
                # On Windows, we need to remove the old file first
                if sys.platform == 'win32' and os.path.exists(yt_dlp_path):
                    os.remove(yt_dlp_path)
                
                os.rename(temp_file, yt_dlp_path)
                print("AutoUpdateThread: Binary successfully updated!")
                return True
                
            except Exception as e:
                print(f"AutoUpdateThread: Error installing binary: {e}")
                # Clean up temp file if it exists
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                return False
                
        except Exception as e:
            print(f"AutoUpdateThread: Binary update failed: {e}")
            return False
    
    def _update_via_pip(self):
        """Update yt-dlp via pip (silent version)."""
        try:
            import subprocess
            import sys
            import pkg_resources
            import requests
            from packaging import version
            
            print("AutoUpdateThread: Checking current pip installation...")
            
            # Get current version
            try:
                current_version = pkg_resources.get_distribution("yt-dlp").version
                print(f"AutoUpdateThread: Current version: {current_version}")
            except pkg_resources.DistributionNotFound:
                print("AutoUpdateThread: yt-dlp not found via pip, attempting installation...")
                current_version = "0.0.0"
            
            # Get the latest version from PyPI
            print("AutoUpdateThread: Checking for latest version...")
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
            
            if response.status_code != 200:
                print("AutoUpdateThread: Failed to check for updates")
                return False
                
            data = response.json()
            latest_version = data["info"]["version"]
            print(f"AutoUpdateThread: Latest version: {latest_version}")
            
            # Compare versions
            if version.parse(latest_version) > version.parse(current_version):
                print(f"AutoUpdateThread: Updating from {current_version} to {latest_version}...")
                
                # Create startupinfo to hide console on Windows
                startupinfo = None
                if sys.platform == 'win32' and hasattr(subprocess, 'STARTUPINFO'):
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = 0  # SW_HIDE
                
                # Run pip update
                print("AutoUpdateThread: Running pip install --upgrade...")
                update_result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                    capture_output=True,
                    text=True,
                    check=False,
                    startupinfo=startupinfo
                )
                
                if update_result.returncode == 0:
                    print("AutoUpdateThread: Pip update completed successfully!")
                    return True
                else:
                    print(f"AutoUpdateThread: Pip update failed: {update_result.stderr}")
                    return False
            else:
                print("AutoUpdateThread: yt-dlp is already up to date!")
                return True
                
        except Exception as e:
            print(f"AutoUpdateThread: Pip update failed: {e}")
            return False