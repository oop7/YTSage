import sys
import os
import webbrowser
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QProgressBar, QLabel, QFileDialog,
                            QHeaderView, QStyle, QStyleFactory, QComboBox, QTextEdit, QDialog, QPlainTextEdit, QCheckBox, QButtonGroup)
from PySide6.QtCore import Qt, Signal, QObject, QThread
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime
import json
from pathlib import Path
from packaging import version
import subprocess
import re
import yt_dlp

class VideoInfoMixin:
    def setup_video_info_section(self):
        # Create a horizontal layout for thumbnail and video info
        media_info_layout = QHBoxLayout()
        media_info_layout.setSpacing(15)

        # Left side container for thumbnail
        thumbnail_container = QWidget()
        thumbnail_container.setFixedWidth(320)
        thumbnail_layout = QVBoxLayout(thumbnail_container)
        thumbnail_layout.setContentsMargins(0, 0, 0, 0)
        
        # Thumbnail on the left
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(320, 180)
        self.thumbnail_label.setStyleSheet("border: 2px solid #3d3d3d; border-radius: 4px;")
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumbnail_layout.addWidget(self.thumbnail_label)
        thumbnail_layout.addStretch()
        
        media_info_layout.addWidget(thumbnail_container)

        # Video information on the right
        video_info_layout = QVBoxLayout()
        video_info_layout.setSpacing(2)  # Reduce spacing between elements
        video_info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Title and info labels
        self.title_label = QLabel()
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        # Add basic info labels
        self.channel_label = QLabel()
        self.views_label = QLabel()
        self.date_label = QLabel()
        self.duration_label = QLabel()

        # Style the info labels
        for label in [self.channel_label, self.views_label, self.date_label, self.duration_label]:
            label.setStyleSheet("""
                QLabel {
                    color: #cccccc;
                    font-size: 12px;
                    padding: 1px 0;
                }
            """)

        # Add labels to video info layout
        video_info_layout.addWidget(self.title_label)
        video_info_layout.addWidget(self.channel_label)
        video_info_layout.addWidget(self.views_label)
        video_info_layout.addWidget(self.date_label)
        video_info_layout.addWidget(self.duration_label)

        # Add spacing before subtitle section
        video_info_layout.addSpacing(10)

        # Create a horizontal layout for subtitle controls
        subtitle_layout = QHBoxLayout()
        subtitle_layout.setSpacing(5)  # Reduce spacing between elements

        # Create subtitle button
        self.subtitle_check = QPushButton("Download Subtitles")
        self.subtitle_check.setFixedHeight(30)
        self.subtitle_check.setFixedWidth(150)  # Set fixed width
        self.subtitle_check.setCheckable(True)
        self.subtitle_check.clicked.connect(self.toggle_subtitle_controls)
        self.subtitle_check.setStyleSheet("""
            QPushButton {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
                min-height: 30px;
            }
            QPushButton:checked {
                background-color: #ff0000;
                border-color: #cc0000;
            }
        """)
        subtitle_layout.addWidget(self.subtitle_check)

        # Create subtitle combo box
        self.subtitle_combo = QComboBox()
        self.subtitle_combo.setFixedHeight(30)
        self.subtitle_combo.setFixedWidth(200)
        self.subtitle_combo.setVisible(False)
        self.subtitle_combo.setStyleSheet("""
            QComboBox {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
                min-height: 30px;
            }
        """)
        subtitle_layout.addWidget(self.subtitle_combo)

        # Create merge subtitles checkbox
        self.merge_subs_checkbox = QCheckBox("Merge Subtitles")
        self.merge_subs_checkbox.setFixedHeight(30)
        self.merge_subs_checkbox.setVisible(False)
        self.merge_subs_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #2b2b2b;
                border-radius: 9px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #ff0000;
                background: #ff0000;
                border-radius: 9px;
            }
        """)
        subtitle_layout.addWidget(self.merge_subs_checkbox)

        # Add stretch to push everything to the left
        subtitle_layout.addStretch()

        # Create a second row for the filter input
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(5)

        # Create subtitle filter input
        self.subtitle_filter_input = QLineEdit()
        self.subtitle_filter_input.setFixedHeight(30)
        self.subtitle_filter_input.setFixedWidth(200)
        self.subtitle_filter_input.setPlaceholderText("Filter languages (e.g., en, es)")
        self.subtitle_filter_input.textChanged.connect(self.filter_subtitles)
        self.subtitle_filter_input.setVisible(False)
        self.subtitle_filter_input.setStyleSheet("""
            QLineEdit {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
                min-height: 30px;
                color: white;
            }
            QLineEdit:focus {
                border-color: #ff0000;
            }
        """)
        filter_layout.addWidget(self.subtitle_filter_input)
        filter_layout.addStretch()

        # Add both layouts to video info
        video_info_layout.addLayout(subtitle_layout)
        video_info_layout.addLayout(filter_layout)
        
        # Add stretch at the bottom
        video_info_layout.addStretch()

        # Add video info layout to main layout
        media_info_layout.addLayout(video_info_layout, stretch=1)

        return media_info_layout

    def setup_playlist_info_section(self):
        self.playlist_info_label = QLabel()
        self.playlist_info_label.setVisible(False)
        self.playlist_info_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #ff9900;
                padding: 5px 8px;
                margin: 0;
                background-color: #2b2b2b;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                min-height: 30px;
                max-height: 30px;
            }
        """)
        self.playlist_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return self.playlist_info_label

    def update_video_info(self, info):
        # Format view count with commas
        views = int(info.get('view_count', 0))
        formatted_views = f"{views:,}"

        # Format upload date
        upload_date = info.get('upload_date', '')
        if upload_date:
            date_obj = datetime.strptime(upload_date, '%Y%m%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
        else:
            formatted_date = 'Unknown date'

        # Format duration
        duration = info.get('duration', 0)
        minutes = duration // 60
        seconds = duration % 60
        duration_str = f"{minutes}:{seconds:02d}"

        # Update labels
        self.title_label.setText(info.get('title', 'Unknown title'))
        self.channel_label.setText(f"Channel: {info.get('uploader', 'Unknown channel')}")
        self.views_label.setText(f"Views: {formatted_views}")
        self.date_label.setText(f"Upload date: {formatted_date}")
        self.duration_label.setText(f"Duration: {duration_str}")

    def toggle_subtitle_controls(self):
        is_checked = self.subtitle_check.isChecked()
        self.subtitle_combo.setVisible(is_checked)
        self.subtitle_filter_input.setVisible(is_checked)
        self.merge_subs_checkbox.setVisible(is_checked)

    def update_subtitle_list(self):
        self.subtitle_combo.clear()

        if not (self.available_subtitles or self.available_automatic_subtitles):
            self.subtitle_combo.addItem("No subtitles available")
            return

        # Add subtitle options
        self.subtitle_combo.addItem("Select subtitle language")

        # Filter and add subtitles
        filter_text = self.subtitle_filter_input.text().lower()

        # Add manual subtitles
        for lang_code, subtitle_info in self.available_subtitles.items():
            if not filter_text or filter_text in lang_code.lower():
                self.subtitle_combo.addItem(f"{lang_code} - Manual")

        # Add auto-generated subtitles
        for lang_code, subtitle_info in self.available_automatic_subtitles.items():
            if not filter_text or filter_text in lang_code.lower():
                self.subtitle_combo.addItem(f"{lang_code} - Auto-generated")

    def filter_subtitles(self):
        self.subtitle_filter = self.subtitle_filter_input.text()
        self.update_subtitle_list()

    def download_thumbnail(self, url):
        try:
            # Store both thumbnail URL and video URL
            self.thumbnail_url = url
            self.video_url = self.url_input.text()  # Get actual video URL

            # Download thumbnail but don't save yet
            response = requests.get(url)
            self.thumbnail_image = Image.open(BytesIO(response.content))

            # Display thumbnail
            image = self.thumbnail_image.resize((320, 180), Image.Resampling.LANCZOS)
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            pixmap = QPixmap()
            pixmap.loadFromData(img_byte_arr.getvalue())
            self.thumbnail_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Error loading thumbnail: {str(e)}")

    def toggle_save_thumbnail(self):
        self.save_thumbnail = self.save_thumbnail_checkbox.isChecked()
        print(f"Save thumbnail toggled: {self.save_thumbnail}")  # Debug print

    def download_thumbnail_file(self, video_url, path):
        if not self.save_thumbnail:
            return False

        try:
            from yt_dlp import YoutubeDL
            import requests  # Use requests instead of urlopen

            print(f"Attempting to save thumbnail for URL: {video_url}")

            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'force_generic_extractor': False,
                'no_warnings': True,
                'extract_flat': False
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                thumbnails = info.get('thumbnails', [])

                if not thumbnails:
                    raise ValueError("No thumbnails available")

                thumbnail_url = max(
                    thumbnails,
                    key=lambda t: (t.get('height', 0) or 0) * (t.get('width', 0) or 0)
                ).get('url')

                if not thumbnail_url:
                    raise ValueError("Failed to extract thumbnail URL")

                # Download using requests
                response = requests.get(thumbnail_url)
                response.raise_for_status()

                # Save the thumbnail
                thumb_dir = os.path.join(path, 'Thumbnails')
                os.makedirs(thumb_dir, exist_ok=True)

                filename = f"{self.sanitize_filename(info['title'])}.jpg"
                thumbnail_path = os.path.join(thumb_dir, filename)

                with open(thumbnail_path, 'wb') as f:
                    f.write(response.content)

                print(f"Thumbnail saved to: {thumbnail_path}")
                self.signals.update_status.emit(f"✅ Thumbnail saved: {filename}")
                return True

        except Exception as e:
            error_msg = f"❌ Thumbnail error: {str(e)}"
            print(f"Thumbnail Save Error: {str(e)}")
            self.signals.update_status.emit(error_msg)
            return False

    def sanitize_filename(self, name):
        """Clean filename for filesystem safety"""
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()[:75]