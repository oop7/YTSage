"""
Base dialogs for YTSage application.
Contains basic utility dialogs like LogWindow and AboutDialog.
"""

from datetime import datetime

from PySide6.QtCore import Qt, QThread, QTimer, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ... import __version__ as APP_VERSION
from ...utils.ytsage_localization import _
from ...utils.ytsage_logger import logger
from ...utils.ytsage_constants import APP_LOG_DIR

from ...core.ytsage_ffmpeg import get_ffmpeg_path
from ...core.ytsage_utils import _version_cache, check_ffmpeg, get_ffmpeg_version, get_ytdlp_version, get_deno_version, refresh_version_cache
from ...core.ytsage_yt_dlp import check_ytdlp_installed, get_yt_dlp_path, check_ytdlp_deno_integration
from ...core.ytsage_deno import check_deno_installed, get_deno_path


class SystemInfoThread(QThread):
    """Background thread to gather system information."""
    info_ready = Signal(dict)

    def run(self):
        info = {}
        
        # yt-dlp Status
        ytdlp_found = check_ytdlp_installed()
        info['ytdlp_found'] = ytdlp_found
        info['ytdlp_version'] = get_ytdlp_version()
        info['ytdlp_path'] = get_yt_dlp_path() if ytdlp_found else None

        # yt-dlp cache status
        ytdlp_cache = _version_cache.get("ytdlp", {})
        info['ytdlp_last_check'] = ytdlp_cache.get("last_check", 0)
        
        # FFmpeg Status
        ffmpeg_found = check_ffmpeg()
        info['ffmpeg_found'] = ffmpeg_found
        info['ffmpeg_version'] = get_ffmpeg_version() if ffmpeg_found else _('about.not_available')
        info['ffmpeg_path'] = get_ffmpeg_path() if ffmpeg_found else None

        # FFmpeg cache status
        ffmpeg_cache = _version_cache.get("ffmpeg", {})
        info['ffmpeg_last_check'] = ffmpeg_cache.get("last_check", 0)
        
        # Deno Status
        deno_found = check_deno_installed()
        info['deno_found'] = deno_found
        info['deno_version'] = get_deno_version() if deno_found else _('about.not_available')
        info['deno_path'] = get_deno_path() if deno_found else None
        
        # Deno cache status
        deno_cache = _version_cache.get("deno", {})
        info['deno_last_check'] = deno_cache.get("last_check", 0)

        # Check integration with yt-dlp if both are present
        info['integration_status'] = False
        if deno_found and ytdlp_found:
             info['integration_status'] = check_ytdlp_deno_integration()
             
        self.info_ready.emit(info)


