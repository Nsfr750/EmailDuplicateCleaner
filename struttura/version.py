# Version information follows Semantic Versioning 2.0.0 (https://semver.org/)
# Update version numbers as needed for releases
VERSION_MAJOR = 2
VERSION_MINOR = 5
VERSION_PATCH = 2

# Additional version qualifiers
VERSION_QUALIFIER = ''  # Could be 'alpha', 'beta', 'rc', or ''

def get_version():
    """
    Generate a full version string.
    """
    version_parts = [str(VERSION_MAJOR), str(VERSION_MINOR), str(VERSION_PATCH)]
    version_str = '.'.join(version_parts)
    
    if VERSION_QUALIFIER:
        version_str += f'-{VERSION_QUALIFIER}'
    
    return version_str

def get_version_info():
    """
    Provide a detailed version information dictionary.
    
    Returns:
        dict: Comprehensive version information
    """
    return {
        'major': VERSION_MAJOR,
        'minor': VERSION_MINOR,
        'patch': VERSION_PATCH,
        'qualifier': VERSION_QUALIFIER,
        'full_version': get_version()
    }

def check_version_compatibility(min_version):
    """
    Check if the current version meets the minimum required version.
    
    Args:
        min_version (str): Minimum version to compare against
    
    Returns:
        bool: True if current version is compatible, False otherwise
    """
    current_parts = [VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH]
    min_parts = [int(part) for part in min_version.split('.')]
    
    for current, minimum in zip(current_parts, min_parts):
        if current > minimum:
            return True
        elif current < minimum:
            return False
    
    return True

# Expose version as a module-level attribute for easy access

def show_version(parent=None):
    """
    Show the current version in a dialog.
    
    Args:
        parent: Parent widget for the dialog.
    """
    from PySide6.QtWidgets import QMessageBox, QApplication
    from PySide6.QtCore import Qt
    
    # Create a QApplication if one doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Create and show the message box
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle("Version Information")
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setTextFormat(Qt.RichText)
    
    version_info = get_version_info()
    
    # Format the message with HTML for better styling
    message = f"""
    <html>
    <body>
        <h2>Email Duplicate Cleaner</h2>
        <p><b>Version:</b> {version_info['full_version']}</p>
        <p><b>Build:</b> {version_info['major']}.{version_info['minor']}.{version_info['patch']}</p>
        <p> 2024 Nsfr750. All rights reserved.</p>
        <hr>
        <p style="font-size: 9pt; color: #666;">
            This software is licensed under the GPL v3.0 License.<br>
            Source code available at: 
            <a href="https://github.com/Nsfr750/EmailDuplicateCleaner">GitHub</a>
        </p>
    </body>
    </html>
    """
    
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    
    # Make links clickable
    msg_box.setTextInteractionFlags(Qt.TextBrowserInteraction)
    
    # Show the dialog
    msg_box.exec()
    
    # Clean up if we created the QApplication
    if app is not QApplication.instance():
        app.quit()

__version__ = get_version()
