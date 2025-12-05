"""
Email Duplicate Cleaner - Database Initializator 2.5.2

This script initializes the database for the Email Duplicate Cleaner application.
It creates tables, sets up migrations, and provides utility functions for database management.
"""

import os
import sys
from flask import Flask
from flask_migrate import Migrate
from models import db, ScanHistory, EmailCleanRecord, UserSettings

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///emails.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }
    
    # Initialize extensions
    db.init_app(app)
    
    # Create migration instance
    # This will be initialized in the app context when needed
    app.migrate = Migrate(app, db)
    
    return app

def init_db():
    """Initialize the database with tables"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default user settings if not exist
        if not UserSettings.query.first():
            default_settings = UserSettings(
                default_client='all',
                default_criteria='strict',
                auto_clean=False
            )
            db.session.add(default_settings)
            db.session.commit()
            
        print("Database initialized successfully!")

def add_scan_history(client_type, folder_path, criteria, total_emails, duplicate_groups, duplicate_emails):
    """Add a new scan history record to the database"""
    app = create_app()
    
    with app.app_context():
        scan = ScanHistory(
            client_type=client_type,
            folder_path=folder_path,
            criteria=criteria,
            total_emails=total_emails,
            duplicate_groups=duplicate_groups,
            duplicate_emails=duplicate_emails
        )
        db.session.add(scan)
        db.session.commit()
        return scan.id

def add_clean_record(scan_id, cleaned_count, error_count, selection_method):
    """Add a new cleaning record to the database"""
    app = create_app()
    
    with app.app_context():
        clean_record = EmailCleanRecord(
            scan_id=scan_id,
            cleaned_count=cleaned_count,
            error_count=error_count,
            selection_method=selection_method
        )
        db.session.add(clean_record)
        db.session.commit()
        return clean_record.id

def get_user_settings():
    """Get the current user settings"""
    app = create_app()
    
    with app.app_context():
        settings = UserSettings.query.first()
        if not settings:
            # Create default settings if not exist
            settings = UserSettings(
                default_client='all',
                default_criteria='strict',
                auto_clean=False
            )
            db.session.add(settings)
            db.session.commit()
        
        return {
            'default_client': settings.default_client,
            'default_criteria': settings.default_criteria,
            'auto_clean': settings.auto_clean,
            'last_custom_folder': settings.last_custom_folder
        }

def update_user_settings(settings_dict):
    """Update user settings with the provided dictionary"""
    app = create_app()
    
    with app.app_context():
        settings = UserSettings.query.first()
        if not settings:
            settings = UserSettings()
            db.session.add(settings)
        
        # Update settings with provided values
        for key, value in settings_dict.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        
        db.session.commit()

def get_scan_history(limit=10):
    """Get recent scan history entries"""
    app = create_app()
    
    with app.app_context():
        scans = ScanHistory.query.order_by(ScanHistory.timestamp.desc()).limit(limit).all()
        
        results = []
        for scan in scans:
            cleaning_records = []
            for record in scan.cleaning_records:
                cleaning_records.append({
                    'cleaned_count': record.cleaned_count,
                    'error_count': record.error_count,
                    'selection_method': record.selection_method,
                    'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            results.append({
                'id': scan.id,
                'client_type': scan.client_type,
                'folder_path': scan.folder_path,
                'criteria': scan.criteria,
                'total_emails': scan.total_emails,
                'duplicate_groups': scan.duplicate_groups,
                'duplicate_emails': scan.duplicate_emails,
                'timestamp': scan.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'cleaning_records': cleaning_records
            })
        
        return results

if __name__ == "__main__":
    # If run as a script, initialize the database
    init_db()
