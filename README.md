<div align="center">

<img src="assets\branding\svg\ytsage-wordmark.svg" width="400" alt="ytsage-wordmark">
<img src="assets\branding\screenshots\main.png" width="800" alt="YTSage Interface"/>

[![PyPI version](https://img.shields.io/pypi/v/ytsage?color=dc2626&style=for-the-badge&logo=pypi&logoColor=white)](https://badge.fury.io/py/ytsage)
[![License: MIT](https://img.shields.io/badge/License-MIT-374151?style=for-the-badge&logo=opensource&logoColor=white)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-1f2937?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Downloads](https://img.shields.io/pepy/dt/ytsage?color=4b5563&style=for-the-badge&label=downloads&logo=download&logoColor=white)](https://pepy.tech/project/ytsage)
[![GitHub Stars](https://img.shields.io/github/stars/oop7/YTSage?color=dc2626&style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/stargazers)

**A modern YouTube downloader with a clean PySide6 interface.**  
Download videos in any quality, extract audio, fetch subtitles, and more.

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#troubleshooting">Troubleshooting</a> •
  <a href="#contributing">Contributing</a>
</p>

</div>

---

<a id="why-ytsage"></a>
## ❓ Why YTSage?

YTSage is designed for users who want a **simple yet powerful YouTube downloader**. Unlike other tools, it offers:

- A clean, modern PySide6 interface
- One-click downloads for video, audio, and subtitles
- Advanced features like SponsorBlock, subtitle merging, and playlist selection
- Cross-platform support and easy installation

<a id="features"></a>
## ✨ Features

<div align="center">

| Core Features                     | Advanced Features                       | Extra Features                     |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 Format Table                   | 🚫 SponsorBlock Integration             | 🎞️ FPS/HDR Display             |
| 🎵 Audio Extraction               | 📝 Multi-Subtitle Select & Merge        | 🔄 Auto-Update yt-dlp                  |
| ✨ Simple UI                      |  💾 Save Description                    | 🛠️ FFmpeg/yt-dlp Detection         |
| 📋 Playlist Support              |  🖼️ Save thumbnail                       | ⚙️ Custom Commands                 |
| 🖼️ Playlist Selector             | 🚀 Speed Limiter                        | 🍪 Login with Cookies              |
| 📑 Embed Chapters                | ✂️ Trim Video Sections                  | 🌐 Proxy Support                   |

</div>

<a id="installation"></a>
## 🚀 Installation

### ⚡ Quick Install (Recommended)

Install YTSage from PyPI:

```bash
pip install ytsage
```

Then launch the app:

```bash
ytsage
```

### 📦 Pre-built Executables

#### 🪟 Windows

| Format | Description |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Standard installer |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | With FFmpeg bundled |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Portable version, no installation required |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Portable with FFmpeg, zipped |

#### 🐧 Linux

| Format | Description |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Debian package |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage, portable |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | RPM package |

#### 🍎 macOS

| Format | Description |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Zipped application for ARM64 |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Disk image installer for ARM64 |
| ![macOS x64 APP](https://img.shields.io/badge/macOS-x64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Zipped application for x64 |
| ![macOS x64 DMG](https://img.shields.io/badge/macOS-x64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Disk image installer for x64 |

> [👉 Download Latest Release](https://github.com/oop7/YTSage/releases/latest)

<details>
<summary>🛠️ Manual Installation from Source</summary>

### 1. Clone the Repository

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. Install Dependencies

#### ⚡ With uv

```bash
uv pip install -r requirements.txt
```

#### 📦 Or with standard pip

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

</details>

<a id="screenshots"></a>
## 📸 Screenshots

<div align="center">
<table>
  <tr>
    <td><img src="assets\branding\screenshots\main.png" alt="Main Interface" width="400"/></td>
    <td><img src="assets\branding\screenshots\playlist.png" alt="Playlist Download" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Main Interface</em></td>
    <td align="center"><em>Playlist Download</em></td>
  </tr>
  <tr>
    <td><img src="assets\branding\screenshots\audio_format.png" alt="Audio Format Selection with Save Thumbnail" width="400"/></td>
    <td><img src="assets\branding\screenshots\subtitle_options.png" alt="Subtitle Options merged with Remove Sponsor Segments" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Audio Format</em></td>
    <td align="center"><em>Subtitle Options</em></td>
  </tr>
</table>
</div>

<a id="usage"></a>
## 📖 Usage

<details>
<summary>🎯 Basic Usage</summary>

1. **Launch YTSage**
2. **Paste YouTube URL** (or use "Paste URL" button)
3. **Click "Analyze"**
4. **Select Format:**
   - `Video` for video downloads
   - `Audio Only` for audio extraction
5. **Choose Options:**
   - Enable subtitles & select language
   - Enable subtitle merge
   - Save thumbnail
   - Remove sponsor segments
   - Save description
   - Embed chapters
6. **Select Output Directory**
7. **Click "Download"**

</details>

<details>
<summary>📋 Playlist Download</summary>

1. **Paste Playlist URL**
2. **Click "Analyze"**
3. **Select videos from the playlist selector (optional, defaults to all)**
4. **Choose desired format/quality**
5. **Click "Download"**

> 💡 The application automatically handles the download queue

</details>

<details>
<summary>🧰 Advanced Options</summary>

- **Subtitle Options:** Filter languages and embed into video file
- **Subtitle Merge:** Merge subtitles into video file for hardcoded subtitles
- **Custom Commands:** Access advanced yt-dlp features via command line arguments
- **Save Description:** Save the description of the video as a text file
- **Save Thumbnail:** Save the thumbnail of the video as an image file
- **Embed Chapters:** Embed chapter markers as metadata in the downloaded video file for compatible video players
- **Remove Sponsor Segments:** Remove sponsor segments from the video using SponsorBlock
- **Speed Limiter:** Limit the download speed (e.g., `500K` for 500 KB/s)
- **Login with Cookies:** Login to YouTube using cookies to access private content  
  How to use it:
  1. **Recommended:** Use the built-in "Extract cookies from browser" option in the app. Select your browser (Chrome, Firefox, etc.) and then select Profile (optional).
  2. Alternatively, extract cookies manually:
     a. Extract cookies from your browser using an extension like [cookie-editor](https://github.com/moustachauve/cookie-editor?tab=readme-ov-file)
     b. Copy the cookies in Netscape format
     c. Create a file named `cookies.txt` and paste the cookies into it
     d. Select the `cookies.txt` file in the app
- **Save Download Path:** Save the default download path for future downloads. You can find this option in the download settings dialog.
- **Update yt-dlp:** Check and update yt-dlp to the latest version from within the app. You can find this option in the download settings dialog.
- **FFmpeg/yt-dlp Detection:** Automatically detect FFmpeg/yt-dlp path and version. You can find this option in the about dialog.
- **Trim Video:** Download only specific parts of a video by specifying time ranges (HH:MM:SS format)
- **Proxy Support:** Use a proxy server for downloads (e.g., `http://<proxy-server>:<port>`)
- **Force output Format:** Force download in a specific format (e.g., `mp4`, `mkv`). You can find this option in the download settings dialog.
- **History**: View past downloads and their statuses. You can redownload or open the file location from the history dialog.

</details>

<details>
<summary>🌍 Localization</summary>

YTSage supports **14 languages** for worldwide accessibility. Select your preferred language from **Custom Options → Language**.

### Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| 🇺🇸 English | `en` | 🇪🇸 Spanish | `es` |
| 🇸🇦 Arabic | `ar` | 🇫🇷 French | `fr` |
| 🇩🇪 German | `de` | 🇮🇳 Hindi | `hi` |
| 🇮🇩 Indonesian | `id` | 🇮🇹 Italian | `it` |
| 🇯🇵 Japanese | `ja` | 🇵🇱 Polish | `pl` |
| 🇧🇷 Portuguese | `pt` | 🇷🇺 Russian | `ru` |
| 🇹🇷 Turkish | `tr` | 🇨🇳 Chinese | `zh` |

> 💡 **Want to contribute a translation?** Check out the [Contributing](#contributing) section to help us add more languages!

</details>

<a id="troubleshooting"></a>
## 🛠️ Troubleshooting

<details>
<summary>Click to view common issues and solutions</summary>

- **Format table not displaying:** Update yt-dlp to the latest version.
- **Download fails:** Check your internet connection and ensure the video is available.
- **Specific download errors:**
  - **Private videos:** Use cookie authentication to access private content.
  - **Age-restricted content:** Login to YouTube account to view age-restricted videos.
  - **Geo-blocked videos:** Consider using a VPN to bypass regional restrictions.
  - **Removed/deleted videos:** Video is no longer available on YouTube.
  - **Live streams:** Live streams cannot be downloaded; wait for the stream to end.
  - **Network errors:** Check your internet connection and try again.
  - **Invalid URLs:** Ensure the URL is correct and from a supported platform.
  - **Premium content:** Requires YouTube Premium membership.
  - **Copyright blocks:** Content is blocked due to copyright restrictions.
- **Separate video and audio files after download:** This happens when FFmpeg is missing or not detected. YTSage requires FFmpeg to merge high-quality video and audio streams.
  - **Solution:** Ensure FFmpeg is installed and accessible in your system's PATH. For Windows users, the easiest option is to download the `YTSage-v<version>-ffmpeg.exe` file, which comes bundled with FFmpeg.

---

#### 🛡️ Windows Defender / Antivirus Warning

Some antivirus software may flag the `.exe` files as false positives. This is a **known limitation** of packaged applications.

**Why this happens:**
- Antivirus heuristics can misidentify packed executables as suspicious

**Safe alternatives:**
- ✅ **Use pip installation:** `pip install ytsage` (recommended)
- ✅ **Build from source**: by following this [guide](.github/CI_CD_README.md)
- ✅ **Whitelist the application** in your antivirus software

#### 🍎 macOS: "App is damaged and can’t be opened"
If you see this error on macOS Sonoma or newer, you need to remove the quarantine attribute.

1.  **Open Terminal** (you can find it using Spotlight).
2.  **Type the following command** but **do not** press Enter yet. Make sure to include the space at the end:
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **Drag the `YTSage.app` file** from your Finder window and drop it directly into the Terminal window. This will automatically paste the correct file path.
4.  **Press Enter** to run the command.
5.  **Try opening YTSage.app again.** It should now launch correctly.

---

#### **Configuration Locations (Advanced)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="contributing"></a>
## 👥 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create your feature branch:
  ```bash
  git checkout -b feature/AmazingFeature
  ```
3. 💾 Commit your changes:
  ```bash
  git commit -m 'Add some AmazingFeature'
  ```
4. 📤 Push to the branch:
  ```bash
  git push origin feature/AmazingFeature
  ```
5. 🔄 Open a Pull Request

<details>
<summary>📂 Project Structure</summary>

## YTSage - Project Structure

This document describes the organized folder structure of YTSage.

### 📁 Project Structure

```
YTSage/
├── 📁 .github/                   # GitHub configuration
│   ├── 📄 CI_CD_README.md         # CI/CD documentation
│   ├── 📁 ISSUE_TEMPLATE/         # Issue templates
│   │   └── 🐛-bug-report.md       # Bug report template
│   └── 📁 workflows/              # GitHub Actions workflows
│       ├── build-linux.yml        # Linux build workflow
│       ├── build-macos.yml        # macOS build workflow
│       └── build-windows.yml      # Windows build workflow
├──  .gitignore                 # Git ignore rules
├──  📁 assets/                    # Static assets and resources
│   ├── 📁 branding/              # Branding assets
│   │   ├── 📁 icons/             # Application icons
│   │   │   ├── icon.icns         # macOS icon
│   │   │   ├── icon.png          # PNG icon
│   │   │   └── YTSage.ico        # Windows icon
│   │   └── 📁 screenshots/       # Screenshots for documentation
│   │       ├── audio_format.png
│   │       ├── main.png
│   │       ├── playlist.png
│   │       └── subtitle_options.png
│   │   └── 📁 svg/               # SVG assets
│   │       └── ytsage-wordmark.svg
│   ├── 📁 Icon/                  # Legacy icon directory
│   │   └── icon.png
│   └── 📁 sound/                 # Audio files
│       └── notification.mp3
├── 📁 languages/                 # Localization files
│   ├── 📄 ar.json                # Arabic translation
│   ├── 📄 de.json                # German translation
│   ├── 📄 en.json                # English translation
│   ├── 📄 es.json                # Spanish translation
│   ├── 📄 fr.json                # French translation
│   ├── 📄 hi.json                # Hindi translation
│   ├── 📄 id.json                # Indonesian translation
│   ├── 📄 it.json                # Italian translation
│   ├── 📄 ja.json                # Japanese translation
│   ├── 📄 pl.json                # Polish translation
│   ├── 📄 pt.json                # Portuguese translation
│   ├── 📄 ru.json                # Russian translation
│   ├── 📄 tr.json                # Turkish translation
│   └── 📄 zh.json                # Chinese translation
├── 📄 LICENSE                    # License file
├── 📄 main.py                    # Application entry point
├── 📄 README.md                  # Project documentation
├── 📄 requirements.txt           # Python dependencies
└── 📁 src/                       # Source code
    ├── 📄 __init__.py            # Main package init
    ├── 📁 core/                  # Core business logic
    │   ├── 📄 __init__.py        # Core package init
    │   ├── 📄 ytsage_downloader.py # Download functionality
    │   ├── 📄 ytsage_ffmpeg.py   # FFmpeg integration
    │   ├── 📄 ytsage_utils.py    # Utility functions
    │   └── 📄 ytsage_yt_dlp.py   # yt-dlp integration
    ├── 📁 gui/                   # User interface components
    │   ├── 📄 __init__.py        # GUI package init
    │   ├── 📄 ytsage_gui_format_table.py # Format table functionality
    │   ├── 📄 ytsage_gui_main.py # Main application window
    │   ├── 📄 ytsage_gui_video_info.py # Video information display
    │   └── 📁 ytsage_gui_dialogs/ # Dialog classes
    │       ├── 📄 __init__.py    # Dialogs package init
    │       ├── 📄 ytsage_dialogs_base.py     # Basic dialogs
    │       ├── 📄 ytsage_dialogs_custom.py   # Custom functionality dialogs
    │       ├── 📄 ytsage_dialogs_ffmpeg.py   # FFmpeg-related dialogs
    │       ├── 📄 ytsage_dialogs_selection.py # Selection dialogs
    │       ├── 📄 ytsage_dialogs_settings.py  # Settings dialogs
    │       └── 📄 ytsage_dialogs_update.py    # Update dialogs
    └── 📁 utils/                 # Utility modules
        ├── 📄 __init__.py        # Utils package init
        ├── 📄 ytsage_config_manager.py # Configuration management
        ├── 📄 ytsage_constants.py # Application constants
        ├── 📄 ytsage_localization.py # Localization utilities
        └── 📄 ytsage_logger.py   # Logging utilities
```

</details>

## ⭐️ Star History

<div align="center">

## Star History

<a href="https://www.star-history.com/#oop7/YTSage&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=oop7/YTSage&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=oop7/YTSage&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=oop7/YTSage&type=Date" />
 </picture>
</a>

</div>

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

<details>
<summary>Show Acknowledgments</summary>

<div align="center">

<p>A heartfelt thank you to everyone who has contributed to this project by opening an issue to suggest an improvement or report a bug.</p>

<table>
    <tr class="section"><th colspan="2">Core Components</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>Download Engine</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>Media Processing</td>
    </tr>
    <tr class="section"><th colspan="2">Libraries & Frameworks</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>GUI Framework</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>Image Processing</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>HTTP Requests</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>Version & Package Handling</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>Markdown Rendering</td>
    </tr>
    <tr>
        <td><a href="https://pyglet.org/">pyglet</a></td>
        <td>Audio Playback</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>Logging</td>
    </tr>
    <tr class="section"><th colspan="2">Assets & Contributors</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 by Universfield</a></td>
        <td>Notification Sound</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>Code Contributor</td>
    </tr>
</table>

</div>

</details>

## ⚠️ Disclaimer

This tool is for personal use only. Please respect YouTube's terms of service and content creators' rights.

---

<div align="center">

Made with ❤️ by [oop7](https://github.com/oop7)

</div>
