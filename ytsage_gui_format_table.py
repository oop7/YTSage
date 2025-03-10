from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QProgressBar, QLabel, QFileDialog,
                            QHeaderView, QStyle, QStyleFactory, QComboBox, QTextEdit, 
                            QDialog, QPlainTextEdit, QCheckBox, QButtonGroup, QScrollArea,
                            QSizePolicy)
from PySide6.QtCore import Qt, Signal, QObject, QThread
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap

class FormatSignals(QObject):
    format_update = Signal(list)

class FormatTableMixin:
    def setup_format_table(self):
        self.format_signals = FormatSignals()
        
        # Format table with improved styling
        self.format_table = QTableWidget()
        self.format_table.setColumnCount(8)
        self.format_table.setHorizontalHeaderLabels(['Select', 'Quality', 'Extension', 'Resolution', 'File Size', 'Codec', 'Audio', 'Notes'])
        
        # Set specific column widths and resize modes
        self.format_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # Select
        self.format_table.setColumnWidth(0, 50)  # Select column width
        
        self.format_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # Quality
        self.format_table.setColumnWidth(1, 100)  # Quality width
        
        self.format_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # Extension
        self.format_table.setColumnWidth(2, 80)  # Extension width
        
        self.format_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Resolution
        self.format_table.setColumnWidth(3, 100)  # Resolution width
        
        self.format_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # File Size
        self.format_table.setColumnWidth(4, 100)  # File Size width
        
        self.format_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Codec
        self.format_table.setColumnWidth(5, 150)  # Codec width
        
        self.format_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Audio
        self.format_table.setColumnWidth(6, 120)  # Audio width
        
        self.format_table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)  # Notes (will stretch)
        
        # Set vertical header (row numbers) visible to false
        self.format_table.verticalHeader().setVisible(False)
        
        # Set selection mode to no selection (since we're using checkboxes)
        self.format_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        self.format_table.setStyleSheet("""
            QTableWidget {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                gridline-color: #3d3d3d;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #3d3d3d;
            }
            QTableWidget::item:selected {
                background-color: transparent;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                padding: 5px;
                border: 1px solid #3d3d3d;
                font-weight: bold;
                color: white;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #2b2b2b;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #ff0000;
                background: #ff0000;
            }
            QWidget {
                background-color: transparent;
            }
        """)
        
        # Store format checkboxes and formats
        self.format_checkboxes = []
        self.all_formats = []
        
        # Set table size policies
        self.format_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Set minimum and maximum heights
        self.format_table.setMinimumHeight(200)
        
        # Connect the signal
        self.format_signals.format_update.connect(self._update_format_table)
        
        return self.format_table

    def filter_formats(self):
        if not hasattr(self, 'all_formats'):
            return
            
        # Clear current table
        self.format_table.setRowCount(0)
        self.format_checkboxes.clear()

        # Determine which formats to show
        filtered_formats = []

        if hasattr(self, 'video_button') and self.video_button.isChecked():
            filtered_formats.extend([f for f in self.all_formats
                                  if f.get('vcodec') != 'none'
                                  and f.get('filesize') is not None])

        if hasattr(self, 'audio_button') and self.audio_button.isChecked():
            filtered_formats.extend([f for f in self.all_formats
                                  if (f.get('vcodec') == 'none'
                                      or 'audio only' in f.get('format_note', '').lower())
                                  and f.get('acodec') != 'none'
                                  and f.get('filesize') is not None])

        # Sort formats by quality
        def get_quality(f):
            if f.get('vcodec') != 'none':
                res = f.get('resolution', '0x0').split('x')[-1]
                try:
                    return int(res)
                except ValueError:
                    return 0
            else:
                return f.get('abr', 0)

        filtered_formats.sort(key=get_quality, reverse=True)

        # Update table with filtered formats
        self.format_signals.format_update.emit(filtered_formats)

    def _update_format_table(self, formats):
        self.format_table.setRowCount(0)
        self.format_checkboxes.clear()
        
        # Find best quality format for recommendations
        best_video_size = max((f.get('filesize', 0) for f in formats if f.get('vcodec') != 'none'), default=0)
        
        for f in formats:
            row = self.format_table.rowCount()
            self.format_table.insertRow(row)
            
            # Add checkbox
            checkbox = QCheckBox()
            checkbox.format_id = str(f.get('format_id', ''))
            checkbox.clicked.connect(lambda checked, cb=checkbox: self.handle_checkbox_click(cb))
            self.format_checkboxes.append(checkbox)
            
            # Create a widget to center the checkbox
            checkbox_widget = QWidget()
            checkbox_widget.setStyleSheet("background-color: transparent;")
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_layout.setSpacing(0)
            self.format_table.setCellWidget(row, 0, checkbox_widget)

            # Quality (replacing Format ID)
            quality_text = self.get_quality_label(f)
            quality_item = QTableWidgetItem(quality_text)
            # Set color based on quality
            if "Best" in quality_text:
                quality_item.setForeground(QColor('#00ff00'))  # Green for best quality
            elif "High" in quality_text:
                quality_item.setForeground(QColor('#00cc00'))  # Light green for high quality
            elif "Medium" in quality_text:
                quality_item.setForeground(QColor('#ffaa00'))  # Orange for medium quality
            elif "Low" in quality_text:
                quality_item.setForeground(QColor('#ff5555'))  # Red for low quality
            self.format_table.setItem(row, 1, quality_item)

            # Extension
            self.format_table.setItem(row, 2, QTableWidgetItem(f.get('ext', '').upper()))

            # Resolution
            resolution = f.get('resolution', 'N/A')
            if f.get('vcodec') == 'none':
                resolution = 'Audio only'
            self.format_table.setItem(row, 3, QTableWidgetItem(resolution))

            # File Size
            filesize = f"{f.get('filesize', 0) / 1024 / 1024:.2f} MB"
            self.format_table.setItem(row, 4, QTableWidgetItem(filesize))

            # Codec
            if f.get('vcodec') == 'none':
                codec = f.get('acodec', 'N/A')
            else:
                codec = f"{f.get('vcodec', 'N/A')}"
                if f.get('acodec') != 'none':
                    codec += f" / {f.get('acodec', 'N/A')}"
            self.format_table.setItem(row, 5, QTableWidgetItem(codec))

            # Audio Status
            needs_audio = f.get('acodec') == 'none'
            audio_status = "Will merge audio" if needs_audio else "✓ Has Audio"
            audio_item = QTableWidgetItem(audio_status)
            if needs_audio:
                audio_item.setForeground(QColor('#ffa500'))
            self.format_table.setItem(row, 6, audio_item)

            # Add Notes column
            notes = self.get_format_notes(f, best_video_size)
            notes_item = QTableWidgetItem(notes)
            if "✨ Recommended" in notes:
                notes_item.setForeground(QColor('#00ff00'))  # Green for recommended
            elif "💾 Storage friendly" in notes:
                notes_item.setForeground(QColor('#00ccff'))  # Blue for storage friendly
            elif "📱 Mobile friendly" in notes:
                notes_item.setForeground(QColor('#ff9900'))  # Orange for mobile
            self.format_table.setItem(row, 7, notes_item)

    def handle_checkbox_click(self, clicked_checkbox):
        for checkbox in self.format_checkboxes:
            if checkbox != clicked_checkbox:
                checkbox.setChecked(False)

    def get_selected_format(self):
        for checkbox in self.format_checkboxes:
            if checkbox.isChecked():
                return checkbox.format_id
        return None

    def update_format_table(self, formats):
        self.all_formats = formats
        self.format_signals.format_update.emit(formats)

    def get_quality_label(self, format_info):
        """Determine quality label based on format information"""
        if format_info.get('vcodec') == 'none':
            # Audio quality
            abr = format_info.get('abr', 0)
            if abr >= 256:
                return "Best Audio"
            elif abr >= 192:
                return "High Audio"
            elif abr >= 128:
                return "Medium Audio"
            else:
                return "Low Audio"
        else:
            # Video quality
            height = 0
            resolution = format_info.get('resolution', '')
            if resolution:
                try:
                    height = int(resolution.split('x')[1])
                except:
                    pass
            
            if height >= 2160:
                return "Best (4K)"
            elif height >= 1440:
                return "Best (2K)"
            elif height >= 1080:
                return "High (1080p)"
            elif height >= 720:
                return "High (720p)"
            elif height >= 480:
                return "Medium (480p)"
            else:
                return "Low Quality"

    def get_format_notes(self, format_info, best_video_size):
        """Generate helpful notes about the format"""
        if format_info.get('vcodec') == 'none':
            # Audio format
            abr = format_info.get('abr', 0)
            if abr >= 256:
                return "✨ Recommended for music"
            elif abr >= 128:
                return "📱 Mobile friendly"
            return "💾 Storage friendly"
        else:
            # Video format
            height = 0
            resolution = format_info.get('resolution', '')
            if resolution:
                try:
                    height = int(resolution.split('x')[1])
                except:
                    pass
            
            filesize = format_info.get('filesize', 0)
            
            notes = []
            
            # Resolution-based recommendations
            if height >= 1440:  # 2K or 4K
                if filesize == best_video_size:
                    notes.append("✨ Recommended for high-end displays")
                else:
                    notes.append("🖥️ Best for large screens")
            elif height == 1080:
                if 'avc1' in format_info.get('vcodec', '').lower():
                    notes.append("✨ Recommended for most devices")
                else:
                    notes.append("👍 Good balance")
            elif height == 720:
                notes.append("📱 Mobile friendly")
            else:
                notes.append("💾 Storage friendly")
            
            # Codec-based notes
            if 'av1' in format_info.get('vcodec', '').lower():
                notes.append("Better compression")
            elif 'vp9' in format_info.get('vcodec', '').lower():
                notes.append("Good for Chrome")
            
            # File size note for large files
            if filesize > 100 * 1024 * 1024:  # More than 100MB
                notes.append("Large file")
            
            return " • ".join(notes)