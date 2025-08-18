"""
Console output redirection for PySide6 applications.

This module provides a way to redirect stdout and stderr to a QTextEdit widget.
"""

from PySide6.QtCore import QObject, Signal

class RedirectStream(QObject):
    """
    A file-like object that emits a signal when written to.
    
    This allows redirecting stdout/stderr to a QTextEdit widget.
    """
    text_written = Signal(str)
    
    def write(self, text):
        """Emit the text that was written to the stream."""
        self.text_written.emit(str(text))
    
    def flush(self):
        """Flush the stream (no-op for this implementation)."""
        pass
