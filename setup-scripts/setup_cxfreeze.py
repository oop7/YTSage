import os
from pathlib import Path

from cx_Freeze import Executable, setup


ROOT = Path(__file__).resolve().parent.parent
version = os.environ.get("VERSION", "0.0.0")
suffix = os.environ.get("YTSAGE_EXECUTABLE_SUFFIX", "")

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
        "PySide6.QtSvg",
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
        "pydoc",
        "doctest",
        "email",
        "test",
        "tests",
    ],
    "include_files": [
        (str(ROOT / "ytsage" / "assets" / "Icon"), "lib/assets/Icon"),
        (str(ROOT / "ytsage" / "assets" / "sound"), "lib/assets/sound"),
        (str(ROOT / "ytsage" / "languages"), "lib/languages"),
        (str(ROOT / "branding" / "icons"), "lib/assets/branding/icons"),
    ],
}

executables = [
    Executable(
        script=str(Path(__file__).resolve().parent / "ytsage_entry.py"),
        target_name=f"YTSage-v{version}{suffix}.exe",
        base="gui",
        icon=str(ROOT / "branding" / "icons" / "YTSage.ico"),
    )
]

setup(
    name="YTSage",
    version=version,
    description="YTSage",
    options={"build_exe": build_exe_options},
    executables=executables,
)
