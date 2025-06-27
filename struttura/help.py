"""
Help Dialog Module

This module provides the Help dialog for the Project.
Displays usage instructions and feature highlights in a tabbed interface.

License: GPL v3.0 (see LICENSE)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from lang.lang import get_string as tr

class Help:
    
    @staticmethod
    def show_help(parent):
        """
        Displays the help window with three tabs: Usage, Features, and Analysis.
        """
        help_window = tk.Toplevel(parent)
        help_window.title(tr('help_title'))
        help_window.geometry("700x500")
        help_window.minsize(600, 400)

        # Center the window on screen
        window_width = 700
        window_height = 500
        screen_width = help_window.winfo_screenwidth()
        screen_height = help_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        help_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(help_window)
        notebook.pack(pady=10, padx=10, fill="both", expand=True)

        # ===== USAGE TAB =====
        usage_frame = ttk.Frame(notebook, padding=10)
        usage_text = tr('help_usage')
        usage_label = ttk.Label(usage_frame, text=usage_text, justify=tk.LEFT, wraplength=650)
        usage_label.pack(fill=tk.BOTH, expand=True, anchor='nw')

        # ===== FEATURES TAB =====
        features_frame = ttk.Frame(notebook, padding=10)
        features_text = tr('help_features')
        features_label = ttk.Label(features_frame, text=features_text, justify=tk.LEFT, wraplength=650)
        features_label.pack(fill=tk.BOTH, expand=True, anchor='nw')

        # ===== ANALYSIS TAB =====
        analysis_frame = ttk.Frame(notebook, padding=10)
        analysis_text = tr('help_analysis')
        
        # Get theme colors
        style = ttk.Style()
        bg_color = style.lookup('TFrame', 'background')
        fg_color = style.lookup('TLabel', 'foreground')
        
        analysis_text_widget = tk.Text(
            analysis_frame, 
            wrap=tk.WORD, 
            font=("Segoe UI", 10), 
            bg=bg_color, 
            fg=fg_color,
            bd=0,
            relief=tk.FLAT,
            padx=5,
            pady=5
        )
        analysis_text_widget.insert(tk.END, analysis_text)
        analysis_text_widget.config(state=tk.DISABLED)
        analysis_text_widget.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Add tabs
        notebook.add(usage_frame, text=tr('usage_tab'))
        notebook.add(features_frame, text=tr('features_tab'))
        notebook.add(analysis_frame, text=tr('analysis_tab'))

        # Close button
        close_btn = ttk.Button(help_window, text=tr('close'), command=help_window.destroy)
        close_btn.pack(pady=10)
        
        # Make the window modal
        help_window.transient(parent)
        help_window.grab_set()
        parent.wait_window(help_window)
