#!/usr/bin/env python3
"""
Email Duplicate Cleaner - GUI Interface

A graphical user interface for the Email Duplicate Cleaner tool.
"""

import os
import sys
import logging
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, scrolledtext, Toplevel
import queue
import sqlite3
import webbrowser
from struttura.sponsor import Sponsor
from lang.lang import lang_manager, get_string
from struttura.logger import setup_logging
from struttura.traceback import setup_traceback_handler
from struttura.log_viewer import LogViewer
from struttura.about import About
from struttura.help import Help
from struttura.sponsor import Sponsor
from struttura.menu import AppMenu
from email_duplicate_cleaner import (
    EmailClientManager, DuplicateEmailFinder, create_test_mailbox,
    BaseEmailClientHandler, ThunderbirdMailHandler, AppleMailHandler,
    OutlookHandler, GenericMailHandler
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
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
        self.root.title(get_string('app_title'))
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
        self.language_var = tk.StringVar(value=lang_manager.language)
        self.debug_var = tk.BooleanVar(value=False)
        self.dark_mode_var = tk.BooleanVar(value=False)
        self.menu = None
        
        # Setup logging and exception handling
        self.log_queue = setup_logging()
        setup_traceback_handler()
        logging.info("Application started.")

        # Create the main frame structure
        self.create_main_frame()
        
        # Create the menu bar
        self.menu = AppMenu(self)
        
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
        self.set_status(get_string('ready_status'))

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
    
    def create_tabs(self):
        """Create the main tab structure"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Create Scan tab
        self.scan_tab = ttk.Frame(self.notebook, padding="10")
        
        # Create Results tab
        self.results_tab = ttk.Frame(self.notebook, padding="10")
        
        # Add tabs to notebook
        self.notebook.add(self.scan_tab, text=get_string("tab_scan"))
        self.notebook.add(self.results_tab, text=get_string("tab_results"))
        
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
        self.client_frame = ttk.LabelFrame(self.scan_tab, text=get_string('scan_client_frame'))
        self.client_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.client_var = tk.StringVar(value="all")
        self.radio_client_all = ttk.Radiobutton(self.client_frame, text=get_string('scan_client_all_radio'), value="all", 
                      variable=self.client_var)
        self.radio_client_all.pack(side=tk.LEFT, padx=5)
        self.radio_client_tb = ttk.Radiobutton(self.client_frame, text=get_string('scan_client_thunderbird_radio'), value="thunderbird", 
                      variable=self.client_var)
        self.radio_client_tb.pack(side=tk.LEFT, padx=5)
        self.radio_client_am = ttk.Radiobutton(self.client_frame, text=get_string('scan_client_apple_mail_radio'), value="apple_mail", 
                      variable=self.client_var)
        self.radio_client_am.pack(side=tk.LEFT, padx=5)
        self.radio_client_ol = ttk.Radiobutton(self.client_frame, text=get_string('scan_client_outlook_radio'), value="outlook", 
                      variable=self.client_var)
        self.radio_client_ol.pack(side=tk.LEFT, padx=5)
        self.radio_client_gen = ttk.Radiobutton(self.client_frame, text=get_string('scan_client_generic_radio'), value="generic", 
                      variable=self.client_var)
        self.radio_client_gen.pack(side=tk.LEFT, padx=5)
        
        # Duplicate detection criteria
        self.criteria_frame = ttk.LabelFrame(self.scan_tab, text=get_string('scan_criteria_frame'))
        self.criteria_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.criteria_var = tk.StringVar(value="strict")
        self.radio_crit_strict = ttk.Radiobutton(self.criteria_frame, text=get_string('scan_criteria_strict_radio'), value="strict", 
                      variable=self.criteria_var)
        self.radio_crit_strict.pack(side=tk.LEFT, padx=5)
        self.radio_crit_content = ttk.Radiobutton(self.criteria_frame, text=get_string('scan_criteria_content_radio'), value="content", 
                      variable=self.criteria_var)
        self.radio_crit_content.pack(side=tk.LEFT, padx=5)
        self.radio_crit_headers = ttk.Radiobutton(self.criteria_frame, text=get_string('scan_criteria_headers_radio'), value="headers", 
                      variable=self.criteria_var)
        self.radio_crit_headers.pack(side=tk.LEFT, padx=5)
        self.radio_crit_subj_send = ttk.Radiobutton(self.criteria_frame, text=get_string('scan_criteria_subject_sender_radio'), value="subject-sender", 
                      variable=self.criteria_var)
        self.radio_crit_subj_send.pack(side=tk.LEFT, padx=5)
        
        # Mail folder list
        self.folder_frame = ttk.LabelFrame(self.scan_tab, text=get_string('scan_folder_frame'))
        self.folder_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
        self.scan_tab.rowconfigure(2, weight=1)
        self.folder_frame.columnconfigure(0, weight=1)
        self.folder_frame.rowconfigure(0, weight=1)

        self.folder_listbox = tk.Listbox(self.folder_frame, selectmode=tk.EXTENDED, exportselection=False)
        self.folder_listbox.grid(row=0, column=0, sticky='nsew')

        y_scrollbar = ttk.Scrollbar(self.folder_frame, orient=tk.VERTICAL, command=self.folder_listbox.yview)
        self.folder_listbox.configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Action buttons for scan tab
        button_frame = ttk.Frame(self.scan_tab)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.auto_clean_var = tk.BooleanVar(value=False)
        self.check_auto_clean = ttk.Checkbutton(button_frame, text=get_string('scan_autoclean_checkbox'), 
                       variable=self.auto_clean_var)
        self.check_auto_clean.pack(side=tk.LEFT, padx=5)
        
        self.find_folders_button = ttk.Button(button_frame, text=get_string('scan_find_folders_button'), 
                                                command=self.find_mail_folders)
        self.find_folders_button.pack(side=tk.LEFT, padx=5)
        
        self.select_all_button = ttk.Button(button_frame, text=get_string('scan_select_all_button'), 
                                              command=self.select_all_folders)
        self.select_all_button.pack(side=tk.LEFT, padx=5)
        
        self.scan_button = ttk.Button(button_frame, text=get_string('scan_button'), 
                                        command=self.scan_selected_folders)
        self.scan_button.pack(side=tk.LEFT, padx=5)
    
    def setup_results_tab(self):
        """Set up the content for the Results tab"""
        # Configura la griglia: 1 riga, 2 colonne
        self.results_tab.columnconfigure(0, weight=3)
        self.results_tab.columnconfigure(1, weight=2)
        self.results_tab.rowconfigure(0, weight=1)
        self.results_tab.rowconfigure(1, weight=0)

        # Frame risultati (sinistra)
        self.results_frame = ttk.Frame(self.results_tab)
        self.results_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5)
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)

        # Treeview con scrollbar
        self.results_tree = ttk.Treeview(
            self.results_frame,
            columns=("date", "from", "subject", "folder"),
            show="tree headings", selectmode="extended"
        )
        self.results_tree.heading("#0", text=get_string('header_group'))
        self.results_tree.column("#0", width=60, stretch=False)
        self.results_tree.heading("date", text=get_string('header_date'))
        self.results_tree.column("date", width=120, stretch=False)
        self.results_tree.heading("from", text=get_string('header_from'))
        self.results_tree.column("from", width=150)
        self.results_tree.heading("subject", text=get_string('header_subject'))
        self.results_tree.column("subject", width=200)
        self.results_tree.heading("folder", text=get_string('header_folder'))
        self.results_tree.column("folder", width=180)

        y_scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=y_scrollbar.set)
        x_scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(xscrollcommand=x_scrollbar.set)

        self.results_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        y_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        x_scrollbar.grid(row=1, column=0, sticky=(tk.E, tk.W))

        # Menu contestuale e binding eventi
        self.email_menu = tk.Menu(self.results_tree, tearoff=0)
        self.email_menu.add_command(label=get_string('menu_view_email'), command=self.view_email_content)
        self.results_tree.bind("<Button-3>", self.show_email_menu)
        self.results_tree.bind("<Double-1>", self.on_item_double_click)
        self.results_tree.bind("<<TreeviewSelect>>", self.update_preview_panel)

        # Frame anteprima (destra)
        self.preview_frame = ttk.Frame(self.results_tab, padding=5)
        self.preview_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.preview_frame.columnconfigure(0, weight=1)
        self.preview_frame.rowconfigure(1, weight=1)

        # Header
        self.preview_header = tk.Label(self.preview_frame, text=get_string('preview_header'), anchor="w", justify="left", font=("Arial", 10, "bold"))
        self.preview_header.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # Contenuto (ScrolledText)
        self.preview_text = scrolledtext.ScrolledText(self.preview_frame, wrap=tk.WORD, font=('Arial', 10), width=50, height=20, state="disabled")
        self.preview_text.grid(row=1, column=0, sticky="nsew")

        # Button frame (sotto)
        button_frame = ttk.Frame(self.results_tab)
        button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Group management buttons
        self.group_buttons_frame = ttk.LabelFrame(button_frame, text=get_string('group_management_frame'))
        self.group_buttons_frame.pack(side=tk.LEFT, padx=10, fill=tk.X)
        self.expand_all_button = ttk.Button(self.group_buttons_frame, text=get_string('expand_all_button'), command=self.expand_all_groups)
        self.expand_all_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.collapse_all_button = ttk.Button(self.group_buttons_frame, text=get_string('collapse_all_button'), command=self.collapse_all_groups)
        self.collapse_all_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Email action buttons
        self.action_buttons_frame = ttk.LabelFrame(button_frame, text=get_string('email_actions_frame'))
        self.action_buttons_frame.pack(side=tk.LEFT, padx=10, fill=tk.X)
        self.view_email_button = ttk.Button(self.action_buttons_frame, text=get_string('view_email_button'), command=self.view_email_content)
        self.view_email_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.clean_selected_button = ttk.Button(self.action_buttons_frame, text=get_string('clean_selected_button'), command=self.clean_selected_groups)
        self.clean_selected_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.clean_all_button = ttk.Button(self.action_buttons_frame, text=get_string('clean_all_button'), command=self.clean_all_groups)
        self.clean_all_button.pack(side=tk.LEFT, padx=5, pady=5)

    def update_preview_panel(self, event=None):
        """Updates the preview panel with the selected email's content."""
        self.preview_header.config(text="")
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", tk.END)

        selected = self.results_tree.selection()
        if not selected:
            self.preview_header.config(text=get_string('preview_header'))
            self.preview_text.config(state="disabled")
            return

        item_id = selected[0]
        
        # Only proceed if it's an email item (not a group)
        if self.results_tree.parent(item_id) == "":
            self.preview_header.config(text=get_string('preview_header_group_selected'))
            self.preview_text.config(state="disabled")
            return
        
        try:
            # Get the parent item (group) and the index in the group
            parent_id = self.results_tree.parent(item_id)
            group_idx = int(parent_id.split('_')[1])
            
            # Get email index from the item text
            email_idx_text = self.results_tree.item(item_id)['text']
            email_idx = int(email_idx_text) - 1

            # Get email info and content
            email_info = self.duplicate_groups[group_idx]['messages'][email_idx]
            email_content = self.duplicate_finder.get_email_content(group_idx, email_idx)

            # Update header
            header_text = (
                f"{get_string('header_from')}: {email_info['from']}\n"
                f"{get_string('header_to')}: {email_info.get('to', get_string('header_to_na'))}\n"
                f"{get_string('header_date')}: {email_info['date']}\n"
                f"{get_string('header_subject')}: {email_info['subject']}"
            )
            self.preview_header.config(text=header_text)

            # Update content
            if isinstance(email_content, bytes):
                try:
                    email_content = email_content.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        email_content = email_content.decode('latin-1')
                    except UnicodeDecodeError:
                        email_content = str(email_content)
            
            self.preview_text.insert('1.0', email_content)

        except (ValueError, IndexError, KeyError) as e:
            self.preview_header.config(text=get_string('preview_header_error'))
            self.preview_text.insert('1.0', f"{get_string('error_previewing_email')}\n\n{e}")
            logging.error(f"Error updating preview panel: {e}", exc_info=True)
        finally:
            self.preview_text.config(state="disabled")

    def create_console(self):
        """Create the output console area"""
        self.console_frame = ttk.LabelFrame(self.main_frame, text=get_string('console_frame_title'))
        self.console_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.S), pady=5)
        
        # Configure the frame
        self.console_frame.columnconfigure(0, weight=1)
        self.console_frame.rowconfigure(0, weight=1)
        
        # Create the console with scrollbars
        self.console = scrolledtext.ScrolledText(self.console_frame, wrap=tk.WORD, 
                                              height=6, width=80,
                                              bg="black", fg="white")
        self.console.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.console.configure(state="disabled")  # Read-only
    
    def set_status(self, message):
        """Update the status bar message"""
        self.status_var.set(message)
    
    def find_mail_folders(self):
        """Find mail folders for the selected email client"""
        logging.info("Finding mail folders for client: %s", self.client_var.get())
        self.folder_listbox.delete(0, tk.END)
        self.set_status(get_string('status_searching_folders'))

        def search_folders():
            try:
                client = self.client_var.get()
                logging.debug("Selected client: %s", client)
                
                if client == "all":
                    logging.info("Searching for all mail folders")
                    self.mail_folders = self.client_manager.get_all_mail_folders()
                else:
                    logging.info("Searching for folders for client: %s", client)
                    self.mail_folders = self.client_manager.get_client_folders(client)
                
                logging.info("Found %d folders", len(self.mail_folders))
                
                # Update UI in the main thread
                self.root.after(0, self.update_folder_list)
                
            except Exception as e:
                error_msg = get_string('error_finding_folders').format(error=str(e))
                logging.error(error_msg, exc_info=True)
                self.root.after(0, lambda: self.show_error(error_msg))
        
        # Run in a separate thread to keep UI responsive
        logging.debug("Starting folder search thread")
        threading.Thread(target=search_folders, daemon=True).start()
    
    def update_folder_list(self):
        """Update the folder listbox with found mail folders"""
        if not self.mail_folders:
            self.set_status(get_string('status_no_folders_found'))
            return
        
        for folder in self.mail_folders:
            self.folder_listbox.insert(tk.END, folder['display_name'])
        
        self.set_status(get_string('status_found_folders').format(count=len(self.mail_folders)))
    
    def select_all_folders(self):
        """Select all folders in the listbox"""
        self.folder_listbox.selection_set(0, tk.END)
    
    def scan_selected_folders(self):
        """Scan selected folders for duplicate emails"""
        logging.info("Starting folder scan")
        selections = self.folder_listbox.curselection()
        
        if not selections:
            logging.warning("No folders selected for scanning")
            messagebox.showwarning(get_string('no_selection_title'), get_string('no_folder_selection_message'))
            return
        
        # Get selected folders
        self.selected_folders = [self.mail_folders[i] for i in selections]
        logging.info("Scanning %d folders", len(self.selected_folders))
        
        # Clear previous results
        self.results_tree.delete(*self.results_tree.get_children())

        # Switch to results tab
        self.notebook.select(1)
        
        # Start scanning thread
        self.set_status(get_string('status_scanning_folders').format(count=len(self.selected_folders)))
        
        def scan_folders():
            try:
                self.duplicate_groups = []
                criteria = self.criteria_var.get()
                logging.info("Using scan criteria: %s", criteria)
                
                for folder in self.selected_folders:
                    logging.info("Scanning folder: %s", folder['display_name'])
                    groups = self.duplicate_finder.scan_folder(folder, criteria)
                    
                    if groups:
                        logging.info("Found %d duplicate groups in folder", len(groups))
                        for group in groups:
                            self.duplicate_groups.append(group)
                    else:
                        logging.info("No duplicates found in folder: %s", folder['display_name'])
                
                # Update UI in the main thread
                self.root.after(0, self.update_results_tree)
                
            except Exception as e:
                error_msg = get_string('error_scanning_folders').format(error=str(e))
                logging.error(error_msg, exc_info=True)
                self.root.after(0, lambda: self.show_error(error_msg))
        
        logging.debug("Starting scan thread")
        self.scanning_thread = threading.Thread(target=scan_folders, daemon=True)
        self.scanning_thread.start()
    
    def update_results_tree(self):
        """Update the results treeview with scanning results"""
        if not self.duplicate_groups:
            self.set_status(get_string('status_no_duplicates_found'))
            return
        
        total_dupes = sum(group['count'] - 1 for group in self.duplicate_groups)
        
        for i, group in enumerate(self.duplicate_groups):
            # Create group parent node
            group_id = get_string('group_prefix').format(index=i+1)
            group_node = self.results_tree.insert("", "end", iid=f"group_{i}", text=group_id, open=True,
                                           values=("", "", f"{len(group['messages'])} {get_string('emails_label')}", ""))
            
            # Add each email in the group
            for j, email_info in enumerate(group['messages']):
                email_node_id = f"group_{i}_{j}"

                # Mark the original email
                prefix = f"({get_string('original_prefix')}) " if j == 0 else ""

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
        
        self.set_status(get_string('status_found_duplicates').format(group_count=len(self.duplicate_groups), dupe_count=total_dupes))

    def clean_selected_groups(self):
        """Clean duplicates from selected groups"""
        logging.info("Starting group cleaning")
        selected_items = self.results_tree.selection()
        
        if not selected_items:
            logging.warning("No groups selected for cleaning")
            messagebox.showwarning(get_string('no_selection_title'), get_string('no_group_selection_message'))
            return

        # Find selected group indices
        group_indices = set()
        for item_id in selected_items:
            try:
                # Only process top-level items (groups)
                if self.results_tree.parent(item_id) == "":
                    group_index = int(item_id.split('_')[1])
                    group_indices.add(group_index)
                else:
                    # If an email is selected, get its group
                    parent_id = self.results_tree.parent(item_id)
                    if parent_id and parent_id.startswith("group_"):
                        group_index = int(parent_id.split('_')[1])
                        group_indices.add(group_index)
            except (ValueError, IndexError) as e:
                logging.error("Error processing selected item: %s", str(e))
                continue
        
        if not group_indices:
            logging.warning("No valid groups found for cleaning")
            messagebox.showwarning(get_string('no_valid_groups_title'), get_string('no_valid_groups_message'))
            return

        # Confirm deletion
        if not messagebox.askyesno(get_string('confirm_deletion_title'), 
                                  get_string('confirm_deletion_message')):
            logging.info("Cleaning cancelled by user")
            return

        # Start cleaning thread
        self.set_status(get_string('status_cleaning_groups').format(count=len(group_indices)))

        def clean_groups():
            try:
                deleted, errors = self.duplicate_finder.delete_duplicates(
                    list(group_indices), selection_method='keep-first'
                )
                logging.info("Deleted %d emails with %d errors", deleted, len(errors))
                
                # Update UI in the main thread
                self.root.after(0, lambda: self.update_after_cleaning(deleted, errors))
                
            except Exception as e:
                error_msg = get_string('error_cleaning_duplicates').format(error=str(e))
                logging.error(error_msg, exc_info=True)
                self.root.after(0, lambda: self.show_error(error_msg))
        
        logging.debug("Starting cleaning thread")
        self.cleaning_thread = threading.Thread(target=clean_groups, daemon=True)
        self.cleaning_thread.start()
    
    def clean_all_groups(self):
        """Clean duplicates from all groups"""
        if not self.duplicate_groups:
            messagebox.showwarning(get_string('no_duplicates_title'), get_string('no_duplicates_message'))
            return

        # Confirm deletion
        if not messagebox.askyesno(get_string('confirm_deletion_title'), 
                                 get_string('confirm_deletion_all_message')):
            return

        # Start cleaning thread
        self.set_status(get_string('status_cleaning_all_groups').format(count=len(self.duplicate_groups)))

        def clean_all():
            try:
                deleted, errors = self.duplicate_finder.delete_duplicates(
                    list(range(len(self.duplicate_groups))), selection_method='keep-first'
                )
                
                # Update UI in the main thread
                self.root.after(0, lambda: self.update_after_cleaning(deleted, errors))
            except Exception as e:
                self.root.after(0, lambda: self.show_error(get_string('error_cleaning_duplicates').format(error=str(e))))

        self.cleaning_thread = threading.Thread(target=clean_all, daemon=True)
        self.cleaning_thread.start()
    
    def update_after_cleaning(self, deleted, errors):
        """Update the UI after cleaning duplicates"""
        if errors:
            error_msg = get_string('cleaning_error_message').format(deleted=deleted, error_count=len(errors))
            self.set_status(error_msg)

            detailed_errors = "\n".join(errors[:10])
            if len(errors) > 10:
                detailed_errors += f"\n... and {len(errors) - 10} more errors"

            messagebox.showwarning(get_string('cleaning_errors_title'), 
                                 f"{error_msg}\n\n{get_string('errors_label')}:\n{detailed_errors}")
        else:
            success_msg = get_string('cleaning_success_message').format(deleted=deleted)
            self.set_status(success_msg)
            messagebox.showinfo(get_string('cleaning_complete_title'), success_msg)

        # Remove cleaned groups and rescan
        self.scan_selected_folders()
    
    def open_folder(self):
        """Open a custom folder for scanning"""
        folder_path = filedialog.askdirectory(title=get_string('dialog_select_folder_title'))

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
                self.show_error(get_string('error_scanning_folder').format(error=str(e)))

    def run_demo_mode(self):
        """Run the application in demo mode with test emails"""
        try:
            if messagebox.askyesno(get_string('demo_mode_title'), 
                                 get_string('demo_mode_confirm_message')):
                logging.info(get_string('demo_mode_running'))
                
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
                messagebox.showinfo(get_string('demo_mode_title'), 
                                  get_string('demo_mode_info_message'))
        except Exception as e:
            self.show_error(get_string('error_demo_mode').format(error=str(e)))
    
    def toggle_debug_mode(self):
        """Toggle debug mode"""
        is_debug = self.debug_var.get()
        if is_debug:
            logging.info(get_string('debug_mode_enabled'))
            # Enable detailed logging
            logging.getLogger().setLevel(logging.DEBUG)
            self.set_status(get_string('status_debug_enabled'))
        else:
            logging.info(get_string('debug_mode_disabled'))
            # Disable detailed logging
            logging.getLogger().setLevel(logging.INFO)
            self.set_status(get_string('status_debug_disabled'))

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

    def switch_language(self):
        """Switch the application language."""
        new_lang = self.language_var.get()
        lang_manager.set_language(new_lang)
        logging.info(f"Language switched to {new_lang}")
        # Removed the restart prompt so the change takes effect silently.
        self.set_status(get_string('ready_status'))

    def show_error(self, message):
        """Show an error message"""
        logging.error(message)
        messagebox.showerror(get_string('error_title'), message)
        self.set_status(f"{get_string('error_prefix')}: {message}")

    def report_bug(self):
        """Open the GitHub issues page in a browser"""
        webbrowser.open("https://github.com/Nsfr750/EmailDuplicateCleaner/issues")

    def on_closing(self):
        """Clean up when closing the application."""
        # Restore stdout
        if self.stdout_redirect:
            sys.stdout = sys.__stdout__
            self.stdout_redirect.stop()

        # Remove temp directory if in demo mode
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
                logging.info("Cleaned up demo environment.")
            except Exception as e:
                logging.error(get_string('error_cleanup_temp_dir').format(error=e))
        
        self.root.destroy()

    def expand_all_groups(self):
        """Expand all groups in the results tree"""
        try:
            logging.debug(get_string('expanding_all_groups'))
            children = self.results_tree.get_children()
            logging.debug(get_string('found_top_level_items').format(count=len(children)))
            
            for item in children:
                self.results_tree.item(item, open=True)
                
            self.set_status(get_string('status_all_groups_expanded'))
        except Exception as e:
            logging.error(f"Error expanding groups: {e}")
            self.show_error(get_string('error_expanding_groups').format(error=str(e)))

    def collapse_all_groups(self):
        """Collapse all groups in the results tree"""
        try:
            logging.debug(get_string('collapsing_all_groups'))
            children = self.results_tree.get_children()
            logging.debug(get_string('found_top_level_items').format(count=len(children)))
            
            for item in children:
                self.results_tree.item(item, open=False)
                
            self.set_status(get_string('status_all_groups_collapsed'))
        except Exception as e:
            logging.error(f"Error collapsing groups: {e}")
            self.show_error(get_string('error_collapsing_groups').format(error=str(e)))

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
            messagebox.showwarning(get_string('no_selection_title'), get_string('no_email_selection_message'))
            return
        
        # Get the first selected item
        item_id = selected_items[0]
        
        # Only proceed if it's an email item (not a group)
        if self.results_tree.parent(item_id) == "":
            messagebox.showwarning(get_string('invalid_selection_title'), get_string('invalid_selection_email_message'))
            return
        
        # Get the parent item (group) and the index in the group
        parent_id = self.results_tree.parent(item_id)
        
        # Get group index (from iid: "group_X")
        group_idx = int(parent_id.split('_')[1])
        
        # Get email index from the item text
        email_idx_text = self.results_tree.item(item_id)['text']  # "Y"
        email_idx = int(email_idx_text) - 1  # Convert to 0-based index
        
        try:
            # Get email content
            email_content = self.duplicate_finder.get_email_content(group_idx, email_idx)
            
            # Create email viewer window
            viewer = tk.Toplevel(self.root)
            viewer.title(get_string('email_viewer_title').format(subject=self.duplicate_groups[group_idx]['messages'][email_idx]['subject']))
            viewer.geometry("700x500")
            viewer.minsize(500, 400)
            
            # Make it modal
            viewer.transient(self.root)
            viewer.grab_set()
            
            # Configure grid
            viewer.columnconfigure(0, weight=1)
            viewer.rowconfigure(1, weight=1)
            
            # Header frame
            header_frame = ttk.LabelFrame(viewer, text=get_string('email_headers_frame'), padding="5")
            header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
            
            # Add header information
            email_info = self.duplicate_groups[group_idx]['messages'][email_idx]
            headers = [
                (get_string('header_from'), email_info['from']),
                (get_string('header_to'), email_info.get('to', get_string('header_to_na'))),
                (get_string('header_date'), email_info['date']),
                (get_string('header_subject'), email_info['subject']),
                (get_string('header_folder'), email_info['folder'])
            ]
            
            for i, (label, value) in enumerate(headers):
                ttk.Label(header_frame, text=label, font=('Arial', 10, 'bold')).grid(
                    row=i, column=0, sticky=tk.W, padx=(0, 10))
                ttk.Label(header_frame, text=value, wraplength=500).grid(
                    row=i, column=1, sticky=tk.W)
            
            # Content frame
            content_frame = ttk.LabelFrame(viewer, text=get_string('email_content_frame'), padding="5")
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
            ttk.Button(button_frame, text=get_string('close_button'), command=viewer.destroy).pack(side=tk.RIGHT)
            
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
            self.show_error(get_string('error_viewing_email').format(error=str(e)))

    def open_log_viewer(self):
        if not hasattr(self, 'log_viewer') or not self.log_viewer.winfo_exists():
            self.log_viewer = LogViewer(self.root, self.log_queue)
        else:
            self.log_viewer.lift()

    def on_folder_shift_up(self, event):
        listbox = self.folder_listbox
        
        if not listbox.curselection():
            listbox.selection_set(tk.ACTIVE)
            listbox.selection_anchor(tk.ACTIVE)

        active_idx = listbox.index(tk.ACTIVE)
        anchor_idx = listbox.index(tk.ANCHOR)

        if active_idx > 0:
            listbox.activate(active_idx - 1)
            new_active_idx = listbox.index(tk.ACTIVE)
            
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(anchor_idx, new_active_idx)
            listbox.see(new_active_idx)
            
        return "break"

    def on_folder_shift_down(self, event):
        listbox = self.folder_listbox

        if not listbox.curselection():
            listbox.selection_set(tk.ACTIVE)
            listbox.selection_anchor(tk.ACTIVE)

        active_idx = listbox.index(tk.ACTIVE)
        anchor_idx = listbox.index(tk.ANCHOR)

        if active_idx < listbox.size() - 1:
            listbox.activate(active_idx + 1)
            new_active_idx = listbox.index(tk.ACTIVE)
            
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(anchor_idx, new_active_idx)
            listbox.see(new_active_idx)
            
        return "break"

    def on_folder_ctrl_arrow(self, direction):
        listbox = self.folder_listbox
        active_idx = listbox.index(tk.ACTIVE)
        
        if direction == "up" and active_idx > 0:
            listbox.activate(active_idx - 1)
            listbox.see(active_idx - 1)
        elif direction == "down" and active_idx < listbox.size() - 1:
            listbox.activate(active_idx + 1)
            listbox.see(active_idx + 1)
            
        return "break"

    def on_mailbox_listbox_select(self, event):
        selections = self.mailbox_list.curselection()
        if selections:
            self.last_anchor = selections[0]

    def on_mailbox_shift_up(self, event, control_pressed=False):
        selections = list(self.mailbox_list.curselection())
        current_focus = self.mailbox_list.index(tk.ACTIVE)

        if not selections:
            self.mailbox_list.selection_set(current_focus)
            return "break"

        if not hasattr(self, 'last_anchor') or self.last_anchor is None:
            self.last_anchor = selections[0]

        if not control_pressed:
            self.mailbox_list.selection_clear(0, tk.END)

        if current_focus > 0:
            self.mailbox_list.activate(current_focus - 1)
            new_focus = self.mailbox_list.index(tk.ACTIVE)
            self.mailbox_list.selection_set(self.last_anchor, new_focus)
            self.mailbox_list.see(new_focus)

        return "break"

    def on_mailbox_shift_down(self, event, control_pressed=False):
        selections = list(self.mailbox_list.curselection())
        current_focus = self.mailbox_list.index(tk.ACTIVE)

        if not selections:
            self.mailbox_list.selection_set(current_focus)
            return "break"

        if not hasattr(self, 'last_anchor') or self.last_anchor is None:
            self.last_anchor = selections[0]

        if not control_pressed:
            self.mailbox_list.selection_clear(0, tk.END)

        if current_focus < self.mailbox_list.size() - 1:
            self.mailbox_list.activate(current_focus + 1)
            new_focus = self.mailbox_list.index(tk.ACTIVE)
            self.mailbox_list.selection_set(self.last_anchor, new_focus)
            self.mailbox_list.see(new_focus)

        return "break"

    def on_mailbox_ctrl_arrow(self, direction):
        current_focus = self.mailbox_list.index(tk.ACTIVE)
        if direction == "up" and current_focus > 0:
            self.mailbox_list.activate(current_focus - 1)
            self.mailbox_list.see(current_focus - 1)
        elif direction == "down" and current_focus < self.mailbox_list.size() - 1:
            self.mailbox_list.activate(current_focus + 1)
            self.mailbox_list.see(current_focus + 1)
        return "break"


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = EmailCleanerGUI(root)

    # Set up clean exit
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    root.mainloop()


if __name__ == "__main__":
    main()
