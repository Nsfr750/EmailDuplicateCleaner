import tkinter as tk
from tkinter import ttk, scrolledtext
import os
from .lang import tr

LOG_FILE = 'traceback.log'
LOG_LEVELS = ["ALL", "INFO", "WARNING", "ERROR"]

class LogViewer:
    """
    A dialog to view the application log file with filtering by log level.
    """
    @staticmethod
    def show_log(root):
        def load_log_lines():
            if not os.path.exists(LOG_FILE):
                return []
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                return f.readlines()

        def filter_lines(lines, level):
            if level == "ALL":
                return lines
            filtered = []
            for line in lines:
                if f"[{level}]" in line:
                    filtered.append(line)
            return filtered

        def update_display():
            lines = load_log_lines()
            filtered = filter_lines(lines, selected_level.get())
            text_area.config(state=tk.NORMAL)
            text_area.delete(1.0, tk.END)
            if filtered:
                text_area.insert(tk.END, ''.join(filtered))
            else:
                text_area.insert(tk.END, tr('no_log_entries', level=selected_level.get()))
            text_area.config(state=tk.DISABLED)

        def on_filter_change():
            update_display()

        log_window = tk.Toplevel(root)
        log_window.title(tr('log_viewer_title'))
        log_window.geometry('700x500')
        log_window.minsize(500, 300)

        # Filter buttons
        selected_level = tk.StringVar(value="ALL")
        filter_frame = ttk.Frame(log_window)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        for level in LOG_LEVELS:
            btn = ttk.Radiobutton(filter_frame, text=level, variable=selected_level, value=level, command=on_filter_change)
            btn.pack(side=tk.LEFT, padx=5)

        # Log text area
        text_area = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, font=('Consolas', 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        update_display()

        # Close button
        close_btn = ttk.Button(log_window, text=tr('close'), command=log_window.destroy)
        close_btn.pack(pady=10)

        log_window.transient(root)
        log_window.grab_set()
        root.wait_window(log_window)
