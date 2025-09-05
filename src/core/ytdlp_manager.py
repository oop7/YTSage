"""
YTDLPManager - A unified abstraction layer for yt-dlp interactions.

This module provides a clean interface for all yt-dlp operations using only
the external binary via subprocess, ensuring consistent behavior across
development and production environments.
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from src.core.ytsage_logging import logger
from src.utils.ytsage_constants import SUBPROCESS_CREATIONFLAGS


class YTDLPManager:
    """
    Unified manager for all yt-dlp interactions using external binary only.
    
    This class provides a clean abstraction layer that handles all yt-dlp
    operations via subprocess, using --dump-json for structured data retrieval.
    """
    
    def __init__(self, ytdlp_path: Union[str, Path] = "yt-dlp"):
        """
        Initialize the YTDLPManager with the path to yt-dlp binary.
        
        Args:
            ytdlp_path: Path to the yt-dlp executable
        """
        self.ytdlp_path = str(ytdlp_path)
        logger.debug(f"YTDLPManager initialized with path: {self.ytdlp_path}")
    
    def _run_command(self, args: List[str], timeout: int = 30) -> Tuple[int, str, str]:
        """
        Execute a yt-dlp command and return the result.
        
        Args:
            args: Command arguments to pass to yt-dlp
            timeout: Command timeout in seconds
            
        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        cmd = [self.ytdlp_path] + args
        logger.debug(f"Executing command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=SUBPROCESS_CREATIONFLAGS
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout} seconds")
            return -1, "", f"Command timed out after {timeout} seconds"
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return -1, "", str(e)
    
    def get_version(self) -> Optional[str]:
        """
        Get the yt-dlp version.
        
        Returns:
            Version string or None if failed
        """
        return_code, stdout, stderr = self._run_command(["--version"])
        if return_code == 0:
            return stdout.strip()
        logger.error(f"Failed to get version: {stderr}")
        return None
    
    def check_availability(self) -> bool:
        """
        Check if yt-dlp is available and working.
        
        Returns:
            True if yt-dlp is working, False otherwise
        """
        # First check if the path exists (for file paths)
        if self.ytdlp_path != "yt-dlp":
            ytdlp_file = Path(self.ytdlp_path)
            if not ytdlp_file.exists():
                logger.debug(f"yt-dlp binary not found at: {self.ytdlp_path}")
                return False
        
        # Then check if it responds to --version
        version = self.get_version()
        return version is not None
    
    def extract_info(self, url: str, extract_flat: bool = False, 
                    playlist_items: Optional[str] = None,
                    cookies_file: Optional[str] = None,
                    browser_cookies: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Extract video/playlist information using --dump-json.
        
        Args:
            url: Video or playlist URL
            extract_flat: Whether to extract playlist items without metadata
            playlist_items: Specific playlist items to extract (e.g., "1-10")
            cookies_file: Path to cookies file
            browser_cookies: Browser to extract cookies from (e.g., "firefox")
            
        Returns:
            Extracted information as dictionary or None if failed
        """
        args = [
            "--dump-json",
            "--no-warnings",
            "--skip-download"
        ]
        
        if extract_flat:
            args.append("--flat-playlist")
        
        if playlist_items:
            args.extend(["--playlist-items", playlist_items])
            
        if cookies_file:
            args.extend(["--cookies", cookies_file])
        elif browser_cookies:
            args.extend(["--cookies-from-browser", browser_cookies])
        
        args.append(url)
        
        return_code, stdout, stderr = self._run_command(args, timeout=60)
        
        if return_code != 0:
            logger.error(f"Failed to extract info for {url}: {stderr}")
            return None
        
        try:
            # For playlists, yt-dlp outputs multiple JSON objects, one per line
            lines = stdout.strip().split('\n')
            if len(lines) == 1:
                # Single video
                return json.loads(lines[0])
            else:
                # Playlist - return the first entry which contains playlist metadata
                # and collect all entries
                playlist_info = json.loads(lines[0])
                entries = []
                for line in lines:
                    if line.strip():
                        entry = json.loads(line)
                        entries.append(entry)
                
                # If it's a playlist, the first entry usually contains the playlist info
                if playlist_info.get('_type') == 'playlist':
                    playlist_info['entries'] = entries[1:]  # Exclude the playlist info entry itself
                    return playlist_info
                else:
                    # Multiple videos but not a playlist
                    return {'entries': entries, '_type': 'multi_video'}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON output: {e}")
            return None
    
    def get_formats(self, url: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get available formats for a video.
        
        Args:
            url: Video URL
            
        Returns:
            List of format dictionaries or None if failed
        """
        info = self.extract_info(url)
        if info and 'formats' in info:
            return info['formats']
        return None
    
    def get_subtitles(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Get available subtitles for a video.
        
        Args:
            url: Video URL
            
        Returns:
            Dictionary of available subtitles or None if failed
        """
        info = self.extract_info(url)
        if info:
            return {
                'subtitles': info.get('subtitles', {}),
                'automatic_captions': info.get('automatic_captions', {})
            }
        return None
    
    def get_thumbnail_info(self, url: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get thumbnail information for a video.
        
        Args:
            url: Video URL
            
        Returns:
            List of thumbnail dictionaries or None if failed
        """
        info = self.extract_info(url)
        if info and 'thumbnails' in info:
            return info['thumbnails']
        return None
    
    def download_thumbnail(self, url: str, output_path: Optional[Path] = None) -> Optional[Path]:
        """
        Download the best quality thumbnail for a video.
        
        Args:
            url: Video URL
            output_path: Optional output path, uses temp file if not provided
            
        Returns:
            Path to downloaded thumbnail or None if failed
        """
        args = [
            "--write-thumbnail",
            "--skip-download",
            "--no-warnings"
        ]
        
        if output_path:
            output_dir = output_path.parent
            output_template = output_path.stem + ".%(ext)s"
            args.extend(["-o", str(output_dir / output_template)])
        else:
            # Use temporary directory
            temp_dir = tempfile.mkdtemp()
            args.extend(["-o", f"{temp_dir}/thumbnail.%(ext)s"])
        
        args.append(url)
        
        return_code, stdout, stderr = self._run_command(args, timeout=30)
        
        if return_code == 0:
            if output_path:
                # Find the actual downloaded file
                for ext in ['jpg', 'jpeg', 'png', 'webp']:
                    potential_path = output_path.parent / f"{output_path.stem}.{ext}"
                    if potential_path.exists():
                        return potential_path
            else:
                # Find the downloaded file in temp directory
                temp_path = Path(temp_dir)
                for file in temp_path.glob("thumbnail.*"):
                    return file
        
        logger.error(f"Failed to download thumbnail: {stderr}")
        return None
    
    def update_binary(self) -> bool:
        """
        Update the yt-dlp binary to the latest version.
        This method is deprecated - use the update_yt_dlp() function instead.
        
        Returns:
            True if update succeeded, False otherwise
        """
        logger.warning("YTDLPManager.update_binary() is deprecated, use update_yt_dlp() function instead")
        
        # Import here to avoid circular imports
        from src.core.ytsage_utils import update_yt_dlp
        
        return update_yt_dlp()
    
    def build_download_command(self, url: str, **options) -> List[str]:
        """
        Build a complete yt-dlp download command with options.
        
        Args:
            url: Video URL
            **options: Various download options
            
        Returns:
            Complete command as list of strings
        """
        cmd = [self.ytdlp_path]
        
        # Format selection
        if options.get('format_id'):
            format_id = options['format_id']
            # Strip the -drc suffix if present
            clean_format_id = format_id.split("-drc")[0] if "-drc" in format_id else format_id
            
            # Check if it's audio-only format by analyzing the format
            info = self.extract_info(url)
            is_audio_format = False
            if info and 'formats' in info:
                for fmt in info['formats']:
                    if fmt.get('format_id') == clean_format_id:
                        if fmt.get('vcodec') == 'none' or 'audio only' in fmt.get('format_note', '').lower():
                            is_audio_format = True
                        break
            
            if is_audio_format:
                cmd.extend(["-f", clean_format_id])
            else:
                cmd.extend(["-f", f"{clean_format_id}+bestaudio/best"])
                
                # Determine merge output format
                if info and 'formats' in info:
                    for fmt in info['formats']:
                        if fmt.get('format_id') == clean_format_id:
                            format_ext = fmt.get('ext')
                            if format_ext:
                                cmd.extend(["--merge-output-format", format_ext])
                            break
        elif options.get('resolution'):
            res_value = options['resolution']
            cmd.extend(["-S", f"res:{res_value}"])
        
        # Output template
        output_path = options.get('output_path', Path.cwd())
        if options.get('is_playlist'):
            template = output_path / "%(playlist_title)s/%(title)s_%(resolution)s.%(ext)s"
        else:
            template = output_path / "%(title)s_%(resolution)s.%(ext)s"
        
        cmd.extend(["-o", str(template)])
        
        # Common options
        cmd.append("--force-overwrites")
        
        # Playlist options
        if options.get('playlist_items'):
            cmd.extend(["--playlist-items", options['playlist_items']])
        
        # Subtitle options
        if options.get('subtitle_langs'):
            cmd.append("--write-subs")
            lang_codes = []
            for sub_selection in options['subtitle_langs']:
                lang_code = sub_selection.split(" - ")[0]
                lang_codes.append(lang_code)
            
            if lang_codes:
                cmd.extend(["--sub-langs", ",".join(lang_codes)])
                cmd.append("--write-auto-subs")
                
                if options.get('merge_subs'):
                    cmd.append("--embed-subs")
        
        # SponsorBlock
        if options.get('enable_sponsorblock') and options.get('sponsorblock_categories'):
            cmd.append("--sponsorblock-remove")
            cmd.append(",".join(options['sponsorblock_categories']))
        
        # Additional options
        if options.get('save_description'):
            cmd.append("--write-description")
        
        if options.get('embed_chapters'):
            cmd.append("--embed-chapters")
        
        if options.get('cookie_file'):
            cmd.extend(["--cookies", str(options['cookie_file'])])
        elif options.get('browser_cookies'):
            cmd.extend(["--cookies-from-browser", options['browser_cookies']])
        
        if options.get('rate_limit'):
            cmd.extend(["-r", options['rate_limit']])
        
        if options.get('download_section'):
            cmd.extend(["--download-sections", options['download_section']])
            if options.get('force_keyframes'):
                cmd.append("--force-keyframes-at-cuts")
        
        # Add URL as final argument
        cmd.append(url)
        
        return cmd


# Global instance for backward compatibility
_ytdlp_manager = None


def get_ytdlp_manager(ytdlp_path: Union[str, Path] = "yt-dlp") -> YTDLPManager:
    """
    Get or create a global YTDLPManager instance.
    
    Args:
        ytdlp_path: Path to yt-dlp executable
        
    Returns:
        YTDLPManager instance
    """
    global _ytdlp_manager
    if _ytdlp_manager is None or _ytdlp_manager.ytdlp_path != str(ytdlp_path):
        _ytdlp_manager = YTDLPManager(ytdlp_path)
    return _ytdlp_manager
