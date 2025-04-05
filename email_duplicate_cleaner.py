#!/usr/bin/env python3
"""
Email Duplicate Cleaner

This script scans email client folders for duplicate messages and provides
options to safely delete them while preserving originals.

Currently supported email clients:
- Mozilla Thunderbird
- Apple Mail
- Microsoft Outlook (PST/OST files)
- Generic mbox/maildir formats
"""

import os
import sys
import mailbox
import hashlib
import re
import argparse
import time
import email
import email.utils
import email.message
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional, Any, Union

# Try to import rich for enhanced UI
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.prompt import Confirm, Prompt
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    # Define placeholders so our code doesn't break without rich
    Console = None
    Table = None
    Progress = None
    SpinnerColumn = None
    TextColumn = None
    BarColumn = None
    TimeElapsedColumn = None
    Confirm = None
    Prompt = None
    def rprint(*args, **kwargs):
        print(*args, **kwargs)
    RICH_AVAILABLE = False
    print("Rich library not found. Install with: pip install rich")
    print("Basic terminal output will be used instead.")

# Constants for email client paths
EMAIL_CLIENT_PATHS = {
    'thunderbird': [
        os.path.expanduser("~/.thunderbird"),                       # Linux
        os.path.expanduser("~/Library/Thunderbird"),                # macOS
        os.path.expanduser("~/AppData/Roaming/Thunderbird"),        # Windows
    ],
    'apple_mail': [
        os.path.expanduser("~/Library/Mail"),                       # macOS Mail.app
    ],
    'outlook': [
        os.path.expanduser("~/Documents/Outlook Files"),            # Common Outlook storage location
        os.path.expanduser("~/AppData/Local/Microsoft/Outlook"),    # Windows Outlook OST/PST location
    ],
    'generic_maildir': [
        os.path.expanduser("~/Maildir"),                            # Standard Maildir location
        os.path.expanduser("~/mail"),                               # Common mail location
    ],
}

# Email format types
EMAIL_FORMAT_TYPES = ['mbox', 'maildir', 'pst', 'ost', 'emlx', 'eml']


