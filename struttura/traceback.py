"""
Traceback Logger 
"""

import sys
import traceback as _std_traceback
import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox
import traceback
import sys
from lang.lang import get_string
import logging

LOG_FILE = 'traceback.log'

def log_exception(exc_type, exc_value, exc_tb):
    """
    Logs uncaught exceptions and their tracebacks to Traceback.log.
    """
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Uncaught exception:\n")
        _std_traceback.print_exception(exc_type, exc_value, exc_tb, file=f)

def get_traceback_module():
    """
    Returns the standard library traceback module (for use in main.py if needed).
    """
    return _std_traceback

class TracebackWindow(tk.Toplevel):
    """A window to display unhandled exception tracebacks."""
    def __init__(self, exc_type, exc_value, exc_tb):
        super().__init__()
        self.title(get_string('traceback_title'))
        self.geometry("600x400")

        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        message_label = tk.Label(main_frame, text=get_string('traceback_message'), justify=tk.LEFT)
        message_label.pack(pady=(0, 10), anchor='w')

        tb_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15)
        tb_text.pack(fill=tk.BOTH, expand=True)

        formatted_traceback = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        tb_text.insert(tk.END, formatted_traceback)
        tb_text.config(state='disabled')

        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=(10, 0), fill=tk.X)

        copy_button = tk.Button(button_frame, text=get_string('copy_to_clipboard'), command=lambda: self.copy_to_clipboard(formatted_traceback))
        copy_button.pack(side=tk.LEFT)

        close_button = tk.Button(button_frame, text=get_string('close_button'), command=self.quit_app)
        close_button.pack(side=tk.RIGHT)

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo(get_string('info'), 'Traceback copied to clipboard.')

    def quit_app(self):
        self.destroy()
        sys.exit(1)

def handle_exception(exc_type, exc_value, exc_tb):
    """Global exception handler."""
    # Log the exception first
    logging.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_tb))
    
    # Then show the window
    TracebackWindow(exc_type, exc_value, exc_tb)

def setup_traceback_handler():
    """Sets the global exception handler."""
    global logging # Make it available to handle_exception
    sys.excepthook = handle_exception

# To enable global exception logging, add this to main.py:
# import traceback as tb_logger
# sys.excepthook = tb_logger.log_exception
# traceback = tb_logger.get_traceback_module()  # if you need the standard library traceback
