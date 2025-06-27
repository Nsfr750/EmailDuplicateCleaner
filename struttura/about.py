import tkinter as tk
from tkinter import ttk
import sys
import os

# Add project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from struttura.version import __version__
from lang.lang import get_string

class About:
    @staticmethod
    def show_about(root):
        about_dialog = tk.Toplevel(root)
        about_dialog.title(get_string('about'))
        about_dialog.geometry('350x250')
        about_dialog.transient(root)
        about_dialog.grab_set()

        # Add app icon or logo here if you have one
        title = ttk.Label(about_dialog, text=get_string('app_title'), font=('Helvetica', 16, 'bold'))
        title.pack(pady=20)

        # Get version dynamically from version.py
        version = ttk.Label(about_dialog, text=f"{get_string('version')} {__version__}")
        version.pack()

        description = ttk.Label(about_dialog, text='', justify=tk.CENTER)
        description.pack(pady=20)

        copyright = ttk.Label(about_dialog, text='© 2025 Nsfr750')
        copyright.pack(pady=10)

        ttk.Button(about_dialog, text=get_string('close'), command=about_dialog.destroy).pack(pady=20)
