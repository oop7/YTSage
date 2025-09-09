import os
import re
import shlex  # For safely parsing command arguments
import subprocess  # For direct CLI command execution
import time
from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal

from src.core.ytsage_logging import logger
from src.core.ytsage_yt_dlp import get_yt_dlp_path
from src.utils.ytsage_constants import SUBPROCESS_CREATIONFLAGS

try:
    import yt_dlp  # Keep yt_dlp import here - only downloader uses it.

    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    logger.warning("yt-dlp not available at startup, will be downloaded at runtime")


class SignalManager(QObject):
    update_formats = Signal(list)
    update_status = Signal(str)
    update_progress = Signal(float)
    playlist_info_label_visible = Signal(bool)
    playlist_info_label_text = Signal(str)
    selected_subs_label_text = Signal(str)
    playlist_select_btn_visible = Signal(bool)
    playlist_select_btn_text = Signal(str)


class DownloadThread(QThread):
    progress_signal = Signal(float)
    status_signal = Signal(str)
    finished_signal = Signal()
    error_signal = Signal(str)
    file_exists_signal = Signal(str)  # New signal for file existence
    update_details = Signal(str)  # New signal for filename, speed, ETA

    def __init__(
        self,
        url,
        path,
        format_id,
        subtitle_langs=None,
        is_playlist=False,
        merge_subs=False,
        enable_sponsorblock=False,
        sponsorblock_categories=None,
        resolution="",
        playlist_items=None,
        save_description=False,
        embed_chapters=False,
        cookie_file=None,
        browser_cookies=None,
        rate_limit=None,
        download_section=None,
        force_keyframes=False,
    ) -> None:
        super().__init__()
        self.url = url
        self.path = Path(path)
        self.format_id = format_id
        self.subtitle_langs = subtitle_langs if subtitle_langs else []
        self.is_playlist = is_playlist
        self.merge_subs = merge_subs
        self.enable_sponsorblock = enable_sponsorblock
        self.sponsorblock_categories = sponsorblock_categories if sponsorblock_categories else ["sponsor"]
        self.resolution = resolution
        self.playlist_items = playlist_items
        self.save_description = save_description
        self.embed_chapters = embed_chapters
        self.cookie_file = cookie_file
        self.browser_cookies = browser_cookies
        self.rate_limit = rate_limit
        self.download_section = download_section
        self.force_keyframes = force_keyframes
        self.paused = False
        self.cancelled = False
        self.process = None
        self.use_direct_command = True  # Flag to use direct CLI command instead of Python API
        self.last_output_time = time.time()
        self.timeout_timer = None
        self.current_filename = None  # Initialize filename storage
        self.last_file_path = None  # Initialize full file path storage
        self.subtitle_files = []  # Track subtitle files that are created
        self.initial_subtitle_files = set()  # Track initial subtitle files before download

    def cleanup_partial_files(self) -> None:
        """Delete any partial files including .part and unmerged format-specific files"""
        try:
            pattern = re.compile(r"\.f\d+\.")  # Pattern to match format codes like .f243.
            for file_path in self.path.iterdir():
                if file_path.suffix == ".part" or pattern.search(file_path.name):
                    try:
                        file_path.unlink(missing_ok=True)
                    except Exception as e:
                        logger.error(f"Error deleting {file_path.name}: {str(e)}")
        except Exception as e:
            self.error_signal.emit(f"Error cleaning partial files: {str(e)}")

    def cleanup_subtitle_files(self) -> None:
        """Delete subtitle files after they have been merged into the video file"""
        deleted_count = [0, 0]

        def safe_delete(path: Path) -> bool:
            try:
                path.unlink(missing_ok=True)
                logger.debug(f"Deleted subtitle file: {path.name}")
                return True
            except Exception as e:
                logger.error(f"Error deleting subtitle file {path}: {e}")
                return False

        try:
            # --- Method 1: Delete tracked subtitle files ---
            for f in self.subtitle_files or []:
                deleted_count[0] += safe_delete(path=Path(f))
            else:
                logger.debug(f"Deleted {deleted_count[0]} of {len(self.subtitle_files)} tracked subtitle files")

            # --- Method 2: Delete new subtitle files not in initial set ---
            new_subtitle_files = {
                f for f in Path(self.path).rglob("*") if f.suffix in [".vtt", ".srt"] and f not in self.initial_subtitle_files
            }
            for subtitle_file in new_subtitle_files:
                deleted_count[1] += safe_delete(path=subtitle_file)
            else:
                logger.debug(f"Deleted {deleted_count[1]} of {len(new_subtitle_files)} new subtitle files")
        except Exception as e:
            logger.error(f"Error cleaning subtitle files: {str(e)}")

    def check_file_exists(self) -> bool | None:
        """Check if the file already exists before downloading"""
        try:
            logger.debug("Starting file existence check")
            # Use yt-dlp to get the filename without downloading, suppressing warnings
            ydl_opts_check = {
                "quiet": True,
                "skip_download": True,
                "no_warnings": True,  # <-- Suppress warnings during check
                "ignoreerrors": True,  # Also ignore other potential errors during this check
                "outtmpl": {"default": f"{self.path.as_posix()}/%(title)s.%(ext)s"},
                "format": (self.format_id if self.format_id else "best"),  # Use selected format or best
            }
            if self.cookie_file:
                ydl_opts_check["cookiefile"] = str(self.cookie_file)
            elif self.browser_cookies:
                ydl_opts_check["cookiesfrombrowser"] = (self.browser_cookies.split(':')[0], 
                                                       self.browser_cookies.split(':')[1] if ':' in self.browser_cookies else None)

            if YT_DLP_AVAILABLE:
                with yt_dlp.YoutubeDL(ydl_opts_check) as ydl:
                    info = ydl.extract_info(self.url, download=False)

                    # Handle cases where info extraction fails silently
                    if not info:
                        logger.debug("Failed to extract info during file existence check. Skipping check.")
                        return False  # Proceed with download attempt

                # Get the title and sanitize it for filename
                title = info.get("title", "video")
                # Don't remove colons and other special characters yet
                logger.debug(f"Original video title: {title}")

                # Get resolution for better matching
                resolution = ""
                for format_info in info.get("formats", []):
                    if format_info.get("format_id") == self.format_id:
                        resolution = format_info.get("resolution", "")
                        break

                logger.debug(f"Resolution: {resolution}")
            else:
                logger.debug("yt-dlp not available, skipping file existence check")
                return False  # Proceed with download attempt

        except Exception as e:
            logger.debug(f"Error checking file existence: {str(e)}")
            import traceback

            traceback.print_exc()
            return None

    def _build_yt_dlp_command(self) -> list:
        """Build the yt-dlp command line with all options for direct execution."""
        # Use the new yt-dlp path function from ytsage_yt_dlp module
        yt_dlp_path = get_yt_dlp_path()
        cmd: list = [yt_dlp_path]
        logger.debug(f"Using yt-dlp from: {yt_dlp_path}")

        # Format selection strategy - use format ID if provided or fallback to resolution
        if self.format_id:
            # Strip the -drc suffix if present to fix issues with certain audio formats
            clean_format_id = self.format_id.split("-drc")[0] if "-drc" in self.format_id else self.format_id

            # Check if this is an audio-only format
            is_audio_format = False
            try:
                if YT_DLP_AVAILABLE:
                    ydl_opts = {
                        "quiet": True,
                        "no_warnings": True,
                        "skip_download": True,
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(self.url, download=False) or {}
                        for fmt in info.get("formats", []):
                            if fmt.get("format_id") == clean_format_id:
                                if fmt.get("vcodec") == "none" or "audio only" in fmt.get("format_note", "").lower():
                                    is_audio_format = True
                                    logger.debug(f"Detected audio-only format for ID: {clean_format_id}")
                                break
            except Exception as e:
                logger.debug(f"Error checking if format is audio-only: {e}")

            # For audio-only formats, don't try to merge with video
            if is_audio_format:
                cmd.extend(["-f", clean_format_id])
                logger.debug(f"Using audio-only format selection: {clean_format_id}")
            else:
                cmd.extend(["-f", f"{clean_format_id}+bestaudio/best"])
                logger.debug(f"Using video format selection with audio: {clean_format_id}+bestaudio/best")

            # Determine output format based on the selected format ID - only for video formats
            if not is_audio_format:
                try:
                    format_ext = None
                    logger.debug(f"Getting format information for format ID: {self.format_id} (using: {clean_format_id})")
                    if YT_DLP_AVAILABLE:
                        ydl_opts = {
                            "quiet": True,
                            "no_warnings": True,
                            "skip_download": True,
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(self.url, download=False) or {}
                            # Look for the clean format ID first
                            for fmt in info.get("formats", []):
                                if fmt.get("format_id") == clean_format_id:
                                    format_ext = fmt.get("ext")
                                    break
                            # If not found, try the original ID as fallback
                            if not format_ext:
                                for fmt in info.get("formats", []):
                                    if fmt.get("format_id") == self.format_id:
                                        format_ext = fmt.get("ext")
                                        break

                    if format_ext:
                        logger.debug(f"Detected format extension: {format_ext}")
                        # Ensure output matches the selected format - only for video formats
                        cmd.extend(["--merge-output-format", format_ext])
                except Exception as e:
                    logger.debug(f"Error detecting format extension: {e}")
                    # If we can't determine the format, don't specify merge-output-format
                    pass
        else:
            # If no specific format ID, use resolution-based sorting (-S)
            res_value = self.resolution if self.resolution else "720"  # Default to 720p if no resolution specified
            cmd.extend(["-S", f"res:{res_value}"])

        # Output template with resolution in filename
        # Use string concatenation instead of Path.joinpath to avoid Path object issues
        base_path = self.path.as_posix()
        
        if self.is_playlist:
            # Create output template with playlist subfolder
            output_template = f"{base_path}/%(playlist_title)s/%(title)s_%(resolution)s.%(ext)s"
        else:
            output_template = f"{base_path}/%(title)s_%(resolution)s.%(ext)s"

        cmd.extend(["-o", output_template])

        # Add common options
        cmd.append("--force-overwrites")

        # Add playlist items if specified
        if self.is_playlist and self.playlist_items:
            cmd.extend(["--playlist-items", self.playlist_items])

        # Add subtitle options if subtitles are selected
        if self.subtitle_langs:
            # Subtitles work with both audio-only and video formats
            # For audio-only formats, subtitles will be downloaded as separate files
            cmd.append("--write-subs")

            # Get language codes from subtitle selections
            lang_codes = []
            for sub_selection in self.subtitle_langs:
                try:
                    # Extract just the language code (e.g., 'en' from 'en - Manual')
                    lang_code = sub_selection.split(" - ")[0]
                    lang_codes.append(lang_code)
                except Exception as e:
                    logger.warning(f"Could not parse subtitle selection '{sub_selection}': {e}")

            if lang_codes:
                cmd.extend(["--sub-langs", ",".join(lang_codes)])
                cmd.append("--write-auto-subs")  # Include auto-generated subtitles

                # Only embed subtitles if merge is enabled
                if self.merge_subs:
                    cmd.append("--embed-subs")

        # Add SponsorBlock if enabled
        if self.enable_sponsorblock and self.sponsorblock_categories:
            cmd.append("--sponsorblock-remove")
            cmd.append(",".join(self.sponsorblock_categories))

        # Add description saving if enabled
        if self.save_description:
            cmd.append("--write-description")

        # Add chapters embedding if enabled
        if self.embed_chapters:
            cmd.append("--embed-chapters")

        # Add cookies if specified
        if self.cookie_file:
            cmd.extend(["--cookies", str(self.cookie_file)])
        elif self.browser_cookies:
            cmd.extend(["--cookies-from-browser", self.browser_cookies])

        # Add rate limit if specified
        if self.rate_limit:
            cmd.extend(["-r", self.rate_limit])

        # Add download section if specified
        if self.download_section:
            cmd.extend(["--download-sections", self.download_section])

            # Add force keyframes option if enabled
            if self.force_keyframes:
                cmd.append("--force-keyframes-at-cuts")

            logger.debug(f"Added download section: {self.download_section}, Force keyframes: {self.force_keyframes}")

        # Add the URL as the final argument
        cmd.append(self.url)

        return cmd

    def run(self) -> None:
        try:
            logger.debug("Starting download thread")

            # First check if file already exists using original method
            existing_file = self.check_file_exists()
            if existing_file:
                logger.debug(f"File exists, emitting signal: {existing_file}")
                self.file_exists_signal.emit(existing_file)
                return

            logger.debug("No existing file found, proceeding with download")

            # Get initial list of subtitle files to compare later
            self.initial_subtitle_files = set()
            if self.merge_subs:
                try:
                    # Scan for existing subtitle files in the directory
                    for file in self.path.rglob("*"):
                        if file.suffix in {".vtt", ".srt"}:
                            self.initial_subtitle_files.add(file)
                    logger.debug(f"Found {len(self.initial_subtitle_files)} existing subtitle files before download")
                except Exception as e:
                    logger.warning(f"Error scanning for initial subtitle files: {e}")

            if self.use_direct_command:
                # Use direct CLI command instead of Python API
                self._run_direct_command()
            else:
                # Original method using Python API - code left for reference
                self._run_python_api()

        except Exception as e:
            # Catch errors during setup
            self.error_signal.emit(f"Critical error in download thread: {str(e)}")
            import traceback

            traceback.print_exc()

    def _run_direct_command(self) -> None:
        """Run yt-dlp as a direct command line process instead of using Python API."""
        try:
            cmd = self._build_yt_dlp_command()
            cmd_str = " ".join(shlex.quote(str(arg)) for arg in cmd)
            logger.debug(f"Executing command: {cmd_str}")

            self.status_signal.emit("🚀 Starting download...")
            self.progress_signal.emit(0)

            # Start the process
            # Extra logic moved to src\utils\ytsage_constants.py

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True,
                creationflags=SUBPROCESS_CREATIONFLAGS,
            )

            # Process output line by line to update progress
            for line in iter(self.process.stdout.readline, ""):  # type: ignore
                if self.cancelled:
                    self.process.terminate()
                    self.cleanup_partial_files()
                    self.status_signal.emit("Download cancelled")
                    return

                # Wait if paused
                while self.paused and not self.cancelled:
                    time.sleep(0.1)

                # Parse the line for download progress and status updates
                self._parse_output_line(line)

            # Wait for process to complete
            return_code = self.process.wait()

            # Special handling for specific errors
            # return code 127 typically means command not found
            if return_code == 127:
                self.error_signal.emit(
                    "Error: yt-dlp executable not found. This could be due to improper installation or a PATH issue."
                )
                return

            if return_code == 0:
                self.progress_signal.emit(100)
                self.status_signal.emit("✅ Download completed!")

                # Clean up subtitle files if they were merged, with a small delay
                # to ensure the embedding process has completed
                if self.merge_subs:
                    # Add a significant delay to ensure ffmpeg has released all file handles
                    # and any post-processing is complete
                    self.status_signal.emit("✅ Download completed! Cleaning up...")
                    time.sleep(3)  # Increased delay to 3 seconds
                    self.cleanup_subtitle_files()

                self.finished_signal.emit()
            else:
                # Check if it was cancelled
                if self.cancelled:
                    self.status_signal.emit("Download cancelled")
                else:
                    # Provide more descriptive error message for possible yt-dlp conflicts
                    if return_code == 1:
                        self.error_signal.emit(
                            f"Download failed with return code {return_code}. This may be due to a conflict with multiple yt-dlp installations. Try uninstalling any system-installed yt-dlp (e.g. through snap or apt) and restart the application."
                        )
                    else:
                        self.error_signal.emit(f"Download failed with return code {return_code}")
                    self.cleanup_partial_files()

        except Exception as e:
            self.error_signal.emit(f"Error in direct command: {str(e)}")
            self.cleanup_partial_files()

    def _parse_output_line(self, line) -> None:
        """Parse yt-dlp command output to update progress and status."""
        line = line.strip()
        # logger.info(f"yt-dlp: {line}")  # Log all output - OPTIONALLY UNCOMMENT FOR VERBOSE DEBUG

        # Extract filename when the destination line appears
        # Use a slightly more robust regex looking for the start of the line
        dest_match = re.search(r"^\[download\] Destination:\s*(.*)", line)
        if dest_match:
            try:
                filepath = dest_match.group(1).strip()
                self.current_filename = Path(filepath).name
                self.last_file_path = filepath  # Store the full path for later cleanup
                logger.debug(f"Extracted filename: {self.current_filename}")  # DEBUG

                # Check if this is an audio-only download by looking in the previous lines
                is_audio_download = False

                # Look for audio format indicators in the current line or preceding output
                # yt-dlp typically mentions format like "Downloading format 251 - audio only"
                if " - audio only" in line:
                    is_audio_download = True
                # Check if the format ID is mentioned earlier in the line
                format_match = re.search(r"Downloading format (\d+)", line)
                if format_match:
                    format_id = format_match.group(1)
                    logger.debug(f"Detected format ID: {format_id}")
                    # Format IDs for audio typically have different patterns
                    # (like 140, 251 for audio vs 137, 248 for video)
                    # This is just a heuristic since format IDs can vary

                # Determine file type based on extension and context
                ext = Path(self.current_filename).suffix.lower()

                # Check if this is explicitly an audio stream download
                if is_audio_download or "Downloading audio" in line:
                    self.status_signal.emit(f"⏬ Downloading audio...")
                # Video file extensions with likely video content
                elif ext in [".mp4", ".webm", ".mkv", ".avi", ".mov", ".flv"]:
                    self.status_signal.emit(f"⏬ Downloading video...")
                # Audio file extensions
                elif ext in [".mp3", ".m4a", ".aac", ".wav", ".ogg", ".opus", ".flac"]:
                    self.status_signal.emit(f"⏬ Downloading audio...")
                # Subtitle file extensions
                elif ext in [".vtt", ".srt", ".ass", ".ssa"]:
                    self.status_signal.emit(f"⏬ Downloading subtitle...")
                # Default case
                else:
                    self.status_signal.emit(f"⏬ Downloading...")
            except Exception as e:
                logger.error(f"Error extracting filename from line '{line}': {e}")
                self.status_signal.emit("⚡ Downloading...")  # Fallback status
            return  # Don't process this line further for speed/ETA

        # Check for specific download types in the output
        if "Downloading video" in line:
            self.status_signal.emit(f"⏬ Downloading video...")
            return

        elif "Downloading audio" in line:
            self.status_signal.emit(f"⏬ Downloading audio...")
            return

        # Detect subtitle file creation
        # Look for lines like "[info] Writing video subtitles to: filename.xx.vtt"
        subtitle_match = re.search(
            r"(?:Writing|Downloading) (?:video )?subtitles.*?(?:to|:)\s*(.+\.(?:vtt|srt))(?:\s|$)",
            line,
            re.IGNORECASE,
        )
        if subtitle_match:
            subtitle_file = subtitle_match.group(1).strip()
            
            # Clean up the path - remove any duplicated directory paths
            # Sometimes yt-dlp output contains malformed paths like "dir: dir/file"
            if ":" in subtitle_file and os.name == 'nt':  # Windows paths
                # Look for pattern like "C:\path: C:\path\file" and extract the latter
                colon_parts = subtitle_file.split(": ")
                if len(colon_parts) > 1:
                    # Take the last part which should be the actual file path
                    subtitle_file = colon_parts[-1].strip()
            
            # Show subtitle download message
            self.status_signal.emit(f"⏬ Downloading subtitle...")
            # Store the subtitle file path for later deletion if merging is enabled
            if self.merge_subs:
                subtitle_path = Path(subtitle_file)
                if not subtitle_path.is_absolute():
                    # If it's a relative path, make it absolute based on current path
                    subtitle_path = self.path.joinpath(subtitle_file)
                self.subtitle_files.append(str(subtitle_path))
                logger.debug(f"Tracking subtitle file for later cleanup: {subtitle_path}")
            return

        # Send status updates based on output line content
        if "Downloading webpage" in line or "Extracting URL" in line:
            self.status_signal.emit("🔍 Fetching video information...")
            self.progress_signal.emit(0)
        elif "Downloading API JSON" in line:
            self.status_signal.emit("📋 Processing playlist data...")
            self.progress_signal.emit(0)
        elif "Downloading m3u8 information" in line:
            self.status_signal.emit("🎯 Preparing video streams...")
            self.progress_signal.emit(0)
        elif "[download] Downloading video " in line:
            self.status_signal.emit("⏬ Downloading video...")
        elif "[download] Downloading audio " in line:
            self.status_signal.emit("⏬ Downloading audio...")
        elif "Downloading format" in line:
            # Try to detect if it's audio or video format
            if " - audio only" in line:
                self.status_signal.emit("⏬ Downloading audio...")
            elif " - video only" in line:
                self.status_signal.emit("⏬ Downloading video...")
            else:
                # Don't emit generic message - format is unclear
                pass

        # Look for download percentage
        percent_match = re.search(r"(\d+\.\d+)%", line)
        if percent_match:
            try:
                percent = float(percent_match.group(1))
                self.progress_signal.emit(percent)
            except (ValueError, IndexError):
                pass

        # Check for download speed and ETA
        if "[download]" in line and "%" in line:
            # Try to extract more detailed status info
            try:
                # Look for speed
                speed_match = re.search(r"at\s+(\d+\.\d+[KMG]iB/s)", line)
                speed_str = speed_match.group(1) if speed_match else "N/A"

                # Look for ETA
                eta_match = re.search(r"ETA\s+(\d+:\d+)", line)
                eta_str = eta_match.group(1) if eta_match else "N/A"

                # Simplify status message to only show the speed and ETA
                status = f"Speed: {speed_str} | ETA: {eta_str}"
                self.update_details.emit(status)
            except Exception as e:
                # If parsing fails, just show basic status (maybe log the error)
                logger.error(f"Error parsing download details line: {line} -> {e}")
                pass  # Keep basic status emission below if needed, or emit generic details

        # Check for post-processing
        if "[Merger]" in line or "Merging formats" in line:
            self.status_signal.emit("✨ Post-processing: Merging formats...")
            self.progress_signal.emit(95)
        elif "SponsorBlock" in line:
            self.status_signal.emit("✨ Post-processing: Removing sponsor segments...")
            self.progress_signal.emit(97)
        elif "Deleting original file" in line:
            self.progress_signal.emit(98)
        elif "has already been downloaded" in line:
            # File already exists - extract filename
            match = re.search(r"(.*?) has already been downloaded", line)
            if match:
                filename = Path(match.group(1)).name
                # Determine file type based on extension for existing file message
                ext = Path(filename).suffix.lower()

                if ext in [".mp4", ".webm", ".mkv", ".avi", ".mov", ".flv"]:
                    self.status_signal.emit(f"⚠️ Video file already exists")
                elif ext in [".mp3", ".m4a", ".aac", ".wav", ".ogg", ".opus", ".flac"]:
                    self.status_signal.emit(f"⚠️ Audio file already exists")
                elif ext in [".vtt", ".srt", ".ass", ".ssa"]:
                    self.status_signal.emit(f"⚠️ Subtitle file already exists")
                else:
                    self.status_signal.emit(f"⚠️ File already exists")

                self.file_exists_signal.emit(filename)
            else:
                logger.info(f"Could not extract filename from 'already downloaded' line: {line}")
                self.status_signal.emit("⚠️ File already exists")  # Fallback status
        elif "Finished downloading" in line:
            self.progress_signal.emit(100)

            # Show completion message based on file type
            if self.current_filename:
                ext = Path(self.current_filename).suffix.lower()

                # Video file extensions
                if ext in [".mp4", ".webm", ".mkv", ".avi", ".mov", ".flv"]:
                    self.status_signal.emit(f"✅ Video download completed!")
                # Audio file extensions
                elif ext in [".mp3", ".m4a", ".aac", ".wav", ".ogg", ".opus", ".flac"]:
                    self.status_signal.emit(f"✅ Audio download completed!")
                # Subtitle file extensions
                elif ext in [".vtt", ".srt", ".ass", ".ssa"]:
                    self.status_signal.emit(f"✅ Subtitle download completed!")
                # Default case
                else:
                    self.status_signal.emit("✅ Download completed!")
            else:
                self.status_signal.emit("✅ Download completed!")

            self.update_details.emit("")  # Clear details label on completion

    def _run_python_api(self) -> None:
        """Original download method using Python API - kept for reference."""
        # The existing run method code using yt_dlp.YoutubeDL starts here
        # This method is no longer used by default

    def pause(self) -> None:
        self.paused = True

    def resume(self) -> None:
        self.paused = False

    def cancel(self) -> None:
        self.cancelled = True
        # Terminate the subprocess if it's running
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass
