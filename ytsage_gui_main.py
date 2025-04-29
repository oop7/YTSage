import sys
import os
import webbrowser
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QProgressBar, QLabel, QFileDialog,
                            QHeaderView, QStyle, QStyleFactory, QComboBox, QTextEdit, QDialog, QPlainTextEdit, QCheckBox, QButtonGroup, QMessageBox, QListWidget,
                            QListWidgetItem, QDialogButtonBox, QScrollArea)
from PySide6.QtCore import Qt, Signal, QObject, QThread, QMetaObject, Q_ARG, QProcess, Slot
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
import markdown

from ytsage_downloader import DownloadThread, SignalManager  # Import downloader related classes
from ytsage_utils import check_ffmpeg, get_yt_dlp_path, load_saved_path, save_path # Import utility functions
from ytsage_gui_dialogs import (LogWindow, CustomCommandDialog, FFmpegCheckDialog, 
                                YTDLPUpdateDialog, AboutDialog, SubtitleSelectionDialog, 
                                PlaylistSelectionDialog, CookieLoginDialog,
                                DownloadSettingsDialog) # <-- Use renamed dialog
from ytsage_gui_format_table import FormatTableMixin # Import FormatTableMixin
from ytsage_gui_video_info import VideoInfoMixin # Import VideoInfoMixin

