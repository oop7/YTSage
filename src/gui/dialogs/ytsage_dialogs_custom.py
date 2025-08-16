"""
Custom functionality dialogs for YTSage application.
Contains dialogs for custom commands, cookies, time ranges, and other special features.
"""

import os
import sys
import threading
import subprocess
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QPlainTextEdit,
                             QCheckBox, QTabWidget, QWidget, QDialogButtonBox,
                             QFileDialog, QGroupBox)
from PySide6.QtCore import Qt, QMetaObject, Q_ARG

from ...core.ytsage_yt_dlp import get_yt_dlp_path

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False


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
        file_dialog.setNameFilter("Cookies files (*.txt *.lwp)")  # Common cookie file extensions
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.cookie_path_input.setText(selected_files[0])

    def get_cookie_file_path(self):
        # Return the selected cookie file path
        return self.cookie_path_input.text()


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
        file_dialog.setNameFilter("Cookies files (*.txt *.lwp)")  # Common cookie file extensions
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
        threading.Thread(target=self._run_command_thread,
                        args=(command, url, path),
                        daemon=True).start()

    def _run_command_thread(self, command, url, path):
        try:
            class CommandLogger:
                def debug(self, msg):
                    QMetaObject.invokeMethod(
                        self.dialog.log_output, "append", Qt.ConnectionType.QueuedConnection,
                        Q_ARG(str, msg)
                    )
                def warning(self, msg):
                    QMetaObject.invokeMethod(
                        self.dialog.log_output, "append", Qt.ConnectionType.QueuedConnection,
                        Q_ARG(str, f"Warning: {msg}")
                    )
                def error(self, msg):
                    QMetaObject.invokeMethod(
                        self.dialog.log_output, "append", Qt.ConnectionType.QueuedConnection,
                        Q_ARG(str, f"Error: {msg}")
                    )
                def __init__(self, dialog):
                    self.dialog = dialog

            # Split command into arguments
            args = command.split()

            # Add SponsorBlock if selected
            yt_dlp_path = get_yt_dlp_path()
            base_cmd = [yt_dlp_path] + args + [url]

            if self.sponsorblock_checkbox.isChecked():
                base_cmd.extend(['--sponsorblock-remove', 'sponsor,selfpromo,interaction'])

            # Show the full command
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
