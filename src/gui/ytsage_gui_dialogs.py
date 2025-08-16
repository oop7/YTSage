"""
YTSage GUI Dialogs Module

This module serves as a centralized import point for all dialog classes in YTSage.
The dialogs have been split into logical modules for better maintainability:

- dialogs.ytsage_dialogs_base: Base utility dialogs (LogWindow, AboutDialog)
- dialogs.ytsage_dialogs_settings: Settings configuration dialogs
- dialogs.ytsage_dialogs_update: Update-related dialogs and threads
- dialogs.ytsage_dialogs_ffmpeg: FFmpeg installation dialogs
- dialogs.ytsage_dialogs_selection: Subtitle and playlist selection dialogs
- dialogs.ytsage_dialogs_custom: Custom functionality dialogs
"""

# Import all dialog classes from the dialogs package
from .dialogs import *

# For backward compatibility, re-export all dialog classes
__all__ = [
    # Base dialogs
    'LogWindow', 'AboutDialog',
    
    # Settings dialogs
    'DownloadSettingsDialog', 'AutoUpdateSettingsDialog',
    
    # Update dialogs and threads
    'VersionCheckThread', 'UpdateThread', 'YTDLPUpdateDialog', 'AutoUpdateThread',
    
    # FFmpeg dialogs
    'FFmpegInstallThread', 'FFmpegCheckDialog',
    
    # Selection dialogs
    'SubtitleSelectionDialog', 'PlaylistSelectionDialog', 'SponsorBlockCategoryDialog',
    
    # Custom functionality dialogs
    'CustomCommandDialog', 'CookieLoginDialog', 'CustomOptionsDialog', 'TimeRangeDialog'
]
