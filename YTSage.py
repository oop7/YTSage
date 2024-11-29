import sys
import os
import threading
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget, 
                            QTableWidgetItem, QProgressBar, QLabel, QFileDialog,
                            QHeaderView, QStyle, QStyleFactory, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QIcon, QPalette, QColor, QPixmap
import yt_dlp
import requests
from io import BytesIO
from PIL import Image
from urllib.request import urlopen
from datetime import datetime

class SignalManager(QObject):
    update_formats = pyqtSignal(list)
    update_status = pyqtSignal(str)
    update_progress = pyqtSignal(float)

class YouTubeDownloaderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
        self.signals = SignalManager()
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
        """)
        self.signals.update_progress.connect(self.update_progress_bar)

    def init_ui(self):
        self.setWindowTitle('YT-GUI Downloader')
        self.setMinimumSize(900, 600)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # URL input section
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('Enter YouTube URL...')
        self.analyze_btn = QPushButton('Analyze')
        self.analyze_btn.clicked.connect(self.analyze_url)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.analyze_btn)
        layout.addLayout(url_layout)

        # Create a horizontal layout for thumbnail and video info
        media_info_layout = QHBoxLayout()
        
        # Thumbnail on the left
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(320, 180)
        self.thumbnail_label.setStyleSheet("border: 2px solid #3d3d3d; border-radius: 4px;")
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        media_info_layout.addWidget(self.thumbnail_label)
        
        # Video information on the right
        video_info_layout = QVBoxLayout()
        self.title_label = QLabel()
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        self.channel_label = QLabel()
        self.views_label = QLabel()
        self.date_label = QLabel()
        self.duration_label = QLabel()
        
        # Subtitle section
        subtitle_layout = QHBoxLayout()
        self.subtitle_check = QPushButton("Download Subtitles")
        self.subtitle_check.setCheckable(True)
        self.subtitle_check.clicked.connect(self.toggle_subtitle_list)
        subtitle_layout.addWidget(self.subtitle_check)
        
        self.subtitle_combo = QComboBox()
        self.subtitle_combo.setVisible(False)
        subtitle_layout.addWidget(self.subtitle_combo)
        subtitle_layout.addStretch()
        
        # Add all info widgets to the video info layout
        video_info_layout.addWidget(self.title_label)
        video_info_layout.addWidget(self.channel_label)
        video_info_layout.addWidget(self.views_label)
        video_info_layout.addWidget(self.date_label)
        video_info_layout.addWidget(self.duration_label)
        video_info_layout.addLayout(subtitle_layout)
        video_info_layout.addStretch()
        
        media_info_layout.addLayout(video_info_layout)
        layout.addLayout(media_info_layout)

        # Simplified format filter buttons
        filter_layout = QHBoxLayout()
        self.filter_label = QLabel("Show formats:")
        filter_layout.addWidget(self.filter_label)
        
        self.video_btn = QPushButton("Video")
        self.video_btn.setCheckable(True)
        self.video_btn.setChecked(True)
        self.video_btn.clicked.connect(self.filter_formats)
        self.video_btn.setProperty("class", "filter-btn")
        
        self.audio_btn = QPushButton("Audio Only")
        self.audio_btn.setCheckable(True)
        self.audio_btn.clicked.connect(self.filter_formats)
        self.audio_btn.setProperty("class", "filter-btn")
        
        filter_layout.addWidget(self.video_btn)
        filter_layout.addWidget(self.audio_btn)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Format table
        self.format_table = QTableWidget()
        self.format_table.setColumnCount(6)
        self.format_table.setHorizontalHeaderLabels(['Format ID', 'Extension', 'Resolution', 'File Size', 'Codec', 'Audio'])
        self.format_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.format_table)

        # Store formats for filtering
        self.all_formats = []

        # Download section
        download_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText('Download path...')
        self.browse_btn = QPushButton('Browse')
        self.browse_btn.clicked.connect(self.browse_path)
        self.download_btn = QPushButton('Download')
        self.download_btn.clicked.connect(self.start_download)
        download_layout.addWidget(self.path_input)
        download_layout.addWidget(self.browse_btn)
        download_layout.addWidget(self.download_btn)
        layout.addLayout(download_layout)

        # Progress section
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel('Ready')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Connect signals
        self.signals.update_formats.connect(self.update_format_table)
        self.signals.update_status.connect(self.status_label.setText)
        self.signals.update_progress.connect(self.update_progress_bar)

    def analyze_url(self):
        url = self.url_input.text()
        if url:
            self.signals.update_status.emit("Analyzing...")
            threading.Thread(target=self._analyze_url_thread, args=(url,), daemon=True).start()

    def _analyze_url_thread(self, url):
        try:
            ydl_opts = {
                'format': 'best',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'writesubtitles': True,
                'allsubtitles': True,
                'writeautomaticsub': True,
                'format_sort': ['res', 'ext', 'size', 'br', 'proto'],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Store all formats and video info
                self.all_formats = info['formats']
                self.video_info = info
                
                # Update UI with video information
                self.signals.update_status.emit("Updating video information...")
                self.update_video_info(info)
                
                # Download and display thumbnail
                thumbnail_url = info.get('thumbnail')
                if thumbnail_url:
                    self.download_thumbnail(thumbnail_url)

                # Update available subtitles (including auto-generated)
                self.available_subtitles = info.get('subtitles', {})
                self.available_automatic_subtitles = info.get('automatic_captions', {})
                self.update_subtitle_list()

                # Update table with filtered formats (default to video)
                self.video_btn.setChecked(True)
                self.audio_btn.setChecked(False)
                self.filter_formats()
                
                self.signals.update_status.emit("Analysis complete")
        except Exception as e:
            error_message = str(e)
            print(f"Error in analysis: {error_message}")
            self.signals.update_status.emit(f"Error: {error_message}")

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

    def toggle_subtitle_list(self):
        self.subtitle_combo.setVisible(self.subtitle_check.isChecked())
        
    def update_subtitle_list(self):
        self.subtitle_combo.clear()
        
        if not (self.available_subtitles or self.available_automatic_subtitles):
            self.subtitle_combo.addItem("No subtitles available")
            return

        self.subtitle_combo.addItem("Select subtitle language")
        
        # Add manual subtitles
        for lang_code, subtitle_info in self.available_subtitles.items():
            self.subtitle_combo.addItem(f"{lang_code} - Manual")
        
        # Add auto-generated subtitles
        for lang_code, subtitle_info in self.available_automatic_subtitles.items():
            self.subtitle_combo.addItem(f"{lang_code} - Auto-generated")

    def download_thumbnail(self, url):
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image = image.resize((320, 180), Image.Resampling.LANCZOS)
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            pixmap = QPixmap()
            pixmap.loadFromData(img_byte_arr)
            self.thumbnail_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Error loading thumbnail: {str(e)}")

    def filter_formats(self):
        # Clear current table
        self.format_table.setRowCount(0)
        
        # Determine which formats to show
        filtered_formats = []
        
        if self.video_btn.isChecked():
            # Include all video formats (both with and without audio)
            filtered_formats.extend([f for f in self.all_formats 
                                  if f.get('vcodec') != 'none' 
                                  and f.get('filesize') is not None])
        
        if self.audio_btn.isChecked():
            # Add audio-only formats
            filtered_formats.extend([f for f in self.all_formats 
                                  if (f.get('vcodec') == 'none' 
                                      or 'audio only' in f.get('format_note', '').lower())
                                  and f.get('acodec') != 'none'
                                  and f.get('filesize') is not None])
        
        # Sort formats by quality
        def get_quality(f):
            if f.get('vcodec') != 'none':
                # Extract height from resolution (e.g., "1920x1080" -> 1080)
                res = f.get('resolution', '0x0').split('x')[-1]
                try:
                    return int(res)
                except ValueError:
                    return 0
            else:
                return f.get('abr', 0)
        
        filtered_formats.sort(key=get_quality, reverse=True)
        
        # Update table with filtered formats
        self.update_format_table(filtered_formats)

    def update_format_table(self, formats):
        self.format_table.setRowCount(0)
        for f in formats:
            row = self.format_table.rowCount()
            self.format_table.insertRow(row)
            
            # Format ID
            self.format_table.setItem(row, 0, QTableWidgetItem(str(f.get('format_id', ''))))
            
            # Extension
            self.format_table.setItem(row, 1, QTableWidgetItem(f.get('ext', '')))
            
            # Resolution
            resolution = f.get('resolution', 'N/A')
            if f.get('vcodec') == 'none':
                resolution = 'Audio only'
            self.format_table.setItem(row, 2, QTableWidgetItem(resolution))
            
            # File Size
            filesize = f"{f.get('filesize', 0) / 1024 / 1024:.2f} MB"
            self.format_table.setItem(row, 3, QTableWidgetItem(filesize))
            
            # Codec
            if f.get('vcodec') == 'none':
                codec = f.get('acodec', 'N/A')
            else:
                codec = f"{f.get('vcodec', 'N/A')}"
                if f.get('acodec') != 'none':
                    codec += f" / {f.get('acodec', 'N/A')}"
            self.format_table.setItem(row, 4, QTableWidgetItem(codec))
            
            # Audio Status
            needs_audio = f.get('acodec') == 'none'
            audio_status = "Will merge audio" if needs_audio else "✓ Has Audio"
            audio_item = QTableWidgetItem(audio_status)
            if needs_audio:
                audio_item.setForeground(QColor('#ffa500'))  # Orange for merge indication
            self.format_table.setItem(row, 5, audio_item)

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if path:
            self.path_input.setText(path)

    def start_download(self):
        url = self.url_input.text()
        path = self.path_input.text()
        selected_items = self.format_table.selectedItems()
        if not selected_items:
            self.signals.update_status.emit("Please select a format")
            return
        
        format_id = self.format_table.item(selected_items[0].row(), 0).text()
        
        # If it's a video format, also download the best audio
        selected_format = next((f for f in self.all_formats if str(f.get('format_id')) == format_id), None)
        if selected_format and selected_format.get('acodec') == 'none':
            format_id = f"{format_id}+bestaudio"
        
        # Check if subtitles should be downloaded
        download_subs = self.subtitle_check.isChecked()
        selected_sub = self.subtitle_combo.currentText().split(' - ')[0] if download_subs else None
        
        threading.Thread(target=self._download_thread, 
                        args=(url, path, format_id, selected_sub), 
                        daemon=True).start()

    def _download_thread(self, url, path, format_id, subtitle_lang=None):
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'merge_output_format': 'mp4',
        }
        
        # Add subtitle options if requested
        if subtitle_lang:
            # Extract language code from the combo box text
            lang_code = subtitle_lang.split(' - ')[0]
            is_auto = 'Auto-generated' in subtitle_lang
            
            ydl_opts.update({
                'writesubtitles': True,
                'subtitleslangs': [lang_code],
                'writeautomaticsub': True,
                'skip_manual_subs': is_auto,  # Skip manual subs if auto is selected
                'skip_auto_subs': not is_auto,  # Skip auto subs if manual is selected
            })
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            error_message = str(e)
            self.signals.update_status.emit(f"Error: {error_message}")

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                downloaded_bytes = int(d.get('downloaded_bytes', 0))
                total_bytes = int(d.get('total_bytes', 1))  # Use 1 as default to avoid division by zero
                # Ensure we're working with integers throughout
                progress = int((downloaded_bytes * 100) // total_bytes)
                # Clamp the value between 0 and 100
                progress = max(0, min(100, progress))
                self.signals.update_progress.emit(progress)
                self.signals.update_status.emit(f"Downloading: {progress}%")
            except Exception as e:
                print(f"Progress calculation error: {str(e)}")
                self.signals.update_status.emit("Downloading...")
        elif d['status'] == 'finished':
            self.signals.update_progress.emit(100)
            self.signals.update_status.emit("Download completed!")

    def update_progress_bar(self, value):
        try:
            # Ensure the value is an integer
            int_value = int(value)
            self.progress_bar.setValue(int_value)
        except Exception as e:
            print(f"Progress bar update error: {str(e)}")

def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = YouTubeDownloaderGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()