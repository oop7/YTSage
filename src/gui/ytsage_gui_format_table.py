from typing import TYPE_CHECKING, cast

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QHeaderView, QSizePolicy, QTableWidget, QTableWidgetItem, QWidget

from src.utils.ytsage_localization import _

if TYPE_CHECKING:
    from src.gui.ytsage_gui_main import YTSageApp


class FormatSignals(QObject):
    format_update = Signal(list)


class FormatTableMixin:
    def setup_format_table(self) -> QTableWidget:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        self.format_signals = FormatSignals()
        # Format table with improved styling
        self.format_table = QTableWidget()
        self.format_table.setColumnCount(8)
        self.format_table.setHorizontalHeaderLabels(
            [
                _("formats.select"),
                _("formats.quality"),
                _("formats.extension"),
                _("formats.resolution"),
                _("formats.file_size"),
                _("formats.codec"),
                _("formats.audio"),
                _("formats.fps"),
            ]
        )

        # Enable alternating row colors
        self.format_table.setAlternatingRowColors(True)

        # Set specific column widths and resize modes
        self.format_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # Select
        self.format_table.setColumnWidth(0, 70)  # Select column width (slightly reduced)

        self.format_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # Quality
        self.format_table.setColumnWidth(1, 110)  # Quality width (increased for better visibility)

        self.format_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # Extension
        self.format_table.setColumnWidth(2, 85)  # Extension width (slightly increased)

        self.format_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Resolution
        self.format_table.setColumnWidth(3, 110)  # Resolution width (increased for better visibility)

        self.format_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # File Size
        self.format_table.setColumnWidth(4, 110)  # File Size width (increased for better readability)

        self.format_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Codec
        self.format_table.setColumnWidth(5, 160)  # Codec width (increased for codec names)

        self.format_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Audio
        self.format_table.setColumnWidth(6, 140)  # Audio width (increased for better text visibility)

        self.format_table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)  # FPS column stretches to fill
        # FPS column will stretch to fill remaining space

        # Set vertical header (row numbers) visible to false
        self.format_table.verticalHeader().setVisible(False)

        # Set selection mode to no selection (since we're using checkboxes)
        self.format_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

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

        # Set table size policies
        self.format_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Set minimum and maximum heights
        self.format_table.setMinimumHeight(200)

        # Connect the signal
        self.format_signals.format_update.connect(self._update_format_table)

        return self.format_table

    def filter_formats(self) -> None:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        if not hasattr(self, "all_formats"):
            return

        # Clear current table
        self.format_table.setRowCount(0)
        self.format_checkboxes.clear()

        # Determine which formats to show
        filtered_formats = []

        if hasattr(self, "video_button") and self.video_button.isChecked():  # type: ignore[reportAttributeAccessIssue]
            filtered_formats.extend([f for f in self.all_formats if f.get("vcodec") != "none" and f.get("filesize") is not None])

        if hasattr(self, "audio_button") and self.audio_button.isChecked():  # type: ignore[reportAttributeAccessIssue]
            filtered_formats.extend(
                [
                    f
                    for f in self.all_formats
                    if (f.get("vcodec") == "none" or "audio only" in f.get("format_note", "").lower())
                    and f.get("acodec") != "none"
                    and f.get("filesize") is not None
                ]
            )

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

        filtered_formats.sort(key=get_quality, reverse=True)

        # Update table with filtered formats
        self.format_signals.format_update.emit(filtered_formats)

    def _update_format_table(self, formats) -> None:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        self.format_table.setRowCount(0)
        self.format_checkboxes.clear()

        is_playlist_mode = hasattr(self, "is_playlist") and self.is_playlist  # type: ignore[reportAttributeAccessIssue]

        # Configure columns based on mode
        if is_playlist_mode:
            self.format_table.setColumnCount(5)
            self.format_table.setHorizontalHeaderLabels([_("formats.select"), _("formats.quality"), _("formats.resolution"), _("formats.fps"), _("formats.audio")])

            # Configure column visibility and resizing for playlist mode
            self.format_table.setColumnHidden(5, True)
            self.format_table.setColumnHidden(6, True)
            self.format_table.setColumnHidden(7, True)

            # Set specific resize modes for playlist columns
            self.format_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.format_table.setColumnWidth(0, 80)  # Match the width set in setup_format_table
            self.format_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.format_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.format_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            self.format_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        else:
            self.format_table.setColumnCount(8)
            self.format_table.setHorizontalHeaderLabels(
                [
                    _("formats.select"),
                    _("formats.quality"),
                    _("formats.extension"),
                    _("formats.resolution"),
                    _("formats.file_size"),
                    _("formats.codec"),
                    _("formats.audio"),
                    _("formats.fps"),
                ]
            )
            # Ensure all columns are visible
            for i in range(2, 8):
                self.format_table.setColumnHidden(i, False)

            # Reapply optimized resize modes for non-playlist mode
            self.format_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.format_table.setColumnWidth(0, 70)  # Match the optimized width
            self.format_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
            self.format_table.setColumnWidth(1, 110)
            self.format_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
            self.format_table.setColumnWidth(2, 85)
            self.format_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            self.format_table.setColumnWidth(3, 110)
            self.format_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
            self.format_table.setColumnWidth(4, 110)
            self.format_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
            self.format_table.setColumnWidth(5, 160)
            self.format_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
            self.format_table.setColumnWidth(6, 140)
            self.format_table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)
            # FPS column stretches to fill remaining space



        for f in formats:
            row = self.format_table.rowCount()
            self.format_table.insertRow(row)

            # Column 0: Select Checkbox (Always shown)
            checkbox = QCheckBox()
            checkbox.format_id = str(f.get("format_id", ""))  # type: ignore[reportAttributeAccessIssue]
            checkbox.clicked.connect(lambda checked, cb=checkbox: self.handle_checkbox_click(cb))
            self.format_checkboxes.append(checkbox)
            checkbox_widget = QWidget()
            checkbox_widget.setStyleSheet("background-color: transparent;")
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_layout.setSpacing(0)
            self.format_table.setCellWidget(row, 0, checkbox_widget)

            # Column 1: Quality (Always shown)
            quality_text = self.get_quality_label(f)
            quality_item = QTableWidgetItem(quality_text)
            # Set color based on quality (check English, Spanish, Portuguese, Russian, Chinese, German, French, Hindi, Indonesian, Turkish, Polish, Italian, Arabic, and Japanese terms)
            quality_lower = quality_text.lower()  # Make comparison case-insensitive
            if any(term.lower() in quality_lower for term in ["Best", "Óptima", "Mejor", "Melhor", "Лучшее", "最佳", "Beste", "Meilleure", "सर्वोत्तम", "Terbaik", "En iyi", "Najlepsza", "Najlepszy", "Najlepsze", "Migliore", "Miglior", "الأفضل", "أفضل", "最高"]):
                quality_item.setForeground(QColor("#00ff00"))  # Green for best quality
            elif any(term.lower() in quality_lower for term in ["High", "Alta", "Alto", "Áudio Alto", "Audio Alto", "Высокое", "高清", "高质量", "Hoch", "Haute", "Élevé", "Audio élevé", "उच्च", "उच्च ऑडियो", "Tinggi", "Audio tinggi", "Yüksek", "Yüksek ses", "Wysoka", "Wysoki", "Wysokie", "Alta", "Audio alto", "عالية", "عالي", "صوت عالي", "高", "高音質"]):
                quality_item.setForeground(QColor("#00cc00"))  # Light green for high quality
            elif any(term.lower() in quality_lower for term in ["Medium", "Media", "Medio", "Média", "Áudio Médio", "Audio Medio", "Среднее", "中等", "Mittel", "Moyenne", "Audio moyen", "मध्यम", "मध्यम ऑडियो", "Sedang", "Audio sedang", "Orta", "Orta ses", "Średnia", "Średni", "Średnie", "Media", "Audio medio", "متوسطة", "متوسط", "صوت متوسط", "中", "中音質"]):
                quality_item.setForeground(QColor("#ffaa00"))  # Orange for medium quality
            elif any(term.lower() in quality_lower for term in ["Low", "Baja", "Bajo", "Baixa", "Áudio Baixo", "Audio Bajo", "Низкое", "低质量", "Niedrig", "Niedriges Audio", "Faible", "Audio faible", "Qualité faible", "निम्न", "निम्न ऑडियो", "निम्न गुणवत्ता", "Rendah", "Audio rendah", "Kualitas rendah", "Düşük", "Düşük ses", "Düşük kalite", "Niska", "Niski", "Niskie", "Bassa", "Audio basso", "Bassa qualità", "منخفضة", "منخفض", "صوت منخفض", "جودة منخفضة", "低", "低音質", "低品質"]):
                quality_item.setForeground(QColor("#ff5555"))  # Red for low quality
            self.format_table.setItem(row, 1, quality_item)

            # --- Populate columns common to both modes (Moved outside the 'if not is_playlist_mode' block) ---

            # Column 2: Resolution (Always shown)
            resolution = f.get("resolution", "N/A")
            if f.get("vcodec") == "none":
                resolution = _("formats.audio_only_resolution")
            self.format_table.setItem(row, 2, QTableWidgetItem(resolution))

            # Column 3: FPS for playlist mode, Extension for normal mode
            if is_playlist_mode:
                # Get FPS for playlist mode
                fps_value = f.get("fps")
                if fps_value is not None:
                    # Format FPS value appropriately
                    if fps_value >= 1:
                        fps_text = f"{fps_value:.0f}fps"
                    else:
                        fps_text = "N/A"  # Very low fps like storyboards
                else:
                    fps_text = "N/A"
                
                fps_item = QTableWidgetItem(fps_text)
                # Color code based on FPS value
                if fps_value and fps_value >= 60:
                    fps_item.setForeground(QColor("#00ff00"))  # Green for 60+ fps
                elif fps_value and fps_value >= 30:
                    fps_item.setForeground(QColor("#ffaa00"))  # Orange for 30+ fps
                elif fps_value and fps_value >= 1:
                    fps_item.setForeground(QColor("#ff5555"))  # Red for low fps
                else:
                    fps_item.setForeground(QColor("#888888"))  # Gray for N/A
                self.format_table.setItem(row, 3, fps_item)
            else:
                # Extension for normal mode (column 2)
                self.format_table.setItem(row, 2, QTableWidgetItem(f.get("ext", "").upper()))

            # Column 4 in playlist mode, Column 6 in normal mode: Audio Status
            needs_audio = f.get("acodec") == "none" and f.get("vcodec") != "none"  # Only mark video-only as needing merge
            audio_status = _("formats.will_merge_audio") if needs_audio else (_("formats.has_audio") if f.get("vcodec") != "none" else _("formats.audio_only"))
            audio_item = QTableWidgetItem(audio_status)
            if needs_audio:
                audio_item.setForeground(QColor("#ffa500"))
            elif audio_status == _("formats.audio_only"):
                audio_item.setForeground(QColor("#cccccc"))  # Neutral color for audio only
            else:  # Has Audio (Video+Audio)
                audio_item.setForeground(QColor("#00cc00"))  # Green for included audio
            # Set item for correct column based on mode
            audio_column_index = 4 if is_playlist_mode else 6
            self.format_table.setItem(row, audio_column_index, audio_item)

            # --- Populate columns only shown in non-playlist mode ---
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
                if fps_value is not None:
                    # Format FPS value appropriately
                    if fps_value >= 1:
                        fps_text = f"{fps_value:.0f}fps"
                    else:
                        fps_text = "N/A"  # Very low fps like storyboards
                else:
                    fps_text = "N/A"
                
                fps_item = QTableWidgetItem(fps_text)
                # Color code based on FPS value
                if fps_value and fps_value >= 60:
                    fps_item.setForeground(QColor("#00ff00"))  # Green for 60+ fps
                elif fps_value and fps_value >= 30:
                    fps_item.setForeground(QColor("#ffaa00"))  # Orange for 30+ fps
                elif fps_value and fps_value >= 1:
                    fps_item.setForeground(QColor("#ff5555"))  # Red for low fps
                else:
                    fps_item.setForeground(QColor("#888888"))  # Gray for N/A
                self.format_table.setItem(row, 7, fps_item)

    def handle_checkbox_click(self, clicked_checkbox) -> None:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        for checkbox in self.format_checkboxes:
            if checkbox != clicked_checkbox:
                checkbox.setChecked(False)

    def get_selected_format(self):
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        for checkbox in self.format_checkboxes:
            if checkbox.isChecked():
                return checkbox.format_id
        return None

    def update_format_table(self, formats) -> None:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        self.all_formats = formats
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


