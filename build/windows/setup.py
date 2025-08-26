"""
cx_Freeze setup script for YTSage
Supports building executables, MSI installers, and ZIP distributions
"""

import sys
from pathlib import Path
from cx_Freeze import setup, Executable

# Build options for executable
build_exe_options = {
    # Packages to include
    "packages": [
        "PySide6.QtCore",
        "PySide6.QtGui", 
        "PySide6.QtWidgets",
        "src.gui.ytsage_gui_main",
        "src.core.ytsage_utils",
        "src.core.ytsage_downloader",
        "src.core.ytsage_ffmpeg",
        "src.core.ytsage_yt_dlp",
        "src.core.ytsage_style",
        "src.core.ytsage_logging",
        "src.gui.ytsage_gui_format_table",
        "src.gui.ytsage_gui_video_info",
        "src.gui.ytsage_gui_dialogs",
        "src.gui.ytsage_gui_dialogs.ytsage_dialogs_base",
        "src.gui.ytsage_gui_dialogs.ytsage_dialogs_custom",
        "src.gui.ytsage_gui_dialogs.ytsage_dialogs_ffmpeg",
        "src.gui.ytsage_gui_dialogs.ytsage_dialogs_selection",
        "src.gui.ytsage_gui_dialogs.ytsage_dialogs_settings",
        "src.gui.ytsage_gui_dialogs.ytsage_dialogs_update",
        "src.utils.ytsage_constants",
        # Additional packages that might be needed
        "requests",
        "PIL",  # Pillow is imported as PIL
        "packaging",
        "markdown",
        "playsound3",
        "loguru",
        "setuptools"
    ],
    
    # Packages to exclude (to reduce size)
    "excludes": [
        "PySide6.QtBluetooth",
        "PySide6.QtNetwork",
        "PySide6.QtOpenGL",
        "PySide6.QtPrintSupport",
        "PySide6.QtSvg",
        "PySide6.QtTest",
        "PySide6.QtXml",
        "PySide6.QtSql",
        "PySide6.QtHelp",
        "PySide6.QtMultimedia",
        "PySide6.QtQml",
        "PySide6.QtQuick",
        "PySide6.QtWebEngineCore",
        "PIL.ImageDraw",
        "PIL.ImageFont",
        "numpy",
        "scipy",
        "wx",
        "pandas",
        "tkinter",
        "yt_dlp",  # Excluded - downloaded dynamically at runtime (all imports are conditional)
        "unittest",
        "test",
        "tests"
    ],
    
    # Include files (assets)
    "include_files": [
        ("assets/Icon/icon.png", "assets/Icon/icon.png"),
        ("assets/sound/notification.mp3", "assets/sound/notification.mp3"),
        ("assets/branding/icons/YTSage.ico", "YTSage.ico")
    ],
    
    # Zip includes (can help reduce file count)
    "zip_include_packages": "*",
    "zip_exclude_packages": [],
    
    # Other options
    "optimize": 2,  # Optimize bytecode
    "build_exe": "dist/YTSage",  # Output directory for executable
}

# MSI build options
bdist_msi_options = {
    "upgrade_code": "{12345678-1234-5678-9ABC-123456789ABC}",  # Generate unique GUID
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\YTSage",
    "install_icon": "assets/branding/icons/YTSage.ico",
    "summary_data": {
        "author": "oop7",
        "comments": "YouTube Video Downloader - Easy to use video downloading tool",
        "keywords": "youtube, downloader, video, audio, converter"
    }
}

# Base configuration for Windows GUI application
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # This prevents console window from appearing

# Executable configuration
executable = Executable(
    "main.py",
    base=base,
    icon="assets/branding/icons/YTSage.ico",
    target_name="YTSage-v4.8.0.exe",
    copyright="Copyright (c) 2024-2025 YTSage",
    trademarks="YTSage"
)

# Setup configuration
setup(
    name="YTSage",
    version="4.8.0",
    description="YouTube Video Downloader",
    author="oop7",
    author_email="oop7_support@proton.me",
    url="https://github.com/oop7/ytsage",
    license="MIT",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=[executable]
)
