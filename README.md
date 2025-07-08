<div align="center">

# 🎥 YTSage

<img src="https://github.com/user-attachments/assets/f95f7bfb-8591-4d32-b795-68e61efd670c" width="800" alt="YTSage Interface"/>

[![PyPI version](https://img.shields.io/pypi/v/ytsage?color=dc2626&style=for-the-badge&logo=pypi&logoColor=white)](https://badge.fury.io/py/ytsage)
[![License: MIT](https://img.shields.io/badge/License-MIT-374151?style=for-the-badge&logo=opensource&logoColor=white)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-1f2937?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Downloads](https://img.shields.io/pypi/dm/ytsage?color=4b5563&style=for-the-badge&logo=download&logoColor=white)](https://pepy.tech/project/ytsage)
[![GitHub Stars](https://img.shields.io/github/stars/oop7/YTSage?color=dc2626&style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/stargazers)

**A modern YouTube downloader with a clean PySide6 interface.**  
Download videos in any quality, extract audio, fetch subtitles, and more.

</div>

## 📑 Table of Contents

<div align="center">

[Why YTSage?](#why-ytsage) |
[Features](#features) |
[Installation](#installation) |
[Screenshots](#screenshots) |
[Usage](#usage) |
[Troubleshooting & FAQ](#troubleshooting--faq) |
[Requirements](#requirements) |
[Contributing](#contributing) |
[License](#license) |
[Acknowledgments](#acknowledgments) |
[Disclaimer](#disclaimer)

</div>

<a id="why-ytsage"></a>

## ❓ Why YTSage?

YTSage is designed for users who want a **simple yet powerful YouTube downloader**. Unlike other tools, it offers:

- A clean, modern PySide6 interface
- One-click downloads for video, audio, and subtitles
- Advanced features like SponsorBlock, subtitle merging, and playlist selection
- Cross-platform support and easy installation

<a id="features"></a>

## ✨ Features

<table align="center">
  <thead>
    <tr>
      <th>Core Features</th>
      <th>Advanced Features</th>
      <th>Extra Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>🎥 Format Table</td>
      <td>🚫 SponsorBlock Integration</td>
      <td>💾 Save Download Path</td>
    </tr>
    <tr>
      <td>🎵 Audio Extraction</td>
      <td>📝 Multi-Subtitle Select & Merge</td>
      <td>🔄 Auto-Update yt-dlp</td>
    </tr>
    <tr>
      <td>✨ Simple UI</td>
      <td>💾 Save Description</td>
      <td>🛠️ FFmpeg/yt-dlp Detection</td>
    </tr>
    <tr>
      <td>📋 Playlist Support</td>
      <td>🖼️ Save thumbnail</td>
      <td>⚙️ Custom Commands</td>
    </tr>
    <tr>
      <td>🖼️ Playlist Selector</td>
      <td>🚀 Speed Limiter</td>
      <td>🍪 Login with Cookies</td>
    </tr>
    <tr>
      <td></td>
      <td>✂️ Trim Video Sections</td>
      <td></td>
    </tr>
  </tbody>
</table>

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

- 🪟 Windows: `YTSage.exe` / `YTSage-ffmpeg.exe` (with FFmpeg)
- 🐧 Linux: `YTSage_{version}_amd64.deb` / `YTSage-x86_64.AppImage`
- 🍎 macOS: `YTSage-macOS-app.zip` / `YTSage-{version}.dmg`

### 🛠️ Manual Installation from Source

> **Prerequisite:**  
> Install [uv](https://github.com/astral-sh/uv) (or use pip as fallback):
> 
> ```bash
> pip install uv
> ```

1. Clone the repository:
   
   ```bash
   git clone https://github.com/oop7/YTSage.git
   cd YTSage
   ```

2. Set up the environment and install dependencies
   
   ```bash
   uv sync
   ```

3. Run the application:
   
   ```bash
   uv run main.py
   ```

<a id="screenshots"></a>

## 📸 Screenshots

<div align="center">
<table>
  <td>
    <tr align="center">
      <img src="https://github.com/user-attachments/assets/f95f7bfb-8591-4d32-b795-68e61efd670c" alt="Main Interface"><br>
      <div align="center"><strong>Main Interface</strong></div><br>
    </tr>
    <tr align="center">
      <img src="https://github.com/user-attachments/assets/f7b3ebab-3054-4c77-8109-c899a8b10047" alt="Playlist Download"><br>
      <div align="center"><strong>Playlist Download</strong></div><br>
    </tr>
    <tr align="center">
      <img src="https://github.com/user-attachments/assets/a80d2ae2-0031-4ed0-bee4-93293634c62a" alt="Audio Format Selection with Save Thumbnail"><br>
      <div align="center"><strong>Audio Format Selection</strong></div><br>
    </tr>
    <tr align="center">
      <img src="https://github.com/user-attachments/assets/5236e3cc-8a8d-4d85-a660-782a740ef9af" alt="Subtitle Options merged with Remove Sponsor Segments"><br>
      <div align="center"><strong>Subtitle & SponsorBlock Options</strong></div><br>
    </tr>
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

- **Quality Selection:** Choose the highest resolution for best quality
- **Subtitle Options:** Filter languages and embed into video
- **Custom Commands:** Access advanced yt-dlp features
- **Save Description:** Save the description of the video
- **Save Thumbnail:** Save the thumbnail of the video
- **Remove Sponsor Segments:** Remove sponsor segments from the video
- **Speed Limiter:** Limit the download speed
- **Login with Cookies:** Login to YouTube using cookies to access private content  
  How to use:
  1. Extract cookies from your browser using [cookie-editor](https://github.com/moustachauve/cookie-editor?tab=readme-ov-file)
  2. Copy the cookies in Netscape format
  3. Create a file named `cookies.txt` and paste the cookies into it
  4. Select the `cookies.txt` file in the app
- **Save Download Path:** Save the download path
- **Update yt-dlp:** Update yt-dlp
- **FFmpeg/yt-dlp Detection:** Automatically detect FFmpeg/yt-dlp
- **Trim Video:** Download only specific parts of a video by specifying time ranges (HH:MM:SS format)

</details>

<a id="troubleshooting--faq"></a>

## 🛠️ Troubleshooting & FAQ

- **Format table not displaying:** Update yt-dlp to the latest version
- **Download fails:** Check your internet connection and ensure the video is available
- **Audio extraction issues:** Verify FFmpeg is properly installed
- **Where are downloads saved?** By default, to your chosen output directory
- **How to update yt-dlp?** Use the built-in auto-update or update manually

<a id="requirements"></a>

## 🧩 Requirements

- **Python:** 3.7 or higher
- **GUI Framework:** PySide6
- **Download Engine:** yt-dlp  
- **Media Processing:** FFmpeg
- **Additional Libraries:** Pillow, requests, packaging, markdown, pygame

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

## 📊 Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=oop7/YTSage&type=Date)](https://star-history.com/#oop7/YTSage&Date)

</div>

<a id="license"></a>

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<a id="acknowledgments"></a>

## 🙏 Acknowledgments

<div align="center">

<table>
  <thead>
    <tr>
      <th>Technology</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
      <td>Download Engine</td>
    </tr>
    <tr>
      <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
      <td>GUI Framework</td>
    </tr>
    <tr>
      <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
      <td>Media Processing</td>
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
      <td>Packaging</td>
    </tr>
    <tr>
      <td><a href="https://python-markdown.github.io/">markdown</a></td>
      <td>Markdown Processing</td>
    </tr>
    <tr>
      <td><a href="https://www.pygame.org/">pygame</a></td>
      <td>Audio Playback</td>
    </tr>
    <tr>
      <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 by Universfield</a></td>
      <td>Notification Sound</td>
    </tr>
  </tbody>
</table>

</div>

<a id="disclaimer"></a>

## ⚠️ Disclaimer

This tool is for personal use only. Please respect YouTube's terms of service and content creators' rights.

---

<div align="center">

Made with ❤️ by [oop7](https://github.com/oop7)

</div>