class YTSageApp(QMainWindow, FormatTableMixin, VideoInfoMixin): # Inherit from mixins
    def __init__(self):
        super().__init__()
        # Check for FFmpeg before proceeding
        if not check_ffmpeg():
            self.show_ffmpeg_dialog()

        self.version = "4.5.0"
        self.check_for_updates()
        self.config_file = Path.home() / '.ytsage_config.json'
        load_saved_path(self)
        # Load custom icon
        icon_path = os.path.join(os.path.dirname(__file__), 'Icon', 'icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Warning: Icon file not found at {icon_path}. Using default icon.")
            self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown)) # Fallback
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
        self.playlist_entries = []   # Initialize playlist entries
        self.selected_playlist_items = None # Initialize selection string
        self.save_description = False # Initialize description state
        self.subtitle_filter = ""
        self.thumbnail_image = None
        self.video_url = ""
        self.selected_subtitles = [] # Initialize selected subtitles list
        self.cookie_file_path = None # Initialize cookie file path
        self.speed_limit_value = None # Store speed limit value
        self.speed_limit_unit_index = 0 # Store speed limit unit index (0: KB/s, 1: MB/s)

        self.init_ui()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #15181b;
            }
            QWidget {
                background-color: #15181b;
                color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
                color: #ffffff;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QPushButton:pressed {
                background-color: #800000;
            }
            QTableWidget {
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
                gridline-color: #1b2021;
            }
            QHeaderView::section {
                background-color: #15181b;
                padding: 5px;
                border: 1px solid #1b2021;
                color: #ffffff;
            }
            QProgressBar {
                border: 2px solid #1b2021;
                border-radius: 4px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #c90000;
                border-radius: 2px;
            }
            QLabel {
                color: #ffffff;
            }
            /* Style for filter buttons */
            QPushButton.filter-btn {
                background-color: #1b2021;
                padding: 5px 10px;
                margin: 0 5px;
            }
            QPushButton.filter-btn:checked {
                background-color: #c90000;
            }
            QPushButton.filter-btn:hover {
                background-color: #444444;
            }
            QPushButton.filter-btn:checked:hover {
                background-color: #a50000;
            }
            /* Modern Scrollbar Styling */
            QScrollBar:vertical {
                border: none;
                background: #15181b;
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
                background: #15181b;
                height: 15px;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: #15181b;
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
                background: #15181b;
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
                background: #15181b;
                width: 15px;
                border-top-left-radius: 7px;
                border-bottom-left-radius: 7px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:horizontal {
                border: none;
                background: #15181b;
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

        # After adding format buttons
        self.video_button.clicked.connect(self.filter_formats)  # Connect video button
        self.audio_button.clicked.connect(self.filter_formats)  # Connect audio button
        
        # Add connections to handle video/audio mode-specific controls
        self.video_button.clicked.connect(self.handle_mode_change)
        self.audio_button.clicked.connect(self.handle_mode_change)
        
        # Initialize UI state based on current mode
        self.handle_mode_change()

    def load_saved_path(self): # Using function from ytsage_utils now - no longer needed in class
        pass # Handled in class init now via ytsage_utils.load_saved_path(self)

    def save_path(self, path): # Using function from ytsage_utils now - no longer needed in class
        save_path(self, path) # Call the utility function

    def init_ui(self):
        self.setWindowTitle('YTSage  v4.5.0')
        self.setMinimumSize(900, 750)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)

        # URL input section
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube video or playlist URL")
        self.url_input.returnPressed.connect(self.analyze_url) # Analyze on Enter key

        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.analyze_url)

        self.paste_button = QPushButton("Paste URL")
        self.paste_button.clicked.connect(self.paste_url)

        url_layout.addWidget(self.url_input, 1)
        url_layout.addWidget(self.paste_button)
        url_layout.addWidget(self.analyze_button)

        layout.addLayout(url_layout)

        # Video info container
        video_info_container = QWidget()
        video_info_layout = QVBoxLayout(video_info_container)
        video_info_layout.setSpacing(5)
        video_info_layout.setContentsMargins(0, 0, 0, 0)

        # Add media info layout (Thumbnail | Video Details)
        media_info_layout = self.setup_video_info_section()
        video_info_layout.addLayout(media_info_layout)

        # Add video info container to main layout
        layout.addWidget(video_info_container)

        # --- Add Playlist Info Section Directly to Main Layout --- 
        # Add playlist info label (initially hidden)
        self.playlist_info_label = self.setup_playlist_info_section()
        layout.addWidget(self.playlist_info_label)

        # Add playlist selection BUTTON (initially hidden) - REPLACED QLineEdit
        self.playlist_select_btn = QPushButton("Select Videos...")
        self.playlist_select_btn.clicked.connect(self.open_playlist_selection_dialog)
        self.playlist_select_btn.setVisible(False)
        self.playlist_select_btn.setStyleSheet("""
            QPushButton {
                padding: 6px 12px; 
                background-color: #1d1e22;
                border: 1px solid #c90000;
                border-radius: 4px;
                color: white;
                font-weight: normal;
                text-align: left;
                padding-left: 10px;
            }
            QPushButton:hover { 
                background-color: #2a2d36;
                border-color: #a50000;
            }
        """)
        layout.addWidget(self.playlist_select_btn)
        # --- End Playlist Info Section ---

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
                background-color: #1d1e22;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #c90000;
            }
            QPushButton:hover {
                background-color: #2a2d36;
            }
            QPushButton:checked:hover {
                background-color: #a50000;
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
                background-color: #1d1e22;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #c90000;
            }
            QPushButton:hover {
                background-color: #2a2d36;
            }
            QPushButton:checked:hover {
                background-color: #a50000;
            }
        """)
        self.format_buttons.addButton(self.audio_button)
        self.format_layout.addWidget(self.audio_button)

        # Add Merge Subtitles checkbox (Moved here)
        self.merge_subs_checkbox = QCheckBox("Merge Subtitles")
        self.merge_subs_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 20px; /* Consistent margin */
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #1d1e22;
                border-radius: 9px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
                border-radius: 9px;
            }
            /* Add disabled state styling if needed */
             QCheckBox:disabled { color: #888888; }
             QCheckBox::indicator:disabled { border-color: #555555; background: #444444; }
        """)
        # Initially disable it, will be enabled if subtitles are selected later
        self.merge_subs_checkbox.setEnabled(False)
        self.format_layout.addWidget(self.merge_subs_checkbox)

        # Add SponsorBlock checkbox
        self.sponsorblock_checkbox = QCheckBox("Remove Sponsor Segments")
        self.sponsorblock_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 20px; /* Consistent margin */
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #1d1e22;
                border-radius: 9px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
                border-radius: 9px;
            }
        """)
        self.format_layout.addWidget(self.sponsorblock_checkbox)

        # Add Save Thumbnail Checkbox (Moved here)
        self.save_thumbnail_checkbox = QCheckBox("Save Thumbnail")
        self.save_thumbnail_checkbox.setChecked(False)
        self.save_thumbnail_checkbox.stateChanged.connect(self.toggle_save_thumbnail)
        self.save_thumbnail_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 20px;
            }
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 9px; }
            QCheckBox::indicator:unchecked { border: 2px solid #666666; background: #1d1e22; border-radius: 9px; }
            QCheckBox::indicator:checked { border: 2px solid #c90000; background: #c90000; border-radius: 9px; }
             QCheckBox:disabled { color: #888888; }
             QCheckBox::indicator:disabled { border-color: #555555; background: #444444; }
        """)
        self.format_layout.addWidget(self.save_thumbnail_checkbox)

        # Add Save Description Checkbox (Moved here)
        self.save_description_checkbox = QCheckBox("Save Description")
        self.save_description_checkbox.setChecked(False)
        self.save_description_checkbox.stateChanged.connect(self.toggle_save_description)
        self.save_description_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 20px;
            }
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 9px; }
            QCheckBox::indicator:unchecked { border: 2px solid #666666; background: #1d1e22; border-radius: 9px; }
            QCheckBox::indicator:checked { border: 2px solid #c90000; background: #c90000; border-radius: 9px; }
             QCheckBox:disabled { color: #888888; }
             QCheckBox::indicator:disabled { border-color: #555555; background: #444444; }
        """)
        self.format_layout.addWidget(self.save_description_checkbox)

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

        # New button for cookie login
        self.cookie_login_button = QPushButton("Login with Cookies")
        self.cookie_login_button.clicked.connect(self.show_cookie_login_dialog) # Connect to a new method

        self.update_ytdlp_btn = QPushButton('Update yt-dlp')
        self.update_ytdlp_btn.clicked.connect(self.update_ytdlp)

        self.about_btn = QPushButton('About')
        self.about_btn.clicked.connect(self.show_about_dialog)

        # --- Rename Path Button to Settings Button ---
        self.settings_button = QPushButton("Download Settings") # Renamed button
        self.settings_button.clicked.connect(self.show_download_settings_dialog) # Renamed method
        self.settings_button.setToolTip(f"Current Path: {self.last_path}\nSpeed Limit: None") # Update initial tooltip
        # --- End Settings Button ---

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
        download_layout.addWidget(self.cookie_login_button)
        download_layout.addWidget(self.update_ytdlp_btn)
        download_layout.addWidget(self.about_btn)
        download_layout.addWidget(self.settings_button)
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
            self.signals.update_status.emit("Analyzing (15%)... Extracting basic info")

            # Clean up the URL to handle both playlist and video URLs
            if 'list=' in url and 'watch?v=' in url:
                playlist_id = url.split('list=')[1].split('&')[0]
                url = f'https://www.youtube.com/playlist?list={playlist_id}'

            # Initial extraction with basic options - suppress warnings here too
            ydl_opts = {
                'quiet': False,
                'no_warnings': True, # <-- Suppress warnings for initial check
                'extract_flat': True,
                'force_generic_extractor': False,
                'ignoreerrors': True,
                'no_color': True,
                'verbose': True
            }

            # Add cookies argument if cookie file path is set
            if self.cookie_file_path:
                ydl_opts['cookiefile'] = self.cookie_file_path

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    basic_info = ydl.extract_info(url, download=False)
                    if not basic_info:
                        raise Exception("Could not extract basic video information")
                except Exception as e:
                    print(f"First extraction failed: {str(e)}")
                    raise Exception("Could not extract video information, please check your link")

            self.signals.update_status.emit("Analyzing (30%)... Extracting detailed info")
            # Configure options for detailed extraction (keep other options)
            # Add no_warnings here as well, as this is where detailed info is fetched
            ydl_opts_detail = {
                'extract_flat': False,
                'format': None,
                'writesubtitles': True,
                'allsubtitles': True,
                'writeautomaticsub': True,
                'playliststart': 1,
                'playlistend': 1,
                'youtube_include_dash_manifest': True,
                'youtube_include_hls_manifest': True,
                'no_warnings': True # <-- Add flag here for detailed extraction
            }

            # Add cookies argument if cookie file path is set
            if self.cookie_file_path:
                ydl_opts_detail['cookiefile'] = self.cookie_file_path

            # Use a separate options dict for the detailed extraction
            with yt_dlp.YoutubeDL(ydl_opts_detail) as ydl_detail:
                try:
                    self.signals.update_status.emit("Analyzing (45%)... Processing video data")
                    if basic_info.get('_type') == 'playlist':
                        self.is_playlist = True
                        self.playlist_info = basic_info
                        self.selected_playlist_items = None # Reset selection for new playlist
                        self.playlist_entries = [entry for entry in basic_info.get('entries', []) if entry] # Store entries

                        # Ensure there are entries before proceeding
                        if not self.playlist_entries:
                            raise Exception("Playlist contains no valid videos.")

                        # Extract detailed info for the FIRST video in the playlist
                        # This provides formats/subs for the UI, assuming consistency
                        first_video_url = self.playlist_entries[0].get('url')
                        if not first_video_url:
                            raise Exception("Could not get URL for the first playlist video.")
                        try:
                            # Use the ydl_detail instance with no_warnings
                            self.video_info = ydl_detail.extract_info(first_video_url, download=False)
                        except Exception as first_video_error:
                             raise Exception(f"Failed to extract info for the first playlist video: {first_video_error}")

                        # Update playlist info label text (remains the same)
                        playlist_text = (f"Playlist: {basic_info.get('title', 'Unknown Playlist')} | "
                                        f"{len(self.playlist_entries)} videos") # Simplified label
                        QMetaObject.invokeMethod(
                            self.playlist_info_label, "setText", Qt.ConnectionType.QueuedConnection,
                            Q_ARG(str, playlist_text)
                        )
                        QMetaObject.invokeMethod(
                            self.playlist_info_label, "setVisible", Qt.ConnectionType.QueuedConnection,
                            Q_ARG(bool, True)
                        )

                        # Show playlist selection BUTTON
                        QMetaObject.invokeMethod(
                            self, # Target object is the YTSageApp instance
                            'update_playlist_button_text', # Name of the slot
                            Qt.ConnectionType.QueuedConnection,
                            Q_ARG(str, "Select Videos... (All selected)") # Argument for the slot
                        )
                        QMetaObject.invokeMethod(
                            self.playlist_select_btn, "setVisible", Qt.ConnectionType.QueuedConnection,
                            Q_ARG(bool, True)
                        )
                    else: # Single video
                        self.is_playlist = False
                        # Use ydl_detail instance here too for consistency
                        self.video_info = ydl_detail.extract_info(url, download=False)
                        self.playlist_entries = [] # Clear entries
                        self.selected_playlist_items = None # Clear selection
                        
                        # Hide playlist info label and button
                        QMetaObject.invokeMethod(
                            self.playlist_info_label, "setVisible", Qt.ConnectionType.QueuedConnection,
                            Q_ARG(bool, False)
                        )
                        QMetaObject.invokeMethod(
                            self.playlist_select_btn, "setVisible", Qt.ConnectionType.QueuedConnection,
                            Q_ARG(bool, False)
                        )

                    # Verify we have format information
                    if not self.video_info or 'formats' not in self.video_info:
                        print(f"Debug - video_info keys: {self.video_info.keys() if self.video_info else 'None'}")
                        raise Exception("No format information available")

                    self.signals.update_status.emit("Analyzing (60%)... Processing formats")
                    self.all_formats = self.video_info['formats']

                    # Update UI
                    self.update_video_info(self.video_info)

                    # Update thumbnail
                    self.signals.update_status.emit("Analyzing (75%)... Loading thumbnail")
                    thumbnail_url = None
                    if self.is_playlist:
                        # Try to get thumbnail from playlist info first
                        thumbnail_url = self.playlist_info.get('thumbnail') 

                    # Fallback to video thumbnail if playlist thumbnail not found or not a playlist
                    if not thumbnail_url:
                        thumbnail_url = self.video_info.get('thumbnail')
                        
                    self.download_thumbnail(thumbnail_url)

                    # Save thumbnail if enabled - use the stored VIDEO URL
                    if self.save_thumbnail:
                        self.download_thumbnail_file(self.video_url, self.path_input.text())

                    # --- Subtitle Handling ---
                    self.signals.update_status.emit("Analyzing (85%)... Processing subtitles")
                    # Clear previous selections when analyzing a new video
                    self.selected_subtitles = []
                    self.available_subtitles = self.video_info.get('subtitles', {})
                    self.available_automatic_subtitles = self.video_info.get('automatic_captions', {})
                    # Update the UI elements related to subtitle selection state
                    QMetaObject.invokeMethod(self.selected_subs_label, "setText", Qt.ConnectionType.QueuedConnection, Q_ARG(str, "0 selected"))
                    # QMetaObject.invokeMethod(self.subtitle_select_btn, "setProperty", Qt.ConnectionType.QueuedConnection, Q_ARG(str, "subtitlesSelected"), Q_ARG(bool, False)) # <-- COMMENT OUT THIS LINE
                    # REMOVE the merge_subs_checkbox update call from here
                    # QMetaObject.invokeMethod(self.merge_subs_checkbox, "setEnabled", Qt.ConnectionType.QueuedConnection, Q_ARG(bool, False))


                    # Update format table
                    self.signals.update_status.emit("Analyzing (95%)... Updating format table")
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
            # Ensure playlist UI is hidden on error too
            QMetaObject.invokeMethod(self.playlist_info_label, "setVisible", Qt.ConnectionType.QueuedConnection, Q_ARG(bool, False))
            QMetaObject.invokeMethod(self.playlist_select_btn, "setVisible", Qt.ConnectionType.QueuedConnection, Q_ARG(bool, False))

    def paste_url(self):
        clipboard = QApplication.clipboard()
        self.url_input.setText(clipboard.text())

    def update_ytdlp(self):
        dialog = YTDLPUpdateDialog(self)
        dialog.exec()

    def show_download_settings_dialog(self): # Renamed method
        dialog = DownloadSettingsDialog(
            self.last_path, 
            self.speed_limit_value, 
            self.speed_limit_unit_index, 
            self
        )
        if dialog.exec():
            # Update Path
            new_path = dialog.get_selected_path()
            path_changed = False
            if new_path != self.last_path:
                self.last_path = new_path
                self.save_path(self.last_path) # Save the updated path
                path_changed = True
                print(f"Download path updated to: {self.last_path}")

            # Update Speed Limit
            new_limit_value = dialog.get_selected_speed_limit()
            new_unit_index = dialog.get_selected_unit_index()
            limit_changed = False
            if new_limit_value != self.speed_limit_value or new_unit_index != self.speed_limit_unit_index:
                self.speed_limit_value = new_limit_value
                self.speed_limit_unit_index = new_unit_index
                limit_changed = True
                print(f"Speed limit updated to: {self.speed_limit_value} {['KB/s', 'MB/s'][self.speed_limit_unit_index] if self.speed_limit_value else 'None'}")

            # Update Tooltip if anything changed
            if path_changed or limit_changed:
                limit_text = "None"
                if self.speed_limit_value:
                     limit_text = f"{self.speed_limit_value} {['KB/s', 'MB/s'][self.speed_limit_unit_index]}"
                self.settings_button.setToolTip(f"Current Path: {self.last_path}\nSpeed Limit: {limit_text}")

    def start_download(self):
        url = self.url_input.text().strip()
        # --- Use self.last_path instead of reading from QLineEdit ---
        path = self.last_path 

        if not url or not path:
            # More specific error message if path is missing
            if not path:
                 self.status_label.setText("Please set a download path using 'Change Path'")
            elif not url:
                 self.status_label.setText("Please enter a URL")
            else:
                 self.status_label.setText("Please enter URL and set download path")
            return
        # --- End Path Change ---

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

        # Get subtitle selection if available - Now get the list
        selected_subs = self.selected_subtitles if hasattr(self, 'selected_subtitles') else []

        # Get playlist selection IF in playlist mode - USE STORED VALUE
        playlist_items_to_download = None
        if self.is_playlist:
            playlist_items_to_download = self.selected_playlist_items # Use the stored selection string

        # --- Use stored speed limit values ---
        rate_limit = None
        if self.speed_limit_value:
            try:
                limit_value = float(self.speed_limit_value)
                if self.speed_limit_unit_index == 0: # KB/s
                    rate_limit = f"{int(limit_value * 1024)}"
                elif self.speed_limit_unit_index == 1: # MB/s
                    rate_limit = f"{int(limit_value * 1024 * 1024)}"
            except ValueError:
                # Use a signal to show error in status bar, similar to URL/Path errors
                self.signals.update_status.emit("❌ Error: Invalid speed limit value set in settings.") 
                return
        # --- End speed limit update ---

        # Save thumbnail if enabled
        if self.save_thumbnail:
            # Consider moving thumbnail download *after* successful video download
            # Or handle errors more gracefully if thumbnail download fails
            try:
                self.download_thumbnail_file(url, path)
            except Exception as e:
                print(f"Warning: Thumbnail download failed: {e}")
                # Optionally inform the user, but don't stop the main download


        # Create download thread with resolution in output template
        self.download_thread = DownloadThread(
            url=url,
            path=path,
            format_id=format_id,
            subtitle_langs=selected_subs, # Pass the list of selected subs
            is_playlist=self.is_playlist, # Use the flag directly
            merge_subs=self.merge_subs_checkbox.isChecked(),
            enable_sponsorblock=self.sponsorblock_checkbox.isChecked(),
            resolution=resolution,
            playlist_items=playlist_items_to_download, # Pass the selection string
            save_description=self.save_description, # Pass the new flag here
            cookie_file=self.cookie_file_path, # Pass the cookie file path
            rate_limit=rate_limit # Pass the calculated rate limit
        )

        # Connect signals
        self.download_thread.progress_signal.connect(self.update_progress_bar)
        self.download_thread.status_signal.connect(self.status_label.setText)
        self.download_thread.update_details.connect(self.download_details_label.setText)
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
        
        # Set completion message based on the file type of last downloaded file
        if self.download_thread and self.download_thread.current_filename:
            filename = self.download_thread.current_filename
            ext = os.path.splitext(filename)[1].lower()
            
            # Video file extensions
            if ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.flv']:
                self.status_label.setText(f"✅ Video download completed!")
            # Audio file extensions
            elif ext in ['.mp3', '.m4a', '.aac', '.wav', '.ogg', '.opus', '.flac']:
                self.status_label.setText(f"✅ Audio download completed!")
            # Subtitle file extensions
            elif ext in ['.vtt', '.srt', '.ass', '.ssa']:
                self.status_label.setText(f"✅ Subtitle download completed!")
            # Default case
            else:
                self.status_label.setText("✅ Download completed!")

    def download_error(self, error_message):
        self.toggle_download_controls(True)
        self.pause_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.status_label.setText(f"Error: {error_message}")
        self.download_details_label.setText("") # Clear details label on error

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
                changelog = latest_release.get("body", "No changelog available.") # Get changelog body
                self.show_update_dialog(latest_version, latest_release["html_url"], changelog) # Pass changelog
        except Exception as e:
            print(f"Failed to check for updates: {str(e)}")

    def show_update_dialog(self, latest_version, release_url, changelog): # Added changelog parameter
        msg = QDialog(self)
        msg.setWindowTitle("Update Available")
        msg.setMinimumWidth(500) # Increased width for changelog
        msg.setMinimumHeight(400) # Added min height
        
        # Set custom icon directly
        icon_path = os.path.join(os.path.dirname(__file__), 'Icon', 'icon.png')
        if os.path.exists(icon_path):
            msg.setWindowIcon(QIcon(icon_path))
        else:
            # Fallback to main window icon if file not found
            msg.setWindowIcon(self.windowIcon())

        layout = QVBoxLayout(msg)
        layout.setSpacing(10) # Added spacing

        # Update message
        message_label = QLabel(
            f"<b>A new version of YTSage is available!</b>\n\n"
            f"Current version: {self.version}\n"
            f"Latest version: {latest_version}"
        )
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        # Changelog Section
        changelog_label = QLabel("<b>Changelog:</b>")
        layout.addWidget(changelog_label)

        changelog_text = QTextEdit()
        changelog_text.setReadOnly(True)
        # Convert Markdown to HTML and set it
        try:
            html_changelog = markdown.markdown(changelog, extensions=['markdown.extensions.tables', 'markdown.extensions.fenced_code'])
            changelog_text.setHtml(html_changelog)
        except Exception as e:
            print(f"Error converting changelog markdown to HTML: {e}")
            changelog_text.setPlainText(changelog) # Fallback to plain text

        changelog_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: #cccccc;
                padding: 5px;
                font-family: Consolas, monospace;
                font-size: 11px; /* Slightly smaller font */
            }
        """)
        changelog_text.setMaximumHeight(200) # Limit height
        layout.addWidget(changelog_text)

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
                padding: 5px 0; /* Adjusted padding */
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 120px; /* Adjusted min-width */
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
            self.status_label.setText("Cancelling download...") # Set status directly
            self.download_details_label.setText("") # Clear details label on cancellation

    def show_ffmpeg_dialog(self):
        dialog = FFmpegCheckDialog(self)
        dialog.exec()

    def toggle_download_controls(self, enabled=True):
        """Enable or disable download-related controls"""
        self.url_input.setEnabled(enabled)
        self.analyze_button.setEnabled(enabled)
        self.format_table.setEnabled(enabled)  # Changed from format_scroll_area to format_table
        self.download_btn.setEnabled(enabled)
        if hasattr(self, 'subtitle_combo'):
            self.subtitle_combo.setEnabled(enabled)
        self.video_button.setEnabled(enabled)
        self.audio_button.setEnabled(enabled)
        self.sponsorblock_checkbox.setEnabled(enabled)
        self.merge_subs_checkbox.setEnabled(enabled) # Enable/disable merge subs checkbox
        self.custom_cmd_btn.setEnabled(enabled) # Enable/disable custom command button
        self.cookie_login_button.setEnabled(enabled) # Enable/disable login button
        self.update_ytdlp_btn.setEnabled(enabled) # Enable/disable update button
        self.settings_button.setEnabled(enabled) # Enable/disable settings button

        # Clear progress/status when controls are re-enabled
        if enabled:
            self.progress_bar.setValue(0)
            self.status_label.setText("Ready")
            self.download_details_label.setText("") # Clear details label

    def handle_format_selection(self, button):
        # Update formats
        self.filter_formats()

    def handle_mode_change(self):
        """Enable or disable features based on video/audio mode"""
        if self.audio_button.isChecked():
            # In Audio Only mode, disable video-specific features
            self.sponsorblock_checkbox.setEnabled(False)
            self.sponsorblock_checkbox.setChecked(False)  # Uncheck when disabled
            self.merge_subs_checkbox.setEnabled(False)
            self.merge_subs_checkbox.setChecked(False)  # Uncheck when disabled
            
            # Allow subtitle selection in Audio Only mode too
            if hasattr(self, 'subtitle_select_btn'):
                self.subtitle_select_btn.setEnabled(True)
        else:
            # In Video mode, enable video-specific features
            self.sponsorblock_checkbox.setEnabled(True)
            # Don't auto-check - leave it to user preference
            
            # Enable merge_subs only if subtitles are selected
            has_subs_selected = len(getattr(self, 'selected_subtitles', [])) > 0
            self.merge_subs_checkbox.setEnabled(has_subs_selected)
            
            # Re-enable subtitle selection button in Video mode
            if hasattr(self, 'subtitle_select_btn'):
                self.subtitle_select_btn.setEnabled(True)

    def show_about_dialog(self): # ADDED METHOD HERE
        dialog = AboutDialog(self)
        dialog.exec()

    def file_already_exists(self, filename):
        """Handle case when file already exists - simplified version"""
        self.toggle_download_controls(True)
        self.pause_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.progress_bar.setValue(100)
        
        # Determine file type based on extension
        ext = os.path.splitext(filename)[1].lower()
        
        # Video file extensions
        if ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.flv']:
            self.status_label.setText(f"⚠️ Video file already exists")
        # Audio file extensions
        elif ext in ['.mp3', '.m4a', '.aac', '.wav', '.ogg', '.opus', '.flac']:
            self.status_label.setText(f"⚠️ Audio file already exists")
        # Subtitle file extensions
        elif ext in ['.vtt', '.srt', '.ass', '.ssa']:
            self.status_label.setText(f"⚠️ Subtitle file already exists")
        # Default case
        else:
            self.status_label.setText("⚠️ File already exists")
        
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

    # --- Add Toggle Methods Here ---
    def toggle_save_thumbnail(self, state):
        print(f"Raw thumbnail state received: {state}") # Debug: Print raw state
        self.save_thumbnail = bool(state == 2) # Compare state directly with 2 (Checked state)
        print(f"Save thumbnail toggled: {self.save_thumbnail}")

    def toggle_save_description(self, state):
        print(f"Raw description state received: {state}") # Debug: Print raw state
        self.save_description = bool(state == 2) # Compare state directly with 2 (Checked state)
        print(f"Save description toggled: {self.save_description}")
    # --- End Toggle Methods ---

    def open_playlist_selection_dialog(self):
        if not self.is_playlist or not self.playlist_entries:
            print("No playlist data available to select from.")
            return

        dialog = PlaylistSelectionDialog(self.playlist_entries, self.selected_playlist_items, self)
        
        if dialog.exec():
            self.selected_playlist_items = dialog.get_selected_items_string()
            print(f"Playlist items selected: {self.selected_playlist_items}")

            # Update button text (this call is safe as it happens in the main thread after dialog closes)
            if self.selected_playlist_items is None:
                 button_text = "Select Videos... (All selected)"
            else:
                selected_indices = dialog._parse_selection_string(self.selected_playlist_items)
                count = len(selected_indices)
                display_text = self.selected_playlist_items if len(self.selected_playlist_items) < 30 else f"{count} videos selected"
                button_text = f"Select Videos... ({display_text})"
            self.playlist_select_btn.setText(button_text) # Direct call is fine here
            
    # --- New Slot for Updating Playlist Button Text --- 
    @Slot(str)
    def update_playlist_button_text(self, text):
        """Safely updates the playlist selection button's text from any thread."""
        if hasattr(self, 'playlist_select_btn'):
             self.playlist_select_btn.setText(text)
    # --- End New Slot ---

    def show_cookie_login_dialog(self):
        dialog = CookieLoginDialog(self)
        if dialog.exec():
            self.cookie_file_path = dialog.get_cookie_file_path()
            if self.cookie_file_path:
                print(f"Selected cookie file: {self.cookie_file_path}") # For debugging
                QMessageBox.information(self, "Cookie File Selected", f"Cookie file selected: {self.cookie_file_path}")
            else:
                self.cookie_file_path = None # Clear path if dialog accepted but no file selected