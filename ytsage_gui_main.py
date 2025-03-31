import sys
import os
import webbrowser
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QProgressBar, QLabel, QFileDialog,
                            QHeaderView, QStyle, QStyleFactory, QComboBox, QTextEdit, QDialog, QPlainTextEdit, QCheckBox, QButtonGroup, QMessageBox)
from PySide6.QtCore import Qt, Signal, QObject, QThread, QMetaObject, Q_ARG, QProcess
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

from ytsage_downloader import DownloadThread, SignalManager  # Import downloader related classes
from ytsage_utils import check_ffmpeg, get_yt_dlp_path, load_saved_path, save_path # Import utility functions
from ytsage_gui_dialogs import LogWindow, CustomCommandDialog, FFmpegCheckDialog, YTDLPUpdateDialog, AboutDialog # Import dialogs
from ytsage_gui_format_table import FormatTableMixin # Import FormatTableMixin
from ytsage_gui_video_info import VideoInfoMixin # Import VideoInfoMixin

class YTSageApp(QMainWindow, FormatTableMixin, VideoInfoMixin): # Inherit from mixins
    def __init__(self):
        super().__init__()
        # Check for FFmpeg before proceeding
        if not check_ffmpeg():
            self.show_ffmpeg_dialog()

        self.version = "4.2.1"
        self.check_for_updates()
        self.config_file = Path.home() / '.ytsage_config.json'
        load_saved_path(self)
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
        self.signals = SignalManager()
        self.download_paused = False
        self.current_download = None
        self.download_cancelled = False
        self.save_thumbnail = False  # Initialize thumbnail state
        self.thumbnail_url = None    # Add this to store thumbnail URL
        self.all_formats = []        # Initialize all_formats
        self.available_subtitles = {}
        self.available_automatic_subtitles = {}
        self.is_playlist = False
        self.playlist_info = None
        self.video_info = None
        self.subtitle_filter = ""
        self.thumbnail_image = None
        self.video_url = ""

        self.init_ui()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                background-color: #363636;
                color: #ffffff;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;  /* YouTube red */
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;  /* Darker red on hover */
            }
            QPushButton:pressed {
                background-color: #990000;  /* Even darker red when pressed */
            }
            QTableWidget {
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                background-color: #363636;
                gridline-color: #3d3d3d;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                padding: 5px;
                border: 1px solid #3d3d3d;
                color: #ffffff;
            }
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #ff0000;  /* YouTube red */
                border-radius: 2px;
            }
            QLabel {
                color: #ffffff;
            }
            /* Style for filter buttons */
            QPushButton.filter-btn {
                background-color: #363636;
                padding: 5px 10px;
                margin: 0 5px;
            }
            QPushButton.filter-btn:checked {
                background-color: #ff0000;
            }
            QPushButton.filter-btn:hover {
                background-color: #444444;
            }
            QPushButton.filter-btn:checked:hover {
                background-color: #cc0000;
            }
            /* Modern Scrollbar Styling */
            QScrollBar:vertical {
                border: none;
                background: #2b2b2b;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #404040;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: #505050;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background: #2b2b2b;
                height: 15px;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: #2b2b2b;
                height: 15px;
                border-bottom-left-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical:hover,
            QScrollBar::add-line:vertical:hover {
                background: #404040;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
                width: 0;
                height: 0;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            /* Horizontal Scrollbar */
            QScrollBar:horizontal {
                border: none;
                background: #2b2b2b;
                height: 14px;
                margin: 0 15px 0 15px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal {
                background: #404040;
                min-width: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #505050;
            }
            QScrollBar::sub-line:horizontal {
                border: none;
                background: #2b2b2b;
                width: 15px;
                border-top-left-radius: 7px;
                border-bottom-left-radius: 7px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:horizontal {
                border: none;
                background: #2b2b2b;
                width: 15px;
                border-top-right-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal:hover,
            QScrollBar::add-line:horizontal:hover {
                background: #404040;
            }
            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
                background: none;
                width: 0;
                height: 0;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        self.signals.update_progress.connect(self.update_progress_bar)

    def load_saved_path(self): # Using function from ytsage_utils now - no longer needed in class
        pass # Handled in class init now via ytsage_utils.load_saved_path(self)

    def save_path(self, path): # Using function from ytsage_utils now - no longer needed in class
        save_path(self, path) # Call the utility function

    def init_ui(self):
        self.setWindowTitle('YTSage  v4.2.1')
        self.setMinimumSize(900, 650)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)

        # URL input section
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('Enter YouTube URL...')

        # Add Paste URL button
        self.paste_btn = QPushButton('Paste URL')
        self.paste_btn.clicked.connect(self.paste_url)

        self.analyze_btn = QPushButton('Analyze')
        self.analyze_btn.clicked.connect(self.analyze_url)

        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.paste_btn)
        url_layout.addWidget(self.analyze_btn)
        layout.addLayout(url_layout)

        # Video info container with smaller fixed height
        video_info_container = QWidget()
        video_info_container.setFixedHeight(220)
        video_info_layout = QVBoxLayout(video_info_container)
        video_info_layout.setSpacing(5)
        video_info_layout.setContentsMargins(0, 0, 0, 0)

        # Add media info layout
        media_info_layout = self.setup_video_info_section()
        video_info_layout.addLayout(media_info_layout)

        # Add playlist info with minimal height
        self.playlist_info_label = self.setup_playlist_info_section()
        self.playlist_info_label.setMaximumHeight(30)
        video_info_layout.addWidget(self.playlist_info_label)

        # Add video info container to main layout
        layout.addWidget(video_info_container)

        # Format controls section with minimal spacing
        layout.addSpacing(5)

        # Format selection layout (horizontal)
        self.format_layout = QHBoxLayout()

        # Show formats label
        self.show_formats_label = QLabel("Show formats:")
        self.show_formats_label.setStyleSheet("color: white;")
        self.format_layout.addWidget(self.show_formats_label)

        # Format buttons group
        self.format_buttons = QButtonGroup(self)
        self.format_buttons.setExclusive(True)

        # Video button
        self.video_button = QPushButton("Video")
        self.video_button.setCheckable(True)
        self.video_button.setChecked(True)  # Set video as default
        self.video_button.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #363636;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #ff0000;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:checked:hover {
                background-color: #cc0000;
            }
        """)
        self.format_buttons.addButton(self.video_button)
        self.format_layout.addWidget(self.video_button)

        # Audio button
        self.audio_button = QPushButton("Audio Only")
        self.audio_button.setCheckable(True)
        self.audio_button.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #363636;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #ff0000;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:checked:hover {
                background-color: #cc0000;
            }
        """)
        self.format_buttons.addButton(self.audio_button)
        self.format_layout.addWidget(self.audio_button)

        # Connect format buttons
        self.format_buttons.buttonClicked.connect(self.handle_format_selection)

        # Add SponsorBlock checkbox
        self.sponsorblock_checkbox = QCheckBox("Remove Sponsor Segments")
        self.sponsorblock_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 20px;
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
        self.format_layout.addWidget(self.sponsorblock_checkbox)

        # Add Save Thumbnail checkbox with same style as SponsorBlock
        self.save_thumbnail_checkbox = QCheckBox("Save Thumbnail")
        self.save_thumbnail_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 20px;
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
        self.save_thumbnail_checkbox.clicked.connect(self.toggle_save_thumbnail)
        self.format_layout.addWidget(self.save_thumbnail_checkbox)

        self.format_layout.addStretch()
        layout.addLayout(self.format_layout)

        # Format table with stretch
        format_table = self.setup_format_table()
        layout.addWidget(format_table, stretch=1)

        # Download section
        download_layout = QHBoxLayout()

        # Add existing buttons
        self.custom_cmd_btn = QPushButton('Custom Command')
        self.custom_cmd_btn.clicked.connect(self.show_custom_command)

        self.update_ytdlp_btn = QPushButton('Update yt-dlp')
        self.update_ytdlp_btn.clicked.connect(self.update_ytdlp)

        self.about_btn = QPushButton('About')
        self.about_btn.clicked.connect(self.show_about_dialog)

        self.path_input = QLineEdit(self.last_path)
        self.path_input.setPlaceholderText('Download path...')

        self.browse_btn = QPushButton('Browse')
        self.browse_btn.clicked.connect(self.browse_path)

        self.download_btn = QPushButton('Download')
        self.download_btn.clicked.connect(self.start_download)

        # Add pause and cancel buttons
        self.pause_btn = QPushButton('Pause')
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setVisible(False)  # Hidden initially

        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setVisible(False)  # Hidden initially

        # Add all buttons to layout in the correct order
        download_layout.addWidget(self.custom_cmd_btn)
        download_layout.addWidget(self.update_ytdlp_btn)
        download_layout.addWidget(self.about_btn)
        download_layout.addWidget(self.path_input)
        download_layout.addWidget(self.browse_btn)
        download_layout.addWidget(self.download_btn)
        download_layout.addWidget(self.pause_btn)
        download_layout.addWidget(self.cancel_btn)

        layout.addLayout(download_layout)

        # Progress section with improved styling
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                color: white;
                background-color: #363636;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #ff0000;
                border-radius: 2px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)

        # Add download details label with improved styling
        self.download_details_label = QLabel()
        self.download_details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.download_details_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 12px;
                padding: 5px;
            }
        """)
        progress_layout.addWidget(self.download_details_label)

        self.status_label = QLabel('Ready')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 12px;
                padding: 5px;
            }
        """)
        progress_layout.addWidget(self.status_label)

        layout.addLayout(progress_layout)

        # Connect signals
        self.signals.update_formats.connect(self.update_format_table)
        self.signals.update_status.connect(self.status_label.setText)
        self.signals.update_progress.connect(self.update_progress_bar)

        # After adding format buttons
        self.video_button.clicked.connect(self.filter_formats)  # Connect video button
        self.audio_button.clicked.connect(self.filter_formats)  # Connect audio button

    def analyze_url(self):
        url = self.url_input.text().strip()
        if not url:
            self.signals.update_status.emit("Invalid URL or please enter a URL.")
            return

        self.signals.update_status.emit("Analyzing (0%)... Preparing request")
        import threading # Import threading here as it is only used in GUI and downloader
        threading.Thread(target=self._analyze_url_thread, args=(url,), daemon=True).start()

    def _analyze_url_thread(self, url):
        try:
            self.signals.update_status.emit("Analyzing (20%)... Extracting basic info")

            # Clean up the URL to handle both playlist and video URLs
            if 'list=' in url and 'watch?v=' in url:
                playlist_id = url.split('list=')[1].split('&')[0]
                url = f'https://www.youtube.com/playlist?list={playlist_id}'

            # Initial extraction with basic options
            ydl_opts = {
                'quiet': False,
                'no_warnings': False,
                'extract_flat': True,
                'force_generic_extractor': False,
                'ignoreerrors': True,
                'no_color': True,
                'verbose': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    basic_info = ydl.extract_info(url, download=False)
                    if not basic_info:
                        raise Exception("Could not extract basic video information")
                except Exception as e:
                    print(f"First extraction failed: {str(e)}")
                    raise Exception("Could not extract video information, please check your link")

            self.signals.update_status.emit("Analyzing (40%)... Extracting detailed info")
            # Configure options for detailed extraction
            ydl_opts.update({
                'extract_flat': False,
                'format': None,
                'writesubtitles': True,
                'allsubtitles': True,
                'writeautomaticsub': True,
                'playliststart': 1,
                'playlistend': 1,
                'youtube_include_dash_manifest': True,
                'youtube_include_hls_manifest': True
            })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    self.signals.update_status.emit("Analyzing (60%)... Processing video data")
                    if basic_info.get('_type') == 'playlist':
                        self.is_playlist = True
                        self.playlist_info = basic_info
                        
                        # Store all playlist entries
                        self.playlist_entries = [entry for entry in basic_info['entries'] if entry]
                        
                        # Update playlist info text
                        playlist_text = (f"Playlist: {basic_info.get('title', 'Unknown')} | "
                                        f"{len(self.playlist_entries)} videos | "
                                        f"Enter video numbers (e.g. 1-5,7,9-11)")
                        QMetaObject.invokeMethod(
                            self.playlist_info_label,
                            "setText",
                            Qt.ConnectionType.QueuedConnection,
                            Q_ARG(str, playlist_text)
                        )
                        QMetaObject.invokeMethod(
                            self.playlist_info_label,
                            "setVisible",
                            Qt.ConnectionType.QueuedConnection,
                            Q_ARG(bool, True)
                        )

                        # Show playlist selection input
                        QMetaObject.invokeMethod(
                            self.playlist_selection_input,
                            "setVisible",
                            Qt.ConnectionType.QueuedConnection,
                            Q_ARG(bool, True)
                        )
                    else:
                        self.is_playlist = False
                        self.video_info = ydl.extract_info(url, download=False)
                        self.playlist_info_label.setVisible(False)

                    # Verify we have format information
                    if not self.video_info or 'formats' not in self.video_info:
                        print(f"Debug - video_info keys: {self.video_info.keys() if self.video_info else 'None'}")
                        raise Exception("No format information available")

                    self.signals.update_status.emit("Analyzing (80%)... Processing formats")
                    self.all_formats = self.video_info['formats']

                    # Update UI
                    self.update_video_info(self.video_info)

                    # Update thumbnail
                    self.signals.update_status.emit("Analyzing (90%)... Loading thumbnail")
                    self.download_thumbnail(self.video_info.get('thumbnail'))

                    # Save thumbnail if enabled - use the stored VIDEO URL
                    if self.save_thumbnail:
                        self.download_thumbnail_file(self.video_url, self.path_input.text())

                    # Update subtitles
                    self.signals.update_status.emit("Analyzing (95%)... Processing subtitles")
                    self.available_subtitles = self.video_info.get('subtitles', {})
                    self.available_automatic_subtitles = self.video_info.get('automatic_captions', {})
                    self.update_subtitle_list()

                    # Update format table
                    self.signals.update_status.emit("Analyzing (98%)... Updating format table")
                    self.video_button.setChecked(True)
                    self.audio_button.setChecked(False)
                    self.filter_formats()

                    self.signals.update_status.emit("Analysis complete!")

                except Exception as e:
                    print(f"Detailed extraction failed: {str(e)}")
                    raise Exception(f"Failed to extract video details: {str(e)}")

        except Exception as e:
            error_message = str(e)
            print(f"Error in analysis: {error_message}")
            self.signals.update_status.emit(f"Error: {error_message}")

    def paste_url(self):
        clipboard = QApplication.clipboard()
        self.url_input.setText(clipboard.text())

    def update_ytdlp(self):
        dialog = YTDLPUpdateDialog(self)
        dialog.exec()

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Download Directory", self.last_path)
        if path:
            self.path_input.setText(path)
            self.save_path(path) # Use save_path utility function
            self.last_path = path

    def start_download(self):
        url = self.url_input.text().strip()
        path = self.path_input.text().strip()

        if not url or not path:
            self.status_label.setText("Please enter URL and download path")
            return

        # Get selected format
        format_id = self.get_selected_format()
        if not format_id:
            self.status_label.setText("Please select a format")
            return

        # Show preparation message
        self.status_label.setText("🚀 Preparing your download...")
        self.progress_bar.setValue(0)

        # Get resolution for filename
        resolution = 'default'
        for checkbox in self.format_checkboxes:
            if checkbox.isChecked():
                parts = checkbox.text().split('•')
                if len(parts) >= 1:
                    resolution = parts[0].strip().lower()
                break

        # Get subtitle selection if available
        subtitle_lang = None
        if hasattr(self, 'subtitle_combo') and self.subtitle_combo.currentIndex() > 0:
            subtitle_lang = self.subtitle_combo.currentText()

        # Check if it's a playlist
        is_playlist = 'playlist' in url.lower() and '/watch?' not in url

        # Get playlist selection if available
        playlist_items = None
        if self.is_playlist and self.playlist_selection_input.isVisible():
            playlist_items = self.playlist_selection_input.text().strip() or None

        # Save thumbnail if enabled
        if self.save_thumbnail:
            self.download_thumbnail_file(url, path)

        # Create download thread with resolution in output template
        self.download_thread = DownloadThread(
            url=url,
            path=path,
            format_id=format_id,
            subtitle_lang=subtitle_lang,
            is_playlist=is_playlist,
            merge_subs=self.merge_subs_checkbox.isChecked(),
            enable_sponsorblock=self.sponsorblock_checkbox.isChecked(),
            resolution=resolution,
            playlist_items=playlist_items
        )

        # Connect signals
        self.download_thread.progress_signal.connect(self.update_progress_bar)
        self.download_thread.status_signal.connect(self.signals.update_status.emit)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.error_signal.connect(self.download_error)
        self.download_thread.file_exists_signal.connect(self.file_already_exists)

        # Reset download state
        self.download_paused = False
        self.download_cancelled = False

        # Show pause/cancel buttons
        self.pause_btn.setText('Pause')
        self.pause_btn.setVisible(True)
        self.cancel_btn.setVisible(True)

        # Start download thread
        self.current_download = self.download_thread
        self.download_thread.start()
        self.toggle_download_controls(False)

    def download_finished(self):
        self.toggle_download_controls(True)
        self.pause_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.progress_bar.setValue(100)
        self.status_label.setText("Download completed!")

    def download_error(self, error_message):
        self.toggle_download_controls(True)
        self.pause_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.status_label.setText(f"Error: {error_message}")

    def update_progress_bar(self, value):
        try:
            # Ensure the value is an integer
            int_value = int(value)
            self.progress_bar.setValue(int_value)
        except Exception as e:
            print(f"Progress bar update error: {str(e)}")

    def toggle_pause(self):
        if self.current_download:
            self.current_download.paused = not self.current_download.paused
            if self.current_download.paused:
                self.pause_btn.setText('Resume')
                self.signals.update_status.emit("Download paused")
            else:
                self.pause_btn.setText('Pause')
                self.signals.update_status.emit("Download resumed")

    def check_for_updates(self):
        try:
            # Get the latest release info from GitHub
            response = requests.get(
                "https://api.github.com/repos/oop7/YTSage/releases/latest",
                headers={"Accept": "application/vnd.github.v3+json"}
            )
            response.raise_for_status()

            latest_release = response.json()
            latest_version = latest_release["tag_name"].lstrip('v')

            # Compare versions
            if version.parse(latest_version) > version.parse(self.version):
                self.show_update_dialog(latest_version, latest_release["html_url"])
        except Exception as e:
            print(f"Failed to check for updates: {str(e)}")

    def show_update_dialog(self, latest_version, release_url):
        msg = QDialog(self)
        msg.setWindowTitle("Update Available")
        msg.setMinimumWidth(400)

        layout = QVBoxLayout(msg)

        # Update message
        message_label = QLabel(
            f"A new version of YTSage is available!\n\n"
            f"Current version: {self.version}\n"
            f"Latest version: {latest_version}"
        )
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        # Buttons
        button_layout = QHBoxLayout()

        download_btn = QPushButton("Download Update")
        download_btn.clicked.connect(lambda: self.open_release_page(release_url))

        remind_btn = QPushButton("Remind Me Later")
        remind_btn.clicked.connect(msg.close)

        button_layout.addWidget(download_btn)
        button_layout.addWidget(remind_btn)
        layout.addLayout(button_layout)

        # Style the dialog
        msg.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
                padding: 10px;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)

        msg.show()

    def open_release_page(self, url):
        webbrowser.open(url)

    def show_custom_command(self):
        dialog = CustomCommandDialog(self)
        dialog.exec()

    def cancel_download(self):
        if self.current_download:
            self.current_download.cancelled = True
            self.signals.update_status.emit("Cancelling download...")

    def show_ffmpeg_dialog(self):
        dialog = FFmpegCheckDialog(self)
        dialog.exec()

    def toggle_download_controls(self, enabled=True):
        """Enable or disable download-related controls"""
        self.url_input.setEnabled(enabled)
        self.analyze_btn.setEnabled(enabled)
        self.format_table.setEnabled(enabled)  # Changed from format_scroll_area to format_table
        self.path_input.setEnabled(enabled)
        self.browse_btn.setEnabled(enabled)
        self.download_btn.setEnabled(enabled)
        if hasattr(self, 'subtitle_combo'):
            self.subtitle_combo.setEnabled(enabled)
        self.video_button.setEnabled(enabled)
        self.audio_button.setEnabled(enabled)
        self.sponsorblock_checkbox.setEnabled(enabled)

    def handle_format_selection(self, button):
        # Update formats
        self.filter_formats()

    def show_about_dialog(self): # ADDED METHOD HERE
        dialog = AboutDialog(self)
        dialog.exec()

    def file_already_exists(self, filename):
        """Handle case when file already exists - simplified version"""
        self.toggle_download_controls(True)
        self.pause_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.progress_bar.setValue(100)
        self.status_label.setText(f"⚠️ File already exists: {filename}")
        
        # Show a simple message dialog
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("File Already Exists")
        msg_box.setText(f"The file already exists:\n{filename}")
        msg_box.setInformativeText("This video has already been downloaded.")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Set the window icon to match the main application
        msg_box.setWindowIcon(self.windowIcon())
        
        # Style the dialog
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)
        
        msg_box.exec()