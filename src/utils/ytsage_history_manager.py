"""
History Manager Module
======================

This module provides **thread-safe** centralized management for download
history in YTSage using SQLite for high performance and scalability.

Features
--------
- Scalable: Uses SQLite instead of parsing potentially large JSON files.
- Thread-safe: Handles database connections safely.
- Migration: Automatically migrates legacy JSON history to SQLite.
- CRUD: Create, Read, Delete, Clear operations for history entries.

Usage
-----
from src.utils.ytsage_history_manager import HistoryManager

# Add a download to history
HistoryManager.add_entry(...)

# Get all history entries
history = HistoryManager.get_all_entries()

# Get recent entries (limit + offset support planned)
# Remove an entry
HistoryManager.remove_entry(entry_id)

# Clear all history
HistoryManager.clear_history()
"""

import json
import sqlite3
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.utils.ytsage_constants import APP_HISTORY_FILE, APP_DATA_DIR
from src.utils.ytsage_logger import logger


class HistoryManager:
    """
    Thread-safe history manager for YTSage using SQLite.
    """

    _lock = threading.RLock()
    # Define DB file next to the old JSON file
    _db_file = APP_DATA_DIR / "ytsage_history.db"
    _connection = None
    _initialized = False

    @classmethod
    def _init_db(cls):
        """Initialize the database: create table and migrate if needed."""
        if cls._initialized:
            return

        with cls._lock:
            # Check if file exists to know if we need to migrate or just create schema
            db_exists = cls._db_file.exists()
            legacy_json_exists = APP_HISTORY_FILE.exists()

            try:
                # Ensure directory exists
                cls._db_file.parent.mkdir(parents=True, exist_ok=True)
                
                # We use a persistent connection to avoid churn
                if cls._connection is None:
                    cls._connection = sqlite3.connect(cls._db_file, check_same_thread=False)
                    cls._connection.row_factory = sqlite3.Row
                
                cursor = cls._connection.cursor()
                
                # Create table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS history (
                        id TEXT PRIMARY KEY,
                        title TEXT,
                        url TEXT,
                        channel TEXT,
                        file_path TEXT,
                        download_date TEXT,
                        file_size INTEGER,
                        thumbnail_url TEXT,
                        format_id TEXT,
                        resolution TEXT,
                        is_audio_only INTEGER,
                        duration TEXT,
                        options TEXT,
                        timestamp REAL
                    )
                """)
                
                # Index for faster sorting by date
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_timestamp 
                    ON history (timestamp DESC)
                """)
                
                # Indexes for faster search (title, channel, url)
                # This prevents full table scans during search
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON history (title)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_channel ON history (channel)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_url ON history (url)")
                
                cls._connection.commit()
            
                # If we just created the DB and have a JSON file, migrate
                if not db_exists and legacy_json_exists:
                    cls._migrate_legacy_json()
                
                cls._initialized = True
                
            except sqlite3.Error as e:
                logger.error(f"Failed to initialize history database: {e}")

    @classmethod
    def _migrate_legacy_json(cls):
        """Migrate legacy JSON history to SQLite."""
        logger.info("Migrating legacy history JSON to SQLite...")
        try:
            with open(APP_HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            if isinstance(data, list):
                count = 0
                # Use the persistent connection
                conn = cls._get_connection()
                try:
                    with conn: # Transaction
                        cursor = conn.cursor()
                        for entry in data:
                            try:
                                # Safely extract download_options logic if complex
                                options_json = json.dumps(entry.get("download_options", {}))
                                
                                # Construct timestamp from isoformat if missing
                                ts = entry.get("timestamp")
                                if not ts and "download_date" in entry:
                                    try:
                                        dt = datetime.fromisoformat(entry["download_date"])
                                        ts = dt.timestamp()
                                    except Exception:
                                        ts = time.time()
                                
                                cursor.execute("""
                                    INSERT OR IGNORE INTO history (
                                        id, title, url, channel, file_path, download_date,
                                        file_size, thumbnail_url, format_id, resolution,
                                        is_audio_only, duration, options, timestamp
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    entry.get("id", str(int(time.time()*1000))),
                                    entry.get("title", ""),
                                    entry.get("url", ""),
                                    entry.get("channel", "Unknown"),
                                    entry.get("file_path", ""),
                                    entry.get("download_date", ""),
                                    entry.get("file_size", 0),
                                    entry.get("thumbnail_url", ""),
                                    entry.get("format_id", ""),
                                    entry.get("resolution", ""),
                                    1 if entry.get("is_audio_only") else 0,
                                    entry.get("duration", ""),
                                    options_json,
                                    ts or time.time()
                                ))
                                count += 1
                            except Exception as e:
                                logger.error(f"Skipped invalid entry during migration: {e}")
                    
                    logger.info(f"Successfully migrated {count} history entries.")
                    
                    # Rename old JSON to .bak to avoid re-migration, or keep as backup
                    try:
                        APP_HISTORY_FILE.rename(APP_HISTORY_FILE.with_suffix(".json.bak"))
                    except Exception as e:
                        logger.warning(f"Could not rename legacy history file: {e}")
                        
                except Exception as e:
                     logger.error(f"Migration transaction failed: {e}")
                    
        except Exception as e:
            logger.error(f"Migration failed: {e}")

    @classmethod
    def _get_connection(cls):
        """Get the persistent database connection."""
        cls._init_db()
        if cls._connection is None:
             # Should be created in _init_db, but just in case
             cls._connection = sqlite3.connect(cls._db_file, check_same_thread=False)
             cls._connection.row_factory = sqlite3.Row
        return cls._connection

    @classmethod
    def get_all_entries(cls, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all history entries, sorted by most recent first.
        
        Args:
            limit: Optional limit on number of entries to return (most recent first)

        Returns:
            List of dictionary entries.
        """
        entries = []
        try:
            with cls._lock:  # Lock for simple concurrency safety
                # Use persistent connection
                conn = cls._get_connection()
                # conn.row_factory is already set in _init_db/_get_connection
                
                cursor = conn.cursor()
                
                query = "SELECT * FROM history ORDER BY timestamp DESC"
                params = ()
                
                if limit is not None:
                    query += " LIMIT ?"
                    params = (limit,)
                    
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                for row in rows:
                    entry = dict(row)
                    # Convert boolean back
                    entry["is_audio_only"] = bool(entry["is_audio_only"])
                    # Parse options JSON
                    try:
                        entry["download_options"] = json.loads(entry["options"]) if entry["options"] else {}
                    except json.JSONDecodeError:
                        entry["download_options"] = {}
                    del entry["options"] # Remove internal column
                    entries.append(entry)
                        
        except Exception as e:
            logger.error(f"Error fetching history: {e}")
            
        return entries

    @classmethod
    def get_entry(cls, entry_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific history entry by ID.

        Args:
            entry_id: The unique entry ID

        Returns:
            Entry dictionary or None if not found
        """
        try:
            with cls._lock:
                conn = cls._get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM history WHERE id = ?", (entry_id,))
                row = cursor.fetchone()
                
                if row:
                    entry = dict(row)
                    entry["is_audio_only"] = bool(entry["is_audio_only"])
                    try:
                        entry["download_options"] = json.loads(entry["options"]) if entry["options"] else {}
                    except json.JSONDecodeError:
                        entry["download_options"] = {}
                    del entry["options"]
                    return entry
            return None
        except Exception as e:
            logger.error(f"Error fetching entry {entry_id}: {e}")
            return None

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
        Add a new entry to the download history.
        """
        if download_options is None:
            download_options = {}

        timestamp = time.time()
        # Ensure unique ID
        unique_id = f"{int(timestamp * 1000)}"
        download_date = datetime.fromtimestamp(timestamp).isoformat()
        
        # Determine file size if not provided
        if file_size is None:
            try:
                p = Path(file_path)
                if p.exists():
                    file_size = p.stat().st_size
            except Exception:
                file_size = 0

        # Allow None for optional strings
        channel = channel or "Unknown"
        duration = duration or ""
        thumbnail_url = thumbnail_url or ""
        
        try:
            with cls._lock:
                conn = cls._get_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO history (
                        id, title, url, channel, file_path, download_date,
                        file_size, thumbnail_url, format_id, resolution,
                        is_audio_only, duration, options, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    unique_id,
                    title,
                    url,
                    channel,
                    str(file_path),
                    download_date,
                    file_size,
                    thumbnail_url,
                    format_id,
                    resolution,
                    1 if is_audio_only else 0,
                    duration,
                    json.dumps(download_options),
                    timestamp
                ))
                conn.commit()
            
            logger.info(f"Added history entry: {title}")
            return unique_id
            
        except Exception as e:
            logger.error(f"Error adding history entry: {e}")
            return ""

    @classmethod
    def remove_entry(cls, entry_id: str) -> bool:
        """Remove an entry from history by ID."""
        try:
            with cls._lock:
                conn = cls._get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM history WHERE id = ?", (entry_id,))
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Removed history entry: {entry_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error removing history entry: {e}")
            return False

    @classmethod
    def clear_history(cls) -> int:
        """Clear all history entries."""
        try:
            with cls._lock:
                conn = cls._get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM history")
                count = cursor.rowcount
                conn.commit()
            logger.info("History cleared")
            return count
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
            return 0
            
    @classmethod
    def search_entries(cls, query: str) -> List[Dict[str, Any]]:
        """
        Search history entries by title, channel, or URL.

        Args:
            query: Search query string

        Returns:
            List of matching history entries
        """
        if not query:
            return cls.get_all_entries()
            
        entries = []
        try:
            search_pattern = f"%{query}%"
            with cls._lock:
                conn = cls._get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM history 
                    WHERE title LIKE ? OR channel LIKE ? OR url LIKE ?
                    ORDER BY timestamp DESC
                """, (search_pattern, search_pattern, search_pattern))
                rows = cursor.fetchall()
                
                for row in rows:
                    entry = dict(row)
                    entry["is_audio_only"] = bool(entry["is_audio_only"])
                    try:
                        entry["download_options"] = json.loads(entry["options"]) if entry["options"] else {}
                    except json.JSONDecodeError:
                        entry["download_options"] = {}
                    del entry["options"]
                    entries.append(entry)
                        
        except Exception as e:
            logger.error(f"Error searching history: {e}")
            
        return entries
