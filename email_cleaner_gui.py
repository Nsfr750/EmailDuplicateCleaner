#!/usr/bin/env python3
"""
Email Duplicate Cleaner - GUI Interface

A graphical user interface for the Email Duplicate Cleaner tool.
This GUI provides easy access to the functionality for scanning and removing
duplicate emails from various email clients.
"""

import os
import sys
import logging
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, Toplevel
import queue
import sqlite3


# Sponsor Class
class Sponsor:
    def show_sponsor_window(self):
        sponsor_root = Toplevel()
        sponsor_root.geometry("300x200")
        sponsor_root.title("Sponsor")

        title_label = tk.Label(sponsor_root, text="Support Us", font=("Arial", 16))
        title_label.pack(pady=10)

        def open_patreon():
            import webbrowser
            webbrowser.open("https://www.patreon.com/Nsfr750")

        def open_github():
            import webbrowser
            webbrowser.open("https://github.com/sponsors/Nsfr750")

        def open_discord():
            import webbrowser
            webbrowser.open("https://discord.gg/BvvkUEP9")

        def open_paypal():
            import webbrowser
            webbrowser.open("https://paypal.me/3dmega")

        # Create and place buttons
        patreon_button = tk.Button(sponsor_root, text="Join the Patreon!", command=open_patreon)
        patreon_button.pack(pady=5)

        github_button = tk.Button(sponsor_root, text="GitHub", command=open_github)
        github_button.pack(pady=5)

        discord_button = tk.Button(sponsor_root, text="Discord", command=open_discord)
        discord_button.pack(pady=5)

        paypal_button = tk.Button(sponsor_root, text="Paypal", command=open_paypal)
        paypal_button.pack(pady=5)

        sponsor_root.mainloop()
        
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Import the core functionality from the CLI version
from email_duplicate_cleaner import (
    EmailClientManager, DuplicateEmailFinder, create_test_mailbox,
    BaseEmailClientHandler, ThunderbirdMailHandler, AppleMailHandler,
    OutlookHandler, GenericMailHandler
)

class RedirectText:
    """Redirect print statements to the GUI console"""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.queue = queue.Queue()
        self.updating = True
        self.update_me()
        
    def write(self, string):
        self.queue.put(string)
        
    def flush(self):
        pass
        
    def update_me(self):
        if not self.updating:
            return
        try:
            while True:
                # Get output from queue
                string = self.queue.get_nowait()
                
                # Update text widget with output
                self.text_widget.configure(state="normal")
                self.text_widget.insert(tk.END, string)
                self.text_widget.see(tk.END)  # Auto-scroll to the end
                self.text_widget.configure(state="disabled")
                self.queue.task_done()
        except queue.Empty:
            pass
        
        # Schedule to check queue again after 100 ms
        self.text_widget.after(100, self.update_me)
    
    def stop(self):
        self.updating = False