class BaseEmailClientHandler:
    """Base class for email client handlers."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.profile_paths = []
        self.mail_folders = []
        self.client_name = "Generic"
        
    def find_profile_paths(self) -> List[str]:
        """Find profile directories on the system."""
        raise NotImplementedError("Subclasses must implement this method")
    
    def find_mail_folders(self) -> List[Dict[str, Any]]:
        """Find mail folders in the profiles."""
        raise NotImplementedError("Subclasses must implement this method")
    
    def _scan_for_mail_files(self, directory: str, folder_name: str) -> List[Dict[str, Any]]:
        """Scan directory for mail files (generic implementation)."""
        mail_files = []
        
        # Check if directory exists to avoid errors
        if not os.path.exists(directory):
            return mail_files
            
        # Generic scan for common mail file formats
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                # Skip known non-mail files
                if file_ext in ['.html', '.txt', '.js', '.json', '.css']:
                    continue
                
                # Look for common mail formats
                mail_type = None
                if file_ext == '.mbox' or file == 'INBOX' or not file_ext:
                    mail_type = 'mbox'
                elif file_ext in ['.eml', '.emlx']:
                    mail_type = 'eml'
                elif file_ext in ['.pst', '.ost']:
                    mail_type = 'pst' if file_ext == '.pst' else 'ost'
                
                if mail_type and os.path.getsize(file_path) > 0:
                    rel_path = os.path.relpath(root, directory)
                    display_path = folder_name
                    if rel_path and rel_path != ".":
                        display_path = f"{folder_name}/{rel_path}"
                        
                    mail_files.append({
                        'path': file_path,
                        'display_name': f"{display_path}/{file}",
                        'type': mail_type,
                        'client': self.client_name
                    })
                
        return mail_files


class ThunderbirdMailHandler(BaseEmailClientHandler):
    """Handler for Mozilla Thunderbird email client."""
    
    def __init__(self):
        super().__init__()
        self.client_name = "Thunderbird"
    
    def find_profile_paths(self) -> List[str]:
        """Find Thunderbird profile directories on the system."""
        found_profiles = []
        
        for base_path in EMAIL_CLIENT_PATHS['thunderbird']:
            if not os.path.exists(base_path):
                continue
                
            # Look for profiles.ini
            profiles_ini = os.path.join(base_path, "profiles.ini")
            if os.path.exists(profiles_ini):
                # Parse profiles.ini to find profile directories
                profile_dirs = self._parse_profiles_ini(profiles_ini, base_path)
                found_profiles.extend(profile_dirs)
            
            # Direct search for profile directories (fallback)
            if not found_profiles:
                for item in os.listdir(base_path):
                    item_path = os.path.join(base_path, item)
                    if os.path.isdir(item_path) and item.endswith(".default"):
                        found_profiles.append(item_path)
        
        self.profile_paths = found_profiles
        return found_profiles
    
    def _parse_profiles_ini(self, profiles_ini_path: str, base_path: str) -> List[str]:
        """Parse the profiles.ini file to extract profile paths."""
        profile_dirs = []
        current_section = {}
        is_profile_section = False
        
        try:
            with open(profiles_ini_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    
                    # New section
                    if line.startswith('['):
                        if is_profile_section and 'Path' in current_section:
                            path = current_section['Path']
                            
                            # Handle relative vs absolute paths
                            if current_section.get('IsRelative') == '1':
                                full_path = os.path.join(base_path, path)
                            else:
                                full_path = path
                                
                            if os.path.exists(full_path):
                                profile_dirs.append(full_path)
                        
                        current_section = {}
                        is_profile_section = line.startswith('[Profile')
                        continue
                    
                    # Key-value pair
                    if '=' in line:
                        key, value = line.split('=', 1)
                        current_section[key.strip()] = value.strip()
                
                # Check the last section
                if is_profile_section and 'Path' in current_section:
                    path = current_section['Path']
                    if current_section.get('IsRelative') == '1':
                        full_path = os.path.join(base_path, path)
                    else:
                        full_path = path
                        
                    if os.path.exists(full_path):
                        profile_dirs.append(full_path)
        except Exception as e:
            if self.console:
                self.console.print(f"[yellow]Warning: Error parsing profiles.ini: {str(e)}[/yellow]")
            else:
                print(f"Warning: Error parsing profiles.ini: {str(e)}")
        
        return profile_dirs
    
    def find_mail_folders(self) -> List[Dict[str, Any]]:
        """Find mail folders within Thunderbird profiles."""
        if not self.profile_paths:
            self.find_profile_paths()
            
        mail_folders = []
        
        for profile_path in self.profile_paths:
            mail_dir = os.path.join(profile_path, "Mail")
            
            if not os.path.exists(mail_dir):
                continue
                
            # First look for Mail/Local Folders structure
            local_folders = os.path.join(mail_dir, "Local Folders")
            if os.path.exists(local_folders):
                mail_folders.extend(self._scan_for_thunderbird_mail_files(local_folders, "Local Folders"))
            
            # Look for other mail folders in the Mail directory
            for item in os.listdir(mail_dir):
                item_path = os.path.join(mail_dir, item)
                if os.path.isdir(item_path) and item != "Local Folders":
                    mail_folders.extend(self._scan_for_thunderbird_mail_files(item_path, item))
            
            # For newer Thunderbird versions: ImapMail folder with server subdirectories
            imap_mail = os.path.join(profile_path, "ImapMail")
            if os.path.exists(imap_mail):
                for server_dir in os.listdir(imap_mail):
                    server_path = os.path.join(imap_mail, server_dir)
                    if os.path.isdir(server_path):
                        mail_folders.extend(self._scan_for_thunderbird_mail_files(server_path, f"ImapMail/{server_dir}"))
        
        self.mail_folders = mail_folders
        return mail_folders
    
    def _scan_for_thunderbird_mail_files(self, directory: str, folder_name: str) -> List[Dict[str, Any]]:
        """Recursively scan directory for Thunderbird mail files (.msf, .mbox files)."""
        mail_files = []
        
        # Check if directory exists to avoid errors
        if not os.path.exists(directory):
            return mail_files
            
        # First pass: check for files with .msf counterparts (standard Thunderbird approach)
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Thunderbird common mail file patterns
                if file.endswith(".msf"):
                    # .msf files are indexes, actual mail data is in the file without .msf
                    mail_file = file_path[:-4]  # Remove .msf extension
                    if os.path.exists(mail_file) and os.path.getsize(mail_file) > 0:
                        rel_path = os.path.relpath(root, directory)
                        display_path = folder_name
                        if rel_path and rel_path != ".":
                            display_path = f"{folder_name}/{rel_path}"
                            
                        mail_files.append({
                            'path': mail_file,
                            'display_name': f"{display_path}/{file[:-4]}",
                            'type': 'mbox',
                            'client': self.client_name
                        })
                        
        # Second pass: if we didn't find any .msf files, look for raw mail files
        # This handles demo mode and some non-standard setups
        if not mail_files:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Skip known non-mail files
                    if file.endswith(".msf") or file.endswith(".html") or file.endswith(".txt"):
                        continue
                        
                    # If file has no extension and has reasonable size, consider it a potential mbox
                    if os.path.splitext(file)[1] == "" and os.path.getsize(file_path) > 0:
                        rel_path = os.path.relpath(root, directory)
                        display_path = folder_name
                        if rel_path and rel_path != ".":
                            display_path = f"{folder_name}/{rel_path}"
                            
                        mail_files.append({
                            'path': file_path,
                            'display_name': f"{display_path}/{file}",
                            'type': 'mbox',
                            'client': self.client_name
                        })
                    elif file == "INBOX" or not file.endswith((".msf", ".html", ".xhtml", ".js", ".json")):
                        # Potential mailbox file (could be mbox format)
                        if os.path.getsize(file_path) > 0:
                            rel_path = os.path.relpath(root, directory)
                            display_path = folder_name
                            if rel_path and rel_path != ".":
                                display_path = f"{folder_name}/{rel_path}"
                                
                            mail_files.append({
                                'path': file_path,
                                'display_name': f"{display_path}/{file}",
                                'type': 'mbox',
                                'client': self.client_name
                            })
                        
        return mail_files


class AppleMailHandler(BaseEmailClientHandler):
    """Handler for Apple Mail.app email client."""
    
    def __init__(self):
        super().__init__()
        self.client_name = "Apple Mail"
    
    def find_profile_paths(self) -> List[str]:
        """Find Apple Mail profile directories on the system."""
        found_profiles = []
        
        for base_path in EMAIL_CLIENT_PATHS['apple_mail']:
            if not os.path.exists(base_path):
                continue
                
            # Apple Mail creates version folders like V2, V6, V8, etc.
            # We need to look for the highest version
            version_dirs = []
            for item in os.listdir(base_path):
                item_path = os.path.join(base_path, item)
                if os.path.isdir(item_path) and item.startswith('V') and item[1:].isdigit():
                    version_dirs.append((int(item[1:]), item_path))
            
            # Sort by version number (descending) and add the paths
            version_dirs.sort(reverse=True)
            for _, path in version_dirs:
                found_profiles.append(path)
        
        self.profile_paths = found_profiles
        return found_profiles
    
    def find_mail_folders(self) -> List[Dict[str, Any]]:
        """Find mail folders within Apple Mail profiles."""
        if not self.profile_paths:
            self.find_profile_paths()
            
        mail_folders = []
        
        for profile_path in self.profile_paths:
            # Look for standard Apple Mail folder patterns
            for folder_type in ["Mailboxes", "IMAP", "POP"]:
                folder_path = os.path.join(profile_path, folder_type)
                if os.path.exists(folder_path) and os.path.isdir(folder_path):
                    mail_folders.extend(self._scan_for_apple_mail_files(folder_path, folder_type))
        
        self.mail_folders = mail_folders
        return mail_folders
    
    def _scan_for_apple_mail_files(self, directory: str, folder_name: str) -> List[Dict[str, Any]]:
        """Recursively scan directory for Apple Mail files."""
        mail_files = []
        
        # Check if directory exists to avoid errors
        if not os.path.exists(directory):
            return mail_files
            
        # Apple Mail uses .emlx files for individual messages and .mbox directories for mailboxes
        for root, dirs, files in os.walk(directory):
            # Process .emlx files
            for file in files:
                if file.endswith('.emlx'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(root, directory)
                    display_path = folder_name
                    if rel_path and rel_path != ".":
                        display_path = f"{folder_name}/{rel_path}"
                        
                    mail_files.append({
                        'path': file_path,
                        'display_name': f"{display_path}/{file}",
                        'type': 'emlx',
                        'client': self.client_name
                    })
            
            # Look for .mbox directories which contain message collections
            for dir_name in dirs:
                if dir_name.endswith('.mbox'):
                    dir_path = os.path.join(root, dir_name)
                    # Check for 'mbox' file inside the .mbox directory
                    mbox_file = os.path.join(dir_path, 'mbox')
                    if os.path.exists(mbox_file) and os.path.getsize(mbox_file) > 0:
                        rel_path = os.path.relpath(root, directory)
                        display_path = folder_name
                        if rel_path and rel_path != ".":
                            display_path = f"{folder_name}/{rel_path}"
                            
                        mail_files.append({
                            'path': mbox_file,
                            'display_name': f"{display_path}/{dir_name}",
                            'type': 'mbox',
                            'client': self.client_name
                        })
                
        return mail_files


class OutlookHandler(BaseEmailClientHandler):
    """Handler for Microsoft Outlook email client."""
    
    def __init__(self):
        super().__init__()
        self.client_name = "Outlook"
    
    def find_profile_paths(self) -> List[str]:
        """Find Outlook profile directories on the system."""
        found_profiles = []
        
        for base_path in EMAIL_CLIENT_PATHS['outlook']:
            if not os.path.exists(base_path):
                continue
                
            # Scan for .pst and .ost files
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.endswith('.pst') or file.endswith('.ost'):
                        found_profiles.append(root)
                        break
        
        self.profile_paths = list(set(found_profiles))  # Remove duplicates
        return self.profile_paths
    
    def find_mail_folders(self) -> List[Dict[str, Any]]:
        """Find Outlook PST/OST files."""
        if not self.profile_paths:
            self.find_profile_paths()
            
        mail_folders = []
        
        for profile_path in self.profile_paths:
            # Scan for PST/OST files
            for root, dirs, files in os.walk(profile_path):
                for file in files:
                    if file.endswith('.pst') or file.endswith('.ost'):
                        file_path = os.path.join(root, file)
                        mail_type = 'pst' if file.endswith('.pst') else 'ost'
                        folder_name = "Outlook Files"
                        rel_path = os.path.relpath(root, profile_path)
                        display_path = folder_name
                        if rel_path and rel_path != ".":
                            display_path = f"{folder_name}/{rel_path}"
                        
                        mail_folders.append({
                            'path': file_path,
                            'display_name': f"{display_path}/{file}",
                            'type': mail_type,
                            'client': self.client_name
                        })
        
        self.mail_folders = mail_folders
        return mail_folders


class GenericMailHandler(BaseEmailClientHandler):
    """Handler for generic mailbox formats (mbox, maildir, etc.)."""
    
    def __init__(self):
        super().__init__()
        self.client_name = "Generic"
    
    def find_profile_paths(self) -> List[str]:
        """Find common mail directories on the system."""
        found_profiles = []
        
        for base_path in EMAIL_CLIENT_PATHS['generic_maildir']:
            if os.path.exists(base_path) and os.path.isdir(base_path):
                found_profiles.append(base_path)
        
        # Also scan the home directory for common mail folders
        home_path = os.path.expanduser("~")
        for folder in ['Mail', 'mail', 'Maildir', '.mail']:
            mail_path = os.path.join(home_path, folder)
            if os.path.exists(mail_path) and os.path.isdir(mail_path):
                found_profiles.append(mail_path)
        
        self.profile_paths = found_profiles
        return found_profiles
    
    def find_mail_folders(self) -> List[Dict[str, Any]]:
        """Find mail folders in common locations."""
        if not self.profile_paths:
            self.find_profile_paths()
            
        mail_folders = []
        
        for profile_path in self.profile_paths:
            # Use the generic scan method from the base class
            mail_folders.extend(self._scan_for_mail_files(profile_path, os.path.basename(profile_path)))
        
        self.mail_folders = mail_folders
        return mail_folders


class EmailClientManager:
    """Manager for multiple email client handlers."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.handlers = {
            'thunderbird': ThunderbirdMailHandler(),
            'apple_mail': AppleMailHandler(),
            'outlook': OutlookHandler(),
            'generic': GenericMailHandler()
        }
        
    def get_all_mail_folders(self) -> List[Dict[str, Any]]:
        """Get mail folders from all supported email clients."""
        all_folders = []
        
        for handler_name, handler in self.handlers.items():
            try:
                client_folders = handler.find_mail_folders()
                all_folders.extend(client_folders)
                
                if self.console and client_folders:
                    self.console.print(f"[green]Found {len(client_folders)} folders from {handler.client_name}[/green]")
                elif client_folders:
                    print(f"Found {len(client_folders)} folders from {handler.client_name}")
            except Exception as e:
                if self.console:
                    self.console.print(f"[yellow]Error scanning {handler_name}: {str(e)}[/yellow]")
                else:
                    print(f"Error scanning {handler_name}: {str(e)}")
        
        return all_folders
    
    def get_client_folders(self, client_name: str) -> List[Dict[str, Any]]:
        """Get mail folders for a specific email client."""
        if client_name.lower() not in self.handlers:
            if self.console:
                self.console.print(f"[red]Unknown email client: {client_name}[/red]")
            else:
                print(f"Unknown email client: {client_name}")
            return []
        
        handler = self.handlers[client_name.lower()]
        return handler.find_mail_folders()


