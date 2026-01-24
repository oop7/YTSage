from typing import TYPE_CHECKING, cast

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QColor, QFontMetrics
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QHeaderView, QSizePolicy, QTableWidget, QTableWidgetItem, QWidget

from src.utils.ytsage_localization import _

if TYPE_CHECKING:
    from src.gui.ytsage_gui_main import YTSageApp


class FormatSignals(QObject):
    format_update = Signal(list)


class FormatTableMixin:
    def _calculate_column_width(self, label: str, min_width: int, padding: int) -> int:
        """Calculate responsive column width based on header text length."""
        self = cast("YTSageApp", self)
        font_metrics = QFontMetrics(self.format_table.horizontalHeader().font())
        text_width = font_metrics.horizontalAdvance(label)
        return max(text_width + padding, min_width)

    def _apply_column_widths(self, header_labels: list[str], is_playlist_mode: bool = False) -> None:
        """Apply responsive column widths to format table."""
        self = cast("YTSageApp", self)
        
        if is_playlist_mode:
            # Playlist mode: 6 columns
            configs = [
                {"min_width": 70, "padding": 40},   # Select
                {"min_width": 100, "padding": 30},  # Quality
                {"min_width": 100, "padding": 30},  # Resolution
                {"min_width": 60, "padding": 30},   # FPS
                {"min_width": 60, "padding": 30},   # HDR
                {"min_width": 100, "padding": 30},  # Audio
            ]
            
            self.format_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            calculated_width = self._calculate_column_width(header_labels[0], configs[0]["min_width"], configs[0]["padding"])
            self.format_table.setColumnWidth(0, calculated_width)
            
            # Remaining columns stretch
            for i in range(1, 6):
                self.format_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        else:
            # Normal mode: 9 columns
            configs = [
                {"min_width": 70, "padding": 40, "stretch": False},   # Select - fixed
                {"min_width": 100, "padding": 30, "stretch": True},   # Quality - stretch
                {"min_width": 85, "padding": 30, "stretch": False},   # Extension - fixed
                {"min_width": 100, "padding": 30, "stretch": True},   # Resolution - stretch
                {"min_width": 90, "padding": 30, "stretch": True},    # File Size - stretch
                {"min_width": 100, "padding": 30, "stretch": True},   # Codec - stretch
                {"min_width": 100, "padding": 30, "stretch": True},   # Audio - stretch
                {"min_width": 60, "padding": 30, "stretch": False},   # FPS - fixed
                {"min_width": 60, "padding": 30, "stretch": False},   # HDR - fixed
            ]
            
            # Apply column widths with mixed fixed and stretch modes
            for col_index, (label, config) in enumerate(zip(header_labels, configs)):
                calculated_width = self._calculate_column_width(label, config["min_width"], config["padding"])
                
                if config["stretch"]:
                    # Stretchable columns for flexible content
                    self.format_table.horizontalHeader().setSectionResizeMode(col_index, QHeaderView.ResizeMode.Stretch)
                else:
                    # Fixed columns for consistent sizing
                    self.format_table.horizontalHeader().setSectionResizeMode(col_index, QHeaderView.ResizeMode.Fixed)
                    self.format_table.setColumnWidth(col_index, calculated_width)

    def setup_format_table(self) -> QTableWidget:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        self.format_signals = FormatSignals()
        # Format table with improved styling
        self.format_table = QTableWidget()
        self.format_table.setColumnCount(9)
        
        # Get translated header labels
        header_labels = [
            _("formats.select"),
            _("formats.quality"),
            _("formats.extension"),
            _("formats.resolution"),
            _("formats.file_size"),
            _("formats.codec"),
            _("formats.audio"),
            _("formats.fps"),
            _("formats.hdr"),
        ]
        self.format_table.setHorizontalHeaderLabels(header_labels)

        # Enable alternating row colors
        self.format_table.setAlternatingRowColors(True)

        # Apply responsive column widths
        self._apply_column_widths(header_labels, is_playlist_mode=False)

        # Set vertical header (row numbers) visible to false
        self.format_table.verticalHeader().setVisible(False)

        # Set selection mode to no selection (since we're using checkboxes)
        self.format_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        # Disable editing to prevent the selection box on double-click
        self.format_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.format_table.setStyleSheet(
            """
            QTableWidget {
                background-color: #1b2021;
                border: 2px solid #1b2021;
                border-radius: 4px;
                gridline-color: #1b2021;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #1b2021;
            }
            QTableWidget::item:selected {
                background-color: transparent;
            }
            QHeaderView::section {
                background-color: #15181b;
                padding: 5px;
                border: 1px solid #1b2021;
                font-weight: bold;
                color: white;
            }
            /* Style alternating rows with more contrast */
            QTableWidget::item:alternate {
                background-color: #212529;
            }
            QTableWidget::item {
                background-color: #16191b;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #15181b;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
            }
            QWidget {
                background-color: transparent;
            }
        """
        )

        # Store format checkboxes and formats
        self.format_checkboxes = []
        self.all_formats = []
        self._row_format_type = []  # Track format type per row: 'video' or 'audio'
        self._table_built = False  # Track if table has been built with current formats

        # Set table size policies
        self.format_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Set minimum and maximum heights
        self.format_table.setMinimumHeight(200)

        # Connect the signal
        self.format_signals.format_update.connect(self._update_format_table)

        return self.format_table

    def filter_formats(self) -> None:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        if not hasattr(self, "all_formats") or not self.all_formats:
            return

        # Check if we need to rebuild the table (first time or formats changed)
        if not self._table_built:
            self._build_full_format_table()
            return

        # Use row visibility for fast filtering instead of rebuilding table
        show_video = hasattr(self, "video_button") and self.video_button.isChecked()  # type: ignore[reportAttributeAccessIssue]
        show_audio = hasattr(self, "audio_button") and self.audio_button.isChecked()  # type: ignore[reportAttributeAccessIssue]

        for row, format_type in enumerate(self._row_format_type):
            if format_type == "video":
                self.format_table.setRowHidden(row, not show_video)
            else:  # audio
                self.format_table.setRowHidden(row, not show_audio)

    def _build_full_format_table(self) -> None:
        """Build the complete format table once with all formats."""
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        # Clear current table
        self.format_table.setRowCount(0)
        self.format_checkboxes.clear()
        self._row_format_type.clear()

        # Separate and filter formats
        video_formats = [f for f in self.all_formats if f.get("vcodec") != "none" and f.get("filesize") is not None]
        audio_formats = [
            f
            for f in self.all_formats
            if (f.get("vcodec") == "none" or "audio only" in f.get("format_note", "").lower())
            and f.get("acodec") != "none"
            and f.get("filesize") is not None
        ]

        # Sort formats by quality
        def get_quality(f):
            if f.get("vcodec") != "none":
                resolution = f.get("resolution", "0x0")
                if resolution is None or not isinstance(resolution, str):
                    return 0
                try:
                    res = resolution.split("x")[-1]
                    return int(res)
                except (ValueError, IndexError):
                    return 0
            else:
                return f.get("abr", 0)

        video_formats.sort(key=get_quality, reverse=True)
        audio_formats.sort(key=get_quality, reverse=True)

        # Combine: video first, then audio (maintains logical grouping)
        all_filtered = [(f, "video") for f in video_formats] + [(f, "audio") for f in audio_formats]

        # Build table with format type tracking
        self._populate_format_table(all_filtered)
        self._table_built = True

        # Apply initial visibility based on current button states
        self.filter_formats()

    def _populate_format_table(self, formats_with_types: list) -> None:
        """Populate the format table with formats and their types."""
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        is_playlist_mode = hasattr(self, "is_playlist") and self.is_playlist  # type: ignore[reportAttributeAccessIssue]

        # Configure columns based on mode
        if is_playlist_mode:
            self.format_table.setColumnCount(6)
            header_labels = [_("formats.select"), _("formats.quality"), _("formats.resolution"), _("formats.fps"), _("formats.hdr"), _("formats.audio")]
            self.format_table.setHorizontalHeaderLabels(header_labels)

            # Configure column visibility and resizing for playlist mode
            self.format_table.setColumnHidden(6, True)
            self.format_table.setColumnHidden(7, True)
            self.format_table.setColumnHidden(8, True)

            # Apply responsive column widths for playlist mode
            self._apply_column_widths(header_labels, is_playlist_mode=True)

        else:
            self.format_table.setColumnCount(9)
            header_labels = [
                _("formats.select"),
                _("formats.quality"),
                _("formats.extension"),
                _("formats.resolution"),
                _("formats.file_size"),
                _("formats.codec"),
                _("formats.audio"),
                _("formats.fps"),
                _("formats.hdr"),
            ]
            self.format_table.setHorizontalHeaderLabels(header_labels)
            self._apply_column_widths(header_labels, is_playlist_mode=False)

        for f, format_type in formats_with_types:
            row = self.format_table.rowCount()
            self.format_table.insertRow(row)
            self._row_format_type.append(format_type)

            # Create checkbox widget
            checkbox = QCheckBox()
            checkbox.setStyleSheet("QCheckBox { margin-left: 8px; }")
            checkbox.format_id = f["format_id"]
            checkbox.is_audio_only = f.get("vcodec") == "none"
            checkbox.has_audio = f.get("acodec") != "none"
            checkbox.clicked.connect(lambda checked, cb=checkbox: self.handle_checkbox_click(cb))
            self.format_checkboxes.append(checkbox)

            # Create a container widget for the checkbox
            checkbox_container = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_container)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.format_table.setCellWidget(row, 0, checkbox_container)

            # Quality label with color coding
            quality_label = self.get_quality_label(f)
            quality_item = QTableWidgetItem(quality_label)
            # Set color based on quality (check multiple language terms)
            quality_lower = quality_label.lower()
            if any(term.lower() in quality_lower for term in ["Best", "Óptima", "Mejor", "Melhor", "Лучшее", "最佳", "Beste", "Meilleure", "सर्वोत्तम", "Terbaik", "En iyi", "Najlepsza", "Najlepszy", "Najlepsze", "Migliore", "Miglior", "الأفضل", "أفضل", "最高"]):
                quality_item.setForeground(QColor("#00ff00"))  # Green for best quality
            elif any(term.lower() in quality_lower for term in ["High", "Alta", "Alto", "Áudio Alto", "Audio Alto", "Высокое", "高清", "高质量", "Hoch", "Haute", "Élevé", "Audio élevé", "उच्च", "उच्च ऑडियो", "Tinggi", "Audio tinggi", "Yüksek", "Yüksek ses", "Wysoka", "Wysoki", "Wysokie", "Audio alto", "عالية", "عالي", "صوت عالي", "高", "高音質"]):
                quality_item.setForeground(QColor("#00cc00"))  # Light green for high quality
            elif any(term.lower() in quality_lower for term in ["Medium", "Media", "Medio", "Média", "Áudio Médio", "Audio Medio", "Среднее", "中等", "Mittel", "Moyenne", "Audio moyen", "मध्यम", "मध्यम ऑडियो", "Sedang", "Audio sedang", "Orta", "Orta ses", "Średnia", "Średni", "Średnie", "Audio medio", "متوسطة", "متوسط", "صوت متوسط", "中", "中音質"]):
                quality_item.setForeground(QColor("#ffaa00"))  # Orange for medium quality
            elif any(term.lower() in quality_lower for term in ["Low", "Baja", "Bajo", "Baixa", "Áudio Baixo", "Audio Bajo", "Низкое", "低质量", "Niedrig", "Niedriges Audio", "Faible", "Audio faible", "Qualité faible", "निम्न", "निम्न ऑडियो", "निम्न गुणवत्ता", "Rendah", "Audio rendah", "Kualitas rendah", "Düşük", "Düşük ses", "Düşük kalite", "Niska", "Niski", "Niskie", "Bassa", "Audio basso", "Bassa qualità", "منخفضة", "منخفض", "صوت منخفض", "جودة منخفضة", "低", "低音質", "低品質"]):
                quality_item.setForeground(QColor("#ff5555"))  # Red for low quality
            self.format_table.setItem(row, 1, quality_item)

            # Resolution
            resolution = f.get("resolution", "N/A")

            if is_playlist_mode:
                # Column 2 for playlist mode: Resolution
                self.format_table.setItem(row, 2, QTableWidgetItem(resolution))

                # Column 3: FPS (Frame Rate)
                fps_value = f.get("fps")
                if fps_value is not None and fps_value >= 1:
                    fps_text = f"{fps_value:.0f}fps"
                else:
                    fps_text = "N/A"
                fps_item = QTableWidgetItem(fps_text)
                if fps_value and fps_value >= 60:
                    fps_item.setForeground(QColor("#00ff00"))
                elif fps_value and fps_value >= 30:
                    fps_item.setForeground(QColor("#ffaa00"))
                elif fps_value and fps_value >= 1:
                    fps_item.setForeground(QColor("#ff5555"))
                else:
                    fps_item.setForeground(QColor("#888888"))
                self.format_table.setItem(row, 3, fps_item)

                # Column 4: HDR
                if f.get("vcodec") == "none":
                    hdr_text = "N/A"
                    hdr_item = QTableWidgetItem(hdr_text)
                    hdr_item.setForeground(QColor("#888888"))
                else:
                    hdr_value = f.get("dynamic_range")
                    if hdr_value and hdr_value != "SDR":
                        hdr_text = hdr_value
                        hdr_item = QTableWidgetItem(hdr_text)
                        hdr_item.setForeground(QColor("#00ffff"))
                    else:
                        hdr_text = "SDR"
                        hdr_item = QTableWidgetItem(hdr_text)
                        hdr_item.setForeground(QColor("#888888"))
                self.format_table.setItem(row, 4, hdr_item)
            else:
                # Extension for normal mode (column 2)
                self.format_table.setItem(row, 2, QTableWidgetItem(f.get("ext", "").upper()))

            # Audio Status column
            needs_audio = f.get("acodec") == "none" and f.get("vcodec") != "none"
            audio_status = _("formats.will_merge_audio") if needs_audio else (_("formats.has_audio") if f.get("vcodec") != "none" else _("formats.audio_only"))
            audio_item = QTableWidgetItem(audio_status)
            if needs_audio:
                audio_item.setForeground(QColor("#ffa500"))
            elif audio_status == _("formats.audio_only"):
                audio_item.setForeground(QColor("#cccccc"))
            else:
                audio_item.setForeground(QColor("#00cc00"))
            audio_column_index = 5 if is_playlist_mode else 6
            self.format_table.setItem(row, audio_column_index, audio_item)

            # Populate columns only shown in non-playlist mode
            if not is_playlist_mode:
                # Column 3: Resolution
                self.format_table.setItem(row, 3, QTableWidgetItem(resolution))

                # Column 4: File Size
                filesize = f"{f.get('filesize', 0) / 1024 / 1024:.2f} MB"
                self.format_table.setItem(row, 4, QTableWidgetItem(filesize))

                # Column 5: Codec
                if f.get("vcodec") == "none":
                    codec = f.get("acodec", "N/A")
                else:
                    codec = f"{f.get('vcodec', 'N/A')}"
                    if f.get("acodec") != "none":
                        codec += f" / {f.get('acodec', 'N/A')}"
                self.format_table.setItem(row, 5, QTableWidgetItem(codec))

                # Column 7: FPS (Frame Rate)
                fps_value = f.get("fps")
                if fps_value is not None and fps_value >= 1:
                    fps_text = f"{fps_value:.0f}fps"
                else:
                    fps_text = "N/A"

                fps_item = QTableWidgetItem(fps_text)
                if fps_value and fps_value >= 60:
                    fps_item.setForeground(QColor("#00ff00"))
                elif fps_value and fps_value >= 30:
                    fps_item.setForeground(QColor("#ffaa00"))
                elif fps_value and fps_value >= 1:
                    fps_item.setForeground(QColor("#ff5555"))
                else:
                    fps_item.setForeground(QColor("#888888"))
                self.format_table.setItem(row, 7, fps_item)

                # Column 8: HDR (Dynamic Range)
                if f.get("vcodec") == "none":
                    hdr_text = "N/A"
                    hdr_item = QTableWidgetItem(hdr_text)
                    hdr_item.setForeground(QColor("#888888"))
                else:
                    hdr_value = f.get("dynamic_range")
                    if hdr_value and hdr_value != "SDR":
                        hdr_text = hdr_value
                        hdr_item = QTableWidgetItem(hdr_text)
                        hdr_item.setForeground(QColor("#00ffff"))
                    else:
                        hdr_text = "SDR"
                        hdr_item = QTableWidgetItem(hdr_text)
                        hdr_item.setForeground(QColor("#888888"))
                self.format_table.setItem(row, 8, hdr_item)

    def _update_format_table(self, formats) -> None:
        """Signal handler that triggers a full table rebuild when formats change."""
        self = cast("YTSageApp", self)  # for autocompletion and type inference.
        
        # Mark table as needing rebuild and trigger it
        self._table_built = False
        self._build_full_format_table()

    def handle_checkbox_click(self, clicked_checkbox) -> None:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        for checkbox in self.format_checkboxes:
            if checkbox != clicked_checkbox:
                checkbox.setChecked(False)

    def get_selected_format(self):
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        for checkbox in self.format_checkboxes:
            if checkbox.isChecked():
                return {
                    "format_id": checkbox.format_id,
                    "is_audio_only": getattr(checkbox, "is_audio_only", False),
                    "has_audio": getattr(checkbox, "has_audio", False),
                }
        return None

    def update_format_table(self, formats) -> None:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        self.all_formats = formats
        self._table_built = False  # Reset flag to trigger rebuild with new formats
        self.format_signals.format_update.emit(formats)

    def get_quality_label(self, format_info) -> str:
        """Determine quality label based on format information"""
        self = cast("YTSageApp", self)  # for autocompletion and type inference.
        
        if format_info.get("vcodec") == "none":
            # Audio quality
            abr = format_info.get("abr", 0)
            if abr >= 256:
                return _("formats.best_audio")
            elif abr >= 192:
                return _("formats.high_audio")
            elif abr >= 128:
                return _("formats.medium_audio")
            else:
                return _("formats.low_audio")
        else:
            # Video quality
            height = 0
            resolution = format_info.get("resolution", "")
            if resolution:
                try:
                    height = int(resolution.split("x")[1])
                except:
                    pass

            if height >= 2160:
                return _("formats.best_4k")
            elif height >= 1440:
                return _("formats.best_2k")
            elif height >= 1080:
                return _("formats.high_1080p")
            elif height >= 720:
                return _("formats.high_720p")
            elif height >= 480:
                return _("formats.medium_480p")
            else:
                return _("formats.low_quality")


