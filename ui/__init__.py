"""
UI components for the Email Duplicate Cleaner application.

This package contains all the PySide6-based UI components for the application.
"""

# Make components available at the package level
from .redirect_stream import RedirectStream
from .main_window import EmailCleanerGUI

__all__ = ['RedirectStream', 'EmailCleanerGUI']
