"""
Updater tab for Custom Options dialog.
Handles checking for and installing FFmpeg updates.
"""

import threading
from typing import TYPE_CHECKING, cast

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.utils.ytsage_localization import _
from src.utils.ytsage_logger import logger
from src.core.ytsage_ffmpeg_updater import check_ffmpeg_update_available, update_ffmpeg
from src.utils.ytsage_constants import OS_NAME

if TYPE_CHECKING:
    from src.gui.ytsage_gui_dialogs.ytsage_dialogs_custom import CustomOptionsDialog


class UpdateWorker(QObject):
    """Worker class for running FFmpeg updates in a separate thread."""
    
    progress = Signal(str)  # Progress messages
    finished = Signal(bool)  # Completion status (success/failure)
    
    def run_update(self):
        """Run the FFmpeg update process."""
        try:
            def progress_callback(msg: str):
                """Callback for progress updates."""
                self.progress.emit(msg)
            
            # Run the update
            success = update_ffmpeg(progress_callback=progress_callback)
            self.finished.emit(success)
            
        except Exception as e:
            logger.exception(f"Error during FFmpeg update: {e}")
            self.progress.emit(f"❌ Error: {e}")
            self.finished.emit(False)


class UpdaterTabWidget(QWidget):
    """Widget for the Updater tab in Custom Options dialog."""
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent: "CustomOptionsDialog" = cast("CustomOptionsDialog", self.parent())
        
        self.update_thread = None
        self.update_worker = None
        
        # State variables
        self.current_version = "Unknown"
        self.latest_version = "Unknown"
        self.update_available = False
        
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # Help text
        help_text = QLabel(_('ffmpeg_updater.description'))
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #999999; padding: 10px;")
        layout.addWidget(help_text)
        
        # FFmpeg Update Section
        ffmpeg_group = QGroupBox(_('ffmpeg_updater.title'))
        ffmpeg_layout = QVBoxLayout(ffmpeg_group)
        
        # Version information layout
        version_layout = QVBoxLayout()
        
        # Current version
        current_layout = QHBoxLayout()
        current_label = QLabel(_('ffmpeg_updater.current_version'))
        current_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        current_layout.addWidget(current_label)
        
        self.current_version_label = QLabel("...")
        self.current_version_label.setStyleSheet("color: #cccccc;")
        current_layout.addWidget(self.current_version_label)
        current_layout.addStretch()
        version_layout.addLayout(current_layout)
        
        # Latest version
        latest_layout = QHBoxLayout()
        latest_label = QLabel(_('ffmpeg_updater.latest_version'))
        latest_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        latest_layout.addWidget(latest_label)
        
        self.latest_version_label = QLabel("...")
        self.latest_version_label.setStyleSheet("color: #cccccc;")
        latest_layout.addWidget(self.latest_version_label)
        latest_layout.addStretch()
        version_layout.addLayout(latest_layout)
        
        ffmpeg_layout.addLayout(version_layout)
        
        # Status label
        self.status_label = QLabel(_('ffmpeg_updater.status_idle'))
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(
            "color: #888888; font-size: 12px; padding: 8px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
        ffmpeg_layout.addWidget(self.status_label)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Check for updates button
        self.check_button = QPushButton(_('ffmpeg_updater.check_updates'))
        self.check_button.clicked.connect(self.check_for_updates)
        self.check_button.setStyleSheet(
            """
            QPushButton {
                padding: 8px 15px;
                background-color: #444444;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666666;
            }
        """
        )
        button_layout.addWidget(self.check_button)
        
        button_layout.addStretch()
        
        # Update button
        self.update_button = QPushButton(_('ffmpeg_updater.update_button'))
        self.update_button.clicked.connect(self.start_update)
        self.update_button.setEnabled(False)
        self.update_button.setStyleSheet(
            """
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QPushButton:disabled {
                background-color: #4a4a4a;
                color: #888888;
            }
        """
        )
        button_layout.addWidget(self.update_button)
        
        ffmpeg_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid #2a2d36;
                border-radius: 4px;
                background-color: #1d1e22;
                text-align: center;
                color: #ffffff;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #c90000;
                border-radius: 2px;
            }
        """
        )
        ffmpeg_layout.addWidget(self.progress_bar)
        
        # Log output
        log_label = QLabel("Update Log:")
        log_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #ffffff; margin-top: 10px;")
        ffmpeg_layout.addWidget(log_label)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Update logs will appear here...")
        self.log_output.setMinimumHeight(150)
        self.log_output.setStyleSheet(
            """
            QTextEdit {
                background-color: #1d1e22;
                color: #ffffff;
                border: 2px solid #2a2d36;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 11px;
            }
        """
        )
        ffmpeg_layout.addWidget(self.log_output)
        
        layout.addWidget(ffmpeg_group)
        layout.addStretch()
    
    def check_for_updates(self) -> None:
        """Check if FFmpeg updates are available."""
        self.check_button.setEnabled(False)
        self.update_button.setEnabled(False)
        self.status_label.setText(_('ffmpeg_updater.status_checking'))
        self.status_label.setStyleSheet(
            "color: #ffaa00; font-size: 12px; padding: 8px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
        self.log_output.append("🔍 Checking for FFmpeg updates...")
        
        # Run check in background thread
        def check_thread():
            try:
                update_available, current_version, latest_version = check_ffmpeg_update_available()
                
                # Update UI in main thread using signals
                self.check_button.setEnabled(True)
                self._update_check_results(update_available, current_version, latest_version)
                
            except Exception as e:
                logger.exception(f"Error checking for updates: {e}")
                self.check_button.setEnabled(True)
                self._show_check_error(str(e))
        
        thread = threading.Thread(target=check_thread, daemon=True)
        thread.start()
    
    def _update_check_results(self, update_available: bool, current_version: str, latest_version: str) -> None:
        """Handle completion of update check."""
        self.update_available = update_available
        self.current_version = current_version
        self.latest_version = latest_version
        
        # Update version labels
        self.current_version_label.setText(current_version)
        self.latest_version_label.setText(latest_version)
        
        # Update status
        if current_version == "Not installed":
            self.status_label.setText(_('ffmpeg_updater.install_first'))
            self.status_label.setStyleSheet(
                "color: #ff6666; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
            self.update_button.setEnabled(True if OS_NAME == "Windows" else False)
            self.log_output.append(f"❌ FFmpeg is not installed. Latest version available: {latest_version}")
        elif update_available:
            self.status_label.setText(_('ffmpeg_updater.status_update_available'))
            self.status_label.setStyleSheet(
                "color: #ffaa00; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
            self.update_button.setEnabled(True if OS_NAME == "Windows" else False)
            self.log_output.append(f"⚠ Update available: {current_version} → {latest_version}")
        else:
            self.status_label.setText(_('ffmpeg_updater.status_up_to_date'))
            self.status_label.setStyleSheet(
                "color: #00cc00; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
            self.update_button.setEnabled(False)
            self.log_output.append(f"✅ FFmpeg is up to date (version {current_version})")
        
        # Show message for non-Windows systems
        if OS_NAME != "Windows" and update_available:
            self.log_output.append("ℹ️ Automatic updates are only available on Windows.")
            self.log_output.append("   Please use your system's package manager to update FFmpeg.")
    
    def _show_check_error(self, error: str) -> None:
        """Handle error during update check."""
        self.status_label.setText(_('ffmpeg_updater.check_failed'))
        self.status_label.setStyleSheet(
            "color: #ff6666; font-size: 12px; padding: 8px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
        self.log_output.append(f"❌ Error checking for updates: {error}")
    
    def start_update(self) -> None:
        """Start the FFmpeg update process."""
        if OS_NAME != "Windows":
            self.log_output.append("❌ Automatic updates are only supported on Windows.")
            return
        
        # Disable buttons during update
        self.check_button.setEnabled(False)
        self.update_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        
        self.log_output.append("=" * 60)
        self.log_output.append("🚀 Starting FFmpeg update process...")
        self.log_output.append("=" * 60)
        
        # Create worker and thread
        self.update_worker = UpdateWorker()
        self.update_thread = threading.Thread(target=self.update_worker.run_update, daemon=True)
        
        # Connect signals
        self.update_worker.progress.connect(self._on_update_progress)
        self.update_worker.finished.connect(self._on_update_finished)
        
        # Start update
        self.update_thread.start()
    
    def _on_update_progress(self, message: str) -> None:
        """Handle progress updates from the update worker."""
        self.log_output.append(message)
        # Auto-scroll to bottom
        cursor = self.log_output.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_output.setTextCursor(cursor)
    
    def _on_update_finished(self, success: bool) -> None:
        """Handle completion of the update process."""
        self.progress_bar.setVisible(False)
        self.check_button.setEnabled(True)
        
        self.log_output.append("=" * 60)
        
        if success:
            self.log_output.append(_('ffmpeg_updater.update_success', version=self.latest_version))
            self.status_label.setText(_('ffmpeg_updater.status_up_to_date'))
            self.status_label.setStyleSheet(
                "color: #00cc00; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
            # Re-check to update version info
            self.check_for_updates()
        else:
            self.log_output.append(_('ffmpeg_updater.update_failed'))
            self.status_label.setText(_('ffmpeg_updater.status_update_available'))
            self.update_button.setEnabled(True)
        
        self.log_output.append("=" * 60)
