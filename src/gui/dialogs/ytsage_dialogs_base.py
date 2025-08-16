"""
Base dialogs for YTSage application.
Contains basic utility dialogs like LogWindow and AboutDialog.
"""

import sys
import os
import webbrowser
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTextEdit, QWidget, QDialogButtonBox, QSizePolicy,
                             QPushButton, QMessageBox, QScrollArea)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QIcon

from ...core.ytsage_ffmpeg import check_ffmpeg_installed, get_ffmpeg_path
from ...core.ytsage_yt_dlp import get_yt_dlp_path, check_ytdlp_installed
from ...core.ytsage_utils import (check_ffmpeg, get_ytdlp_version, get_ffmpeg_version, 
                         refresh_version_cache, _version_cache)


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


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent # Store parent to access version etc.
        self.setWindowTitle("About YTSage")
        self.setMinimumSize(460, 420)  # Slightly increased to accommodate paths
        self.resize(460, 440)  # Slightly increased initial size
        self.setMaximumSize(500, 480)  # Reasonable maximum size
        
        # Set window flags to make dialog independent of parent movement
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)  # Reduced spacing
        layout.setContentsMargins(20, 20, 20, 20)  # Reduced margins
        layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinAndMaxSize)

        # App Information Section
        app_info_widget = self._create_app_info_section()
        layout.addWidget(app_info_widget)

        # Separator - subtle and compact
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #2a2a2a; margin: 8px 20px;")
        layout.addWidget(separator)

        # System Information Section
        system_info_widget = self._create_system_info_section()
        layout.addWidget(system_info_widget)

        # Close Button - compact positioning
        layout.addSpacing(10)  # Reduced space before button
        button_layout = QHBoxLayout()
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        
        # Center the button
        button_layout.addStretch()
        button_layout.addWidget(button_box)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Apply overall styling - improved consistency
        self.setStyleSheet("""
            QDialog { 
                background-color: #15181b; 
                color: #ffffff; 
            }
            QLabel { 
                color: #cccccc; 
            }
            QPushButton {
                padding: 10px 30px;
                background-color: #c90000;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                font-size: 12px;
                min-width: 80px;
            }
            QPushButton:hover { 
                background-color: #a50000; 
            }
            QPushButton:pressed { 
                background-color: #800000; 
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #333333;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                background-color: #15181b;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                color: #ffffff;
                font-size: 14px;
            }
        """)

    def _create_app_info_section(self):
        """Create the application information section - compact version"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(6)  # Reduced spacing
        
        # Title and Version - more compact
        title_label = QLabel("<span style='color: #c90000; font-size: 28px; font-weight: 300; letter-spacing: 2px;'>YTSage</span>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel(f"<span style='color: #cccccc; font-size: 13px; font-weight: normal;'>Version {getattr(self.parent, 'version', '4.7.0')}</span>")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        # Description - more compact
        description_label = QLabel("A simple GUI frontend for the powerful yt-dlp video downloader.")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("color: #ffffff; font-size: 11px; margin: 6px 0;")
        layout.addWidget(description_label)

        # Author and Links - compact single line
        info_layout = QHBoxLayout()
        info_layout.setSpacing(15)
        
        author_label = QLabel("By: <a href='https://github.com/oop7/' style='color: #c90000; text-decoration: none; font-size: 10px;'>oop7</a>")
        author_label.setOpenExternalLinks(True)
        info_layout.addWidget(author_label)

        repo_label = QLabel("GitHub: <a href='https://github.com/oop7/YTSage/' style='color: #c90000; text-decoration: none; font-size: 10px;'>YTSage</a>")
        repo_label.setOpenExternalLinks(True)
        info_layout.addWidget(repo_label)
        
        # Center the info layout
        info_container = QHBoxLayout()
        info_container.addStretch()
        info_container.addLayout(info_layout)
        info_container.addStretch()
        
        layout.addLayout(info_container)
        
        return widget

    def _create_system_info_section(self):
        """Create the system information section with compact design"""
        # Create main container with compact styling
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                border: 1px solid #333333;
                border-radius: 8px;
                background-color: #15181b;
                margin-top: 5px;
            }
        """)
        
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(8)  # Compact spacing
        main_layout.setContentsMargins(15, 10, 15, 10)
        
        # Create header with title and refresh button on same line
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        # System Information title
        title_label = QLabel("System Information")
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                padding: 0px;
                margin: 0px;
            }
        """)
        header_layout.addWidget(title_label)
        
        # Add stretch to push refresh button to the right
        header_layout.addStretch()
        
        # Create refresh button
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setFixedSize(16, 16)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 0px;
                background-color: transparent;
                border: none;
                color: #cccccc;
                font-size: 10px;
                font-weight: normal;
                margin: 0px;
            }
            QPushButton:hover {
                color: #ffffff;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
            QPushButton:pressed {
                color: #c90000;
                background-color: rgba(201, 0, 0, 0.1);
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_version_info)
        header_layout.addWidget(self.refresh_btn)
        
        main_layout.addLayout(header_layout)
        
        # Compact status grid layout
        self.status_container = QVBoxLayout()
        self.status_container.setSpacing(6)  # Tight spacing
        self.status_container.setContentsMargins(0, 0, 0, 0)
        
        main_layout.addLayout(self.status_container)
        
        # Show loading message initially
        self._show_loading_message()
        
        # Populate system information asynchronously
        QTimer.singleShot(100, self.update_system_info)
        
        return container

    def _show_loading_message(self):
        """Show a compact loading message while system information is being gathered."""
        loading_label = QLabel("🔄 Loading system information...")
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 11px;
                font-style: italic;
                padding: 10px;
            }
        """)
        
        self.status_container.addWidget(loading_label)

    def _create_status_item(self, icon, name, status_text, version_text, path_text=None, cache_status=""):
        """Create a compact status item widget"""
        item_widget = QWidget()
        # Adjust height based on whether we have path info
        item_height = 50 if path_text else 35
        item_widget.setMaximumHeight(item_height)
        item_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Main layout
        item_layout = QVBoxLayout(item_widget)
        item_layout.setContentsMargins(8, 4, 8, 4)
        item_layout.setSpacing(2)
        
        # First row: Icon, name, status, version
        first_row = QHBoxLayout()
        first_row.setSpacing(8)
        
        # Icon and name - compact
        name_label = QLabel(f"{icon} <b>{name}</b>")
        name_label.setStyleSheet("font-size: 12px; color: #ffffff; font-weight: bold;")
        name_label.setMinimumWidth(80)
        first_row.addWidget(name_label)
        
        # Status - compact
        status_label = QLabel(status_text)
        status_label.setStyleSheet("font-size: 11px; font-weight: bold;")
        status_label.setMinimumWidth(70)
        first_row.addWidget(status_label)
        
        # Version info - improved readability
        version_info = version_text
        if cache_status:
            version_info += cache_status
            
        version_label = QLabel(version_info)
        version_label.setStyleSheet("font-size: 11px; color: #cccccc;")  # Increased from 10px
        version_label.setWordWrap(False)
        first_row.addWidget(version_label)
        
        # Add stretch to push everything left
        first_row.addStretch()
        
        item_layout.addLayout(first_row)
        
        # Second row: Path (if provided)
        if path_text:
            path_label = QLabel(f"📁 {path_text}")
            path_label.setStyleSheet("font-size: 10px; color: #aaaaaa; margin-left: 12px;")  # Increased from 9px, better color
            path_label.setWordWrap(False)
            # Truncate very long paths
            if len(path_text) > 60:
                truncated_path = "..." + path_text[-57:]
                path_label.setText(f"📁 {truncated_path}")
            item_layout.addWidget(path_label)
        
        # Subtle background with minimal border
        item_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(45, 45, 45, 0.3);
                border: 1px solid #2a2a2a;
                border-radius: 4px;
                margin: 1px;
            }
            QWidget:hover {
                background-color: rgba(60, 60, 60, 0.4);
            }
        """)
        
        return item_widget

    def update_system_info(self):
        """Update the system information display with compact layout."""
        # Clear existing items
        for i in reversed(range(self.status_container.count())):
            child = self.status_container.itemAt(i).widget()
            if child:
                child.deleteLater()

        # yt-dlp Status - compact version with path
        ytdlp_found = check_ytdlp_installed()
        ytdlp_status_text = "<span style='color: #4CAF50;'>✓ Detected</span>" if ytdlp_found else "<span style='color: #F44336;'>✗ Missing</span>"
        ytdlp_version = get_ytdlp_version()
        
        # Get yt-dlp path
        ytdlp_path = get_yt_dlp_path() if ytdlp_found else None
        ytdlp_path_text = ytdlp_path if ytdlp_path and ytdlp_path != "yt-dlp" else None
        
        # Simplified cache status
        ytdlp_cache = _version_cache.get('ytdlp', {})
        last_check = ytdlp_cache.get('last_check', 0)
        cache_status = ""
        if last_check > 0:
            from datetime import datetime
            cache_time = datetime.fromtimestamp(last_check).strftime("%H:%M")
            cache_status = f" <span style='color: #888; font-size: 10px;'>({cache_time})</span>"  # Increased from 9px
        
        ytdlp_item = self._create_status_item(
            "🎥", "yt-dlp", ytdlp_status_text, ytdlp_version + cache_status, ytdlp_path_text
        )
        self.status_container.addWidget(ytdlp_item)

        # FFmpeg Status - compact version with path
        ffmpeg_found = check_ffmpeg()
        ffmpeg_status_text = "<span style='color: #4CAF50;'>✓ Detected</span>" if ffmpeg_found else "<span style='color: #F44336;'>✗ Missing</span>"
        ffmpeg_version = get_ffmpeg_version() if ffmpeg_found else "Not Available"
        
        # Get FFmpeg path
        ffmpeg_path_text = None
        if ffmpeg_found:
            ffmpeg_path = get_ffmpeg_path()
            ffmpeg_path_text = ffmpeg_path if ffmpeg_path else None
        
        # Simplified cache status for FFmpeg
        ffmpeg_cache = _version_cache.get('ffmpeg', {})
        last_check = ffmpeg_cache.get('last_check', 0)
        cache_status = ""
        if last_check > 0 and ffmpeg_found:
            from datetime import datetime
            cache_time = datetime.fromtimestamp(last_check).strftime("%H:%M")
            cache_status = f" <span style='color: #888; font-size: 10px;'>({cache_time})</span>"  # Increased from 9px
        
        ffmpeg_item = self._create_status_item(
            "🎬", "FFmpeg", ffmpeg_status_text, ffmpeg_version + cache_status, ffmpeg_path_text
        )
        self.status_container.addWidget(ffmpeg_item)

    def refresh_version_info(self):
        """Refresh version information manually."""
        self.refresh_btn.setText("🔄 Refreshing...")
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
        self.refresh_btn.setText("🔄 Refresh")
        self.refresh_btn.setEnabled(True)
        
        if success:
            self.update_system_info()
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
