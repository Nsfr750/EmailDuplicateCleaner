# Email Duplicate Cleaner

A Python tool to scan, identify, and remove duplicate emails from various email clients. Offers web-based, desktop graphical, and command-line interfaces.

## Features

- Automatically detects email client profiles (Thunderbird, Apple Mail, Outlook, Generic mbox/maildir formats)
- Multiple interfaces (Web, GUI, CLI)
- Dark mode and debug mode support
- Multiple duplicate detection criteria
- Interactive cleaning with preview
- Demo mode for testing


## Getting Started

### Installation

1. Clone this repository
2. Install the required dependencies:
```
pip install -r requirements.txt
```

### Running the Application

1. Click the Run button to start in demo mode
2. Choose an interface:
   - Web: Access via port 5000
   - GUI: Native window interface
   - CLI: Command-line interface

## Usage Examples

### Web Interface
```
python email_cleaner_web.py
```
Access at `http://0.0.0.0:5000`

### Desktop GUI
```
python email_cleaner_gui.py
```

### Command Line Demo
```
python email_duplicate_cleaner.py --demo
```

## Detection Methods

- `strict`: Message-ID + Date + From + Subject + Content
- `content`: Content only
- `headers`: Message-ID + Date + From + Subject  
- `subject-sender`: Subject + From fields only

## Safety Features

- Always preserves at least one copy of each email
- Keeps oldest email by default
- Original emails recoverable from trash
- Demo mode for safe testing

## Project Structure

- `email_cleaner_web.py`: Web interface
- `email_cleaner_gui.py`: Desktop GUI 
- `email_duplicate_cleaner.py`: Core functionality and CLI
- `static/`: Web assets (CSS, JS)
- `templates/`: HTML templates

## Workflows

- Demo Mode: Runs with test emails
- Help: Shows usage information 
- GUI Mode: Launches desktop interface
- Web Mode: Starts web server

## Social Links

<<<<<<< HEAD
- [GitHub](https://github.com/Nsfr750)
- [Patreon](https://www.patreon.com/Nsfr750)
- [Discord](https://discord.gg/BvvkUEP9)
- [Paypal](https://paypal.me/3dmega)
=======
- [Patreon](https://www.patreon.com/Nsfr750)
- [GitHub](https://github.com/Nsfr750)
- [Discord](https://discord.gg/BvvkUEP9)
- [Payapal](https://paypal.me/3dmega)
>>>>>>> 6739661d04695ad084125677d7e26bb86239d054
