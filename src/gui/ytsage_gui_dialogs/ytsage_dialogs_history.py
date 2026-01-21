"""
History Dialog for YTSage application.
Displays download history with thumbnails and provides options to redownload or remove entries.
"""

import os
import subprocess
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import requests
from PIL import Image
from PySide6.QtCore import Qt, QSize, Signal, QThread, QTimer
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QWidget,
    QFrame,
    QMenu,
    QMessageBox,
    QSizePolicy,
    QProgressBar,
)

from src.utils.ytsage_history_manager import HistoryManager
from src.utils.ytsage_constants import APP_THUMBNAILS_DIR, SUBPROCESS_CREATIONFLAGS
from src.utils.ytsage_localization import _
from src.utils.ytsage_logger import logger

if TYPE_CHECKING:
    from src.gui.ytsage_gui_main import YTSageApp


class HistoryLoaderThread(QThread):
    """Thread to load history and pre-fetch thumbnails."""
    
    entries_loaded = Signal(list)
    thumbnail_loaded = Signal(str)
    
    def run(self):
        try:
            # HistoryManager uses get_all_entries, not get_all
            entries = HistoryManager.get_all_entries()
            
            # Emit entries immediately so UI shows up
            self.entries_loaded.emit(entries)
            
            # Pre-fetch thumbnails in background
            for entry in entries:
                thumbnail_url = entry.get("thumbnail_url")
                entry_id = entry.get("id", "")
                
                if not thumbnail_url or not entry_id:
                    continue
                    
                thumbnail_filename = f"{entry_id}.jpg"
                thumbnail_path = APP_THUMBNAILS_DIR / thumbnail_filename
                
                # If not exists, download it
                if not thumbnail_path.exists():
                    try:
                        response = requests.get(thumbnail_url, timeout=5)
                        if response.status_code == 200:
                            APP_THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
                            
                            image = Image.open(BytesIO(response.content))
                            image.save(thumbnail_path, "JPEG", quality=95, optimize=True)
                            self.thumbnail_loaded.emit(entry_id)
                    except Exception as e:
                        logger.debug(f"Error caching thumbnail in background: {e}")
            
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            self.entries_loaded.emit([])


