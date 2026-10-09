import os
from pathlib import Path

from cx_Freeze import Executable, setup


ROOT = Path(__file__).resolve().parent.parent
version = os.environ.get("VERSION", "0.0.0")

include_files_list = [
    (str(ROOT / "ytsage" / "assets" / "Icon"), "lib/assets/Icon"),
    (str(ROOT / "ytsage" / "assets" / "sound"), "lib/assets/sound"),
    (str(ROOT / "ytsage" / "languages"), "lib/languages"),
    (str(ROOT / "branding" / "icons"), "lib/assets/branding/icons"),
    (str(ROOT / "ytsage.desktop"), "share/applications/ytsage.desktop"),
    (str(ROOT / "branding" / "icons" / "icon.png"), "share/pixmaps/ytsage.png"),
]

build_exe_options = {
    "optimize": 2,
    "silent": True,
    "packages": [
        "ytsage",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "PySide6.QtMultimedia",
        "PySide6.QtNetwork",
        "PySide6.QtDBus",
        "PySide6.QtSvg",
        "requests",
        "PIL",
        "packaging",
        "markdown",
        "loguru",
        "setuptools",
    ],
    "zip_include_packages": [
        "PySide6",
        "shiboken6",
        "requests",
        "PIL",
        "packaging",
    ],
    "excludes": [
        "PySide6.QtBluetooth",
        "PySide6.QtOpenGL",
        "PySide6.QtPrintSupport",
        "PySide6.QtTest",
        "PySide6.QtXml",
        "PySide6.QtSql",
        "PySide6.QtHelp",
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
        "yt_dlp",
        "unittest",
        "test",
        "tests",
        "pydoc",
        "doctest",
        "email",
    ],
    "include_files": include_files_list,
    "bin_includes": [],
    "bin_excludes": [],
    "replace_paths": [("*", "")],
}

executables = [
    Executable(
        script=str(ROOT / "setup-scripts" / "ytsage_entry.py"),
        target_name="ytsage",
        icon=str(ROOT / "branding" / "icons" / "icon.png"),
    )
]

setup(
    name="ytsage",
    version=version,
    description="YTSage",
    options={
        "build_exe": build_exe_options,
        "bdist_appimage": {
            "target_name": f"ytsage-v{version}.AppImage",
        },
    },
    executables=executables,
)
