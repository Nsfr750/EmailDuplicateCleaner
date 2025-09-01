# User Guide

This guide provides detailed instructions on how to use EmailDuplicateCleaner effectively.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Basic Operations](#basic-operations)
4. [Advanced Features](#advanced-features)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [Frequently Asked Questions](#frequently-asked-questions)

## Getting Started

### Launching the Application

#### GUI Mode
```bash
python email_cleaner_gui.py
```

#### Web Interface
```bash
python email_cleaner_web.py
```

### First Run Setup

1. **Account Configuration**
   - Click on 'Settings' > 'Add Account'
   - Enter your email credentials
   - Select the appropriate server settings
   - Test the connection

2. **Initial Scan**
   - Select the folders to scan
   - Choose scan options (aggressiveness, file types, etc.)
   - Click 'Start Scan'

## Interface Overview

### Main Window
- **Toolbar**: Quick access to common functions
- **Folder View**: Navigate your email folders
- **Preview Pane**: View email contents
- **Status Bar**: Shows current operation status

### Scan Results
- **Duplicate Groups**: Emails grouped by similarity
- **Preview**: Compare email contents
- **Actions**: Available operations for selected items

## Basic Operations

### Scanning for Duplicates
1. Select the folders to scan
2. Choose scan options
3. Click 'Start Scan'
4. Review the results

### Managing Duplicates
- **Select**: Click to select individual emails
- **Select Group**: Click the group header to select all duplicates
- **Preview**: Double-click to view email contents
- **Delete**: Remove selected emails
- **Mark as Read/Unread**: Change read status
- **Move**: Move emails to a different folder

## Advanced Features

### Custom Filters
Create custom filters to refine your duplicate search:

1. Go to 'Filters' > 'New Filter'
2. Define filter criteria (date range, sender, subject, etc.)
3. Save the filter for future use

### Batch Operations
Perform actions on multiple emails at once:
- Select multiple emails using Ctrl+Click or Shift+Click
- Right-click for context menu options
- Use the toolbar for quick actions

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| F5 | Refresh view |
| Del | Delete selected emails |
| Ctrl+A | Select all emails |
| Ctrl+F | Find emails |
| Ctrl+S | Save current view |
| F1 | Help |

## Frequently Asked Questions

### How do I recover deleted emails?
Deleted emails are moved to your email's trash folder. You can restore them from there.

### Can I schedule automatic scans?
Yes, use the built-in scheduler in Settings > Scheduler.

### How is the duplicate detection algorithm configured?
Adjust the sensitivity in Settings > Advanced > Duplicate Detection.

### Is my email data stored on your servers?
No, all processing is done locally on your computer.
