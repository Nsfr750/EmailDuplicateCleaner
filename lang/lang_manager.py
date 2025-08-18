"""
Language Manager Module

This module provides a language management system that loads translations from JSON files
and provides a simple interface for retrieving translated strings.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
from PySide6.QtCore import QObject, Signal, Slot, QLocale

class LanguageManager(QObject):
    """
    Manages application translations loaded from JSON files.
    
    The LanguageManager loads translation files from the specified directory
    and provides methods to retrieve translated strings by key.
    """
    
    # Signal emitted when the language is changed
    language_changed = Signal(str)
    
    def __init__(self, lang_dir: str = None, default_lang: str = 'en'):
        """
        Initialize the language manager.
        
        Args:
            lang_dir: Directory containing language JSON files. If None, uses 'lang' in the current directory.
            default_lang: Default language code (e.g., 'en', 'it').
        """
        super().__init__()
        self._translations: Dict[str, Dict[str, str]] = {}
        self._current_lang = default_lang
        # Look for language files in the same directory as this file
        self._lang_dir = Path(lang_dir) if lang_dir else Path(__file__).parent
        
        # Load translations
        self.load_translations()
        
        # Try to set system language if available
        self._try_set_system_language()
    
    def _try_set_system_language(self) -> None:
        """Try to set the language based on system settings."""
        system_lang = QLocale.system().name()[:2]  # Get first 2 chars (e.g., 'en', 'it')
        if system_lang in self._translations:
            self._current_lang = system_lang
    
    def load_translations(self) -> None:
        """Load all translation files from the language directory."""
        self._translations.clear()
        
        if not self._lang_dir.exists():
            raise FileNotFoundError(f"Language directory not found: {self._lang_dir}")
        
        # Find all JSON files in the language directory
        for lang_file in self._lang_dir.glob('*.json'):
            lang_code = lang_file.stem  # Get language code from filename (e.g., 'en' from 'en.json')
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self._translations[lang_code] = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading language file {lang_file}: {e}")
    
    def set_language(self, lang_code: str) -> bool:
        """
        Set the current language.
        
        Args:
            lang_code: Language code (e.g., 'en', 'it')
            
        Returns:
            bool: True if language was changed, False if not found
        """
        if lang_code in self._translations:
            self._current_lang = lang_code
            self.language_changed.emit(lang_code)
            return True
        return False
    
    def get_language(self) -> str:
        """Get the current language code."""
        return self._current_lang
    
    def get_available_languages(self) -> Dict[str, str]:
        """
        Get a dictionary of available language codes and their display names.
        
        Returns:
            Dict[str, str]: Dictionary mapping language codes to display names
        """
        return {
            'en': self.get('menu_settings_language_en', 'English'),
            'it': self.get('menu_settings_language_it', 'Italian')
        }
    
    def get(self, key: str, default: Optional[str] = None, **kwargs) -> str:
        """
        Get a translated string by key.
        
        Args:
            key: Translation key
            default: Default value if key not found
            **kwargs: Format arguments for the translated string
            
        Returns:
            str: The translated string, or the key if not found
        """
        # Try to get the translation for the current language
        translation = self._translations.get(self._current_lang, {})
        result = translation.get(key, None)
        
        # If not found and not English, try English as fallback
        if result is None and self._current_lang != 'en':
            result = self._translations.get('en', {}).get(key, None)
        
        # If still not found, use the key or default
        if result is None:
            return default if default is not None else key
        
        # Format the string with any provided arguments
        try:
            return result.format(**kwargs) if kwargs else result
        except (KeyError, IndexError):
            return result  # Return unformatted string if formatting fails
    
    def __call__(self, key: str, default: Optional[str] = None, **kwargs) -> str:
        """Alias for get() to allow using the instance as a callable."""
        return self.get(key, default, **kwargs)


# Global instance for convenience
language_manager = LanguageManager()

def get_string(key: str, default: Optional[str] = None, **kwargs) -> str:
    """
    Convenience function to get a translated string.
    
    Args:
        key: Translation key
        default: Default value if key not found
        **kwargs: Format arguments for the translated string
        
    Returns:
        str: The translated string, or the key if not found
    """
    return language_manager.get(key, default, **kwargs)
