"""
Update checking functionality for the Email Duplicate Cleaner application.

This module provides functionality to check for application updates
and notify the user when a new version is available.
"""

import logging
import json
import requests
import sys
import os
from pathlib import Path
from typing import Optional, Tuple, Callable, Dict, Any

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QDialogButtonBox, QCheckBox, QApplication, QTextBrowser, QWidget
)
from PySide6.QtCore import Qt, QUrl, QDateTime, QTimer, QObject, Signal
from PySide6.QtGui import QDesktopServices

# Get the application directory
APP_DIR = Path(__file__).parent.parent
UPDATES_FILE = APP_DIR / 'updates.json'

# Configure logger
logger = logging.getLogger(__name__)

class UpdateChecker(QObject):
    """Handles checking for application updates."""
    
    # Signal emitted when an update check is complete
    update_available = Signal(dict)  # Emits release info if update is available
    no_update_available = Signal()   # Emitted when no update is available
    check_failed = Signal(str)       # Emits error message if check fails
    
    def __init__(self, current_version: str, parent: Optional[QObject] = None, 
                 config_path: Optional[Path] = None):
        """Initialize the update checker.
        
        Args:
            current_version: The current version of the application.
            parent: Parent QObject.
            config_path: Path to the configuration file (optional).
        """
        super().__init__(parent)
        self.current_version = current_version
        self.config_path = config_path or UPDATES_FILE
        self.config = self._load_config()
        self.update_url = "https://api.github.com/repos/Nsfr750/EmailDuplicateCleaner/releases/latest"
        self.latest_release = None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load the update configuration."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading update config: {e}")
        return {
            'last_checked': None,
            'last_version': None,
            'dont_ask_until': None,
            'skip_version': None
        }
    
    def _save_config(self) -> None:
        """Save the update configuration."""
        try:
            os.makedirs(self.config_path.parent, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving update config: {e}")
            raise
    
    def check_update(self, force: bool = False) -> None:
        """Check for updates asynchronously.
        
        Emits update_available, no_update_available, or check_failed signal when done.
        
        Args:
            force: If True, skip the cache and force a check.
        """
        # Check if we should skip this version
        if not force and self.config.get('skip_version') == self.current_version:
            self.no_update_available.emit()
            return
            
        # Check if we've checked recently
        if not force and not self._should_check():
            self.no_update_available.emit()
            return
            
        # Start a thread to perform the network request
        def do_check():
            try:
                response = requests.get(self.update_url, timeout=10)
                response.raise_for_status()
                release = response.json()
                self.latest_release = release
                
                # Update last checked time
                self.config['last_checked'] = QDateTime.currentDateTime().toString(Qt.ISODate)
                self.config['last_version'] = release['tag_name']
                self._save_config()
                
                # Check if this is a new version
                if self._is_newer_version(release['tag_name']):
                    self.update_available.emit(release)
                else:
                    self.no_update_available.emit()
                    
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Error checking for updates: {error_msg}")
                self.check_failed.emit(error_msg)
        
        # Run the check in a separate thread
        QTimer.singleShot(0, do_check)
    
    def _should_check(self) -> bool:
        """Check if we should perform an update check."""
        last_checked = self.config.get('last_checked')
        if not last_checked:
            return True
            
        try:
            last_checked = QDateTime.fromString(last_checked, Qt.ISODate)
            if not last_checked.isValid():
                return True
                
            # Check if at least 24 hours have passed
            return last_checked.daysTo(QDateTime.currentDateTime()) >= 1
        except Exception:
            return True
    
    def _is_newer_version(self, v1: str) -> bool:
        """Check if v1 is a newer version than the current version."""
        return self._version_compare(v1, self.current_version) > 0
    
    def _version_compare(self, v1: str, v2: str) -> int:
        """Compare two version strings.
        
        Returns:
            1 if v1 > v2, -1 if v1 < v2, 0 if equal
        """
        def parse_version(v: str) -> list:
            # Remove 'v' prefix if present and split by dots
            v = v.lstrip('v')
            parts = []
            for part in v.split('.'):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If part is not a number, keep it as string for comparison
                    parts.append(part)
            return parts
            
        try:
            v1_parts = parse_version(v1)
            v2_parts = parse_version(v2)
            
            # Pad with zeros if versions have different lengths
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts += [0] * (max_len - len(v1_parts))
            v2_parts += [0] * (max_len - len(v2_parts))
            
            for i in range(max_len):
                if v1_parts[i] > v2_parts[i]:
                    return 1
                elif v1_parts[i] < v2_parts[i]:
                    return -1
            return 0
            
        except Exception:
            # Fallback to string comparison if version format is invalid
            return (v1 > v2) - (v1 < v2)
    
    def get_release_notes(self) -> str:
        """Get the release notes for the latest release."""
        return self.latest_release.get('body', '')
    
    def get_release_url(self) -> str:
        """Get the URL for the latest release."""
        return self.latest_release.get('html_url', '')
    
    def skip_version(self, version: str) -> None:
        """Skip this version and close the dialog."""
        self.config['skip_version'] = version
        self._save_config()


class UpdateDialog(QDialog):
    """Dialog to show when an update is available."""
    
    def __init__(self, update_checker: UpdateChecker, parent: Optional[QWidget] = None):
        """Initialize the update dialog."""
        super().__init__(parent)
        self.update_checker = update_checker
        self.setWindowTitle("Update Available")
        self.setMinimumSize(500, 400)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("A new version is available!")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        # Current and new version
        current_version = QLabel(f"Current version: {self.update_checker.current_version}")
        new_version = QLabel(f"New version: {self.update_checker.latest_release.get('tag_name', '')}")
        
        # Release notes
        notes_label = QLabel("Release notes:")
        notes = QTextBrowser()
        notes.setMarkdown(self.update_checker.get_release_notes())
        notes.setOpenExternalLinks(True)
        
        # Buttons
        btn_box = QDialogButtonBox()
        
        skip_btn = QPushButton("Skip This Version")
        skip_btn.clicked.connect(self.skip_version)
        btn_box.addButton(skip_btn, QDialogButtonBox.ActionRole)
        
        later_btn = QPushButton("Remind Me Later")
        later_btn.clicked.connect(self.reject)
        btn_box.addButton(later_btn, QDialogButtonBox.RejectRole)
        
        update_btn = QPushButton("Download Update")
        update_btn.setDefault(True)
        update_btn.clicked.connect(self.download_update)
        btn_box.addButton(update_btn, QDialogButtonBox.AcceptRole)
        
        # Layout
        layout.addWidget(title)
        layout.addWidget(current_version)
        layout.addWidget(new_version)
        layout.addSpacing(10)
        layout.addWidget(notes_label)
        layout.addWidget(notes, 1)  # Make notes expandable
        layout.addWidget(btn_box)
    
    def skip_version(self):
        """Skip this version and close the dialog."""
        self.update_checker.skip_version(self.update_checker.latest_release['tag_name'])
        self.reject()
    
    def download_update(self):
        """Open the download page in the default browser."""
        QDesktopServices.openUrl(QUrl(self.update_checker.get_release_url()))
        self.accept()


def check_for_updates(parent: Optional[QWidget] = None, current_version: str = "__version__", 
                    force_check: bool = False) -> UpdateChecker:
    """Check for application updates and show a dialog if an update is available.
    
    Args:
        parent: Parent widget for dialogs.
        current_version: Current application version.
        force_check: If True, skip the cache and force a check.
        
    Returns:
        The UpdateChecker instance that can be used to monitor the update status.
    """
    checker = UpdateChecker(current_version, parent)
    
    def on_update_available(release):
        dialog = UpdateDialog(checker, parent)
        dialog.exec()
    
    def on_check_failed(error):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.warning(
            parent,
            "Update Check Failed",
            f"Failed to check for updates: {error}",
            QMessageBox.Ok
        )
    
    # Connect signals
    checker.update_available.connect(on_update_available)
    checker.check_failed.connect(on_check_failed)
    
    # Start the check
    checker.check_update(force=force_check)
    return checker