class LogWindow(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(_("dialogs.ytdlp_log_title"))
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout(self)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(
            """
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: Consolas, monospace;
                font-size: 12px;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
            }
        """
        )

        layout.addWidget(self.log_text)

    def append_log(self, message) -> None:
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


class AboutDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent = parent  # Store parent to access version etc.
        self.info_thread = None
        self.refresh_thread = None
        self.setWindowTitle(_("about.title"))
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
        """
        )

    def _create_app_info_section(self) -> QWidget:
        """Create the application information section - compact version"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(6)  # Reduced spacing

        # Title and Version - more compact
        title_label = QLabel(
            "<span style='color: #c90000; font-size: 28px; font-weight: 300; letter-spacing: 2px;'>YTSage</span>"
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel(
            f"<span style='color: #cccccc; font-size: 13px; font-weight: normal;'>"
            f"{_('about.version', version=getattr(self._parent, 'version', APP_VERSION))}</span>"
        )
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        # Description - more compact
        description_label = QLabel(_("about.description"))
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("color: #ffffff; font-size: 11px; margin: 6px 0;")
        layout.addWidget(description_label)

        # Author and Links - compact single line
        info_layout = QHBoxLayout()
        info_layout.setSpacing(15)

        author_link = '<a href="https://github.com/oop7/" style="color: #c90000; text-decoration: none;">oop7</a>'
        author_label = QLabel(
            f"{_('about.author', author=author_link)}"
        )
        author_label.setOpenExternalLinks(True)
        info_layout.addWidget(author_label)

        repo_link = '<a href="https://github.com/oop7/YTSage/" style="color: #c90000; text-decoration: none;">YTSage</a>'
        repo_label = QLabel(
            f"{_('about.github', repo=repo_link)}"
        )
        repo_label.setOpenExternalLinks(True)
        info_layout.addWidget(repo_label)

        sponsor_link = '<a href="https://github.com/sponsors/oop7" style="color: #c90000; text-decoration: none;">❤️ Sponsor</a>'
        sponsor_label = QLabel(sponsor_link)
        sponsor_label.setOpenExternalLinks(True)
        info_layout.addWidget(sponsor_label)

        # Center the info layout
        info_container = QHBoxLayout()
        info_container.addStretch()
        info_container.addLayout(info_layout)
        info_container.addStretch()

        layout.addLayout(info_container)

        return widget

    def _create_system_info_section(self) -> QWidget:
        """Create the system information section with compact design"""
        # Create main container with compact styling
        container = QWidget()
        container.setStyleSheet(
            """
            QWidget {
                border: 1px solid #333333;
                border-radius: 8px;
                background-color: #15181b;
                margin-top: 5px;
            }
        """
        )

        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(8)  # Compact spacing
        main_layout.setContentsMargins(15, 10, 15, 10)

        # Create header with title and refresh button on same line
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 5)

        # System Information title
        title_label = QLabel(_("about.system_info"))
        title_label.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                padding: 0px;
                margin: 0px;
            }
        """
        )
        header_layout.addWidget(title_label)

        # Add stretch to push refresh button to the right
        header_layout.addStretch()

        # Create logs button (minimal)
        self.logs_btn = QPushButton(_("about.open_logs")) # Expected to be small text or icon
        self.logs_btn.setToolTip(_("about.logs_tooltip"))
        self.logs_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logs_btn.setStyleSheet(
            """
            QPushButton {
                padding: 1px 6px;
                background-color: transparent;
                border: 1px solid #333;
                border-radius: 4px;
                color: #888888;
                font-size: 10px;
                margin-right: 8px;
            }
            QPushButton:hover {
                color: #ffffff;
                border-color: #555;
                background-color: rgba(255, 255, 255, 0.05);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """
        )
        self.logs_btn.clicked.connect(self.open_logs_folder)
        header_layout.addWidget(self.logs_btn)

        # Create refresh button
        self.refresh_btn = QPushButton(_("about.refresh"))
        self.refresh_btn.setFixedSize(16, 16)
        self.refresh_btn.setStyleSheet(
            """
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
        """
        )
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

    def _show_loading_message(self) -> None:
        """Show a compact loading message while system information is being gathered."""
        # Strip the emoji from the localized string to avoid rendering issues
        loading_text = _("about.loading").replace("🔄", "").strip()
        loading_label = QLabel(loading_text)
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_label.setStyleSheet(
            """
            QLabel {
                color: #888888;
                font-size: 11px;
                padding: 10px;
            }
        """
        )

        self.status_container.addWidget(loading_label)

    def _create_status_item(self, icon, name, status_text, version_text, path_text=None, cache_status="") -> QWidget:
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
            if len(str(path_text)) > 60:
                truncated_path = "..." + str(path_text)[-57:]
                path_label.setText(f"📁 {truncated_path}")
            item_layout.addWidget(path_label)

        # Subtle background with minimal border
        item_widget.setStyleSheet(
            """
            QWidget {
                background-color: rgba(45, 45, 45, 0.3);
                border: 1px solid #2a2a2a;
                border-radius: 4px;
                margin: 1px;
            }
            QWidget:hover {
                background-color: rgba(60, 60, 60, 0.4);
            }
        """
        )

        return item_widget

    def update_system_info(self) -> None:
        """Start background thread to gather system info."""
        if self.info_thread and self.info_thread.isRunning():
            return

        self.info_thread = SystemInfoThread()
        self.info_thread.info_ready.connect(self._populate_system_info)
        self.info_thread.start()

    def _populate_system_info(self, info: dict) -> None:
        """Populate UI with gathered info."""
        # Clear existing items
        for i in reversed(range(self.status_container.count())):
            child = self.status_container.itemAt(i).widget()
            if child:
                child.deleteLater()

        # yt-dlp Status - compact version with path
        ytdlp_found = info['ytdlp_found']
        ytdlp_status_text = (
            f"<span style='color: #4CAF50;'>{_('about.detected')}</span>" if ytdlp_found else f"<span style='color: #F44336;'>{_('about.missing')}</span>"
        )
        ytdlp_version = info['ytdlp_version']

        # Get yt-dlp path
        ytdlp_path = info['ytdlp_path']
        ytdlp_path_text = ytdlp_path if ytdlp_path and ytdlp_path != "yt-dlp" else None

        # Simplified cache status
        last_check = info['ytdlp_last_check']
        cache_status = ""
        if last_check > 0:
            cache_time = datetime.fromtimestamp(last_check).strftime("%H:%M")
            cache_status = f" <span style='color: #888; font-size: 10px;'>({cache_time})</span>"  # Increased from 9px

        ytdlp_item = self._create_status_item(
            "🎥",
            "yt-dlp",
            ytdlp_status_text,
            ytdlp_version + cache_status,
            ytdlp_path_text,
        )
        self.status_container.addWidget(ytdlp_item)

        # FFmpeg Status - compact version with path
        ffmpeg_found = info['ffmpeg_found']
        ffmpeg_status_text = (
            f"<span style='color: #4CAF50;'>{_('about.detected')}</span>"
            if ffmpeg_found
            else f"<span style='color: #F44336;'>{_('about.missing')}</span>"
        )
        ffmpeg_version = info['ffmpeg_version']

        # Get FFmpeg path
        ffmpeg_path_text = info['ffmpeg_path']

        # Simplified cache status for FFmpeg
        last_check = info['ffmpeg_last_check']
        cache_status = ""
        if last_check > 0 and ffmpeg_found:
            cache_time = datetime.fromtimestamp(last_check).strftime("%H:%M")
            cache_status = f" <span style='color: #888; font-size: 10px;'>({cache_time})</span>"  # Increased from 9px

        ffmpeg_item = self._create_status_item(
            "🎬",
            "FFmpeg",
            ffmpeg_status_text,
            ffmpeg_version + cache_status,
            ffmpeg_path_text,
        )
        self.status_container.addWidget(ffmpeg_item)

        # Deno Status - compact version with path (only show path if in app bin directory)
        deno_found = info['deno_found']
        deno_status_text = (
            f"<span style='color: #4CAF50;'>{_('about.detected')}</span>" if deno_found else f"<span style='color: #F44336;'>{_('about.missing')}</span>"
        )
        deno_version = info['deno_version']

        # Get Deno path - only show if in app bin directory
        deno_path_text = None
        if deno_found:
            deno_path = info['deno_path']
            # Only show path if it's not the fallback "deno" and the file exists
            if deno_path and deno_path != "deno":
                from pathlib import Path
                from ...utils.ytsage_constants import DENO_APP_BIN_PATH
                # Check if the path is our managed binary
                if Path(deno_path).resolve() == DENO_APP_BIN_PATH.resolve():
                    deno_path_text = deno_path

        # Simplified cache status for Deno
        last_check = info['deno_last_check']
        cache_status = ""
        if last_check > 0 and deno_found:
            cache_time = datetime.fromtimestamp(last_check).strftime("%H:%M")
            cache_status = f" <span style='color: #888; font-size: 10px;'>({cache_time})</span>"
        
        # Check integration with yt-dlp if both are present
        integration_status = ""
        if info.get('integration_status', False):
             integration_status = f" <span style='color: #4CAF50; font-size: 10px; font-weight: bold;'> + yt-dlp</span>"

        deno_item = self._create_status_item(
            "🦕",
            "Deno",
            deno_status_text,
            deno_version + cache_status + integration_status,
            deno_path_text,
        )
        self.status_container.addWidget(deno_item)


    def open_logs_folder(self):
        """Open the application logs folder in the system file explorer."""
        try:
            if not APP_LOG_DIR.exists():
                logger.warning(f"Log directory does not exist: {APP_LOG_DIR}")
                APP_LOG_DIR.mkdir(parents=True, exist_ok=True)
            
            log_url = QUrl.fromLocalFile(str(APP_LOG_DIR))
            QDesktopServices.openUrl(log_url)
        except Exception as e:
            logger.error(f"Failed to open log folder: {e}")
            # Minimal error feedback since this is about dialog
            self.logs_btn.setToolTip(f"Error: {str(e)}")

    def refresh_version_info(self) -> None:
        """Refresh version information manually."""
        if self.refresh_thread and self.refresh_thread.isRunning():
            return

        self.refresh_btn.setText(_('about.refreshing'))
        self.refresh_btn.setEnabled(False)

        # Perform refresh in a separate thread to avoid blocking UI
        class RefreshThread(QThread):
            finished = Signal(bool)

            def run(self):
                success = refresh_version_cache(force=True)
                self.finished.emit(success)

        self.refresh_thread = RefreshThread()
        self.refresh_thread.finished.connect(self.on_refresh_finished)
        self.refresh_thread.start()

    def _wait_for_worker_threads(self) -> None:
        """Wait for any active worker threads to finish before closing."""
        for thread in (self.refresh_thread, self.info_thread):
            if thread and thread.isRunning():
                thread.wait()

    def closeEvent(self, event) -> None:
        self._wait_for_worker_threads()
        super().closeEvent(event)

    def accept(self) -> None:
        self._wait_for_worker_threads()
        super().accept()

    def reject(self) -> None:
        self._wait_for_worker_threads()
        super().reject()

    def on_refresh_finished(self, success) -> None:
        """Handle refresh completion."""
        self.refresh_btn.setText(_('about.refresh'))
        self.refresh_btn.setEnabled(True)

        if success:
            self.update_system_info()
        else:
            # Show error message with proper styling
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle(_('about.refresh_failed'))
            msg_box.setText(_('about.refresh_failed_message'))
            msg_box.setWindowIcon(self.windowIcon())
            msg_box.setStyleSheet(
                """
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
            """
            )
            msg_box.exec()
