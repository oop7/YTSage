"""
cx_Freeze setup script for YTSage with FFmpeg bundle
Supports building executables, MSI installers, and ZIP distributions with FFmpeg
"""

import sys
from pathlib import Path
from cx_Freeze import setup, Executable
import os

# Get FFmpeg path from environment variable or use default
FFMPEG_PATH = os.environ.get('FFMPEG_PATH', r'C:\Users\atela\AppData\Local\ffmpeg\ffmpeg-7.1.1-full_build\bin')

# Prepare include files list
include_files = [
    ("src/", "src/"),  # Include entire src directory
    ("assets/Icon/icon.png", "assets/Icon/icon.png"),
    ("assets/sound/notification.mp3", "assets/sound/notification.mp3"),
    ("assets/branding/icons/YTSage.ico", "YTSage.ico"),
]

# Add FFmpeg binaries if they exist
ffmpeg_binaries = ["ffmpeg.exe", "ffprobe.exe", "ffplay.exe"]
for binary in ffmpeg_binaries:
    ffmpeg_file = os.path.join(FFMPEG_PATH, binary)
    if os.path.exists(ffmpeg_file):
        include_files.append((ffmpeg_file, binary))
        print(f"Including FFmpeg binary: {binary}")
    else:
        print(f"Warning: FFmpeg binary not found: {ffmpeg_file}")

# Build options for executable
build_exe_options = {
    # Let cx_Freeze auto-discover packages from main.py instead of explicit listing
    "packages": [
        "PySide6.QtCore",
        "PySide6.QtGui", 
        "PySide6.QtWidgets",
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
    
    # Include files (assets + FFmpeg binaries + source code)
    "include_files": include_files,
    
    # Zip includes (can help reduce file count)
    "zip_include_packages": "*",
    "zip_exclude_packages": [],
    
    # Other options
    "optimize": 2,  # Optimize bytecode
    "build_exe": "dist/YTSage-FFmpeg",  # Output directory for executable
}

# MSI build options - simplified to avoid cx_Freeze issues
bdist_msi_options = {
    "upgrade_code": "{87654321-4321-8765-CBA9-987654321CBA}",  # Different GUID for FFmpeg version
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\YTSage"
    # Removed summary_data that might cause silent failures
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
    target_name="YTSage-v4.7.4-ffmpeg.exe",
    copyright="Copyright (c) 2024-2025 YTSage",
    trademarks="YTSage"
)

# Setup configuration
setup(
    name="YTSage-FFmpeg",
    version="4.7.4",  # Updated to match expected version
    description="YouTube Video Downloader with FFmpeg",
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
