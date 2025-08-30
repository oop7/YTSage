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
from src.gui.ytsage_gui_dialogs.ytsage_dialogs_base import AboutDialog, LogWindow
from src.gui.ytsage_gui_dialogs.ytsage_dialogs_custom import CustomOptionsDialog, TimeRangeDialog
from src.gui.ytsage_gui_dialogs.ytsage_dialogs_ffmpeg import FFmpegCheckDialog, FFmpegInstallThread
from src.gui.ytsage_gui_dialogs.ytsage_dialogs_selection import (
    PlaylistSelectionDialog,
    SponsorBlockCategoryDialog,
    SubtitleSelectionDialog,
)
from src.gui.ytsage_gui_dialogs.ytsage_dialogs_settings import AutoUpdateSettingsDialog, DownloadSettingsDialog
from src.gui.ytsage_gui_dialogs.ytsage_dialogs_update import AutoUpdateThread, UpdateThread, VersionCheckThread, YTDLPUpdateDialog

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
]
