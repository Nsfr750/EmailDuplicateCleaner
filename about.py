import tkinter as tk
from tkinter import ttk, messagebox
from version import get_version

class About:
    def show_about(self):
        about_root = tk.Toplevel()
        about_root.title("About")
        about_root.geometry("400x300")

        # Title
        title_label = tk.Label(about_root, text="Email Duplicate Cleaner", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Version
        version_label = tk.Label(about_root, text=f"Version {get_version()}")
        version_label.pack()

        # Description
        description_label = tk.Label(about_root, text="A tool to scan, identify, and remove duplicate emails\nfrom various email clients.", justify=tk.CENTER)
        description_label.pack(pady=20)

        # Links
        def open_github():
            import webbrowser
            webbrowser.open("https://github.com/Nsfr750/EmailDuplicateCleaner")

        def open_issues():
            import webbrowser
            webbrowser.open("https://github.com/Nsfr750/EmailDuplicateCleaner/issues")

        github_button = tk.Button(about_root, text="GitHub Repository", command=open_github)
        github_button.pack(pady=5)

        issues_button = tk.Button(about_root, text="Report Issues", command=open_issues)
        issues_button.pack(pady=5)

        # Copyright
        copyright_label = tk.Label(about_root, text="© 2025 Nsfr750", font=("Arial", 10))
        copyright_label.pack(pady=10)

        # Close button
        close_button = tk.Button(about_root, text="Close", command=about_root.destroy)
        close_button.pack(pady=10)
