from PySide6.QtCore import QThread, Signal, QObject
import yt_dlp # Keep yt_dlp import here - only downloader uses it.
import time
import os
import re
from pathlib import Path

class SignalManager(QObject):
    update_formats = Signal(list)
    update_status = Signal(str)
    update_progress = Signal(float)

class DownloadThread(QThread):
    progress_signal = Signal(float)
    status_signal = Signal(str)
    finished_signal = Signal()
    error_signal = Signal(str)
    file_exists_signal = Signal(str)  # New signal for file existence

    def __init__(self, url, path, format_id, subtitle_lang=None, is_playlist=False, merge_subs=False, enable_sponsorblock=False, resolution='', playlist_items=None):
        super().__init__()
        self.url = url
        self.path = path
        self.format_id = format_id
        self.subtitle_lang = subtitle_lang
        self.is_playlist = is_playlist
        self.merge_subs = merge_subs
        self.enable_sponsorblock = enable_sponsorblock
        self.resolution = resolution
        self.playlist_items = playlist_items
        self.paused = False
        self.cancelled = False

    def cleanup_partial_files(self):
        """Delete any partial files including .part and unmerged format-specific files"""
        try:
            pattern = re.compile(r'\.f\d+\.')  # Pattern to match format codes like .f243.
            for filename in os.listdir(self.path):
                file_path = os.path.join(self.path, filename)
                if filename.endswith('.part') or pattern.search(filename):
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting {filename}: {str(e)}")
        except Exception as e:
            self.error_signal.emit(f"Error cleaning partial files: {str(e)}")

    def check_file_exists(self):
        """Check if the file already exists before downloading"""
        try:
            print("DEBUG: Starting file existence check")
            # Use yt-dlp to get the filename without downloading
            with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
                info = ydl.extract_info(self.url, download=False)
                
                # Get the title and sanitize it for filename
                title = info.get('title', 'video')
                # Don't remove colons and other special characters yet
                print(f"DEBUG: Original video title: {title}")
                
                # Get resolution for better matching
                resolution = ""
                for format_info in info.get('formats', []):
                    if format_info.get('format_id') == self.format_id:
                        resolution = format_info.get('resolution', '')
                        break
                
                print(f"DEBUG: Resolution: {resolution}")
                
                # Create the expected filename (more specific)
                if self.is_playlist and info.get('playlist_title'):
                    playlist_title = re.sub(r'[\\/*?"<>|]', "", info.get('playlist_title', '')).strip()
                    base_path = os.path.join(self.path, playlist_title)
                else:
                    base_path = self.path
                
                # Normalize the path to use consistent separators
                base_path = os.path.normpath(base_path)
                print(f"DEBUG: Base path: {base_path}")
                
                # Instead of trying to predict the exact filename, scan the directory
                # and look for files that contain both the title and resolution
                if os.path.exists(base_path):
                    for filename in os.listdir(base_path):
                        if filename.endswith('.mp4'):
                            # Check if both title parts and resolution are in the filename
                            title_words = title.lower().split()
                            filename_lower = filename.lower()
                            
                            # Check if most title words are in the filename
                            title_match = all(word in filename_lower for word in title_words[:3])
                            resolution_match = resolution.lower() in filename_lower
                            
                            print(f"DEBUG: Checking file: {filename}, Title match: {title_match}, Resolution match: {resolution_match}")
                            
                            if title_match and resolution_match:
                                print(f"DEBUG: Found matching file: {filename}")
                                return filename
                
                print("DEBUG: No matching file found")
                return None
        except Exception as e:
            print(f"DEBUG: Error checking file existence: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def run(self):
        try:
            print("DEBUG: Starting download thread")
            # First check if file already exists
            existing_file = self.check_file_exists()
            if existing_file:
                print(f"DEBUG: File exists, emitting signal: {existing_file}")
                self.file_exists_signal.emit(existing_file)
                return
            
            print("DEBUG: No existing file found, proceeding with download")
            class DebugLogger:
                def debug(self, msg):
                    # Print all debug messages to help diagnose issues
                    print(f"YT-DLP DEBUG: {msg}")
                    
                    # Check for file exists message - look for both patterns
                    if "already exists" in msg or "has already been downloaded" in msg:
                        print(f"FILE EXISTS DETECTED: {msg}")
                        # Try to extract the filename
                        import re
                        match = re.search(r'File (.*?) already exists', msg)
                        if not match:
                            match = re.search(r'(.*?) has already been downloaded', msg)
                        
                        if match:
                            filename = os.path.basename(match.group(1))
                            self.thread.file_exists_signal.emit(filename)
                            raise Exception("FileExistsError")
                            
                    # Add detection of post-processing messages
                    if "Downloading" in msg:
                        self.thread.status_signal.emit("⚡ Downloading video...")
                    elif "Post-process" in msg or "Sponsorblock" in msg:
                        self.thread.status_signal.emit("✨ Post-processing: Removing sponsor segments...")
                        self.thread.progress_signal.emit(99)  # Keep progress bar at 99%
                    elif any(x in msg.lower() for x in ['downloading webpage', 'downloading api']):
                        self.thread.status_signal.emit("🔍 Fetching video information...")
                        self.thread.progress_signal.emit(0)
                    elif 'extracting' in msg.lower():
                        self.thread.status_signal.emit("📦 Extracting video data...")
                        self.thread.progress_signal.emit(0)
                    elif 'downloading m3u8' in msg.lower():
                        self.thread.status_signal.emit("🎯 Preparing video streams...")
                        self.thread.progress_signal.emit(0)

                def warning(self, msg):
                    print(f"YT-DLP WARNING: {msg}")
                    self.thread.status_signal.emit(f"⚠️ Warning: {msg}")
                    # Also check for file exists in warnings
                    if "already exists" in msg or "has already been downloaded" in msg:
                        print(f"FILE EXISTS DETECTED IN WARNING: {msg}")
                        import re
                        match = re.search(r'File (.*?) already exists', msg)
                        if not match:
                            match = re.search(r'(.*?) has already been downloaded', msg)
                            
                        if match:
                            filename = os.path.basename(match.group(1))
                            self.thread.file_exists_signal.emit(filename)
                            raise Exception("FileExistsError")

                def error(self, msg):
                    print(f"YT-DLP ERROR: {msg}")
                    self.thread.status_signal.emit(f"❌ Error: {msg}")
                    # Also check for file exists in errors
                    if "already exists" in msg or "has already been downloaded" in msg:
                        print(f"FILE EXISTS DETECTED IN ERROR: {msg}")
                        import re
                        match = re.search(r'File (.*?) already exists', msg)
                        if not match:
                            match = re.search(r'(.*?) has already been downloaded', msg)
                            
                        if match:
                            filename = os.path.basename(match.group(1))
                            self.thread.file_exists_signal.emit(filename)
                            raise Exception("FileExistsError")

                def __init__(self, thread):
                    self.thread = thread

            def progress_hook(d):
                if self.cancelled:
                    raise Exception("Download cancelled by user")

                if d['status'] == 'downloading':
                    while self.paused and not self.cancelled:
                        time.sleep(0.1)
                        continue

                    try:
                        downloaded_bytes = d.get('downloaded_bytes', 0)
                        total_bytes = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)

                        if total_bytes:
                            progress = (downloaded_bytes / total_bytes) * 100
                            self.progress_signal.emit(progress)

                        speed = d.get('speed', 0)
                        if speed:
                            speed_str = f"{speed/1024/1024:.1f} MB/s"
                        else:
                            speed_str = "N/A"

                        eta = d.get('eta', 0)
                        if eta:
                            eta_str = f"{eta//60}:{eta%60:02d}"
                        else:
                            eta_str = "N/A"

                        filename = os.path.basename(d.get('filename', ''))
                        status = f"Speed: {speed_str} | ETA: {eta_str} | File: {filename}"
                        self.status_signal.emit(status)

                    except Exception as e:
                        self.status_signal.emit("⚡ Downloading...")

                elif d['status'] == 'finished':
                    if self.enable_sponsorblock:
                        self.progress_signal.emit(99)
                        self.status_signal.emit("✨ Post-processing: Removing sponsor segments...")
                    else:
                        self.progress_signal.emit(100)
                        self.status_signal.emit("✅ Download completed!")

            # Get the extension from the format_id
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                try:
                    info = ydl.extract_info(self.url, download=False)
                    selected_format = next(
                        f for f in info['formats'] 
                        if str(f.get('format_id', '')) == self.format_id
                    )
                    output_ext = selected_format.get('ext', 'mp4')
                except Exception as e:
                    self.error_signal.emit(f"Failed to get video information: {str(e)}")
                    return

            # Base yt-dlp options with resolution in filename
            output_template = '%(title)s_%(resolution)s.%(ext)s'
            if self.is_playlist:
                output_template = '%(playlist_title)s/%(title)s_%(resolution)s.%(ext)s'

            ydl_opts = {
                'format': f'{self.format_id}+bestaudio/best',
                'outtmpl': os.path.join(self.path, output_template),
                'progress_hooks': [progress_hook],
                'merge_output_format': 'mp4',
                'logger': DebugLogger(self),
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }],
                'force_overwrites': True
            }

            # Add subtitle options if selected
            if self.subtitle_lang:
                lang_code = self.subtitle_lang.split(' - ')[0]
                is_auto = 'Auto-generated' in self.subtitle_lang
                ydl_opts.update({
                    'writesubtitles': True,
                    'subtitleslangs': [lang_code],
                    'writeautomaticsub': True,
                    'skip_manual_subs': is_auto,
                    'skip_auto_subs': not is_auto,
                    'embedsubtitles': self.merge_subs,
                })
                
                if self.merge_subs:
                    ydl_opts['postprocessors'].extend([
                        {
                            'key': 'FFmpegSubtitlesConvertor',
                            'format': 'srt',
                        },
                        {
                            'key': 'FFmpegEmbedSubtitle',
                            'already_have_subtitle': False,
                        }
                    ])

            # Add SponsorBlock options if enabled
            if self.enable_sponsorblock:
                ydl_opts['postprocessors'].extend([{
                    'key': 'SponsorBlock',
                    'categories': ['sponsor'],
                    'api': 'https://sponsor.ajay.app'
                }, {
                    'key': 'ModifyChapters',
                    'remove_sponsor_segments': ['sponsor'],
                    'sponsorblock_chapter_title': '[SponsorBlock]',
                    'force_keyframes': False
                }])

            # Add playlist items if specified
            if self.playlist_items:
                ydl_opts['playlist_items'] = self.playlist_items

            try:
                # Download the video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.url])

                if not self.cancelled:
                    self.finished_signal.emit()
                    
                    # Clean up subtitle files after successful download
                    if self.merge_subs:
                        for filename in os.listdir(self.path):
                            if filename.lower().endswith(('.vtt', '.srt', '.ass')):
                                try:
                                    os.remove(os.path.join(self.path, filename))
                                except Exception as e:
                                    self.error_signal.emit(f"Error deleting subtitle file: {str(e)}")
            
            except Exception as e:
                if str(e) == "Download cancelled by user":
                    self.cleanup_partial_files()
                    self.error_signal.emit("Download cancelled")
                else:
                    self.error_signal.emit(f"Download failed: {str(e)}")

        except Exception as e:
            self.error_signal.emit(f"Critical error: {str(e)}")