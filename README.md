# Email Duplicate Cleaner

A Python tool to scan, identify, and remove duplicate emails from various email clients. Offers web-based, desktop graphical, and command-line interfaces.

## Supported Email Clients

- Mozilla Thunderbird
- Apple Mail
- Microsoft Outlook (PST/OST files)
- Generic mbox/maildir formats

## Features

- Automatically detects email client profiles on Windows, macOS, and Linux
- Scans individual or all mail folders for duplicate messages
- Supports multiple duplicate detection criteria
- Provides web, desktop GUI, and CLI interfaces
- Interactive CLI with rich text formatting
- Preserves at least one copy of each email
- Includes demo mode for testing without an email client installation

## Usage

### Web Interface

To launch the web-based interface:

```
python email_cleaner_web.py
```

Then open http://localhost:5000 in your browser. The web interface provides all features in a responsive, browser-based UI:
- Select email client types and detection criteria 
- Browse and select mail folders to scan
- View duplicate emails with detailed information
- Clean selected or all duplicate groups with a single click
- Run in demo mode for testing
- Real-time console output display

### Desktop GUI Interface

To launch the desktop graphical user interface:

```
python email_cleaner_gui.py
```

The GUI provides easy access to all features:
- Select client types and detection criteria
- Browse and select mail folders to scan
- View duplicate emails in a tree view
- Clean selected or all duplicate groups with a single click
- Run in demo mode for testing

### Command-Line Interface

To try the tool with the built-in demo:

```
python email_duplicate_cleaner.py --demo
```

This creates a temporary mail folder with sample emails containing duplicates.

For automatic cleaning in demo mode:
```
python email_duplicate_cleaner.py --demo --auto-clean
```

### Advanced CLI Usage

Scan all supported email clients and interactively remove duplicates:

```
python email_duplicate_cleaner.py --scan-all
```

Scan a specific email client:

```
python email_duplicate_cleaner.py --client thunderbird --scan-all
```

Supported client options: 
- `thunderbird`
- `apple_mail`
- `outlook`
- `generic`
- `all` (default)

## Duplicate Detection Methods

The tool offers several methods for identifying duplicates:

- `strict` (default): Uses Message-ID, Date, From, Subject, and message body content
- `content`: Only compares message body content
- `headers`: Uses Message-ID, Date, From, and Subject
- `subject-sender`: Only compares Subject and From fields

## Safety Features

- Always preserves at least one copy of each email
- By default, keeps the oldest email in each duplicate group
- Original emails can be restored from your email client's trash folder if needed

**Note:** Always backup your email client's data files before using this tool on real emails.
# EmailDuplicateCleaner
