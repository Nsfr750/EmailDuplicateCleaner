"""
Menu Module

This module provides the main menu for the Email Duplicate Cleaner application.
It is designed to be a separate, reusable component.

License: GPL v3.0 (see LICENSE)
"""

import tkinter as tk
import webbrowser
import sys
import os

# Add project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from lang.lang import get_string as tr
from struttura.about import About
from struttura.help import Help
from struttura.sponsor import Sponsor

class AppMenu:
    """Manages the application's menu bar."""

    def __init__(self, app):
        """Initialize the menu and attach it to the root window."""
        self.app = app
        self.root = app.root
        self.create_menu()

    def create_menu(self):
        """Create the application menu bar."""
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=tr('menu_file'), menu=file_menu)
        file_menu.add_command(label=tr('menu_file_open_folder'), command=self.app.open_folder)
        file_menu.add_command(label=tr('menu_file_run_demo'), command=self.app.run_demo_mode)
        file_menu.add_separator()
        file_menu.add_command(label=tr('menu_file_exit'), command=self.app.on_closing)

        # Tools menu
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=tr('menu_tools'), menu=tools_menu)
        tools_menu.add_command(label=tr('menu_tools_log_viewer'), command=self.app.open_log_viewer)

        # Settings menu
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=tr('menu_settings'), menu=settings_menu)
        
        lang_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label=tr('menu_settings_language'), menu=lang_menu)
        lang_menu.add_radiobutton(label=tr('menu_settings_language_en'), variable=self.app.lang_var, value='en', command=self.app.switch_language)
        lang_menu.add_radiobutton(label=tr('menu_settings_language_it'), variable=self.app.lang_var, value='it', command=self.app.switch_language)

        settings_menu.add_separator()
        dark_mode_var = tk.BooleanVar(value=False) # This should be tied to the app's state
        settings_menu.add_checkbutton(label=tr('menu_settings_dark_mode'), variable=dark_mode_var, command=self.app.toggle_dark_mode)
  
        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label=tr('menu_help'), command=lambda: Help.show_help(self.root))
        help_menu.add_separator()
        help_menu.add_command(label=tr('menu_help_about'), command=lambda: About.show_about(self.root))
        help_menu.add_command(label=tr('menu_sponsors_us'), command=lambda: Sponsor(self.root).show_sponsor())
        self.menu_bar.add_cascade(label=tr('menu_help'), menu=help_menu)  
  
    def destroy(self):
        """Destroy the menu bar."""
        self.menu_bar.destroy()
