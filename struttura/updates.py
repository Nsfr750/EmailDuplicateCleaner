"""
Update checking functionality for the Email Duplicate Cleaner application.
"""
import logging
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple, Callable
import requests
import json
from pathlib import Path
import os

# Get the application directory
APP_DIR = Path(__file__).parent.parent
UPDATES_FILE = APP_DIR / 'updates.json'

# Configure logger
logger = logging.getLogger(__name__)

class UpdateChecker:
    """Handles checking for application updates."""
    
    def __init__(self, current_version: str, config_path: Optional[Path] = None):
        """Initialize the update checker.
        
        Args:
            current_version: The current version of the application.
            config_path: Path to the configuration file (optional).
        """
        self.current_version = current_version
        self.config_path = config_path or UPDATES_FILE
        self.config = self._load_config()
        self.update_url = "https://api.github.com/repos/Nsfr750/EmailDuplicateCleaner/releases/latest"
    
    def _load_config(self) -> dict:
        """Load the update configuration."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading update config: {e}")
        return {
            'last_checked': None,
            'last_version': None,
            'dont_ask_until': None
        }
    
    def _save_config(self) -> None:
        """Save the update configuration."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving update config: {e}")
    
    def check_for_updates(self, parent: Optional[tk.Tk] = None, force_check: bool = False) -> Tuple[bool, Optional[dict]]:
        """Check for available updates.
        
        Args:
            parent: Parent window for dialogs.
            force_check: If True, skip the cache and force a check.
            
        Returns:
            Tuple of (update_available, update_info)
        """
        try:
            logger.info("Checking for updates...")
            response = requests.get(self.update_url, timeout=10)
            response.raise_for_status()
            release = response.json()
            
            latest_version = release['tag_name'].lstrip('v')
            self.config['last_checked'] = release['published_at']
            self.config['last_version'] = latest_version
            self._save_config()
            
            if self._version_compare(latest_version, self.current_version) > 0:
                logger.info(f"Update available: {latest_version}")
                return True, {
                    'version': latest_version,
                    'url': release['html_url'],
                    'notes': release['body'],
                    'published_at': release['published_at']
                }
            else:
                logger.info("No updates available")
                if parent:
                    messagebox.showinfo(
                        'No Updates',
                        'You are using the latest version.',
                        parent=parent
                    )
                return False, None
                
        except requests.RequestException as e:
            logger.error(f"Error checking for updates: {e}")
            if parent:
                messagebox.showerror(
                    'Update Error',
                    f'Failed to check for updates: {str(e)}',
                    parent=parent
                )
            return False, None
    
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
    
    def show_update_dialog(self, parent: tk.Tk, update_info: dict) -> None:
        """Show a dialog with update information."""
        from tkinter import ttk
        
        dialog = tk.Toplevel(parent)
        dialog.title("Update Available")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = 500
        height = 300
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create main frame
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Update info
        ttk.Label(
            main_frame,
            text=f"Version {update_info['version']} is available!",
            font=('TkDefaultFont', 12, 'bold')
        ).pack(pady=(0, 10))
        
        # Release notes
        notes_frame = ttk.LabelFrame(main_frame, text="Release Notes", padding=5)
        notes_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        text = tk.Text(
            notes_frame,
            wrap=tk.WORD,
            width=60,
            height=10,
            font=('TkDefaultFont', 9)
        )
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text.insert('1.0', update_info['notes'])
        text.config(state='disabled')
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Buttons
        ttk.Button(
            btn_frame,
            text="Download Now",
            command=lambda: self._open_download(update_info['url'])
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Remind Me Later",
            command=dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        # Make the dialog modal
        dialog.wait_window()
    
    def _open_download(self, url: str) -> None:
        """Open the download URL in the default browser."""
        import webbrowser
        webbrowser.open(url)
        self.dialog.destroy()


def check_for_updates(parent: Optional[tk.Tk] = None, current_version: str = "__version__", force_check: bool = False) -> None:
    """Check for application updates and show a dialog if an update is available.
    
    Args:
        parent: Parent window for dialogs.
        current_version: Current application version.
        force_check: If True, skip the cache and force a check.
    """
    checker = UpdateChecker(current_version)
    update_available, update_info = checker.check_for_updates(parent, force_check=force_check)
    
    if update_available and update_info:
        checker.show_update_dialog(parent, update_info)
