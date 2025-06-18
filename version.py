"""
Version management for Email Duplicate Cleaner.

This module provides a centralized version tracking system 
for the Email Duplicate Cleaner project.
"""

# Version information follows Semantic Versioning 2.0.0 (https://semver.org/)
VERSION_MAJOR = 2
VERSION_MINOR = 3
VERSION_PATCH = 3

# Additional version qualifiers
VERSION_QUALIFIER = ''  # Could be 'alpha', 'beta', 'rc', or ''

def get_version():
    """
    Generate a full version string.
    
    Returns:
        str: Formatted version string
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
    """
    current_version_parts = [VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH]
    min_version_parts = [int(part) for part in min_version.split('.')]
    
    for current, minimum in zip(current_version_parts, min_version_parts):
        if current > minimum:
            return True
        elif current < minimum:
            return False
    
    return True

# Expose version as a module-level attribute for easy access
__version__ = "2.3.3"
__release_date__ = "2025-06-18"

# Version history
VERSION_HISTORY = {
    "2.3.3": {
        "date": "2025-06-18",
        "changes": [
            "Fixed critical bugs in the web interface",
            "Added missing Flask route decorators for API endpoints",
            "Corrected JavaScript typo for history tab",
            "Improved template creation logic",
            "Enhanced error handling and database context management in APIs"
        ]
    },
    "2.3.0": {
        "date": "2025-05-20",
        "changes": [
            "Added web interface with modern design",
            "Implemented dark mode toggle",
            "Added comprehensive help system",
            "Improved error handling",
            "Enhanced user experience with better UI components"
        ]
    },
    "2.2.3": {
        "date": "2025-05-19",
        "changes": [
            "Initial web interface version",
            "Basic scanning and cleaning functionality",
            "History tracking",
            "Settings management"
        ]
    }
}
