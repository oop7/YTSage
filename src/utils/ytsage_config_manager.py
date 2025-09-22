"""
Config Manager Module
=====================

This module provides **thread-safe** centralized management for application
configuration in YTSage. It handles reading, writing, and managing settings
stored in a JSON file, with support for nested keys via dot notation.

Thread safety is ensured using a reentrant lock (`RLock`), so multiple threads
can safely access or modify settings concurrently.

Features
--------
- Thread-safe operations for getting, setting, and deleting configuration values.
- Loads settings from a JSON config file (`APP_CONFIG_FILE`).
- Creates the config file with default values if missing or corrupt.
- Retrieves, sets, and deletes settings using dot-separated keys.
- Provides safe error handling with logging instead of raising exceptions.
- Persists updates back to disk automatically.

Usage
-----
from src.utils.ytsage_config_manager import ConfigManager

# Load settings (auto-loads if not already loaded)
download_path = ConfigManager.get("download_path")

# Update a value
ConfigManager.set("download_path", "D:/Downloads")

# Retrieve nested value
last_check = ConfigManager.get("cached_versions.ytdlp.last_check")

# Delete a key
ConfigManager.delete("cached_versions.ffmpeg.path")

Design Notes
------------
- Settings are stored in `ConfigManager.settings` (a dict).
- Default values are defined in `ConfigManager.default_config`.
- All modifications trigger a save (`_save`) to keep JSON in sync.
- Logs actions and errors using the app's central logger.
- Uses `RLock` to allow safe concurrent access from multiple threads.

Exceptions
----------
- Any issues during file I/O (permissions, disk errors, JSON corruption)
  are caught and logged. The application continues running with defaults
  when possible.
"""

import json
import threading
from typing import Any

from src.utils.ytsage_constants import APP_CONFIG_FILE, USER_HOME_DIR
from src.utils.ytsage_logger import logger


class ConfigManager:
    """
    Thread-safe configuration manager for YTSage.

    Provides methods to load, save, get, set, and delete settings stored in a JSON file.
    Supports nested keys via dot notation and automatically persists changes.
    """

    _lock = threading.RLock()
    _config_file = APP_CONFIG_FILE
    _settings: dict[str, Any] = {}
    _default_config = {
        "download_path": str(USER_HOME_DIR / "Downloads"),
        "speed_limit_value": None,
        "speed_limit_unit_index": 0,
        "cookie_file_path": None,
        "last_used_cookie_file": None,
        "proxy_url": None,
        "geo_proxy_url": None,
        "auto_update_ytdlp": True,
        "auto_update_frequency": "daily",
        "last_update_check": 0,
        "cached_versions": {
            "ytdlp": {"version": None, "path": None, "last_check": 0, "path_mtime": 0},
            "ffmpeg": {"version": None, "path": None, "last_check": 0, "path_mtime": 0},
        },
    }

    @classmethod
    def _load(cls) -> None:
        """
        Loads configuration settings from a JSON file if it exists and is valid.
        If the file is missing or corrupt, loads default settings and creates or overwrites the config file as needed.
        Logs actions and errors during the process.
        """
        with cls._lock:
            if cls._config_file.exists():
                try:
                    with open(cls._config_file, "r", encoding="utf-8") as f:
                        cls._settings = json.load(f)
                    logger.info("Config loaded from file.")
                except json.JSONDecodeError:
                    cls._settings = cls._default_config.copy()
                    logger.warning("Config file corrupt, loaded defaults.")
            else:
                cls._settings = cls._default_config.copy()
                cls._save()
                logger.info("Config file not found, created default config.")

    @classmethod
    def _save(cls) -> None:
        """
        Save current settings to JSON file.

        Note:
            May raise exceptions if the file cannot be written due to permission issues,
            disk errors, or other I/O problems.
        """
        with cls._lock:
            try:
                with open(cls._config_file, "w", encoding="utf-8") as f:
                    json.dump(cls._settings, f, indent=4)
                logger.debug("Config saved to file.")
            except (OSError, PermissionError) as e:
                logger.exception(f"Failed to save config: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error while saving config: {e}")

    @classmethod
    def get(cls, key: str) -> Any:
        """
        Retrieve a configuration value using a dotted key notation.
        Args:
            key (str): The dotted key string representing the path to the desired setting (e.g., "database.host").
            Any: The value associated with the given key, or None if the key does not exist.
        Notes:
            - If the configuration settings are not loaded, this method will load them before attempting retrieval.
            - If any part of the dotted key path is missing, None is returned and a debug message is logged.
        """
        with cls._lock:
            if not cls._settings:
                cls._load()
            parts = key.split(".")
            value = cls._settings
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    logger.debug(f"Config key '{key}' not found.")
                    return None
            return value

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Sets a configuration value for a given key.
        If the configuration settings are not loaded, loads them first.
        Supports nested keys using dot notation (e.g., "database.host").
        Updates the configuration dictionary with the provided value,
        saves the updated settings, and logs the change.
        Args:
            key (str): The configuration key, possibly nested using dots.
            value (Any): The value to set for the specified key.
        Returns:
            None
        """
        with cls._lock:
            if not cls._settings:
                cls._load()
            parts = key.split(".")
            d = cls._settings
            for part in parts[:-1]:
                d = d.setdefault(part, {})
            d[parts[-1]] = value
            cls._save()
            logger.info(f"Config key '{key}' set to '{value}'.")

    @classmethod
    def delete(cls, key: str) -> None:
        """
        Deletes a configuration key from the settings.
        If the key is nested (dot-separated), traverses the settings dictionary accordingly.
        If the key exists, removes it and saves the updated settings.
        Logs the deletion or if the key was not found.
        Args:
            key (str): The dot-separated configuration key to delete.
        Returns:
            None
        """
        with cls._lock:
            if not cls._settings:
                cls._load()
            parts = key.split(".")
            d = cls._settings
            for part in parts[:-1]:
                if part not in d:
                    logger.debug(f"Config key '{key}' not found for deletion.")
                    return
                d = d[part]
            if parts[-1] in d:
                d.pop(parts[-1], None)
                cls._save()
                logger.info(f"Config key '{key}' deleted.")
            else:
                logger.debug(f"Config key '{key}' not found for deletion.")
