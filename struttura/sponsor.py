import tkinter as tk
from tkinter import ttk
import webbrowser
import sys
import os

# Add project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from lang.lang import get_string as tr

# Sponsor Class
class Sponsor(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

    def show_sponsor(self):
        self.title(tr('sponsor'))
        self.geometry('500x150')
        
        # Sponsor buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        
        buttons = [
            (tr('sponsor_on_github'), "https://github.com/sponsors/Nsfr750"),
            (tr('join_discord'), "https://discord.gg/BvvkUEP9"),
            (tr('buy_me_a_coffee'), "https://paypal.me/3dmega"),
            (tr('join_the_patreon'), "https://www.patreon.com/Nsfr750")
        ]
        
        for text, url in buttons:
            btn = tk.Button(btn_frame, text=text, pady=5,
                          command=lambda u=url: webbrowser.open(u))
            btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        tk.Button(self, text=tr('close'), command=self.destroy).pack(pady=10)
