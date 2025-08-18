"""
Scan tab for the Email Duplicate Cleaner application.

This module contains the ScanTab class which provides the UI for scanning
email folders for duplicates.
"""

import threading
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton,
    QButtonGroup, QListWidget, QCheckBox, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, Signal, Slot

from .. import get_string

class ScanTab(QWidget):
    """
    Tab for scanning email folders for duplicates.
    
    This tab allows users to select email clients, scan criteria, and
    folders to scan for duplicate emails.
    """
    
    # Signals
    scan_started = Signal()
    scan_completed = Signal(list, str)  # folders, criteria
    
    def __init__(self, parent=None):
        """Initialize the scan tab."""
        super().__init__(parent)
        self.parent = parent
        self.mail_folders = []
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # Client selection group
        client_group = QGroupBox(get_string('scan_client_frame'))
        client_layout = QHBoxLayout()
        
        self.client_group = QButtonGroup()
        self.radio_client_all = QRadioButton(get_string('scan_client_all_radio'))
        self.radio_client_tb = QRadioButton(get_string('scan_client_thunderbird_radio'))
        self.radio_client_am = QRadioButton(get_string('scan_client_apple_mail_radio'))
        self.radio_client_ol = QRadioButton(get_string('scan_client_outlook_radio'))
        self.radio_client_gen = QRadioButton(get_string('scan_client_generic_radio'))
        
        self.client_group.addButton(self.radio_client_all)
        self.client_group.addButton(self.radio_client_tb)
        self.client_group.addButton(self.radio_client_am)
        self.client_group.addButton(self.radio_client_ol)
        self.client_group.addButton(self.radio_client_gen)
        
        client_layout.addWidget(self.radio_client_all)
        client_layout.addWidget(self.radio_client_tb)
        client_layout.addWidget(self.radio_client_am)
        client_layout.addWidget(self.radio_client_ol)
        client_layout.addWidget(self.radio_client_gen)
        
        client_group.setLayout(client_layout)
        layout.addWidget(client_group)
        
        # Criteria selection group
        criteria_group = QGroupBox(get_string('scan_criteria_frame'))
        criteria_layout = QHBoxLayout()
        
        self.criteria_group = QButtonGroup()
        self.radio_crit_strict = QRadioButton(get_string('scan_criteria_strict_radio'))
        self.radio_crit_content = QRadioButton(get_string('scan_criteria_content_radio'))
        self.radio_crit_headers = QRadioButton(get_string('scan_criteria_headers_radio'))
        self.radio_crit_subj_send = QRadioButton(get_string('scan_criteria_subject_sender_radio'))
        
        self.criteria_group.addButton(self.radio_crit_strict)
        self.criteria_group.addButton(self.radio_crit_content)
        self.criteria_group.addButton(self.radio_crit_headers)
        self.criteria_group.addButton(self.radio_crit_subj_send)
        
        criteria_layout.addWidget(self.radio_crit_strict)
        criteria_layout.addWidget(self.radio_crit_content)
        criteria_layout.addWidget(self.radio_crit_headers)
        criteria_layout.addWidget(self.radio_crit_subj_send)
        
        criteria_group.setLayout(criteria_layout)
        layout.addWidget(criteria_group)
        
        # Folder list
        folder_group = QGroupBox(get_string('scan_folder_frame'))
        folder_layout = QVBoxLayout()
        
        self.folder_list = QListWidget()
        self.folder_list.setSelectionMode(self.folder_list.MultiSelection)
        
        folder_layout.addWidget(self.folder_list)
        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group, 1)  # Stretch factor 1
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.check_auto_clean = QCheckBox(get_string('scan_autoclean_checkbox'))
        self.btn_find_folders = QPushButton(get_string('scan_find_folders_button'))
        self.btn_select_all = QPushButton(get_string('scan_select_all_button'))
        self.btn_scan = QPushButton(get_string('scan_button'))
        
        button_layout.addWidget(self.check_auto_clean)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_find_folders)
        button_layout.addWidget(self.btn_select_all)
        button_layout.addWidget(self.btn_scan)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.btn_find_folders.clicked.connect(self.find_mail_folders)
        self.btn_select_all.clicked.connect(self.select_all_folders)
        self.btn_scan.clicked.connect(self.start_scan)
        
        # Set defaults
        self.radio_client_all.setChecked(True)
        self.radio_crit_strict.setChecked(True)
    
    def find_mail_folders(self):
        """Find mail folders for the selected email client."""
        client_type = None
        
        if self.radio_client_tb.isChecked():
            client_type = "thunderbird"
        elif self.radio_client_am.isChecked():
            client_type = "apple_mail"
        elif self.radio_client_ol.isChecked():
            client_type = "outlook"
        elif self.radio_client_gen.isChecked():
            client_type = "generic"
        
        try:
            self.mail_folders = self.parent.client_manager.find_mail_folders(client_type)
            self.update_folder_list()
        except Exception as e:
            QMessageBox.critical(self, get_string('error'), 
                               get_string('error_finding_folders').format(error=str(e)))
    
    def update_folder_list(self):
        """Update the folder list widget with found mail folders."""
        self.folder_list.clear()
        
        for folder in self.mail_folders:
            item = QListWidgetItem(folder['name'])
            item.setData(Qt.UserRole, folder['path'])
            self.folder_list.addItem(item)
    
    def select_all_folders(self):
        """Select all folders in the list."""
        for i in range(self.folder_list.count()):
            self.folder_list.item(i).setSelected(True)
    
    def start_scan(self):
        """Start scanning selected folders for duplicates."""
        selected_items = self.folder_list.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, get_string('warning'), 
                              get_string('no_folders_selected'))
            return
        
        # Get selected folder paths
        selected_paths = [item.data(Qt.UserRole) for item in selected_items]
        
        # Get scan criteria
        criteria = "strict"
        if self.radio_crit_content.isChecked():
            criteria = "content"
        elif self.radio_crit_headers.isChecked():
            criteria = "headers"
        elif self.radio_crit_subj_send.isChecked():
            criteria = "subject-sender"
        
        # Emit signal to start scan
        self.scan_started.emit()
        
        # Start scanning in a separate thread
        self.scan_thread = threading.Thread(
            target=self._scan_folders,
            args=(selected_paths, criteria)
        )
        self.scan_thread.daemon = True
        self.scan_thread.start()
    
    def _scan_folders(self, folder_paths, criteria):
        """
        Scan folders for duplicates (runs in a separate thread).
        
        Args:
            folder_paths: List of folder paths to scan
            criteria: Criteria to use for detecting duplicates
        """
        try:
            # TODO: Implement actual scanning logic
            # This is a placeholder - replace with actual implementation
            import time
            time.sleep(2)  # Simulate work
            
            # Emit signal when done
            self.scan_completed.emit(folder_paths, criteria)
        except Exception as e:
            # Handle any errors that occur during scanning
            import traceback
            error_msg = f"Error during scan: {str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)  # This will be captured by the console
            
            # Show error message in the UI thread
            self.scan_completed.emit([], "error")
    
    def set_ui_enabled(self, enabled):
        """Enable or disable UI elements."""
        self.radio_client_all.setEnabled(enabled)
        self.radio_client_tb.setEnabled(enabled)
        self.radio_client_am.setEnabled(enabled)
        self.radio_client_ol.setEnabled(enabled)
        self.radio_client_gen.setEnabled(enabled)
        
        self.radio_crit_strict.setEnabled(enabled)
        self.radio_crit_content.setEnabled(enabled)
        self.radio_crit_headers.setEnabled(enabled)
        self.radio_crit_subj_send.setEnabled(enabled)
        
        self.folder_list.setEnabled(enabled)
        self.check_auto_clean.setEnabled(enabled)
        self.btn_find_folders.setEnabled(enabled)
        self.btn_select_all.setEnabled(enabled)
        self.btn_scan.setEnabled(enabled)
