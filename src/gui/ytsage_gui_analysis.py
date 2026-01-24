from typing import TYPE_CHECKING, cast

import json
import threading
import subprocess
from PySide6.QtCore import QMetaObject, Qt, Q_ARG
from PySide6.QtWidgets import QMessageBox

from src.core.ytsage_utils import validate_video_url, parse_yt_dlp_error
from src.core.ytsage_yt_dlp import get_yt_dlp_path
from src.utils.ytsage_constants import SUBPROCESS_CREATIONFLAGS
from src.utils.ytsage_localization import _
from src.utils.ytsage_logger import logger

if TYPE_CHECKING:
    from src.gui.ytsage_gui_main import YTSageApp

class AnalysisMixin:
    def analyze_url(self) -> None:
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

        # Reset analysis state and disable controls
        self.analysis_completed = False
        self.toggle_analysis_dependent_controls(enabled=False)

        self.signals.update_status.emit(_("main_ui.analyzing_preparing"))
        self.is_analyzing = True
        threading.Thread(target=self._analyze_url_thread, args=(url,), daemon=True).start()

    def _analyze_url_thread(self, url) -> None:
        self = cast("YTSageApp", self)
        try:
            self.signals.update_status.emit(_("main_ui.analyzing_extracting_basic"))

            # Clean up the URL to handle both playlist and video URLs
            if "list=" in url and "watch?v=" in url:
                playlist_id = url.split("list=")[1].split("&")[0]
                url = f"https://www.youtube.com/playlist?list={playlist_id}"

            # Always use subprocess to call yt-dlp binary (Python package removed)
            self._analyze_url_with_subprocess(url)

        except Exception as e:
            logger.exception(f"Error in analysis: {e}")
            self.signals.update_status.emit(_("errors.generic_error", error=str(e)))
            # Ensure playlist UI is hidden on error too
            self.signals.playlist_info_label_visible.emit(False)
            self.signals.playlist_select_btn_visible.emit(False)
        finally:
            self.is_analyzing = False


    def _analyze_url_with_subprocess(self, url) -> None:
        """Analyze URL using yt-dlp executable when Python module is not available"""
        self = cast("YTSageApp", self)

        try:
            yt_dlp_path = get_yt_dlp_path()
            if not yt_dlp_path:
                logger.error("yt-dlp executable not found. Please install yt-dlp first.")
                self.signals.update_status.emit(_("errors.ytdlp_not_found"))
                self.signals.playlist_info_label_visible.emit(False)
                self.signals.playlist_select_btn_visible.emit(False)
                return

            self.signals.update_status.emit(_("main_ui.analyzing_extracting_ytdlp"))

            # Clean up the URL to handle both playlist and video URLs
            if "list=" in url and "watch?v=" in url:
                playlist_id = url.split("list=")[1].split("&")[0]
                url = f"https://www.youtube.com/playlist?list={playlist_id}"

            # Build command for basic info extraction
            # Use --flat-playlist for fast initial extraction of playlist info + --dump-single-json
            # This fetches minimal info for all videos quickly without downloading full details for each
            cmd = [yt_dlp_path, "--dump-single-json", "--flat-playlist", "--no-warnings", url]

            # Add cookies if available
            if self.cookie_file_path:
                cmd.extend(["--cookies", str(self.cookie_file_path)])
            elif self.browser_cookies_option:
                cmd.extend(["--cookies-from-browser", self.browser_cookies_option])

            # Add proxy settings if available
            if self.proxy_url:
                cmd.extend(["--proxy", self.proxy_url])
            
            if self.geo_proxy_url:
                cmd.extend(["--geo-verification-proxy", self.geo_proxy_url])

            logger.debug(f"Executing yt-dlp command: {cmd}")

            # Execute command with hidden console window on Windows
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, creationflags=SUBPROCESS_CREATIONFLAGS)

            if result.returncode != 0:
                logger.error(f"yt-dlp failed: {result.stderr}")
                self.signals.update_status.emit(_("errors.ytdlp_failed", error=result.stderr))
                self.signals.playlist_info_label_visible.emit(False)
                self.signals.playlist_select_btn_visible.emit(False)
                return

            json_lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

            if not json_lines:
                logger.error("No data returned from yt-dlp")
                self.signals.update_status.emit(_("errors.no_data_returned"))
                self.signals.playlist_info_label_visible.emit(False)
                self.signals.playlist_select_btn_visible.emit(False)
                return

            try:
                first_info = json.loads(json_lines[0])
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse yt-dlp output: {e}")
                self.signals.update_status.emit(_("errors.parse_failed", error=str(e)))
                self.signals.playlist_info_label_visible.emit(False)
                self.signals.playlist_select_btn_visible.emit(False)
                return

            self.signals.update_status.emit(_("main_ui.analyzing_processing_data"))

            if first_info.get("_type") == "playlist":
                # Handle playlist
                self.is_playlist = True
                self.playlist_info = first_info
                self.selected_playlist_items = None
                self.playlist_entries = first_info.get("entries", [])

                if not self.playlist_entries:
                    logger.error("Playlist contains no valid videos.")
                    self.signals.update_status.emit(_("errors.playlist_no_videos"))
                    self.signals.playlist_info_label_visible.emit(False)
                    self.signals.playlist_select_btn_visible.emit(False)
                    return

                # Even with flat-playlist, we need one video's formats to populate the table.
                # Just use the first video URL to get full details quickly.
                self.signals.update_status.emit(_("main_ui.analyzing_fetching_first_video"))
                first_video_entry = self.playlist_entries[0]
                first_video_url = first_video_entry.get("url")
                
                # Fetch full info for just the first video to get formats
                cmd_single = [yt_dlp_path, "--dump-single-json", "--no-warnings", first_video_url]
                 # Add cookies & proxy to this single request too
                if self.cookie_file_path:
                    cmd_single.extend(["--cookies", str(self.cookie_file_path)])
                elif self.browser_cookies_option:
                    cmd_single.extend(["--cookies-from-browser", self.browser_cookies_option])
                if self.proxy_url:
                    cmd_single.extend(["--proxy", self.proxy_url])
                if self.geo_proxy_url:
                    cmd_single.extend(["--geo-verification-proxy", self.geo_proxy_url])
                    
                result_single = subprocess.run(cmd_single, capture_output=True, text=True, timeout=60, creationflags=SUBPROCESS_CREATIONFLAGS)
                
                if result_single.returncode == 0:
                     self.video_info = json.loads(result_single.stdout)
                else:
                    # Fallback to whatever minimal info we have, might fail table population
                     self.video_info = first_video_entry

                # Update playlist info label
                playlist_text = _("playlist.display_format",
                                 title=first_info.get('title', _('playlist.unknown')),
                                 count=len(self.playlist_entries))

                self.signals.playlist_info_label_text.emit(playlist_text)
                self.signals.playlist_info_label_visible.emit(True)

                # Show playlist selection button
                self.signals.playlist_select_btn_text.emit(_("main_ui.select_videos_all"))
                self.signals.playlist_select_btn_visible.emit(True)

            else:
                # Handle single video
                self.is_playlist = False
                self.video_info = first_info
                self.playlist_entries = []
                self.selected_playlist_items = None

                # Hide playlist UI
                self.signals.playlist_info_label_visible.emit(False)
                self.signals.playlist_select_btn_visible.emit(False)

            # Verify we have format information
            if not self.video_info or "formats" not in self.video_info:
                logger.error("No format information available")
                self.signals.update_status.emit(_("errors.no_format_info"))
                self.signals.playlist_info_label_visible.emit(False)
                self.signals.playlist_select_btn_visible.emit(False)
                return

            self.signals.update_status.emit(_("main_ui.analyzing_processing_formats_ytdlp"))
            self.all_formats = self.video_info["formats"]

            # Update UI
            self.update_video_info(self.video_info)

            # Update thumbnail
            self.signals.update_status.emit(_("main_ui.analyzing_loading_thumbnail_ytdlp"))
            # Try to get thumbnail from playlist info first
            # Fallback to video thumbnail if playlist thumbnail not found or not a playlist
            thumbnail_url = (self.playlist_info or {}).get("thumbnail") or (self.video_info or {}).get("thumbnail")

            self.download_thumbnail(thumbnail_url)

            # Save thumbnail if enabled
            if self.save_thumbnail:
                self.download_thumbnail_file(self.video_url, self.last_path)

            # Handle subtitles
            self.signals.update_status.emit(_("main_ui.analyzing_processing_subtitles_ytdlp"))
            self.selected_subtitles = []
            self.available_subtitles = self.video_info.get("subtitles", {})
            self.available_automatic_subtitles = self.video_info.get("automatic_captions", {})

            # Update subtitle UI
            self.signals.selected_subs_label_text.emit(_("main_ui.zero_selected"))

            # Update format table
            self.signals.update_status.emit(_("main_ui.analyzing_updating_table"))
            self.video_button.setChecked(True)
            self.audio_button.setChecked(False)
            self.filter_formats()

            self.signals.update_status.emit(_("main_ui.analysis_complete"))

            # Mark analysis as complete and enable analysis-dependent controls
            self.analysis_completed = True
            QMetaObject.invokeMethod(
                self,
                "toggle_analysis_dependent_controls",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(bool, True),
            )

        except subprocess.TimeoutExpired:
             logger.error("Analysis timed out")
             self.signals.update_status.emit(_("errors.timeout"))
        except Exception as e:
            logger.exception(f"Unexpected error in analysis: {e}")
            self.signals.update_status.emit(_("errors.generic_error", error=str(e)))
