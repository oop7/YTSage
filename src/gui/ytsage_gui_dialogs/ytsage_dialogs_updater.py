"""
Updater tab for Custom Options dialog.
Handles FFmpeg version checking and yt-dlp auto-update settings.
"""

import re
import subprocess
import threading
from typing import Optional, Tuple, TYPE_CHECKING, cast

import requests
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.core.ytsage_utils import (
    get_auto_update_settings,
    get_ffmpeg_version_direct,
    update_auto_update_settings,
)
from src.core.ytsage_yt_dlp import get_yt_dlp_path
from src.core.ytsage_deno import check_deno_update, upgrade_deno
from src.gui.ytsage_gui_dialogs.ytsage_dialogs_update import YTDLPUpdateDialog
from src.utils.ytsage_config_manager import ConfigManager
from src.utils.ytsage_localization import _
from src.utils.ytsage_logger import logger
from src.utils.ytsage_constants import (
    FFMPEG_7Z_VERSION_URL,
    OS_NAME,
    SUBPROCESS_CREATIONFLAGS,
)

if TYPE_CHECKING:
    from src.gui.ytsage_gui_dialogs.ytsage_dialogs_custom import CustomOptionsDialog


# Helper functions for FFmpeg version checking (copied from removed ytsage_ffmpeg_updater.py)
def get_latest_ffmpeg_version() -> Optional[str]:
    """
    Fetch the latest FFmpeg version from the version URL.
    
    Returns:
        str: Version string (e.g., "8.0") or None if fetch failed
    """
    try:
        response = requests.get(FFMPEG_7Z_VERSION_URL, timeout=10)
        response.raise_for_status()
        version = response.text.strip()
        
        # Validate version format (should be something like "8.0" or "7.1.1")
        if re.match(r'^\d+\.\d+(\.\d+)?$', version):
            logger.info(f"Latest FFmpeg version: {version}")
            return version
        else:
            logger.warning(f"Unexpected version format: {version}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Failed to fetch latest FFmpeg version: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error fetching FFmpeg version: {e}")
        return None


def parse_version(version_str: str) -> Tuple[int, ...]:
    """
    Parse version string into tuple of integers for comparison.
    
    Args:
        version_str: Version string like "8.0" or "7.1.1"
        
    Returns:
        Tuple of integers (e.g., (8, 0) or (7, 1, 1))
    """
    try:
        # Extract version numbers from string
        match = re.search(r'(\d+\.\d+(?:\.\d+)?)', version_str)
        if match:
            version_str = match.group(1)
        
        parts = version_str.split('.')
        return tuple(int(p) for p in parts)
    except (ValueError, AttributeError):
        logger.warning(f"Could not parse version: {version_str}")
        return (0,)


def compare_versions(current: str, latest: str) -> bool:
    """
    Compare two version strings.
    
    Args:
        current: Current version string
        latest: Latest version string
        
    Returns:
        True if update is needed (latest > current), False otherwise
    """
    try:
        current_tuple = parse_version(current)
        latest_tuple = parse_version(latest)
        
        logger.info(f"Comparing versions - Current: {current_tuple}, Latest: {latest_tuple}")
        
        # Pad shorter version with zeros for comparison
        max_len = max(len(current_tuple), len(latest_tuple))
        current_padded = current_tuple + (0,) * (max_len - len(current_tuple))
        latest_padded = latest_tuple + (0,) * (max_len - len(latest_tuple))
        
        return latest_padded > current_padded
    except Exception as e:
        logger.exception(f"Error comparing versions: {e}")
        return False


