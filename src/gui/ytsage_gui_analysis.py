from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast

import json
import subprocess
from PySide6.QtCore import QMetaObject, Qt, Q_ARG, QThread, Signal
from PySide6.QtWidgets import QMessageBox

from src.core.ytsage_utils import validate_video_url, parse_yt_dlp_error
from src.core.ytsage_yt_dlp import get_yt_dlp_path
from src.utils.ytsage_constants import SUBPROCESS_CREATIONFLAGS
from src.utils.ytsage_localization import _
from src.utils.ytsage_logger import logger

if TYPE_CHECKING:
    from src.gui.ytsage_gui_main import YTSageApp


class AnalysisThread(QThread):
    """
    Thread-safe QThread for URL analysis.
    All results are passed back via signals to ensure thread safety.
    """
    # Signals for status updates
    status_update = Signal(str)
    
    # Signals for playlist UI
    playlist_info_visible = Signal(bool)
    playlist_info_text = Signal(str)
    playlist_select_btn_visible = Signal(bool)
    playlist_select_btn_text = Signal(str)
    
    # Signal for analysis results - passes all data at once
    analysis_complete = Signal(dict)
    
    # Signal for errors
    analysis_error = Signal(str)
    
    # Signal when thread finishes (success or failure)
    analysis_finished = Signal()

    def __init__(
        self,
        url: str,
        cookie_file_path: Optional[str] = None,
        browser_cookies_option: Optional[str] = None,
        proxy_url: Optional[str] = None,
        geo_proxy_url: Optional[str] = None,
        parent=None
    ) -> None:
        super().__init__(parent)
        self.url = url
        self.cookie_file_path = cookie_file_path
        self.browser_cookies_option = browser_cookies_option
        self.proxy_url = proxy_url
        self.geo_proxy_url = geo_proxy_url
        self._cancelled = False

    def cancel(self) -> None:
        """Request cancellation of the analysis."""
        self._cancelled = True

    def run(self) -> None:
        """Main thread execution - performs URL analysis."""
        try:
            self.status_update.emit(_("main_ui.analyzing_extracting_basic"))
            
            url = self.url
            # Clean up the URL to handle both playlist and video URLs
            if "list=" in url and "watch?v=" in url:
                playlist_id = url.split("list=")[1].split("&")[0]
                url = f"https://www.youtube.com/playlist?list={playlist_id}"

            self._analyze_url_with_subprocess(url)

        except Exception as e:
            logger.exception(f"Error in analysis: {e}")
            self.analysis_error.emit(_("errors.generic_error", error=str(e)))
            self.playlist_info_visible.emit(False)
            self.playlist_select_btn_visible.emit(False)
        finally:
            self.analysis_finished.emit()

    def _add_auth_options(self, cmd: List[str]) -> None:
        """Add authentication and proxy options to command."""
        if self.cookie_file_path:
            cmd.extend(["--cookies", str(self.cookie_file_path)])
        elif self.browser_cookies_option:
            cmd.extend(["--cookies-from-browser", self.browser_cookies_option])
        
        if self.proxy_url:
            cmd.extend(["--proxy", self.proxy_url])
        
        if self.geo_proxy_url:
            cmd.extend(["--geo-verification-proxy", self.geo_proxy_url])

    def _analyze_url_with_subprocess(self, url: str) -> None:
        """Analyze URL using yt-dlp executable."""
        if self._cancelled:
            return

        yt_dlp_path = get_yt_dlp_path()
        if not yt_dlp_path:
            logger.error("yt-dlp executable not found. Please install yt-dlp first.")
            self.analysis_error.emit(_("errors.ytdlp_not_found"))
            self.playlist_info_visible.emit(False)
            self.playlist_select_btn_visible.emit(False)
            return

        self.status_update.emit(_("main_ui.analyzing_extracting_ytdlp"))

        # Build command for basic info extraction
        cmd = [yt_dlp_path, "--dump-single-json", "--flat-playlist", "--no-warnings", url]
        self._add_auth_options(cmd)

        logger.debug(f"Executing yt-dlp command: {cmd}")

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300,
                creationflags=SUBPROCESS_CREATIONFLAGS
            )
        except subprocess.TimeoutExpired:
            logger.error("Analysis timed out")
            self.analysis_error.emit(_("errors.timeout"))
            return

        if self._cancelled:
            return

        if result.returncode != 0:
            logger.error(f"yt-dlp failed: {result.stderr}")
            self.analysis_error.emit(_("errors.ytdlp_failed", error=result.stderr))
            self.playlist_info_visible.emit(False)
            self.playlist_select_btn_visible.emit(False)
            return

        json_lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

        if not json_lines:
            logger.error("No data returned from yt-dlp")
            self.analysis_error.emit(_("errors.no_data_returned"))
            self.playlist_info_visible.emit(False)
            self.playlist_select_btn_visible.emit(False)
            return

        try:
            first_info = json.loads(json_lines[0])
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse yt-dlp output: {e}")
            self.analysis_error.emit(_("errors.parse_failed", error=str(e)))
            self.playlist_info_visible.emit(False)
            self.playlist_select_btn_visible.emit(False)
            return

        if self._cancelled:
            return

        self.status_update.emit(_("main_ui.analyzing_processing_data"))

        # Prepare result data
        result_data: Dict[str, Any] = {
            "is_playlist": False,
            "playlist_info": None,
            "playlist_entries": [],
            "video_info": None,
            "all_formats": [],
            "available_subtitles": {},
            "available_automatic_subtitles": {},
            "thumbnail_url": None,
        }

        if first_info.get("_type") == "playlist":
            result_data["is_playlist"] = True
            result_data["playlist_info"] = first_info
            playlist_entries = first_info.get("entries", [])
            result_data["playlist_entries"] = playlist_entries

            if not playlist_entries:
                logger.error("Playlist contains no valid videos.")
                self.analysis_error.emit(_("errors.playlist_no_videos"))
                self.playlist_info_visible.emit(False)
                self.playlist_select_btn_visible.emit(False)
                return

            # Fetch full info for the first video to get formats
            self.status_update.emit(_("main_ui.analyzing_fetching_first_video"))
            first_video_entry = playlist_entries[0]
            first_video_url = first_video_entry.get("url")

            cmd_single = [yt_dlp_path, "--dump-single-json", "--no-warnings", first_video_url]
            self._add_auth_options(cmd_single)

            try:
                result_single = subprocess.run(
                    cmd_single, capture_output=True, text=True, timeout=60,
                    creationflags=SUBPROCESS_CREATIONFLAGS
                )
                if result_single.returncode == 0:
                    result_data["video_info"] = json.loads(result_single.stdout)
                else:
                    result_data["video_info"] = first_video_entry
            except subprocess.TimeoutExpired:
                result_data["video_info"] = first_video_entry

            if self._cancelled:
                return

            # Update playlist UI via signals
            playlist_text = _("playlist.display_format",
                             title=first_info.get('title', _('playlist.unknown')),
                             count=len(playlist_entries))
            self.playlist_info_text.emit(playlist_text)
            self.playlist_info_visible.emit(True)
            self.playlist_select_btn_text.emit(_("main_ui.select_videos_all"))
            self.playlist_select_btn_visible.emit(True)

        else:
            # Handle single video
            result_data["is_playlist"] = False
            result_data["video_info"] = first_info
            result_data["playlist_entries"] = []
            result_data["playlist_info"] = None

            # Hide playlist UI
            self.playlist_info_visible.emit(False)
            self.playlist_select_btn_visible.emit(False)

        # Verify we have format information
        video_info = result_data["video_info"]
        if not video_info or "formats" not in video_info:
            logger.error("No format information available")
            self.analysis_error.emit(_("errors.no_format_info"))
            self.playlist_info_visible.emit(False)
            self.playlist_select_btn_visible.emit(False)
            return

        self.status_update.emit(_("main_ui.analyzing_processing_formats_ytdlp"))
        result_data["all_formats"] = video_info.get("formats", [])

        # Get thumbnail URL
        self.status_update.emit(_("main_ui.analyzing_loading_thumbnail_ytdlp"))
        playlist_info = result_data.get("playlist_info") or {}
        thumbnail_url = playlist_info.get("thumbnail") or video_info.get("thumbnail")
        result_data["thumbnail_url"] = thumbnail_url

        # Handle subtitles
        self.status_update.emit(_("main_ui.analyzing_processing_subtitles_ytdlp"))
        result_data["available_subtitles"] = video_info.get("subtitles", {})
        result_data["available_automatic_subtitles"] = video_info.get("automatic_captions", {})

        self.status_update.emit(_("main_ui.analyzing_updating_table"))

        # Emit all results at once
        self.analysis_complete.emit(result_data)


