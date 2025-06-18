# 📧 Email Duplicate Cleaner

A comprehensive Python tool designed to scan, identify, and remove duplicate emails across multiple email clients. Featuring web, desktop, and command-line interfaces.

## 🚀 Version

**Current Version:** 2.3.3 (Stable)
[![GitHub release](https://img.shields.io/badge/release-v2.3.3-blue)](https://github.com/Nsfr750/EmailDuplicateCleaner)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen)](https://github.com/Nsfr750/EmailDuplicateCleaner/blob/master/README.md)
[![Python Versions](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12-blue)](https://www.python.org/)

## ✨ Features

### 🔍 Duplicate Detection
- Multiple detection criteria:
  - Strict: Comprehensive comparison
  - Content Only: Message body analysis
  - Headers: Metadata-based matching
  - Subject+Sender: Focused identification

### 🖥️ Multi-Interface Support
- Web Interface
- Desktop GUI
- Command-Line Interface

### 🌓 Enhanced User Experience
- Modern web interface with dark/light mode
- Interactive preview with real-time updates
- Comprehensive help system
- Debug mode with detailed logging
- Demo mode for testing and learning

### 🔒 Email Client Compatibility
Supports:
- Mozilla Thunderbird
- Apple Mail
- Microsoft Outlook
- Generic mbox/maildir formats

### 🏗️ Technical Highlights
- Modern web interface built with Flask
- SQLAlchemy for database management
- Comprehensive help system with dynamic content
- Modular architecture with clear separation of concerns
- Cross-platform compatibility
- Extensive error handling and logging

## 🛠️ Prerequisites

- Python 3.8+
- pip
- Supported OS: Windows, macOS, Linux

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Nsfr750/EmailDuplicateCleaner.git
cd EmailDuplicateCleaner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

#### Web Interface
```bash
python email_cleaner_web.py
```
Access at `http://localhost:5000`

#### Desktop GUI
```bash
python email_cleaner_gui.py
```

#### Command Line Demo
```bash
python email_duplicate_cleaner.py --demo
```

## 🤝 Contributing

Interested in contributing? Check out our [Contributing Guidelines](CONTRIBUTING.md)!

## 📄 License

This project is licensed under the MIT License.

## 🐛 Issues

Found a bug? [Open an issue](https://github.com/Nsfr750/EmailDuplicateCleaner/issues)

## 📊 Detection Methods

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

- [GitHub](https://github.com/sponsors/Nsfr750)
- [Patreon](https://www.patreon.com/Nsfr750)
- [Discord](https://discord.gg/BvvkUEP9)
- [Paypal](https://paypal.me/3dmega)
