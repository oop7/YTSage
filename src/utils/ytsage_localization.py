"""
Localization Manager Module
==========================

This module provides centralized localization support for YTSage application.
It handles loading language files, switching languages, and retrieving localized strings.

Features
--------
- Thread-safe operations for getting localized text
- Fallback to English when translation is missing
- Support for multiple languages via JSON files
- Dynamic language switching without restart
- Nested key support with dot notation

Usage
-----
from src.utils.ytsage_localization import LocalizationManager

# Get localized text
text = LocalizationManager.get_text("download.ready")
button_text = LocalizationManager.get_text("buttons.download")

# Change language
LocalizationManager.set_language("es")

# Get available languages
languages = LocalizationManager.get_available_languages()
"""

import json
import threading
from pathlib import Path
from typing import Any, Dict

from src.utils.ytsage_logger import logger


class LocalizationManager:
    """
    Thread-safe localization manager for YTSage.
    
    Handles loading, caching, and retrieving localized strings from JSON language files.
    """
    
    _lock = threading.RLock()
    _current_language = "en"
    _languages: Dict[str, Dict[str, Any]] = {}
    _languages_dir = Path(__file__).parent.parent.parent / "languages"
    
    # Fallback English strings embedded in code
    _fallback_strings = {
        "app": {
            "title": "YTSage",
            "version": "v{version}",
            "ready": "Ready"
        },
        "buttons": {
            "download": "Download",
            "pause": "Pause", 
            "resume": "Resume",
            "cancel": "Cancel",
            "browse": "Browse",
            "clear": "Clear",
            "ok": "OK",
            "apply": "Apply",
            "close": "Close"
        },
        "dialogs": {
            "custom_options": "Custom Options",
            "settings": "Settings"
        },
        "tabs": {
            "cookies": "Login with Cookies",
            "custom_command": "Custom Command", 
            "proxy": "Proxy",
            "language": "Language"
        },
        "language": {
            "select_language": "Select Language:",
            "current_language": "Current language: {language}",
            "restart_required": "Language changes will take effect after restarting the application.",
            "english": "English",
            "spanish": "Español (Spanish)",
            "portuguese": "Português (Portuguese)",
            "russian": "Русский (Russian)",
            "chinese": "中文 (简体) (Chinese Simplified)",
            "german": "Deutsch (German)",
            "french": "Français (French)",
            "hindi": "हिन्दी (Hindi)",
            "indonesian": "Bahasa Indonesia (Indonesian)",
            "turkish": "Türkçe (Turkish)",
            "polish": "Polski (Polish)",
            "italian": "Italiano (Italian)"
        },
        "download": {
            "preparing": "🚀 Preparing your download...",
            "completed": "✅ Download completed!",
            "video_completed": "✅ Video download completed!",
            "audio_completed": "✅ Audio download completed!", 
            "subtitle_completed": "✅ Subtitle download completed!",
            "please_set_path": "Please set a download path using 'Change Path'",
            "please_enter_url": "Please enter a URL",
            "please_enter_url_and_path": "Please enter URL and set download path",
            "please_select_format": "Please select a format"
        },
        "formats": {
            "show_formats": "Show formats:"
        }
    }
    
    @classmethod
    def _ensure_languages_dir(cls) -> None:
        """Ensure the languages directory exists."""
        cls._languages_dir.mkdir(exist_ok=True)
    
    @classmethod
    def _load_language(cls, language_code: str) -> Dict[str, Any]:
        """
        Load a language file from disk.
        
        Args:
            language_code: The language code (e.g., 'en', 'es')
            
        Returns:
            Dictionary containing the language strings, or empty dict if not found
        """
        language_file = cls._languages_dir / f"{language_code}.json"
        
        if not language_file.exists():
            logger.warning(f"Language file not found: {language_file}")
            return {}
            
        try:
            with open(language_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Failed to load language file {language_file}: {e}")
            return {}
    
    @classmethod
    def _get_nested_value(cls, data: Dict[str, Any], key: str) -> Any:
        """
        Get a nested value from dictionary using dot notation.
        
        Args:
            data: Dictionary to search in
            key: Dot-separated key (e.g., "app.title")
            
        Returns:
            The value if found, None otherwise
        """
        parts = key.split(".")
        value = data
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None
                
        return value
    
    @classmethod
    def get_text(cls, key: str, **kwargs) -> str:
        """
        Get localized text for the given key.
        
        Args:
            key: Dot-separated key for the text (e.g., "app.title")
            **kwargs: Format parameters for the text
            
        Returns:
            Localized text, with fallback to English if not found
        """
        with cls._lock:
            # Load current language if not cached
            if cls._current_language not in cls._languages:
                cls._languages[cls._current_language] = cls._load_language(cls._current_language)
            
            # Try to get from current language
            current_lang_data = cls._languages.get(cls._current_language, {})
            text = cls._get_nested_value(current_lang_data, key)
            
            # Fallback to embedded English strings
            if text is None:
                text = cls._get_nested_value(cls._fallback_strings, key)
            
            # Final fallback to key itself
            if text is None:
                logger.warning(f"Localization key not found: {key}")
                text = key
            
            # Format the text with provided parameters
            if kwargs and isinstance(text, str):
                try:
                    text = text.format(**kwargs)
                except (KeyError, ValueError) as e:
                    logger.warning(f"Failed to format localized text '{key}': {e}")
            
            return str(text)
    
    @classmethod
    def set_language(cls, language_code: str) -> None:
        """
        Set the current language.
        
        Args:
            language_code: The language code to set (e.g., 'en', 'es')
        """
        with cls._lock:
            if language_code != cls._current_language:
                cls._current_language = language_code
                # Clear cache to force reload
                cls._languages.clear()
                logger.info(f"Language set to: {language_code}")
    
    @classmethod
    def get_current_language(cls) -> str:
        """Get the current language code."""
        return cls._current_language
    
    @classmethod
    def get_available_languages(cls) -> Dict[str, str]:
        """
        Get available languages from the languages directory.
        
        Returns:
            Dictionary mapping language codes to display names
        """
        cls._ensure_languages_dir()
        
        available_languages = {"en": cls.get_text("language.english")}
        
        # Scan for language files
        for language_file in cls._languages_dir.glob("*.json"):
            lang_code = language_file.stem
            if lang_code != "en":  # Skip English as it's already added
                # Try to get language display name from the file
                lang_data = cls._load_language(lang_code)
                display_name = cls._get_nested_value(lang_data, "language.display_name")
                if display_name:
                    available_languages[lang_code] = display_name
                else:
                    # Fallback display name
                    available_languages[lang_code] = lang_code.upper()
        
        return available_languages
    
    @classmethod
    def initialize(cls, language_code: str = "en") -> None:
        """
        Initialize the localization system.
        
        Args:
            language_code: Initial language code to use
        """
        with cls._lock:
            cls._ensure_languages_dir()
            cls.set_language(language_code)
            logger.info(f"Localization system initialized with language: {language_code}")


# Convenience function for getting localized text
def _(key: str, **kwargs) -> str:
    """
    Convenience function to get localized text.
    
    Args:
        key: Dot-separated key for the text
        **kwargs: Format parameters
        
    Returns:
        Localized text
    """
    return LocalizationManager.get_text(key, **kwargs)