# YTSage

A modern YouTube downloader with a clean PyQt6 interface. Download videos in any quality, extract audio, fetch subtitles (including auto-generated), and view video metadata. Built with yt-dlp for reliable performance.

## Screenshots

### Main Interface
![Main Interface](https://github.com/user-attachments/assets/0dc04ecf-082e-458a-acfe-2c5482d36de2)

*Main interface with video metadata and thumbnail preview*

### Audio Format Selection

![Format Selection](https://github.com/user-attachments/assets/d2f8a638-0b6b-49f1-990d-c9c4791902a6)

*Smart format selection with quality options*

### Subtitle Options

![Subtitle Options](https://github.com/user-attachments/assets/b001ceb5-5446-4b56-b00c-b578814e2cf0)

*Support for both manual and auto-generated subtitles*

## Features

- 🎥 Smart video quality selection with automatic audio merging
- 🎵 Audio-only extraction
- 📝 Manual and auto-generated subtitle support
- ℹ️ Video metadata display (views, upload date, duration)
- 🖼️ Thumbnail preview
- 🎨 Clean, user-friendly interface
- 🚀 Built on yt-dlp for robust downloading

## Download

You can download the latest executable from the [Releases](https://github.com/yourusername/YTSage/releases) page.

### Pre-built Executables
- Windows: `YTSage.exe`
- No installation required - just download and run!

## Build from Source

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/YTSage.git

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

1. Run the application
2. Paste a YouTube URL into the input field
3. Click "Analyze" to load video information
4. Select your desired format:
   - Choose "Video" for video downloads (will automatically merge with best audio)
   - Choose "Audio Only" for audio extraction
5. Enable subtitle download if needed
6. Select the output directory
7. Click "Download" to start

### Build Executable

#### Install PyInstaller if you haven't already

- Create the executable

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name=YTSage YTSage.py
```

## Requirements

- Python 3.7+
- PyQt6
- yt-dlp
- Pillow
- requests

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

## Disclaimer

This tool is for personal use only. Please respect YouTube's terms of service and content creators' rights.
