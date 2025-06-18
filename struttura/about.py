import tkinter as tk
from tkinter import ttk, messagebox
from struttura.version import get_version
from lang.lang import get_string

class About:
    """A class to display the about window."""
    def show_about(self):
        about_root = tk.Toplevel()
        about_root.title(get_string('about_title'))
        about_root.geometry("400x300")

        # Title
        title_label = tk.Label(about_root, text=get_string('app_title'), font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Version
        version_label = tk.Label(about_root, text=f"{get_string('version_label')} {get_version()}")
        version_label.pack()

        # Description
        description_label = tk.Label(about_root, text=get_string('about_description'), justify=tk.CENTER)
        description_label.pack(pady=20)

        # Links
        def open_github():
            import webbrowser
            webbrowser.open("https://github.com/Nsfr750/EmailDuplicateCleaner")

        def open_issues():
            import webbrowser
            webbrowser.open("https://github.com/Nsfr750/EmailDuplicateCleaner/issues")

        github_button = tk.Button(about_root, text=get_string('github_button'), command=open_github)
        github_button.pack(pady=5)

        issues_button = tk.Button(about_root, text=get_string('issues_button'), command=open_issues)
        issues_button.pack(pady=5)

        # Copyright
        copyright_label = tk.Label(about_root, text=get_string('copyright_label'), font=("Arial", 10))
        copyright_label.pack(pady=10)

        # Close button
        close_button = tk.Button(about_root, text=get_string('close_button'), command=about_root.destroy)
        close_button.pack(pady=10)
