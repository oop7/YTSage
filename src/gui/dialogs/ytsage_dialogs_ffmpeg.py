"""
FFmpeg installation dialogs for YTSage application.
Contains dialogs and threads for checking and installing FFmpeg.
"""

import sys
import os
import webbrowser
import contextlib
from io import StringIO
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QStyle, QSizePolicy, QDialogButtonBox)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QIcon

from ...core.ytsage_ffmpeg import auto_install_ffmpeg, check_ffmpeg_installed


class FFmpegInstallThread(QThread):
    finished = Signal(bool)
    progress = Signal(str)

    def run(self):
        # Redirect stdout to capture progress messages
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
        self.setWindowTitle('FFmpeg Installation')
        self.setMinimumWidth(450)
        self.setMinimumHeight(200)
        self.resize(450, 220)
        
        # Set the window icon to match the main app
        if parent and parent.windowIcon():
            self.setWindowIcon(parent.windowIcon())
        else:
            # Try to load the icon directly if parent not available
            # Navigate from src/gui/dialogs/ to project root, then to assets/Icon/
            current_dir = os.path.dirname(os.path.abspath(__file__))  # dialogs/
            gui_dir = os.path.dirname(current_dir)                    # gui/
            src_dir = os.path.dirname(gui_dir)                        # src/
            project_root = os.path.dirname(src_dir)                   # project root
            icon_path = os.path.join(project_root, 'assets', 'Icon', 'icon.png')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and improved spacing
        header_text = QLabel("FFmpeg Installation")
        header_text.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; padding: 5px 0;")
        header_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_text)

        # Message
        self.message_label = QLabel(
            "YTSage needs FFmpeg to process videos.\n\n"
            "Choose an installation option below:"
        )
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("font-size: 13px; color: #cccccc; padding: 10px 0; line-height: 1.4;")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message_label)

        # Progress label with improved styling and compact height
        self.progress_label = QLabel("")
        self.progress_label.setWordWrap(True)
        self.progress_label.setMinimumHeight(60)  # Smaller but visible area
        self.progress_label.setMaximumHeight(80)  # Limit maximum height
        self.progress_label.setStyleSheet("""
            QLabel {
                background-color: #1d1e22;
                color: #cccccc;
                border: 1px solid #3d3d3d;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                line-height: 1.2;
            }
        """)
        self.progress_label.hide()
        layout.addWidget(self.progress_label)
        
        # Add minimal stretch - just enough to push buttons down slightly
        layout.addSpacing(10)

        # Buttons container - simple approach that should work
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)  # Simple spacing
        
        # Install button
        self.install_btn = QPushButton("Install FFmpeg")
        self.install_btn.clicked.connect(self.start_installation)
        button_layout.addWidget(self.install_btn)

        # Manual install button
        self.manual_btn = QPushButton("Manual Guide")
        self.manual_btn.clicked.connect(lambda: webbrowser.open('https://github.com/oop7/ffmpeg-install-guide'))
        button_layout.addWidget(self.manual_btn)

        # Close button
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)

        # Style the dialog to match app theme
        self.setStyleSheet("""
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
        """)

        # Initialize installation thread
        self.install_thread = None

    def start_installation(self):
        self.install_btn.setEnabled(False)
        self.manual_btn.setEnabled(False)
        self.close_btn.setEnabled(False)
        
        # Check if FFmpeg is already installed
        if check_ffmpeg_installed():
            self.message_label.setText("FFmpeg is already installed!")
            self.progress_label.setText("Installation complete. You can close this dialog and continue using YTSage.")
            self.progress_label.show()
            self.install_btn.hide()
            self.manual_btn.hide()
            self.close_btn.setEnabled(True)
            return
            
        self.message_label.setText("Installing FFmpeg... Please wait")
        self.progress_label.show()

        self.install_thread = FFmpegInstallThread()
        self.install_thread.finished.connect(self.installation_finished)
        self.install_thread.progress.connect(self.update_progress)
        self.install_thread.start()

    def update_progress(self, message):
        self.progress_label.setText(message)

    def installation_finished(self, success):
        if success:
            self.message_label.setText("FFmpeg has been installed successfully!")
            self.progress_label.setText("Installation complete. You can now close this dialog and continue using YTSage.")
            self.install_btn.hide()
            self.manual_btn.hide()
        else:
            self.message_label.setText("FFmpeg installation encountered an issue.")
            self.progress_label.setText("Please try using the manual installation guide instead.")
            self.install_btn.setEnabled(True)
            self.manual_btn.setEnabled(True)
        
        self.close_btn.setEnabled(True)
