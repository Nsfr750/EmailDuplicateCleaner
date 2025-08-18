"""
Results tab for the Email Duplicate Cleaner application.

This module contains the ResultsTab class which displays and manages
duplicate email groups found during scanning, with Wand integration
for image processing and previews.
"""

import os
import tempfile
from pathlib import Path
from wand.image import Image as WandImage

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QSplitter, QTextEdit, QMessageBox, QMenu, QFileDialog,
    QLabel, QProgressDialog, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal, QSize, QUrl, QTimer
from PySide6.QtGui import QDesktopServices, QAction, QPixmap, QIcon

from .. import get_string

class ResultsTab(QWidget):
    """
    Tab for displaying and managing duplicate email groups.
    
    This tab shows the results of the duplicate scan and provides
    options for cleaning or exporting the results, with Wand integration
    for handling email previews and thumbnails.
    """
    
    # Signals
    clean_requested = Signal(list)  # List of group indices to clean
    preview_requested = Signal(dict)  # Email data for preview
    
    def __init__(self, parent=None):
        """Initialize the results tab."""
        super().__init__(parent)
        self.parent = parent
        self.duplicate_groups = []
        self.temp_dir = None
        
        # Create temporary directory for preview images
        self.create_temp_dir()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        main_layout = QVBoxLayout(self)
        
        # Create splitter for results and preview
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Results tree
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels([
            get_string('results_column_date'),
            get_string('results_column_from'),
            get_string('results_column_subject'),
            get_string('results_column_size')
        ])
        self.results_tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.results_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.results_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.results_tree.itemSelectionChanged.connect(self.update_preview)
        self.results_tree.setSelectionBehavior(QTreeWidget.SelectRows)
        self.results_tree.setIndentation(20)
        self.results_tree.setColumnWidth(0, 150)  # Date
        self.results_tree.setColumnWidth(1, 200)  # From
        self.results_tree.setColumnWidth(2, 300)  # Subject
        self.results_tree.setColumnWidth(3, 100)  # Size
        
        # Preview panel
        self.preview_panel = QTextEdit()
        self.preview_panel.setReadOnly(True)
        self.preview_panel.setAcceptRichText(True)
        
        # Add widgets to splitter
        self.splitter.addWidget(self.results_tree)
        self.splitter.addWidget(self.preview_panel)
        self.splitter.setSizes([600, 400])
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.btn_expand_all = QPushButton(get_string('results_expand_all_button'))
        self.btn_collapse_all = QPushButton(get_string('results_collapse_all_button'))
        self.btn_export = QPushButton(get_string('results_export_button'))
        self.btn_clean_selected = QPushButton(get_string('results_clean_selected_button'))
        self.btn_clean_all = QPushButton(get_string('results_clean_all_button'))
        
        # Set button icons
        self.btn_expand_all.setIcon(self.style().standardIcon(
            self.style().SP_TitleBarNormalButton))
        self.btn_collapse_all.setIcon(self.style().standardIcon(
            self.style().SP_TitleBarMinButton))
        self.btn_export.setIcon(self.style().standardIcon(
            self.style().SP_DialogSaveButton))
        self.btn_clean_selected.setIcon(self.style().standardIcon(
            self.style().SP_DialogDiscardButton))
        self.btn_clean_all.setIcon(self.style().standardIcon(
            self.style().SP_TrashIcon))
        
        button_layout.addWidget(self.btn_expand_all)
        button_layout.addWidget(self.btn_collapse_all)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_export)
        button_layout.addWidget(self.btn_clean_selected)
        button_layout.addWidget(self.btn_clean_all)
        
        # Add widgets to main layout
        main_layout.addWidget(self.splitter, 1)  # Stretch factor 1
        main_layout.addLayout(button_layout)
        
        # Connect signals
        self.btn_expand_all.clicked.connect(self.expand_all_groups)
        self.btn_collapse_all.clicked.connect(self.collapse_all_groups)
        self.btn_export.clicked.connect(self.export_results)
        self.btn_clean_selected.clicked.connect(self.clean_selected_groups)
        self.btn_clean_all.clicked.connect(self.clean_all_groups)
    
    def create_temp_dir(self):
        """Create a temporary directory for preview images."""
        if self.temp_dir is not None and os.path.exists(self.temp_dir):
            return
            
        self.temp_dir = tempfile.mkdtemp(prefix="email_duplicate_cleaner_")
    
    def cleanup_temp_dir(self):
        """Clean up the temporary directory and its contents."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                print(f"Error cleaning up temp directory: {e}")
    
    def update_results(self, duplicate_groups):
        """
        Update the results with new duplicate groups.
        
        Args:
            duplicate_groups: List of duplicate email groups
        """
        self.duplicate_groups = duplicate_groups
        self.results_tree.clear()
        
        for i, group in enumerate(duplicate_groups):
            if not group:
                continue
                
            # Create group item
            group_item = QTreeWidgetItem([
                "",  # Date
                f"{get_string('results_group')} {i+1} ({len(group)} {get_string('results_emails')})",
                "",  # Subject
                self.format_size(sum(email.get('size', 0) for email in group))
            ])
            group_item.setData(0, Qt.UserRole, {'type': 'group', 'index': i})
            self.results_tree.addTopLevelItem(group_item)
            
            # Add email items
            for email in group:
                email_item = QTreeWidgetItem([
                    email.get('date', ''),
                    email.get('from', ''),
                    email.get('subject', ''),
                    self.format_size(email.get('size', 0))
                ])
                email_item.setData(0, Qt.UserRole, {'type': 'email', 'data': email})
                group_item.addChild(email_item)
            
            # Expand the group by default
            group_item.setExpanded(True)
    
    def update_preview(self):
        """Update the preview panel with the selected email content."""
        selected_items = self.results_tree.selectedItems()
        if not selected_items:
            return
            
        item = selected_items[0]
        item_data = item.data(0, Qt.UserRole)
        
        if not item_data or item_data.get('type') != 'email':
            self.preview_panel.clear()
            return
            
        email_data = item_data.get('data', {})
        if not email_data:
            return
            
        # Format email content for preview
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 10px; }}
                .header {{ margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #ddd; }}
                .field {{ margin-bottom: 8px; }}
                .field-label {{ font-weight: bold; color: #555; }}
                .body {{ margin-top: 15px; white-space: pre-wrap; }}
                .attachments {{ margin-top: 15px; padding-top: 10px; border-top: 1px solid #eee; }}
                .attachment {{ margin: 5px 0; padding: 5px; background: #f5f5f5; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>{email_data.get('subject', get_string('no_subject'))}</h2>
            </div>
            
            <div class="field">
                <span class="field-label">{get_string('preview_from')}:</span>
                <span>{email_data.get('from', get_string('unknown_sender'))}</span>
            </div>
            
            <div class="field">
                <span class="field-label">{get_string('preview_to')}:</span>
                <span>{email_data.get('to', get_string('unknown_recipient'))}</span>
            </div>
            
            <div class="field">
                <span class="field-label">{get_string('preview_date')}:</span>
                <span>{email_data.get('date', get_string('unknown_date'))}</span>
            </div>
            
            <div class="field">
                <span class="field-label">{get_string('preview_size')}:</span>
                <span>{self.format_size(email_data.get('size', 0))}</span>
            </div>
        """
        
        # Add email body
        body = email_data.get('body', '')
        if body:
            html += f"""
            <div class="body">
                {body}
            </div>
            """
        
        # Add attachments if any
        attachments = email_data.get('attachments', [])
        if attachments:
            html += """
            <div class="attachments">
                <div class="field-label">Attachments:</div>
            """
            
            for i, attachment in enumerate(attachments, 1):
                filename = attachment.get('filename', f'file_{i}')
                size = self.format_size(attachment.get('size', 0))
                content_type = attachment.get('content_type', 'application/octet-stream')
                
                # Generate thumbnail for images using Wand
                thumbnail_html = ""
                if content_type.startswith('image/'):
                    thumbnail_path = self.generate_thumbnail(attachment)
                    if thumbnail_path:
                        thumbnail_html = f'<br><img src="{thumbnail_path}" style="max-width: 200px; max-height: 150px; margin-top: 5px;">'
                
                html += f"""
                <div class="attachment">
                    <div>{filename}</div>
                    <div style="font-size: 0.9em; color: #666;">
                        {content_type} • {size}
                    </div>
                    {thumbnail_html}
                </div>
                """
            
            html += "</div>"  # Close attachments div
        
        html += "</body></html>"
        
        # Set HTML content
        self.preview_panel.setHtml(html)
    
    def generate_thumbnail(self, attachment):
        """
        Generate a thumbnail for an image attachment using Wand.
        
        Args:
            attachment: Dictionary containing attachment data
            
        Returns:
            Path to the generated thumbnail or None if generation failed
        """
        if not attachment or 'data' not in attachment:
            return None
            
        try:
            # Create temp directory if it doesn't exist
            self.create_temp_dir()
            
            # Generate a unique filename for the thumbnail
            filename = attachment.get('filename', 'preview')
            ext = os.path.splitext(filename)[1].lower()
            if not ext:
                ext = '.jpg'
                
            temp_path = os.path.join(self.temp_dir, f"thumb_{hash(str(attachment))}{ext}")
            
            # Create thumbnail using Wand
            with WandImage(blob=attachment['data']) as img:
                # Resize while maintaining aspect ratio
                img.transform(resize='200x150>')
                img.format = 'jpeg' if ext.lower() in ('.jpg', '.jpeg') else ext[1:]
                img.save(filename=temp_path)
                
            return temp_path
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            return None
    
    def show_context_menu(self, position):
        """Show context menu for the results tree."""
        item = self.results_tree.itemAt(position)
        if not item:
            return
            
        item_data = item.data(0, Qt.UserRole)
        if not item_data:
            return
            
        menu = QMenu(self)
        
        if item_data.get('type') == 'email':
            view_action = QAction(get_string('menu_view_email'), self)
            view_action.triggered.connect(lambda: self.view_email(item_data['data']))
            menu.addAction(view_action)
            
            open_folder_action = QAction(get_string('menu_open_containing_folder'), self)
            open_folder_action.triggered.connect(lambda: self.open_containing_folder(item_data['data']))
            menu.addAction(open_folder_action)
            
            menu.addSeparator()
            
            copy_action = QAction(get_string('menu_copy_email_info'), self)
            copy_action.triggered.connect(lambda: self.copy_email_info(item_data['data']))
            menu.addAction(copy_action)
        
        menu.exec_(self.results_tree.viewport().mapToGlobal(position))
    
    def view_email(self, email_data):
        """View the full email in a separate window."""
        # Emit signal to show email in a separate window
        self.preview_requested.emit(email_data)
    
    def open_containing_folder(self, email_data):
        """Open the folder containing the email."""
        file_path = email_data.get('filepath')
        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, get_string('error'), get_string('file_not_found'))
            return
            
        folder_path = os.path.dirname(file_path)
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
    
    def copy_email_info(self, email_data):
        """Copy email information to clipboard."""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        
        info = f"From: {email_data.get('from', '')}\n"
        info += f"To: {email_data.get('to', '')}\n"
        info += f"Date: {email_data.get('date', '')}\n"
        info += f"Subject: {email_data.get('subject', '')}\n"
        info += f"Size: {self.format_size(email_data.get('size', 0))}\n"
        
        clipboard.setText(info)
        self.parent.statusBar().showMessage(get_string('email_info_copied'), 3000)
    
    def expand_all_groups(self):
        """Expand all groups in the results tree."""
        for i in range(self.results_tree.topLevelItemCount()):
            item = self.results_tree.topLevelItem(i)
            item.setExpanded(True)
    
    def collapse_all_groups(self):
        """Collapse all groups in the results tree."""
        for i in range(self.results_tree.topLevelItemCount()):
            item = self.results_tree.topLevelItem(i)
            item.setExpanded(False)
    
    def clean_selected_groups(self):
        """Clean the selected duplicate groups."""
        selected_items = self.results_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, get_string('warning'), get_string('no_groups_selected'))
            return
            
        # Get unique group indices from selected items
        group_indices = set()
        for item in selected_items:
            item_data = item.data(0, Qt.UserRole)
            if not item_data:
                continue
                
            if item_data.get('type') == 'group':
                group_indices.add(item_data.get('index'))
            elif item_data.get('type') == 'email':
                # Find the parent group
                parent = item.parent()
                if parent:
                    parent_data = parent.data(0, Qt.UserRole)
                    if parent_data and parent_data.get('type') == 'group':
                        group_indices.add(parent_data.get('index'))
        
        if not group_indices:
            QMessageBox.warning(self, get_string('warning'), get_string('no_valid_groups_selected'))
            return
            
        # Confirm before cleaning
        reply = QMessageBox.question(
            self,
            get_string('confirm_clean_title'),
            get_string('confirm_clean_message').format(count=len(group_indices)),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.clean_requested.emit(sorted(list(group_indices)))
    
    def clean_all_groups(self):
        """Clean all duplicate groups."""
        if not self.duplicate_groups:
            QMessageBox.warning(self, get_string('warning'), get_string('no_groups_to_clean'))
            return
            
        # Confirm before cleaning
        reply = QMessageBox.question(
            self,
            get_string('confirm_clean_all_title'),
            get_string('confirm_clean_all_message').format(count=len(self.duplicate_groups)),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.clean_requested.emit(list(range(len(self.duplicate_groups))))
    
    def export_results(self):
        """Export the results to a file."""
        if not self.duplicate_groups:
            QMessageBox.information(self, get_string('info'), get_string('no_results_to_export'))
            return
            
        # Get save file name
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            get_string('export_dialog_title'),
            os.path.expanduser("~/duplicate_emails.txt"),
            "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return  # User cancelled
            
        try:
            if file_path.lower().endswith('.csv'):
                self.export_to_csv(file_path)
            else:
                self.export_to_text(file_path)
                
            QMessageBox.information(
                self,
                get_string('export_success_title'),
                get_string('export_success_message').format(path=file_path)
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                get_string('export_error_title'),
                get_string('export_error_message').format(error=str(e))
            )
    
    def export_to_text(self, file_path):
        """Export results to a text file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"=== {get_string('export_header')} ===\n\n")
            
            for i, group in enumerate(self.duplicate_groups, 1):
                f.write(f"{get_string('results_group')} {i} ({len(group)} {get_string('results_emails')}):\n")
                
                for email in group:
                    f.write(f"  - {email.get('date', '')} | {email.get('from', '')} | ")
                    f.write(f"{email.get('subject', '')} | {self.format_size(email.get('size', 0))}\n")
                
                f.write("\n")
    
    def export_to_csv(self, file_path):
        """Export results to a CSV file."""
        import csv
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'Group',
                'Date',
                'From',
                'To',
                'Subject',
                'Size',
                'File Path'
            ])
            
            # Write data
            for i, group in enumerate(self.duplicate_groups, 1):
                for email in group:
                    writer.writerow([
                        f"Group {i}",
                        email.get('date', ''),
                        email.get('from', ''),
                        email.get('to', ''),
                        email.get('subject', ''),
                        email.get('size', 0),
                        email.get('filepath', '')
                    ])
    
    @staticmethod
    def format_size(size_bytes):
        """
        Format a size in bytes to a human-readable string.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string (e.g., "1.5 MB")
        """
        if size_bytes == 0:
            return "0 B"
            
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        i = 0
        size = float(size_bytes)
        
        while size >= 1024 and i < len(units) - 1:
            size /= 1024
            i += 1
            
        return f"{size:.2f} {units[i]}"
    
    def closeEvent(self, event):
        """Clean up resources when the tab is closed."""
        self.cleanup_temp_dir()
        event.accept()