class HistoryEntryWidget(QFrame):
    """Widget representing a single history entry."""
    
    remove_requested = Signal(str)  # Emit entry ID when remove is requested
    redownload_requested = Signal(dict)  # Emit entry data when redownload is requested
    
    def __init__(self, entry: dict, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.entry_id = entry.get("id", "")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI for this history entry."""
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: #1d1e22;
                border: 1px solid #2a2d36;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            }
            QFrame:hover {
                background-color: #252830;
                border-color: #3a3d46;
            }
        """)
        
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Thumbnail - Larger size to utilize available space
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(280, 158)  # 16:9 ratio, larger to fill space
        self.thumbnail_label.setStyleSheet("""
            QLabel {
                border: 2px solid #3d3d3d;
                border-radius: 6px;
                background-color: #15181b;
            }
        """)
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setScaledContents(True)
        
        # Load thumbnail
        self.load_thumbnail()
        
        main_layout.addWidget(self.thumbnail_label, alignment=Qt.AlignmentFlag.AlignTop)
        
        # Info section
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        # Title
        title = self.entry.get("title", _("video_info.unknown_title"))
        self.title_label = QLabel(title)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
            }
        """)
        info_layout.addWidget(self.title_label)
        
        # Channel (if available)
        channel = self.entry.get("channel")
        if channel:
            channel_label = QLabel(f"{_('video_info.channel')}: {channel}")
            channel_label.setStyleSheet("color: #cccccc; font-size: 12px;")
            info_layout.addWidget(channel_label)
        
        # Download date
        download_date = self.entry.get("download_date", "")
        if download_date:
            try:
                dt = datetime.fromisoformat(download_date)
                date_str = dt.strftime("%Y-%m-%d %H:%M")
                date_label = QLabel(_("history.downloaded_on", date=date_str))
                date_label.setStyleSheet("color: #aaaaaa; font-size: 11px;")
                info_layout.addWidget(date_label)
            except Exception as e:
                logger.debug(f"Error parsing date: {e}")
        
        # File size and type
        file_size = self.entry.get("file_size", 0)
        is_audio = self.entry.get("is_audio_only", False)
        
        size_type_layout = QHBoxLayout()
        
        # File type badge
        type_badge = QLabel(_("history.audio_download") if is_audio else _("history.video_download"))
        type_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {'#c90000' if not is_audio else '#0066cc'};
                color: white;
                padding: 2px 8px;
                border-radius: 3px;
                font-size: 10px;
                font-weight: bold;
            }}
        """)
        size_type_layout.addWidget(type_badge)
        
        # File size
        if file_size > 0:
            size_str = self.format_file_size(file_size)
            size_label = QLabel(_("history.file_size", size=size_str))
            size_label.setStyleSheet("color: #aaaaaa; font-size: 11px;")
            size_type_layout.addWidget(size_label)
        
        size_type_layout.addStretch()
        info_layout.addLayout(size_type_layout)
        
        info_layout.addStretch()
        
        main_layout.addLayout(info_layout, 1)
        
        # Three-dot menu button
        self.menu_button = QPushButton("⋮")
        self.menu_button.setFixedSize(40, 40)
        self.menu_button.setStyleSheet("""
            QPushButton {
                background-color: #2a2d36;
                border: none;
                border-radius: 20px;
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a3d46;
            }
            QPushButton:pressed {
                background-color: #c90000;
            }
        """)
        self.menu_button.clicked.connect(self.show_menu)
        
        main_layout.addWidget(self.menu_button, alignment=Qt.AlignmentFlag.AlignTop)
    
    def load_thumbnail(self):
        """Load and display the thumbnail."""
        thumbnail_url = self.entry.get("thumbnail_url")
        
        if not thumbnail_url:
            self.set_placeholder_thumbnail()
            return
        
        # Check if thumbnail is cached
        thumbnail_filename = f"{self.entry_id}.jpg"
        thumbnail_path = APP_THUMBNAILS_DIR / thumbnail_filename
        
        if thumbnail_path.exists():
            try:
                pixmap = QPixmap(str(thumbnail_path))
                if not pixmap.isNull():
                    # Don't scale here, let setScaledContents handle it
                    self.thumbnail_label.setPixmap(pixmap)
                    return
            except Exception as e:
                logger.debug(f"Error loading cached thumbnail: {e}")
        
        # If not in cache, just set placeholder. 
        # Background thread will download it and notify parent to reload.
        self.set_placeholder_thumbnail()

    def reload_thumbnail(self):
        """Reload thumbnail from cache (called when background download finishes)."""
        self.load_thumbnail()
    
    def set_placeholder_thumbnail(self):
        """Set a placeholder when thumbnail is not available."""
        self.thumbnail_label.setText("📹" if not self.entry.get("is_audio_only") else "🎵")
        self.thumbnail_label.setStyleSheet("""
            QLabel {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #15181b;
                color: #666666;
                font-size: 48px;
            }
        """)
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def show_menu(self):
        """Show the context menu with options."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2a2d36;
                border: 1px solid #3a3d46;
                color: white;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #c90000;
            }
        """)
        
        # Open file location
        open_action = menu.addAction("📁 " + _("history.open_location"))
        open_action.triggered.connect(self.open_file_location)
        
        # Redownload
        redownload_action = menu.addAction("⬇️ " + _("history.redownload"))
        redownload_action.triggered.connect(self.redownload)
        
        menu.addSeparator()
        
        # Remove from history
        remove_action = menu.addAction("🗑️ " + _("history.remove"))
        remove_action.triggered.connect(self.remove_from_history)
        
        # Show menu at button position
        menu.exec(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))
    
    def open_file_location(self):
        """Open the file location in the system file explorer."""
        file_path = Path(self.entry.get("file_path", ""))
        
        if not file_path.exists():
            QMessageBox.warning(
                self,
                _("history.file_not_found"),
                _("history.file_not_found_message", path=str(file_path))
            )
            return
        
        try:
            # On Windows, use explorer with /select to highlight the file
            if os.name == "nt":
                subprocess.run(['explorer', '/select,', str(file_path)], creationflags=SUBPROCESS_CREATIONFLAGS)
            # On macOS, use open with -R to reveal in Finder
            elif subprocess.sys.platform == "darwin":
                subprocess.run(['open', '-R', str(file_path)])
            # On Linux, try to open the folder
            else:
                folder_path = file_path.parent
                subprocess.run(['xdg-open', str(folder_path)])
            
            logger.info(f"Opened file location: {file_path}")
        except Exception as e:
            logger.exception(f"Error opening file location: {e}")
            QMessageBox.warning(self, "Error", f"Could not open file location: {str(e)}")
    
    def redownload(self):
        """Request redownload of this entry."""
        reply = QMessageBox.question(
            self,
            _("history.redownload_confirm_title"),
            _("history.redownload_confirm_message", title=self.entry.get("title", "")),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.redownload_requested.emit(self.entry)
    
    def remove_from_history(self):
        """Request removal of this entry from history."""
        reply = QMessageBox.question(
            self,
            _("history.remove_confirm_title"),
            _("history.remove_confirm_message", title=self.entry.get("title", "")),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.remove_requested.emit(self.entry_id)


class HistoryDialog(QDialog):
    """Dialog to display and manage download history."""
    
    redownload_requested = Signal(dict)  # Signal to request redownload in main window
    
    def __init__(self, parent: Optional["YTSageApp"] = None):
        super().__init__(parent)
        self.parent_app = parent
        self.entry_widgets = []
        self.entry_widgets_map = {}  # Map entry_id -> widget
        
        self.setup_ui()
        
        # Show loading state initially
        self.show_loading_state()
        
        # Start loading history in background after a short delay
        # to ensure the dialog is shown first
        QTimer.singleShot(100, self.start_loading_history)
        
    def start_loading_history(self):
        """Start the background thread to load history."""
        self.loader_thread = HistoryLoaderThread()
        self.loader_thread.entries_loaded.connect(self.on_history_loaded)
        self.loader_thread.thumbnail_loaded.connect(self.update_entry_thumbnail)
        self.loader_thread.start()
        
    def on_history_loaded(self, entries):
        """Called when history is loaded from background thread."""
        self.load_history_entries(entries)

    def update_entry_thumbnail(self, entry_id: str):
        """Called when a thumbnail is downloaded in the background."""
        if entry_id in self.entry_widgets_map:
            self.entry_widgets_map[entry_id].reload_thumbnail()
    
    def setup_ui(self):
        """Setup the dialog UI."""
        self.setWindowTitle(_("history.title"))
        self.setMinimumSize(700, 500)
        self.resize(850, 600)
        
        # Set window flags
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with title and buttons
        header_layout = QHBoxLayout()
        
        title_label = QLabel(_("history.title"))
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: white;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Clear all button
        self.clear_all_btn = QPushButton(_("history.clear_all"))
        self.clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #c90000;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QPushButton:pressed {
                background-color: #800000;
            }
        """)
        self.clear_all_btn.clicked.connect(self.clear_all_history)
        header_layout.addWidget(self.clear_all_btn)
        
        layout.addLayout(header_layout)
        
        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(_("history.search_placeholder"))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
                color: #ffffff;
                font-size: 13px;
            }
        """)
        self.search_input.textChanged.connect(self.filter_history)
        layout.addWidget(self.search_input)
        
        # Scroll area for history entries
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        # Container for history entries
        self.history_container = QWidget()
        self.history_layout = QVBoxLayout(self.history_container)
        self.history_layout.setSpacing(10)
        self.history_layout.setContentsMargins(0, 0, 0, 0)
        self.history_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll_area.setWidget(self.history_container)
        layout.addWidget(scroll_area)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #15181b;
            }
            QLabel {
                color: #ffffff;
            }
        """)
    
    def clear_history_list(self):
        """Clear existing history widgets."""
        for widget in self.entry_widgets:
            widget.deleteLater()
        self.entry_widgets.clear()
        self.entry_widgets_map.clear()

    def show_loading_state(self):
        """Show loading indicator."""
        # Clear existing content
        self.clear_history_list()
        
        loading_widget = QWidget()
        loading_layout = QVBoxLayout(loading_widget)
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        spinner_label = QLabel("⏳")  # Simple spinner icon
        spinner_label.setStyleSheet("font-size: 48px; color: #c90000;")
        spinner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_layout.addWidget(spinner_label)
        
        # text_label removed as per user request
        
        self.history_layout.addWidget(loading_widget)
        self.entry_widgets.append(loading_widget)
        
        self.status_label.setText("Loading...")
        self.clear_all_btn.setEnabled(False)

    def load_history(self):
        """Load and display history entries."""
        if hasattr(self, 'history_container'):
             self.show_loading_state()
             self.start_loading_history()

    def load_history_entries(self, entries):
        """Populate the history list with entries."""
        self.clear_history_list()
        
        if not entries:
            self.show_empty_state()
            return
        
        # Create widgets for each entry
        for entry in entries:
            widget = HistoryEntryWidget(entry, self.history_container)
            widget.remove_requested.connect(self.remove_entry)
            widget.redownload_requested.connect(self.handle_redownload)
            
            self.history_layout.addWidget(widget)
            
            # Map widget by ID for updates
            entry_id = entry.get("id")
            if entry_id:
                self.entry_widgets_map[entry_id] = widget
            self.entry_widgets.append(widget)
        
        # Update status
        count = len(entries)
        if count == 1:
            status_text = _("history.one_entry")
        else:
            status_text = _("history.entries_count", count=count)
        self.status_label.setText(status_text)
        self.clear_all_btn.setEnabled(True)
    
    def show_empty_state(self):
        """Show empty state when there's no history."""
        empty_widget = QWidget()
        empty_layout = QVBoxLayout(empty_widget)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel("📂")
        icon_label.setStyleSheet("font-size: 64px; color: #555555;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(icon_label)
        
        title_label = QLabel(_("history.no_history"))
        title_label.setStyleSheet("font-size: 16px; color: #888888; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(title_label)
        
        desc_label = QLabel(_("history.no_history_description"))
        desc_label.setStyleSheet("font-size: 13px; color: #666666;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(desc_label)
        
        self.history_layout.addWidget(empty_widget)
        self.entry_widgets.append(empty_widget)
        
        self.status_label.setText("")
        self.clear_all_btn.setEnabled(False)
    
    def filter_history(self, query: str):
        """Filter history entries based on search query."""
        if not query:
            # Show all entries
            for widget in self.entry_widgets:
                widget.show()
            return
        
        # Hide/show based on query
        query_lower = query.lower()
        visible_count = 0
        
        for widget in self.entry_widgets:
            if isinstance(widget, HistoryEntryWidget):
                title = (widget.entry.get("title") or "").lower()
                channel = (widget.entry.get("channel") or "").lower()
                
                if query_lower in title or query_lower in channel:
                    widget.show()
                    visible_count += 1
                else:
                    widget.hide()
    
    def remove_entry(self, entry_id: str):
        """Remove an entry from history."""
        success = HistoryManager.remove_entry(entry_id)
        
        if success:
            # Reload history
            self.load_history()
            logger.info(f"Removed entry from history: {entry_id}")
        else:
            QMessageBox.warning(self, "Error", "Failed to remove entry from history")
    
    def clear_all_history(self):
        """Clear all history entries."""
        reply = QMessageBox.question(
            self,
            _("history.clear_confirm_title"),
            _("history.clear_confirm_message"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            count = HistoryManager.clear_history()
            self.load_history()
            logger.info(f"Cleared all history: {count} entries")
    
    def handle_redownload(self, entry: dict):
        """Handle redownload request."""
        # Emit signal to parent window
        self.redownload_requested.emit(entry)
        
        # Close dialog
        self.accept()
