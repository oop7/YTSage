"""
History Manager Module
======================

This module provides **thread-safe** centralized management for download
history in YTSage. It handles reading, writing, and managing download history
stored in a JSON file.

Thread safety is ensured using a reentrant lock (`RLock`), so multiple threads
can safely access or modify history concurrently.

Features
--------
- Thread-safe operations for getting, adding, and removing history entries.
- Loads history from a JSON file (`APP_HISTORY_FILE`).
- Creates the history file if missing or corrupt.
- Manages download history with metadata including thumbnails, file paths, and download options.
- Provides safe error handling with logging instead of raising exceptions.
- Persists updates back to disk automatically.

Usage
-----
from src.utils.ytsage_history_manager import HistoryManager

# Add a download to history
HistoryManager.add_entry(
    title="Video Title",
    url="https://youtube.com/watch?v=...",
    thumbnail_url="https://...",
    file_path="/path/to/file.mp4",
    format_id="137+140",
    is_audio_only=False,
    resolution="1080p",
    download_options={...}
)

# Get all history entries
history = HistoryManager.get_all_entries()

# Remove an entry
HistoryManager.remove_entry(entry_id)

# Clear all history
HistoryManager.clear_history()

Design Notes
------------
- History entries are stored in `HistoryManager._history` (a list of dicts).
- Each entry has a unique ID based on timestamp.
- All modifications trigger a save (`_save`) to keep JSON in sync.
- Logs actions and errors using the app's central logger.
- Uses `RLock` to allow safe concurrent access from multiple threads.

Exceptions
----------
- Any issues during file I/O (permissions, disk errors, JSON corruption)
  are caught and logged. The application continues running with an empty
  history when possible.
"""

import json
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.utils.ytsage_constants import APP_HISTORY_FILE
from src.utils.ytsage_logger import logger


