import json
import subprocess
import threading
import webbrowser
from pathlib import Path

import markdown
import requests
from packaging import version
from PySide6.QtCore import Q_ARG, QMetaObject, Qt, QTimer, Slot, QThread, Signal, QUrl, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QStyle,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QGraphicsOpacityEffect,
    QGraphicsBlurEffect,
    QGraphicsScene,
    QGraphicsPixmapItem,
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor

from .. import __version__ as APP_VERSION
from ..core.ytsage_downloader import DownloadThread, SignalManager  # Import downloader related classes
from ..core.ytsage_utils import check_ffmpeg, load_saved_path, parse_yt_dlp_error, save_path, should_check_for_auto_update, validate_video_url
from ..core.ytsage_yt_dlp import get_yt_dlp_path, setup_ytdlp  # Import the new yt-dlp functions
from ..core.ytsage_deno import get_deno_path, setup_deno  # Import the new Deno functions
from .ytsage_gui_dialogs import (  # use of src\gui\ytsage_gui_dialogs\__init__.py
    AboutDialog,
    AutoUpdateThread,
    CustomOptionsDialog,
    DownloadSettingsDialog,
    FFmpegCheckDialog,
    HistoryDialog,
    PlaylistSelectionDialog,
    TimeRangeDialog,
    YTDLPUpdateDialog,
)
from .ytsage_gui_format_table import FormatTableMixin
from .ytsage_gui_video_info import VideoInfoMixin
from .ytsage_gui_analysis import AnalysisMixin
from ..utils.ytsage_constants import (
    ICON_PATH,
    SOUND_PATH,
    SUBPROCESS_CREATIONFLAGS,
    VIDEO_EXTENSIONS,
    AUDIO_EXTENSIONS,
    SUBTITLE_EXTENSIONS,
)
from ..utils.ytsage_logger import logger
from ..utils.ytsage_config_manager import ConfigManager
from ..utils.ytsage_localization import LocalizationManager, _
from ..utils.ytsage_history_manager import HistoryManager
from .ytsage_stylesheet import StyleSheet

from concurrent.futures import ThreadPoolExecutor, as_completed


class UpdateCheckThread(QThread):
    """Background thread for checking application updates with parallel network requests."""
    
    update_available = Signal(str, str, str)  # version, url, changelog

    # Reduced timeouts for faster failure detection
    PYPI_TIMEOUT = 8
    GITHUB_TIMEOUT = 5

    def __init__(self, current_version):
        super().__init__()
        self.current_version = current_version

    def _fetch_pypi_version(self) -> tuple[str | None, str | None]:
        """Fetch latest version from PyPI. Returns (version, error)."""
        try:
            response = requests.get(
                "https://pypi.org/pypi/ytsage/json",
                timeout=self.PYPI_TIMEOUT,
            )
            response.raise_for_status()
            pypi_data = response.json()
            return pypi_data["info"]["version"], None
        except requests.Timeout:
            return None, "PyPI request timed out"
        except requests.RequestException as e:
            return None, f"PyPI request failed: {e}"
        except Exception as e:
            return None, f"Error parsing PyPI response: {e}"

    def _fetch_github_changelog(self) -> str:
        """Fetch changelog from GitHub. Returns changelog text or fallback message."""
        fallback = "View the full changelog on the [GitHub Releases](https://github.com/oop7/YTSage/releases) page."
        try:
            response = requests.get(
                "https://api.github.com/repos/oop7/YTSage/releases/latest",
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=self.GITHUB_TIMEOUT,
            )
            if response.status_code == 200:
                gh_data = response.json()
                return gh_data.get("body", fallback) or fallback
            return fallback
        except Exception:
            # Silently fallback if GitHub API fails (rate limiting, network issues, etc.)
            return fallback

    def _fetch_github_beta_version(self) -> tuple[str | None, str | None, str | None]:
        """Fetch latest version code from GitHub releases (including betas). Returns (version, tag, changelog)."""
        try:
            response = requests.get(
                "https://api.github.com/repos/oop7/YTSage/releases",
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=self.GITHUB_TIMEOUT,
            )
            if response.status_code != 200:
                logger.debug(f"GitHub Releases API returned {response.status_code}")
                return None, None, None

            releases = response.json()
            if not releases:
                return None, None, None

            latest_release = None
            highest_ver = version.parse("0.0.0")

            for rel in releases:
                tag = rel.get("tag_name", "")
                ver_str = tag.lstrip("v")
                try:
                    v = version.parse(ver_str)
                    if v > highest_ver:
                        highest_ver = v
                        latest_release = rel
                except Exception:
                    continue
            
            if latest_release:
                return str(highest_ver), latest_release.get("tag_name"), latest_release.get("body")
            return None, None, None

        except Exception as e:
            logger.debug(f"GitHub beta check error: {e}")
            return None, None, None

    def run(self):
        """Check for updates using parallel network requests for better performance."""
        try:
            # Check for beta updates if enabled
            check_beta = ConfigManager.get("check_beta_updates")
            
            if check_beta:
                latest_ver_str, tag, changelog = self._fetch_github_beta_version()
                
                if latest_ver_str and version.parse(latest_ver_str) > version.parse(self.current_version):
                    release_url = f"https://github.com/oop7/YTSage/releases/tag/{tag}"
                    if not changelog:
                        changelog = "View the full changelog on GitHub."
                    self.update_available.emit(latest_ver_str, release_url, changelog)
                # Return if beta check completes (whether update found or not), 
                # effectively skipping PyPI check if beta is enabled. 
                # This ensures we don't downgrade or conflict.
                return

            # Use ThreadPoolExecutor to make both requests in parallel
            # This reduces total wait time from potentially 15s to ~8s max
            with ThreadPoolExecutor(max_workers=2) as executor:
                # Submit both tasks
                pypi_future = executor.submit(self._fetch_pypi_version)
                github_future = executor.submit(self._fetch_github_changelog)

                # Get PyPI result (this is required)
                latest_version, error = pypi_future.result()
                
                if error:
                    logger.debug(f"Update check failed: {error}")
                    return
                
                if not latest_version:
                    logger.debug("No version returned from PyPI")
                    return

                # Compare versions
                if version.parse(latest_version) > version.parse(self.current_version):
                    release_url = "https://github.com/oop7/YTSage/releases/latest"
                    
                    # Get GitHub changelog (may already be complete due to parallel execution)
                    changelog = github_future.result()
                    
                    self.update_available.emit(latest_version, release_url, changelog)

        except Exception as e:
            logger.debug(f"Failed to check for updates: {e}")


