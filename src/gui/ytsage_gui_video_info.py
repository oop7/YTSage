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
from ..core.ytsage_logging import logger
try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    logger.warning("yt-dlp not available at startup, will be downloaded at runtime")
from .ytsage_gui_dialogs import SubtitleSelectionDialog, SponsorBlockCategoryDialog

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
        self.like_count_label = QLabel()

        # Style the info labels
        for label in [self.channel_label, self.views_label, self.date_label, self.duration_label, self.like_count_label]:
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
        video_info_layout.addWidget(self.like_count_label)
        video_info_layout.addWidget(self.date_label)
        video_info_layout.addWidget(self.duration_label)

        # Add spacing before subtitle section
        video_info_layout.addSpacing(10)

        # --- Subtitle Section ---
        subtitle_layout = QHBoxLayout()
        subtitle_layout.setSpacing(10)

        # Subtitle selection button
        self.subtitle_select_btn = QPushButton("Select Subtitles...") # Renamed & changed text
        self.subtitle_select_btn.setFixedHeight(30)
        # self.subtitle_select_btn.setFixedWidth(150) # Let it size naturally or adjust as needed
        self.subtitle_select_btn.clicked.connect(self.open_subtitle_dialog)
        self.subtitle_select_btn.setStyleSheet("""
            QPushButton {
                background-color: #1d1e22;
                border: 2px solid #1d1e22;
                border-radius: 4px;
                padding: 5px 10px; /* Adjusted padding */
            }
            QPushButton:hover { background-color: #2a2d36; }
            /* Optional: Style differently if subtitles ARE selected */
            QPushButton[subtitlesSelected="true"] {
                 border-color: #c90000; /* Indicate selection */
            }
            /* Style for disabled state */
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #888888;
                border-color: #3d3d3d;
            }
        """)
        self.subtitle_select_btn.setProperty("subtitlesSelected", False) # Custom property for styling
        subtitle_layout.addWidget(self.subtitle_select_btn)

        # Label to show number of selected subtitles
        self.selected_subs_label = QLabel("0 selected")
        self.selected_subs_label.setStyleSheet("color: #cccccc; padding-left: 5px;")
        subtitle_layout.addWidget(self.selected_subs_label)

        # Add the subtitle layout to the main video info layout
        video_info_layout.addLayout(subtitle_layout)
        # --- End Subtitle Section ---

        # Add small spacing between subtitle and sponsorblock sections
        video_info_layout.addSpacing(4)

        # --- SponsorBlock Section ---
        sponsorblock_layout = QHBoxLayout()
        
        self.sponsorblock_select_btn = QPushButton("SponsorBlock Categories...")
        self.sponsorblock_select_btn.setFixedHeight(30)
        self.sponsorblock_select_btn.clicked.connect(self.open_sponsorblock_dialog)
        self.sponsorblock_select_btn.setStyleSheet("""
            QPushButton {
                background-color: #1d1e22;
                border: 2px solid #1d1e22;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover { 
                background-color: #2a2d36; 
            }
            QPushButton[sponsorBlockSelected="true"] {
                border-color: #c90000;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #888888;
                border-color: #3d3d3d;
            }
        """)
        self.sponsorblock_select_btn.setProperty("sponsorBlockSelected", False)
        self.sponsorblock_select_btn.setProperty("sponsorBlockSelected", False)
        sponsorblock_layout.addWidget(self.sponsorblock_select_btn)
        
        # Label to show selection count
        self.selected_sponsorblock_label = QLabel("0 selected")
        self.selected_sponsorblock_label.setStyleSheet("color: #cccccc; padding-left: 5px;")
        sponsorblock_layout.addWidget(self.selected_sponsorblock_label)
        
        sponsorblock_layout.addStretch()
        
        # Add the sponsorblock layout to the main video info layout
        video_info_layout.addLayout(sponsorblock_layout)
        # --- End SponsorBlock Section ---

        # Initialize SponsorBlock categories as empty initially (will be set to defaults when user opens dialog)
        self.selected_sponsorblock_categories = []
        self._update_sponsorblock_display()

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
                color: #ffffff;
                padding: 5px 8px;
                margin: 0;
                background-color: #1d1e22;
                border: 1px solid #c90000;
                border-radius: 4px;
                min-height: 30px;
                max-height: 30px;
            }
        """)
        self.playlist_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return self.playlist_info_label

    def update_video_info(self, info):
        if hasattr(self, 'is_playlist') and self.is_playlist:
            # Playlist Mode: Show playlist title and video count
            self.title_label.setText(self.playlist_info.get('title', 'Unknown Playlist'))
            
            num_videos = len(getattr(self, 'playlist_entries', []))
            self.duration_label.setText(f"Total Videos: {num_videos}")
            
            # Hide video-specific info
            self.channel_label.setText("")
            self.views_label.setText("")
            self.date_label.setText("")
            self.like_count_label.setText("")
            self.channel_label.setVisible(False)
            self.views_label.setVisible(False)
            self.date_label.setVisible(False)
            self.like_count_label.setVisible(False)
        else:
            # Single Video Mode: Show standard video info
            # Ensure labels are visible first
            self.channel_label.setVisible(True)
            self.views_label.setVisible(True)
            self.date_label.setVisible(True)
            self.like_count_label.setVisible(True)

            # Format view count with commas
            views = info.get('view_count')
            formatted_views = f"{views:,}" if views is not None else 'N/A'

            # Format like count with commas
            likes = info.get('like_count')
            formatted_likes = f"{likes:,}" if likes is not None else 'N/A'
    
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
            self.like_count_label.setText(f"Likes: {formatted_likes}")
            self.date_label.setText(f"Upload date: {formatted_date}")
            self.duration_label.setText(f"Duration: {duration_str}")

    def open_subtitle_dialog(self):
        if not hasattr(self, 'available_subtitles') or not hasattr(self, 'available_automatic_subtitles'):
             logger.warning("Subtitle info not loaded yet.")
             return

        if not hasattr(self, 'selected_subtitles'):
            self.selected_subtitles = []

        dialog = SubtitleSelectionDialog(
            self.available_subtitles,
            self.available_automatic_subtitles,
            self.selected_subtitles,
            self # Parent for the dialog
        )

        # Access the main application window (parent of the mixin's widget)
        # to find the merge checkbox
        main_window = self # In this context, self should be the YTSageApp instance
        if not isinstance(main_window, QMainWindow):
             # If the structure is different, this might need adjustment
             # Maybe self.parentWidget() or similar depending on how Mixin is used
             logger.warning("Cannot find main window to access merge checkbox.")
             merge_checkbox = None
        else:
             merge_checkbox = getattr(main_window, 'merge_subs_checkbox', None)


        if dialog.exec(): # If user clicks OK
            self.selected_subtitles = dialog.get_selected_subtitles()
            logger.info(f"Selected subtitles: {self.selected_subtitles}")
            # Update UI to reflect selection
            count = len(self.selected_subtitles)
            self.selected_subs_label.setText(f"{count} selected")
            self.subtitle_select_btn.setProperty("subtitlesSelected", count > 0)

            # Enable/disable the merge checkbox in the parent window
            if merge_checkbox:
                # Only enable merge checkbox if we're not in Audio Only mode
                is_audio_only = hasattr(main_window, 'audio_button') and main_window.audio_button.isChecked()
                # In audio-only mode, we still allow subtitle selection but not merging
                should_enable = count > 0 and not is_audio_only
                merge_checkbox.setEnabled(should_enable)
            else:
                logger.warning("merge_subs_checkbox not found on parent window.")

            # Re-apply stylesheet to update button border if property changed
            self.subtitle_select_btn.style().unpolish(self.subtitle_select_btn)
            self.subtitle_select_btn.style().polish(self.subtitle_select_btn)
        # No else needed for cancel, state remains unchanged

    def open_sponsorblock_dialog(self):
        """Open the SponsorBlock category selection dialog."""
        # Initialize selected categories if not exists or empty (first time opening)
        if not hasattr(self, 'selected_sponsorblock_categories') or not self.selected_sponsorblock_categories:
            # Use None to let the dialog set its own defaults
            dialog_categories = None
        else:
            dialog_categories = self.selected_sponsorblock_categories
        
        dialog = SponsorBlockCategoryDialog(dialog_categories, self)
        
        if dialog.exec():
            self.selected_sponsorblock_categories = dialog.get_selected_categories()
            logger.info(f"SponsorBlock categories selected: {self.selected_sponsorblock_categories}")
            self._update_sponsorblock_display()
    
    def _update_sponsorblock_display(self):
        """Update the SponsorBlock button and label to reflect current selection."""
        if not hasattr(self, 'selected_sponsorblock_categories'):
            self.selected_sponsorblock_categories = []
            
        count = len(self.selected_sponsorblock_categories)
        
        # Update label text
        if count == 0:
            self.selected_sponsorblock_label.setText("0 selected")
        elif count == 1:
            self.selected_sponsorblock_label.setText("1 category selected")
        else:
            self.selected_sponsorblock_label.setText(f"{count} categories selected")
        
        # Update button property for styling
        self.sponsorblock_select_btn.setProperty("sponsorBlockSelected", count > 0)
        
        # Force style refresh
        self.sponsorblock_select_btn.style().unpolish(self.sponsorblock_select_btn)
        self.sponsorblock_select_btn.style().polish(self.sponsorblock_select_btn)

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
            logger.error(f"Error loading thumbnail: {str(e)}")

    def download_thumbnail_file(self, video_url, path):
        if not self.save_thumbnail:
            return False

        try:
            from yt_dlp import YoutubeDL
            import requests  # Use requests instead of urlopen

            logger.debug(f"Attempting to save thumbnail for URL: {video_url}")

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

                logger.info(f"Thumbnail saved to: {thumbnail_path}")
                self.signals.update_status.emit(f"✅ Thumbnail saved: {filename}")
                return True

        except Exception as e:
            error_msg = f"❌ Thumbnail error: {str(e)}"
            logger.error(f"Thumbnail Save Error: {str(e)}")
            self.signals.update_status.emit(error_msg)
            return False

    def sanitize_filename(self, name):
        """Clean filename for filesystem safety"""
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()[:75]