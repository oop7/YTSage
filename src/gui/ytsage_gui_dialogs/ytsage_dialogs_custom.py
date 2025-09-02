"""
Custom functionality dialogs for YTSage application.
Contains dialogs for custom commands, cookies, time ranges, and other special features.
"""

import subprocess
import threading
from pathlib import Path
from typing import TYPE_CHECKING, cast

from PySide6.QtCore import Q_ARG, QMetaObject, QObject, Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.core.ytsage_yt_dlp import get_yt_dlp_path
from src.utils.ytsage_constants import YTDLP_DOCS_URL

if TYPE_CHECKING:
    from src.gui.ytsage_gui_main import YTSageApp  # only for type hints (no runtime import)


class CommandWorker(QObject):
    """Worker class for running yt-dlp commands in a separate thread"""

    # Signals for communicating with the main thread
    output_received = Signal(str)  # For command output lines
    command_finished = Signal(bool, int)  # For completion (success, exit_code)
    error_occurred = Signal(str)  # For errors

    def __init__(self, command, url, path):
        super().__init__()
        self.command = command
        self.url = url
        self.path = path

    def run_command(self):
        """Run the yt-dlp command and emit signals for output"""
        try:
            # Split command into arguments
            args = self.command.split()

            # Build the full command
            yt_dlp_path = get_yt_dlp_path()
            base_cmd = [yt_dlp_path] + args

            # Add download path if specified
            if self.path:
                base_cmd.extend(["-P", self.path])

            # Add URL at the end
            base_cmd.append(self.url)

            # Emit the full command
            self.output_received.emit(f"🔧 Full command: {' '.join(str(cmd) for cmd in base_cmd)}")
            self.output_received.emit("=" * 50)

            # Run the command
            proc = subprocess.Popen(
                base_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            # Stream output
            for line in proc.stdout:  # type: ignore[reportOptionalIterable]
                if line.strip():  # Only show non-empty lines
                    self.output_received.emit(line.rstrip())

            ret = proc.wait()
            self.output_received.emit("=" * 50)

            if ret != 0:
                self.output_received.emit(f"❌ Command failed with exit code {ret}")
                self.command_finished.emit(False, ret)
            else:
                self.output_received.emit("✅ Command completed successfully!")
                self.command_finished.emit(True, ret)

        except Exception as e:
            self.output_received.emit("=" * 50)
            self.error_occurred.emit(f"❌ Error executing command: {str(e)}")


class CustomOptionsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent: YTSageApp = cast("YTSageApp", self.parent())  # cast will help with auto complete and type hint checking.
        self.setWindowTitle("Custom Options")
        self.setMinimumSize(550, 400)  # Made even shorter
        layout = QVBoxLayout(self)

        # Create tab widget to organize content
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # === Cookies Tab ===
        cookies_tab = QWidget()
        cookies_layout = QVBoxLayout(cookies_tab)

        # Help text
        help_text = QLabel(
            "Choose how to provide cookies for logging in.\n"
            "This allows downloading of private videos and premium quality audio."
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #999999; padding: 10px;")
        cookies_layout.addWidget(help_text)

        # Cookie source selection
        cookie_source_group = QGroupBox("Cookie Source")
        cookie_source_layout = QVBoxLayout(cookie_source_group)

        # Radio buttons for cookie source
        self.cookie_file_radio = QRadioButton("Use cookie file (Netscape format)")
        self.cookie_file_radio.setChecked(True)
        self.cookie_file_radio.toggled.connect(self.on_cookie_source_changed)
        cookie_source_layout.addWidget(self.cookie_file_radio)

        self.cookie_browser_radio = QRadioButton("Extract cookies from browser")
        self.cookie_browser_radio.toggled.connect(self.on_cookie_source_changed)
        cookie_source_layout.addWidget(self.cookie_browser_radio)

        cookies_layout.addWidget(cookie_source_group)

        # Cookie file section
        self.cookie_file_group = QGroupBox("Cookie File")
        file_layout = QVBoxLayout(self.cookie_file_group)

        # File path input and browse button
        path_layout = QHBoxLayout()
        self.cookie_path_input = QLineEdit()
        self.cookie_path_input.setPlaceholderText("Path to cookies file (Netscape format)")
        if hasattr(self._parent, "cookie_file_path") and self._parent.cookie_file_path:
            # Convert Path to string properly and validate
            cookie_path_str = str(self._parent.cookie_file_path)
            # Only set if it looks like a valid path (more than just a drive letter)
            if len(cookie_path_str) > 3 and not cookie_path_str.endswith(":"):
                self.cookie_path_input.setText(cookie_path_str)
        path_layout.addWidget(self.cookie_path_input)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_cookie_file)
        path_layout.addWidget(self.browse_button)
        file_layout.addLayout(path_layout)

        cookies_layout.addWidget(self.cookie_file_group)

        # Browser selection section
        self.cookie_browser_group = QGroupBox("Browser Selection")
        browser_layout = QVBoxLayout(self.cookie_browser_group)

        browser_help = QLabel("Select the browser to extract cookies from. Make sure the browser is closed before extraction.")
        browser_help.setWordWrap(True)
        browser_help.setStyleSheet("color: #999999; font-size: 11px;")
        browser_layout.addWidget(browser_help)

        browser_select_layout = QHBoxLayout()
        browser_select_layout.addWidget(QLabel("Browser:"))

        self.browser_combo = QComboBox()
        self.browser_combo.addItems(["chrome", "firefox", "safari", "edge", "opera", "brave", "chromium", "vivaldi"])
        browser_select_layout.addWidget(self.browser_combo)
        browser_layout.addLayout(browser_select_layout)

        # Optional profile field
        profile_layout = QHBoxLayout()
        profile_layout.addWidget(QLabel("Profile (optional):"))
        self.profile_input = QLineEdit()
        self.profile_input.setPlaceholderText("Profile name or path (leave empty for default)")
        profile_layout.addWidget(self.profile_input)
        browser_layout.addLayout(profile_layout)

        cookies_layout.addWidget(self.cookie_browser_group)

        # Initially hide browser group
        self.cookie_browser_group.setVisible(False)

        # Status indicator for cookies
        self.cookie_status = QLabel("")
        self.cookie_status.setStyleSheet("color: #999999; font-style: italic;")
        cookies_layout.addWidget(self.cookie_status)

        cookies_layout.addStretch()

        # === Custom Command Tab ===
        command_tab = QWidget()
        command_layout = QVBoxLayout(command_tab)

        # Improved help text
        cmd_help_text = QLabel(
            "Enter your custom yt-dlp command below. The current URL will be automatically appended.<br><br>"
            "For complete list of options and usage examples, "
            f'<a href="{YTDLP_DOCS_URL}">click here to view the official yt-dlp documentation</a>.<br><br>'
            "Note: Download path and output filename template will be automatically handled."
        )
        cmd_help_text.setWordWrap(True)
        cmd_help_text.setOpenExternalLinks(True)  # Enable clicking links
        cmd_help_text.setTextFormat(Qt.TextFormat.RichText)  # Enable HTML rendering
        cmd_help_text.setStyleSheet(
            """
            QLabel {
                color: #cccccc; 
                font-size: 12px; 
                padding: 10px; 
                background-color: #1a1d20; 
                border-radius: 6px; 
                line-height: 1.4;
            }
            QLabel a {
                color: #4da6ff;
                text-decoration: underline;
            }
            QLabel a:hover {
                color: #66b3ff;
            }
        """
        )
        command_layout.addWidget(cmd_help_text)

        # Command input label
        input_label = QLabel("yt-dlp Arguments:")
        input_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff; margin-top: 10px;")
        command_layout.addWidget(input_label)

        # Command input
        self.command_input = QPlainTextEdit()
        self.command_input.setPlaceholderText("Enter yt-dlp arguments here...\n\n" "e.g. --extract-audio --audio-format mp3")
        self.command_input.setMinimumHeight(80)  # Reduced further from 100
        self.command_input.setStyleSheet(
            """
            QPlainTextEdit {
                background-color: #1d1e22;
                color: #ffffff;
                border: 2px solid #2a2d36;
                border-radius: 6px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.4;
            }
            QPlainTextEdit:focus {
                border-color: #c90000;
            }
        """
        )
        command_layout.addWidget(self.command_input)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(lambda: self.command_input.clear())
        clear_btn.setStyleSheet(
            """
            QPushButton {
                padding: 8px 15px;
                background-color: #444444;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """
        )
        button_layout.addWidget(clear_btn)

        button_layout.addStretch()  # Push run button to the right

        # Run command button
        self.run_btn = QPushButton("Run Command")
        self.run_btn.clicked.connect(self.run_custom_command)
        self.run_btn.setDefault(True)
        button_layout.addWidget(self.run_btn)

        command_layout.addLayout(button_layout)

        # Output label
        output_label = QLabel("Command Output:")
        output_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff; margin-top: 15px;")
        command_layout.addWidget(output_label)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Command output will appear here...")
        self.log_output.setMinimumHeight(100)  # Reduced further from 120
        self.log_output.setStyleSheet(
            """
            QTextEdit {
                background-color: #1d1e22;
                color: #ffffff;
                border: 2px solid #2a2d36;
                border-radius: 6px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
            }
            QTextEdit:focus {
                border-color: #c90000;
            }
        """
        )
        command_layout.addWidget(self.log_output)

        # Add tabs to the tab widget
        self.tab_widget.addTab(cookies_tab, "Login with Cookies")
        self.tab_widget.addTab(command_tab, "Custom Command")

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Apply global styles
        self.setStyleSheet(
            """
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
            QRadioButton {
                color: #ffffff;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #666666;
                background: #1d1e22;
                border-radius: 9px;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
                border-radius: 9px;
            }
            QComboBox {
                padding: 8px;
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
                color: #ffffff;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                border: none;
                width: 12px;
                height: 12px;
                background: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMgNEw2IDdMOSA0IiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }
            QComboBox QAbstractItemView {
                background-color: #1d1e22;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                selection-background-color: #c90000;
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
        """
        )

        # Initialize dialog with current settings (after all widgets and styles are set)
        self._initialize_cookie_settings()

    def _initialize_cookie_settings(self) -> None:
        """Initialize the dialog with current cookie settings from parent"""
        if hasattr(self._parent, "browser_cookies_option") and self._parent.browser_cookies_option:
            # Browser cookies are active
            self.cookie_browser_radio.setChecked(True)
            browser_parts = self._parent.browser_cookies_option.split(":")
            browser = browser_parts[0]
            profile = browser_parts[1] if len(browser_parts) > 1 else ""

            # Set browser selection
            index = self.browser_combo.findText(browser)
            if index >= 0:
                self.browser_combo.setCurrentIndex(index)

            # Set profile if any
            self.profile_input.setText(profile)

            self.cookie_status.setText(f"Browser cookies active: {self._parent.browser_cookies_option}")
            self.cookie_status.setStyleSheet("color: #00cc00; font-style: italic;")
        elif hasattr(self._parent, "cookie_file_path") and self._parent.cookie_file_path:
            # File cookies are active - ensure file radio is selected and update status
            self.cookie_file_radio.setChecked(True)
            self.cookie_status.setText(f"Cookie file active: {self._parent.cookie_file_path.name}")
            self.cookie_status.setStyleSheet("color: #00cc00; font-style: italic;")
        else:
            # No cookies configured - ensure file radio is selected by default
            self.cookie_file_radio.setChecked(True)

    def on_cookie_source_changed(self) -> None:
        """Handle cookie source radio button changes"""
        if self.cookie_file_radio.isChecked():
            self.cookie_file_group.setVisible(True)
            self.cookie_browser_group.setVisible(False)
            self.cookie_status.setText("")
        else:
            self.cookie_file_group.setVisible(False)
            self.cookie_browser_group.setVisible(True)
            self.cookie_status.setText("Browser cookies will be extracted when applied")
            self.cookie_status.setStyleSheet("color: #ffaa00; font-style: italic;")

    def browse_cookie_file(self) -> None:
        # Open file dialog to select cookie file
        selected_files, _ = QFileDialog.getOpenFileName(self, "Select Cookie File", "", "Cookies files (*.txt *.lwp)")

        if selected_files:
            # Ensure we have a valid full path
            cookie_path = Path(selected_files).resolve()
            self.cookie_path_input.setText(str(cookie_path))
            self.cookie_status.setText("Cookie file selected - Click OK to apply")
            self.cookie_status.setStyleSheet("color: #00cc00; font-style: italic;")

    def get_cookie_file_path(self) -> Path | None:
        # Return the selected cookie file path if it's not empty and using file mode
        if self.cookie_file_radio.isChecked():
            path_text = self.cookie_path_input.text().strip()
            if path_text:
                path = Path(path_text)
                if path.exists() and path.is_file():
                    return path
                else:
                    # File doesn't exist or is not a file - still return path for user feedback
                    return path if len(path_text) > 3 else None  # Avoid single letters like 'C'
        return None

    def get_browser_cookies_option(self) -> str | None:
        """Returns the --cookies-from-browser option string if browser mode is selected"""
        if self.cookie_browser_radio.isChecked():
            browser = self.browser_combo.currentText()
            profile = self.profile_input.text().strip()

            if profile:
                return f"{browser}:{profile}"
            else:
                return browser
        return None

    def is_using_browser_cookies(self) -> bool:
        """Returns True if browser cookies mode is selected"""
        return self.cookie_browser_radio.isChecked()

    def run_custom_command(self) -> None:
        url = self._parent.url_input.text().strip()
        if not url:
            self.log_output.append("❌ Error: No URL provided. Please enter a URL in the main window.")
            return

        command = self.command_input.toPlainText().strip()
        if not command:
            self.log_output.append("❌ Error: No command provided. Please enter yt-dlp arguments.")
            return

        # Get download path from parent
        path = self._parent.last_path

        self.log_output.clear()
        self.log_output.append("🚀 Executing custom yt-dlp command")
        self.log_output.append(f"📍 URL: {url}")
        self.log_output.append(f"⚙️  Arguments: {command}")
        if path:
            self.log_output.append(f"📁 Download path: {path}")
        self.log_output.append("=" * 50)
        self.run_btn.setEnabled(False)
        self.run_btn.setText("Running...")

        # Create worker and thread
        self.worker = CommandWorker(command, url, path)
        self.worker_thread = threading.Thread(target=self.worker.run_command, daemon=True)

        # Connect worker signals to our slots
        self.worker.output_received.connect(self.on_output_received)
        self.worker.command_finished.connect(self.on_command_finished)
        self.worker.error_occurred.connect(self.on_error_occurred)

        # Start the thread
        self.worker_thread.start()

    def on_output_received(self, text: str):
        """Slot for receiving output from the worker"""
        self.log_output.append(text)

    def on_command_finished(self, success: bool, exit_code: int):
        """Slot for when command finishes"""
        self.run_btn.setEnabled(True)
        self.run_btn.setText("Run Command")

    def on_error_occurred(self, error_msg: str):
        """Slot for handling errors"""
        self.log_output.append(error_msg)
        self.run_btn.setEnabled(True)
        self.run_btn.setText("Run Command")


class TimeRangeDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Download Video Section")
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
        self.force_keyframes.setStyleSheet(
            """
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
        """
        )
        layout.addWidget(self.force_keyframes)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Apply styling
        self.setStyleSheet(
            """
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
        """
        )

        # Initialize preview
        # self.update_preview() # Removed preview functionality

    def get_download_sections(self) -> str | None:
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

    def get_force_keyframes(self) -> bool:
        """Returns whether to force keyframes at cuts"""
        return self.force_keyframes.isChecked()
