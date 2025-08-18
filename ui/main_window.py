"""
Main window for the Email Duplicate Cleaner application.

This module contains the main window class that serves as the primary
interface for the application.
"""

import sys
import logging
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QTabWidget, QStatusBar, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QSettings

from .tabs.scan_tab import ScanTab
from .tabs.results_tab import ResultsTab
from .tabs.analysis_tab import AnalysisTab
from ..struttura.logger import setup_logging
from ..struttura.traceback import setup_traceback_handler
from ..struttura.updates import UpdateChecker
from ..lang.lang_manager import get_string
from ..email_duplicate_cleaner import EmailClientManager

class EmailCleanerGUI(QMainWindow):
    """
    Main window for the Email Duplicate Cleaner application.
    
    This class represents the main application window and manages the
    overall UI layout and state.
    """
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle(get_string('app_title'))
        self.resize(1000, 700)
        self.setMinimumSize(800, 600)
        
        # Set up instance variables
        self.client_manager = EmailClientManager()
        self.mail_folders = []
        self.selected_folders = []
        self.duplicate_groups = []
        self.scanning_thread = None
        self.cleaning_thread = None
        self.temp_dir = None
        self.debug_mode = False
        self.dark_mode = False
        
        # Initialize update checker
        from struttura.version import __version__
        self.update_checker = UpdateChecker(current_version=__version__)
        
        # Setup logging and exception handling
        setup_logging()
        setup_traceback_handler()
        logging.info("Application started (PySide6 GUI)")
        
        # Create the main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create the main tab widget
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.scan_tab = ScanTab(self)
        self.results_tab = ResultsTab(self)
        self.analysis_tab = AnalysisTab(self)
        
        self.tab_widget.addTab(self.scan_tab, get_string("tab_scan"))
        self.tab_widget.addTab(self.results_tab, get_string("tab_results"))
        self.tab_widget.addTab(self.analysis_tab, get_string("tab_analysis"))
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(get_string('ready_status'))
        
        # Load settings
        self.load_settings()
        
        # Check for updates after a short delay
        QTimer.singleShot(2000, self.check_for_updates)
    
    def load_settings(self):
        """Load application settings from persistent storage."""
        settings = QSettings("EmailDuplicateCleaner", "EmailDuplicateCleaner")
        
        # Window geometry
        if settings.contains("geometry"):
            self.restoreGeometry(settings.value("geometry"))
        
        # Window state
        if settings.contains("windowState"):
            self.restoreState(settings.value("windowState"))
        
        # Debug mode
        self.debug_mode = settings.value("debugMode", False, type=bool)
        
        # Dark mode
        self.dark_mode = settings.value("darkMode", False, type=bool)
        self.apply_theme()
    
    def save_settings(self):
        """Save application settings to persistent storage."""
        settings = QSettings("EmailDuplicateCleaner", "EmailDuplicateCleaner")
        
        # Window geometry and state
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        
        # Debug mode
        settings.setValue("debugMode", self.debug_mode)
        
        # Dark mode
        settings.setValue("darkMode", self.dark_mode)
    
    def apply_theme(self):
        """Apply the current theme (light/dark) to the application."""
        if self.dark_mode:
            self.set_dark_theme()
        else:
            self.set_light_theme()
    
    def set_dark_theme(self):
        """Apply a dark theme to the application."""
        # Set dark palette
        dark_palette = self.palette()
        dark_palette.setColor(dark_palette.Window, Qt.darkGray)
        dark_palette.setColor(dark_palette.WindowText, Qt.white)
        dark_palette.setColor(dark_palette.Base, Qt.darkGray)
        dark_palette.setColor(dark_palette.AlternateBase, Qt.gray)
        dark_palette.setColor(dark_palette.ToolTipBase, Qt.white)
        dark_palette.setColor(dark_palette.ToolTipText, Qt.white)
        dark_palette.setColor(dark_palette.Text, Qt.white)
        dark_palette.setColor(dark_palette.Button, Qt.darkGray)
        dark_palette.setColor(dark_palette.ButtonText, Qt.white)
        dark_palette.setColor(dark_palette.BrightText, Qt.red)
        dark_palette.setColor(dark_palette.Link, Qt.cyan)
        dark_palette.setColor(dark_palette.Highlight, Qt.cyan)
        dark_palette.setColor(dark_palette.HighlightedText, Qt.black)
        
        self.setPalette(dark_palette)
    
    def set_light_theme(self):
        """Apply a light theme to the application."""
        # Reset to default palette
        self.setPalette(self.style().standardPalette())
    
    def check_for_updates(self, force_check=False):
        """Check for application updates."""
        try:
            update_available, update_info = self.update_checker.check_for_updates(
                parent=self,
                force_check=force_check
            )
            
            if update_available and update_info:
                # Show update dialog with the new version
                self.update_checker.show_update_dialog(self, update_info)
                
        except Exception as e:
            logging.error(f"Error checking for updates: {e}")
            QMessageBox.critical(
                self, 
                get_string('error'),
                get_string('update_check_error').format(error=str(e))
            )
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Save settings
        self.save_settings()
        
        # Check for running operations
        if self.scanning_thread and self.scanning_thread.is_alive():
            if QMessageBox.question(
                self,
                get_string('confirm_exit_title'),
                get_string('scan_in_progress_exit'),
                QMessageBox.Yes | QMessageBox.No
            ) == QMessageBox.No:
                event.ignore()
                return
        
        if self.cleaning_thread and self.cleaning_thread.is_alive():
            if QMessageBox.question(
                self,
                get_string('confirm_exit_title'),
                get_string('clean_in_progress_exit'),
                QMessageBox.Yes | QMessageBox.No
            ) == QMessageBox.No:
                event.ignore()
                return
        
        # Accept the close event
        event.accept()