def check_ffmpeg_version() -> Tuple[bool, str, str]:
    """
    Check FFmpeg version and compare with latest.
    
    Returns:
        Tuple of (update_available, current_version, latest_version)
    """
    try:
        # Get current version
        current_version = get_ffmpeg_version_direct()
        if current_version in ["Not found", "Error getting version", "Unknown version"]:
            current_version = "Not installed"
        
        # Get latest version
        latest_version = get_latest_ffmpeg_version()
        if latest_version is None:
            latest_version = "Unknown"
            return False, current_version, latest_version
        
        # If not installed, update is available
        if current_version == "Not installed":
            return True, current_version, latest_version
        
        # Compare versions
        update_needed = compare_versions(current_version, latest_version)
        
        return update_needed, current_version, latest_version
        
    except Exception as e:
        logger.exception(f"Error checking FFmpeg version: {e}")
        return False, "Error", "Error"


class UpdaterTabWidget(QWidget):
    """Widget for the Updater tab in Custom Options dialog."""
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent: "CustomOptionsDialog" = cast("CustomOptionsDialog", self.parent())
        
        # State variables
        self.current_version = "Unknown"
        self.latest_version = "Unknown"
        self.update_available = False
        
        self._init_ui()
        self._load_auto_update_settings()
    
    def _init_ui(self) -> None:
        """Initialize the UI components."""
        # Main layout for the tab
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background: transparent; }")
        
        # Create a widget to hold all content
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        # Help text
        help_text = QLabel(_('ffmpeg_updater.description'))
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #999999; padding: 10px;")
        layout.addWidget(help_text)
        
        # FFmpeg Version Check Section
        ffmpeg_group = QGroupBox(_('ffmpeg_updater.title'))
        ffmpeg_layout = QVBoxLayout(ffmpeg_group)
        
        # Version information layout
        version_layout = QVBoxLayout()
        
        # Current version
        current_layout = QHBoxLayout()
        current_label = QLabel(_('ffmpeg_updater.current_version'))
        current_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        current_layout.addWidget(current_label)
        
        self.current_version_label = QLabel("...")
        self.current_version_label.setStyleSheet("color: #cccccc;")
        current_layout.addWidget(self.current_version_label)
        current_layout.addStretch()
        version_layout.addLayout(current_layout)
        
        # Latest version
        latest_layout = QHBoxLayout()
        latest_label = QLabel(_('ffmpeg_updater.latest_version'))
        latest_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        latest_layout.addWidget(latest_label)
        
        self.latest_version_label = QLabel("...")
        self.latest_version_label.setStyleSheet("color: #cccccc;")
        latest_layout.addWidget(self.latest_version_label)
        latest_layout.addStretch()
        version_layout.addLayout(latest_layout)
        
        ffmpeg_layout.addLayout(version_layout)
        
        # Status label
        self.status_label = QLabel(_('ffmpeg_updater.status_idle'))
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(
            "color: #888888; font-size: 12px; padding: 8px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
        ffmpeg_layout.addWidget(self.status_label)
        
        # Check version button
        check_button_layout = QHBoxLayout()
        self.check_button = QPushButton(_('ffmpeg_updater.check_updates'))
        self.check_button.clicked.connect(self.check_for_updates)
        self.check_button.setStyleSheet(
            """
            QPushButton {
                padding: 8px 15px;
                background-color: #444444;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666666;
            }
        """
        )
        check_button_layout.addWidget(self.check_button)
        check_button_layout.addStretch()
        ffmpeg_layout.addLayout(check_button_layout)
        
        # Installation guide info
        guide_label = QLabel(_('ffmpeg_updater.guide_info'))
        guide_label.setWordWrap(True)
        guide_label.setOpenExternalLinks(True)  # Enable clickable links
        guide_label.setTextFormat(Qt.TextFormat.RichText)  # Enable HTML formatting
        guide_label.setStyleSheet(
            """
            QLabel {
                color: #cccccc; 
                font-size: 11px; 
                padding: 8px; 
                background-color: #1a1d20; 
                border-radius: 4px;
            }
            QLabel a {
                color: #4da6ff;
                text-decoration: underline;
            }
            QLabel a:hover {
                color: #66b3ff;
            }
        """
        )
        ffmpeg_layout.addWidget(guide_label)
        
        layout.addWidget(ffmpeg_group)
        
        # === Deno Version Check & Update Section ===
        deno_group = QGroupBox(_('deno_updater.title'))
        deno_layout = QVBoxLayout(deno_group)
        
        # Description
        deno_desc = QLabel(_('deno_updater.description'))
        deno_desc.setWordWrap(True)
        deno_desc.setStyleSheet("color: #999999; padding: 10px;")
        deno_layout.addWidget(deno_desc)
        
        # Version information layout
        deno_version_layout = QVBoxLayout()
        
        # Current version
        deno_current_layout = QHBoxLayout()
        deno_current_label = QLabel(_('deno_updater.current_version'))
        deno_current_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        deno_current_layout.addWidget(deno_current_label)
        
        self.deno_current_version_label = QLabel("...")
        self.deno_current_version_label.setStyleSheet("color: #cccccc;")
        deno_current_layout.addWidget(self.deno_current_version_label)
        deno_current_layout.addStretch()
        deno_version_layout.addLayout(deno_current_layout)
        
        # Latest version
        deno_latest_layout = QHBoxLayout()
        deno_latest_label = QLabel(_('deno_updater.latest_version'))
        deno_latest_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        deno_latest_layout.addWidget(deno_latest_label)
        
        self.deno_latest_version_label = QLabel("...")
        self.deno_latest_version_label.setStyleSheet("color: #cccccc;")
        deno_latest_layout.addWidget(self.deno_latest_version_label)
        deno_latest_layout.addStretch()
        deno_version_layout.addLayout(deno_latest_layout)
        
        deno_layout.addLayout(deno_version_layout)
        
        # Status label
        self.deno_status_label = QLabel(_('deno_updater.status_idle'))
        self.deno_status_label.setWordWrap(True)
        self.deno_status_label.setStyleSheet(
            "color: #888888; font-size: 12px; padding: 8px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
        deno_layout.addWidget(self.deno_status_label)
        
        # Buttons layout
        deno_button_layout = QHBoxLayout()
        
        # Check for updates button
        self.deno_check_button = QPushButton(_('deno_updater.check_updates'))
        self.deno_check_button.clicked.connect(self.check_deno_updates)
        self.deno_check_button.setStyleSheet(
            """
            QPushButton {
                padding: 8px 15px;
                background-color: #444444;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666666;
            }
        """
        )
        deno_button_layout.addWidget(self.deno_check_button)
        
        # Update button (initially hidden)
        self.deno_update_button = QPushButton(_('deno_updater.update_now'))
        self.deno_update_button.clicked.connect(self.update_deno)
        self.deno_update_button.setVisible(False)
        self.deno_update_button.setStyleSheet(
            """
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QPushButton:pressed {
                background-color: #800000;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666666;
            }
        """
        )
        deno_button_layout.addWidget(self.deno_update_button)
        
        deno_button_layout.addStretch()
        deno_layout.addLayout(deno_button_layout)
        
        layout.addWidget(deno_group)
        
        # === yt-dlp Release Channel Section ===
        ytdlp_channel_group = QGroupBox(_("settings.ytdlp_channel"))
        ytdlp_channel_layout = QVBoxLayout()
        ytdlp_channel_layout.setSpacing(5)  # Reduce spacing
        ytdlp_channel_layout.setContentsMargins(10, 10, 10, 10)  # Reduce margins
        
        # Description
        channel_desc = QLabel(_("settings.ytdlp_channel_description"))
        channel_desc.setWordWrap(True)
        channel_desc.setStyleSheet("color: #cccccc; font-size: 11px; padding: 2px;")
        ytdlp_channel_layout.addWidget(channel_desc)
        
        # Radio buttons for channel selection
        self.channel_stable_radio = QRadioButton(_("settings.ytdlp_channel_stable"))
        self.channel_nightly_radio = QRadioButton(_("settings.ytdlp_channel_nightly"))
        
        radio_button_style = """
            QRadioButton {
                color: #ffffff;
                spacing: 5px;
                padding: 3px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #666666;
                background: #15181b;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
            }
        """
        self.channel_stable_radio.setStyleSheet(radio_button_style)
        self.channel_nightly_radio.setStyleSheet(radio_button_style)
        
        # Connect radio button signals
        self.channel_stable_radio.toggled.connect(self._on_channel_changed)
        self.channel_nightly_radio.toggled.connect(self._on_channel_changed)
        
        ytdlp_channel_layout.addWidget(self.channel_stable_radio)
        ytdlp_channel_layout.addWidget(self.channel_nightly_radio)
        
        # Status label for channel operations
        self.channel_status_label = QLabel("")
        self.channel_status_label.setWordWrap(True)
        self.channel_status_label.setStyleSheet(
            "color: #888888; font-size: 11px; padding: 5px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
        self.channel_status_label.setVisible(False)
        ytdlp_channel_layout.addWidget(self.channel_status_label)
        
        ytdlp_channel_group.setLayout(ytdlp_channel_layout)
        layout.addWidget(ytdlp_channel_group)
        
        # === Auto-Update yt-dlp Section ===
        auto_update_group_box = QGroupBox(_("settings.auto_update_ytdlp"))
        auto_update_layout = QVBoxLayout()

        # Enable/Disable auto-update checkbox
        self.auto_update_enabled = QCheckBox(_("settings.enable_auto_updates"))
        auto_update_layout.addWidget(self.auto_update_enabled)

        # Frequency options
        frequency_label = QLabel(_("settings.update_frequency"))
        frequency_label.setStyleSheet("color: #ffffff; margin-top: 10px;")
        auto_update_layout.addWidget(frequency_label)

        self.startup_radio = QRadioButton(_("settings.check_startup"))
        self.daily_radio = QRadioButton(_("settings.check_daily"))
        self.weekly_radio = QRadioButton(_("settings.check_weekly"))

        self.startup_radio.setStyleSheet(
            """
            QRadioButton {
                color: #ffffff;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #666666;
                background: #15181b;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
            }
        """
        )
        self.daily_radio.setStyleSheet(self.startup_radio.styleSheet())
        self.weekly_radio.setStyleSheet(self.startup_radio.styleSheet())

        auto_update_layout.addWidget(self.startup_radio)
        auto_update_layout.addWidget(self.daily_radio)
        auto_update_layout.addWidget(self.weekly_radio)

        # Test update button
        test_update_layout = QHBoxLayout()
        test_update_button = QPushButton(_("settings.check_updates_now"))
        test_update_button.clicked.connect(self.test_update_check)
        test_update_button.setStyleSheet(
            """
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QPushButton:pressed {
                background-color: #800000;
            }
        """
        )
        test_update_layout.addWidget(test_update_button)
        test_update_layout.addStretch()
        auto_update_layout.addLayout(test_update_layout)

        auto_update_group_box.setLayout(auto_update_layout)
        layout.addWidget(auto_update_group_box)
        
        layout.addStretch()
        
        # Set the content widget to the scroll area
        scroll_area.setWidget(content_widget)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)
    
    def _load_auto_update_settings(self) -> None:
        """Load current auto-update settings for yt-dlp."""
        try:
            auto_settings = get_auto_update_settings()
            
            # Set checkbox
            self.auto_update_enabled.setChecked(auto_settings["enabled"])
            
            # Set current selection based on saved settings
            current_frequency = auto_settings["frequency"]
            if current_frequency == "startup":
                self.startup_radio.setChecked(True)
            elif current_frequency == "daily":
                self.daily_radio.setChecked(True)
            else:  # weekly
                self.weekly_radio.setChecked(True)
            
            # Load channel setting
            channel = ConfigManager.get("ytdlp_channel")
            if channel is None:
                channel = "stable"  # Default to stable if not set
            
            if channel == "nightly":
                self.channel_nightly_radio.setChecked(True)
            else:
                self.channel_stable_radio.setChecked(True)
            
            # Update status label
            self._update_channel_status(channel)
            
        except Exception as e:
            logger.exception(f"Error loading auto-update settings: {e}")
    
    def get_auto_update_settings(self) -> tuple[bool, str]:
        """Returns the auto-update settings from the dialog."""
        enabled = self.auto_update_enabled.isChecked()

        if self.startup_radio.isChecked():
            frequency = "startup"
        elif self.daily_radio.isChecked():
            frequency = "daily"
        else:  # weekly_radio is checked
            frequency = "weekly"

        return enabled, frequency
    
    def _on_channel_changed(self, checked: bool) -> None:
        """Handle channel selection change."""
        if not checked:
            return
        
        # Determine which channel was selected
        new_channel = "nightly" if self.channel_nightly_radio.isChecked() else "stable"
        current_channel = ConfigManager.get("ytdlp_channel")
        if current_channel is None:
            current_channel = "stable"
        
        # If channel hasn't actually changed, just update status
        if new_channel == current_channel:
            self._update_channel_status(new_channel)
            return
        
        # Show switching message
        self.channel_status_label.setText(_("settings.ytdlp_switching_channel", channel=new_channel))
        self.channel_status_label.setStyleSheet(
            "color: #ffaa00; font-size: 11px; padding: 5px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
        self.channel_status_label.setVisible(True)
        
        # Disable radio buttons during switch
        self.channel_stable_radio.setEnabled(False)
        self.channel_nightly_radio.setEnabled(False)
        
        # Run channel switch in background thread
        def switch_channel():
            try:
                # Get yt-dlp path
                yt_dlp_path = get_yt_dlp_path()
                
                # Build the update command
                # When switching to stable from nightly, we need to get the latest stable version
                # to force the switch even if versions have the same date
                update_target = new_channel
                
                if new_channel == "stable" and current_channel == "nightly":
                    # Get the latest stable version tag from PyPI (no rate limiting)
                    logger.info("Fetching latest stable version tag from PyPI...")
                    try:
                        import requests
                        response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
                        response.raise_for_status()
                        latest_tag = response.json()["info"]["version"]
                        if latest_tag:
                            update_target = f"stable@{latest_tag}"
                            logger.info(f"Latest stable version tag: {latest_tag}")
                        else:
                            logger.warning("Could not determine latest stable tag, using 'stable'")
                    except Exception as e:
                        logger.warning(f"Failed to fetch latest stable tag, using 'stable': {e}")
                
                # Run the update-to command
                logger.info(f"Switching yt-dlp to {new_channel} channel...")
                logger.debug(f"Running command: {yt_dlp_path} --update-to {update_target}")
                result = subprocess.run(
                    [yt_dlp_path, "--update-to", update_target],
                    capture_output=True,
                    text=True,
                    timeout=120,
                    creationflags=SUBPROCESS_CREATIONFLAGS,
                )
                
                # Log the output for debugging
                if result.stdout:
                    logger.debug(f"yt-dlp stdout: {result.stdout.strip()}")
                if result.stderr:
                    logger.debug(f"yt-dlp stderr: {result.stderr.strip()}")
                logger.debug(f"yt-dlp return code: {result.returncode}")
                
                if result.returncode == 0:
                    # Success - save the preference
                    ConfigManager.set("ytdlp_channel", new_channel)
                    logger.info(f"Successfully switched to {new_channel} channel")
                    
                    # Update UI
                    self.channel_status_label.setText(_("settings.ytdlp_channel_switched", channel=new_channel))
                    self.channel_status_label.setStyleSheet(
                        "color: #00cc00; font-size: 11px; padding: 5px; "
                        "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
                    )
                    
                    # Make executable on Unix systems
                    if OS_NAME != "Windows":
                        import os
                        os.chmod(yt_dlp_path, 0o755)
                else:
                    # Failed - revert radio button
                    error_msg = result.stderr.strip() if result.stderr else result.stdout.strip() if result.stdout else "Unknown error"
                    logger.error(f"Failed to switch channel: {error_msg}")
                    
                    self.channel_status_label.setText(_("settings.ytdlp_channel_switch_failed", error=error_msg))
                    self.channel_status_label.setStyleSheet(
                        "color: #ff6666; font-size: 11px; padding: 5px; "
                        "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
                    )
                    
                    # Revert radio selection
                    if current_channel == "nightly":
                        self.channel_nightly_radio.setChecked(True)
                    else:
                        self.channel_stable_radio.setChecked(True)
                        
            except subprocess.TimeoutExpired:
                logger.error("Channel switch timed out")
                self.channel_status_label.setText(_("settings.ytdlp_channel_switch_failed", error="Timeout"))
                self.channel_status_label.setStyleSheet(
                    "color: #ff6666; font-size: 11px; padding: 5px; "
                    "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
                )
                # Revert radio selection
                if current_channel == "nightly":
                    self.channel_nightly_radio.setChecked(True)
                else:
                    self.channel_stable_radio.setChecked(True)
                    
            except Exception as e:
                logger.exception(f"Error switching channel: {e}")
                self.channel_status_label.setText(_("settings.ytdlp_channel_switch_failed", error=str(e)))
                self.channel_status_label.setStyleSheet(
                    "color: #ff6666; font-size: 11px; padding: 5px; "
                    "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
                )
                # Revert radio selection
                if current_channel == "nightly":
                    self.channel_nightly_radio.setChecked(True)
                else:
                    self.channel_stable_radio.setChecked(True)
            finally:
                # Re-enable radio buttons
                self.channel_stable_radio.setEnabled(True)
                self.channel_nightly_radio.setEnabled(True)
        
        # Start the thread
        thread = threading.Thread(target=switch_channel, daemon=True)
        thread.start()
    
    def _update_channel_status(self, channel: str) -> None:
        """Update the channel status label."""
        self.channel_status_label.setText(_("settings.ytdlp_current_channel", channel=channel))
        self.channel_status_label.setStyleSheet(
            "color: #888888; font-size: 11px; padding: 5px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
        self.channel_status_label.setVisible(True)
    
    def test_update_check(self) -> None:
        """Open the yt-dlp update dialog with proper progress tracking."""
        # Create and show the update dialog (non-modal to prevent blocking)
        dialog = YTDLPUpdateDialog(self)
        dialog.setModal(False)  # Make it non-modal
        dialog.show()  # Use show() instead of exec() to avoid blocking
    
    def check_for_updates(self) -> None:
        """Check FFmpeg version and compare with latest."""
        self.check_button.setEnabled(False)
        self.status_label.setText(_('ffmpeg_updater.status_checking'))
        self.status_label.setStyleSheet(
            "color: #ffaa00; font-size: 12px; padding: 8px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
        
        # Run check in background thread
        def check_thread():
            try:
                update_available, current_version, latest_version = check_ffmpeg_version()
                
                # Update UI in main thread
                self.check_button.setEnabled(True)
                self._update_check_results(update_available, current_version, latest_version)
                
            except Exception as e:
                logger.exception(f"Error checking FFmpeg version: {e}")
                self.check_button.setEnabled(True)
                self._show_check_error(str(e))
        
        thread = threading.Thread(target=check_thread, daemon=True)
        thread.start()
    
    def _update_check_results(self, update_available: bool, current_version: str, latest_version: str) -> None:
        """Handle completion of version check."""
        self.update_available = update_available
        self.current_version = current_version
        self.latest_version = latest_version
        
        # Update version labels
        self.current_version_label.setText(current_version)
        self.latest_version_label.setText(latest_version)
        
        # Update status
        if current_version == "Not installed":
            self.status_label.setText(_('ffmpeg_updater.status_not_installed'))
            self.status_label.setStyleSheet(
                "color: #ff6666; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
        elif update_available:
            self.status_label.setText(_('ffmpeg_updater.status_update_available'))
            self.status_label.setStyleSheet(
                "color: #ffaa00; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
        else:
            self.status_label.setText(_('ffmpeg_updater.status_up_to_date'))
            self.status_label.setStyleSheet(
                "color: #00cc00; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
    
    def _show_check_error(self, error: str) -> None:
        """Handle error during version check."""
        self.status_label.setText(_('ffmpeg_updater.check_failed'))
        self.status_label.setStyleSheet(
            "color: #ff6666; font-size: 12px; padding: 8px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
    
    def check_deno_updates(self) -> None:
        """Check for Deno updates."""
        self.deno_check_button.setEnabled(False)
        self.deno_update_button.setVisible(False)
        self.deno_status_label.setText(_('deno_updater.status_checking'))
        self.deno_status_label.setStyleSheet(
            "color: #ffaa00; font-size: 12px; padding: 8px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
        
        # Run check in background thread
        def check_thread():
            try:
                update_available, current_version, latest_version = check_deno_update()
                
                # Update UI in main thread
                self.deno_check_button.setEnabled(True)
                self._update_deno_check_results(update_available, current_version, latest_version)
                
            except Exception as e:
                logger.exception(f"Error checking Deno version: {e}")
                self.deno_check_button.setEnabled(True)
                self._show_deno_check_error(str(e))
        
        thread = threading.Thread(target=check_thread, daemon=True)
        thread.start()
    
    def _update_deno_check_results(self, update_available: bool, current_version: str, latest_version: str) -> None:
        """Handle completion of Deno version check."""
        # Update version labels
        self.deno_current_version_label.setText(current_version)
        self.deno_latest_version_label.setText(latest_version)
        
        # Update status
        if current_version in ["Not found", "Error getting version"]:
            self.deno_status_label.setText(_('deno_updater.status_not_installed'))
            self.deno_status_label.setStyleSheet(
                "color: #ff6666; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
        elif update_available:
            self.deno_status_label.setText(_('deno_updater.status_update_available'))
            self.deno_status_label.setStyleSheet(
                "color: #ffaa00; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
            # Show update button
            self.deno_update_button.setVisible(True)
        else:
            self.deno_status_label.setText(_('deno_updater.status_up_to_date'))
            self.deno_status_label.setStyleSheet(
                "color: #00cc00; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
    
    def _show_deno_check_error(self, error: str) -> None:
        """Handle error during Deno version check."""
        self.deno_status_label.setText(_('deno_updater.check_failed'))
        self.deno_status_label.setStyleSheet(
            "color: #ff6666; font-size: 12px; padding: 8px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
    
    def update_deno(self) -> None:
        """Update Deno to the latest version."""
        self.deno_check_button.setEnabled(False)
        self.deno_update_button.setEnabled(False)
        self.deno_status_label.setText(_('deno_updater.updating'))
        self.deno_status_label.setStyleSheet(
            "color: #ffaa00; font-size: 12px; padding: 8px; "
            "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
        )
        
        # Run update in background thread
        def update_thread():
            try:
                success, output = upgrade_deno()
                
                # Update UI in main thread
                self.deno_check_button.setEnabled(True)
                self.deno_update_button.setEnabled(True)
                self._handle_deno_update_result(success, output)
                
            except Exception as e:
                logger.exception(f"Error updating Deno: {e}")
                self.deno_check_button.setEnabled(True)
                self.deno_update_button.setEnabled(True)
                self._handle_deno_update_result(False, str(e))
        
        thread = threading.Thread(target=update_thread, daemon=True)
        thread.start()
    
    def _handle_deno_update_result(self, success: bool, output: str) -> None:
        """Handle Deno update completion."""
        if success:
            self.deno_status_label.setText(_('deno_updater.update_success'))
            self.deno_status_label.setStyleSheet(
                "color: #00cc00; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
            self.deno_update_button.setVisible(False)
            
            # Re-check version to update display
            self.check_deno_updates()
        else:
            # Extract meaningful error from output
            error_msg = output if output else "Unknown error"
            self.deno_status_label.setText(_('deno_updater.update_failed', error=error_msg))
            self.deno_status_label.setStyleSheet(
                "color: #ff6666; font-size: 12px; padding: 8px; "
                "background-color: #2a2d36; border-radius: 4px; margin: 5px 0;"
            )
