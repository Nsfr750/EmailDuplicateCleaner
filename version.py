"""
Version management for Email Duplicate Cleaner.

This module provides a centralized version tracking system 
for the Email Duplicate Cleaner project.
"""

# Version information follows Semantic Versioning 2.0.0 (https://semver.org/)
VERSION_MAJOR = 2
VERSION_MINOR = 2
VERSION_PATCH = 4

# Additional version qualifiers
VERSION_QUALIFIER = 'beta'  # Could be 'alpha', 'beta', 'rc', or ''

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
__version__ = get_version()
