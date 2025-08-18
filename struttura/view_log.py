"""
Log Viewer for Email Duplicate Cleaner

This module provides a log viewer window with filtering and management capabilities.
"""

import os
from pathlib import Path
from datetime import datetime
from send2trash import send2trash

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QTextEdit,
    QLabel, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor, QFont

# Import translation
from lang.lang_manager import language_manager

def tr(key, **kwargs):
    """Translation helper function."""
    return language_manager.get(key, **kwargs)

class LogViewer(QDialog):
    """Log viewer dialog for viewing and managing application logs."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr('log_viewer.title'))
        self.setMinimumSize(800, 600)
        self.current_log_file = None
        self.log_dir = Path("logs")
        
        # Ensure logs directory exists
        self.log_dir.mkdir(exist_ok=True)
        
        self.setup_ui()
        self.load_log_files()
        self.apply_dark_theme()
        
        # Auto-refresh timer - created in the main thread context
        self.refresh_timer = QTimer()
        self.refresh_timer.setTimerType(Qt.VeryCoarseTimer)  # More efficient for this use case
        self.refresh_timer.timeout.connect(self.refresh_log)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Top controls
        control_layout = QHBoxLayout()
        
        # Log file selector
        control_layout.addWidget(QLabel(tr('log_viewer.select_log')))
        self.log_selector = QComboBox()
        self.log_selector.currentTextChanged.connect(self.on_log_selected)
        control_layout.addWidget(self.log_selector, 1)
        
        # Log level filter
        control_layout.addWidget(QLabel(tr('log_viewer.filter_level')))
        self.level_filter = QComboBox()
        self.level_filter.addItems([
            tr('log_viewer.all_levels'),
            'DEBUG',
            'INFO',
            'WARNING',
            'ERROR',
            'CRITICAL'
        ])
        self.level_filter.currentTextChanged.connect(self.refresh_log)
        control_layout.addWidget(self.level_filter)
        
        # Refresh button
        self.refresh_btn = QPushButton(tr('log_viewer.refresh'))
        self.refresh_btn.clicked.connect(self.refresh_log)
        control_layout.addWidget(self.refresh_btn)
        
        # Export button
        self.export_btn = QPushButton(tr('log_viewer.export'))
        self.export_btn.clicked.connect(self.export_log)
        control_layout.addWidget(self.export_btn)
        
        # Delete button
        self.delete_btn = QPushButton(tr('log_viewer.delete'))
        self.delete_btn.clicked.connect(self.delete_log)
        control_layout.addWidget(self.delete_btn)
        
        layout.addLayout(control_layout)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Consolas", 10))
        layout.addWidget(self.log_display)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Close button
        self.close_btn = QPushButton(tr('common.close'))
        self.close_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
    
    def apply_dark_theme(self):
        """Apply dark theme to the log viewer."""
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #f0f0f0;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #f0f0f0;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton, QComboBox {
                background-color: #3c3f41;
                color: #f0f0f0;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover, QComboBox:hover {
                background-color: #4e5153;
            }
            QPushButton:pressed {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #f0f0f0;
            }
        """)
    
    def load_log_files(self):
        """Load available log files from the logs directory."""
        self.log_selector.clear()
        
        # Add log files to the selector
        log_files = sorted(
            [f for f in self.log_dir.glob("*.log") if f.is_file()],
            key=os.path.getmtime,
            reverse=True
        )
        
        if not log_files:
            self.log_selector.addItem(tr('log_viewer.no_logs_found'))
            self.export_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            return
        
        for log_file in log_files:
            self.log_selector.addItem(log_file.name, str(log_file))
        
        # Select the first log file by default
        if self.log_selector.count() > 0:
            self.current_log_file = Path(self.log_selector.currentData())
            self.refresh_log()
    
    def on_log_selected(self, log_name):
        """Handle log file selection change."""
        if not log_name or log_name == tr('log_viewer.no_logs_found'):
            self.current_log_file = None
            self.log_display.clear()
            self.export_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            return
        
        self.current_log_file = Path(self.log_dir, log_name)
        self.export_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)
        self.refresh_log()
    
    def refresh_log(self):
        """Refresh the log display with current filters."""
        if not self.current_log_file or not self.current_log_file.exists():
            self.log_display.clear()
            return
        
        try:
            with open(self.current_log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()
            
            self.log_display.clear()
            
            # Get selected log level filter
            selected_level = self.level_filter.currentText()
            
            for line in logs:
                if not line.strip():
                    continue
                
                # Apply log level filter
                log_level = self.get_log_level(line)
                if selected_level != tr('log_viewer.all_levels') and log_level != selected_level:
                    continue
                
                # Add log line with appropriate formatting
                self.append_log_line(line, log_level)
            
            # Scroll to bottom
            self.log_display.moveCursor(QTextCursor.End)
            
        except Exception as e:
            self.log_display.setPlainText(tr('log_viewer.error_loading_log').format(error=str(e)))
    
    def get_log_level(self, log_line):
        """Extract log level from log line."""
        for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            if f' - {level} - ' in log_line:
                return level
        return 'INFO'
    
    def append_log_line(self, line, level):
        """Append a log line with appropriate formatting."""
        cursor = self.log_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Set text color based on log level
        format = QTextCharFormat()
        
        if 'DEBUG' in level:
            format.setForeground(QColor('#888888'))  # Gray
        elif 'INFO' in level:
            format.setForeground(QColor('#ffffff'))  # White
        elif 'WARNING' in level:
            format.setForeground(QColor('#ffcc00'))  # Yellow
        elif 'ERROR' in level or 'CRITICAL' in level:
            format.setForeground(QColor('#ff6b68'))  # Red
        
        cursor.insertText(line, format)
    
    def export_log(self):
        """Export the current log to a file."""
        if not self.current_log_file:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"log_export_{timestamp}.log"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr('log_viewer.export_dialog_title'),
            default_name,
            "Log Files (*.log);;All Files (*)"
        )
        
        if file_path:
            try:
                import shutil
                shutil.copy2(self.current_log_file, file_path)
                QMessageBox.information(
                    self,
                    tr('common.success'),
                    tr('log_viewer.export_success').format(path=file_path)
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    tr('common.error'),
                    tr('log_viewer.export_error').format(error=str(e))
                )
    
    def delete_log(self):
        """Delete the currently selected log file."""
        if not self.current_log_file:
            return
        
        reply = QMessageBox.question(
            self,
            tr('common.confirm'),
            tr('log_viewer.confirm_delete').format(file=self.current_log_file.name),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Move to trash instead of permanent deletion
                send2trash(str(self.current_log_file))
                self.load_log_files()  # Refresh the log file list
                QMessageBox.information(
                    self,
                    tr('common.success'),
                    tr('log_viewer.delete_success').format(file=self.current_log_file.name)
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    tr('common.error'),
                    tr('log_viewer.delete_error').format(error=str(e))
                )
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.refresh_timer.stop()
        event.accept()
