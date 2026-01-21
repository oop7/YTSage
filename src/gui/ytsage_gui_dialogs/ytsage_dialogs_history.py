"""
History Dialog for YTSage application.
Displays download history with thumbnails using a virtualized list for performance.
"""

import os
import subprocess
import json
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Optional, List, Any, Dict

import requests
from PIL import Image
from PySide6.QtCore import (
    Qt, QSize, Signal, QThread, QTimer, QAbstractListModel, 
    QModelIndex, QRect, QPoint, QEvent
)
from PySide6.QtGui import (
    QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen,
    QMouseEvent, QDesktopServices, QAction, QCursor, QPainterPath
)
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListView,
    QWidget,
    QMenu,
    QMessageBox,
    QStyledItemDelegate,
    QStyle,
    QApplication
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
    thumbnail_loaded = Signal(str, bytes) # entry_id, image_bytes
    
    def run(self):
        try:
            # Load entries from DB
            entries = HistoryManager.get_all_entries()
            self.entries_loaded.emit(entries)
            
            # Background thumbnail loader
            for entry in entries:
                if self.isInterruptionRequested():
                    break
                    
                thumbnail_url = entry.get("thumbnail_url")
                entry_id = entry.get("id", "")
                
                if not thumbnail_url or not entry_id:
                    continue
                    
                thumbnail_filename = f"{entry_id}.jpg"
                thumbnail_path = APP_THUMBNAILS_DIR / thumbnail_filename
                
                if not thumbnail_path.exists():
                    try:
                        response = requests.get(thumbnail_url, timeout=5)
                        if response.status_code == 200:
                            APP_THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
                            
                            # Optimize image before saving
                            img_io = BytesIO(response.content)
                            image = Image.open(img_io)
                            
                            # Save to disk
                            image.save(thumbnail_path, "JPEG", quality=90, optimize=True)
                            
                            # Emit bytes for memory cache
                            self.thumbnail_loaded.emit(entry_id, response.content)
                    except Exception as e:
                        logger.debug(f"Error caching thumbnail: {e}")
                        
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            self.entries_loaded.emit([])


class HistoryModel(QAbstractListModel):
    """List Model for History Entries."""
    
    EntryRole = Qt.ItemDataRole.UserRole + 1
    IdRole = Qt.ItemDataRole.UserRole + 2
    ThumbnailRole = Qt.ItemDataRole.UserRole + 3

    def __init__(self, entries=None, parent=None):
        super().__init__(parent)
        self._entries = entries or []
        self.thumbnail_cache = {}  # Map entry_id -> QPixmap

    def rowCount(self, parent=QModelIndex()):
        return len(self._entries)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._entries)):
            return None
        
        entry = self._entries[index.row()]
        entry_id = entry.get("id")

        if role == self.EntryRole:
            return entry
        
        elif role == self.IdRole:
            return entry_id

        elif role == self.ThumbnailRole:
            return self.thumbnail_cache.get(entry_id)

        elif role == Qt.ItemDataRole.DisplayRole:
            return entry.get("title", "")
            
        return None

    def update_entries(self, entries):
        self.beginResetModel()
        self._entries = entries
        self.endResetModel()

    def remove_item(self, row):
        if 0 <= row < len(self._entries):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._entries[row]
            self.endRemoveRows()
            
    def update_thumbnail(self, entry_id, pixmap):
        """Update cache and notify view."""
        self.thumbnail_cache[entry_id] = pixmap
        # Find index for this ID
        for i, entry in enumerate(self._entries):
            if entry.get("id") == entry_id:
                idx = self.index(i)
                self.dataChanged.emit(idx, idx, [self.ThumbnailRole])
                break


