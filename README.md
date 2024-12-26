# YTSage

A modern YouTube downloader with a clean PyQt6 interface. Download videos in any quality, extract audio, fetch subtitles (including auto-generated), and view video metadata. Built with yt-dlp for reliable performance.

## Screenshots

### Main Interface

![Screenshot1](https://github.com/user-attachments/assets/414ceb6b-957f-4dd6-bfa7-6a5d72818522)

*Main interface with video metadata and thumbnail preview*

### Playlist download support with auto-detection

![Screenshot2](https://github.com/user-attachments/assets/d889b659-6196-4e53-a4ea-ff81b698e7f3)

*Playlist download with auto-detection*
### Audio Format Selection

![Screenshot](https://github.com/user-attachments/assets/b40641a2-659e-4a9f-9002-57badc37916d)

*Smart format selection with quality options*

### Subtitle Options

![Screenshot3](https://github.com/user-attachments/assets/0f356c89-9c8b-4050-ad74-fd006ebed22e)

*Support for both manual and auto-generated subtitles*

## Features

- 🎥 Smart video quality selection with automatic audio merging
- 🎵 Audio-only extraction
- 📝 Manual and auto-generated subtitle support
- ℹ️ Video metadata display (views, upload date, duration)
- 🖼️ Thumbnail preview
- 🎨 Clean, user-friendly interface
- 🚀 Built on yt-dlp for robust downloading
- ⏯️ Download control (pause, resume, and cancel)
- 📊 Real-time progress tracking (speed, ETA, percentage)
- 📝 Built-in yt-dlp log viewer
- ⚙️ Custom yt-dlp command support
- 📋 Playlist download support with auto-detection
- 💾 Save download path memory
- 🔄 Automatic updates checker
- ⚠️ User-friendly error messages
- 🛠️ FFmpeg installation checker and guide

## Download

You can download the latest executable from the [Releases](https://github.com/oop7/YTSage/releases) page.

### Pre-built Executables
- Windows: `YTSage.exe`
- macOS: `YTSage.app`
- Linux: `YTSage.AppImage`
- No installation required - just download and run!

### PyPI Package
You can also install YTSage directly from PyPI:
```bash
pip install YTSage
```


### Installation

1. Clone the repository:
```bash
git clone https://github.com/oop7/YTSage.git

cd YTSage
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python YTSage.py
```

# Usage

1. **Run the application**  
2. **Paste a YouTube URL** into the input field  
3. **Click "Analyze"** to load video information  
4. **Select your desired format**:  
   - Choose **"Video"** for video downloads (will automatically merge with best audio)  
   - Choose **"Audio Only"** for audio extraction  
5. **Enable subtitle download** if needed  
6. **Select the output directory**  
7. **Click "Download"** to start  

---

### Additional Steps for Playlist Download:

1. **Paste the Playlist URL**: Instead of a single video URL, paste the URL of the entire YouTube playlist into the input field.  
2. **Analyze the Playlist**: Click "Analyze" to load information for all videos in the playlist.  
3. **Select Best Quality**: Ensure that the best quality option is selected for both video and audio.  
4. **Download the Playlist**: Click "Download" to start downloading all videos in the playlist. The application should automatically handle the download queue.  

---

### Note:  
- **Best Quality**: Always select the highest available resolution (e.g., 1080p, 4K) for video and the best audio format (e.g., 320kbps) for the best experience.  
- **Subtitle Download**: If you need subtitles, enable this option before starting the download.  
- **Output Directory**: Choose a directory with enough storage space, especially for large playlists.  

By following these steps, you can efficiently download entire playlists in the best quality without encountering issues.  

## Requirements

- Python 3.7+
- PyQt6
- yt-dlp
- Pillow
- requests
- ffmpeg
- packaging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the powerful downloading engine
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [FFmpeg](https://ffmpeg.org/) for the audio and video processing
- [Pillow](https://pypi.org/project/Pillow/) for the image processing
- [requests](https://pypi.org/project/requests/) for the HTTP requests
- [packaging](https://pypi.org/project/packaging/) for the package management
- [PyInstaller](https://pypi.org/project/PyInstaller/) for the executable creation

## Disclaimer

This tool is for personal use only. Please respect YouTube's terms of service and content creators' rights.