class HistoryManager:
    """
    Thread-safe history manager for YTSage.

    Provides methods to load, save, get, add, and remove download history entries.
    Automatically persists changes to disk.
    """

    _lock = threading.RLock()
    _history_file = APP_HISTORY_FILE
    _history: List[Dict[str, Any]] = []
    _loaded = False

    @classmethod
    def _load(cls) -> None:
        """
        Loads download history from a JSON file if it exists and is valid.
        If the file is missing or corrupt, initializes with an empty history.
        Logs actions and errors during the process.
        """
        with cls._lock:
            if cls._history_file.exists():
                try:
                    with open(cls._history_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # Ensure it's a list
                        if isinstance(data, list):
                            cls._history = data
                        else:
                            cls._history = []
                            logger.warning("History file format invalid, initialized empty history.")
                    logger.info(f"History loaded from file: {len(cls._history)} entries.")
                except json.JSONDecodeError:
                    cls._history = []
                    logger.warning("History file corrupt, initialized empty history.")
                except Exception as e:
                    cls._history = []
                    logger.error(f"Error loading history file: {e}")
            else:
                cls._history = []
                cls._save()
                logger.info("History file not found, created empty history.")
            cls._loaded = True

    @classmethod
    def _save(cls) -> None:
        """
        Save current history to JSON file.

        Note:
            May raise exceptions if the file cannot be written due to permission issues,
            disk errors, or other I/O problems.
        """
        with cls._lock:
            try:
                # Ensure parent directory exists
                cls._history_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(cls._history_file, "w", encoding="utf-8") as f:
                    json.dump(cls._history, f, indent=2, ensure_ascii=False)
                logger.debug(f"History saved to file: {len(cls._history)} entries.")
            except (OSError, PermissionError) as e:
                logger.exception(f"Failed to save history: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error while saving history: {e}")

    @classmethod
    def _ensure_loaded(cls) -> None:
        """Ensure history is loaded before any operation."""
        with cls._lock:
            if not cls._loaded:
                cls._load()

    @classmethod
    def add_entry(
        cls,
        title: str,
        url: str,
        thumbnail_url: Optional[str],
        file_path: str,
        format_id: str,
        is_audio_only: bool,
        resolution: str,
        file_size: Optional[int] = None,
        channel: Optional[str] = None,
        duration: Optional[str] = None,
        download_options: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Add a new download entry to history.

        Args:
            title: Video/audio title
            url: Original URL
            thumbnail_url: Thumbnail URL (can be None)
            file_path: Path to downloaded file
            format_id: Format ID used for download
            is_audio_only: Whether it's audio-only download
            resolution: Resolution string (e.g., "1080p", "best audio")
            file_size: File size in bytes (optional)
            channel: Channel name (optional)
            duration: Duration string (optional)
            download_options: Dictionary of all download options used (optional)

        Returns:
            str: The unique ID of the created entry
        """
        cls._ensure_loaded()
        
        with cls._lock:
            # Generate unique ID based on timestamp
            entry_id = f"{int(time.time() * 1000)}"
            
            # Get file size if not provided
            if file_size is None:
                try:
                    file_path_obj = Path(file_path)
                    if file_path_obj.exists():
                        file_size = file_path_obj.stat().st_size
                except Exception as e:
                    logger.debug(f"Could not get file size: {e}")
                    file_size = 0
            
            entry = {
                "id": entry_id,
                "title": title,
                "url": url,
                "thumbnail_url": thumbnail_url,
                "file_path": file_path,
                "download_date": datetime.now().isoformat(),
                "format_id": format_id,
                "is_audio_only": is_audio_only,
                "resolution": resolution,
                "file_size": file_size or 0,
                "channel": channel,
                "duration": duration,
                "download_options": download_options or {},
            }
            
            # Add to beginning of list (most recent first)
            cls._history.insert(0, entry)
            cls._save()
            
            logger.info(f"Added entry to history: {title}")
            return entry_id

    @classmethod
    def get_all_entries(cls, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all history entries.

        Args:
            limit: Optional limit on number of entries to return (most recent first)

        Returns:
            List of history entry dictionaries
        """
        cls._ensure_loaded()
        
        with cls._lock:
            if limit is not None:
                return cls._history[:limit]
            return cls._history.copy()

    @classmethod
    def get_entry(cls, entry_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific history entry by ID.

        Args:
            entry_id: The unique entry ID

        Returns:
            Entry dictionary or None if not found
        """
        cls._ensure_loaded()
        
        with cls._lock:
            for entry in cls._history:
                if entry.get("id") == entry_id:
                    return entry.copy()
            return None

    @classmethod
    def remove_entry(cls, entry_id: str) -> bool:
        """
        Remove a specific entry from history.

        Args:
            entry_id: The unique entry ID to remove

        Returns:
            bool: True if entry was found and removed, False otherwise
        """
        cls._ensure_loaded()
        
        with cls._lock:
            for i, entry in enumerate(cls._history):
                if entry.get("id") == entry_id:
                    removed = cls._history.pop(i)
                    cls._save()
                    logger.info(f"Removed entry from history: {removed.get('title', 'Unknown')}")
                    return True
            
            logger.debug(f"Entry ID '{entry_id}' not found in history.")
            return False

    @classmethod
    def clear_history(cls) -> int:
        """
        Clear all history entries.

        Returns:
            int: Number of entries that were cleared
        """
        cls._ensure_loaded()
        
        with cls._lock:
            count = len(cls._history)
            cls._history = []
            cls._save()
            logger.info(f"Cleared all history: {count} entries removed.")
            return count

    @classmethod
    def search_entries(cls, query: str) -> List[Dict[str, Any]]:
        """
        Search history entries by title, channel, or URL.

        Args:
            query: Search query string

        Returns:
            List of matching history entries
        """
        cls._ensure_loaded()
        
        if not query:
            return cls.get_all_entries()
        
        query_lower = query.lower()
        
        with cls._lock:
            results = []
            for entry in cls._history:
                # Search in title, channel, and URL
                title = (entry.get("title") or "").lower()
                channel = (entry.get("channel") or "").lower()
                url = (entry.get("url") or "").lower()
                
                if query_lower in title or query_lower in channel or query_lower in url:
                    results.append(entry.copy())
            
            return results

    @classmethod
    def get_statistics(cls) -> Dict[str, Any]:
        """
        Get statistics about download history.

        Returns:
            Dictionary with statistics (total_downloads, total_size, etc.)
        """
        cls._ensure_loaded()
        
        with cls._lock:
            total_downloads = len(cls._history)
            total_size = sum(entry.get("file_size", 0) for entry in cls._history)
            video_count = sum(1 for entry in cls._history if not entry.get("is_audio_only", False))
            audio_count = sum(1 for entry in cls._history if entry.get("is_audio_only", False))
            
            return {
                "total_downloads": total_downloads,
                "total_size": total_size,
                "video_count": video_count,
                "audio_count": audio_count,
            }
