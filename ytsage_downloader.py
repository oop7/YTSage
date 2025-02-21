from PySide6.QtCore import QThread, Signal, QObject
import yt_dlp # Keep yt_dlp import here - only downloader uses it.
import time
import os
import re

class SignalManager(QObject):
    update_formats = Signal(list)
    update_status = Signal(str)
    update_progress = Signal(float)

class DownloadThread(QThread):
    progress_signal = Signal(float)
    status_signal = Signal(str)
    finished_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, url, path, format_id, subtitle_lang=None, is_playlist=False, merge_subs=False, enable_sponsorblock=False, resolution=''):
        super().__init__()
        self.url = url
        self.path = path
        self.format_id = format_id
        self.subtitle_lang = subtitle_lang
        self.is_playlist = is_playlist
        self.merge_subs = merge_subs
        self.enable_sponsorblock = enable_sponsorblock
        self.resolution = resolution
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

    def run(self):
        try:
            class DebugLogger:
                def debug(self, msg):
                    # Add detection of post-processing messages
                    if "Downloading" in msg:
                        self.thread.status_signal.emit("Downloading...")
                    elif "Post-process" in msg or "Sponsorblock" in msg:
                        self.thread.status_signal.emit("Post-processing: Removing sponsor segments...")
                        self.thread.progress_signal.emit(99)  # Keep progress bar at 99%
                    elif any(x in msg.lower() for x in ['downloading webpage', 'downloading api', 'extracting', 'downloading m3u8']):
                        self.thread.status_signal.emit("Preparing for download...")
                        self.thread.progress_signal.emit(0)

                def warning(self, msg):
                    self.thread.status_signal.emit(f"Warning: {msg}")

                def error(self, msg):
                    self.thread.status_signal.emit(f"Error: {msg}")

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
                        self.status_signal.emit("Downloading...")

                elif d['status'] == 'finished':
                    if self.enable_sponsorblock:
                        self.progress_signal.emit(99)
                        self.status_signal.emit("Post-processing: Removing sponsor segments...")
                    else:
                        self.progress_signal.emit(100)
                        self.status_signal.emit("Download completed!")

            # Base yt-dlp options with resolution in filename
            output_template = '%(title)s_%(resolution)s.%(ext)s'
            if self.is_playlist:
                output_template = '%(playlist_title)s/%(title)s_%(resolution)s.%(ext)s'

            ydl_opts = {
                'format': f'{self.format_id}+bestaudio/best',
                'outtmpl': os.path.join(self.path, output_template),
                'progress_hooks': [progress_hook],
                'merge_output_format': 'mkv' if self.merge_subs else 'mp4',
                'logger': DebugLogger(self),
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mkv' if self.merge_subs else 'mp4'
                }]
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
                self.progress_signal.emit(99)
                self.status_signal.emit("Post-processing: Removing sponsor segments...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

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
            self.error_signal.emit(str(e))