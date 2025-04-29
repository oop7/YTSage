import sys
import os
import webbrowser
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QProgressBar, QLabel, QFileDialog,
                            QHeaderView, QStyle, QStyleFactory, QComboBox, QTextEdit, QDialog, QPlainTextEdit, QCheckBox, QButtonGroup, QListWidget,
                            QListWidgetItem, QDialogButtonBox, QScrollArea, QGroupBox)
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
                                     text=True,
                                     startupinfo=None if sys.platform != 'win32' else subprocess.STARTUPINFO(dwFlags=subprocess.STARTF_USESHOWWINDOW, wShowWindow=subprocess.SW_HIDE), # Hide console window on Windows
                                     creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0) # Hide console window on Windows
                if result.returncode == 0:
                    current_version = result.stdout.strip()
                else: # Try fallback if command failed
                    import yt_dlp
                    current_version = yt_dlp.version.__version__
            except Exception:
                 # Fallback to importing yt_dlp package directly if subprocess fails
                try:
                    import yt_dlp
                    current_version = yt_dlp.version.__version__
                except ImportError:
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
    update_finished = Signal(bool, str) # success (bool), message/error (str)
    
    def run(self):
        error_message = ""
        success = False
        try:
            self.update_status.emit("Starting update process...")
            
            # Determine paths (similar logic as before)
            python_path = sys.executable # Default to current interpreter
            yt_dlp_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()

            if getattr(sys, 'frozen', False) and sys.platform == 'win32':
                 alt_python_path = os.path.join(os.path.dirname(sys.executable), 'python.exe')
                 if os.path.exists(alt_python_path):
                     python_path = alt_python_path
            
            # Create and configure QProcess
            process = QProcess()
            process.setWorkingDirectory(yt_dlp_dir)
            process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels) # Combine stdout/stderr
            
            # Prepare command arguments
            pip_args = ['install', '--upgrade', '--no-cache-dir', 'yt-dlp']
            if sys.platform == 'win32':
                command = python_path
                args = ['-m', 'pip'] + pip_args
            else:
                # Assume pip is in PATH or use python -m pip for robustness
                command = python_path 
                args = ['-m', 'pip'] + pip_args 
                # Alternative if pip is guaranteed in PATH: command = 'pip', args = pip_args

            # Start the process
            self.update_status.emit(f"Running: {command} {' '.join(args)}")
            process.start(command, args)
            
            # Wait for finish (use QProcess event loop, not blocking waitForFinished)
            if not process.waitForStarted(5000): # Wait 5s for process to start
                 raise RuntimeError("Update process failed to start.")

            if not process.waitForFinished(-1): # Wait indefinitely for finish
                 raise RuntimeError("Update process failed to finish.")

            exit_code = process.exitCode()
            output = process.readAll().data().decode(errors='ignore') # Read combined output
            
            if exit_code == 0:
                self.update_status.emit("Update completed successfully!")
                success = True
                error_message = "Update successful. Please restart the application."
            else:
                self.update_status.emit(f"Update failed (Exit Code: {exit_code})")
                error_message = f"Update failed.\nExit Code: {exit_code}\nOutput:\n{output}"
                success = False
                
        except Exception as e:
            error_message = f"Update failed with exception: {e}"
            self.update_status.emit(error_message)
            success = False
            
        self.update_finished.emit(success, error_message)


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
                border-radius: 4px;
                text-align: center;
                color: white;
                background-color: #1d1e22;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #c90000;
                border-radius: 2px;
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
        self.update_btn.setEnabled(False)
        self.close_btn.setEnabled(False)
        self.status_label.setText("Initializing update...")
        self.progress_bar.setRange(0, 0) # Indeterminate progress
        self.progress_bar.show()
        
        # Create and start the update thread
        self.update_thread = UpdateThread()
        self.update_thread.update_status.connect(self.on_update_status) # Connect status signal
        self.update_thread.update_finished.connect(self.on_update_finished) # Connect finished signal
        self.update_thread.start()

    def on_update_status(self, message):
        """Slot to receive status messages from UpdateThread."""
        self.status_label.setText(message)

    def on_update_finished(self, success, message):
        """Slot called when the UpdateThread finishes."""
        self.progress_bar.setRange(0, 100) # Set determinate range
        self.progress_bar.setValue(100) # Mark as complete
        self.progress_bar.hide() # Optionally hide progress bar again
        self.status_label.setText(message)
        self.close_btn.setEnabled(True)
        
        if success:
            # Optionally re-check version automatically after successful update
            self.check_version() 
        else:
            # Re-enable update button only if failed?
            # self.update_btn.setEnabled(True) # Decide if appropriate
            pass # Keep update button disabled on failure for now

    def closeEvent(self, event):
        """Ensure threads are terminated if the dialog is closed prematurely."""
        if hasattr(self, 'version_check_thread') and self.version_check_thread.isRunning():
            self.version_check_thread.quit() # Ask thread to stop
            self.version_check_thread.wait() # Wait for it to finish
        if hasattr(self, 'update_thread') and self.update_thread.isRunning():
            self.update_thread.quit()
            self.update_thread.wait()
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

        # yt-dlp path
        yt_dlp_path = get_yt_dlp_path()
        yt_dlp_path_text = yt_dlp_path if yt_dlp_path else 'yt-dlp not found in PATH'
        yt_dlp_label = QLabel(f"<b>yt-dlp Path:</b> {yt_dlp_path_text}")
        yt_dlp_label.setWordWrap(True)
        info_layout.addWidget(yt_dlp_label)

        # FFmpeg Status
        ffmpeg_found = check_ffmpeg()
        ffmpeg_status_text = "<span style='color: #00ff00;'>Detected</span>" if ffmpeg_found else "<span style='color: #ff5555;'>Not Detected</span>"
        ffmpeg_label = QLabel(f"<b>FFmpeg Status:</b> {ffmpeg_status_text}")
        info_layout.addWidget(ffmpeg_label)

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
        self.current_path = current_path
        self.current_limit = current_limit if current_limit is not None else "" # Handle None
        self.current_unit_index = current_unit_index

        layout = QVBoxLayout(self)

        # --- Download Path Section ---
        path_group_box = QGroupBox("Download Path")
        path_layout = QVBoxLayout()

        self.path_display = QLabel(self.current_path)
        self.path_display.setWordWrap(True)
        self.path_display.setStyleSheet("QLabel { color: #cccccc; padding: 5px; border: 1px solid #3d3d3d; border-radius: 4px; background-color: #363636; }")
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