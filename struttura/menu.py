"""
Menu Module

This module provides the main menu for the Email Duplicate Cleaner application.
It is designed to be a separate, reusable component using PySide6.

License: GPL v3.0 (see LICENSE)
"""

import sys
import os
import webbrowser
from pathlib import Path

from PySide6.QtWidgets import (
    QMenuBar, QMenu
)
from PySide6.QtGui import QKeySequence, QAction, QActionGroup
from PySide6.QtCore import Qt, Signal, QObject

# Add project root to the Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from lang.lang_manager import language_manager as lm, get_string as tr

class AppMenu(QObject):
    """Manages the application's menu bar using PySide6."""
    
    # Signals
    open_folder_triggered = Signal()
    run_demo_triggered = Signal()
    open_log_viewer_triggered = Signal()
    show_help_triggered = Signal()
    show_about_triggered = Signal()
    show_sponsor_triggered = Signal()
    exit_triggered = Signal()
    debug_mode_toggled = Signal(bool)
    dark_mode_toggled = Signal(bool)
    language_selected = Signal(str)

    def __init__(self, parent=None):
        """Initialize the menu and attach it to the parent window."""
        super().__init__(parent)
        self.parent = parent
        self.menu_bar = None
        self.language_group = None
        self.create_menu()

    def create_menu(self):
        """Create the application menu bar."""
        if not self.parent:
            return
            
        self.menu_bar = QMenuBar()
        
        # File menu
        file_menu = self.menu_bar.addMenu(lm.get('menu_file'))
        
        # Open Folder action
        open_folder_action = QAction(lm.get('menu_file_open_folder'), self.parent)
        open_folder_action.setShortcut(QKeySequence.Open)
        open_folder_action.triggered.connect(self.open_folder_triggered.emit)
        file_menu.addAction(open_folder_action)
        
        # Run Demo action
        run_demo_action = QAction(lm.get('menu_file_run_demo'), self.parent)
        run_demo_action.triggered.connect(self.run_demo_triggered.emit)
        file_menu.addAction(run_demo_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction(lm.get('menu_file_exit'), self.parent)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.exit_triggered.emit)
        file_menu.addAction(exit_action)

        # Tools menu
        tools_menu = self.menu_bar.addMenu(lm.get('menu_tools'))
        
        # Log Viewer action
        log_action = QAction(lm.get('menu_tools_log_viewer'), self)
        log_action.triggered.connect(self.open_log_viewer_triggered.emit)
        tools_menu.addAction(log_action)
        
        # Debug mode toggle
        self.debug_action = QAction(lm.get('menu_tools_debug'), self)
        self.debug_action.setCheckable(True)
        self.debug_action.setChecked(False)
        self.debug_action.triggered.connect(self.toggle_debug_mode)
        tools_menu.addAction(self.debug_action)
        
        tools_menu.addSeparator()
        
        # View menu
        view_menu = self.menu_bar.addMenu(lm.get('menu_view'))
        
        # Dark mode toggle
        self.dark_mode_action = QAction(lm.get('menu_view_dark_mode'), self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setChecked(False)
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(self.dark_mode_action)
        
        # Settings menu
        settings_menu = self.menu_bar.addMenu(lm.get('menu_settings'))
        
        # Language submenu
        language_menu = settings_menu.addMenu(lm.get('menu_settings_language'))
        
        # Language actions
        self.language_group = QActionGroup(self)
        self.language_group.setExclusive(True)
        
        # English
        en_action = QAction(lm.get('menu_settings_language_en'), self)
        en_action.setCheckable(True)
        en_action.setData('en')
        en_action.triggered.connect(self.on_language_selected)
        self.language_group.addAction(en_action)
        language_menu.addAction(en_action)
        
        # Italian
        it_action = QAction(lm.get('menu_settings_language_it'), self)
        it_action.setCheckable(True)
        it_action.setData('it')
        it_action.triggered.connect(self.on_language_selected)
        self.language_group.addAction(it_action)
        language_menu.addAction(it_action)
        
        # Set default language
        en_action.setChecked(True)
        
        # Help menu
        self.help_menu = self.menu_bar.addMenu(lm.get('menu_help'))
        
        help_action = QAction(lm.get('menu_help_help'), self)
        help_action.triggered.connect(self.show_help_triggered.emit)
        self.help_menu.addAction(help_action)
        
        about_action = QAction(lm.get('menu_help_about'), self)
        about_action.triggered.connect(self.show_about_triggered.emit)
        self.help_menu.addAction(about_action)
        
        sponsor_action = QAction(tr('menu_help_sponsor'), self)
        sponsor_action.triggered.connect(self.show_sponsor_triggered.emit)
        self.help_menu.addAction(sponsor_action)
        
        # Add menu bar to parent if it's a QMainWindow
        
    def on_language_selected(self):
        """Handle language selection from the menu."""
        action = self.sender()
        if action and hasattr(action, 'data'):
            language_code = action.data()
            self.language_selected.emit(language_code)
            
    def toggle_debug_mode(self, checked):
        """Toggle debug mode."""
        self.debug_mode_toggled.emit(checked)
        
    def toggle_dark_mode(self, checked):
        """Toggle dark mode."""
        self.dark_mode_toggled.emit(checked)
        if hasattr(self.parent, 'setMenuBar'):
            self.parent.setMenuBar(self.menu_bar)
    
    def open_folder(self):
        """Emit signal to open folder."""
        self.open_folder_triggered.emit()
    
    def run_demo_mode(self):
        """Emit signal to run demo mode."""
        self.run_demo_triggered.emit()
    
    def exit_application(self):
        """Emit signal to exit application."""
        self.exit_triggered.emit()
    
    def toggle_debug_mode(self, checked):
        """Handle debug mode toggle."""
        self.debug_mode_toggled.emit(checked)
    
    def toggle_dark_mode(self, checked):
        """Handle dark mode toggle."""
        self.dark_mode_toggled.emit(checked)
    
    def set_language(self, lang_code):
        """Set the current language in the UI and update all menu items."""
        if not self.menu_bar:
            return
            
        # Update menu titles
        for action in self.menu_bar.actions():
            menu = action.menu()
            if not menu:
                continue
                
            # Update menu titles
            if action.text() in [tr('menu_file'), tr('menu_tools'), tr('menu_view'), 
                              tr('menu_settings'), tr('menu_help')]:
                menu.setTitle(tr(menu.objectName().replace('_menu', '')))
                
                # Update all actions in the menu
                for menu_action in menu.actions():
                    if menu_action.isSeparator():
                        continue
                        
                    # Update action text
                    action_text = menu_action.text()
                    if action_text in [tr('menu_file_open_folder'), tr('menu_file_run_demo'), 
                                     tr('menu_file_exit'), tr('menu_tools_log_viewer'),
                                     tr('menu_tools_debug'), tr('menu_view_dark_mode'),
                                     tr('menu_settings_language'), tr('menu_help_help'),
                                     tr('menu_help_about'), tr('menu_help_sponsor')]:
                        menu_action.setText(tr(menu_action.objectName()))
        
        # Update language radio buttons
        for action in self.language_group.actions():
            lang_code = action.data()
            if lang_code == 'en':
                action.setText(tr('menu_settings_language_en'))
            elif lang_code == 'it':
                action.setText(tr('menu_settings_language_it'))
                
        # Update the checked state of the current language
        current_lang = lm.get_language()
        for action in self.language_group.actions():
            if action.data() == current_lang:
                action.setChecked(True)
                break
    
    def destroy(self):
        """Clean up the menu bar."""
        if self.menu_bar:
            self.menu_bar.deleteLater()
            self.menu_bar = None
