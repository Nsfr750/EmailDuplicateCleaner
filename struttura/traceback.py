"""
Traceback Handler for Email Duplicate Cleaner

This module provides a custom traceback handler that displays unhandled
exceptions in a user-friendly PySide6-based dialog with options to copy
the traceback and continue or quit the application.
"""

import sys
import traceback as _std_traceback
import datetime
import logging
from pathlib import Path
from typing import Optional, Type, Any, Tuple, TypeVar

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit, QPushButton, 
    QHBoxLayout, QMessageBox, QApplication
)
from PySide6.QtCore import Qt, QSize, QTimer, Signal, QObject
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor, QFont, QTextOption

from .logger import logger

# Handle missing lang module
try:
    from lang.lang_manager import get_string
except ImportError:
    # Fallback if lang module is not found
    def get_string(key, *args, **kwargs):
        return key  # Return the key as-is if translation is not available

# Type variables for exception handling
ExcType = TypeVar('ExcType', bound=BaseException)

class TracebackSignals(QObject):
    """Signals for thread-safe traceback handling."""
    show_dialog = Signal(object, object, object, object)  # exc_type, exc_value, exc_tb, is_fatal

class TracebackDialog(QDialog):
    """A dialog to display unhandled exception tracebacks."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(get_string('traceback_title'))
        self.setMinimumSize(700, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self._setup_ui()
        self._setup_styles()
    
    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Message label
        self.message_label = QLabel(get_string('traceback_message'))
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)
        
        # Traceback text area
        self.traceback_edit = QTextEdit()
        self.traceback_edit.setReadOnly(True)
        self.traceback_edit.setLineWrapMode(QTextEdit.NoWrap)
        self.traceback_edit.setFontFamily('Consolas')
        self.traceback_edit.setFontPointSize(10)
        layout.addWidget(self.traceback_edit, 1)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.copy_button = QPushButton(get_string('copy_to_clipboard'))
        self.copy_button.setIcon(self.style().standardIcon(
            self.style().SP_DialogSaveButton))
        self.copy_button.clicked.connect(self._copy_to_clipboard)
        
        self.continue_button = QPushButton(get_string('continue_button'))
        self.continue_button.setIcon(self.style().standardIcon(
            self.style().SP_DialogOkButton))
        self.continue_button.clicked.connect(self.accept)
        
        self.quit_button = QPushButton(get_string('quit_button'))
        self.quit_button.setIcon(self.style().standardIcon(
            self.style().SP_DialogCancelButton))
        self.quit_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.copy_button)
        button_layout.addStretch()
        button_layout.addWidget(self.continue_button)
        button_layout.addWidget(self.quit_button)
        
        layout.addLayout(button_layout)
    
    def _setup_styles(self):
        """Set up the dialog styles."""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QTextEdit {
                background-color: #2b2b2b;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 5px;
                selection-background-color: #3d80df;
            }
            QPushButton {
                padding: 5px 15px;
                border: 1px solid #aaa;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
    
    def set_exception(self, exc_type: Type[BaseException], 
                     exc_value: BaseException, 
                     exc_tb: Any,
                     is_fatal: bool = True):
        """Set the exception details to display."""
        self.is_fatal = is_fatal
        
        # Format the traceback
        tb_lines = _std_traceback.format_exception(exc_type, exc_value, exc_tb)
        formatted_tb = "".join(tb_lines)
        
        # Set the traceback text with syntax highlighting
        self.traceback_edit.clear()
        
        # Use a monospace font for the traceback
        font = self.traceback_edit.font()
        font.setFamily('Consolas')
        font.setPointSize(10)
        self.traceback_edit.setFont(font)
        
        # Set the text
        cursor = self.traceback_edit.textCursor()
        cursor.insertText(formatted_tb)
        
        # Highlight the error message
        self._highlight_error(cursor, formatted_tb)
        
        # Show/hide continue button based on whether this is a fatal error
        self.continue_button.setVisible(not is_fatal)
        
        # Center the dialog on the screen
        self.center_on_screen()
    
    def _highlight_error(self, cursor: QTextCursor, text: str):
        """Highlight the error message in the traceback."""
        # Find the error message line (usually the last line)
        error_text = text.strip().split('\n')[-1]
        if not error_text:
            return
        
        # Create a format for the error message
        error_format = QTextCharFormat()
        error_format.setForeground(QColor('#ff6b6b'))  # Light red
        error_format.setFontWeight(QFont.Bold)
        
        # Find and format the error text
        cursor.movePosition(QTextCursor.Start)
        while cursor.find(error_text):
            cursor.mergeCharFormat(error_format)
    
    def center_on_screen(self):
        """Center the dialog on the screen."""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def _copy_to_clipboard(self):
        """Copy the traceback to the clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.traceback_edit.toPlainText())
        
        # Show a temporary message
        QMessageBox.information(
            self,
            get_string('info'),
            get_string('traceback_copied'),
            QMessageBox.Ok
        )
    
    def reject(self):
        """Handle the close/quit button."""
        if self.is_fatal:
            QApplication.quit()
        else:
            super().reject()

class TracebackHandler:
    """Handles uncaught exceptions and displays them in a dialog."""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.signals = TracebackSignals()
        self.signals.show_dialog.connect(self._show_dialog)
        self.dialog = None
    
    def handle_exception(self, exc_type: Type[BaseException], 
                        exc_value: BaseException, 
                        exc_tb: Any,
                        is_fatal: bool = True):
        """Handle an uncaught exception."""
        # Log the exception
        logger.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_tb))
        
        # Show the dialog in the main thread
        self.signals.show_dialog.emit(exc_type, exc_value, exc_tb, is_fatal)
    
    def _show_dialog(self, exc_type: Type[BaseException], 
                    exc_value: BaseException, 
                    exc_tb: Any,
                    is_fatal: bool):
        """Show the traceback dialog (must be called from the main thread)."""
        if self.dialog is None:
            self.dialog = TracebackDialog(self.parent)
        
        self.dialog.set_exception(exc_type, exc_value, exc_tb, is_fatal)
        
        # Show the dialog modally
        if is_fatal:
            self.dialog.setWindowModality(Qt.ApplicationModal)
            self.dialog.exec_()
            QApplication.quit()
        else:
            self.dialog.setWindowModality(Qt.WindowModal)
            self.dialog.exec_()

# Global instance
traceback_handler = TracebackHandler()

def setup_traceback_handler():
    """Set up the global exception handler."""
    def handle_exception(exc_type, exc_value, exc_tb):
        traceback_handler.handle_exception(exc_type, exc_value, exc_tb)
    
    sys.excepthook = handle_exception

def get_traceback_module():
    """Get the standard library traceback module."""
    return _std_traceback
