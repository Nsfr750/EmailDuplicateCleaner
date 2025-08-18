"""
Email Duplicate Cleaner - PySide6 GUI

This module provides a modern PySide6-based graphical user interface
for the Email Duplicate Cleaner application.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

# Import the EmailClientManager from the main module
from email_duplicate_cleaner import EmailClientManager

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QTabWidget, QTextEdit, QComboBox,
    QFileDialog, QMessageBox, QProgressBar, QSplitter, QGroupBox, QCheckBox,
    QFormLayout, QSpinBox, QLineEdit, QDialog, QDialogButtonBox, QMenuBar,
    QMenu, QStatusBar, QToolBar, QSplashScreen, QSizePolicy, QRadioButton
)
from PySide6.QtGui import QAction
from PySide6.QtCore import (
    Qt, QThread, Signal, QObject, QTimer, QSize, QUrl, QEvent, QSettings
)
from PySide6.QtGui import (
    QIcon, QPixmap, QDesktopServices, QFont, QTextCursor, QTextCharFormat,
    QColor, QTextOption, QFontMetrics, QGuiApplication, QScreen, QKeySequence
)

# Add project root to the Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Initialize language manager
from lang.lang_manager import language_manager

def tr(key: str, **kwargs) -> str:
    """Convenience function for translations."""
    return language_manager.get(key, **kwargs)

# Import application modules
from email_duplicate_cleaner import EmailClientManager
from struttura.logger import setup_logging, ThreadSafeLogger
from struttura.menu import AppMenu
from struttura.updates import UpdateChecker
from struttura.help import Help
from struttura.about import About
from struttura.sponsor import SponsorDialog
from struttura.version import show_version, get_version_info
from struttura.traceback_handler import setup_traceback_handler

# Set up logging using the centralized logger
from struttura.logger import logger as app_logger
from struttura.logger import setup_logging

# Initialize the logger with debug level
logger = app_logger
setup_logging(logging.DEBUG)

# Log application startup
logger.info("Application starting...")
logger.info(f"Python version: {sys.version}")

logger.info("Application starting...")
logger.info(f"Python version: {sys.version}")
logger.info(f"Working directory: {os.getcwd()}")
logger.info(f"Python path: {sys.path}")

# Set up global exception handler
setup_traceback_handler()

class EmailCleanerGUI(QMainWindow):
    """Main application window for the Email Duplicate Cleaner."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Application state
        self.email_manager = EmailClientManager()
        self.current_folder = None
        self.duplicate_groups = []
        self.settings = QSettings("EmailDuplicateCleaner", "EmailDuplicateCleaner")
        
        # Log viewer
        self.log_viewer = None
        
        # Connect language change signal
        language_manager.language_changed.connect(self.on_language_changed)
        
        # Initialize UI
        self.init_ui()
        
        # Load settings
        self.load_settings()
        
        # Check for updates after a short delay
        QTimer.singleShot(1000, self.check_for_updates)
    
    def init_ui(self):
        """Set up the user interface."""
        self.setWindowTitle(f"Email Duplicate Cleaner {get_version_info()['full_version']}")
        self.setMinimumSize(1024, 768)
        
        # Set application icon if available
        icon_path = Path(__file__).parent / "icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main content area
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Email clients and folders
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Email clients list
        self.client_combo = QComboBox()
        self.client_combo.currentIndexChanged.connect(self.on_client_changed)
        email_client_label = QLabel()
        email_client_label.setObjectName("emailClientLabel")
        left_layout.addWidget(email_client_label)
        left_layout.addWidget(self.client_combo)
        
        # Folders list
        self.folder_list = QListWidget()
        self.folder_list.itemClicked.connect(self.on_folder_selected)
        folder_label = QLabel()
        folder_label.setObjectName("folderLabel")
        left_layout.addWidget(folder_label)
        left_layout.addWidget(self.folder_list, 1)
        
        # Add left panel to splitter
        content_splitter.addWidget(left_panel)
        
        # Right panel - Main content
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Scan tab
        self.scan_tab = QWidget()
        self.setup_scan_tab()
        self.tabs.addTab(self.scan_tab, tr('tabs.scan'))
        
        # Duplicates tab
        self.duplicates_tab = QWidget()
        self.setup_duplicates_tab()
        self.tabs.addTab(self.duplicates_tab, tr('tabs.duplicates'))
        
        # Analysis tab
        self.analysis_tab = QWidget()
        self.setup_analysis_tab()
        self.tabs.addTab(self.analysis_tab, tr('tabs.analysis'))
        
        # Results tab
        self.results_tab = QWidget()
        self.setup_results_tab()
        self.tabs.addTab(self.results_tab, tr('tabs.results'))
        
        # Tools tab
        self.tools_tab = QWidget()
        self.setup_tools_tab()
        self.tabs.addTab(self.tools_tab, tr('tabs.tools'))
        
        # Settings tab
        self.settings_tab = QWidget()
        self.setup_settings_tab()
        self.tabs.addTab(self.settings_tab, tr('tabs.settings'))
        
        right_layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Add right panel to splitter
        content_splitter.addWidget(right_panel)
        
        # Set initial sizes
        content_splitter.setSizes([300, 700])
        
        # Add splitter to main layout
        main_layout.addWidget(content_splitter)
        
        # Load email clients
        self.load_email_clients()
    
    def on_open_folder(self):
        """Handle open folder action."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder:
            self.current_folder = folder
            self.status_bar.showMessage(f"Selected folder: {folder}")
    
    def create_menu_bar(self):
        """Create the menu bar using the AppMenu class."""
        # Create the AppMenu instance
        self.app_menu = AppMenu(self)
        self.setMenuBar(self.app_menu.menu_bar)
        
        # Connect menu signals to our methods
        self.app_menu.open_folder_triggered.connect(self.on_open_folder)
        self.app_menu.show_help_triggered.connect(self.show_help)
        self.app_menu.show_about_triggered.connect(self.show_about)
        self.app_menu.show_sponsor_triggered.connect(self.show_sponsor)
        self.app_menu.exit_triggered.connect(self.close)
        
        # Connect language selection signal
        self.app_menu.language_selected.connect(language_manager.set_language)
        
        # Set initial language in the menu
        current_lang = language_manager.get_language()
        for action in self.app_menu.language_group.actions():
            if action.data() == current_lang:
                action.setChecked(True)
                break
        
        # Only connect debug and dark mode toggles if the methods exist
        if hasattr(self, 'set_debug_mode'):
            self.app_menu.debug_mode_toggled.connect(self.set_debug_mode)
            self.app_menu.debug_action.setChecked(False)  # Or get from settings
            
        if hasattr(self, 'toggle_dark_mode'):
            self.app_menu.dark_mode_toggled.connect(self.toggle_dark_mode)
            self.app_menu.dark_mode_action.setChecked(False)  # Or get from settings
        
        # Connect to the open_log_viewer_triggered signal if the method exists
        if hasattr(self, 'open_log_viewer'):
            self.app_menu.open_log_viewer_triggered.connect(self.open_log_viewer)
            
        # Add check for updates action to the help menu
        check_updates_action = QAction("Check for &Updates...", self)
        check_updates_action.triggered.connect(self.check_for_updates)
        self.app_menu.help_menu.addAction(check_updates_action)
    
    def create_toolbar(self):
        """Create the toolbar."""
        self.toolbar = self.addToolBar("Tools")
        self.toolbar.setObjectName("mainToolbar")  # Set object name for state saving
        
        # Add actions
        self.toolbar.addAction("Scan Folder").triggered.connect(self.on_scan_folder)
        self.toolbar.addSeparator()
        self.toolbar.addAction("Analyze").triggered.connect(self.on_analyze)
        self.toolbar.addAction("Clean Up").triggered.connect(self.on_clean_up)
        
        # Add toolbar toggle action
        self.toolbar_toggle = QAction("Show Toolbar", self)
        self.toolbar_toggle.setCheckable(True)
        self.toolbar_toggle.setChecked(True)
        self.toolbar_toggle.triggered.connect(
            lambda checked: self.toolbar.setVisible(checked)
        )
    
    def setup_scan_tab(self):
        """Set up the scan tab."""
        layout = QVBoxLayout(self.scan_tab)
        
        # Add scan tab content here
        scan_label = QLabel(tr('scan_description'))
        scan_label.setWordWrap(True)
        layout.addWidget(scan_label)
        
        # Add scan button
        scan_button = QPushButton(tr('scan_button'))
        scan_button.clicked.connect(self.on_scan_folder)
        layout.addWidget(scan_button)
        
        # Add stretch to push content to the top
        layout.addStretch()
    
    def setup_duplicates_tab(self):
        """Set up the duplicates tab."""
        layout = QVBoxLayout(self.duplicates_tab)
        
        # Add duplicates tab content here
        duplicates_label = QLabel(tr('tabs.duplicates'))
        layout.addWidget(duplicates_label)
        
        # Add stretch to push content to the top
        layout.addStretch()
        
        # Duplicate groups list
        self.duplicate_groups_list = QListWidget()
        self.duplicate_groups_list.itemSelectionChanged.connect(self.on_duplicate_group_selected)
        
        # Email preview
        self.email_preview = QTextEdit()
        self.email_preview.setReadOnly(True)
        
        # Splitter for duplicates and preview
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.duplicate_groups_list)
        splitter.addWidget(self.email_preview)
        splitter.setSizes([300, 200])
        
        layout.addWidget(splitter)
    
    def setup_analysis_tab(self):
        """Set up the analysis tab."""
        layout = QVBoxLayout(self.analysis_tab)
        
        # Add analysis tab content here
        analysis_label = QLabel(tr('tabs.analysis'))
        layout.addWidget(analysis_label)
        
        # Add stretch to push content to the top
        layout.addStretch()
    
    def setup_results_tab(self):
        """Set up the results tab."""
        layout = QVBoxLayout(self.results_tab)
        
        # Add results tab content here
        results_label = QLabel(tr('tabs.results'))
        layout.addWidget(results_label)
        
        # Add stretch to push content to the top
        layout.addStretch()
    
    def setup_tools_tab(self):
        """Set up the tools tab."""
        layout = QVBoxLayout(self.tools_tab)
        
        # Add tools tab content here
        tools_label = QLabel(tr('tabs.tools'))
        layout.addWidget(tools_label)
        
        # Add stretch to push content to the top
        layout.addStretch()
    
    def setup_settings_tab(self):
        """Set up the settings tab."""
        layout = QVBoxLayout(self.settings_tab)
        
        # Add settings tab content here
        settings_label = QLabel(tr('tabs.settings'))
        layout.addWidget(settings_label)
        
        # Add language selection
        lang_group = QGroupBox(tr('menu_settings_language'))
        lang_layout = QVBoxLayout()
        
        # English radio button
        self.en_radio = QRadioButton(tr('menu_settings_language_en'))
        self.en_radio.toggled.connect(lambda: self.on_language_selected('en'))
        lang_layout.addWidget(self.en_radio)
        
        # Italian radio button
        self.it_radio = QRadioButton(tr('menu_settings_language_it'))
        self.it_radio.toggled.connect(lambda: self.on_language_selected('it'))
        lang_layout.addWidget(self.it_radio)
        
        # Set current language
        current_lang = language_manager.get_language()
        if current_lang == 'it':
            self.it_radio.setChecked(True)
        else:
            self.en_radio.setChecked(True)
        
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)
        
        # Add stretch to push content to the top
        layout.addStretch()
        # Analysis results
        self.analysis_results = QTextEdit()
        self.analysis_results.setReadOnly(True)
        
        layout.addWidget(QLabel("Analysis Results:"))
        layout.addWidget(self.analysis_results, 1)
    
    def load_email_clients(self):
        """Load available email clients."""
        self.client_combo.clear()
        
        # Add supported email clients
        self.client_combo.addItem(tr('email_client.select'), None)
        self.client_combo.addItem(tr('email_client.thunderbird'), "thunderbird")
        self.client_combo.addItem(tr('email_client.apple_mail'), "apple_mail")
        self.client_combo.addItem(tr('email_client.outlook'), "outlook")
        self.client_combo.addItem(tr('email_client.generic'), "generic")
    
    def on_client_changed(self, index):
        """Handle email client selection change."""
        client_id = self.client_combo.currentData()
        if not client_id:
            self.folder_list.clear()
            return
        
        # TODO: Load folders for the selected client
        self.folder_list.clear()
        self.folder_list.addItem("Loading folders...")
        
        # Simulate loading folders
        QTimer.singleShot(1000, self.load_folders)
    
    def load_folders(self):
        """Load folders for the selected email client."""
        client_id = self.client_combo.currentData()
        if not client_id:
            return
        
        self.folder_list.clear()
        
        # TODO: Load actual folders from the email client
        # This is a placeholder - replace with actual implementation
        folders = [
            "Inbox", "Sent", "Drafts", "Trash", "Junk",
            "Archive", "Important", "Starred", "Personal", "Work"
        ]
        
        for folder in folders:
            self.folder_list.addItem(folder)
    
    def on_folder_selected(self, item):
        """Handle folder selection."""
        self.current_folder = item.text()
        self.status_bar.showMessage(f"Selected folder: {self.current_folder}")
    
    def on_scan_folder(self):
        """Handle scan folder action."""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder Selected", "Please select a folder to scan.")
            return
        
        # Show progress
        self.status_bar.showMessage(f"Scanning folder: {self.current_folder}...")
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setVisible(True)
        
        # Simulate scanning
        QTimer.singleShot(2000, self.on_scan_complete)
    
    def on_scan_complete(self):
        """Handle scan completion."""
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Scan complete")
        
        # Show results
        QMessageBox.information(
            self,
            "Scan Complete",
            f"Found 5 duplicate email groups in {self.current_folder}."
        )
        
        # Update UI with results
        self.update_duplicates_list()
    
    def update_duplicates_list(self):
        """Update the duplicates list with sample data."""
        self.duplicate_groups_list.clear()
        
        # Sample data - replace with actual results
        groups = [
            "Meeting Invitation (5 duplicates)",
            "Newsletter: Weekly Digest (3 duplicates)",
            "Invoice #12345 (2 duplicates)",
            "Project Update (4 duplicates)",
            "Vacation Photos (2 duplicates)"
        ]
        
        for group in groups:
            self.duplicate_groups_list.addItem(group)
    
    def on_duplicate_group_selected(self):
        """Handle selection of a duplicate group."""
        current_item = self.duplicate_groups_list.currentItem()
        if not current_item:
            return
        
        # Update email preview with sample content
        self.email_preview.setPlainText(
            f"Preview of selected duplicate group: {current_item.text()}\n\n"
            "This is a preview of the email content. In a real implementation, "
            "this would show the actual email content of the selected duplicate group."
        )
    
    def on_analyze(self):
        """Handle analyze action."""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder Selected", "Please select a folder to analyze.")
            return
        
        # Show progress
        self.status_bar.showMessage(f"Analyzing folder: {self.current_folder}...")
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setVisible(True)
        
        # Simulate analysis
        QTimer.singleShot(1500, self.on_analysis_complete)
    
    def on_analysis_complete(self):
        """Handle analysis completion."""
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Analysis complete")
        
        # Update analysis tab with results
        self.analysis_results.setPlainText(
            "Analysis Results for 'Inbox':\n"
            "----------------------------------------\n"
            "Total emails: 1,245\n"
            "Duplicate emails: 42 (3.4%)\n"
            "Potential space savings: 12.7 MB\n\n"
            "Top duplicate senders:\n"
            "- newsletter@example.com (15 duplicates)\n"
            "- notifications@service.com (8 duplicates)\n"
            "- noreply@social.net (5 duplicates)\n\n"
            "Largest duplicate groups:\n"
            "- \"Meeting Invitation\" (5 duplicates, 2.1 MB)\n"
            "- \"Weekly Digest\" (3 duplicates, 1.8 MB)\n"
            "- \"Your Order Confirmation\" (3 duplicates, 1.2 MB)"
        )
        
        # Switch to analysis tab
        self.tabs.setCurrentWidget(self.analysis_tab)
    
    def on_clean_up(self):
        """Handle clean up action."""
        if self.duplicate_groups_list.count() == 0:
            QMessageBox.information(
                self,
                "No Duplicates Found",
                "No duplicate emails were found to clean up."
            )
            return
        
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Clean Up",
            "This will remove all duplicate emails, keeping only the first occurrence "
            "of each. This action cannot be undone.\n\n"
            "Are you sure you want to continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Show progress
            self.status_bar.showMessage("Cleaning up duplicates...")
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.progress_bar.setVisible(True)
            
            # Simulate cleanup
            QTimer.singleShot(2500, self.on_cleanup_complete)
    
    def on_cleanup_complete(self):
        """Handle cleanup completion."""
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Cleanup complete")
        
        # Show results
        QMessageBox.information(
            self,
            "Cleanup Complete",
            "Successfully removed 12 duplicate emails, freeing up 5.3 MB of disk space."
        )
        
        # Refresh the UI
        self.duplicate_groups_list.clear()
        self.email_preview.clear()
    
    def toggle_toolbar(self, visible):
        """Toggle toolbar visibility."""
        self.toolbar.setVisible(visible)
    
    def show_sponsor(self):
        """Show sponsor dialog."""
        try:
            print("\n=== Starting show_sponsor ===")
            print("Creating SponsorDialog instance...")
            
            # Create the dialog
            sponsor_dialog = SponsorDialog(self)
            print("SponsorDialog instance created successfully")
            
            # Set window flags to ensure proper dialog behavior
            sponsor_dialog.setWindowFlags(
                Qt.Window | 
                Qt.Dialog | 
                Qt.WindowTitleHint | 
                Qt.WindowCloseButtonHint |
                Qt.WindowSystemMenuHint
            )
            
            # Show the dialog modally
            print("Executing SponsorDialog...")
            result = sponsor_dialog.exec_()
            print(f"SponsorDialog closed with result: {result}")
            
        except ImportError as e:
            error_msg = f"Import error in show_sponsor: {str(e)}"
            print(error_msg)
            QMessageBox.critical(
                self,
                "Import Error",
                f"Failed to load required modules: {str(e)}\n\nPlease make sure all dependencies are installed."
            )
        except Exception as e:
            error_msg = f"Unexpected error in show_sponsor: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Error",
                f"An unexpected error occurred while showing the sponsor dialog.\n\n{str(e)}"
            )
        finally:
            print("=== show_sponsor completed ===\n")
    
    def show_about(self):
        """Show about dialog."""
        About.show_about(self)
    
    def show_help(self):
        """Show help dialog."""
        Help.show_help(self)
        
    def open_log_viewer(self):
        """Open the log viewer dialog."""
        try:
            from struttura.view_log import LogViewer
            self.log_viewer = LogViewer(self)
            self.log_viewer.finished.connect(self.log_viewer_finished)
            self.log_viewer.show()
            self.log_viewer.raise_()
            self.log_viewer.activateWindow()
        except Exception as e:
            logger.error(f"Error opening log viewer: {str(e)}", exc_info=True)
            QMessageBox.critical(
                self,
                tr('error_title'),
                f"Error opening log viewer: {str(e)}"
            )
    
    def log_viewer_finished(self):
        """Handle log viewer close event."""
        if self.log_viewer:
            self.log_viewer.deleteLater()
        self.log_viewer = None
    
    def check_for_updates(self):
        """Check for application updates."""
        self.status_bar.showMessage("Checking for updates...")
        
        # Get current version from the version module
        from struttura.version import __version__
        
        # Create and configure the update checker
        self.update_checker = UpdateChecker(current_version=__version__)
        self.update_checker.update_available.connect(self.on_update_available)
        self.update_checker.no_update_available.connect(self.on_no_update_available)
        self.update_checker.check_failed.connect(self.on_update_check_failed)
        
        # Start the update check
        self.update_checker.check_update()
    
    def on_update_available(self, release_info):
        """Handle update available event."""
        self.status_bar.showMessage("Update available!")
        
        # Show update dialog
        from struttura.updates import UpdateDialog
        dialog = UpdateDialog(release_info, self)
        if dialog.exec_() == QDialog.Accepted:
            # User chose to update
            QDesktopServices.openUrl(QUrl(release_info['html_url']))
    
    def on_no_update_available(self):
        """Handle no update available event."""
        self.status_bar.showMessage("You have the latest version.", 3000)
    
    def on_update_check_failed(self, error):
        """Handle update check failure."""
        self.status_bar.showMessage(f"Update check failed: {error}", 5000)
        QMessageBox.warning(
            self,
            "Update Check Failed",
            f"Failed to check for updates: {error}"
        )
    
    def load_settings(self):
        """Load application settings."""
        # Window geometry
        if self.settings.value("window/geometry"):
            self.restoreGeometry(self.settings.value("window/geometry"))
        
        # Window state
        if self.settings.value("window/state"):
            self.restoreState(self.settings.value("window/state"))
        
        # Other settings
        toolbar_visible = self.settings.value("ui/toolbar_visible", True, type=bool)
        if hasattr(self, 'toolbar_toggle'):
            self.toolbar_toggle.setChecked(toolbar_visible)
        if hasattr(self, 'toolbar'):
            self.toolbar.setVisible(toolbar_visible)
    
    def save_settings(self):
        """Save application settings."""
        # Window geometry and state
        self.settings.setValue("window/geometry", self.saveGeometry())
        self.settings.setValue("window/state", self.saveState())
        
        # Other settings
        self.settings.setValue("ui/toolbar_visible", self.toolbar_toggle.isChecked())
    
    def on_language_selected(self, lang_code):
        """Handle language selection from radio buttons."""
        if lang_code != language_manager.get_language():
            language_manager.set_language(lang_code)
    
    def on_language_changed(self, lang_code):
        """Handle language change and update the UI."""
        logger.info(f"Language changed to: {lang_code}")
        try:
            # Update the menu
            if hasattr(self, 'app_menu'):
                self.app_menu.set_language(lang_code)
            
            # Retranslate the UI
            self.retranslate_ui()
            
            # Show status message
            self.status_bar.showMessage(tr('status.language_changed').format(language=lang_code.upper()))
            
        except Exception as e:
            logger.error(f"Error changing language: {str(e)}", exc_info=True)
            self.status_bar.showMessage(tr('error.language_change_failed'))
    
    def retranslate_ui(self):
        """Retranslate UI elements when language changes."""
        try:
            # Window title
            self.setWindowTitle(tr('app.title').format(version=get_version_info()['full_version']))
            
            # Email client selection
            if hasattr(self, 'client_combo') and self.client_combo.count() > 0:
                self.client_combo.setItemText(0, tr('email_client.select'))
            
            # Folder list
            if hasattr(self, 'folder_list') and hasattr(self.folder_list, 'parent'):
                folder_label = self.folder_list.parent().layout().itemAt(0).widget()
                if isinstance(folder_label, QLabel):
                    folder_label.setText(tr('folders.label'))
            
            # Tabs
            if hasattr(self, 'tabs') and self.tabs.count() >= 2:
                self.tabs.setTabText(0, tr('tabs.duplicates'))
                self.tabs.setTabText(1, tr('tabs.analysis'))
            
            # Toolbar actions
            if hasattr(self, 'toolbar'):
                for action in self.toolbar.actions():
                    if action.text() == tr('actions.scan_folder') or action.text() == "Scan Folder":
                        action.setText(tr('actions.scan_folder'))
                    elif action.text() == tr('actions.analyze') or action.text() == "Analyze":
                        action.setText(tr('actions.analyze'))
                    elif action.text() == tr('actions.clean_up') or action.text() == "Clean Up":
                        action.setText(tr('actions.clean_up'))
            
            # Status bar
            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage(tr('status.ready'))
            
            # Menu items
            if hasattr(self, 'app_menu') and hasattr(self.app_menu, 'retranslate_ui'):
                self.app_menu.retranslate_ui()
                
            logger.info(f"UI retranslated to: {language_manager.get_language()}")
            
        except Exception as e:
            logger.error(f"Error retranslating UI: {str(e)}", exc_info=True)
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.save_settings()
        event.accept()


def show_splash_screen():
    """Show a splash screen while the application loads."""
    # Create and show the splash screen
    splash_pix = QPixmap(400, 200)
    splash_pix.fill(Qt.white)
    
    splash = QSplashScreen(splash_pix)
    splash.show()
    
    # Add some text to the splash screen
    splash.showMessage(
        "Loading Email Duplicate Cleaner...",
        Qt.AlignBottom | Qt.AlignHCenter,
        Qt.black
    )
    
    # Simulate loading time
    QApplication.processEvents()
    
    return splash


def main():
    """Main entry point for the application."""
    try:
        # Set up the application
        app = QApplication(sys.argv)
        
        # Set application metadata
        app.setApplicationName("Email Duplicate Cleaner")
        app.setApplicationVersion(get_version_info()['full_version'])
        app.setOrganizationName("Nsfr750")
        app.setOrganizationDomain("github.com/Nsfr750")
        
        # Set style
        app.setStyle('Fusion')
        
        # Show splash screen
        splash = show_splash_screen()
        
        # Create and show the main window
        print("Creating main window...")
        window = EmailCleanerGUI()
        print("Main window created")
        
        # Center the window on screen
        screen = QGuiApplication.primaryScreen().geometry()
        window_rect = window.frameGeometry()
        window_rect.moveCenter(screen.center())
        window.move(window_rect.topLeft())
        
        # Show the main window and finish splash screen
        window.show()
        splash.finish(window)
        print("Main window shown and splash screen finished")
        
        # Debug info
        print(f"Window geometry: {window.geometry()}")
        print(f"Window is visible: {window.isVisible()}")
        print(f"Window is active: {window.isActiveWindow()}")
        
        # Start the event loop
        print("Starting event loop...")
        return app.exec()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        return 1


if __name__ == "__main__":
    main()
