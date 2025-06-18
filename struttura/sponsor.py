import tkinter as tk
import webbrowser
from lang.lang import get_string

# Sponsor Class
class Sponsor:
    def show_sponsor_window(self):
        sponsor_root = tk.Toplevel()
        sponsor_root.geometry("300x200")
        sponsor_root.title(get_string('sponsor_title'))

        title_label = tk.Label(sponsor_root, text=get_string('sponsor_support_us'), font=("Arial", 16))
        title_label.pack(pady=10)

        def open_patreon():
            webbrowser.open("https://www.patreon.com/Nsfr750")

        def open_github():
            webbrowser.open("https://github.com/sponsors/Nsfr750")

        def open_discord():
            webbrowser.open("https://discord.gg/BvvkUEP9")

        def open_paypal():
            webbrowser.open("https://paypal.me/3dmega")

        # Create and place buttons
        patreon_button = tk.Button(sponsor_root, text=get_string('sponsor_patreon_button'), command=open_patreon)
        patreon_button.pack(pady=5)

        github_button = tk.Button(sponsor_root, text=get_string('sponsor_github_button'), command=open_github)
        github_button.pack(pady=5)

        discord_button = tk.Button(sponsor_root, text=get_string('sponsor_discord_button'), command=open_discord)
        discord_button.pack(pady=5)

        paypal_button = tk.Button(sponsor_root, text=get_string('sponsor_paypal_button'), command=open_paypal)
        paypal_button.pack(pady=5)
