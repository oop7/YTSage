<div align="center">

# 🎥 YTSage

<img src="https://github.com/user-attachments/assets/04959c77-695b-4a69-b8fc-7103fe530236" width="800" alt="YTSage Interface"/>

[![PyPI version](https://badge.fury.io/py/YTSage.svg)](https://badge.fury.io/py/YTSage)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Downloads](https://pepy.tech/badge/ytsage)](https://pepy.tech/project/ytsage)

**A modern YouTube downloader with a clean PySide6 interface.**  
Download videos in any quality, extract audio, fetch subtitles, and more.

[Installation](#installation) •
[Features](#features) •
[Usage](#usage) •
[Screenshots](#screenshots) •
[Contributing](#contributing)

</div>

---

## ✨ Features

<div align="center">

| Core Features | Advanced Features | Extra Features |
|--------------|-------------------|----------------|
| 🎥 Smart Video Quality | 🚫 SponsorBlock Integration | 💾 Save Download Path |
| 🎵 Audio Extraction | 📝 Subtitle Support & Filtering | 🔄 Auto-Updates |
| 📊 Real-time Progress | ⚙️ Custom Commands | 🛠️ FFmpeg Tools |
| 📋 Playlist Support | 🖼️ Thumbnail Management | ⚠️ Error Handling |

</div>

## 🚀 Installation

### Quick Install (Recommended)
```bash
pip install YTSage
```
```bash
# Run the application
ytsage
```

<details>
<summary>📦 Other Installation Methods</summary>

### Pre-built Executables
- 🪟 Windows: `YTSage.exe`
- 🍎 macOS: `YTSage.dmg`
- 🐧 Linux: `YTSage.AppImage`

### Manual Installation
```bash
# Clone repository
git clone https://github.com/oop7/YTSage.git

# Navigate to directory
cd YTSage

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```
</details>

## 📸 Screenshots

<div align="center">
<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/04959c77-695b-4a69-b8fc-7103fe530236" alt="Main Interface" width="400"/></td>
    <td><img src="https://github.com/user-attachments/assets/537b8553-9657-42b2-a452-051c4cb2e32a" alt="Playlist Download" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Main Interface</em></td>
    <td align="center"><em>Playlist Download</em></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/51a6a613-6c97-4581-b728-38c91c0b2d24" alt="Audio Format" width="400"/></td>
    <td><img src="https://github.com/user-attachments/assets/4e8c686f-98e2-435a-add8-758e317b56fe" alt="Subtitle Options" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Audio Format Selection with Save Thumbnail</em></td>
    <td align="center"><em>Subtitle Options merged with Remove Sponsor Segments</em></td>
  </tr>
</table>
</div>

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
   - Enable subtitle embedding
   - Save thumbnail
   - Remove sponsor segments
6. **Select Output Directory**
7. **Click "Download"**

</details>

<details>
<summary>📋 Playlist Download</summary>

1. **Paste Playlist URL**
2. **Click "Analyze"**
3. **Select Best Quality**
4. **Click "Download"**

> 💡 The application automatically handles the download queue

</details>

<details>
<summary>⚙️ Advanced Options</summary>

- **Quality Selection:** Choose highest resolution for best quality
- **Subtitle Options:** Filter languages and embed into video
- **SponsorBlock:** Automatically skip promotional content
- **Custom Commands:** Access advanced yt-dlp features
- **Output Directory:** Ensure sufficient storage space

</details>

## 🛠️ Requirements

```plaintext
Python 3.7+
PySide6
yt-dlp
Pillow
requests
FFmpeg
packaging
```

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

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

<div align="center">

| Technology | Purpose |
|------------|---------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download Engine |
| [PySide6](https://wiki.qt.io/Qt_for_Python) | GUI Framework |
| [FFmpeg](https://ffmpeg.org/) | Media Processing |
| [Pillow](https://python-pillow.org/) | Image Processing |

</div>

## ⚠️ Disclaimer

This tool is for personal use only. Please respect YouTube's terms of service and content creators' rights.

---

<div align="center">

Made with ❤️ by [oop7](https://github.com/oop7)

</div>
