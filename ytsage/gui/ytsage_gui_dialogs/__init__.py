"""
Dialog modules for YTSage GUI.

This package contains all dialog classes organized by functionality:

    - ytsage_dialogs_base: Base utility dialogs
    - ytsage_dialogs_settings: Settings configuration dialogs
    - ytsage_dialogs_update: Update-related dialogs and threads
    - ytsage_dialogs_ffmpeg: FFmpeg installation dialogs
    - ytsage_dialogs_selection: Subtitle and playlist selection dialogs
    - ytsage_dialogs_custom: Custom functionality dialogs
"""

# Re-export all dialog classes for backward compatibility
from .ytsage_dialogs_base import AboutDialog, LogWindow
from .ytsage_dialogs_custom import CustomOptionsDialog, TimeRangeDialog
from .ytsage_dialogs_ffmpeg import FFmpegCheckDialog, FFmpegInstallThread
from .ytsage_dialogs_history import HistoryDialog
from .ytsage_dialogs_selection import (
    PlaylistSelectionDialog,
    SponsorBlockCategoryDialog,
    SubtitleSelectionDialog,
)
from .ytsage_dialogs_settings import AutoUpdateSettingsDialog, DownloadSettingsDialog
from .ytsage_dialogs_update import AutoUpdateThread, UpdateThread, VersionCheckThread, YTDLPUpdateDialog
from .ytsage_dialogs_updater import UpdaterTabWidget

__all__ = [
    # Base dialogs
    "LogWindow",
    "AboutDialog",
    
    # Settings dialogs
    "DownloadSettingsDialog",
    "AutoUpdateSettingsDialog",
    
    # Update dialogs and threads
    "VersionCheckThread",
    "UpdateThread",
    "YTDLPUpdateDialog",
    "AutoUpdateThread",
    
    # FFmpeg dialogs
    "FFmpegInstallThread",
    "FFmpegCheckDialog",
    
    # Selection dialogs
    "SubtitleSelectionDialog",
    "PlaylistSelectionDialog",
    "SponsorBlockCategoryDialog",
    
    # Custom functionality dialogs
    "CustomOptionsDialog",
    "TimeRangeDialog",
    
    # Updater widget
    "UpdaterTabWidget",
    
    # History dialog
    "HistoryDialog",
]
