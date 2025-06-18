import tkinter as tk
from tkinter import ttk
import webbrowser
from lang.lang import get_string

# Sponsor Class
class Sponsor:
    def show_sponsor_window(self):
        sponsor_root = tk.Toplevel()
        sponsor_root.title(get_string('sponsor_window_title'))

        main_frame = ttk.Frame(sponsor_root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text=get_string('sponsor_window_main_text'), font=("Arial", 12), wraplength=380, justify=tk.CENTER).pack(pady=(0, 15))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=5)

        def open_patreon():
            webbrowser.open("https://www.patreon.com/Nsfr750")

        def open_github():
            webbrowser.open("https://github.com/sponsors/Nsfr750")

        def open_paypal():
            webbrowser.open("https://paypal.me/3dmega")

        ttk.Button(button_frame, text=get_string('sponsor_window_patreon_button'), command=open_patreon).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text=get_string('sponsor_window_github_button'), command=open_github).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text=get_string('sponsor_window_paypal_button'), command=open_paypal).pack(side=tk.LEFT, padx=10)

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=(20, 10))

        def close_window():
            sponsor_root.destroy()

        ttk.Button(main_frame, text=get_string('dialog_close_button'), command=close_window).pack(side=tk.RIGHT, pady=(0, 10))

        sponsor_root.update_idletasks()
        x = sponsor_root.winfo_x() + (sponsor_root.winfo_width() - sponsor_root.winfo_width()) // 2
        y = sponsor_root.winfo_y() + (sponsor_root.winfo_height() - sponsor_root.winfo_height()) // 2
        sponsor_root.geometry(f"+{x}+{y}")
