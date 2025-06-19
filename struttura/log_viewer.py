import tkinter as tk
from tkinter import scrolledtext, ttk
import sys
import os
import logging
import queue
from tkinter import filedialog

# Add project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from lang.lang import get_string

class LogViewer(tk.Toplevel):
    """A Toplevel window to display logs."""
    def __init__(self, parent, log_queue):
        super().__init__(parent)
        self.title(get_string("log_viewer_title"))
        self.geometry("700x400")

        self.log_queue = log_queue
        self.parent = parent

        self.create_widgets()
        self.after(100, self.process_queue)

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))

        log_level_label = ttk.Label(controls_frame, text=get_string('log_level_label'))
        log_level_label.pack(side=tk.LEFT, padx=(0, 5))

        self.log_level_var = tk.StringVar(value="INFO")
        log_level_menu = ttk.Combobox(controls_frame, textvariable=self.log_level_var, 
                                      values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], 
                                      state="readonly", width=10)
        log_level_menu.pack(side=tk.LEFT)
        log_level_menu.bind("<<ComboboxSelected>>", self.filter_logs)

        clear_button = ttk.Button(controls_frame, text=get_string('clear_log'), command=self.clear_log)
        clear_button.pack(side=tk.RIGHT, padx=(5, 0))

        export_button = ttk.Button(controls_frame, text=get_string('export_log'), command=self.export_log)
        export_button.pack(side=tk.RIGHT)

        # Log display
        self.log_tree = ttk.Treeview(main_frame, columns=("timestamp", "level", "message"), show="headings")
        self.log_tree.pack(fill=tk.BOTH, expand=True)

        self.log_tree.heading("timestamp", text=get_string('log_timestamp_header'))
        self.log_tree.heading("level", text=get_string('log_level_name_header'))
        self.log_tree.heading("message", text=get_string('log_message_header'))

        self.log_tree.column("timestamp", width=150, stretch=False)
        self.log_tree.column("level", width=80, stretch=False)
        self.log_tree.column("message", width=550)

        # Store all logs for filtering
        self.all_logs = []

    def process_queue(self):
        try:
            while True:
                record = self.log_queue.get_nowait()
                self.display_log(record)
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_queue)

    def display_log(self, record):
        log_entry = {
            'timestamp': record.asctime,
            'level': record.levelname,
            'message': record.getMessage(),
            'levelno': record.levelno
        }
        self.all_logs.append(log_entry)

        # Insert if it matches current filter
        if record.levelno >= logging.getLevelName(self.log_level_var.get()):
            self.log_tree.insert("", tk.END, values=(log_entry['timestamp'], log_entry['level'], log_entry['message']))

    def filter_logs(self, event=None):
        self.log_tree.delete(*self.log_tree.get_children())
        level_filter = logging.getLevelName(self.log_level_var.get())

        for log_entry in self.all_logs:
            if log_entry['levelno'] >= level_filter:
                self.log_tree.insert("", tk.END, values=(log_entry['timestamp'], log_entry['level'], log_entry['message']))

    def clear_log(self):
        self.log_tree.delete(*self.log_tree.get_children())
        self.all_logs.clear()

    def export_log(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".log",
                                                 filetypes=[("Log Files", "*.log"), ("All Files", "*.*")],
                                                 title=get_string('export_log'))
        if file_path:
            with open(file_path, 'w') as f:
                for log_entry in self.all_logs:
                    f.write(f"{log_entry['timestamp']} - {log_entry['level']} - {log_entry['message']}\n")
