"""
Struttura Package

This package contains core components for the Email Duplicate Cleaner application.
"""

# Make the struttura package importable
from pathlib import Path

# Add the parent directory to the Python path
import sys
import os

# Get the directory containing this file
current_dir = Path(__file__).parent

# Add the project root to the Python path if it's not already there
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
