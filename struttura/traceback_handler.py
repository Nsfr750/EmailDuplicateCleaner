"""
Traceback Handler Module

This module provides a global exception handler that displays unhandled exceptions
in a user-friendly dialog using PySide6.
"""

import sys
import traceback
import logging
import os
from pathlib import Path
from typing import Type, Any, Optional

from PySide6.QtWidgets import (
    QApplication, QMessageBox, QTextEdit, QVBoxLayout, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QHBoxLayout, QPushButton, QWidget
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QTextCursor, QTextCharFormat, QTextOption, QFont

# Add project root to the Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from lang.lang_manager import get_string as _


class ExceptionDialog(QDialog):
    """Dialog to display unhandled exceptions."""
    
    def __init__(self, error_message: str, traceback_text: str, parent: Optional[QWidget] = None):
        """Initialize the exception dialog.
        
        Args:
            error_message: The error message to display.
            traceback_text: The full traceback text.
            parent: The parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle(_("dialog_unhandled_exception_title"))
        self.setMinimumSize(700, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.setup_ui(error_message, traceback_text)
    
    def setup_ui(self, error_message: str, traceback_text: str):
        """Set up the user interface.
        
        Args:
            error_message: The error message to display.
            traceback_text: The full traceback text.
        """
        layout = QVBoxLayout(self)
        
        # Error message
        error_label = QLabel(_("dialog_unhandled_exception_message").format(error=error_message))
        error_label.setWordWrap(True)
        error_label.setStyleSheet("font-weight: bold; color: #d32f2f;")
        
        # Traceback text area
        traceback_label = QLabel(_("traceback_details") + ":")
        
        self.traceback_edit = QTextEdit()
        self.traceback_edit.setReadOnly(True)
        self.traceback_edit.setFont(QFont("Courier"))
        self.traceback_edit.setLineWrapMode(QTextEdit.NoWrap)
        self.traceback_edit.setPlainText(traceback_text)
        
        # Buttons
        button_box = QDialogButtonBox()
        
        copy_btn = QPushButton(_("copy_to_clipboard"))
        copy_btn.clicked.connect(self.copy_to_clipboard)
        
        close_btn = QPushButton(_("close"))
        close_btn.clicked.connect(self.accept)
        
        button_box.addButton(copy_btn, QDialogButtonBox.ActionRole)
        button_box.addButton(close_btn, QDialogButtonBox.AcceptRole)
        
        # Layout
        layout.addWidget(error_label)
        layout.addSpacing(10)
        layout.addWidget(traceback_label)
        layout.addWidget(self.traceback_edit, 1)  # Make the text edit expandable
        layout.addWidget(button_box)
    
    def copy_to_clipboard(self):
        """Copy the traceback to the clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.traceback_edit.toPlainText())


def show_traceback(exc_type: Type[BaseException], exc_value: BaseException, exc_tb: Any):
    """Global exception handler that shows a detailed error dialog.
    
    Args:
        exc_type: The exception type.
        exc_value: The exception value.
        exc_tb: The traceback object.
    """
    tb_string = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    error_message = str(exc_value)
    logging.critical("Unhandled exception:\n%s", tb_string)
    
    # Create a QApplication if one doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Show the error dialog
    dialog = ExceptionDialog(error_message, tb_string)
    dialog.exec()
    
    # If we created the QApplication, we should clean it up
    if app is not QApplication.instance():
        app.quit()


def setup_traceback_handler():
    """Set up the global exception handler."""
    sys.excepthook = show_traceback
