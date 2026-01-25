"""
FFmpeg installation dialogs for YTSage application.
Contains dialogs and threads for checking and installing FFmpeg.
"""

import webbrowser

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from ...core.ytsage_ffmpeg import auto_install_ffmpeg, check_ffmpeg_installed
from ...utils.ytsage_constants import ICON_PATH
from ...utils.ytsage_localization import _


class FFmpegInstallThread(QThread):
    finished = Signal(bool)
    progress = Signal(str)

    def run(self) -> None:
        # Use a callback to capture progress instead of stdout redirection
        def progress_callback(msg: str):
            self.progress.emit(msg)
        
        # Install FFmpeg with progress callback
        success = auto_install_ffmpeg(progress_callback=progress_callback)
        self.finished.emit(success)


class FFmpegCheckDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(_("ffmpeg.installation_title"))
        self.setMinimumWidth(500)
        self.setMinimumHeight(280)
        self.resize(500, 300)

        # Set the window icon to match the main app
        if parent and parent.windowIcon():
            self.setWindowIcon(parent.windowIcon())
        else:
            # Try to load the icon directly if parent not available
            # icon_path logic moved to src\utils\ytsage_constants.py

            if ICON_PATH.exists():
                self.setWindowIcon(QIcon(str(ICON_PATH)))

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and improved spacing
        header_text = QLabel(_("ffmpeg.installation_title"))
        header_text.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; padding: 5px 0;")
        header_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_text)

        # Message
        self.message_label = QLabel(_("ffmpeg.installation_message"))
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("font-size: 13px; color: #cccccc; padding: 10px 0; line-height: 1.4;")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message_label)

        # Progress label with improved styling
        self.progress_label = QLabel("")
        self.progress_label.setWordWrap(True)
        self.progress_label.setMinimumHeight(80)
        self.progress_label.setMaximumHeight(120)
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.progress_label.setStyleSheet(
            """
            QLabel {
                background-color: #1d1e22;
                color: #cccccc;
                border: 1px solid #3d3d3d;
                border-radius: 6px;
                padding: 12px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                line-height: 1.4;
            }
        """
        )
        self.progress_label.hide()
        layout.addWidget(self.progress_label)

        # Add stretch to push buttons to bottom
        layout.addStretch()

        # Buttons container - simple approach that should work
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        # Install button
        self.install_btn = QPushButton(_("ffmpeg.install_button"))
        self.install_btn.clicked.connect(self.start_installation)
        button_layout.addWidget(self.install_btn)

        # Manual install button
        self.manual_btn = QPushButton(_("ffmpeg.manual_guide"))
        self.manual_btn.clicked.connect(lambda: webbrowser.open("https://github.com/oop7/ffmpeg-install-guide"))
        button_layout.addWidget(self.manual_btn)

        # Close button
        self.close_btn = QPushButton(_("buttons.close"))
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)

        # Style the dialog to match app theme
        self.setStyleSheet(
            """
            QDialog {
                background-color: #15181b;
                color: #ffffff;
            }
            QLabel {
                color: #cccccc;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #c90000;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                font-size: 13px;
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
        """
        )

        # Initialize installation thread
        self.install_thread = None
        self.progress_messages = []  # Store progress messages

    def start_installation(self) -> None:
        self.install_btn.setEnabled(False)
        self.manual_btn.setEnabled(False)
        self.close_btn.setEnabled(False)

        # Check if FFmpeg is already installed
        if check_ffmpeg_installed():
            self.message_label.setText(_("ffmpeg.already_installed"))
            self.progress_label.setText(_("ffmpeg.installation_complete"))
            self.progress_label.show()
            self.install_btn.hide()
            self.manual_btn.hide()
            self.close_btn.setEnabled(True)
            return

        self.message_label.setText(_("ffmpeg.installing"))
        self.progress_messages = []  # Clear previous messages
        self.progress_label.show()

        self.install_thread = FFmpegInstallThread()
        self.install_thread.finished.connect(self.installation_finished)
        self.install_thread.progress.connect(self.update_progress)
        self.install_thread.start()

    def update_progress(self, message) -> None:
        # Keep only the last 5 messages to avoid overflow
        self.progress_messages.append(message)
        if len(self.progress_messages) > 5:
            self.progress_messages.pop(0)
        
        # Display the messages
        self.progress_label.setText("\n".join(self.progress_messages))

    def installation_finished(self, success) -> None:
        if success:
            self.message_label.setText(_("ffmpeg.install_success"))
            self.progress_label.setText(_("ffmpeg.installation_complete_close"))
            self.install_btn.hide()
            self.manual_btn.hide()
        else:
            self.message_label.setText(_("ffmpeg.installation_failed"))
            self.progress_label.setText(_("ffmpeg.try_manual"))
            self.install_btn.setEnabled(True)
            self.manual_btn.setEnabled(True)

        self.close_btn.setEnabled(True)
