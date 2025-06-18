import tkinter as tk
from tkinter import ttk
from lang.lang import get_string
from version import __version__

class About:
    """A class to display the about window."""
    def show_about(self):
        about_root = tk.Toplevel()
        about_root.title(get_string("about_window_title"))
        about_root.transient(about_root.master)
        about_root.grab_set()
        about_root.resizable(False, False)

        main_frame = ttk.Frame(about_root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text=get_string('app_title'), font=("Arial", 16, "bold")).pack()
        ttk.Label(main_frame, text=f"{get_string('about_window_version')} {__version__}").pack(pady=(0, 10))

        ttk.Label(main_frame, text=get_string('about_window_description'), wraplength=380, justify=tk.CENTER).pack(pady=10)

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)

        ttk.Label(main_frame, text=f"{get_string('about_window_developer')} Nsfr750").pack()

        ttk.Button(main_frame, text=get_string("dialog_close_button"), command=about_root.destroy).pack(pady=(20, 0))

        about_root.update_idletasks()
        x = about_root.master.winfo_x() + (about_root.master.winfo_width() - about_root.winfo_width()) // 2
        y = about_root.master.winfo_y() + (about_root.master.winfo_height() - about_root.winfo_height()) // 2
        about_root.geometry(f"+{x}+{y}")
