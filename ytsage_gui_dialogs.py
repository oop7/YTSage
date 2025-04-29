import sys
import os
import webbrowser
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QProgressBar, QLabel, QFileDialog,
                            QHeaderView, QStyle, QStyleFactory, QComboBox, QTextEdit, QDialog, QPlainTextEdit, QCheckBox, QButtonGroup)
from PySide6.QtCore import Qt, Signal, QObject, QThread, QProcess
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
import yt_dlp
from ytsage_ffmpeg import auto_install_ffmpeg, check_ffmpeg_installed

from ytsage_utils import check_ffmpeg, get_yt_dlp_path, load_saved_path, save_path # Import utility functions


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
                background-color: #363636;
                color: #ffffff;
                border: 2px solid #3d3d3d;
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
                border-radius: 9px;  /* Make indicator round */
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #2b2b2b;
                border-radius: 9px;  /* Make indicator round */
            }
            QCheckBox::indicator:checked {
                border: 2px solid #ff0000;
                background: #ff0000;
                border-radius: 9px;  /* Make indicator round */
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
                background-color: #2b2b2b;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.log_output)

        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
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

class YTDLPUpdateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update yt-dlp")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Status label
        self.status_label = QLabel("Checking for updates...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
                padding: 10px;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
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
                background-color: #cc0000;
            }
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                color: white;
                background-color: #363636;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #ff0000;
                border-radius: 2px;
            }
        """)
        
        # Start version check
        self.check_version()
    
    def check_version(self):
        try:
            # Get current version using yt-dlp command
            import subprocess
            import sys
            import os
            
            # Get the yt-dlp executable path
            if getattr(sys, 'frozen', False):
                if sys.platform == 'win32':
                    yt_dlp_path = os.path.join(os.path.dirname(sys.executable), 'yt-dlp.exe')
                else:
                    yt_dlp_path = os.path.join(os.path.dirname(sys.executable), 'yt-dlp')
            else:
                yt_dlp_path = 'yt-dlp'
            
            # Get current version
            try:
                result = subprocess.run([yt_dlp_path, '--version'], 
                                     capture_output=True, 
                                     text=True)
                current_version = result.stdout.strip()
            except Exception:
                import yt_dlp
                current_version = yt_dlp.version.__version__
            
            # Get latest version from PyPI
            import requests
            response = requests.get("https://pypi.org/pypi/yt-dlp/json")
            latest_version = response.json()["info"]["version"]
            
            # Clean up version strings
            current_version = current_version.replace('_', '.')
            latest_version = latest_version.replace('_', '.')
            
            # Compare versions
            from packaging import version
            try:
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
                    self.status_label.setText(f"Update available!\nCurrent version: {current_version}\nLatest version: {latest_version}")
                    self.update_btn.setEnabled(True)
                else:
                    self.status_label.setText(f"yt-dlp is up to date (version {current_version})")
                    self.update_btn.setEnabled(False)
                    
        except Exception as e:
            self.status_label.setText(f"Error checking version: {str(e)}")
            self.update_btn.setEnabled(False)
    
    def perform_update(self):
        try:
            self.update_btn.setEnabled(False)
            self.close_btn.setEnabled(False)
            self.status_label.setText("Updating yt-dlp...")
            self.progress_bar.setRange(0, 0)
            self.progress_bar.show()
            
            # Get the yt-dlp path
            if getattr(sys, 'frozen', False):
                if sys.platform == 'win32':
                    yt_dlp_path = os.path.join(os.path.dirname(sys.executable), 'yt-dlp.exe')
                else:
                    yt_dlp_path = os.path.join(os.path.dirname(sys.executable), 'yt-dlp')
            else:
                yt_dlp_path = 'yt-dlp'
            
            # Create a QProcess for updating
            process = QProcess()
            process.setWorkingDirectory(os.path.dirname(yt_dlp_path))
            
            if sys.platform == 'win32':
                # For Windows, use pip to update
                python_path = os.path.join(os.path.dirname(sys.executable), 'python.exe')
                if not os.path.exists(python_path):
                    python_path = sys.executable
                
                process.start(python_path, ['-m', 'pip', 'install', '--upgrade', '--no-cache-dir', 'yt-dlp'])
            else:
                # For Unix systems
                process.start('pip', ['install', '--upgrade', '--no-cache-dir', 'yt-dlp'])
            
            process.waitForFinished()
            
            if process.exitCode() == 0:
                self.status_label.setText("Update completed successfully!\nPlease restart the application.")
                self.check_version()  # Recheck version after update
            else:
                error = process.readAllStandardError().data().decode()
                self.status_label.setText(f"Update failed: {error}")
            
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(100)
            self.close_btn.setEnabled(True)
            
        except Exception as e:
            self.status_label.setText(f"Update failed: {str(e)}")
            self.close_btn.setEnabled(True)
            self.progress_bar.hide()

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('About YTSage')
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)

        # App title and version
        title_label = QLabel("YTSage")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ff0000;
            padding: 10px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel(f"Version {parent.version}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        # Description
        description = QLabel(
            "A modern YouTube downloader with a clean interface.\n"
            "Download videos in any quality, extract audio, fetch subtitles,\n"
            "and view video metadata. Built with yt-dlp for reliable performance."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        # Features list
        features_label = QLabel(
            "Key Features:\n"
            "• Smart video quality selection\n"
            "• Audio extraction\n"
            "• Subtitle support\n"
            "• Playlist downloads\n"
            "• Real-time progress tracking\n"
            "• Custom command support\n"
            "• SponsorBlock Integration\n"
            "• Save Thumbnail\n"
            "• One-click updates"
        )
        features_label.setStyleSheet("padding: 10px;")
        layout.addWidget(features_label)

        # Credits
        credits_label = QLabel(
            "Powered by:\n"
            "• yt-dlp\n"
            "• PySide6\n"
            "• FFmpeg"
        )
        credits_label.setStyleSheet("padding: 10px;")
        layout.addWidget(credits_label)

        # GitHub link
        github_btn = QPushButton("Visit GitHub Repository")
        github_btn.clicked.connect(lambda: webbrowser.open('https://github.com/oop7/YTSage'))
        layout.addWidget(github_btn)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        # Style the dialog
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)