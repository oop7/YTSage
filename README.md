<div align="center">

<img src="branding\svg\ytsage-wordmark.svg" width="400" alt="ytsage-wordmark">
<img src="branding\screenshots\main.png" width="800" alt="YTSage Interface"/>

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-1f2937?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![PyPI Downloads](https://img.shields.io/pepy/dt/ytsage?color=1f2937&style=for-the-badge&label=downloads&logo=python&logoColor=white)](https://pepy.tech/project/ytsage)
[![GitHub Downloads](https://img.shields.io/github/downloads/oop7/YTSage/total?color=1f2937&style=for-the-badge&label=downloads&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-1f2937?style=for-the-badge&logo=opensource&logoColor=white)](https://opensource.org/licenses/MIT)
[![Supported Platforms](https://img.shields.io/badge/platform-cross--platform-1f2937?style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![GitHub Stars](https://img.shields.io/github/stars/oop7/YTSage?color=c90000&style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/stargazers)
[![PyPI version](https://img.shields.io/pypi/v/ytsage?color=c90000&style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/ytsage/)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/oop7?color=c90000&style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/oop7)

**A modern YouTube downloader with a clean PySide6 interface.**  
Download videos in any quality, extract audio, fetch subtitles, and more.

### 🌍 README Languages

English: [EN](README.md)
| العربية: [AR](readme-translations/README.ar.md)
| Deutsch: [DE](readme-translations/README.de.md)
| Español: [ES](readme-translations/README.es.md)
| Français: [FR](readme-translations/README.fr.md)
| हिन्दी: [HI](readme-translations/README.hi.md)
| Bahasa Indonesia: [ID](readme-translations/README.id.md)
| Italiano: [IT](readme-translations/README.it.md)
| 日本語: [JA](readme-translations/README.ja.md)
| Polski: [PL](readme-translations/README.pl.md)
| Português: [PT](readme-translations/README.pt.md)
| Русский: [RU](readme-translations/README.ru.md)
| Türkçe: [TR](readme-translations/README.tr.md)
| 中文: [ZH](readme-translations/README.zh.md)

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#troubleshooting">Troubleshooting</a> •
  <a href="#sponsor">Sponsor</a> •
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
- Optional Generic Mode for yt-dlp-supported sites beyond YouTube
- Cross-platform support and easy installation

<a id="features"></a>
## ✨ Features

<div align="center">

| Core Features                     | Advanced Features                       | Extra Features                     |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 Format Table                   | 🚫 SponsorBlock Integration             | 🎞️ FPS/HDR Display             |
| 🎵 Audio Extraction               | 📝 Multi-Subtitle Select & Merge        | 🔄 Auto-Update yt-dlp                               |
| ✨ Simple UI                      |  💾 Save Description & Thumbnail        | 🛠️ FFmpeg/yt-dlp/Deno Detection    |
| 📋 Playlist Support & Selector   | 🚀 Speed Limiter                        | ⚙️ Custom Commands                 |
| 📑 Embed Chapters                | ✂️ Trim Video Sections                  | 🍪 Login with Cookies              |
| 📜 Download History              | 🔄 Release Channel Selection            | 🌐 Proxy Support                   |
| 🎚️ Audio Format Conversion       | 🎬 Video Format Settings                | 🆙 Built-in Updater Tab            |
| 🌍 Generic Mode                   | 🔊 Audio Normalization (EBU R128)       | 🌍 Localization in 14 Languages    |
| 💾 Export Playlists               | ⚙️ Default Quality & Subtitles          |         |
</div>

<a id="installation"></a>
## 🚀 Installation

### ⚡ Quick Install (Recommended)

Install YTSage from PyPI:

```bash
pip install ytsage
```

<details>
<summary>🔄 Update an existing installation</summary>

```bash
pip install --upgrade ytsage
```

</details>

Then launch the app:

```bash
ytsage
```

### 📦 Pre-built Executables

> [👉 Download Latest Release](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| Format | Description |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Standard installer |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | With FFmpeg bundled |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Portable version, no installation required |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Portable with FFmpeg, zipped |

<details>
<summary>🛠️ Installation Steps</summary>

1. **EXE Installer (`.exe`)**: Double-click the file and follow the setup wizard.
2. **Portable Version (`.zip`)**: Extract the archive to your desired location and run `ytsage.exe`.
3. **FFmpeg Bundled**: Choose the FFmpeg bundled versions if you don't have FFmpeg installed on your system.
</details>

#### 🐧 Linux

| Format | Description |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Debian package |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage, portable |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | RPM package |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Flatpak Bundle |

<details>
<summary>🛠️ Installation Steps</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # Fix missing dependencies if any
  ```
- **RPM (`.rpm`)**:
  ```bash
  sudo rpm -i ytsage-*.rpm
  ```
- **AppImage (`.AppImage`)**:
  ```bash
  chmod +x YTSage-*.AppImage
  ./YTSage-*.AppImage
  ```
- **Flatpak**: Follow instructions on Flathub or run:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| Format | Description |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Zipped application for Apple Silicon |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Disk image installer for Apple Silicon |

<details>
<summary>🛠️ Installation Steps</summary>

- **DMG Installer (`.dmg`)**: Double-click to mount, then drag `YTSage.app` into your Applications folder.
- **App Archive (`.zip`)**: Extract the zip and move `YTSage.app` to your Applications folder.

*Note: If you encounter an "App is damaged" error, see the [macOS troubleshooting section](#troubleshooting) below.*
</details>

---

<details>
<summary>💻 Manual Installation from Source</summary>

### 1. Clone the Repository

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. Install Dependencies

#### ⚡ With uv

```bash
uv pip install .
```

#### 📦 Or with standard pip

```bash
pip install .
```

### 3. Run the Application

```bash
python -m ytsage.main
```

</details>

<a id="screenshots"></a>
## 📸 Screenshots

<div align="center">
<table>
  <tr>
    <td><img src="branding\screenshots\Download-Settings.png" alt="Download Settings" width="400"/></td>
    <td><img src="branding\screenshots\playlist.png" alt="Playlist Download" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Download Settings</em></td>
    <td align="center"><em>Playlist Download</em></td>
  </tr>
  <tr>
    <td><img src="branding\screenshots\audio_format.png" alt="Audio Format Selection with Save Thumbnail" width="400"/></td>
    <td><img src="branding\screenshots\Custom-Option.png" alt="Custom Options" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Audio Format</em></td>
    <td align="center"><em>Custom Options</em></td>
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

> 💡 The default download directory is the user's "Downloads" folder.

</details>

<details>
<summary>📋 Playlist Download</summary>

1. **Paste Playlist URL**
2. **Click "Analyze"**
3. **Select videos from the playlist selector (optional, defaults to all)**
4. **Choose desired format/quality**
5. **Click "Download"**

> 💡 The application automatically handles the download queue, and you can export the playlist entries to `.txt`, `.csv`, `.m3u`, or `.json` using the **Save Playlist As** button.

</details>

<details>
<summary>🌍 Generic Mode for non-YouTube sites</summary>

Use Generic Mode when you want YTSage to accept URLs from sites supported by yt-dlp, such as Dailymotion, CBC Gem, TikTok, and others.

How to use it:

1. Open `Download Settings`.
2. Enable `Generic Mode`.
3. Paste a supported non-YouTube video or playlist URL.
4. Click `Analyze`.
5. Choose a format and download as usual.

Notes:

- Generic Mode only changes URL validation inside YTSage. The target site must still be supported by your installed yt-dlp version.
- Some sites require cookies, a login session, a proxy, or extra yt-dlp arguments depending on the extractor.
- If a site fails, update yt-dlp first from the built-in updater tab before reporting the issue.

</details>

<details>
<summary>🧰 Media and Download Options</summary>

- **Subtitle Options:** Filter languages and embed subtitles into the video file
- **Subtitle Merge:** Merge subtitles into the video file for hardcoded subtitles
- **Save Description:** Save the video description as a text file
- **Save Thumbnail:** Save the video thumbnail as an image file
- **Embed Chapters:** Embed chapter markers as metadata for compatible video players
- **Remove Sponsor Segments:** Remove sponsor segments from the video using SponsorBlock
- **Trim Video:** Download only specific parts of a video by specifying time ranges in `HH:MM:SS` format

</details>

<details>
<summary>⚙️ Output and File Settings</summary>

- **Speed Limiter:** Limit the download speed, for example `500K` for 500 KB/s
- **Save Download Path:** Save the default download path for future downloads. Available in **Download Settings → Download Path**.
- **Default Video Resolution:** Set your preferred default video resolution for automatic selection (e.g., 1080p, 720p). Available in **Download Settings → Default Video Resolution**.
- **Default Subtitle Languages:** Set default subtitle languages to auto-select automatically (comma-separated, e.g., `en,es`). Available in **Download Settings → Default Subtitle Languages**.
- **Output Filename Format:** Customize the output filename format using variables like `%(title)s`, `%(uploader)s`, `%(playlist_index)s`, and `%(resolution)s`. Available in **Download Settings → Filename Format**.
- **Force Output Format:** Force video downloads into a specific container format such as `mp4`, `webm`, or `mkv`. Available in **Download Settings → Output Format Settings**.
- **Audio Format Conversion:** Convert audio-only downloads to preferred formats such as `AAC`, `MP3`, `FLAC`, `WAV`, `Opus`, `M4A`, `Vorbis`, or `Best`. Available in **Download Settings → Audio Format Settings**.
- **Audio Normalization:** Standardize volume for audio-only downloads using EBU R128.
- **Concurrent Connections:** Increase download speed dramatically by downloading files in multiple fragments concurrently. Available in **Download Settings → General → Concurrent Connections** (Defaults to 1, recommended maximum is 8-10 to prevent IP limiting).

</details>

<details>
<summary>🌐 Access and Network</summary>

- **Login with Cookies:** Login to YouTube using cookies to access private content.
  How to use it:
  1. **Recommended:** Use the built-in `Extract cookies from browser` option in the app, then select your browser and optionally a profile.
  2. Alternatively, extract cookies manually:
     a. Export cookies from your browser using an extension like [cookie-editor](https://github.com/moustachauve/cookie-editor?tab=readme-ov-file)
     b. Copy the cookies in Netscape format
     c. Create a file named `cookies.txt` and paste the cookies into it
     d. Select the `cookies.txt` file in the app
- **Proxy Support:** Use a proxy server for downloads, for example `http://<proxy-server>:<port>`
- **Generic Mode:** Allow YTSage to analyze and download from non-YouTube sites supported by yt-dlp. Enable it from **Download Settings → Generic Mode**.

</details>

<details>
<summary>🛠️ Tools and Maintenance</summary>

- **Custom Commands:** Access advanced yt-dlp features via command line arguments
- **Updater Tab:** Manage built-in update tools from one place in Custom Options:
  - **yt-dlp Updates:** Check for updates and switch between Stable and Nightly release channels
  - **FFmpeg Version Checker:** Check your FFmpeg version and open installation guides
  - **Deno Updates:** Check and update the Deno runtime
- **FFmpeg/yt-dlp/Deno Detection:** Automatically detect FFmpeg, yt-dlp, and Deno paths and versions from the About dialog.
- **Download History:** View past downloads with thumbnails and statuses from the **History** button.

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

### README Translations

| Language | File | Language | File |
|----------|------|----------|------|
| 🇺🇸 English | [README.md](README.md) | 🇪🇸 Spanish | [README.es.md](readme-translations/README.es.md) |
| 🇸🇦 Arabic | [README.ar.md](readme-translations/README.ar.md) | 🇫🇷 French | [README.fr.md](readme-translations/README.fr.md) |
| 🇩🇪 German | [README.de.md](readme-translations/README.de.md) | 🇮🇳 Hindi | [README.hi.md](readme-translations/README.hi.md) |
| 🇮🇩 Indonesian | [README.id.md](readme-translations/README.id.md) | 🇮🇹 Italian | [README.it.md](readme-translations/README.it.md) |
| 🇯🇵 Japanese | [README.ja.md](readme-translations/README.ja.md) | 🇵🇱 Polish | [README.pl.md](readme-translations/README.pl.md) |
| 🇧🇷 Portuguese | [README.pt.md](readme-translations/README.pt.md) | 🇷🇺 Russian | [README.ru.md](readme-translations/README.ru.md) |
| 🇹🇷 Turkish | [README.tr.md](readme-translations/README.tr.md) | 🇨🇳 Chinese | [README.zh.md](readme-translations/README.zh.md) |

> 💡 **Want to contribute a translation?** Check out the [Contributing](#contributing) section to help us add more languages!

</details>

<a id="troubleshooting"></a>
## 🛠️ Troubleshooting

<details>
<summary>Click to view common issues and solutions</summary>

- **Format table not displaying:** Update yt-dlp to the latest version, and switch to yt-dlp nightly.
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

<a id="sponsor"></a>
## 💖 Sponsor

If YTSage saves you time, consider sponsoring the project. Sponsorship helps cover development time, testing across platforms, and future improvements.

- GitHub Sponsors: https://github.com/sponsors/oop7
- The sponsor link is also available directly inside the app from the About dialog.

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

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

### 🌍 Contributing Translations

- Update the matching localized README file (for example `readme-translations/README.es.md`)
- Keep app strings in sync by editing `ytsage/languages/<code>.json`
- If your language is missing, start from `README.md` and create `README.<code>.md`

<details>
<summary>📂 Project Structure</summary>

## YTSage - Project Structure

This document describes the organized folder structure of YTSage.

### 📁 Project Structure

```
YTSage/
├── 📁 .github/                   # GitHub configuration
│   ├── 📁 ISSUE_TEMPLATE/         # Issue templates
│   │   └── 🐛-bug-report.md       # Bug report template
│   ├─── 📁 workflows/              # GitHub Actions workflows
│   │   ├── build-linux.yml        # Linux build workflow
│   │   ├── build-macos.yml        # macOS build workflow
│   │   │── build-windows.yml      # Windows build workflow
|   |   └── release-all.yml          # Master release workflow
│   └── 📄 CI_CD_README.md        # CI/CD documentation
├──  📁 branding/                 # Branding assets (Screenshots, SVGs)
│   ├── 📁 icons/                 # Application icons
│   ├── 📁 screenshots/           # Screenshots for documentation
│   └── 📁 svg/                   # SVG assets
├── 📄 LICENSE                    # License file
├── 📄 pyproject.toml             # Project metadata and dependencies
├── 📄 README.md                  # Project documentation
├── 📄 requirements.txt           # Python dependencies (dev)
└── 📁 ytsage/                    # Source package
    ├── 📁 assets/                # Runtime assets
    │   ├── 📁 Icon/              # Application icons
    │   └── 📁 sound/             # Audio files
    ├── 📁 languages/             # Localization files
    │   ├── 📄 ar.json            # Arabic translation
    │   ├── 📄 de.json            # German translation
    │   ├── 📄 en.json            # English translation
    │   └── ...                   # Other languages
    ├── 📁 core/                  # Core business logic
    │   ├── 📄 __init__.py        # Core package init
    │   ├── 📄 ytsage_deno.py     # Deno integration
    │   ├── 📄 ytsage_downloader.py # Download functionality
    │   ├── 📄 ytsage_ffmpeg.py   # FFmpeg integration
    │   ├── 📄 ytsage_utils.py    # Utility functions
    │   └── 📄 ytsage_yt_dlp.py   # yt-dlp integration
    ├── 📁 gui/                   # User interface components
    │   ├── 📄 __init__.py        # GUI package init
    │   ├── 📄 ytsage_gui_main.py # Main application window
    │   └── 📁 ytsage_gui_dialogs/ # Dialog classes
    ├── 📁 utils/                 # Utility modules
    │   ├── 📄 __init__.py        # Utils package init
    │   ├── 📄 ytsage_config_manager.py # Configuration management
    │   └── 📄 ytsage_logger.py   # Logging utilities
    ├── 📄 __init__.py            # Package entry point
    └── 📄 main.py                # Main execution script
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
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>Runtime for integration with yt-dlp</td>
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
