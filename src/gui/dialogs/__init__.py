"""
Dialog modules for YTSage GUI.

This package contains all dialog classes organized by functionality:
- Base dialogs (LogWindow, AboutDialog)
- Settings dialogs (DownloadSettingsDialog, AutoUpdateSettingsDialog)
- Update dialogs (YTDLPUpdateDialog, update threads)
- FFmpeg dialogs (FFmpegCheckDialog, installation)
- Selection dialogs (SubtitleSelectionDialog, PlaylistSelectionDialog)
- Custom dialogs (CustomCommandDialog, CookieLoginDialog, etc.)
"""

# Re-export all dialog classes for backward compatibility
from .ytsage_dialogs_base import LogWindow, AboutDialog
from .ytsage_dialogs_settings import DownloadSettingsDialog, AutoUpdateSettingsDialog
from .ytsage_dialogs_update import (VersionCheckThread, UpdateThread, YTDLPUpdateDialog, 
                                   AutoUpdateThread)
from .ytsage_dialogs_ffmpeg import FFmpegInstallThread, FFmpegCheckDialog
from .ytsage_dialogs_selection import SubtitleSelectionDialog, PlaylistSelectionDialog, SponsorBlockCategoryDialog
from .ytsage_dialogs_custom import (CustomCommandDialog, CookieLoginDialog, 
                                   CustomOptionsDialog, TimeRangeDialog)

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
