"""
Email Duplicate Cleaner - Database Models

This module contains database models for the Email Duplicate Cleaner application.
These models are used to store email scanning history, user settings, and other data.
"""

import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class ScanHistory(db.Model):
    """Model for tracking scan history"""
    id = db.Column(db.Integer, primary_key=True)
    client_type = db.Column(db.String(50), nullable=False)
    folder_path = db.Column(db.String(1024), nullable=False)
    criteria = db.Column(db.String(50), nullable=False, default='strict')
    total_emails = db.Column(db.Integer, default=0)
    duplicate_groups = db.Column(db.Integer, default=0)
    duplicate_emails = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ScanHistory {self.folder_path} ({self.timestamp})>"

class EmailCleanRecord(db.Model):
    """Model for tracking cleaning operations"""
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scan_history.id'))
    cleaned_count = db.Column(db.Integer, default=0)
    error_count = db.Column(db.Integer, default=0)
    selection_method = db.Column(db.String(50), default='keep-first')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    scan = db.relationship('ScanHistory', backref=db.backref('cleaning_records', lazy=True))
    
    def __repr__(self):
        return f"<EmailCleanRecord {self.cleaned_count} emails ({self.timestamp})>"

class UserSettings(db.Model):
    """Model for storing user preferences"""
    id = db.Column(db.Integer, primary_key=True)
    default_client = db.Column(db.String(50), default='all')
    default_criteria = db.Column(db.String(50), default='strict')
    auto_clean = db.Column(db.Boolean, default=False)
    last_custom_folder = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f"<UserSettings client={self.default_client}, criteria={self.default_criteria}>"
class FilterSettings(db.Model):
    """Model for storing filter settings"""
    id = db.Column(db.Integer, primary_key=True)
    date_from = db.Column(db.DateTime, nullable=True)
    date_to = db.Column(db.DateTime, nullable=True)
    sender_domains = db.Column(db.String(1024), nullable=True)
    recipient_domains = db.Column(db.String(1024), nullable=True)
    size_min = db.Column(db.Integer, nullable=True)
    size_max = db.Column(db.Integer, nullable=True)
    attachment_types = db.Column(db.String(1024), nullable=True)
    regex_pattern = db.Column(db.String(1024), nullable=True)
    
    def __repr__(self):
        return f"<FilterSettings id={self.id}>"

class EmailStatistics(db.Model):
    """Model for tracking email statistics"""
    id = db.Column(db.Integer, primary_key=True)
    scan_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_space_saved = db.Column(db.Integer, default=0)  # In bytes
    duplicate_count = db.Column(db.Integer, default=0)
    most_common_sender = db.Column(db.String(255))
    avg_email_size = db.Column(db.Integer)  # In bytes
    largest_attachment = db.Column(db.Integer)  # In bytes
    
    def __repr__(self):
        return f"<EmailStatistics date={self.scan_date}>"
class CleaningStatistics(db.Model):
    """Model for tracking cleaning statistics"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    space_saved = db.Column(db.Integer, default=0)  # In bytes
    emails_cleaned = db.Column(db.Integer, default=0)
    folder_path = db.Column(db.String(1024))
    sender_domain = db.Column(db.String(255))
    
    def __repr__(self):
        return f"<CleaningStatistics date={self.date}>"