class EmailCleanerGUI:
    """Main GUI Application for Email Duplicate Cleaner"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Email Duplicate Cleaner")
        self.root.geometry("950x650")
        self.root.minsize(800, 600)
        
        # Set up instance variables
        self.client_manager = EmailClientManager()
        self.duplicate_finder = DuplicateEmailFinder()
        self.mail_folders = []
        self.folder_listbox = None
        self.selected_folders = []
        self.duplicate_groups = []
        self.scanning_thread = None
        self.cleaning_thread = None
        self.stdout_redirect = None
        self.temp_dir = None
        
        # Create the main frame structure
        self.create_main_frame()
        
        # Create the menu bar
        self.create_menu()
        
        # Create tabs
        self.create_tabs()
        
        # Create the output console
        self.create_console()
        
        # Configure app appearance
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TCheckbutton', font=('Arial', 10))
        self.style.configure('TRadiobutton', font=('Arial', 10))
        
        # Redirect stdout to our console
        self.stdout_redirect = RedirectText(self.console)
        sys.stdout = self.stdout_redirect
        
        # Set initial status
        self.set_status("Ready")
    
    def create_main_frame(self):
        """Create the main frame structure"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid layout (2 rows, 1 column)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)  # Tab content
        self.main_frame.rowconfigure(1, weight=0)  # Status bar
        
        # Add status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, 
                                    relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def create_menu(self):
        """Create the application menu bar"""
        menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Scan Custom Folder", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Run Demo Mode", command=self.run_demo_mode)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # View menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        self.dark_mode_var = tk.BooleanVar(value=False)
        self.debug_mode_var = tk.BooleanVar(value=False)
        view_menu.add_checkbutton(label="Dark Mode", variable=self.dark_mode_var, command=self.toggle_dark_mode)
        view_menu.add_checkbutton(label="Debug Mode", variable=self.debug_mode_var, command=self.toggle_debug_mode)
        menu_bar.add_cascade(label="View", menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Help", command=self.show_help)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # Sponsor menu
        sponsor_menu = tk.Menu(menu_bar, tearoff=0)
        sponsor = Sponsor()
        sponsor_menu.add_command(label="Sponsor Us", command=sponsor.show_sponsor_window)
        menu_bar.add_cascade(label="Sponsor", menu=sponsor_menu)

        self.root.config(menu=menu_bar)
    
    def create_tabs(self):
        """Create the main tab structure"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Create Scan tab
        self.scan_tab = ttk.Frame(self.notebook, padding="10")
        
        # Create Results tab
        self.results_tab = ttk.Frame(self.notebook, padding="10")
        
        # Add tabs to notebook
        self.notebook.add(self.scan_tab, text="Scan")
        self.notebook.add(self.results_tab, text="Results")
        
        # Set up the Scan tab content
        self.setup_scan_tab()
        
        # Set up the Results tab content
        self.setup_results_tab()
    
    def setup_scan_tab(self):
        """Set up the content for the Scan tab"""
        # Configure grid
        self.scan_tab.columnconfigure(0, weight=0)  # Label column
        self.scan_tab.columnconfigure(1, weight=1)  # Content column
        
        # Client selection
        ttk.Label(self.scan_tab, text="Email Client:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.client_var = tk.StringVar(value="all")
        client_frame = ttk.Frame(self.scan_tab)
        client_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Radiobutton(client_frame, text="All Clients", value="all", 
                      variable=self.client_var).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(client_frame, text="Thunderbird", value="thunderbird", 
                      variable=self.client_var).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(client_frame, text="Apple Mail", value="apple_mail", 
                      variable=self.client_var).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(client_frame, text="Outlook", value="outlook", 
                      variable=self.client_var).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(client_frame, text="Generic", value="generic", 
                      variable=self.client_var).pack(side=tk.LEFT, padx=5)
        
        # Duplicate detection criteria
        ttk.Label(self.scan_tab, text="Detection Criteria:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.criteria_var = tk.StringVar(value="strict")
        criteria_frame = ttk.Frame(self.scan_tab)
        criteria_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Radiobutton(criteria_frame, text="Strict", value="strict", 
                      variable=self.criteria_var).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(criteria_frame, text="Content Only", value="content", 
                      variable=self.criteria_var).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(criteria_frame, text="Headers", value="headers", 
                      variable=self.criteria_var).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(criteria_frame, text="Subject+Sender", value="subject-sender", 
                      variable=self.criteria_var).pack(side=tk.LEFT, padx=5)
        
        # Mail folder list
        ttk.Label(self.scan_tab, text="Mail Folders:").grid(row=2, column=0, sticky=tk.NW, pady=5)
        folder_frame = ttk.Frame(self.scan_tab)
        folder_frame.grid(row=2, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5)
        self.scan_tab.rowconfigure(2, weight=1)
        
        folder_frame.columnconfigure(0, weight=1)
        folder_frame.rowconfigure(0, weight=1)
        
        # Create folder listbox with scrollbar
        self.folder_listbox = tk.Listbox(folder_frame, selectmode=tk.MULTIPLE, height=10)
        scrollbar = ttk.Scrollbar(folder_frame, orient=tk.VERTICAL, command=self.folder_listbox.yview)
        self.folder_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.folder_listbox.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Button frame
        button_frame = ttk.Frame(self.scan_tab)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.auto_clean_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(button_frame, text="Auto-clean (keep oldest emails)", 
                       variable=self.auto_clean_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Find Folders", command=self.find_mail_folders).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Select All", command=self.select_all_folders).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Scan Selected", command=self.scan_selected_folders).pack(side=tk.LEFT, padx=5)
    
    def setup_results_tab(self):
        """Set up the content for the Results tab"""
        # Configure grid
        self.results_tab.columnconfigure(0, weight=1)
        self.results_tab.rowconfigure(0, weight=1)
        self.results_tab.rowconfigure(1, weight=0)
        
        # Results treeview
        self.results_frame = ttk.Frame(self.results_tab)
        self.results_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5)
        
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        
        # Create treeview with scrollbar
        self.results_tree = ttk.Treeview(self.results_frame, columns=("date", "from", "subject", "folder"),
                                    show="tree headings", selectmode="extended")
        
        # Set column headings
        self.results_tree.heading("#0", text="Group")
        self.results_tree.column("#0", width=60, stretch=False)
        self.results_tree.heading("date", text="Date")
        self.results_tree.column("date", width=120, stretch=False)
        self.results_tree.heading("from", text="From")
        self.results_tree.column("from", width=150)
        self.results_tree.heading("subject", text="Subject")
        self.results_tree.column("subject", width=200)
        self.results_tree.heading("folder", text="Folder")
        self.results_tree.column("folder", width=180)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=y_scrollbar.set)
        
        x_scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(xscrollcommand=x_scrollbar.set)
        
        # Place treeview and scrollbars
        self.results_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        y_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        x_scrollbar.grid(row=1, column=0, sticky=(tk.E, tk.W))
        
        # Add right-click menu for viewing email content
        self.email_menu = tk.Menu(self.results_tree, tearoff=0)
        self.email_menu.add_command(label="View Email Content", command=self.view_email_content)
        
        # Bind right-click and double-click events
        self.results_tree.bind("<Button-3>", self.show_email_menu)
        self.results_tree.bind("<Double-1>", self.on_item_double_click)
        
        # Print debug information
        print(f"Treeview initialized: {self.results_tree}")
        
        # Button frame
        button_frame = ttk.Frame(self.results_tab)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Group management buttons
        group_buttons_frame = ttk.LabelFrame(button_frame, text="Group Management")
        group_buttons_frame.pack(side=tk.LEFT, padx=10, fill=tk.X)
        
        ttk.Button(group_buttons_frame, text="Expand All Groups", 
                  command=self.expand_all_groups).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(group_buttons_frame, text="Collapse All Groups", 
                  command=self.collapse_all_groups).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Email action buttons
        action_buttons_frame = ttk.LabelFrame(button_frame, text="Email Actions")
        action_buttons_frame.pack(side=tk.LEFT, padx=10, fill=tk.X)
        
        ttk.Button(action_buttons_frame, text="View Selected Email", 
                  command=self.view_email_content).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(action_buttons_frame, text="Clean Selected Groups", 
                  command=self.clean_selected_groups).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(action_buttons_frame, text="Clean All Groups", 
                  command=self.clean_all_groups).pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_console(self):
        """Create the output console area"""
        console_frame = ttk.LabelFrame(self.main_frame, text="Console Output")
        console_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.S), pady=5)
        
        # Configure the frame
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        
        # Create the console with scrollbars
        self.console = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD, 
                                              height=6, width=80,
                                              bg="black", fg="white")
        self.console.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.console.configure(state="disabled")  # Read-only
    
    def set_status(self, message):
        """Update the status bar message"""
        self.status_var.set(message)
    
    def find_mail_folders(self):
        """Find mail folders for the selected email client"""
        self.folder_listbox.delete(0, tk.END)
        self.set_status("Searching for mail folders...")
        
        def search_folders():
            client = self.client_var.get()
            
            try:
                if client == "all":
                    self.mail_folders = self.client_manager.get_all_mail_folders()
                else:
                    self.mail_folders = self.client_manager.get_client_folders(client)
                
                # Update UI in the main thread
                self.root.after(0, self.update_folder_list)
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Error finding mail folders: {str(e)}"))
        
        # Run in a separate thread to keep UI responsive
        threading.Thread(target=search_folders, daemon=True).start()
    
    def update_folder_list(self):
        """Update the folder listbox with found mail folders"""
        if not self.mail_folders:
            self.set_status("No mail folders found")
            return
        
        for folder in self.mail_folders:
            self.folder_listbox.insert(tk.END, folder['display_name'])
        
        self.set_status(f"Found {len(self.mail_folders)} mail folders")
    
    def select_all_folders(self):
        """Select all folders in the listbox"""
        self.folder_listbox.selection_set(0, tk.END)
    
    def scan_selected_folders(self):
        """Scan selected folders for duplicate emails"""
        selections = self.folder_listbox.curselection()
        
        if not selections:
            messagebox.showwarning("No Selection", "Please select at least one folder to scan")
            return
        
        # Get selected folders
        self.selected_folders = [self.mail_folders[i] for i in selections]
        
        # Clear previous results
        self.results_tree.delete(*self.results_tree.get_children())
        
        # Switch to results tab
        self.notebook.select(1)
        
        # Start scanning thread
        self.set_status(f"Scanning {len(self.selected_folders)} folders...")
        
        def scan_folders():
            self.duplicate_groups = []
            criteria = self.criteria_var.get()
            
            try:
                for folder in self.selected_folders:
                    print(f"Scanning folder: {folder['display_name']}")
                    groups = self.duplicate_finder.scan_folder(folder, criteria)
                    
                    if groups:
                        for group in groups:
                            self.duplicate_groups.append(group)
                
                # Update UI in the main thread
                self.root.after(0, self.update_results_tree)
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Error scanning folders: {str(e)}"))
        
        self.scanning_thread = threading.Thread(target=scan_folders, daemon=True)
        self.scanning_thread.start()
    
    def update_results_tree(self):
        """Update the results treeview with scanning results"""
        if not self.duplicate_groups:
            self.set_status("No duplicate emails found")
            return
        
        total_dupes = sum(group['count'] - 1 for group in self.duplicate_groups)
        
        for i, group in enumerate(self.duplicate_groups):
            # Create group parent node
            group_id = f"Group {i+1}"
            group_node = self.results_tree.insert("", "end", text=group_id, open=True,
                                           values=("", "", f"{len(group['messages'])} emails", ""))
            
            # Add each email in the group
            for j, email_info in enumerate(group['messages']):
                email_node_id = f"group_{i}_{j}"
                
                # Mark the original email
                prefix = "(orig) " if j == 0 else ""
                
                self.results_tree.insert(
                    group_node, "end", iid=email_node_id,
                    text=f"{j+1}",
                    values=(
                        email_info['date'],
                        email_info['from'],
                        prefix + email_info['subject'],
                        email_info['folder']
                    )
                )
        
        self.set_status(f"Found {len(self.duplicate_groups)} duplicate groups with {total_dupes} duplicate emails")
    
    def clean_selected_groups(self):
        """Clean duplicates from selected groups"""
        selected_items = self.results_tree.selection()
        
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select groups to clean")
            return
        
        # Find selected group indices
        group_indices = set()
        for item_id in selected_items:
            # Only process top-level items (groups)
            if self.results_tree.parent(item_id) == "":
                group_index = int(self.results_tree.item(item_id)['text'].split()[1]) - 1
                group_indices.add(group_index)
            else:
                # If an email is selected, get its group
                parent_id = self.results_tree.parent(item_id)
                if parent_id and self.results_tree.parent(parent_id) == "":
                    group_index = int(self.results_tree.item(parent_id)['text'].split()[1]) - 1
                    group_indices.add(group_index)
        
        if not group_indices:
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion", 
                                 "Are you sure you want to delete duplicates from the selected groups?\n"
                                 "This will keep the oldest email in each group."):
            return
        
        # Start cleaning thread
        self.set_status(f"Cleaning {len(group_indices)} groups...")
        
        def clean_groups():
            try:
                deleted, errors = self.duplicate_finder.delete_duplicates(
                    list(group_indices), selection_method='keep-first'
                )
                
                # Update UI in the main thread
                self.root.after(0, lambda: self.update_after_cleaning(deleted, errors))
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Error cleaning duplicates: {str(e)}"))
        
        self.cleaning_thread = threading.Thread(target=clean_groups, daemon=True)
        self.cleaning_thread.start()
    
    def clean_all_groups(self):
        """Clean duplicates from all groups"""
        if not self.duplicate_groups:
            messagebox.showwarning("No Duplicates", "No duplicate groups to clean")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion", 
                                 "Are you sure you want to delete duplicates from all groups?\n"
                                 "This will keep the oldest email in each group."):
            return
        
        # Start cleaning thread
        self.set_status(f"Cleaning all {len(self.duplicate_groups)} groups...")
        
        def clean_all():
            try:
                deleted, errors = self.duplicate_finder.delete_duplicates(
                    list(range(len(self.duplicate_groups))), selection_method='keep-first'
                )
                
                # Update UI in the main thread
                self.root.after(0, lambda: self.update_after_cleaning(deleted, errors))
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Error cleaning duplicates: {str(e)}"))
        
        self.cleaning_thread = threading.Thread(target=clean_all, daemon=True)
        self.cleaning_thread.start()
    
    def update_after_cleaning(self, deleted, errors):
        """Update the UI after cleaning duplicates"""
        if errors:
            error_msg = f"Deleted {deleted} duplicate emails with {len(errors)} errors"
            self.set_status(error_msg)
            
            detailed_errors = "\n".join(errors[:10])
            if len(errors) > 10:
                detailed_errors += f"\n... and {len(errors) - 10} more errors"
            
            messagebox.showwarning("Cleaning Errors", 
                                 f"{error_msg}\n\nErrors:\n{detailed_errors}")
        else:
            success_msg = f"Successfully deleted {deleted} duplicate emails"
            self.set_status(success_msg)
            messagebox.showinfo("Cleaning Complete", success_msg)
        
        # Remove cleaned groups and rescan
        self.scan_selected_folders()
    
    def open_folder(self):
        """Open a custom folder for scanning"""
        folder_path = filedialog.askdirectory(title="Select Mail Folder")
        
        if folder_path:
            self.mail_folders = []
            self.folder_listbox.delete(0, tk.END)
            
            # Create a generic mail handler for this path
            custom_handler = GenericMailHandler()
            custom_handler.profile_paths = [folder_path]
            
            try:
                self.mail_folders = custom_handler.find_mail_folders()
                self.update_folder_list()
            except Exception as e:
                self.show_error(f"Error scanning folder: {str(e)}")
    
    def run_demo_mode(self):
        """Run the application in demo mode with test emails"""
        try:
            if messagebox.askyesno("Demo Mode", 
                                 "This will create a temporary mailbox with sample emails for demonstration.\n"
                                 "Would you like to continue?"):
                print("Running in demo mode with test emails...")
                
                # Create test mailbox
                self.temp_dir, profile_path = create_test_mailbox()
                
                # Set up a generic mail handler for this path
                custom_handler = GenericMailHandler()
                custom_handler.profile_paths = [profile_path]
                
                # Clear previous folders and find new ones
                self.mail_folders = []
                self.folder_listbox.delete(0, tk.END)
                
                self.mail_folders = custom_handler.find_mail_folders()
                self.update_folder_list()
                
                # Select all folders
                self.select_all_folders()
                
                # Notify user
                messagebox.showinfo("Demo Mode", 
                                  "Demo mailbox created. All folders are selected.\n"
                                  "Click 'Scan Selected' to find duplicates.")
        except Exception as e:
            self.show_error(f"Error setting up demo mode: {str(e)}")
    
    def toggle_dark_mode(self):
        """Toggle dark mode theme"""
        is_dark = self.dark_mode_var.get()
        bg_color = '#1a1a1a' if is_dark else '#ffffff'
        fg_color = '#e0e0e0' if is_dark else '#000000'
        selected_bg = '#404040' if is_dark else '#0078d7'
        
        self.root.configure(bg=bg_color)
        
        # Update all frames and widgets
        for widget in self.root.winfo_children():
            if isinstance(widget, (ttk.Frame, ttk.LabelFrame)):
                widget.configure(style='Dark.TFrame' if is_dark else 'TFrame')
            elif isinstance(widget, ttk.Label):
                widget.configure(style='Dark.TLabel' if is_dark else 'TLabel')
            elif isinstance(widget, ttk.Button):
                widget.configure(style='Dark.TButton' if is_dark else 'TButton')
                
        # Update styles
        self.style.configure('Dark.TFrame', background=bg_color)
        self.style.configure('Dark.TLabel', background=bg_color, foreground=fg_color)
        self.style.configure('Dark.TButton', background=selected_bg)
        
        # Update console colors
        self.console.configure(bg='#1a1a1a' if is_dark else '#ffffff',
                             fg='#00ff00' if is_dark else '#000000')

    def toggle_debug_mode(self):
        """Toggle debug mode"""
        is_debug = self.debug_mode_var.get()
        if is_debug:
            print("Debug mode enabled")
            # Enable detailed logging
            logging.getLogger().setLevel(logging.DEBUG)
            self.set_status("Debug mode enabled")
        else:
            print("Debug mode disabled")
            # Disable detailed logging
            logging.getLogger().setLevel(logging.INFO)
            self.set_status("Debug mode disabled")

    def show_error(self, message):
        """Show an error message"""
        print(f"ERROR: {message}")
        messagebox.showerror("Error", message)
        self.set_status("Error: " + message)
    
    def show_about(self):
        """Show the about dialog"""
        about_text = """Email Duplicate Cleaner

Version 2.2.3

A tool to scan, identify, and remove duplicate emails
from various email clients.

Supported Email Clients:
- Mozilla Thunderbird
- Apple Mail
- Microsoft Outlook
- Generic mbox/maildir formats

© 2025 by Nsfr750"""
        
        messagebox.showinfo("About Email Duplicate Cleaner", about_text)
    
    def show_help(self):
        """Show the help dialog"""
        help_text = """Email Duplicate Cleaner - Help

1. Select an email client or "All Clients"
2. Choose duplicate detection criteria
3. Click "Find Folders" to locate mail folders
4. Select folders you want to scan
5. Click "Scan Selected" to find duplicates
6. Review duplicate groups in the Results tab
7. Double-click on any email or click "View Selected Email" to view the full content
8. Select groups and click "Clean Selected Groups" 
   or "Clean All Groups" to remove duplicates

Detection Criteria:
- Strict: Uses Message-ID, Date, From, Subject, and content
- Content Only: Only compares message content
- Headers: Uses Message-ID, Date, From, and Subject
- Subject+Sender: Only compares Subject and From fields

Note: The tool always keeps at least one copy of each email.
You can also right-click on any email to view its full content."""
        
        messagebox.showinfo("Help", help_text)
    
    def expand_all_groups(self):
        """Expand all groups in the results tree"""
        try:
            print("Expanding all groups...")
            children = self.results_tree.get_children()
            print(f"Found {len(children)} top-level items")
            
            for item in children:
                print(f"Expanding item: {self.results_tree.item(item, 'text')}")
                self.results_tree.item(item, open=True)
                
            self.set_status("All groups expanded")
        except Exception as e:
            print(f"Error expanding groups: {e}")
            self.show_error(f"Error expanding groups: {str(e)}")
    
    def collapse_all_groups(self):
        """Collapse all groups in the results tree"""
        try:
            print("Collapsing all groups...")
            children = self.results_tree.get_children()
            print(f"Found {len(children)} top-level items")
            
            for item in children:
                print(f"Collapsing item: {self.results_tree.item(item, 'text')}")
                self.results_tree.item(item, open=False)
                
            self.set_status("All groups collapsed")
        except Exception as e:
            print(f"Error collapsing groups: {e}")
            self.show_error(f"Error collapsing groups: {str(e)}")
        
    def show_email_menu(self, event):
        """Show the context menu for email items"""
        # Get the item under cursor
        item = self.results_tree.identify_row(event.y)
        if item:
            # Only show menu for email items (not group items)
            if self.results_tree.parent(item) != "":
                self.results_tree.selection_set(item)
                self.email_menu.post(event.x_root, event.y_root)
    
    def on_item_double_click(self, event):
        """Handle double-click on tree items"""
        # Get the item under cursor
        item = self.results_tree.identify_row(event.y)
        if not item:
            return
            
        # If it's a group item (parent is ""), toggle expand/collapse
        if self.results_tree.parent(item) == "":
            # Check if the item is already open
            if self.results_tree.item(item, "open"):
                self.results_tree.item(item, open=False)  # Collapse
            else:
                self.results_tree.item(item, open=True)   # Expand
                
        # If it's an email item (has a parent), view the email content
        else:
            self.results_tree.selection_set(item)
            self.view_email_content()
    
    def view_email_content(self):
        """View the content of the selected email"""
        selected_items = self.results_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an email to view")
            return
        
        # Get the first selected item
        item_id = selected_items[0]
        
        # Only proceed if it's an email item (not a group)
        if self.results_tree.parent(item_id) == "":
            messagebox.showwarning("Invalid Selection", "Please select an email (not a group) to view")
            return
        
        # Get the parent item (group) and the index in the group
        parent_id = self.results_tree.parent(item_id)
        group_text = self.results_tree.item(parent_id)['text']  # "Group X"
        
        # Get group index (X-1 because our display is 1-based, but code is 0-based)
        group_idx = int(group_text.split()[1]) - 1
        
        # Get email index from the item text
        email_idx_text = self.results_tree.item(item_id)['text']  # "Y"
        email_idx = int(email_idx_text) - 1  # Convert to 0-based index
        
        try:
            # Get email content
            email_content = self.duplicate_finder.get_email_content(group_idx, email_idx)
            
            # Create email viewer window
            viewer = tk.Toplevel(self.root)
            viewer.title(f"Email Content - {self.duplicate_groups[group_idx]['messages'][email_idx]['subject']}")
            viewer.geometry("700x500")
            viewer.minsize(500, 400)
            
            # Make it modal
            viewer.transient(self.root)
            viewer.grab_set()
            
            # Configure grid
            viewer.columnconfigure(0, weight=1)
            viewer.rowconfigure(1, weight=1)
            
            # Header frame
            header_frame = ttk.LabelFrame(viewer, text="Email Headers", padding="5")
            header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
            
            # Add header information
            email_info = self.duplicate_groups[group_idx]['messages'][email_idx]
            headers = [
                ("From:", email_info['from']),
                ("To:", email_info.get('to', 'N/A')),
                ("Date:", email_info['date']),
                ("Subject:", email_info['subject']),
                ("Folder:", email_info['folder'])
            ]
            
            for i, (label, value) in enumerate(headers):
                ttk.Label(header_frame, text=label, font=('Arial', 10, 'bold')).grid(
                    row=i, column=0, sticky=tk.W, padx=(0, 10))
                ttk.Label(header_frame, text=value, wraplength=500).grid(
                    row=i, column=1, sticky=tk.W)
            
            # Content frame
            content_frame = ttk.LabelFrame(viewer, text="Email Content", padding="5")
            content_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
            content_frame.columnconfigure(0, weight=1)
            content_frame.rowconfigure(0, weight=1)
            
            # Email content text widget
            content_text = scrolledtext.ScrolledText(
                content_frame, wrap=tk.WORD, font=('Arial', 10),
                width=80, height=20
            )
            content_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
            
            # Insert email content
            if isinstance(email_content, bytes):
                try:
                    email_content = email_content.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        email_content = email_content.decode('latin-1')
                    except UnicodeDecodeError:
                        email_content = str(email_content)
            
            content_text.insert('1.0', email_content)
            content_text.configure(state='disabled')  # Make read-only
            
            # Button frame
            button_frame = ttk.Frame(viewer)
            button_frame.grid(row=2, column=0, sticky=(tk.E, tk.W), padx=5, pady=5)
            
            # Close button
            ttk.Button(button_frame, text="Close", command=viewer.destroy).pack(side=tk.RIGHT)
            
            # Center the window on screen
            viewer.update_idletasks()
            width = viewer.winfo_width()
            height = viewer.winfo_height()
            x = (viewer.winfo_screenwidth() // 2) - (width // 2)
            y = (viewer.winfo_screenheight() // 2) - (height // 2)
            viewer.geometry(f"{width}x{height}+{x}+{y}")
            
            # Set focus to the viewer window
            viewer.focus_set()
            
        except Exception as e:
            self.show_error(f"Error viewing email content: {str(e)}")
    
    def show_sponsor_menu(self):
        """Display the Sponsor window"""
        sponsor = Sponsor()
        sponsor.show_sponsor_window()
        
    def on_closing(self):
        """Clean up when closing the application"""
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # Stop redirect thread
        if self.stdout_redirect:
            self.stdout_redirect.stop()
        
        # Remove temp directory if in demo mode
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
                print("Cleaned up demo environment")
            except Exception:
                pass
        
        self.root.destroy()


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = EmailCleanerGUI(root)
    
    # Set up clean exit
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