class YTSageApp(QMainWindow, FormatTableMixin, VideoInfoMixin, AnalysisMixin):  # Inherit from mixins

    def __init__(self) -> None:
        super().__init__()

        # Initialize localization system
        saved_language = ConfigManager.get("language") or "en"
        LocalizationManager.initialize(saved_language)

        self.version = APP_VERSION
        load_saved_path(self)
        # Load custom icon
        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))
        else:
            logger.warning(f"Icon file not found at {ICON_PATH}. Using default icon.")
            self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))  # Fallback
        self.signals = SignalManager()
        self.download_paused = False
        self.current_download = None
        self.download_cancelled = False
        self.is_updating_ytdlp = False  # Initialize update flag
        self.is_analyzing = False  # Initialize analysis flag
        self.save_thumbnail = False  # Initialize thumbnail state
        self.thumbnail_url = None  # Add this to store thumbnail URL
        self.all_formats = []  # Initialize all_formats
        self.available_subtitles = {}
        self.available_automatic_subtitles = {}
        self.is_playlist = False
        self.playlist_info = None
        self.video_info = None
        self.playlist_entries = []  # Initialize playlist entries
        self.selected_playlist_items = None  # Initialize selection string
        self.save_description = False  # Initialize description state
        self.embed_chapters = False  # Initialize chapters state
        self.subtitle_filter = ""
        self.thumbnail_image = None
        self.video_url = ""
        self.selected_subtitles = []  # Initialize selected subtitles list
        # Initialize cookie settings from saved config
        self._initialize_cookie_settings_from_config()
        # Initialize proxy settings from config
        self.proxy_url = ConfigManager.get("proxy_url")
        self.geo_proxy_url = ConfigManager.get("geo_proxy_url")
        self.speed_limit_value = None  # Store speed limit value
        self.speed_limit_unit_index = 0  # Store speed limit unit index (0: KB/s, 1: MB/s)
        self.download_section = None
        self.force_keyframes = False
        # Initialize output format settings
        self.force_output_format = ConfigManager.get("force_output_format") or False
        self.preferred_output_format = ConfigManager.get("preferred_output_format") or "mp4"
        self.force_audio_format = ConfigManager.get("force_audio_format") or False
        self.preferred_audio_format = ConfigManager.get("preferred_audio_format") or "best"
        self.audio_normalization = ConfigManager.get("audio_normalization") or False
        self.generic_mode_enabled = ConfigManager.get("generic_mode") or False
        # Track if video analysis is completed
        self.analysis_completed = False

        # Initialize audio player
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.init_ui()
        
        # Defer heavy start-up tasks to ensure UI renders immediately
        QTimer.singleShot(100, self._perform_startup_checks)

        self.setStyleSheet(StyleSheet.MAIN)
        self.signals.update_progress.connect(self.update_progress_bar)

        # After adding format buttons
        self.video_button.clicked.connect(self.filter_formats)  # Connect video button
        self.audio_button.clicked.connect(self.filter_formats)  # Connect audio button

        # Add connections to handle video/audio mode-specific controls
        self.video_button.clicked.connect(self.handle_mode_change)
        self.audio_button.clicked.connect(self.handle_mode_change)

        # Initialize UI state based on current mode
        self.handle_mode_change()


    def _perform_startup_checks(self):
        """Perform potentially blocking startup checks after UI is shown."""
        
        # Check for FFmpeg before proceeding
        if not check_ffmpeg():
            self.show_ffmpeg_dialog()

        # Check for yt-dlp in our app's bin directory or system PATH
        ytdlp_path = get_yt_dlp_path()
        if ytdlp_path == "yt-dlp":  # Not found in app dir or PATH
            self.show_ytdlp_setup_dialog()
        else:
            logger.info(f"Using yt-dlp from: {ytdlp_path}")

        # Check for Deno in our app's bin directory
        deno_path = get_deno_path()
        if deno_path == "deno":  # Not found in app dir
            self.show_deno_setup_dialog()
        else:
            logger.info(f"Using Deno from: {deno_path}")

        self.check_for_updates()

        # Check for auto-updates if enabled
        QTimer.singleShot(2000, self.check_auto_update_ytdlp) # Further delay auto-update check

    def play_notification_sound(self) -> None:
        """Play notification sound asynchronously (non-blocking)."""
        try:
            # Check if the notification sound file exists
            if not SOUND_PATH.exists():
                logger.warning(f"Notification sound file not found at: {SOUND_PATH}")
                return

            # Play the sound using QtMultimedia
            self.player.setSource(QUrl.fromLocalFile(str(SOUND_PATH)))
            self.player.play()
            logger.debug("Notification sound played")
        except Exception as e:
            logger.exception(f"Error playing notification sound: {e}")

    def _initialize_cookie_settings_from_config(self) -> None:
        """Initialize cookie settings and restore from last session if active."""
        self.cookie_file_path = None
        self.browser_cookies_option = None

        # Check if the user wants to remember cookies across sessions
        remember_val = ConfigManager.get("cookie_remember")
        should_remember = True if remember_val is None else remember_val
        
        if ConfigManager.get("cookie_active") and should_remember:
            source = ConfigManager.get("cookie_source")
            if source == "file":
                saved_path = ConfigManager.get("cookie_file_path")
                if saved_path and Path(saved_path).exists():
                    self.cookie_file_path = Path(saved_path)
                    logger.info(f"Restored cookie file from previous session: {self.cookie_file_path}")
            elif source == "browser":
                browser = ConfigManager.get("cookie_browser")
                profile = ConfigManager.get("cookie_browser_profile")
                if browser:
                    self.browser_cookies_option = f"{browser}:{profile}" if profile else browser
                    logger.info(f"Restored browser cookies from previous session: {self.browser_cookies_option}")
        else:
            # Revert activation back if the user opted NOT to remember them
            ConfigManager.set("cookie_active", False)
            logger.debug("Cookie settings initialized - no cookies active")

    def init_ui(self) -> None:
        self.setWindowTitle(f"{_('app.title')}  {_('app.version', version=self.version)}")
        self.setMinimumSize(900, 750)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)

        # URL input section
        url_layout = QHBoxLayout()
        url_layout.setSpacing(10)
        
        self.url_input = QLineEdit()
        self._update_url_placeholder()
        self.url_input.returnPressed.connect(self.analyze_url)  # Analyze on Enter key
        self.url_input.textChanged.connect(self._on_url_text_changed)  # Enable/disable analyze button
        self.url_input.setMinimumHeight(42)

        # Paste URL button
        self.paste_button = QPushButton(_("buttons.paste_url"))
        self.paste_button.clicked.connect(self.paste_url)
        self.paste_button.setMinimumHeight(42)
        self.paste_button.setMinimumWidth(115)
        self.paste_button.setStyleSheet(StyleSheet.PASTE_BUTTON)

        # Analyze button with app's red theme
        self.analyze_button = QPushButton(_("buttons.analyze"))
        self.analyze_button.clicked.connect(self.analyze_url)
        self.analyze_button.setEnabled(False)  # Disabled until URL is entered
        self.analyze_button.setMinimumHeight(42)
        self.analyze_button.setMinimumWidth(115)
        self.analyze_button.setStyleSheet(StyleSheet.ANALYZE_BUTTON)

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

        # Playlist buttons layout
        playlist_btns_layout = QHBoxLayout()

        # Add playlist selection BUTTON (initially hidden) - REPLACED QLineEdit
        self.playlist_select_btn = QPushButton(_("buttons.select_videos"))
        self.playlist_select_btn.clicked.connect(self.open_playlist_selection_dialog)
        self.playlist_select_btn.setVisible(False)
        self.playlist_select_btn.setStyleSheet(StyleSheet.PLAYLIST_BUTTON)
        playlist_btns_layout.addWidget(self.playlist_select_btn)

        # Save playlist as button
        self.save_playlist_btn = QPushButton(_("buttons.save_playlist", default="Save Playlist As"))
        self.save_playlist_btn.clicked.connect(self.save_playlist_to_file)
        self.save_playlist_btn.setVisible(False)
        self.save_playlist_btn.setStyleSheet(StyleSheet.PLAYLIST_BUTTON)
        playlist_btns_layout.addWidget(self.save_playlist_btn)

        layout.addLayout(playlist_btns_layout)
        # --- End Playlist Info Section ---

        # Format controls section with minimal spacing
        layout.addSpacing(5)

        # Format selection layout (horizontal)
        self.format_layout = QHBoxLayout()

        # Show formats label
        self.show_formats_label = QLabel(_("formats.show_formats"))
        self.show_formats_label.setStyleSheet("color: white;")
        self.format_layout.addWidget(self.show_formats_label)

        # Format buttons group
        self.format_buttons = QButtonGroup(self)
        self.format_buttons.setExclusive(True)

        # Video button
        self.video_button = QPushButton(_("buttons.video"))
        self.video_button.setCheckable(True)
        self.video_button.setChecked(True)  # Set video as default
        self.video_button.setStyleSheet(StyleSheet.FORMAT_TOGGLE_BUTTON)
        self.format_buttons.addButton(self.video_button)
        self.format_layout.addWidget(self.video_button)

        # Audio button
        self.audio_button = QPushButton(_("buttons.audio_only"))
        self.audio_button.setCheckable(True)
        self.audio_button.setStyleSheet(StyleSheet.FORMAT_TOGGLE_BUTTON)
        self.format_buttons.addButton(self.audio_button)
        self.format_layout.addWidget(self.audio_button)

        # Add Merge Subtitles checkbox (Moved here)
        self.merge_subs_checkbox = QCheckBox(_("main_ui.merge_subtitles"))
        self.merge_subs_checkbox.setStyleSheet(StyleSheet.CHECKBOX)
        # Initially disable it, will be enabled if subtitles are selected later
        self.merge_subs_checkbox.setEnabled(False)
        self.format_layout.addWidget(self.merge_subs_checkbox)

        # Add Save Thumbnail Checkbox (Moved here)
        self.save_thumbnail_checkbox = QCheckBox(_("main_ui.save_thumbnail"))
        self.save_thumbnail_checkbox.setChecked(False)
        self.save_thumbnail_checkbox.stateChanged.connect(self.toggle_save_thumbnail)
        self.save_thumbnail_checkbox.setStyleSheet(StyleSheet.CHECKBOX)
        self.format_layout.addWidget(self.save_thumbnail_checkbox)

        # Add Save Description Checkbox (Moved here)
        self.save_description_checkbox = QCheckBox(_("main_ui.save_description"))
        self.save_description_checkbox.setChecked(False)
        self.save_description_checkbox.stateChanged.connect(self.toggle_save_description)
        self.save_description_checkbox.setStyleSheet(StyleSheet.CHECKBOX)
        self.format_layout.addWidget(self.save_description_checkbox)

        # Add Embed Chapters Checkbox
        self.embed_chapters_checkbox = QCheckBox(_("main_ui.embed_chapters"))
        self.embed_chapters_checkbox.setChecked(False)
        self.embed_chapters_checkbox.stateChanged.connect(self.toggle_embed_chapters)
        self.embed_chapters_checkbox.setStyleSheet(StyleSheet.CHECKBOX)
        self.format_layout.addWidget(self.embed_chapters_checkbox)

        self.format_layout.addStretch()

        layout.addLayout(self.format_layout)

        # Format table with stretch
        format_table = self.setup_format_table()
        layout.addWidget(format_table, stretch=1)

        # Download section
        download_layout = QHBoxLayout()

        # Replace the two separate buttons with a single Custom Options button
        self.custom_options_btn = QPushButton(_("buttons.custom_options"))
        self.custom_options_btn.clicked.connect(self.show_custom_options)

        self.about_btn = QPushButton(_("buttons.about"))
        self.about_btn.clicked.connect(self.show_about_dialog)
        
        self.history_btn = QPushButton(_("buttons.history"))
        self.history_btn.clicked.connect(self.show_history_dialog)

        # Add new Time Range button
        self.time_range_btn = QPushButton(_("buttons.trim_video"))
        self.time_range_btn.clicked.connect(self.show_time_range_dialog)

        # --- Rename Path Button to Settings Button ---
        self.settings_button = QPushButton(_("buttons.download_settings"))  # Renamed button
        self.settings_button.clicked.connect(self.show_download_settings_dialog)  # Renamed method
        self._update_settings_tooltip()
        # --- End Settings Button ---

        self.download_btn = QPushButton(_("buttons.download"))
        self.download_btn.clicked.connect(self.start_download)

        # Add pause and cancel buttons
        self.pause_btn = QPushButton(_("buttons.pause"))
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setVisible(False)  # Hidden initially

        self.cancel_btn = QPushButton(_("buttons.cancel"))
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setVisible(False)  # Hidden initially

        # Add all buttons to layout in the correct order
        download_layout.addWidget(self.custom_options_btn)
        download_layout.addWidget(self.about_btn)
        download_layout.addWidget(self.history_btn)
        download_layout.addWidget(self.time_range_btn)  # New button position
        download_layout.addWidget(self.settings_button)
        download_layout.addWidget(self.download_btn)
        download_layout.addWidget(self.pause_btn)
        download_layout.addWidget(self.cancel_btn)

        layout.addLayout(download_layout)

        # Progress section with improved styling
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 10000)  # Use 0-10000 range for 0.01% precision
        self.progress_bar.setFormat("%p%")  # Display as percentage
        self.progress_bar.setStyleSheet(StyleSheet.PROGRESS_BAR)
        progress_layout.addWidget(self.progress_bar)
        
        # Setup smooth animation for progress bar
        self._progress_animation = QPropertyAnimation(self.progress_bar, b"value")
        self._progress_animation.setDuration(150)  # 150ms smooth transition
        self._progress_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Add download details label with improved styling
        self.download_details_label = QLabel()
        self.download_details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.download_details_label.setStyleSheet(StyleSheet.STATUS_LABEL)
        progress_layout.addWidget(self.download_details_label)

        # Create a horizontal layout for status label and open folder button
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel(_("app.ready"))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(StyleSheet.STATUS_LABEL)
        status_layout.addWidget(self.status_label)

        # Add "Open Folder" button (initially hidden)
        self.open_folder_btn = QPushButton("📁")
        self.open_folder_btn.setToolTip(_("buttons.open_folder"))
        self.open_folder_btn.setFixedSize(30, 30)
        self.open_folder_btn.setStyleSheet(StyleSheet.OPEN_FOLDER_BUTTON)
        self.open_folder_btn.clicked.connect(self.open_download_folder)
        self.open_folder_btn.setVisible(False)  # Hidden by default
        status_layout.addWidget(self.open_folder_btn)
        
        progress_layout.addLayout(status_layout)

        layout.addLayout(progress_layout)

        # Connect signals
        self.signals.update_formats.connect(self.update_format_table)
        self.signals.update_status.connect(self.set_status_message_animated)
        self.signals.update_progress.connect(self.update_progress_bar)

        # Connect new signals
        self.signals.playlist_info_label_visible.connect(lambda v: self.set_widget_visible_animated(self.playlist_info_label, v))
        self.signals.playlist_info_label_text.connect(self.playlist_info_label.setText)
        self.signals.selected_subs_label_text.connect(self.selected_subs_label.setText)
        self.signals.playlist_select_btn_visible.connect(lambda v: self.set_widget_visible_animated(self.playlist_select_btn, v))
        self.signals.playlist_select_btn_visible.connect(lambda v: self.set_widget_visible_animated(self.save_playlist_btn, v))
        self.signals.playlist_select_btn_text.connect(self.playlist_select_btn.setText)

        # Disable analysis-dependent controls until video is analyzed
        self.toggle_analysis_dependent_controls(enabled=False)

    def _on_url_text_changed(self, text: str) -> None:
        """Enable or disable the Analyze button based on URL input content."""
        self.analyze_button.setEnabled(bool(text.strip()))

    def _get_speed_limit_tooltip_text(self) -> str:
        """Return the current speed limit string for the settings tooltip."""
        if self.speed_limit_value:
            return f"{self.speed_limit_value} {['KB/s', 'MB/s'][self.speed_limit_unit_index]}"
        return _("main_ui.speed_limit_none")

    def _update_settings_tooltip(self) -> None:
        """Refresh the download settings tooltip text."""
        self.settings_button.setToolTip(
            _(
                "main_ui.settings_tooltip",
                path=self.last_path,
                speed_limit=self._get_speed_limit_tooltip_text(),
            )
        )

    def _update_url_placeholder(self) -> None:
        """Update the URL placeholder based on the selected validation mode."""
        placeholder_key = "main_ui.url_placeholder_generic" if self.generic_mode_enabled else "main_ui.url_placeholder"
        self.url_input.setPlaceholderText(_(placeholder_key))



    def paste_url(self) -> None:
        clipboard = QApplication.clipboard()
        self.url_input.setText(clipboard.text())

    def show_download_settings_dialog(self) -> None:  # Renamed method
        dialog = DownloadSettingsDialog(self.last_path, self.speed_limit_value, self.speed_limit_unit_index, self)
        if self.run_dialog_with_blur(dialog):
            # Update Path
            new_path = dialog.get_selected_path()
            path_changed = False
            if new_path != self.last_path:
                self.last_path = new_path
                save_path(self, self.last_path)  # Save the updated path
                path_changed = True
                logger.info(f"Download path updated to: {self.last_path}")

            # Update Speed Limit
            new_limit_value = dialog.get_selected_speed_limit()
            new_unit_index = dialog.get_selected_unit_index()
            limit_changed = False
            if new_limit_value != self.speed_limit_value or new_unit_index != self.speed_limit_unit_index:
                self.speed_limit_value = new_limit_value
                self.speed_limit_unit_index = new_unit_index
                limit_changed = True
                logger.info(
                    f"Speed limit updated to: {self.speed_limit_value} {['KB/s', 'MB/s'][self.speed_limit_unit_index] if self.speed_limit_value else 'None'}"
                )

            # Update Output Format Settings
            new_force_format = dialog.get_force_format_enabled()
            new_preferred_format = dialog.get_preferred_format()
            format_changed = False
            if new_force_format != self.force_output_format or new_preferred_format != self.preferred_output_format:
                self.force_output_format = new_force_format
                self.preferred_output_format = new_preferred_format
                format_changed = True
                logger.info(f"Output format settings updated - Force: {self.force_output_format}, Preferred: {self.preferred_output_format}")

            # Update Audio Format Settings
            new_force_audio_format = dialog.get_force_audio_format_enabled()
            new_preferred_audio_format = dialog.get_preferred_audio_format()
            new_audio_normalization = dialog.get_audio_normalization_enabled()
            audio_format_changed = False
            if (new_force_audio_format != self.force_audio_format or 
                new_preferred_audio_format != self.preferred_audio_format or
                new_audio_normalization != self.audio_normalization):
                self.force_audio_format = new_force_audio_format
                self.preferred_audio_format = new_preferred_audio_format
                self.audio_normalization = new_audio_normalization
                audio_format_changed = True
                logger.info(f"Audio format settings updated - Force: {self.force_audio_format}, Preferred: {self.preferred_audio_format}, Norm: {self.audio_normalization}")

            # Update Generic Mode Setting
            new_generic_mode = dialog.get_generic_mode_enabled()
            generic_mode_changed = False
            if new_generic_mode != self.generic_mode_enabled:
                self.generic_mode_enabled = new_generic_mode
                generic_mode_changed = True
                self._update_url_placeholder()
                logger.info(f"Generic mode updated - Enabled: {self.generic_mode_enabled}")

            # Update Tooltip if anything changed
            if path_changed or limit_changed or format_changed or audio_format_changed or generic_mode_changed:
                self._update_settings_tooltip()

    def start_download(self) -> None:
        if self.is_updating_ytdlp:
            QMessageBox.warning(self, _("update.update_in_progress_title"), _("update.update_in_progress_message"))
            return

        url = self.url_input.text().strip()
        # --- Use self.last_path instead of reading from QLineEdit ---
        path = self.last_path

        if not url or not path:
            # More specific error message if path is missing
            if not path:
                self.set_status_message_animated(_('download.please_set_path'))
                self.animate_widget_shake(self.settings_button)
            elif not url:
                self.set_status_message_animated(_('download.please_enter_url'))
                self.animate_widget_shake(self.url_input)
            else:
                self.set_status_message_animated(_('download.please_enter_url_and_path'))
                self.animate_widget_shake(self.url_input)
                self.animate_widget_shake(self.settings_button)
            return
        # --- End Path Change ---
        
        # Validate URL before starting download
        is_valid, error_message = validate_video_url(url, generic_mode=self.generic_mode_enabled)
        if not is_valid:
            QMessageBox.warning(self, _("main_ui.error_title"), error_message)
            self.animate_widget_shake(self.url_input)
            return

        # Get selected format
        selected_format = self.get_selected_format()
        if not selected_format:
            self.set_status_message_animated(_('download.please_select_format'))
            self.animate_widget_shake(self.format_table)
            return
        format_id = selected_format["format_id"]
        is_audio_only = bool(selected_format.get("is_audio_only"))
        format_has_audio = bool(selected_format.get("has_audio"))

        # Show preparation message
        self.status_label.setText(_('download.preparing'))
        self.progress_bar.setValue(0)  # Reset progress (range is 0-10000)
        self.open_folder_btn.setVisible(False)  # Hide the open folder button on new download

        # Get resolution for filename
        resolution = "default"
        for row in range(self.format_table.rowCount()):
            cell_widget = self.format_table.cellWidget(row, 0)
            if cell_widget:
                cb = cell_widget.layout().itemAt(0).widget()
                if isinstance(cb, QCheckBox) and cb.isChecked():
                    if self.is_playlist:
                        res_item = self.format_table.item(row, 2)
                    else:
                        res_item = self.format_table.item(row, 3)
                    
                    if res_item and res_item.text() != "N/A":
                        resolution = res_item.text().replace("≤ ", "").strip()
                    break

        # Get subtitle selection if available - Now get the list
        selected_subs = self.selected_subtitles if hasattr(self, "selected_subtitles") else []

        # Get playlist selection IF in playlist mode - USE STORED VALUE
        playlist_items_to_download = None
        if self.is_playlist:
            playlist_items_to_download = self.selected_playlist_items  # Use the stored selection string

        # --- Use stored speed limit values ---
        rate_limit = None
        if self.speed_limit_value:
            try:
                limit_value = float(self.speed_limit_value)
                if self.speed_limit_unit_index == 0:  # KB/s
                    rate_limit = f"{int(limit_value * 1024)}"
                elif self.speed_limit_unit_index == 1:  # MB/s
                    rate_limit = f"{int(limit_value * 1024 * 1024)}"
            except ValueError:
                # Use a signal to show error in status bar, similar to URL/Path errors
                self.signals.update_status.emit(_("errors.invalid_speed_limit"))
                return
        # --- End speed limit update ---

        # Save thumbnail if enabled
        if self.save_thumbnail:
            # Consider moving thumbnail download *after* successful video download
            # Or handle errors more gracefully if thumbnail download fails
            try:
                self.download_thumbnail_file(url, path)
            except Exception as e:
                logger.warning(f"Thumbnail download failed: {e}", exc_info=True)
                # Optionally inform the user, but don't stop the main download

        # Get filename format from config
        filename_format = ConfigManager.get("filename_format")
        concurrent_fragments = ConfigManager.get("concurrent_fragments") or 1

        # Create download thread with resolution in output template
        self.download_thread = DownloadThread(
            url=url,
            path=path,
            format_id=format_id,
            is_audio_only=is_audio_only,
            format_has_audio=format_has_audio,
            subtitle_langs=selected_subs,  # Pass the list of selected subs
            is_playlist=self.is_playlist,  # Use the flag directly
            merge_subs=self.merge_subs_checkbox.isChecked(),
            enable_sponsorblock=len(self.selected_sponsorblock_categories) > 0,
            sponsorblock_categories=self.selected_sponsorblock_categories,
            resolution=resolution,
            playlist_items=playlist_items_to_download,  # Pass the selection string
            save_description=self.save_description,  # Pass the new flag here
            embed_chapters=self.embed_chapters,  # Pass the embed chapters flag
            cookie_file=self.cookie_file_path,  # Pass the cookie file path
            browser_cookies=self.browser_cookies_option,  # Pass the browser cookies option
            rate_limit=rate_limit,  # Pass the calculated rate limit
            download_section=self.download_section,  # Pass the download section
            force_keyframes=self.force_keyframes,  # Pass the force keyframes setting
            proxy_url=self.proxy_url,  # Pass the proxy URL
            geo_proxy_url=self.geo_proxy_url,  # Pass the geo-verification proxy URL
            force_output_format=self.force_output_format,  # Pass force output format setting
            preferred_output_format=self.preferred_output_format,  # Pass preferred format
            force_audio_format=self.force_audio_format,  # Pass force audio format setting
            preferred_audio_format=self.preferred_audio_format,  # Pass preferred audio format
            audio_normalization=self.audio_normalization,  # Pass audio normalization setting
            filename_format=filename_format,  # Pass the filename format
            concurrent_fragments=concurrent_fragments, # Pass the concurrent fragments
        )

        # Connect signals
        self.download_thread.progress_signal.connect(self.update_progress_bar)
        self.download_thread.status_signal.connect(self.set_status_message_animated)
        self.download_thread.update_details.connect(self.download_details_label.setText)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.error_signal.connect(self.download_error)
        self.download_thread.file_exists_signal.connect(self.file_already_exists)

        # Reset download state
        self.download_paused = False
        self.download_cancelled = False

        # Show pause/cancel buttons
        self.pause_btn.setText(_("buttons.pause"))
        self.animate_widget_fade_in(self.pause_btn)
        self.animate_widget_fade_in(self.cancel_btn)

        # Start download thread
        self.current_download = self.download_thread
        self.download_thread.start()
        self.toggle_download_controls(False)

    def download_finished(self) -> None:
        self.toggle_download_controls(True)
        self.animate_widget_fade_out(self.pause_btn)
        self.animate_widget_fade_out(self.cancel_btn)
        self.progress_bar.setValue(10000)  # 100% in 0-10000 range

        # Set completion message based on the file type of last downloaded file
        if self.download_thread and self.download_thread.current_filename:
            filename = Path(self.download_thread.current_filename)
            ext = filename.suffix.lower()

            # Video file extensions
            if ext in VIDEO_EXTENSIONS:
                self.set_status_message_animated(_('download.video_completed'))
            # Audio file extensions
            elif ext in AUDIO_EXTENSIONS:
                self.set_status_message_animated(_('download.audio_completed'))
            # Subtitle file extensions
            elif ext in SUBTITLE_EXTENSIONS:
                self.set_status_message_animated(_('download.subtitle_completed'))
            # Default case
            else:
                self.set_status_message_animated(_('download.completed'))
            
            # Show the open folder button
            self.animate_widget_fade_in(self.open_folder_btn)
            
            # Save to history
            try:
                if self.download_thread.last_file_path and self.video_info:
                    # Get video information
                    title = self.video_info.get("title", _("video_info.unknown_title"))
                    channel = self.video_info.get("channel", None) or self.video_info.get("uploader", None)
                    duration = self.video_info.get("duration_string", None)
                    
                    # Prepare download options
                    download_options = {
                        "format_id": self.download_thread.format_id,
                        "subtitle_langs": self.download_thread.subtitle_langs,
                        "merge_subs": self.download_thread.merge_subs,
                        "enable_sponsorblock": self.download_thread.enable_sponsorblock,
                        "sponsorblock_categories": self.download_thread.sponsorblock_categories,
                        "save_description": self.download_thread.save_description,
                        "embed_chapters": self.download_thread.embed_chapters,
                        "download_section": self.download_thread.download_section,
                        "force_keyframes": self.download_thread.force_keyframes,
                    }
                    
                    # Add to history
                    HistoryManager.add_entry(
                        title=title,
                        url=self.video_url,
                        thumbnail_url=self.thumbnail_url,
                        file_path=str(self.download_thread.last_file_path),
                        format_id=self.download_thread.format_id,
                        is_audio_only=self.download_thread.is_audio_only,
                        resolution=self.download_thread.resolution,
                        channel=channel,
                        duration=duration,
                        download_options=download_options,
                    )
                    logger.info(f"Added download to history: {title}")
            except Exception as e:
                logger.error(f"Error saving to history: {e}", exc_info=True)

        # Play notification sound when download completes
        self.play_notification_sound()

    def open_download_folder(self) -> None:
        """Open the folder containing the downloaded file and select it if possible"""
        try:
            if self.download_thread and self.download_thread.last_file_path:
                file_path = Path(self.download_thread.last_file_path)
                
                if file_path.exists():
                    # On Windows, use explorer with /select to highlight the file
                    if subprocess.sys.platform == "win32":
                        subprocess.run(['explorer', '/select,', str(file_path)], creationflags=SUBPROCESS_CREATIONFLAGS)
                    # On macOS, use open with -R to reveal in Finder
                    elif subprocess.sys.platform == "darwin":
                        subprocess.run(['open', '-R', str(file_path)])
                    # On Linux, try to open the folder (file selection not widely supported)
                    else:
                        folder_path = file_path.parent
                        subprocess.run(['xdg-open', str(folder_path)])
                    
                    logger.info(f"Opened folder for: {file_path}")
                else:
                    # If file doesn't exist, just open the download folder
                    folder_path = Path(self.last_path)
                    if folder_path.exists():
                        if subprocess.sys.platform == "win32":
                            subprocess.run(['explorer', str(folder_path)], creationflags=SUBPROCESS_CREATIONFLAGS)
                        elif subprocess.sys.platform == "darwin":
                            subprocess.run(['open', str(folder_path)])
                        else:
                            subprocess.run(['xdg-open', str(folder_path)])
                    else:
                        logger.warning(f"Download folder does not exist: {folder_path}")
            else:
                # Fallback to opening the general download folder
                folder_path = Path(self.last_path)
                if folder_path.exists():
                    if subprocess.sys.platform == "win32":
                        subprocess.run(['explorer', str(folder_path)], creationflags=SUBPROCESS_CREATIONFLAGS)
                    elif subprocess.sys.platform == "darwin":
                        subprocess.run(['open', str(folder_path)])
                    else:
                        subprocess.run(['xdg-open', str(folder_path)])
                else:
                    logger.warning(f"Download folder does not exist: {folder_path}")
                    
        except Exception as e:
            logger.exception(f"Error opening download folder: {e}")
            QMessageBox.warning(self, _("main_ui.error_title"), _("main_ui.open_folder_error", error=str(e)))

    def download_error(self, error_message) -> None:
        self.toggle_download_controls(True)
        self.pause_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.status_label.setText(_("errors.generic_error", error=error_message))
        self.download_details_label.setText("")  # Clear details label on error

    def update_progress_bar(self, value) -> None:
        try:
            # Scale float percentage (0-100) to progress bar range (0-10000) for precision
            scaled_value = int(float(value) * 100)
            
            # Use smooth animation for progress updates
            if self._progress_animation.state() == QPropertyAnimation.State.Running:
                self._progress_animation.stop()
            
            current_value = self.progress_bar.value()
            # Only animate if there's a meaningful change (avoid micro-animations)
            if abs(scaled_value - current_value) > 10:  # More than 0.1% change
                self._progress_animation.setStartValue(current_value)
                self._progress_animation.setEndValue(scaled_value)
                self._progress_animation.start()
            else:
                self.progress_bar.setValue(scaled_value)
        except Exception as e:
            logger.exception(f"Progress bar update error: {e}")

    def toggle_pause(self) -> None:
        if self.current_download:
            self.current_download.paused = not self.current_download.paused
            if self.current_download.paused:
                self.pause_btn.setText(_("buttons.resume"))
                self.signals.update_status.emit(_("download.paused"))
            else:
                self.pause_btn.setText(_("buttons.pause"))
                self.signals.update_status.emit(_("download.resumed"))

    def check_for_updates(self) -> None:
        """Starts the update check in a background thread."""
        if ConfigManager.get("check_app_updates") is False:
            logger.info("App version checker is disabled in settings.")
            return

        self.update_thread = UpdateCheckThread(self.version)
        self.update_thread.update_available.connect(self.show_update_dialog)
        self.update_thread.start()

    def show_update_dialog(self, latest_version, release_url, changelog) -> None:  # Added changelog parameter
        msg = QDialog(self)
        msg.setWindowTitle(_("update_dialog.title"))
        msg.setMinimumWidth(600)  # Increased width for better layout
        msg.setMinimumHeight(450)  # Increased height for better spacing

        # Set custom icon directly
        try:
            if self.windowIcon() and not self.windowIcon().isNull():
                msg.setWindowIcon(self.windowIcon())
            else:
                # Fallback to icon file
                # icon_path logic moved to src\utils\ytsage_constants.py
                if ICON_PATH.exists():
                    msg.setWindowIcon(QIcon(str(ICON_PATH)))
        except Exception:
            pass

        layout = QVBoxLayout(msg)
        layout.setSpacing(15)  # Increased spacing for better layout
        layout.setContentsMargins(20, 20, 20, 20)  # Added margins

        # Header with icon and title
        header_layout = QHBoxLayout()

        # Add update icon
        icon_label = QLabel()
        icon_label.setPixmap(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload).pixmap(32, 32))
        header_layout.addWidget(icon_label)

        # Title
        title_label = QLabel(f"<h2 style='color: #c90000; margin: 0;'>{_('update_dialog.title')}</h2>")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Update message with better formatting
        message_label = QLabel(
            f"<div style='font-size: 13px; line-height: 1.4;'>"
            f"<b style='color: #ffffff;'>{_('update_dialog.new_version_available')}</b><br><br>"
            f"<span style='color: #cccccc;'>{_('update_dialog.current_version_label')} <b style='color: #ffffff;'>{self.version}</b></span><br>"
            f"<span style='color: #cccccc;'>{_('update_dialog.latest_version_label')} <b style='color: #00ff88;'>{latest_version}</b></span>"
            f"</div>"
        )
        message_label.setWordWrap(True)
        message_label.setStyleSheet(StyleSheet.UPDATE_DIALOG_MESSAGE)
        layout.addWidget(message_label)

        # Changelog Section
        changelog_label = QLabel(f"<b style='color: #ffffff; font-size: 14px;'>{_('update_dialog.changelog')}:</b>")
        changelog_label.setStyleSheet("padding: 5px 0; margin-top: 10px;")
        layout.addWidget(changelog_label)

        changelog_text = QTextEdit()
        changelog_text.setReadOnly(True)
        # Convert Markdown to HTML and set it
        try:
            html_changelog = markdown.markdown(
                changelog,
                extensions=[
                    "markdown.extensions.tables",
                    "markdown.extensions.fenced_code",
                ],
            )
            changelog_text.setHtml(html_changelog)
        except Exception as e:
            logger.warning(f"Error converting changelog markdown to HTML: {e}", exc_info=True)
            changelog_text.setPlainText(changelog)  # Fallback to plain text

        changelog_text.setStyleSheet(StyleSheet.UPDATE_DIALOG_CHANGELOG)
        changelog_text.setMaximumHeight(180)  # Limit height
        layout.addWidget(changelog_text)

        # Buttons with better styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        download_btn = QPushButton(_('update_dialog.download_update'))
        download_btn.clicked.connect(lambda: self.open_release_page(release_url))
        download_btn.setStyleSheet(StyleSheet.UPDATE_DIALOG_DOWNLOAD_BTN)

        remind_btn = QPushButton(_('update_dialog.remind_later'))
        remind_btn.clicked.connect(msg.close)
        remind_btn.setStyleSheet(StyleSheet.UPDATE_DIALOG_REMIND_BTN)

        button_layout.addStretch()
        button_layout.addWidget(download_btn)
        button_layout.addWidget(remind_btn)
        layout.addLayout(button_layout)

        # Style the dialog with improved theme matching
        msg.setStyleSheet(StyleSheet.UPDATE_DIALOG_MAIN)

        self.run_dialog_with_blur(msg)

    def open_release_page(self, url):
        webbrowser.open(url)

    def check_auto_update_ytdlp(self) -> None:
        """Check and perform auto-update for yt-dlp if enabled and due."""
        try:
            # Check if auto-update should be performed
            if should_check_for_auto_update():
                logger.info("Performing auto-update check for yt-dlp...")
                # Perform the auto-update in a non-blocking way
                # We don't want to block the UI startup for this
                QTimer.singleShot(2000, self._perform_auto_update)  # Delay 2 seconds after startup
        except Exception as e:
            logger.exception(f"Error in auto-update check: {e}")

    def _perform_auto_update(self) -> None:
        """Actually perform the auto-update check and update if needed in a background thread."""
        # Check if a download is currently running or analysis is in progress
        if (self.current_download and self.current_download.isRunning()) or self.is_analyzing:
            logger.info("Download or analysis in progress, skipping auto-update check.")
            return

        try:
            self.is_updating_ytdlp = True  # Set flag
            # Create and start the auto-update thread to avoid blocking the UI

            self.auto_update_thread = AutoUpdateThread()
            self.auto_update_thread.update_finished.connect(self._on_auto_update_finished)
            self.auto_update_thread.start()
        except Exception as e:
            self.is_updating_ytdlp = False  # Reset flag on error
            logger.exception(f"Error starting auto-update thread: {e}")

    def _on_auto_update_finished(self, success, message) -> None:
        self.is_updating_ytdlp = False  # Reset flag
        """Handle auto-update completion."""
        if success:
            logger.info(f"Auto-update completed successfully: {message}")
        else:
            logger.warning(f"Auto-update completed with issues: {message}")

        # Clean up the thread reference and ensure it's properly finished
        if hasattr(self, "auto_update_thread"):
            # Disconnect all signals to prevent further callbacks
            self.auto_update_thread.update_finished.disconnect()
            # Make sure thread is finished
            if self.auto_update_thread.isRunning():
                self.auto_update_thread.quit()
                self.auto_update_thread.wait(1000)  # Wait up to 1 second
            # Remove the reference
            delattr(self, "auto_update_thread")

    def closeEvent(self, event) -> None:
        """Handle application close event to ensure proper cleanup of background threads."""
        try:
            # Stop the analysis thread if it's running
            if hasattr(self, "_analysis_thread") and self._analysis_thread is not None and self._analysis_thread.isRunning():
                logger.info("Stopping analysis thread...")
                self._analysis_thread.cancel()
                if not self._analysis_thread.wait(2000):  # Wait up to 2 seconds
                    logger.warning("Force terminating analysis thread...")
                    self._analysis_thread.terminate()
                    self._analysis_thread.wait(1000)

            # Stop the auto-update thread if it's running
            if hasattr(self, "auto_update_thread") and self.auto_update_thread.isRunning():
                logger.info("Stopping auto-update thread...")
                self.auto_update_thread.quit()
                if not self.auto_update_thread.wait(3000):  # Wait up to 3 seconds for graceful shutdown
                    logger.warning("Force terminating auto-update thread...")
                    self.auto_update_thread.terminate()
                    self.auto_update_thread.wait(1000)  # Wait for termination

            # Cancel any running downloads
            if self.current_download and self.current_download.isRunning():
                logger.info("Canceling running download...")
                self.current_download.cancel()
                if not self.current_download.wait(3000):  # Wait up to 3 seconds for graceful shutdown
                    logger.warning("Force terminating download thread...")
                    self.current_download.terminate()
                    self.current_download.wait(1000)  # Wait for termination

            logger.info("Application closing...")
            event.accept()
        except Exception as e:
            logger.exception(f"Error during application close: {e}")
            event.accept()  # Accept the close event anyway

    def show_custom_options(self) -> None:
        dialog = CustomOptionsDialog(self)
        if self.run_dialog_with_blur(dialog):
            # Handle proxy options
            proxy_url = dialog.get_proxy_url()
            geo_proxy_url = dialog.get_geo_proxy_url()

            # Update instance variables
            self.proxy_url = proxy_url
            self.geo_proxy_url = geo_proxy_url

            # Save proxy settings to config
            ConfigManager.set("proxy_url", proxy_url)
            ConfigManager.set("geo_proxy_url", geo_proxy_url)

            # Show confirmation messages
            if proxy_url:
                logger.info(f"Main proxy set: {self.proxy_url}")
                QMessageBox.information(
                    self,
                    _("proxy.set_title"),
                    _("proxy.set_message", proxy=proxy_url),
                )

            if geo_proxy_url:
                logger.info(f"Geo-verification proxy set: {self.geo_proxy_url}")
                QMessageBox.information(
                    self,
                    _("proxy.geo_set_title"),
                    _("proxy.geo_set_message", proxy=geo_proxy_url),
                )

            # Show a combined message if both are cleared
            if not proxy_url and not geo_proxy_url and (ConfigManager.get("proxy_url") or ConfigManager.get("geo_proxy_url")):
                QMessageBox.information(
                    self,
                    _("proxy.cleared_title"),
                    _("proxy.cleared_message"),
                )

    def show_about_dialog(self) -> None:  # ADDED METHOD HERE
        dialog = AboutDialog(self)
        self.run_dialog_with_blur(dialog)
    
    def show_history_dialog(self) -> None:
        """Show the download history dialog."""
        dialog = HistoryDialog(self)
        dialog.redownload_requested.connect(self.handle_redownload_from_history)
        self.run_dialog_with_blur(dialog)
    
    def handle_redownload_from_history(self, entry: dict) -> None:
        """Handle redownload request from history dialog."""
        try:
            # Set URL
            url = entry.get("url", "")
            if url:
                self.url_input.setText(url)
                self.video_url = url
                
                # Analyze the URL to get format info
                logger.info(f"Redownloading from history: {entry.get('title', 'Unknown')}")
                QMessageBox.information(
                    self,
                    _("history.redownload_started"),
                    _("history.redownload_started") + f"\n\n{entry.get('title', '')}"
                )
                
                # Trigger analysis
                self.analyze_url()
            else:
                QMessageBox.warning(self, _("main_ui.error_title"), _("history.no_url_error"))
        except Exception as e:
            logger.error(f"Error handling redownload from history: {e}", exc_info=True)
            QMessageBox.warning(self, _("main_ui.error_title"), _("history.redownload_failed", error=str(e)))

    def file_already_exists(self, filename) -> None:
        """Handle case when file already exists - simplified version"""
        self.toggle_download_controls(True)
        self.pause_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.progress_bar.setValue(10000)  # 100% in 0-10000 range

        # Determine file type based on extension
        ext = Path(filename).suffix.lower()

        # Video file extensions
        if ext in VIDEO_EXTENSIONS:
            self.status_label.setText(_("status.video_file_exists"))
        # Audio file extensions
        elif ext in AUDIO_EXTENSIONS:
            self.status_label.setText(_("status.audio_file_exists"))
        # Subtitle file extensions
        elif ext in SUBTITLE_EXTENSIONS:
            self.status_label.setText(_("status.subtitle_file_exists"))
        # Default case
        else:
            self.status_label.setText(_("status.file_exists"))

        # Show a simple message dialog
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle(_("file_exists_dialog.title"))
        msg_box.setText(_("file_exists_dialog.message", filename=filename))
        msg_box.setInformativeText(_("file_exists_dialog.info"))
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        # Set the window icon to match the main application
        msg_box.setWindowIcon(self.windowIcon())

        # Style the dialog
        msg_box.setStyleSheet(StyleSheet.FILE_EXISTS_DIALOG)

        msg_box.exec()


    # --- Add Toggle Methods Here ---
    def toggle_save_thumbnail(self, state) -> None:
        logger.debug(f"Raw thumbnail state received: {state}")  # Debug: Print raw state
        self.save_thumbnail = bool(state == 2)  # Compare state directly with 2 (Checked state)
        logger.debug(f"Save thumbnail toggled: {self.save_thumbnail}")

    def toggle_save_description(self, state) -> None:
        logger.debug(f"Raw description state received: {state}")  # Debug: Print raw state
        self.save_description = bool(state == 2)  # Compare state directly with 2 (Checked state)
        logger.debug(f"Save description toggled: {self.save_description}")

    def toggle_embed_chapters(self, state) -> None:
        logger.debug(f"Raw chapters state received: {state}")  # Debug: Print raw state
        self.embed_chapters = bool(state == 2)  # Compare state directly with 2 (Checked state)
        logger.debug(f"Embed chapters toggled: {self.embed_chapters}")

    # --- End Toggle Methods ---

    def open_playlist_selection_dialog(self) -> None:
        if not self.is_playlist or not self.playlist_entries:
            logger.info("No playlist data available to select from.")
            return

        dialog = PlaylistSelectionDialog(self.playlist_entries, self.selected_playlist_items, self)

        if self.run_dialog_with_blur(dialog):
            self.selected_playlist_items = dialog.get_selected_items_string()
            logger.info(f"Playlist items selected: {self.selected_playlist_items}")

            # Update button text (this call is safe as it happens in the main thread after dialog closes)
            if self.selected_playlist_items is None:
                button_text = "Select Videos... (All selected)"
            else:
                selected_indices = dialog._parse_selection_string(self.selected_playlist_items)
                count = len(selected_indices)
                display_text = (
                    self.selected_playlist_items if len(self.selected_playlist_items) < 30 else f"{count} videos selected"
                )
                button_text = f"Select Videos... ({display_text})"
            self.playlist_select_btn.setText(button_text)  # Direct call is fine here

    def save_playlist_to_file(self) -> None:
        """Save current playlist URLs/info to a file."""
        if not getattr(self, "playlist_entries", None):
            QMessageBox.warning(self, _("playlist.save_error_title", default="Save Error"), _("playlist.no_videos_to_save", default="No playlist entries gathered!"))
            return
            
        default_dir = str(Path(self.last_path) / "playlist.txt")
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            _("playlist.save_as", default="Save Playlist As"),
            default_dir,
            "Text files (*.txt);;M3U playlists (*.m3u);;CSV files (*.csv);;JSON files (*.json)"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if "Text files" in selected_filter:
                    for index, entry in enumerate(self.playlist_entries):
                        duration = entry.get("duration")
                        duration_str = ""
                        if duration:
                            try:
                                m, s = divmod(int(duration), 60)
                                h, m = divmod(m, 60)
                                if h > 0:
                                    duration_str = f" [{h}:{m:02d}:{s:02d}]"
                                else:
                                    duration_str = f" [{m:02d}:{s:02d}]"
                            except (ValueError, TypeError):
                                pass
                        
                        title = entry.get('title', f'Video {index + 1}')
                        # Formatting output to include index and duration
                        f.write(f"{index + 1}. {title}{duration_str} - {entry.get('url', '')}\n")
                elif "M3U" in selected_filter:
                    f.write("#EXTM3U\n")
                    for entry in self.playlist_entries:
                        duration = int(entry.get('duration', 0)) if entry.get('duration') else 0
                        title = entry.get('title', 'Unknown Title')
                        f.write(f"#EXTINF:{duration},{title}\n{entry.get('url', '')}\n")
                elif "CSV" in selected_filter:
                    import csv
                    writer = csv.writer(f, lineterminator='\n')
                    # Adding Playlist Index to CSV and formatting Title with index and duration
                    writer.writerow(['Playlist Index', 'Title', 'URL', 'Duration', 'Uploader'])
                    for index, entry in enumerate(self.playlist_entries):
                        duration = entry.get("duration")
                        duration_str = ""
                        if duration:
                            try:
                                m, s = divmod(int(duration), 60)
                                h, m = divmod(m, 60)
                                if h > 0:
                                    duration_str = f" [{h}:{m:02d}:{s:02d}]"
                                else:
                                    duration_str = f" [{m:02d}:{s:02d}]"
                            except (ValueError, TypeError):
                                pass
                        
                        title = entry.get('title', f'Video {index + 1}')
                        formatted_title = f"{index + 1}. {title}{duration_str}"
                        writer.writerow([index + 1, formatted_title, entry.get('url', ''), entry.get('duration', ''), entry.get('uploader', '')])
                elif "JSON" in selected_filter:
                    import json
                    json.dump(self.playlist_entries, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, _("playlist.save_success_title", default="Success"), _("playlist.saved_successfully", default="Playlist saved successfully."))
        except Exception as e:
            logger.exception(f"Error saving playlist: {e}")
            QMessageBox.critical(self, _("playlist.save_error_title", default="Error"), _("playlist.save_error_msg", default="Failed to save playlist."))

    # --- New Slot for Updating Playlist Button Text ---
    # moved to SignalManager as Signal and added to init_ui() method.

    def toggle_download_controls(self, enabled=True) -> None:
        """Enable or disable download-related controls"""
        self.url_input.setEnabled(enabled)
        # Analyze button should only be enabled if there's text in the URL input
        if enabled:
            self.analyze_button.setEnabled(bool(self.url_input.text().strip()))
        else:
            self.analyze_button.setEnabled(False)
        self.format_table.setEnabled(enabled)  # Changed from format_scroll_area to format_table
        self.download_btn.setEnabled(enabled)
        if hasattr(self, "subtitle_combo"):
            self.subtitle_combo.setEnabled(enabled)  # type: ignore[reportAttributeAccessIssue]
        self.video_button.setEnabled(enabled)
        self.audio_button.setEnabled(enabled)
        if hasattr(self, "sponsorblock_select_btn"):
            self.sponsorblock_select_btn.setEnabled(enabled)
        self.merge_subs_checkbox.setEnabled(enabled)  # Enable/disable merge subs checkbox
        self.custom_options_btn.setEnabled(enabled)  # Enable/disable custom options button
        self.time_range_btn.setEnabled(enabled)  # Enable/disable time range button
        self.settings_button.setEnabled(enabled)  # Enable/disable settings button

        # Clear progress/status when controls are re-enabled
        if enabled:
            self.progress_bar.setValue(0)  # Reset progress (range is 0-10000)
            self.status_label.setText(_("status.ready"))
            self.download_details_label.setText("")  # Clear details label

    @Slot(bool)
    def toggle_analysis_dependent_controls(self, enabled=True) -> None:
        """Enable or disable controls that require video analysis to be completed"""
        # Determine tooltip text for disabled state
        tooltip_text = "" if enabled else _("main_ui.analyze_first_tooltip")
        
        # Subtitle selection
        if hasattr(self, "subtitle_select_btn"):
            self.subtitle_select_btn.setEnabled(enabled)
            if not enabled:
                self.subtitle_select_btn.setToolTip(tooltip_text)
            else:
                self.subtitle_select_btn.setToolTip("")
        
        # SponsorBlock (only if not in audio mode)
        if hasattr(self, "sponsorblock_select_btn"):
            is_audio_mode = self.audio_button.isChecked()
            self.sponsorblock_select_btn.setEnabled(enabled and not is_audio_mode)
            if not enabled or is_audio_mode:
                self.sponsorblock_select_btn.setToolTip(tooltip_text if not enabled else _("main_ui.audio_mode_disabled"))
            else:
                self.sponsorblock_select_btn.setToolTip("")
        
        # Save Thumbnail checkbox
        if hasattr(self, "save_thumbnail_checkbox"):
            self.save_thumbnail_checkbox.setEnabled(enabled)
            if not enabled:
                self.save_thumbnail_checkbox.setToolTip(tooltip_text)
            else:
                self.save_thumbnail_checkbox.setToolTip("")
        
        # Save Description checkbox
        if hasattr(self, "save_description_checkbox"):
            self.save_description_checkbox.setEnabled(enabled)
            if not enabled:
                self.save_description_checkbox.setToolTip(tooltip_text)
            else:
                self.save_description_checkbox.setToolTip("")
        
        # Embed Chapters checkbox
        if hasattr(self, "embed_chapters_checkbox"):
            self.embed_chapters_checkbox.setEnabled(enabled)
            if not enabled:
                self.embed_chapters_checkbox.setToolTip(tooltip_text)
            else:
                self.embed_chapters_checkbox.setToolTip("")
        
        # Merge Subtitles (only if subtitles are selected and not in audio mode)
        if hasattr(self, "merge_subs_checkbox"):
            has_subs = len(getattr(self, "selected_subtitles", [])) > 0
            is_audio_mode = self.audio_button.isChecked()
            should_enable = enabled and has_subs and not is_audio_mode
            self.merge_subs_checkbox.setEnabled(should_enable)
            if not enabled:
                self.merge_subs_checkbox.setToolTip(tooltip_text)
            elif not has_subs:
                self.merge_subs_checkbox.setToolTip(_("main_ui.select_subtitles_first"))
            elif is_audio_mode:
                self.merge_subs_checkbox.setToolTip(_("main_ui.audio_mode_disabled"))
            else:
                self.merge_subs_checkbox.setToolTip("")

    def handle_format_selection(self, button) -> None:
        # Update formats
        self.filter_formats()

    def handle_mode_change(self) -> None:
        """Enable or disable features based on video/audio mode"""
        # Only allow enabling if analysis is complete
        can_enable = self.analysis_completed
        
        if self.audio_button.isChecked():
            # In Audio Only mode, disable video-specific features
            if hasattr(self, "sponsorblock_select_btn"):
                self.sponsorblock_select_btn.setEnabled(False)
                self.sponsorblock_select_btn.setToolTip(_("main_ui.audio_mode_disabled"))
            if hasattr(self, "selected_sponsorblock_categories"):
                self.selected_sponsorblock_categories = []  # Clear selection when disabled
            if hasattr(self, "_update_sponsorblock_display"):
                self._update_sponsorblock_display()
            self.merge_subs_checkbox.setEnabled(False)
            self.merge_subs_checkbox.setChecked(False)  # Uncheck when disabled
            if not can_enable:
                self.merge_subs_checkbox.setToolTip(_("main_ui.analyze_first_tooltip"))
            else:
                self.merge_subs_checkbox.setToolTip(_("main_ui.audio_mode_disabled"))

            # Allow subtitle selection in Audio Only mode if analysis is complete
            if hasattr(self, "subtitle_select_btn"):
                self.subtitle_select_btn.setEnabled(can_enable)
                if not can_enable:
                    self.subtitle_select_btn.setToolTip(_("main_ui.analyze_first_tooltip"))
                else:
                    self.subtitle_select_btn.setToolTip("")
        else:
            # In Video mode, enable video-specific features (if analysis complete)
            if hasattr(self, "sponsorblock_select_btn"):
                self.sponsorblock_select_btn.setEnabled(can_enable)
                if not can_enable:
                    self.sponsorblock_select_btn.setToolTip(_("main_ui.analyze_first_tooltip"))
                else:
                    self.sponsorblock_select_btn.setToolTip("")
            # Don't automatically restore categories - let user choose when they open the dialog

            # Enable merge_subs only if subtitles are selected and analysis is complete
            has_subs_selected = len(getattr(self, "selected_subtitles", [])) > 0
            should_enable_merge = can_enable and has_subs_selected
            self.merge_subs_checkbox.setEnabled(should_enable_merge)
            if not can_enable:
                self.merge_subs_checkbox.setToolTip(_("main_ui.analyze_first_tooltip"))
            elif not has_subs_selected:
                self.merge_subs_checkbox.setToolTip(_("main_ui.select_subtitles_first"))
            else:
                self.merge_subs_checkbox.setToolTip("")

            # Re-enable subtitle selection button in Video mode (if analysis complete)
            if hasattr(self, "subtitle_select_btn"):
                self.subtitle_select_btn.setEnabled(can_enable)
                if not can_enable:
                    self.subtitle_select_btn.setToolTip(_("main_ui.analyze_first_tooltip"))
                else:
                    self.subtitle_select_btn.setToolTip("")

    # Keep these methods for backwards compatibility - they just call the new dialog now
    def show_custom_command(self) -> None:
        dialog = CustomOptionsDialog(self)
        dialog.tab_widget.setCurrentIndex(1)  # Select the Custom Command tab
        self.run_dialog_with_blur(dialog)

    def show_cookie_login_dialog(self) -> None:
        dialog = CustomOptionsDialog(self)
        dialog.tab_widget.setCurrentIndex(0)  # Select the Cookie Login tab
        if self.run_dialog_with_blur(dialog):
            # Handle cookies
            cookie_path = dialog.get_cookie_file_path()
            browser_cookies = dialog.get_browser_cookies_option()

            if cookie_path:
                self.cookie_file_path = cookie_path
                self.browser_cookies_option = None  # Clear browser cookies if file is used
                logger.info(f"Selected cookie file: {self.cookie_file_path}")
                QMessageBox.information(
                    self,
                    _("main_ui.cookie_file_selected_title"),
                    _("main_ui.cookie_file_selected_message", path=self.cookie_file_path),
                )
            elif browser_cookies:
                self.browser_cookies_option = browser_cookies
                self.cookie_file_path = None  # Clear file cookies if browser is used
                logger.info(f"Selected browser cookies: {self.browser_cookies_option}")
                QMessageBox.information(
                    self,
                    _("main_ui.browser_cookies_selected_title"),
                    _("main_ui.browser_cookies_selected_message", browser=browser_cookies),
                )
            else:
                self.cookie_file_path = None  # Clear path if dialog accepted but no file selected
                self.browser_cookies_option = None  # Clear browser cookies too

    def cancel_download(self) -> None:
        if self.current_download:
            self.current_download.cancelled = True
            self.set_status_message_animated(_("status.cancelling"))  # Set status directly
            self.download_details_label.setText("")  # Clear details label on cancellation

    def show_ffmpeg_dialog(self) -> None:
        dialog = FFmpegCheckDialog(self)
        self.run_dialog_with_blur(dialog)

    # Add method for showing time range dialog
    def show_time_range_dialog(self) -> None:
        dialog = TimeRangeDialog(self)
        if self.run_dialog_with_blur(dialog):
            # Store the time range settings
            self.download_section = dialog.get_download_sections()
            self.force_keyframes = dialog.get_force_keyframes()

            if self.download_section:
                self.time_range_btn.setStyleSheet(StyleSheet.TIME_RANGE_BTN_ACTIVE)
                self.time_range_btn.setToolTip(_("main_ui.time_range_set", section=self.download_section))
            else:
                # Reset to default style if no section is selected
                self.download_section = None
                self.force_keyframes = False
                self.time_range_btn.setStyleSheet("")
                self.time_range_btn.setToolTip("")

    def show_ytdlp_setup_dialog(self) -> None:
        """Show the yt-dlp setup dialog to configure yt-dlp"""
        yt_dlp_path = setup_ytdlp(self)
        if yt_dlp_path != "yt-dlp":
            success_dialog = QMessageBox(self)
            success_dialog.setIcon(QMessageBox.Icon.Information)
            success_dialog.setWindowTitle(_("ytdlp_setup.success_dialog_title"))
            success_dialog.setText(_("ytdlp_setup.success_dialog_message", path=yt_dlp_path))
            success_dialog.setWindowIcon(self.windowIcon())
            success_dialog.setStyleSheet(StyleSheet.SETUP_SUCCESS_DIALOG)
            self.run_dialog_with_blur(success_dialog)

    def show_deno_setup_dialog(self) -> None:
        """Show the Deno setup dialog to configure Deno"""
        deno_path = setup_deno(self)
        if deno_path != "deno":
            success_dialog = QMessageBox(self)
            success_dialog.setIcon(QMessageBox.Icon.Information)
            success_dialog.setWindowTitle(_("deno.setup_required"))
            success_dialog.setText(f"{_('deno.success')}\n{deno_path}")
            success_dialog.setWindowIcon(self.windowIcon())
            success_dialog.setStyleSheet(StyleSheet.SETUP_SUCCESS_DIALOG)
            self.run_dialog_with_blur(success_dialog)

    def animate_widget_fade_in(self, widget: QWidget, duration: int = 300) -> None:
        """Fade in a widget using opacity animation."""
        # Check if the main window has a graphics effect (blur) active.
        # If so, animating a child widget with another effect causes QPainter conflicts.
        # NOTE: With the new Screenshot Overlay method, 'self.graphicsEffect()' on the MainWindow isn't used.
        # However, we should still be careful if the widget itself already has an effect.
        
        # Stop fade out if running
        if hasattr(widget, '_fade_out_anim'):
             try:
                 if widget._fade_out_anim.state() == QPropertyAnimation.State.Running:
                     widget._fade_out_anim.stop()
             except RuntimeError:
                 pass
        
        if widget.isVisible() and widget.graphicsEffect() is None:
            return

        # Setup opacity effect if not present
        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        
        # Determine start value (current opacity if previously animating)
        start_val = effect.opacity() if widget.isVisible() else 0.0
        end_val = 1.0
        
        # Setup animation
        anim = QPropertyAnimation(effect, b"opacity", widget)
        anim.setDuration(duration)
        anim.setStartValue(start_val)
        anim.setEndValue(end_val)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # Show widget before animation
        widget.setVisible(True)
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        
        # Keep reference to avoid garbage collection
        widget._fade_anim = anim

    def animate_widget_fade_out(self, widget: QWidget, duration: int = 300) -> None:
        """Fade out a widget and then hide it."""
        
        # Stop fade in if running
        if hasattr(widget, '_fade_anim'):
             try:
                 if widget._fade_anim.state() == QPropertyAnimation.State.Running:
                     widget._fade_anim.stop()
             except RuntimeError:
                 pass

        if not widget.isVisible():
            return

        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
            effect.setOpacity(1.0)
        
        start_val = effect.opacity()
        
        anim = QPropertyAnimation(effect, b"opacity", widget)
        anim.setDuration(duration)
        anim.setStartValue(start_val)
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.Type.InQuad)
        
        def on_finished():
            widget.setVisible(False)
            widget.setGraphicsEffect(None) # Remove effect to restore normal painting
            
        anim.finished.connect(on_finished)
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        
        widget._fade_out_anim = anim # Keep reference

    def set_widget_visible_animated(self, widget: QWidget, visible: bool) -> None:
        """Toggle widget visibility with fade animation."""
        if visible:
            self.animate_widget_fade_in(widget)
        else:
            self.animate_widget_fade_out(widget)

    def animate_widget_shake(self, widget: QWidget) -> None:
        """Shake a widget left and right to indicate an error or invalid input."""
        # Stop shake if running
        if hasattr(widget, '_shake_anim'):
             try:
                 if widget._shake_anim.state() == QPropertyAnimation.State.Running:
                     return
             except RuntimeError:
                 pass

        # Use current position as baseline
        pos = widget.pos()
        x = pos.x()
        y = pos.y()
        
        anim = QPropertyAnimation(widget, b"pos", widget)
        anim.setDuration(300)
        anim.setLoopCount(1)
        
        # Create keyframes for shake effect
        anim.setKeyValueAt(0, QPoint(x, y))
        anim.setKeyValueAt(0.2, QPoint(x - 5, y))
        anim.setKeyValueAt(0.4, QPoint(x + 5, y))
        anim.setKeyValueAt(0.6, QPoint(x - 5, y))
        anim.setKeyValueAt(0.8, QPoint(x + 5, y))
        anim.setKeyValueAt(1.0, QPoint(x, y))
        
        widget._shake_anim = anim
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)


    def set_status_message_animated(self, message: str) -> None:
        """Update status label with a cross-fade animation."""
        if self.status_label.text() == message:
             return

        # If previous animation is running, stop it
        if hasattr(self.status_label, '_status_anim'):
            try:
                if self.status_label._status_anim.state() == QPropertyAnimation.State.Running:
                    self.status_label._status_anim.stop()
            except RuntimeError:
                pass  # Animation object already deleted

        # Create effect if needed
        effect = self.status_label.graphicsEffect()
        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(self.status_label)
            self.status_label.setGraphicsEffect(effect)
        
        # 1. Fade OUT
        anim1 = QPropertyAnimation(effect, b"opacity", self.status_label)
        anim1.setDuration(150)
        anim1.setStartValue(1.0)
        anim1.setEndValue(0.0)
        anim1.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # 2. Change Text & Fade IN
        anim2 = QPropertyAnimation(effect, b"opacity", self.status_label)
        anim2.setDuration(150)
        anim2.setStartValue(0.0)
        anim2.setEndValue(1.0)
        anim2.setEasingCurve(QEasingCurve.Type.InQuad)
        
        def on_fade_out_finished():
            self.status_label.setText(message)
            anim2.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
            
        anim1.finished.connect(on_fade_out_finished)
        anim1.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        
        # Store ref
        self.status_label._status_anim = anim1 
        self.status_label._status_anim2 = anim2

    def run_dialog_with_blur(self, dialog: QDialog) -> int:
        """Run a dialog with a static background screenshot blur to avoid QPainter conflicts."""
        
        # 1. Capture the current state of the window (screenshot)
        pixmap = self.grab()
        
        # 2. Create the blur using a Graphics Scene method (much safer than QGraphicsBlurEffect on live widget)
        # However, for simplicity and performance with PySide6, we can just apply a blur to the image
        # or use a simplified overlay.
        # Let's manually blur the pixmap or use a simpler transparent overlay if blur is too heavy manually.
        # Actually, using QGraphicsBlurEffect on a temporary QGraphicsScene rendering to a pixmap is a valid way
        # to generate a single blurred frame.
        
        blurred_pixmap = self._apply_blur_to_pixmap(pixmap, radius=10)
        
        # 3. Create an overlay widget that covers the Main Window
        overlay = QLabel(self)
        overlay.setPixmap(blurred_pixmap)
        overlay.setGeometry(0, 0, self.width(), self.height())
        overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False) # Block mouse
        overlay.show()
        
        # Animate overlay Fade In
        opacity_effect = QGraphicsOpacityEffect(overlay)
        overlay.setGraphicsEffect(opacity_effect)
        
        anim = QPropertyAnimation(opacity_effect, b"opacity", overlay)
        anim.setDuration(250)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        
        # 4. Run the dialog
        # Ensure dialog is on top
        result = dialog.exec()
        
        # 5. Remove overlay
        overlay.deleteLater()
        
        return result

    def _apply_blur_to_pixmap(self, source_pixmap: QPixmap, radius: int) -> QPixmap:
        """Helper to create a blurred version of a pixmap."""
        if source_pixmap.isNull():
             return source_pixmap
             
        # Create a QGraphicsScene to apply the effect to the pixmap
        scene = QGraphicsScene()
        item = QGraphicsPixmapItem(source_pixmap)
        scene.addItem(item)
        
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(radius)
        item.setGraphicsEffect(blur)
        
        # Render back to pixmap
        result = source_pixmap.copy() # Match size/format
        result.fill(Qt.GlobalColor.transparent)
        
        with QPainter(result) as painter:
            scene.render(painter, target=source_pixmap.rect().toRectF(), source=source_pixmap.rect().toRectF())
            
            # Optional: Add a dark tint for 'dimming' effect
            painter.setBrush(QBrush(QColor(0, 0, 0, 100))) # 100/255 opacity black
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(source_pixmap.rect())

        return result


