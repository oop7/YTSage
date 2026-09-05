<div align="center">

<img src="branding/svg/ytsage-wordmark.svg" width="400" alt="ytsage-wordmark">
<img src="branding/screenshots/main.png" width="800" alt="YTSage Interface"/>

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-1f2937?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![PyPI Downloads](https://img.shields.io/pepy/dt/ytsage?color=1f2937&style=for-the-badge&label=downloads&logo=python&logoColor=white)](https://pepy.tech/project/ytsage)
[![GitHub Downloads](https://img.shields.io/github/downloads/oop7/YTSage/total?color=1f2937&style=for-the-badge&label=downloads&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![Telegram Channel](https://img.shields.io/badge/Telegram-YTSage--Official-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/YTsage_official)
[![License: MIT](https://img.shields.io/badge/License-MIT-1f2937?style=for-the-badge&logo=opensource&logoColor=white)](https://opensource.org/licenses/MIT)
[![Supported Platforms](https://img.shields.io/badge/platform-cross--platform-1f2937?style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![GitHub Stars](https://img.shields.io/github/stars/oop7/YTSage?color=c90000&style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/stargazers)
[![PyPI version](https://img.shields.io/pypi/v/ytsage?color=c90000&style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/ytsage/)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/oop7?color=c90000&style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/oop7)

**Modern YouTube downloader with a clean PySide6 interface.**  
Download videos in any quality, extract audio, fetch subtitles, and more.

### 🌍 README Languages

English: [EN](README.md)
| Arabic: [AR](readme-translations/README.ar.md)
| German: [DE](readme-translations/README.de.md)
| Spanish: [ES](readme-translations/README.es.md)
| French: [FR](readme-translations/README.fr.md)
| Hindi: [HI](readme-translations/README.hi.md)
| Indonesian: [ID](readme-translations/README.id.md)
| Italian: [IT](readme-translations/README.it.md)
| Japanese: [JA](readme-translations/README.ja.md)
| Korean: [KO](readme-translations/README.ko.md)
| Polish: [PL](readme-translations/README.pl.md)
| Portuguese: [PT](readme-translations/README.pt.md)
| Russian: [RU](readme-translations/README.ru.md)
| Turkish: [TR](readme-translations/README.tr.md)
| Chinese: [ZH](readme-translations/README.zh.md)
| Persian: [FA](readme-translations/README.fa.md)

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#troubleshooting">Troubleshooting</a> •
  <a href="https://t.me/YTsage_official">Telegram</a> •
  <a href="#sponsor">Sponsor</a> •
  <a href="#contributing">Contributing</a>
</p>

</div>

---

<a id="why-ytsage"></a>
## ❓ Why YTSage?

YTSage is designed for users who want a **simple yet powerful YouTube downloader**. Unlike other tools, it offers:

- A modern and clean PySide6 interface
- One-click downloads for video, audio, and subtitles
- Advanced features like SponsorBlock, subtitle merging, and playlist selection
- Optional Generic Mode for sites supported by yt-dlp beyond YouTube
- Cross-platform support and easy installation

<a id="features"></a>
## ✨ Features

<div align="center">

| Core Features | Advanced Features | Extra Features |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 Format Table | 🚫 SponsorBlock Integration | 🎞️ FPS/HDR Display |
| 🎵 Audio Extraction | 📝 Subtitle Selection & Merging | 🔄 Auto Update yt-dlp |
| ✨ Simple UI | 💾 Save Description & Thumbnail | 🛠️ FFmpeg/yt-dlp/Deno Detection |
| 📋 Playlist Support & Selector | 🚀 Speed Limiter | ⚙️ Custom Commands |
| 📑 Chapter Integration | ✂️ Video Section Trimming | 🍪 Login with Cookies |
| 📜 Download History | 🔄 Version Channel Selection | 🌐 Proxy Support |
| 🎚️ Audio Format Conversion | 🎬 Video Format Settings | 🆙 Built-in Updater Tab |
| 🌍 Generic Mode | 🔊 Audio Normalization (EBU R128) | 🌍 Localized in 16 Languages |
| 💾 Playlist Export | ⚙️ Default Quality & Subtitles | |
</div>

<a id="installation"></a>
## 🚀 Installation

### 📦 Download the App (Easiest Method)
*If you just want to use YTSage and don't know what Python is, start here*

[![Download Latest Release](https://img.shields.io/github/v/release/oop7/YTSage?label=Download%20Latest%20Release&style=for-the-badge&color=2ea44f&logo=github)](https://github.com/oop7/YTSage/releases/latest)

Simply download the pre-built installer for your operating system:

#### 🪟 Windows

| Format | Description |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | **Standard Installer (Recommended)** - Just double-click to install. |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | With FFmpeg Included (Use this if you don't already have FFmpeg). |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Portable version, no installation needed. |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Portable with FFmpeg, zipped. |

<details>
<summary>🛠️ Installation Steps</summary>

1. **EXE Installer (`.exe`)**: Double-click the file and follow the setup wizard.
2. **Portable Version (`.zip`)**: Extract the archive to your desired location and launch `ytsage.exe`.
3. **FFmpeg Included**: Choose versions with FFmpeg included if you don't have FFmpeg installed on your system.
</details>

#### 🍎 macOS

> ⚠️ **Note:** These installers are natively built for **Apple Silicon (M1/M2/M3/M4)**. If you are using an older Intel Mac, please use the [Python installation method](#-install-via-python--pypi) below.

| Format | Description |
|--------|-------------|
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | **Disk Image Installer (Recommended)** - Open and drag to Applications. |
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Zipped Application for Apple Silicon. |

<details>
<summary>🛠️ Installation Steps</summary>

- **DMG Installer (`.dmg`)**: Double-click to mount, then drag `YTSage.app` to your Applications folder.
- **Application Archive (`.zip`)**: Extract the zip and move `YTSage.app` to your Applications folder.

*Note: If you encounter an "Application is damaged" error, see the troubleshooting section below.*
</details>

#### 🐧 Linux

| Format | Description |
|--------|-------------|
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | **Portable AppImage (Recommended)** |
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Debian Package |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | RPM Package |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Flatpak Bundle |

<details>
<summary>🛠️ Installation Steps</summary>

- **AppImage (`.AppImage`)**:
  ```bash
  chmod +x YTSage-*.AppImage
  ./YTSage-*.AppImage
  ```
- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # Fix missing dependencies if needed
  ```
- **RPM (`.rpm`)**:
  ```bash
  sudo rpm -i ytsage-*.rpm
  ```
- **Flatpak**: Follow instructions on Flathub or run:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

---

### 🐍 Install via Python / PyPI
*You can also install YTSage via Python (Requires Python 3.11+)*

> 💡 **Awesome Feature:** If you install via pip on **Windows**, YTSage will automatically detect and help set up FFmpeg for you *(macOS and Linux users can follow our easy **[FFmpeg Installation Guide](https://github.com/oop7/ffmpeg-install-guide)**)*

```bash
pip install --pre ytsage
```

<details>
<summary>🔄 Update existing installation</summary>

```bash
pip install --upgrade --pre ytsage
```

</details>

Then launch the application:

```bash
ytsage
```

You can also open YTSage with a video or playlist URL prefilled and analyzed immediately:

```bash
ytsage "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

---

### 💻 Manual Source Installation (Developer)
*Run YTSage directly from the source code.*

<details>
<summary>View manual installation steps</summary>

#### 1. Clone the repository

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

#### 2. Install dependencies

**⚡ Using uv**
```bash
uv pip install .
```

**📦 Or using standard pip**
```bash
pip install .
```

#### 3. Run the application

```bash
python -m ytsage.main
```

</details>

<p align="right"><a href="#readme">⬆️ Back to Top</a></p>

<a id="screenshots"></a>
## 📸 Screenshots

<div align="center">
<table>
  <tr>
    <td><img src="branding/screenshots/Download-Settings.png" alt="Download Settings" width="400"/></td>
    <td><img src="branding/screenshots/playlist.png" alt="Playlist Download" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Download Settings</em></td>
    <td align="center"><em>Playlist Download</em></td>
  </tr>
  <tr>
    <td><img src="branding/screenshots/audio_format.png" alt="Audio Format Selection" width="400"/></td>
    <td><img src="branding/screenshots/Custom-Option.png" alt="Custom Options" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Audio Format</em></td>
    <td align="center"><em>Custom Options</em></td>
  </tr>
</table>
</div>

<p align="right"><a href="#readme">⬆️ Back to Top</a></p>

<a id="usage"></a>
## 📖 Usage

<details>
<summary>🎯 Basic Usage</summary>

1. **Launch YTSage**
2. **Paste YouTube URL** (or use "Paste URL" button)
3. **Click "Analyze"**
4. **Select Format:**
   - `Video` for video downloads
   - `Audio` for audio extraction
> 💡 You can now select and merge multiple audio tracks from the Audio section into a single video. Whether you want to combine a video with multiple language tracks, or merge several audio streams together.
5. **Choose Options:**
   - Enable Subtitles and select language
   - Enable Subtitle Merging
   - Save Thumbnail
   - Remove Sponsored Segments
   - Save Description
   - Embed Chapters (Chapters, Metadata, Thumbnail)

6. **Click "Download"**

> 💡 Default download directory is the user's "Downloads" folder.

</details>

<details>
<summary>📋 Playlist Download</summary>

1. **Paste Playlist URL**
2. **Click "Analyze"**
3. **Select videos from the playlist selector (optional, defaults to all)**
4. **Choose desired format/quality**
5. **Click "Download"**

> 💡 You can export playlist entries as (`.txt`, `.csv`, `.m3u`, or `.json`) by clicking on "Save Playlist As" button.

</details>

<details>
<summary>🌍 Generic Mode for Non-YouTube Sites</summary>

Use Generic Mode when you want YTSage to accept URLs from sites supported by yt-dlp, such as Dailymotion, CBC Gem, TikTok, and others.

How to use it:

1. Open `Download Settings`.
2. Toggle on `Generic Mode`.
3. Paste a supported video or playlist URL that is not from YouTube.
4. Click `Analyze`.
5. Choose a format and download as usual.

Notes:

- Generic mode only changes the URL validation inside YTSage. The target site must still be supported by your installed version of yt-dlp.
- Some sites require cookies, login sessions, proxy, or extra yt-dlp arguments depending on the extractor.
- If a site fails, update yt-dlp from the built-in updater tab first before reporting an issue.

</details>

<details>
<summary>🧰 Media & Download Options</summary>

- **Subtitle Options:** Filter languages and embed subtitles into the video file.
- **Subtitle Merging:** Merge subtitles into the video file for hardcoded/burned-in subtitles.
- **Save Description:** Save the video description as a text file.
- **Save Thumbnail:** Save the video thumbnail as an image file.
- **Embed:** This button allows you to embed chapters, metadata, and thumbnail into the downloaded video file.
- **Remove Sponsored Segments:** Remove sponsored segments from the video using SponsorBlock.
- **Trim Video:** Download only specific parts of a video by specifying time ranges in `HH:MM:SS` format.

</details>

<details>
<summary>⚙️ Output & File Settings</summary>

- **Speed Limiter:** Limit download speed, e.g., `500K` for 500 KB/s. Available in **Download Settings → General → Speed Limit**.
- **Save Download Path:** Saves default download directory across sessions. Available in **Download Settings → General → Download Path**.
- **Concurrent Connections:** Accelerate downloads using multiple connections/fragments (1 to 20 fragments). Available in **Download Settings → General → Concurrent Connections**.
- **Download History Toggle:** Enable or disable saving download history. Available in **Download Settings → General → Download History**.
- **Notification Sounds:** Enable or disable completion audio notification. Available in **Download Settings → General → Notification Sound**.
- **Force Output Format:** Force video container format (`mp4`, `webm`, `mkv`). Available in **Download Settings → Format → Output Format Settings**.
- **Audio Format Conversion:** Convert audio downloads to preferred formats (`AAC`, `MP3`, `FLAC`, `WAV`, `Opus`, `M4A`, `Vorbis`, or `Best`). Available in **Download Settings → Format → Audio Format Settings**.
- **Audio Normalization:** Normalize volume using EBU R128 standard for audio downloads. Available in **Download Settings → Format → Audio Format Settings**.
- **Default Video Resolution & Subtitles:** Auto-select default height (e.g. `1080`, `720`) and preferred subtitle languages (`en`, `es`, etc.) plus subtitle container format (`srt`, `vtt`, `ass`, `lrc`). Available in **Download Settings → Format → Default Selection Settings**.
- **Output Filename Format:** Customize output naming template using yt-dlp variables (e.g. `%(title)s_%(resolution)s_[%(id)s].%(ext)s`). Reset button included. Available in **Download Settings → File → Filename Format**.

</details>

<details>
<summary>🌐 Access & Network</summary>

- **Login with Cookies:** Access private or age-restricted content. Access via **Custom Options → Cookies**:
- **Browser Cookie Extraction (Recommended)**
  - Direct extraction from installed browsers: **Firefox** (preferred), **Chrome**, **Edge**, **Brave**, **Opera**, **Vivaldi**, etc.
    - Includes optional profile selection.
  - **Cookie File:** Load a Netscape format `cookies.txt` file.
- **Proxy & Geo-Verification Proxy Support:** Configure main proxy server and optional geo-verification proxy (SOCKS4/5 or HTTP/HTTPS) to bypass location restrictions. Access via **Custom Options → Proxy**.
- **Generic Mode:** Allow YTSage to process and download from non-YouTube URLs supported by yt-dlp. Toggle in **Download Settings → General → Generic Mode**.

</details>

<details>
<summary>🛠️ Tools & Maintenance</summary>

- **Custom Commands:** Execute custom `yt-dlp` arguments directly with live output logging and execution console. Access via **Custom Options → Custom Command**.
- **Updater Tab:** Comprehensive tool management inside **Custom Options → Updater**:
  - **App Updates:** Toggle automatic application update checks and enable/disable **Beta Releases** channel checks.
  - **yt-dlp Updates & Channel Selection:** Check for yt-dlp updates and switch release channels between **Stable** and **Nightly**.
  - **FFmpeg Version Checker:** Check local FFmpeg status/version against the latest release with step-by-step setup guides.
  - **Deno Updater:** Check, install, and upgrade the Deno JavaScript runtime required for yt-dlp ETP plugins.
- **FFmpeg/yt-dlp/Deno Detection:** Automatic detection and status verification of system dependencies visible from the **About** dialog.
- **Download History:** Browse, search, filter, and open past download history with thumbnails, original URLs, and local files. Access via the **History** button on the main toolbar.

</details>

<details>
<summary>🌍 Localization</summary>

YTSage supports **16 languages** for global accessibility. Select your preferred language in **Custom Options → Language**.

### Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| 🇺🇸 English | `en` | 🇪🇸 Spanish | `es` |
| 🇸🇦 Arabic | `ar` | 🇫🇷 French | `fr` |
| 🇩🇪 German | `de` | 🇮🇳 Hindi | `hi` |
| 🇮🇩 Indonesian | `id` | 🇮🇹 Italian | `it` |
| 🇯🇵 Japanese | `ja` | 🇰🇷 Korean | `ko` |
| 🇵🇱 Polish | `pl` | 🇧🇷 Portuguese | `pt` |
| 🇷🇺 Russian | `ru` | 🇹🇷 Turkish | `tr` |
| 🇨🇳 Chinese | `zh` | 🇮🇷 Persian | `fa` |

### README Translations

| Language | File | Language | File |
|----------|------|----------|------|
| 🇺🇸 English | [README.md](README.md) | 🇪🇸 Spanish | [readme-translations/README.es.md](readme-translations/README.es.md) |
| 🇸🇦 Arabic | [readme-translations/README.ar.md](readme-translations/README.ar.md) | 🇫🇷 French | [readme-translations/README.fr.md](readme-translations/README.fr.md) |
| 🇩🇪 German | [readme-translations/README.de.md](readme-translations/README.de.md) | 🇮🇳 Hindi | [readme-translations/README.hi.md](readme-translations/README.hi.md) |
| 🇮🇩 Indonesian | [readme-translations/README.id.md](readme-translations/README.id.md) | 🇮🇹 Italian | [readme-translations/README.it.md](readme-translations/README.it.md) |
| 🇯🇵 Japanese | [readme-translations/README.ja.md](readme-translations/README.ja.md) | 🇰🇷 Korean | [readme-translations/README.ko.md](readme-translations/README.ko.md) |
| 🇵🇱 Polish | [readme-translations/README.pl.md](readme-translations/README.pl.md) | 🇧🇷 Portuguese | [readme-translations/README.pt.md](readme-translations/README.pt.md) |
| 🇷🇺 Russian | [readme-translations/README.ru.md](readme-translations/README.ru.md) | 🇹🇷 Turkish | [readme-translations/README.tr.md](readme-translations/README.tr.md) |
| 🇨🇳 Chinese | [readme-translations/README.zh.md](readme-translations/README.zh.md) | 🇮🇷 Persian | [readme-translations/README.fa.md](readme-translations/README.fa.md) |

> 💡 **Want to contribute a translation?** Check out the [Contributing](#contributing) section to help us add more languages!

</details>

<p align="right"><a href="#readme">⬆️ Back to Top</a></p>

<a id="troubleshooting"></a>
## 🛠️ Troubleshooting

<details>
<summary>Click to view common issues and solutions</summary>

- **Format table not appearing:** Update yt-dlp to the latest version and switch to nightly yt-dlp.
- **Download failed:** Check your internet connection and ensure the video is available.
- **Specific Download Errors:**
  - **Private Videos:** Use cookie authentication to access private content.
  - **Age-Restricted Content:** Log in to your YouTube account to view age-restricted videos.
  - **Geo-Blocked Videos:** Consider using a VPN to bypass regional restrictions.
  - **Deleted Videos:** Video is no longer available on YouTube.
  - **Live Streams:** Live streams cannot be downloaded; wait for the broadcast to end.
  - **Network Errors:** Check your internet connection and try again.
  - **Invalid URLs:** Ensure the URL is correct and from a supported platform.
  - **Premium Content:** Requires a YouTube Premium subscription.
  - **Copyright Blocks:** Content is blocked due to copyright restrictions.
- **Video and audio files remain separate after download:** This happens when FFmpeg is missing or not detected. YTSage requires FFmpeg to merge high-quality video and audio streams.
  - **Solution:** Ensure FFmpeg is installed and accessible in your system's PATH. For Windows users, the easiest option is to download the `YTSage-v<version>-ffmpeg.exe` file, which comes bundled with FFmpeg.

---

#### 🛡️ Windows Defender / Antivirus Warning

Some antivirus software may flag `.exe` files as false positives. This is a **known limitation** of packaged applications.

**Why this happens:**
- Antivirus heuristics can mistakenly identify packaged executables as suspicious.

**Safe Alternatives:**
- ✅ **Use pip install:** `pip install ytsage` (Recommended)
- ✅ **Build from Source**: by following this [guide](.github/CI_CD_README.md)
- ✅ **Whitelist the app** in your antivirus software.

#### 🍎 macOS: "Application is damaged and cannot be opened"
If you see this error on macOS Sonoma or newer, you need to remove the quarantine attribute.

1.  **Open Terminal** (you can find this using Spotlight).
2.  **Type the following command** but **do not** press Enter yet. Make sure to include the space at the end:
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **Drag the `YTSage.app` file** from your Finder window and drop it directly into the Terminal window. This will automatically paste the correct file path.
4.  **Press Enter** to run the command.
5.  **Try opening YTSage.app again.** It should now launch correctly.

---

#### **Config Locations (Advanced)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<p align="right"><a href="#readme">⬆️ Back to Top</a></p>

<a id="sponsor"></a>
## 💖 Sponsor

If YTSage saves you time, please consider sponsoring the project. Sponsoring helps cover development time, testing across all platforms, and future improvements.

- GitHub Sponsors: https://github.com/sponsors/oop7
- Buy Me a Coffee: https://www.buymeacoffee.com/oop7
- Direct bank transfer / SWIFT: Contact me via email at [`oop7_support@proton.me`](mailto:oop7_support@proton.me)

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="contributing"></a>

## 👥 Contributing

<details>
<summary>Click to expand Contributing Guidelines</summary>

We welcome contributions! Here’s how you can help:

1. 🍴 Fork the **Beta branch**
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

- Update the relevant localized README file (e.g., `readme-translations/README.fr.md`)
- Keep app strings synced by editing `ytsage/languages/<code>.json`
- If your language is missing, start from `README.md` and create `readme-translations/README.<code>.md`

</details>

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
│   ├─── 📁 workflows/            # GitHub Actions workflows
│   │   ├── build-linux.yml        # Linux build workflow
│   │   ├── build-macos.yml        # macOS build workflow
│   │   │── build-windows.yml      # Windows build workflow
|   |   └── release-all.yml        # Release master workflow
|   |   └── star-history.yml       # Star history workflow
│   └── 📄 CI_CD_README.md        # CI/CD documentation
├──  📁 branding/                 # Branding assets (Screenshots, SVGs)
│   ├── 📁 icons/                 # App icons
│   ├── 📁 screenshots/           # Documentation screenshots
│   └── 📁 svg/                   # SVG assets
├── 📄 LICENSE                    # License file
├── 📄 pyproject.toml             # Project metadata and dependencies
├── 📄 README.md                  # Project documentation
├── 📄 requirements.txt           # Python dependencies (dev)
└── 📁 ytsage/                    # Source package
    ├── 📁 assets/                # Runtime assets
    │   ├── 📁 Icon/              # App icons
    │   └── 📁 sound/             # Sound files
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
    ├── 📁 gui/                   # UI components
    │   ├── 📄 __init__.py        # GUI package init
    │   ├── 📄 ytsage_gui_main.py # Main app window
    │   └── 📁 ytsage_gui_dialogs/ # Dialog classes
    ├── 📁 utils/                 # Utility modules
    │   ├── 📄 __init__.py        # Utils package init
    │   ├── 📄 ytsage_config_manager.py # Config management
    │   └── 📄 ytsage_logger.py   # Logging utilities
    ├── 📄 __init__.py            # Package entry point
    └── 📄 main.py                # Main execution script
```

</details>

<p align="right"><a href="#readme">⬆️ Back to Top</a></p>

## ⭐️ Star History

<div align="center">

[![Star History Chart](./branding/svg/star-history-dark.svg)](https://github.com/oop7/YTSage/stargazers)

</div>

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

<div align="left">

<p>A big thanks to everyone who contributed to this project by opening an issue to suggest an improvement or report a bug</p>
<p>Special thanks to <a href="https://github.com/bastik-1001"><strong>@bastik-1001</strong></a> and <a href="https://github.com/dj23me"><strong>@dj23me</strong></a> for being the first and major donors supporting this project ❤️</p>


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
        <td>Runtime for yt-dlp plugins</td>
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
        <td>Version/Package Management</td>
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
        <td><a href="https://github.com/bastik-1001">@bastik-1001</a></td>
        <td>First & Major Donor Support</td>
    </tr>
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

## ⚠️ Disclaimer

This tool is for personal use only. Please respect YouTube's Terms of Service and content creator rights.

---

<div align="center">

Made with ❤️ by [oop7](https://github.com/oop7)

</div>
