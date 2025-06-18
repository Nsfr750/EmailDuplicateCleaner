import sys
import traceback
from tkinter import messagebox
import logging
import os

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lang.lang import get_string

def show_traceback(exc_type, exc_value, exc_tb):
    tb_string = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    error_message = str(exc_value)
    logging.critical("Unhandled exception:\n%s", tb_string)

    messagebox.showerror(
        get_string("dialog_unhandled_exception_title"),
        get_string("dialog_unhandled_exception_message").format(
            error=error_message,
            traceback=tb_string
        )
    )

def setup_traceback_handler():
    """Sets the global exception handler."""
    sys.excepthook = show_traceback
