"""
Analysis tab for the Email Duplicate Cleaner application.

This module contains the AnalysisTab class which provides analysis
and statistics about the duplicate emails found.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QFormLayout, QGroupBox
)
from PySide6.QtCore import Qt

from .. import get_string

class AnalysisTab(QWidget):
    """
    Tab for displaying analysis and statistics about duplicate emails.
    
    This tab provides insights into the duplicate emails found,
    including statistics, charts, and other analytical information.
    """
    
    def __init__(self, parent=None):
        """Initialize the analysis tab."""
        super().__init__(parent)
        self.parent = parent
        self.duplicate_stats = {}
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        main_layout = QVBoxLayout(self)
        
        # Create tab widget for different analysis views
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.summary_tab = self.create_summary_tab()
        self.details_tab = self.create_details_tab()
        self.charts_tab = self.create_charts_tab()
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.summary_tab, get_string('analysis_summary_tab'))
        self.tab_widget.addTab(self.details_tab, get_string('analysis_details_tab'))
        self.tab_widget.addTab(self.charts_tab, get_string('analysis_charts_tab'))
        
        # Add tab widget to main layout
        main_layout.addWidget(self.tab_widget)
        
        # Add stretch to push content to the top
        main_layout.addStretch()
    
    def create_summary_tab(self):
        """Create the summary tab with key statistics."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Summary group
        summary_group = QGroupBox(get_string('analysis_summary_group'))
        summary_layout = QFormLayout()
        
        # Summary statistics
        self.total_emails_label = QLabel("0")
        self.unique_emails_label = QLabel("0")
        self.duplicate_emails_label = QLabel("0")
        self.duplicate_groups_label = QLabel("0")
        self.space_wasted_label = QLabel("0 MB")
        
        # Add rows to form layout
        summary_layout.addRow(get_string('analysis_total_emails') + ":", self.total_emails_label)
        summary_layout.addRow(get_string('analysis_unique_emails') + ":", self.unique_emails_label)
        summary_layout.addRow(get_string('analysis_duplicate_emails') + ":", self.duplicate_emails_label)
        summary_layout.addRow(get_string('analysis_duplicate_groups') + ":", self.duplicate_groups_label)
        summary_layout.addRow(get_string('analysis_space_wasted') + ":", self.space_wasted_label)
        
        summary_group.setLayout(summary_layout)
        
        # Add group to tab layout
        layout.addWidget(summary_group)
        
        # Add stretch to push content to the top
        layout.addStretch()
        
        return tab
    
    def create_details_tab(self):
        """Create the details tab with a table of duplicate groups."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Create table widget
        self.details_table = QTableWidget()
        self.details_table.setColumnCount(5)
        self.details_table.setHorizontalHeaderLabels([
            get_string('analysis_table_group'),
            get_string('analysis_table_count'),
            get_string('analysis_table_size'),
            get_string('analysis_table_senders'),
            get_string('analysis_table_subjects')
        ])
        
        # Configure table properties
        self.details_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.details_table.verticalHeader().setVisible(False)
        self.details_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.details_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Add table to layout
        layout.addWidget(self.details_table)
        
        return tab
    
    def create_charts_tab(self):
        """Create the charts tab with visual representations of the data."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Placeholder for charts
        self.chart_placeholder = QLabel(get_string('analysis_charts_placeholder'))
        self.chart_placeholder.setAlignment(Qt.AlignCenter)
        
        # Add placeholder to layout
        layout.addWidget(self.chart_placeholder)
        
        return tab
    
    def update_analysis(self, duplicate_groups):
        """
        Update the analysis with new duplicate groups data.
        
        Args:
            duplicate_groups: List of duplicate email groups
        """
        if not duplicate_groups:
            self.clear_analysis()
            return
        
        # Calculate statistics
        total_emails = sum(len(group) for group in duplicate_groups)
        unique_emails = sum(1 for group in duplicate_groups for _ in group)
        duplicate_emails = total_emails - len(duplicate_groups)
        
        # Update summary tab
        self.total_emails_label.setText(str(total_emails))
        self.unique_emails_label.setText(str(unique_emails))
        self.duplicate_emails_label.setText(str(duplicate_emails))
        self.duplicate_groups_label.setText(str(len(duplicate_groups)))
        
        # Update details tab
        self.update_details_table(duplicate_groups)
        
        # TODO: Update charts when implemented
        
        # Store statistics for later use
        self.duplicate_stats = {
            'total_emails': total_emails,
            'unique_emails': unique_emails,
            'duplicate_emails': duplicate_emails,
            'duplicate_groups': len(duplicate_groups)
        }
    
    def update_details_table(self, duplicate_groups):
        """
        Update the details table with duplicate group information.
        
        Args:
            duplicate_groups: List of duplicate email groups
        """
        # Clear existing data
        self.details_table.setRowCount(0)
        
        # Add rows for each duplicate group
        for i, group in enumerate(duplicate_groups):
            if not group:
                continue
                
            # Calculate group statistics
            group_size = len(group)
            total_size = sum(email.get('size', 0) for email in group)
            senders = set(email.get('from', '') for email in group)
            subjects = set(email.get('subject', '') for email in group)
            
            # Create table row
            row = self.details_table.rowCount()
            self.details_table.insertRow(row)
            
            # Add cells to row
            self.details_table.setItem(row, 0, QTableWidgetItem(f"{i+1}"))
            self.details_table.setItem(row, 1, QTableWidgetItem(str(group_size)))
            self.details_table.setItem(row, 2, QTableWidgetItem(self.format_size(total_size)))
            self.details_table.setItem(row, 3, QTableWidgetItem(", ".join(senders)))
            self.details_table.setItem(row, 4, QTableWidgetItem(" | ".join(subjects)))
    
    def clear_analysis(self):
        """Clear all analysis data and reset the UI."""
        # Reset summary
        self.total_emails_label.setText("0")
        self.unique_emails_label.setText("0")
        self.duplicate_emails_label.setText("0")
        self.duplicate_groups_label.setText("0")
        self.space_wasted_label.setText("0 MB")
        
        # Clear details table
        self.details_table.setRowCount(0)
        
        # Clear stored statistics
        self.duplicate_stats = {}
    
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
