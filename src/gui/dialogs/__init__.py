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
from src.gui.dialogs.ytsage_dialogs_base import AboutDialog, LogWindow
from src.gui.dialogs.ytsage_dialogs_custom import (
    CookieLoginDialog,
    CustomCommandDialog,
    CustomOptionsDialog,
    TimeRangeDialog,
)
from src.gui.dialogs.ytsage_dialogs_ffmpeg import FFmpegCheckDialog, FFmpegInstallThread
from src.gui.dialogs.ytsage_dialogs_selection import (
    PlaylistSelectionDialog,
    SponsorBlockCategoryDialog,
    SubtitleSelectionDialog,
)
from src.gui.dialogs.ytsage_dialogs_settings import (
    AutoUpdateSettingsDialog,
    DownloadSettingsDialog,
)
from src.gui.dialogs.ytsage_dialogs_update import (
    AutoUpdateThread,
    UpdateThread,
    VersionCheckThread,
    YTDLPUpdateDialog,
)

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
    "CustomCommandDialog",
    "CookieLoginDialog",
    "CustomOptionsDialog",
    "TimeRangeDialog",
]
