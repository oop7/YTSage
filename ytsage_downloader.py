from PySide6.QtCore import QThread, Signal, QObject, QProcess, QTimer
import yt_dlp # Keep yt_dlp import here - only downloader uses it.
import time
import os
import re
import subprocess # For direct CLI command execution
import shlex # For safely parsing command arguments
import sys  # Added to get executable path information
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
    update_details = Signal(str) # New signal for filename, speed, ETA

    def __init__(self, url, path, format_id, subtitle_langs=None, is_playlist=False, merge_subs=False, enable_sponsorblock=False, resolution='', playlist_items=None, save_description=False, cookie_file=None, rate_limit=None, download_section=None, force_keyframes=False):
        super().__init__()
        self.url = url
        self.path = path
        self.format_id = format_id
        self.subtitle_langs = subtitle_langs if subtitle_langs else []
        self.is_playlist = is_playlist
        self.merge_subs = merge_subs
        self.enable_sponsorblock = enable_sponsorblock
        self.resolution = resolution
        self.playlist_items = playlist_items
        self.save_description = save_description
        self.cookie_file = cookie_file
        self.rate_limit = rate_limit
        self.download_section = download_section
        self.force_keyframes = force_keyframes
        self.paused = False
        self.cancelled = False
        self.process = None
        self.use_direct_command = True  # Flag to use direct CLI command instead of Python API
        self.last_output_time = time.time()
        self.timeout_timer = None
        self.current_filename = None # Initialize filename storage
        self.last_file_path = None # Initialize full file path storage
        self.subtitle_files = [] # Track subtitle files that are created
        self.initial_subtitle_files = set() # Track initial subtitle files before download

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

    def cleanup_subtitle_files(self):
        """Delete subtitle files after they have been merged into the video file"""
        if not self.merge_subs:
            return  # Only cleanup if merge_subs is enabled
        
        try:
            deleted_count = 0
            
            # Method 1: Delete tracked subtitle files from output messages
            if self.subtitle_files:
                for subtitle_file in self.subtitle_files:
                    try:
                        if os.path.isfile(subtitle_file):
                            os.remove(subtitle_file)
                            deleted_count += 1
                            print(f"DEBUG: Deleted tracked subtitle file: {os.path.basename(subtitle_file)}")
                    except Exception as e:
                        print(f"Error deleting subtitle file {subtitle_file}: {str(e)}")
                
                print(f"DEBUG: Deleted {deleted_count} of {len(self.subtitle_files)} tracked subtitle files")
            
            # Method 2: Find newly created subtitle files by comparing with initial set
            try:
                new_subtitle_files = set()
                for root, dirs, files in os.walk(self.path):
                    for file in files:
                        if file.endswith('.vtt') or file.endswith('.srt'):
                            full_path = os.path.join(root, file)
                            if full_path not in self.initial_subtitle_files:
                                new_subtitle_files.add(full_path)
                
                if new_subtitle_files:
                    print(f"DEBUG: Found {len(new_subtitle_files)} new subtitle files to delete")
                    for subtitle_file in new_subtitle_files:
                        try:
                            if os.path.isfile(subtitle_file):
                                os.remove(subtitle_file)
                                deleted_count += 1
                                print(f"DEBUG: Deleted new subtitle file: {os.path.basename(subtitle_file)}")
                        except Exception as e:
                            print(f"Error deleting new subtitle file {subtitle_file}: {str(e)}")
            except Exception as e:
                print(f"Error in finding new subtitle files: {str(e)}")
                
            # Method 3: As a last resort, use timestamp-based approach for recently created files
            if self.last_file_path and deleted_count == 0:
                target_dir = os.path.dirname(self.last_file_path)
                
                # Look for subtitle files created in last 5 minutes
                now = time.time()
                for filename in os.listdir(target_dir):
                    if filename.endswith('.vtt') or filename.endswith('.srt'):
                        file_path = os.path.join(target_dir, filename)
                        
                        # Check if it was created in the last 5 minutes
                        file_time = os.path.getctime(file_path)
                        if now - file_time < 300:  # 5 minutes
                            try:
                                os.remove(file_path)
                                deleted_count += 1
                                print(f"DEBUG: Deleted subtitle file by timestamp: {filename}")
                            except Exception as e:
                                print(f"Error deleting subtitle file {filename}: {str(e)}")
            
            print(f"DEBUG: Total subtitle files deleted: {deleted_count}")
                                
        except Exception as e:
            print(f"Error cleaning subtitle files: {str(e)}")

    def check_file_exists(self):
        """Check if the file already exists before downloading"""
        try:
            print("DEBUG: Starting file existence check")
            # Use yt-dlp to get the filename without downloading, suppressing warnings
            ydl_opts_check = {
                'quiet': True, 
                'skip_download': True,
                'no_warnings': True, # <-- Suppress warnings during check
                'ignoreerrors': True, # Also ignore other potential errors during this check
                'outtmpl': {'default': os.path.join(self.path, '%(title)s.%(ext)s')},
                'format': self.format_id if self.format_id else 'best' # Use selected format or best
            }
            if self.cookie_file:
                ydl_opts_check['cookiefile'] = self.cookie_file

            with yt_dlp.YoutubeDL(ydl_opts_check) as ydl:
                info = ydl.extract_info(self.url, download=False)
                
                # Handle cases where info extraction fails silently
                if not info:
                    print("DEBUG: Failed to extract info during file existence check. Skipping check.")
                    return False # Proceed with download attempt

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

    def _build_yt_dlp_command(self):
        """Build the yt-dlp command line with all options for direct execution."""
        # Use bundled yt-dlp executable instead of system PATH
        # Determine if we're running from a PyInstaller bundle
        if getattr(sys, 'frozen', False):
            # We're running from a PyInstaller bundle
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
            yt_dlp_path = os.path.join(base_path, "yt-dlp.exe" if os.name == 'nt' else "yt-dlp")
            if os.path.exists(yt_dlp_path):
                cmd = [yt_dlp_path]
                print(f"DEBUG: Using bundled yt-dlp from: {yt_dlp_path}")
                
                # Check if the bundled executable is actually executable
                if not os.access(yt_dlp_path, os.X_OK) and os.name != 'nt':  # Skip check on Windows
                    print(f"WARNING: Bundled yt-dlp exists but is not executable: {yt_dlp_path}")
                    try:
                        # Try to make it executable
                        os.chmod(yt_dlp_path, 0o755)
                        print(f"Fixed permissions on bundled yt-dlp")
                    except Exception as e:
                        print(f"Failed to fix permissions: {e}")
            else:
                # Fall back to regular command if bundled version not found
                cmd = ["yt-dlp"]
                print(f"DEBUG: Bundled yt-dlp not found at {yt_dlp_path}, using system PATH")
        else:
            # We're running from source, use system PATH
            cmd = ["yt-dlp"]
            print("DEBUG: Using system PATH for yt-dlp")
        
        # Format selection strategy - use format ID if provided or fallback to resolution
        if self.format_id:
            # Strip the -drc suffix if present to fix issues with certain audio formats
            clean_format_id = self.format_id.split('-drc')[0] if '-drc' in self.format_id else self.format_id
            
            # Check if this is an audio-only format
            is_audio_format = False
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'skip_download': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(self.url, download=False)
                    for fmt in info.get('formats', []):
                        if fmt.get('format_id') == clean_format_id:
                            if fmt.get('vcodec') == 'none' or 'audio only' in fmt.get('format_note', '').lower():
                                is_audio_format = True
                                print(f"DEBUG: Detected audio-only format for ID: {clean_format_id}")
                            break
            except Exception as e:
                print(f"DEBUG: Error checking if format is audio-only: {e}")
            
            # For audio-only formats, don't try to merge with video
            if is_audio_format:
                cmd.extend(["-f", clean_format_id])
                print(f"DEBUG: Using audio-only format selection: {clean_format_id}")
            else:
                cmd.extend(["-f", f"{clean_format_id}+bestaudio/best"])
                print(f"DEBUG: Using video format selection with audio: {clean_format_id}+bestaudio/best")
            
            # Determine output format based on the selected format ID - only for video formats
            if not is_audio_format:
                try:
                    format_ext = None
                    print(f"DEBUG: Getting format information for format ID: {self.format_id} (using: {clean_format_id})")
                    ydl_opts = {
                        'quiet': True,
                        'no_warnings': True,
                        'skip_download': True,
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(self.url, download=False)
                        # Look for the clean format ID first
                        for fmt in info.get('formats', []):
                            if fmt.get('format_id') == clean_format_id:
                                format_ext = fmt.get('ext')
                                break
                        # If not found, try the original ID as fallback
                        if not format_ext:
                            for fmt in info.get('formats', []):
                                if fmt.get('format_id') == self.format_id:
                                    format_ext = fmt.get('ext')
                                    break
                    
                    if format_ext:
                        print(f"DEBUG: Detected format extension: {format_ext}")
                        # Ensure output matches the selected format - only for video formats
                        cmd.extend(["--merge-output-format", format_ext])
                except Exception as e:
                    print(f"DEBUG: Error detecting format extension: {e}")
                    # If we can't determine the format, don't specify merge-output-format
                    pass
        else:
            # If no specific format ID, use resolution-based sorting (-S)
            res_value = self.resolution if self.resolution else "720"  # Default to 720p if no resolution specified
            cmd.extend(["-S", f"res:{res_value}"])
        
        # Output template with resolution in filename
        output_template = os.path.join(self.path, '%(title)s_%(resolution)s.%(ext)s')
        
        # Handle playlist directory creation if needed
        if self.is_playlist:
            # Create output template with playlist subfolder
            output_template = os.path.join(self.path, '%(playlist_title)s/%(title)s_%(resolution)s.%(ext)s')
        
        cmd.extend(["-o", output_template])
        
        # Add common options
        cmd.append("--force-overwrites")
        
        # Add playlist items if specified
        if self.is_playlist and self.playlist_items:
            cmd.extend(["--playlist-items", self.playlist_items])
        
        # Add subtitle options if selected
        if self.subtitle_langs:
            # Subtitles work with both audio-only and video formats
            # For audio-only formats, subtitles will be downloaded as separate files
            cmd.append("--write-subs")
            
            # Get language codes from subtitle selections
            lang_codes = []
            for sub_selection in self.subtitle_langs:
                try:
                    # Extract just the language code (e.g., 'en' from 'en - Manual')
                    lang_code = sub_selection.split(' - ')[0]
                    lang_codes.append(lang_code)
                except Exception as e:
                    print(f"Warning: Could not parse subtitle selection '{sub_selection}': {e}")
            
            if lang_codes:
                cmd.extend(["--sub-langs", ",".join(lang_codes)])
                cmd.append("--write-auto-subs")  # Include auto-generated subtitles
                
                # Add embedding if requested - only applies to video formats
                if self.merge_subs:
                    cmd.append("--embed-subs")
        
        # Add SponsorBlock if enabled
        if self.enable_sponsorblock:
            cmd.append("--sponsorblock-remove")
            cmd.append("sponsor")
        
        # Add description saving if enabled
        if self.save_description:
            cmd.append("--write-description")
        
        # Add cookies if specified
        if self.cookie_file:
            cmd.extend(["--cookies", self.cookie_file])
        
        # Add rate limit if specified
        if self.rate_limit:
            cmd.extend(["-r", self.rate_limit])
        
        # Add download section if specified
        if self.download_section:
            cmd.extend(["--download-sections", self.download_section])
            
            # Add force keyframes option if enabled
            if self.force_keyframes:
                cmd.append("--force-keyframes-at-cuts")
                
            print(f"DEBUG: Added download section: {self.download_section}, Force keyframes: {self.force_keyframes}")
        
        # Add the URL as the final argument
        cmd.append(self.url)
        
        return cmd
    
    def run(self):
        try:
            print("DEBUG: Starting download thread")
            
            # First check if file already exists using original method
            existing_file = self.check_file_exists()
            if existing_file:
                print(f"DEBUG: File exists, emitting signal: {existing_file}")
                self.file_exists_signal.emit(existing_file)
                return
            
            print("DEBUG: No existing file found, proceeding with download")
            
            # Get initial list of subtitle files to compare later
            self.initial_subtitle_files = set()
            if self.merge_subs:
                try:
                    # Scan for existing subtitle files in the directory
                    for root, dirs, files in os.walk(self.path):
                        for file in files:
                            if file.endswith('.vtt') or file.endswith('.srt'):
                                self.initial_subtitle_files.add(os.path.join(root, file))
                    print(f"DEBUG: Found {len(self.initial_subtitle_files)} existing subtitle files before download")
                except Exception as e:
                    print(f"Warning: Error scanning for initial subtitle files: {e}")
            
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
    
    def _run_direct_command(self):
        """Run yt-dlp as a direct command line process instead of using Python API."""
        try:
            cmd = self._build_yt_dlp_command()
            cmd_str = " ".join(shlex.quote(str(arg)) for arg in cmd)
            print(f"DEBUG: Executing command: {cmd_str}")
            
            self.status_signal.emit("🚀 Starting download...")
            self.progress_signal.emit(0)
            
            # Start the process
            # Add creationflags=subprocess.CREATE_NO_WINDOW to hide console on Windows
            creation_flags = 0
            if os.name == 'nt': # Only use flag on Windows
                creation_flags = subprocess.CREATE_NO_WINDOW
                
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True,
                creationflags=creation_flags # Add this flag
            )
            
            # Process output line by line to update progress
            for line in iter(self.process.stdout.readline, ''):
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
                self.error_signal.emit("Error: yt-dlp executable not found. This could be due to improper installation or a PATH issue.")
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
                        self.error_signal.emit(f"Download failed with return code {return_code}. This may be due to a conflict with multiple yt-dlp installations. Try uninstalling any system-installed yt-dlp (e.g. through snap or apt) and restart the application.")
                    else:
                        self.error_signal.emit(f"Download failed with return code {return_code}")
                    self.cleanup_partial_files()
                    
        except Exception as e:
            self.error_signal.emit(f"Error in direct command: {str(e)}")
            self.cleanup_partial_files()
    
    def _parse_output_line(self, line):
        """Parse yt-dlp command output to update progress and status."""
        line = line.strip()
        # print(f"yt-dlp: {line}")  # Log all output - OPTIONALLY UNCOMMENT FOR VERBOSE DEBUG
        
        # Extract filename when the destination line appears
        # Use a slightly more robust regex looking for the start of the line
        dest_match = re.search(r'^\[download\] Destination:\s*(.*)', line)
        if dest_match:
            try:
                filepath = dest_match.group(1).strip()
                self.current_filename = os.path.basename(filepath)
                self.last_file_path = filepath  # Store the full path for later cleanup
                print(f"DEBUG: Extracted filename: {self.current_filename}") # DEBUG
                
                # Check if this is an audio-only download by looking in the previous lines
                is_audio_download = False
                
                # Look for audio format indicators in the current line or preceding output
                # yt-dlp typically mentions format like "Downloading format 251 - audio only"
                if ' - audio only' in line:
                    is_audio_download = True
                # Check if the format ID is mentioned earlier in the line
                format_match = re.search(r'Downloading format (\d+)', line)
                if format_match:
                    format_id = format_match.group(1)
                    print(f"DEBUG: Detected format ID: {format_id}")
                    # Format IDs for audio typically have different patterns 
                    # (like 140, 251 for audio vs 137, 248 for video)
                    # This is just a heuristic since format IDs can vary
                    
                # Determine file type based on extension and context
                ext = os.path.splitext(self.current_filename)[1].lower()
                
                # Check if this is explicitly an audio stream download
                if is_audio_download or 'Downloading audio' in line:
                    self.status_signal.emit(f"⏬ Downloading audio...")
                # Video file extensions with likely video content
                elif ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.flv']:
                    self.status_signal.emit(f"⏬ Downloading video...")
                # Audio file extensions
                elif ext in ['.mp3', '.m4a', '.aac', '.wav', '.ogg', '.opus', '.flac']:
                    self.status_signal.emit(f"⏬ Downloading audio...")
                # Subtitle file extensions
                elif ext in ['.vtt', '.srt', '.ass', '.ssa']:
                    self.status_signal.emit(f"⏬ Downloading subtitle...")
                # Default case
                else:
                    self.status_signal.emit(f"⏬ Downloading...")
            except Exception as e:
                print(f"Error extracting filename from line '{line}': {e}")
                self.status_signal.emit("⚡ Downloading...") # Fallback status
            return # Don't process this line further for speed/ETA
        
        # Check for specific download types in the output
        if "Downloading video" in line:
            self.status_signal.emit(f"⏬ Downloading video...")
            return
        
        elif "Downloading audio" in line:
            self.status_signal.emit(f"⏬ Downloading audio...")
            return
            
        # Detect subtitle file creation
        # Look for lines like "[info] Writing video subtitles to: filename.xx.vtt"
        subtitle_match = re.search(r'(?:Writing|Downloading) (?:video )?subtitles.*?(?:to|:)\s*(.*\.(?:vtt|srt))', line, re.IGNORECASE)
        if subtitle_match:
            subtitle_file = subtitle_match.group(1).strip()
            # Show subtitle download message
            self.status_signal.emit(f"⏬ Downloading subtitle...")
            # Store the subtitle file path for later deletion if merging is enabled
            if self.merge_subs:
                if not os.path.isabs(subtitle_file):
                    # If it's a relative path, make it absolute based on current path
                    subtitle_file = os.path.join(self.path, subtitle_file)
                self.subtitle_files.append(subtitle_file)
                print(f"DEBUG: Tracking subtitle file for later cleanup: {subtitle_file}")
            return
        
        # Send status updates based on output line content
        if 'Downloading webpage' in line or 'Extracting URL' in line:
            self.status_signal.emit("🔍 Fetching video information...")
            self.progress_signal.emit(0)
        elif 'Downloading API JSON' in line:
            self.status_signal.emit("📋 Processing playlist data...")
            self.progress_signal.emit(0)
        elif 'Downloading m3u8 information' in line:
            self.status_signal.emit("🎯 Preparing video streams...")
            self.progress_signal.emit(0)
        elif '[download] Downloading video ' in line:
            self.status_signal.emit("⏬ Downloading video...")
        elif '[download] Downloading audio ' in line:
            self.status_signal.emit("⏬ Downloading audio...")
        elif 'Downloading format' in line:
            # Try to detect if it's audio or video format
            if ' - audio only' in line:
                self.status_signal.emit("⏬ Downloading audio...")
            elif ' - video only' in line:
                self.status_signal.emit("⏬ Downloading video...")
            else:
                # Don't emit generic message - format is unclear
                pass
            
        # Look for download percentage
        percent_match = re.search(r'(\d+\.\d+)%', line)
        if percent_match:
            try:
                percent = float(percent_match.group(1))
                self.progress_signal.emit(percent)
            except (ValueError, IndexError):
                pass
                
        # Check for download speed and ETA
        if '[download]' in line and '%' in line:
            # Try to extract more detailed status info
            try:
                # Look for speed
                speed_match = re.search(r'at\s+(\d+\.\d+[KMG]iB/s)', line)
                speed_str = speed_match.group(1) if speed_match else "N/A"
                
                # Look for ETA
                eta_match = re.search(r'ETA\s+(\d+:\d+)', line)
                eta_str = eta_match.group(1) if eta_match else "N/A"
                
                # Simplify status message to only show the speed and ETA
                status = f"Speed: {speed_str} | ETA: {eta_str}"
                self.update_details.emit(status)
            except Exception as e:
                # If parsing fails, just show basic status (maybe log the error)
                print(f"Error parsing download details line: {line} -> {e}")
                pass # Keep basic status emission below if needed, or emit generic details
                
        # Check for post-processing
        if '[Merger]' in line or 'Merging formats' in line:
            self.status_signal.emit("✨ Post-processing: Merging formats...")
            self.progress_signal.emit(95)
        elif 'SponsorBlock' in line:
            self.status_signal.emit("✨ Post-processing: Removing sponsor segments...")
            self.progress_signal.emit(97)
        elif 'Deleting original file' in line:
            self.progress_signal.emit(98)
        elif 'has already been downloaded' in line:
            # File already exists - extract filename
            match = re.search(r'(.*?) has already been downloaded', line)
            if match:
                filename = os.path.basename(match.group(1))
                # Determine file type based on extension for existing file message
                ext = os.path.splitext(filename)[1].lower()
                
                if ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.flv']:
                    self.status_signal.emit(f"⚠️ Video file already exists")
                elif ext in ['.mp3', '.m4a', '.aac', '.wav', '.ogg', '.opus', '.flac']:
                    self.status_signal.emit(f"⚠️ Audio file already exists")
                elif ext in ['.vtt', '.srt', '.ass', '.ssa']:
                    self.status_signal.emit(f"⚠️ Subtitle file already exists")
                else:
                    self.status_signal.emit(f"⚠️ File already exists")
                
                self.file_exists_signal.emit(filename)
            else:
                print(f"Could not extract filename from 'already downloaded' line: {line}")
                self.status_signal.emit("⚠️ File already exists") # Fallback status
        elif 'Finished downloading' in line:
            self.progress_signal.emit(100)
            
            # Show completion message based on file type
            if self.current_filename:
                ext = os.path.splitext(self.current_filename)[1].lower()
                
                # Video file extensions
                if ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.flv']:
                    self.status_signal.emit(f"✅ Video download completed!")
                # Audio file extensions
                elif ext in ['.mp3', '.m4a', '.aac', '.wav', '.ogg', '.opus', '.flac']:
                    self.status_signal.emit(f"✅ Audio download completed!")
                # Subtitle file extensions
                elif ext in ['.vtt', '.srt', '.ass', '.ssa']:
                    self.status_signal.emit(f"✅ Subtitle download completed!")
                # Default case
                else:
                    self.status_signal.emit("✅ Download completed!")
            else:
                self.status_signal.emit("✅ Download completed!")
                
            self.update_details.emit("") # Clear details label on completion
    
    def _run_python_api(self):
        """Original download method using Python API - kept for reference."""
        # The existing run method code using yt_dlp.YoutubeDL starts here
        # This method is no longer used by default

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def cancel(self):
        self.cancelled = True
        # Terminate the subprocess if it's running
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass