import re
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, cast

import requests
from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from src.gui.ytsage_gui_dialogs import (  # use of src\gui\ytsage_gui_dialogs\__init__.py
    SponsorBlockCategoryDialog,
    SubtitleSelectionDialog,
)
from src.utils.ytsage_localization import _
from src.utils.ytsage_logger import logger

if TYPE_CHECKING:
    from src.gui.ytsage_gui_main import YTSageApp


class VideoInfoMixin:
    def setup_video_info_section(self) -> QHBoxLayout:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

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
        self.title_label.setStyleSheet("font-size: 12px; font-weight: bold;")

        # Add basic info labels
        self.channel_label = QLabel()
        self.views_label = QLabel()
        self.date_label = QLabel()
        self.duration_label = QLabel()
        self.like_count_label = QLabel()

        # Style the info labels
        for label in [
            self.channel_label,
            self.views_label,
            self.date_label,
            self.duration_label,
            self.like_count_label,
        ]:
            label.setStyleSheet(
                """
                QLabel {
                    color: #999999;
                    font-size: 11px;
                    padding: 0px;
                }
            """
            )

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
        self.subtitle_select_btn = QPushButton(_("main_ui.select_subtitles"))  # Renamed & changed text
        self.subtitle_select_btn.setFixedHeight(30)
        # self.subtitle_select_btn.setFixedWidth(150) # Let it size naturally or adjust as needed
        self.subtitle_select_btn.clicked.connect(self.open_subtitle_dialog)
        self.subtitle_select_btn.setStyleSheet(
            """
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
        """
        )
        self.subtitle_select_btn.setProperty("subtitlesSelected", False)  # Custom property for styling
        subtitle_layout.addWidget(self.subtitle_select_btn)

        # Label to show number of selected subtitles
        self.selected_subs_label = QLabel(_("selection.none_selected"))
        self.selected_subs_label.setStyleSheet("color: #cccccc; padding-left: 5px;")
        subtitle_layout.addWidget(self.selected_subs_label)

        # Add the subtitle layout to the main video info layout
        video_info_layout.addLayout(subtitle_layout)
        # --- End Subtitle Section ---

        # Add small spacing between subtitle and sponsorblock sections
        video_info_layout.addSpacing(4)

        # --- SponsorBlock Section ---
        sponsorblock_layout = QHBoxLayout()

        self.sponsorblock_select_btn = QPushButton(_("main_ui.sponsorblock_categories"))
        self.sponsorblock_select_btn.setFixedHeight(30)
        self.sponsorblock_select_btn.clicked.connect(self.open_sponsorblock_dialog)
        self.sponsorblock_select_btn.setStyleSheet(
            """
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
        """
        )
        self.sponsorblock_select_btn.setProperty("sponsorBlockSelected", False)
        self.sponsorblock_select_btn.setProperty("sponsorBlockSelected", False)
        sponsorblock_layout.addWidget(self.sponsorblock_select_btn)

        # Label to show selection count
        self.selected_sponsorblock_label = QLabel(_("selection.none_selected"))
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

    def setup_playlist_info_section(self) -> QLabel:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        self.playlist_info_label = QLabel()
        self.playlist_info_label.setVisible(False)
        self.playlist_info_label.setStyleSheet(
            """
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
        """
        )
        self.playlist_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return self.playlist_info_label

    def update_video_info(self, info) -> None:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        if hasattr(self, "is_playlist") and self.is_playlist:
            # Playlist Mode: Show playlist title and video count
            self.title_label.setText(self.playlist_info.get("title", _("playlist.unknown")))

            num_videos = len(getattr(self, "playlist_entries", []))
            self.duration_label.setText(_("playlist.total_videos", count=num_videos))

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
            views = info.get("view_count")
            formatted_views = f"{views:,}" if views is not None else "N/A"

            # Format like count with commas
            likes = info.get("like_count")
            formatted_likes = f"{likes:,}" if likes is not None else "N/A"

            # Format upload date
            upload_date = info.get("upload_date", "")
            if upload_date:
                date_obj = datetime.strptime(upload_date, "%Y%m%d")
                formatted_date = date_obj.strftime("%B %d, %Y")
            else:
                formatted_date = _("video_info.unknown_date")

            # Format duration
            duration = info.get("duration", 0)
            minutes = duration // 60
            seconds = duration % 60
            duration_str = f"{minutes}:{seconds:02d}"

            # Update labels with localized text
            self.title_label.setText(info.get("title", _("video_info.unknown_title")))
            self.channel_label.setText(f"{_("video_info.channel")}: {info.get('uploader', _("video_info.unknown_channel"))}")
            self.views_label.setText(f"{_("video_info.views")}: {formatted_views}")
            self.like_count_label.setText(f"{_("video_info.likes")}: {formatted_likes}")
            self.date_label.setText(f"{_("video_info.upload_date")}: {formatted_date}")
            self.duration_label.setText(f"{_("video_info.duration")}: {duration_str}")

    def open_subtitle_dialog(self) -> None:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        if not hasattr(self, "available_subtitles") or not hasattr(self, "available_automatic_subtitles"):
            logger.warning("Subtitle info not loaded yet.")
            return

        if not hasattr(self, "selected_subtitles"):
            self.selected_subtitles = []

        dialog = SubtitleSelectionDialog(
            self.available_subtitles,  # type: ignore[reportAttributeAccessIssue]
            self.available_automatic_subtitles,  # type: ignore[reportAttributeAccessIssue]
            self.selected_subtitles,
            self,  # Parent for the dialog
        )

        # removed extra logic for mapping to main_windows
        merge_checkbox = getattr(self, "merge_subs_checkbox", None)

        if dialog.exec():  # If user clicks OK
            self.selected_subtitles = dialog.get_selected_subtitles()
            logger.info(f"Selected subtitles: {self.selected_subtitles}")
            # Update UI to reflect selection
            count = len(self.selected_subtitles)
            self.selected_subs_label.setText(_("subtitle_selection.count_selected", count=count))
            self.subtitle_select_btn.setProperty("subtitlesSelected", count > 0)

            # Enable/disable the merge checkbox in the parent window
            if merge_checkbox:
                # Only enable merge checkbox if we're not in Audio Only mode and analysis is complete
                is_audio_only = hasattr(self, "audio_button") and self.audio_button.isChecked()
                has_analysis = getattr(self, "analysis_completed", False)
                # In audio-only mode, we still allow subtitle selection but not merging
                should_enable = count > 0 and not is_audio_only and has_analysis
                merge_checkbox.setEnabled(should_enable)
                # Update tooltip
                if not has_analysis:
                    merge_checkbox.setToolTip(_("main_ui.analyze_first_tooltip"))
                elif is_audio_only:
                    merge_checkbox.setToolTip(_("main_ui.audio_mode_disabled"))
                elif count == 0:
                    merge_checkbox.setToolTip(_("main_ui.select_subtitles_first"))
                else:
                    merge_checkbox.setToolTip("")
            else:
                logger.warning("merge_subs_checkbox not found on parent window.")

            # Re-apply stylesheet to update button border if property changed
            self.subtitle_select_btn.style().unpolish(self.subtitle_select_btn)
            self.subtitle_select_btn.style().polish(self.subtitle_select_btn)
        # No else needed for cancel, state remains unchanged

    def open_sponsorblock_dialog(self) -> None:
        """Open the SponsorBlock category selection dialog."""
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        # Initialize selected categories if not exists or empty (first time opening)
        if not hasattr(self, "selected_sponsorblock_categories") or not self.selected_sponsorblock_categories:
            # Use None to let the dialog set its own defaults
            dialog_categories = None
        else:
            dialog_categories = self.selected_sponsorblock_categories

        dialog = SponsorBlockCategoryDialog(dialog_categories, self)

        if dialog.exec():
            self.selected_sponsorblock_categories = dialog.get_selected_categories()
            logger.info(f"SponsorBlock categories selected: {self.selected_sponsorblock_categories}")
            self._update_sponsorblock_display()

    def _update_sponsorblock_display(self) -> None:
        """Update the SponsorBlock button and label to reflect current selection."""
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

        if not hasattr(self, "selected_sponsorblock_categories"):
            self.selected_sponsorblock_categories = []

        count = len(self.selected_sponsorblock_categories)

        # Update label text
        if count == 0:
            self.selected_sponsorblock_label.setText(_("selection.none_selected"))
        elif count == 1:
            self.selected_sponsorblock_label.setText(_("selection.one_selected"))
        else:
            self.selected_sponsorblock_label.setText(_("selection.count_selected", count=count))

        # Update button property for styling
        self.sponsorblock_select_btn.setProperty("sponsorBlockSelected", count > 0)

        # Force style refresh
        self.sponsorblock_select_btn.style().unpolish(self.sponsorblock_select_btn)
        self.sponsorblock_select_btn.style().polish(self.sponsorblock_select_btn)

    def download_thumbnail(self, url) -> None:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.

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
            image.save(img_byte_arr, format="PNG")
            pixmap = QPixmap()
            pixmap.loadFromData(img_byte_arr.getvalue())
            self.thumbnail_label.setPixmap(pixmap)
        except Exception as e:
            logger.exception(f"Error loading thumbnail: {e}")

    def download_thumbnail_file(self, video_url, path) -> bool:
        self = cast("YTSageApp", self)  # for autocompletion and type inference.
        if not self.save_thumbnail:
            return False

        try:
            # Use cached thumbnail image from analysis if available
            if self.thumbnail_image is None:
                logger.info("No thumbnail image cached from analysis")
                self.signals.update_status.emit(_("status.thumbnail_no_image"))
                return False

            # Get video title from cached video_info
            video_title = "thumbnail"
            if self.video_info and "title" in self.video_info:
                video_title = self.video_info["title"]
            elif self.playlist_info and "title" in self.playlist_info:
                video_title = self.playlist_info["title"]

            logger.debug(f"Saving cached thumbnail for: {video_title}")

            # Save the thumbnail
            thumb_dir = Path(path).joinpath("Thumbnails")
            thumb_dir.mkdir(exist_ok=True)

            filename = f"{self.sanitize_filename(video_title)}.jpg"
            thumbnail_path = thumb_dir.joinpath(filename)

            # Save the cached PIL Image directly
            # Convert to RGB if necessary (in case of RGBA or other modes)
            if self.thumbnail_image.mode in ("RGBA", "P"):
                rgb_image = self.thumbnail_image.convert("RGB")
                rgb_image.save(thumbnail_path, "JPEG", quality=95)
            else:
                self.thumbnail_image.save(thumbnail_path, "JPEG", quality=95)

            logger.info(f"Thumbnail saved to: {thumbnail_path}")
            self.signals.update_status.emit(_("status.thumbnail_saved", filename=filename))
            return True

        except Exception as e:
            logger.exception(f"Thumbnail Save Error: {e}")
            self.signals.update_status.emit(_("status.thumbnail_error", error=str(e)))
            return False

    def sanitize_filename(self, name) -> str:
        """Clean filename for filesystem safety"""
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()[:75]
