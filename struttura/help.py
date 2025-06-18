from lang.lang import get_string

def get_help_content():
    """
    Returns the help content as a string.
    """
    return get_string('help_content')

import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lang.lang import get_string

class HelpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title(get_string("help_window_title"))
        self.geometry("700x550")
        self.transient(parent)
        self.grab_set()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        text_frame = ttk.Frame(self)
        text_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        help_text_widget = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Arial", 10), state="disabled")
        help_text_widget.grid(row=0, column=0, sticky="nsew")

        self.populate_help_text(help_text_widget)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        ttk.Button(button_frame, text=get_string("dialog_close_button"), command=self.destroy).pack(side=tk.RIGHT)

        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def populate_help_text(self, widget):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)

        help_content = get_help_content()

        widget.tag_configure('h1', font=('Arial', 16, 'bold'), spacing3=10)
        widget.tag_configure('h2', font=('Arial', 14, 'bold'), spacing3=8)
        widget.tag_configure('h3', font=('Arial', 12, 'italic'), spacing3=5)

        for line in help_content.split('\n'):
            if line.startswith('### '):
                widget.insert(tk.END, line[4:] + '\n', 'h3')
            elif line.startswith('## '):
                widget.insert(tk.END, line[3:] + '\n', 'h2')
            elif line.startswith('# '):
                widget.insert(tk.END, line[2:] + '\n', 'h1')
            elif line.strip() == '---':
                widget.insert(tk.END, '\n' + '-'*80 + '\n\n')
            else:
                widget.insert(tk.END, line + '\n')

        widget.config(state="disabled")