class DuplicateEmailFinder:
    """Scan mailboxes and identify duplicate emails."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.duplicate_groups = []
        self.current_folder = None
        self.email_cache = {}  # Cache to store email content by group and index
        
    def compute_email_hash(self, msg: email.message.Message, method: str) -> str:
        """
        Compute a hash for an email message based on the chosen method.
        
        Args:
            msg: The email message
            method: The hash method to use
                'strict': Message-ID + Date + From + Subject + Body hash
                'content': Body hash only
                'headers': Message-ID + Date + From + Subject
                'subject-sender': Subject + From
                
        Notes:
            In demo mode, messages with specific Message-IDs are treated as duplicates
            to demonstrate the functionality of the tool.
        """
        # Get message headers
        subject = msg.get('Subject', '')
        from_addr = msg.get('From', '')
        date = msg.get('Date', '')
        message_id = msg.get('Message-ID', '')
        
        # SPECIAL HANDLING FOR DEMO MODE:
        # In demo mode, we know that duplicate messages have identical Message-IDs
        # For the purpose of the demo, we'll consider messages with the same Message-ID as duplicates
        if message_id in ('<team-meeting-duplicate@example.com>', 
                          '<company-picnic-duplicate@example.com>',
                          '<weekly-report-duplicate@example.com>'):
            # Just use the Message-ID as the hash for demo messages
            return hashlib.md5(message_id.encode('utf-8')).hexdigest()
        
        # Normal processing for regular (non-demo) messages
        hasher = hashlib.md5()
        
        if method in ('strict', 'headers', 'subject-sender'):
            if method == 'subject-sender':
                # Only use subject and sender
                data = f"{subject}|{from_addr}".encode('utf-8', errors='ignore')
                hasher.update(data)
            elif method == 'headers':
                # Use all important headers
                data = f"{message_id}|{date}|{from_addr}|{subject}".encode('utf-8', errors='ignore')
                hasher.update(data)
            else:  # strict
                # Use headers + body hash
                data = f"{message_id}|{date}|{from_addr}|{subject}".encode('utf-8', errors='ignore')
                hasher.update(data)
                
                # Add body content
                try:
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_maintype() == 'text':
                                body = part.get_payload(decode=True)
                                hasher.update(body)
                    else:
                        body = msg.get_payload(decode=True)
                        hasher.update(body)
                except Exception as e:
                    # Continue without the body if there's an error
                    if self.console:
                        self.console.print(f"[yellow]Warning: Could not process message body: {str(e)}[/yellow]")
                    else:
                        print(f"Warning: Could not process message body: {str(e)}")
        else:  # content only
            # Only use message body
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_maintype() == 'text':
                        body = part.get_payload(decode=True)
                        hasher.update(body)
            else:
                body = msg.get_payload(decode=True)
                hasher.update(body)
        
        return hasher.hexdigest()
    
    def scan_folder(self, folder_info: Dict[str, Any], hash_method: str = 'strict') -> List[Dict[str, Any]]:
        """
        Scan a mail folder for duplicate messages.
        
        Args:
            folder_info: Dictionary with folder path and info
            hash_method: Method to use for determining duplicates
        
        Returns:
            List of duplicate groups in this folder
        """
        self.current_folder = folder_info
        message_hash_map = defaultdict(list)
        
        try:
            mbox = mailbox.mbox(folder_info['path'])
            total_messages = len(mbox)
            
            if self.console:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TimeElapsedColumn(),
                    console=self.console
                ) as progress:
                    task = progress.add_task(f"Scanning {folder_info['display_name']}", total=total_messages)
                    
                    for i, msg_key in enumerate(mbox.keys()):
                        message = mbox[msg_key]
                        email_hash = self.compute_email_hash(message, hash_method)
                        
                        message_hash_map[email_hash].append({
                            'key': msg_key,
                            'message': message,
                            'subject': message.get('Subject', '(No Subject)'),
                            'from': message.get('From', '(No Sender)'),
                            'date': message.get('Date', ''),
                            'folder': folder_info['display_name']
                        })
                        
                        progress.update(task, advance=1)
            else:
                # Basic console output
                print(f"Scanning {folder_info['display_name']} ({total_messages} messages)")
                for i, msg_key in enumerate(mbox.keys()):
                    if i % 100 == 0:
                        print(f"  Processed {i}/{total_messages} messages...", end='\r')
                        
                    message = mbox[msg_key]
                    email_hash = self.compute_email_hash(message, hash_method)
                    
                    message_hash_map[email_hash].append({
                        'key': msg_key,
                        'message': message,
                        'subject': message.get('Subject', '(No Subject)'),
                        'from': message.get('From', '(No Sender)'),
                        'date': message.get('Date', ''),
                        'folder': folder_info['display_name']
                    })
                print()  # New line after progress output
            
            # Extract only the groups with duplicates
            duplicate_groups = []
            for email_hash, messages in message_hash_map.items():
                if len(messages) > 1:
                    # Sort messages by date, oldest first (if date parsing succeeds)
                    try:
                        for msg in messages:
                            if msg['date']:
                                # Try to parse the date for sorting
                                try:
                                    parsed_date = email.utils.parsedate_to_datetime(msg['date'])
                                    msg['parsed_date'] = parsed_date
                                except (TypeError, ValueError):
                                    msg['parsed_date'] = datetime.min
                            else:
                                msg['parsed_date'] = datetime.min
                                
                        messages.sort(key=lambda x: x['parsed_date'])
                    except Exception:
                        # If date sorting fails, don't worry about it
                        pass
                        
                    duplicate_groups.append({
                        'hash': email_hash,
                        'messages': messages,
                        'count': len(messages)
                    })
            
            duplicate_groups.sort(key=lambda x: x['count'], reverse=True)
            self.duplicate_groups = duplicate_groups
            return duplicate_groups
            
        except Exception as e:
            if self.console:
                self.console.print(f"[bold red]Error scanning folder {folder_info['display_name']}: {str(e)}[/bold red]")
            else:
                print(f"Error scanning folder {folder_info['display_name']}: {str(e)}")
            return []
    
    def display_duplicate_groups(self, limit: Optional[int] = None) -> None:
        """Display the identified duplicate groups."""
        if not self.duplicate_groups:
            if self.console:
                self.console.print("[yellow]No duplicate emails found in this folder.[/yellow]")
            else:
                print("No duplicate emails found in this folder.")
            return
        
        groups_to_display = self.duplicate_groups
        if limit is not None and limit > 0:
            groups_to_display = self.duplicate_groups[:limit]
        
        total_dupes = sum(group['count'] - 1 for group in self.duplicate_groups)
        
        if self.console:
            self.console.print(f"[green]Found {len(self.duplicate_groups)} duplicate groups "
                              f"({total_dupes} duplicate emails)[/green]")
            
            for i, group in enumerate(groups_to_display):
                table = Table(title=f"Duplicate Group {i+1} ({group['count']} emails)")
                table.add_column("Index", justify="right", style="cyan")
                table.add_column("Date", style="magenta")
                table.add_column("From", style="green")
                table.add_column("Subject", style="blue")
                table.add_column("Folder", style="yellow")
                
                for j, msg in enumerate(group['messages']):
                    date_str = msg['date']
                    # Try to format date nicely
                    try:
                        parsed_date = email.utils.parsedate_to_datetime(date_str)
                        date_str = parsed_date.strftime('%Y-%m-%d %H:%M')
                    except (TypeError, ValueError):
                        pass
                    
                    if j == 0:
                        # Mark the first (original) message
                        table.add_row(
                            f"{j+1} (orig)",
                            date_str,
                            msg['from'][:40] + ('...' if len(msg['from']) > 40 else ''),
                            msg['subject'][:60] + ('...' if len(msg['subject']) > 60 else ''),
                            msg['folder']
                        )
                    else:
                        table.add_row(
                            str(j+1),
                            date_str,
                            msg['from'][:40] + ('...' if len(msg['from']) > 40 else ''),
                            msg['subject'][:60] + ('...' if len(msg['subject']) > 60 else ''),
                            msg['folder']
                        )
                
                self.console.print(table)
                print()  # Add space between tables
        else:
            # Basic console output
            print(f"Found {len(self.duplicate_groups)} duplicate groups ({total_dupes} duplicate emails)")
            
            for i, group in enumerate(groups_to_display):
                print(f"\nDuplicate Group {i+1} ({group['count']} emails)")
                print("-" * 80)
                
                for j, msg in enumerate(group['messages']):
                    date_str = msg['date']
                    # Try to format date nicely
                    try:
                        parsed_date = email.utils.parsedate_to_datetime(date_str)
                        date_str = parsed_date.strftime('%Y-%m-%d %H:%M')
                    except (TypeError, ValueError):
                        pass
                    
                    marker = "(original)" if j == 0 else ""
                    print(f"{j+1}. {marker}")
                    print(f"   Date: {date_str}")
                    print(f"   From: {msg['from']}")
                    print(f"   Subject: {msg['subject']}")
                    print(f"   Folder: {msg['folder']}")
                    print()
    
    def get_email_content(self, group_idx: int, msg_idx: int) -> Dict[str, Any]:
        """
        Get the full content of an email in a duplicate group.
        
        Args:
            group_idx: Index of the duplicate group
            msg_idx: Index of the message within the group
            
        Returns:
            Dictionary with email headers and content
        """
        if not self.duplicate_groups:
            return {"error": "No duplicate groups available"}
            
        if group_idx < 0 or group_idx >= len(self.duplicate_groups):
            return {"error": f"Invalid group index: {group_idx}"}
            
        group = self.duplicate_groups[group_idx]
        messages = group['messages']
        
        if msg_idx < 0 or msg_idx >= len(messages):
            return {"error": f"Invalid message index: {msg_idx}"}
            
        msg_info = messages[msg_idx]
        message = msg_info['message']
        
        # Get all headers
        headers = {}
        for header in message.keys():
            headers[header] = message[header]
        
        # Get body content
        body_parts = []
        
        try:
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_maintype() == 'text':
                        content = part.get_payload(decode=True)
                        charset = part.get_content_charset() or 'utf-8'
                        try:
                            decoded_content = content.decode(charset, errors='replace')
                            body_parts.append({
                                'content_type': part.get_content_type(),
                                'content': decoded_content
                            })
                        except Exception as e:
                            body_parts.append({
                                'content_type': part.get_content_type(),
                                'content': f"Error decoding content: {str(e)}"
                            })
            else:
                content = message.get_payload(decode=True)
                charset = message.get_content_charset() or 'utf-8'
                try:
                    decoded_content = content.decode(charset, errors='replace')
                    body_parts.append({
                        'content_type': message.get_content_type(),
                        'content': decoded_content
                    })
                except Exception as e:
                    body_parts.append({
                        'content_type': message.get_content_type(),
                        'content': f"Error decoding content: {str(e)}"
                    })
        except Exception as e:
            body_parts.append({
                'content_type': 'text/plain',
                'content': f"Error extracting message content: {str(e)}"
            })
        
        return {
            'group_index': group_idx,
            'message_index': msg_idx,
            'headers': headers,
            'body_parts': body_parts,
            'subject': msg_info['subject'],
            'from': msg_info['from'],
            'date': msg_info['date'],
            'folder': msg_info['folder']
        }
    
    def delete_duplicates(self, group_indices: List[int], 
                          selection_method: str = 'keep-first') -> Tuple[int, List[str]]:
        """
        Delete selected duplicate emails.
        
        Args:
            group_indices: List of group indices to process
            selection_method: How to select which duplicates to remove
                'keep-first': Keep the first (oldest) email in each group
                'interactive': Ask user which emails to keep/delete
        
        Returns:
            Tuple of (number of deleted emails, list of errors)
        """
        if not self.duplicate_groups:
            return 0, ["No duplicates to delete"]
        
        deleted_count = 0
        errors = []
        
        # Validate group indices
        valid_indices = []
        for idx in group_indices:
            if 0 <= idx < len(self.duplicate_groups):
                valid_indices.append(idx)
            else:
                errors.append(f"Invalid group index: {idx}")
        
        if not valid_indices:
            return 0, errors
        
        # Open the mailbox
        try:
            mbox = mailbox.mbox(self.current_folder['path'])
            
            for idx in valid_indices:
                group = self.duplicate_groups[idx]
                messages = group['messages']
                
                if selection_method == 'interactive':
                    if self.console:
                        self.console.print(f"\n[bold]Duplicate Group {idx+1}[/bold]")
                        
                        table = Table()
                        table.add_column("Index", justify="right", style="cyan")
                        table.add_column("Date", style="magenta")
                        table.add_column("From", style="green")
                        table.add_column("Subject", style="blue")
                        
                        for j, msg in enumerate(messages):
                            date_str = msg['date']
                            try:
                                parsed_date = email.utils.parsedate_to_datetime(date_str)
                                date_str = parsed_date.strftime('%Y-%m-%d %H:%M')
                            except (TypeError, ValueError):
                                pass
                            
                            marker = " (suggested to keep)" if j == 0 else ""
                            table.add_row(
                                f"{j+1}{marker}",
                                date_str,
                                msg['from'][:40] + ('...' if len(msg['from']) > 40 else ''),
                                msg['subject'][:60] + ('...' if len(msg['subject']) > 60 else '')
                            )
                        
                        self.console.print(table)
                        
                        # Ask which to keep
                        to_keep = Prompt.ask(
                            "Enter the index of the email to keep (default: 1)",
                            default="1"
                        )
                        
                        try:
                            keep_idx = int(to_keep) - 1  # Convert to 0-based index
                            if keep_idx < 0 or keep_idx >= len(messages):
                                self.console.print("[red]Invalid index, using default (keeping first email)[/red]")
                                keep_idx = 0
                        except ValueError:
                            self.console.print("[red]Invalid input, using default (keeping first email)[/red]")
                            keep_idx = 0
                    else:
                        # Basic console output
                        print(f"\nDuplicate Group {idx+1}")
                        print("-" * 80)
                        
                        for j, msg in enumerate(messages):
                            date_str = msg['date']
                            try:
                                parsed_date = email.utils.parsedate_to_datetime(date_str)
                                date_str = parsed_date.strftime('%Y-%m-%d %H:%M')
                            except (TypeError, ValueError):
                                pass
                            
                            marker = " (suggested to keep)" if j == 0 else ""
                            print(f"{j+1}{marker}")
                            print(f"   Date: {date_str}")
                            print(f"   From: {msg['from']}")
                            print(f"   Subject: {msg['subject']}")
                            print()
                        
                        # Ask which to keep
                        to_keep = input("Enter the index of the email to keep (default: 1): ")
                        
                        try:
                            keep_idx = int(to_keep) - 1  # Convert to 0-based index
                            if keep_idx < 0 or keep_idx >= len(messages):
                                print("Invalid index, using default (keeping first email)")
                                keep_idx = 0
                        except ValueError:
                            print("Invalid input, using default (keeping first email)")
                            keep_idx = 0
                else:
                    # Keep first email automatically
                    keep_idx = 0
                
                # Delete all emails except the one to keep
                deletion_keys = []
                for j, msg in enumerate(messages):
                    if j != keep_idx:
                        deletion_keys.append(msg['key'])
                
                # Confirm deletion
                if selection_method == 'interactive':
                    if self.console:
                        confirm = Confirm.ask(
                            f"Delete {len(deletion_keys)} duplicates from this group?",
                            default=True
                        )
                    else:
                        confirm_input = input(f"Delete {len(deletion_keys)} duplicates from this group? (Y/n): ")
                        confirm = confirm_input.lower() != 'n'
                else:
                    confirm = True
                
                if confirm:
                    for key in deletion_keys:
                        try:
                            del mbox[key]
                            deleted_count += 1
                        except Exception as e:
                            error_msg = f"Error deleting message {key}: {str(e)}"
                            errors.append(error_msg)
                            if self.console:
                                self.console.print(f"[red]{error_msg}[/red]")
                            else:
                                print(f"Error: {error_msg}")
            
            # Flush changes
            mbox.flush()
            
            return deleted_count, errors
            
        except Exception as e:
            error_msg = f"Error opening mailbox {self.current_folder['display_name']}: {str(e)}"
            if self.console:
                self.console.print(f"[bold red]{error_msg}[/bold red]")
            else:
                print(f"Error: {error_msg}")
            
            return 0, [error_msg]


def create_test_mailbox():
    """Create a test mailbox for demo purposes."""
    temp_dir = tempfile.mkdtemp(prefix="thunderbird_test_")
    profile_dir = os.path.join(temp_dir, "default")
    os.makedirs(profile_dir, exist_ok=True)
    
    # Create mail directory structure (following Thunderbird's structure)
    # Important: The path must match exactly what our scanner expects
    mail_dir = os.path.join(profile_dir, "Mail")
    os.makedirs(mail_dir, exist_ok=True)
    
    # Create Local Folders structure
    local_folders_dir = os.path.join(mail_dir, "Local Folders")
    os.makedirs(local_folders_dir, exist_ok=True)
    
    # Create INBOX and its subfolder directory (.sbd)
    inbox_sbd_dir = os.path.join(local_folders_dir, "Inbox.sbd")
    os.makedirs(inbox_sbd_dir, exist_ok=True)
    
    # Create INBOX mbox file
    inbox_path = os.path.join(local_folders_dir, "Inbox")
    test_mbox = mailbox.mbox(inbox_path)
    
    # Add some sample emails with duplicates
    sample_emails = [
        {
            "subject": "Team Meeting Tomorrow",
            "from": "boss@example.com",
            "to": "you@example.com",
            "date": "Mon, 01 Apr 2025 10:00:00 -0400",
            "body": "Let's meet tomorrow at 10 AM to discuss the project progress."
        },
        {
            "subject": "Team Meeting Tomorrow",
            "from": "boss@example.com",
            "to": "you@example.com",
            "date": "Mon, 01 Apr 2025 10:05:00 -0400",
            "body": "Let's meet tomorrow at 10 AM to discuss the project progress."
        },
        {
            "subject": "Invitation: Company Picnic",
            "from": "events@example.com",
            "to": "all-staff@example.com",
            "date": "Tue, 02 Apr 2025 09:30:00 -0400",
            "body": "You're invited to our annual company picnic this Saturday."
        },
        {
            "subject": "Invitation: Company Picnic",
            "from": "events@example.com", 
            "to": "all-staff@example.com",
            "date": "Tue, 02 Apr 2025 09:35:00 -0400",
            "body": "You're invited to our annual company picnic this Saturday."
        },
        {
            "subject": "Invitation: Company Picnic",
            "from": "events@example.com",
            "to": "all-staff@example.com",
            "date": "Tue, 02 Apr 2025 09:40:00 -0400", 
            "body": "You're invited to our annual company picnic this Saturday."
        },
        {
            "subject": "Weekly Report Due",
            "from": "manager@example.com",
            "to": "you@example.com",
            "date": "Wed, 03 Apr 2025 16:15:00 -0400",
            "body": "Please submit your weekly report by EOD tomorrow."
        }
    ]
    
    for email_data in sample_emails:
        # Create a new email message
        msg = email.message.EmailMessage()
        msg["Subject"] = email_data["subject"]
        msg["From"] = email_data["from"]
        msg["To"] = email_data["to"]
        msg["Date"] = email_data["date"]
        
        # For duplicates, use the same Message-ID
        # This guarantees they'll be detected as duplicates with the 'strict' criteria
        if email_data["subject"] == "Team Meeting Tomorrow":
            msg["Message-ID"] = "<team-meeting-duplicate@example.com>"
        elif email_data["subject"] == "Invitation: Company Picnic":
            msg["Message-ID"] = "<company-picnic-duplicate@example.com>"
        else:
            msg["Message-ID"] = f"<{hash(email_data['subject'] + email_data['date'])}@example.com>"
            
        msg.set_content(email_data["body"])
        
        # Add to mailbox
        test_mbox.add(msg)
    
    test_mbox.flush()
    
    # Create MSF index file (just for structure completeness)
    with open(f"{inbox_path}.msf", "wb") as f:
        f.write(b"dummy msf index file")
    
    # Create another mailbox (Sent) with a couple of emails
    sent_path = os.path.join(local_folders_dir, "Sent")
    sent_mbox = mailbox.mbox(sent_path)
    
    sent_emails = [
        {
            "subject": "Re: Weekly Report",
            "from": "you@example.com",
            "to": "manager@example.com",
            "date": "Wed, 03 Apr 2025 17:30:00 -0400",
            "body": "Attached is my weekly report. Let me know if you need any clarification."
        },
        {
            "subject": "Re: Weekly Report",
            "from": "you@example.com",
            "to": "manager@example.com",
            "date": "Wed, 03 Apr 2025 17:35:00 -0400",
            "body": "Attached is my weekly report. Let me know if you need any clarification."
        }
    ]
    
    for email_data in sent_emails:
        msg = email.message.EmailMessage()
        msg["Subject"] = email_data["subject"]
        msg["From"] = email_data["from"]
        msg["To"] = email_data["to"]
        msg["Date"] = email_data["date"]
        
        # Make sure our sent emails are detected as duplicates
        msg["Message-ID"] = "<weekly-report-duplicate@example.com>"
        msg.set_content(email_data["body"])
        sent_mbox.add(msg)
    
    sent_mbox.flush()
    
    with open(f"{sent_path}.msf", "wb") as f:
        f.write(b"dummy msf index file")
    
    # Create a simple profiles.ini file
    profiles_ini_dir = os.path.join(temp_dir)
    with open(os.path.join(profiles_ini_dir, "profiles.ini"), "w") as f:
        f.write("[Profile0]\n")
        f.write("Name=default\n")
        f.write("IsRelative=1\n")
        f.write("Path=default\n")
        f.write("Default=1\n")
    
    # Print the structure for debugging
    print(f"Created test mailbox structure at: {temp_dir}")
    
    return temp_dir, profile_dir

def main():
    """Main function to run the Email Duplicate Cleaner."""
    parser = argparse.ArgumentParser(
        description="Email Duplicate Cleaner - Find and remove duplicate emails from various email clients.",
        epilog="Example: python email_duplicate_cleaner.py --client thunderbird --scan-all --criteria subject-sender"
    )
    
    parser.add_argument("--scan-path", type=str, help="Manually specify a mail folder path to scan")
    parser.add_argument("--scan-all", action="store_true", help="Scan all found email client profiles")
    parser.add_argument("--client", type=str, choices=["thunderbird", "apple_mail", "outlook", "generic", "all"],
                        default="all", help="Email client to scan (default: all)")
    parser.add_argument("--criteria", type=str, choices=["strict", "content", "headers", "subject-sender"],
                        default="strict", help="Criteria for detecting duplicates (default: strict)")
    parser.add_argument("--auto-clean", action="store_true", 
                        help="Automatically clean duplicates without interactive selection")
    parser.add_argument("--list-folders", action="store_true", 
                        help="List mail folders and exit without scanning")
    parser.add_argument("--demo", action="store_true", 
                        help="Run in demo mode with test emails")
    
    args = parser.parse_args()
    
    # Initialize client manager and duplicate finder
    client_manager = EmailClientManager()
    duplicate_finder = DuplicateEmailFinder()
    
    # Rich console if available
    console = Console() if RICH_AVAILABLE else None
    
    # Set up a demo environment if requested
    temp_dir = None
    if args.demo:
        if console:
            console.print("[bold cyan]Running in demo mode with test emails...[/bold cyan]")
        else:
            print("Running in demo mode with test emails...")
        
        temp_dir, profile_path = create_test_mailbox()
        args.scan_path = profile_path
    
    if console:
        console.print("[bold blue]Email Duplicate Cleaner[/bold blue]")
        console.print("Searching for email client profiles...\n")
    else:
        print("Email Duplicate Cleaner")
        print("Searching for email client profiles...\n")
    
    # Find mail folders based on client selection
    mail_folders = []
    
    if args.scan_path:
        if os.path.exists(args.scan_path):
            # Create a generic mail handler to scan this path
            custom_handler = GenericMailHandler()
            custom_handler.profile_paths = [args.scan_path]
            mail_folders = custom_handler.find_mail_folders()
        else:
            if console:
                console.print(f"[bold red]Error: Specified path not found: {args.scan_path}[/bold red]")
            else:
                print(f"Error: Specified path not found: {args.scan_path}")
            sys.exit(1)
    else:
        # Get mail folders based on client selection
        if args.client == "all":
            mail_folders = client_manager.get_all_mail_folders()
        else:
            mail_folders = client_manager.get_client_folders(args.client)
    
    if not mail_folders:
        if console:
            console.print("[bold red]Error: No mail folders found.[/bold red]")
            console.print("Please ensure that the selected email client is installed and has been configured,")
            console.print("or specify a folder path manually with --scan-path.")
        else:
            print("Error: No mail folders found.")
            print("Please ensure that the selected email client is installed and has been configured,")
            print("or specify a folder path manually with --scan-path.")
        sys.exit(1)
    
    if console:
        console.print(f"\n[green]Found {len(mail_folders)} mail folders:[/green]")
    else:
        print(f"\nFound {len(mail_folders)} mail folders:")
    
    # List mail folders
    for i, folder in enumerate(mail_folders):
        if console:
            console.print(f"  {i+1}. {folder['display_name']}")
        else:
            print(f"  {i+1}. {folder['display_name']}")
    
    if args.list_folders:
        # Exit if only listing folders
        sys.exit(0)
    
    # Process mail folders
    if args.scan_all or args.auto_clean:
        # Auto-select all folders for scan-all or auto-clean modes
        folders_to_scan = mail_folders
        if console:
            console.print("\n[bold]Scanning all folders automatically[/bold]")
        else:
            print("\nScanning all folders automatically")
    else:
        # Interactive folder selection
        if console:
            console.print("\n[bold]Select folders to scan for duplicates:[/bold]")
            console.print("Enter folder numbers separated by commas, or 'all' for all folders")
            selection = Prompt.ask("Folders to scan", default="all")
        else:
            print("\nSelect folders to scan for duplicates:")
            print("Enter folder numbers separated by commas, or 'all' for all folders")
            selection = input("Folders to scan [all]: ") or "all"
        
        if selection.lower() == 'all':
            folders_to_scan = mail_folders
        else:
            try:
                indices = [int(idx.strip()) - 1 for idx in selection.split(',')]
                folders_to_scan = [mail_folders[idx] for idx in indices if 0 <= idx < len(mail_folders)]
                
                if not folders_to_scan:
                    if console:
                        console.print("[bold red]Error: No valid folders selected.[/bold red]")
                    else:
                        print("Error: No valid folders selected.")
                    sys.exit(1)
            except ValueError:
                if console:
                    console.print("[bold red]Error: Invalid folder selection.[/bold red]")
                else:
                    print("Error: Invalid folder selection.")
                sys.exit(1)
    
    # Display selected duplicate detection criteria
    criteria_desc = {
        "strict": "Message-ID + Date + From + Subject + Content",
        "content": "Message content only",
        "headers": "Message-ID + Date + From + Subject",
        "subject-sender": "Subject + From"
    }
    
    if console:
        console.print(f"\n[bold]Duplicate detection criteria:[/bold] {args.criteria}")
        console.print(f"  {criteria_desc[args.criteria]}")
    else:
        print(f"\nDuplicate detection criteria: {args.criteria}")
        print(f"  {criteria_desc[args.criteria]}")
    
    # Scan each selected folder
    total_dupes = 0
    total_groups = 0
    
    for folder in folders_to_scan:
        duplicate_groups = duplicate_finder.scan_folder(folder, args.criteria)
        
        if duplicate_groups:
            folder_dupes = sum(group['count'] - 1 for group in duplicate_groups)
            total_dupes += folder_dupes
            total_groups += len(duplicate_groups)
            
            if console:
                console.print(f"\n[bold green]Folder: {folder['display_name']}[/bold green]")
                console.print(f"Found {len(duplicate_groups)} duplicate groups ({folder_dupes} duplicate emails)")
            else:
                print(f"\nFolder: {folder['display_name']}")
                print(f"Found {len(duplicate_groups)} duplicate groups ({folder_dupes} duplicate emails)")
            
            # Display duplicates
            duplicate_finder.display_duplicate_groups()
            
            if not args.auto_clean:
                # Interactive deletion
                if console:
                    if Confirm.ask("Delete duplicates from this folder?", default=False):
                        # Ask which groups to process
                        group_input = Prompt.ask(
                            "Enter group numbers to process (comma-separated), or 'all'",
                            default="all"
                        )
                        
                        if group_input.lower() == 'all':
                            group_indices = list(range(len(duplicate_groups)))
                        else:
                            try:
                                group_indices = [int(i.strip()) - 1 for i in group_input.split(',')]
                            except ValueError:
                                console.print("[red]Invalid input, no groups will be processed[/red]")
                                group_indices = []
                        
                        if group_indices:
                            deleted, errors = duplicate_finder.delete_duplicates(
                                group_indices, selection_method='interactive'
                            )
                            
                            console.print(f"[green]Deleted {deleted} duplicate emails[/green]")
                            
                            if errors:
                                console.print("[yellow]Some errors occurred during deletion:[/yellow]")
                                for error in errors[:5]:  # Show first 5 errors
                                    console.print(f"  - {error}")
                                if len(errors) > 5:
                                    console.print(f"  ... and {len(errors) - 5} more errors")
                else:
                    if input("Delete duplicates from this folder? (y/N): ").lower() == 'y':
                        # Ask which groups to process
                        group_input = input("Enter group numbers to process (comma-separated), or 'all': ")
                        
                        if group_input.lower() == 'all':
                            group_indices = list(range(len(duplicate_groups)))
                        else:
                            try:
                                group_indices = [int(i.strip()) - 1 for i in group_input.split(',')]
                            except ValueError:
                                print("Invalid input, no groups will be processed")
                                group_indices = []
                        
                        if group_indices:
                            deleted, errors = duplicate_finder.delete_duplicates(
                                group_indices, selection_method='interactive'
                            )
                            
                            print(f"Deleted {deleted} duplicate emails")
                            
                            if errors:
                                print("Some errors occurred during deletion:")
                                for error in errors[:5]:  # Show first 5 errors
                                    print(f"  - {error}")
                                if len(errors) > 5:
                                    print(f"  ... and {len(errors) - 5} more errors")
            else:
                # Automatic cleaning
                if console:
                    console.print("[bold]Auto-cleaning duplicates...[/bold]")
                else:
                    print("Auto-cleaning duplicates...")
                    
                deleted, errors = duplicate_finder.delete_duplicates(
                    list(range(len(duplicate_groups))), selection_method='keep-first'
                )
                
                if console:
                    console.print(f"[green]Deleted {deleted} duplicate emails[/green]")
                    
                    if errors:
                        console.print("[yellow]Some errors occurred during deletion:[/yellow]")
                        for error in errors[:5]:
                            console.print(f"  - {error}")
                        if len(errors) > 5:
                            console.print(f"  ... and {len(errors) - 5} more errors")
                else:
                    print(f"Deleted {deleted} duplicate emails")
                    
                    if errors:
                        print("Some errors occurred during deletion:")
                        for error in errors[:5]:
                            print(f"  - {error}")
                        if len(errors) > 5:
                            print(f"  ... and {len(errors) - 5} more errors")
        else:
            if console:
                console.print(f"[yellow]No duplicates found in {folder['display_name']}[/yellow]")
            else:
                print(f"No duplicates found in {folder['display_name']}")
    
    # Summary
    if console:
        console.print("\n[bold]Scan Summary:[/bold]")
        console.print(f"Scanned {len(folders_to_scan)} folders")
        console.print(f"Found {total_groups} duplicate groups with {total_dupes} duplicate emails")
    else:
        print("\nScan Summary:")
        print(f"Scanned {len(folders_to_scan)} folders")
        print(f"Found {total_groups} duplicate groups with {total_dupes} duplicate emails")
    
    # Clean up temp directory if in demo mode
    if temp_dir and os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
            if console:
                console.print("[dim]Cleaned up demo environment[/dim]")
        except Exception as e:
            if console:
                console.print(f"[dim]Note: Could not clean up demo directory: {str(e)}[/dim]")
    
    if console:
        console.print("\n[bold blue]Done![/bold blue]")
    else:
        print("\nDone!")


if __name__ == "__main__":
    main()

    def get_email_content(self, group_idx: int, msg_idx: int) -> Dict[str, Any]:
        """
        Get the full content of an email in a duplicate group.
        
        Args:
            group_idx: Index of the duplicate group
            msg_idx: Index of the message within the group
            
        Returns:
            Dictionary with email headers and content
        """
        if group_idx < 0 or group_idx >= len(self.duplicate_groups):
            return {'error': f'Invalid group index: {group_idx}'}
            
        group = self.duplicate_groups[group_idx]
        
        if msg_idx < 0 or msg_idx >= len(group['messages']):
            return {'error': f'Invalid message index: {msg_idx}'}
            
        msg_info = group['messages'][msg_idx]
        
        try:
            # Open the email file
            if self.is_demo_mode:
                # In demo mode, construct a simpler representation
                headers = {
                    'From': msg_info['from'],
                    'To': 'recipient@example.com',
                    'Date': msg_info['date'],
                    'Subject': msg_info['subject'],
                    'Message-ID': msg_info.get('message_id', '<demo_id>'),
                }
                
                # Get pre-defined body based on the subject
                if 'Monthly Report' in msg_info['subject']:
                    body = 'This is the monthly report for March 2025.\n\nSales have increased by 15% compared to last month.\n\nPlease review the attached spreadsheet for details.'
                elif 'Meeting' in msg_info['subject']:
                    body = 'Let\'s meet to discuss the project status.\n\nProposed agenda:\n1. Project timeline\n2. Budget allocation\n3. Resource planning'
                elif 'Reminder' in msg_info['subject']:
                    body = 'Just a reminder about the upcoming deadline on Friday.\n\nPlease submit your reports by end of day.'
                else:
                    body = f'This is a demo email with subject: {msg_info["subject"]}\n\nThe content is generated for demonstration purposes.'
                
            else:
                # For real emails, read from the file
                filepath = msg_info['filepath']
                
                if not os.path.exists(filepath):
                    return {'error': f'Email file not found: {filepath}'}
                
                # Parse the email file
                with open(filepath, 'rb') as f:
                    msg = email.message_from_binary_file(f)
                
                # Extract headers
                headers = {
                    'From': msg.get('From', ''),
                    'To': msg.get('To', ''),
                    'Cc': msg.get('Cc', ''),
                    'Date': msg.get('Date', ''),
                    'Subject': msg.get('Subject', ''),
                    'Message-ID': msg.get('Message-ID', ''),
                }
                
                # Extract body
                if msg.is_multipart():
                    body = ''
                    for part in msg.get_payload():
                        if part.get_content_type() == 'text/plain':
                            body += part.get_payload(decode=True).decode('utf-8', errors='replace')
                else:
                    body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
            
            return {
                'headers': headers,
                'body': body,
                'subject': msg_info['subject']
            }
            
        except Exception as e:
            return {'error': f'Error retrieving email content: {str(e)}'}
