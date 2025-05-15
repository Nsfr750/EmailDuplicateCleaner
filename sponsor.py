import tkinter as tk
import webbrowser

# Sponsor Class
class Sponsor:
    def show_sponsor_window(self):
        sponsor_root = tk.Toplevel()
        sponsor_root.geometry("300x200")
        sponsor_root.title("Sponsor")

        title_label = tk.Label(sponsor_root, text="Support Us", font=("Arial", 16))
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
        patreon_button = tk.Button(sponsor_root, text="Join the Patreon!", command=open_patreon)
        patreon_button.pack(pady=5)

        github_button = tk.Button(sponsor_root, text="GitHub", command=open_github)
        github_button.pack(pady=5)

        discord_button = tk.Button(sponsor_root, text="Discord", command=open_discord)
        discord_button.pack(pady=5)

        paypal_button = tk.Button(sponsor_root, text="PayPal", command=open_paypal)
        paypal_button.pack(pady=5)