class HistoryDelegate(QStyledItemDelegate):
    """Delegate to render history cards similar to the widgets."""
    
    menu_clicked = Signal(QModelIndex, QPoint) # Signal for menu click
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.padding = 10
        self.thumb_width = 240
        self.thumb_height = 135
        # Increased card height to accommodate spacing
        self.card_height = 175
        # Define margins for spacing between cards
        self.h_margin = 10
        self.v_margin = 8
    
    def sizeHint(self, option, index):
        return QSize(option.rect.width(), self.card_height)

    def paint(self, painter, option, index):
        entry = index.data(HistoryModel.EntryRole)
        if not entry:
            return
            
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = option.rect
        # Apply margins for spacing
        card_rect = rect.adjusted(self.h_margin, self.v_margin, -self.h_margin, -self.v_margin)
        
        is_hover = option.state & QStyle.StateFlag.State_MouseOver
        bg_color = QColor("#252830") if is_hover else QColor("#1d1e22")
        border_color = QColor("#3a3d46") if is_hover else QColor("#2a2d36")
        
        # Draw Card
        path = QPainterPath()
        path.addRoundedRect(card_rect, 8, 8)
        
        painter.fillPath(path, QBrush(bg_color))
        painter.setPen(QPen(border_color, 1))
        painter.drawPath(path)
        
        # Draw Thumbnail
        thumb_rect = QRect(
            card_rect.left() + 10, 
            card_rect.top() + 10, 
            self.thumb_width, 
            self.thumb_height
        )
        
        pixmap = index.data(HistoryModel.ThumbnailRole)
        if pixmap and not pixmap.isNull():
            scaled = pixmap.scaled(
                thumb_rect.size(), 
                Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                Qt.TransformationMode.SmoothTransformation
            )
            # Clip to rect
            painter.setClipRect(thumb_rect)
            painter.drawPixmap(thumb_rect.topLeft(), scaled)
            painter.setClipping(False)
        else:
            painter.fillRect(thumb_rect, QColor("#15181b"))
            painter.setPen(QPen(QColor("#666666")))
            icon_char = "🎵" if entry.get("is_audio_only") else "📹"
            painter.setFont(QFont("Segoe UI Emoji", 24))
            painter.drawText(thumb_rect, Qt.AlignmentFlag.AlignCenter, icon_char)

        # Draw Border around thumb
        painter.setPen(QPen(QColor("#3d3d3d"), 2))
        painter.drawRect(thumb_rect)

        # Text Area
        text_x = thumb_rect.right() + 12
        text_width = card_rect.right() - text_x - 85 # Leave even more space for the larger 60px button
        
        # Title
        title_rect = QRect(text_x, thumb_rect.top(), text_width, 50)
        painter.setPen(QColor("#ffffff"))
        font_title = QFont()
        font_title.setBold(True)
        font_title.setPixelSize(14)
        painter.setFont(font_title)
        
        # Use simple alignment flags
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap, entry.get("title", ""))
        
        current_y = title_rect.bottom() + 5
        
        # Channel
        channel = entry.get("channel")
        if channel:
            painter.setPen(QColor("#cccccc"))
            font_meta = QFont()
            font_meta.setPixelSize(12)
            painter.setFont(font_meta)
            painter.drawText(text_x, current_y, f"{_('video_info.channel')}: {channel}")
            current_y += 18

        # Date
        date_str = entry.get("download_date", "")[:16].replace('T', ' ')
        if date_str:
            painter.setPen(QColor("#aaaaaa"))
            painter.setFont(QFont("Arial", 11))
            painter.drawText(text_x, current_y, f"{_('history.downloaded_on', date=date_str)}")
            current_y += 25
            
        # Badge
        is_audio = entry.get("is_audio_only", False)
        badge_text = _("history.audio_download") if is_audio else _("history.video_download")
        badge_color = QColor("#0066cc") if is_audio else QColor("#c90000")
        
        badge_rect = QRect(text_x, current_y, 80, 20)
        painter.setBrush(QBrush(badge_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(badge_rect, 3, 3)
        
        painter.setPen(QColor("white"))
        font_badge = QFont()
        font_badge.setBold(True)
        font_badge.setPixelSize(10)
        painter.setFont(font_badge)
        painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, badge_text)
        
        # File Size
        file_size = entry.get("file_size", 0)
        if file_size > 0:
            size_str = self.format_file_size(file_size)
            painter.setPen(QColor("#aaaaaa"))
            painter.setFont(QFont("Arial", 11))
            painter.drawText(badge_rect.right() + 10, current_y + 14, size_str)

        # Menu Button
        menu_rect = self.get_menu_rect(card_rect)
        
        # Check hover on menu button specifically
        mouse_pos = QCursor.pos()
        if option.widget:
            mouse_pos = option.widget.mapFromGlobal(mouse_pos)
            
        if menu_rect.contains(mouse_pos):
             painter.setPen(QColor("#c90000")) 
        else:
             painter.setPen(QColor("#ffffff"))

        painter.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        painter.drawText(menu_rect, Qt.AlignmentFlag.AlignCenter, "⋮")
        
        painter.restore()

    def get_menu_rect(self, card_rect):
        # Widen the clickable area significantly (60x50) and shift slightly left
        # to fix "left side not working" issues.
        w = 60
        h = 50
        margin_right = 5
        margin_top = 5
        return QRect(
            card_rect.right() - w - margin_right, 
            card_rect.top() + margin_top, 
            w, 
            h
        )

    def editorEvent(self, event, model, option, index):
        """Handle mouse clicks."""
        if event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton:
                # Use same margins as paint to ensure hit consistency
                card_rect = option.rect.adjusted(self.h_margin, self.v_margin, -self.h_margin, -self.v_margin)
                menu_rect = self.get_menu_rect(card_rect)
                
                if menu_rect.contains(event.pos()):
                    self.menu_clicked.emit(index, event.globalPos())
                    return True
        
        return super().editorEvent(event, model, option, index)

    def format_file_size(self, size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"


class HistoryDialog(QDialog):
    """Dialog to display and manage download history."""
    
    redownload_requested = Signal(dict)
    
    def __init__(self, parent: Optional["YTSageApp"] = None):
        super().__init__(parent)
        self.parent_app = parent
        
        self.setup_ui()
        self.show_loading_state()
        
        QTimer.singleShot(100, self.start_loading_history)
        
    def setup_ui(self):
        self.setWindowTitle(_("history.title"))
        self.resize(850, 600)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self.setStyleSheet("""
            QDialog { background-color: #15181b; }
            QLabel { color: #ffffff; }
        """)
        
        layout = QVBoxLayout(self)
        
        # --- Header ---
        header = QHBoxLayout()
        title = QLabel(_("history.title"))
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        
        self.clear_btn = QPushButton(_("history.clear_all"))
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #c90000; color: white; padding: 6px 12px;
                border: none; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #a50000; }
            QPushButton:disabled { background-color: #555555; color: #aaaaaa; }
        """)
        self.clear_btn.clicked.connect(self.clear_all_history)
        header.addWidget(self.clear_btn)
        layout.addLayout(header)
        
        # --- Search ---
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(_("history.search_placeholder"))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px; border: 2px solid #2a2d36; border-radius: 4px;
                background-color: #1b2021; color: white;
            }
        """)
        self.search_input.textChanged.connect(self.filter_history)
        layout.addWidget(self.search_input)
        
        # --- List View ---
        self.list_view = QListView()
        self.list_view.setStyleSheet("""
            QListView {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListView::item {
                border: none;
                background: transparent;
            }
        """)
        self.list_view.setVerticalScrollMode(QListView.ScrollMode.ScrollPerPixel)
        self.list_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list_view.setUniformItemSizes(True)
        self.list_view.setSelectionMode(QListView.SelectionMode.NoSelection)
        self.list_view.setMouseTracking(True)
        self.list_view.setResizeMode(QListView.ResizeMode.Adjust)
        
        self.model = HistoryModel([], self)
        self.list_view.setModel(self.model)
        
        self.delegate = HistoryDelegate(self.list_view)
        self.delegate.menu_clicked.connect(self.show_context_menu)
        self.list_view.setItemDelegate(self.delegate)
        
        self.list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.on_context_menu_requested)
        
        layout.addWidget(self.list_view)
        
        # --- Status ---
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        layout.addWidget(self.status_label)

    def show_loading_state(self):
        self.status_label.setText("Loading history...")
        self.clear_btn.setEnabled(False)

    def start_loading_history(self):
        self.loader_thread = HistoryLoaderThread()
        self.loader_thread.entries_loaded.connect(self.on_entries_loaded)
        self.loader_thread.thumbnail_loaded.connect(self.on_thumbnail_loaded)
        self.loader_thread.start()

    def on_entries_loaded(self, entries):
        self.model.update_entries(entries)
        
        count = len(entries)
        if count == 0:
            self.status_label.setText(_("history.no_history"))
            self.clear_btn.setEnabled(False)
        else:
            self.status_label.setText(_("history.entries_count", count=count))
            self.clear_btn.setEnabled(True)
            
        self.load_cached_thumbnails(entries)

    def load_cached_thumbnails(self, entries):
        for entry in entries:
            eid = entry.get("id")
            if not eid: continue
            
            p = APP_THUMBNAILS_DIR / f"{eid}.jpg"
            if p.exists():
                pix = QPixmap(str(p))
                if not pix.isNull():
                    self.model.thumbnail_cache[eid] = pix

    def on_thumbnail_loaded(self, entry_id, data_bytes):
        pixmap = QPixmap()
        pixmap.loadFromData(data_bytes)
        if not pixmap.isNull():
            self.model.update_thumbnail(entry_id, pixmap)

    def on_context_menu_requested(self, pos):
        index = self.list_view.indexAt(pos)
        if index.isValid():
            global_pos = self.list_view.mapToGlobal(pos)
            self.show_context_menu(index, global_pos)

    def show_context_menu(self, index, global_pos):
        entry = index.data(HistoryModel.EntryRole)
        if not entry: return
        
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2a2d36; border: 1px solid #3a3d46; color: white;
            }
            QMenu::item {
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background-color: #c90000;
            }
        """)
        
        act_open = menu.addAction("📁 " + _("history.open_location"))
        act_redownload = menu.addAction("⬇️ " + _("history.redownload"))
        menu.addSeparator()
        act_remove = menu.addAction("🗑️ " + _("history.remove"))
        
        action = menu.exec(global_pos)
        
        if action == act_open:
            self.open_file_location(entry)
        elif action == act_redownload:
            self.redownload_entry(entry)
        elif action == act_remove:
            self.remove_entry(index)

    def open_file_location(self, entry):
        path_str = entry.get("file_path", "")
        if not path_str: return
        
        path = Path(path_str)
        if not path.exists():
            QMessageBox.warning(self, "Error", f"File not found: {path}")
            return
            
        try:
            if os.name == "nt":
                subprocess.run(['explorer', '/select,', str(path)], creationflags=SUBPROCESS_CREATIONFLAGS)
            elif subprocess.sys.platform == "darwin":
                subprocess.run(['open', '-R', str(path)])
            else:
                folder_path = path.parent
                subprocess.run(['xdg-open', str(folder_path)])
        except Exception as e:
            logger.error(f"Failed to open file: {e}")

    def redownload_entry(self, entry):
        reply = QMessageBox.question(
            self,
            _("history.redownload_confirm_title"),
            _("history.redownload_confirm_message", title=entry.get("title")),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.redownload_requested.emit(entry)
            self.accept()

    def remove_entry(self, index):
        entry = index.data(HistoryModel.EntryRole)
        reply = QMessageBox.question(
            self,
            _("history.remove_confirm_title"),
            _("history.remove_confirm_message", title=entry.get("title")),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if HistoryManager.remove_entry(entry.get("id")):
                self.model.remove_item(index.row())
                self.status_label.setText(
                    _("history.entries_count", count=self.model.rowCount())
                )

    def clear_all_history(self):
        reply = QMessageBox.question(
            self,
            _("history.clear_confirm_title"),
            _("history.clear_confirm_message"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            HistoryManager.clear_history()
            self.model.update_entries([])
            self.clear_btn.setEnabled(False)
            self.status_label.setText(_("history.no_history"))

    def filter_history(self, query):
        results = HistoryManager.search_entries(query)
        self.model.update_entries(results)
        self.load_cached_thumbnails(results)