class AnalysisMixin:
    """Mixin class providing URL analysis functionality for YTSageApp."""
    
    # Track the current analysis thread
    _analysis_thread: Optional[AnalysisThread] = None

    def analyze_url(self) -> None:
        """Start URL analysis in a background thread."""
        self = cast("YTSageApp", self)
        
        if self.is_updating_ytdlp:
            QMessageBox.warning(self, _("update.update_in_progress_title"), _("update.update_in_progress_message"))
            return

        url = self.url_input.text().strip()
        if not url:
            self.signals.update_status.emit(_("main_ui.invalid_url_or_enter"))
            return
        
        # Validate URL before processing
        is_valid, error_message = validate_video_url(url)
        if not is_valid:
            QMessageBox.warning(self, _("main_ui.error_title"), error_message)
            return

        # Cancel any existing analysis thread
        if self._analysis_thread is not None and self._analysis_thread.isRunning():
            self._analysis_thread.cancel()
            self._analysis_thread.wait(1000)  # Wait up to 1 second

        # Reset analysis state and disable controls
        self.analysis_completed = False
        self.toggle_analysis_dependent_controls(enabled=False)

        self.signals.update_status.emit(_("main_ui.analyzing_preparing"))
        self.is_analyzing = True

        # Create and configure the analysis thread
        self._analysis_thread = AnalysisThread(
            url=url,
            cookie_file_path=self.cookie_file_path,
            browser_cookies_option=self.browser_cookies_option,
            proxy_url=self.proxy_url,
            geo_proxy_url=self.geo_proxy_url,
            parent=self
        )

        # Connect signals to handlers
        self._analysis_thread.status_update.connect(self.signals.update_status.emit)
        self._analysis_thread.playlist_info_visible.connect(self.signals.playlist_info_label_visible.emit)
        self._analysis_thread.playlist_info_text.connect(self.signals.playlist_info_label_text.emit)
        self._analysis_thread.playlist_select_btn_visible.connect(self.signals.playlist_select_btn_visible.emit)
        self._analysis_thread.playlist_select_btn_text.connect(self.signals.playlist_select_btn_text.emit)
        self._analysis_thread.analysis_complete.connect(self._on_analysis_complete)
        self._analysis_thread.analysis_error.connect(self._on_analysis_error)
        self._analysis_thread.analysis_finished.connect(self._on_analysis_finished)

        # Start the thread
        self._analysis_thread.start()

    def _on_analysis_complete(self, result_data: Dict[str, Any]) -> None:
        """Handle successful analysis completion - runs in main thread."""
        self = cast("YTSageApp", self)
        
        # Update instance variables with results (safe - we're in main thread)
        self.is_playlist = result_data["is_playlist"]
        self.playlist_info = result_data["playlist_info"]
        self.playlist_entries = result_data["playlist_entries"]
        self.video_info = result_data["video_info"]
        self.all_formats = result_data["all_formats"]
        self.available_subtitles = result_data["available_subtitles"]
        self.available_automatic_subtitles = result_data["available_automatic_subtitles"]
        self.selected_playlist_items = None
        self.selected_subtitles = []

        # Update UI components (safe - we're in main thread)
        self.update_video_info(self.video_info)

        # Download thumbnail
        thumbnail_url = result_data.get("thumbnail_url")
        if thumbnail_url:
            self.download_thumbnail(thumbnail_url)

        # Save thumbnail if enabled
        if self.save_thumbnail:
            self.download_thumbnail_file(self.video_url, self.last_path)

        # Update subtitle UI
        self.signals.selected_subs_label_text.emit(_("main_ui.zero_selected"))

        # Update format table
        self.video_button.setChecked(True)
        self.audio_button.setChecked(False)
        self.filter_formats()

        self.signals.update_status.emit(_("main_ui.analysis_complete"))

        # Mark analysis as complete and enable controls
        self.analysis_completed = True
        self.toggle_analysis_dependent_controls(enabled=True)

    def _on_analysis_error(self, error_message: str) -> None:
        """Handle analysis error - runs in main thread."""
        self = cast("YTSageApp", self)
        self.signals.update_status.emit(error_message)

    def _on_analysis_finished(self) -> None:
        """Handle analysis thread completion - runs in main thread."""
        self = cast("YTSageApp", self)
        self.is_analyzing = False
