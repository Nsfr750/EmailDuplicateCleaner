# 📧 Email Duplicate Cleaner

A comprehensive Python tool designed to scan, identify, and remove duplicate emails across multiple email clients. Featuring web, desktop, and command-line interfaces.

## 🚀 Version

**Current Version:**
[![GitHub release](https://img.shields.io/badge/release-v2.5.2-green)](https://github.com/Nsfr750/EmailDuplicateCleaner)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen)](https://github.com/Nsfr750/EmailDuplicateCleaner/blob/master/README.md)
[![Python Versions](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12-blue)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI](https://img.shields.io/pypi/v/email-duplicate-cleaner)](https://pypi.org/project/email-duplicate-cleaner/)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/3dmega)

## ✨ What's New in 2.5.2

- 🚀 Updated to version 2.5.2
- 🐛 Fixed version number display in the about dialog
- 📚 Updated documentation to reflect the latest changes

## ✨ What's New in 2.5.1

- 🐛 Fixed QAction import error in PySide6 GUI
- 🌐 Added complete English translations
- 📄 Included GPL-3.0 license file
- 🔄 Improved error handling in GUI initialization
- ⬆️ Updated dependencies for better stability

## ✨ Features

### 🔍 Duplicate Detection

- Multiple detection criteria:
  - Strict: Comprehensive comparison
  - Content Only: Message body analysis
  - Headers: Metadata-based matching
  - Subject+Sender: Focused identification

### 📊 Email Analysis

- Advanced email analytics:
  - Sender analysis: Identify top senders and domains
  - Timeline analysis: Visualize email patterns over time
  - Attachment analysis: File types, sizes, and frequencies
  - Thread analysis: View and manage conversation threads
  - Duplicate analysis: Detailed duplicate detection insights
  - Exportable reports in multiple formats (Text, HTML, JSON)

### 🖥️ Multi-Interface Support

- **Web Interface** - Modern, responsive design with dark/light mode
- **Desktop GUI** - Native desktop experience with PySide6
- **Command-Line Interface** - Powerful automation and scripting support

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

### 💰 Support This Project

If you find this tool useful, please consider supporting its development:

- [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/3dmega) Support via PayPal
- :money_with_wings: **Monero (XMR)**: 
  ```
  47Jc6MC47WJVFhiQFYwHyBNQP5BEsjUPG6tc8R37FwcTY8K5Y3LvFzveSXoGiaDQSxDrnCUBJ5WBj6Fgmsfix8VPD4w3gXF
  ```

## 📦 Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/Nsfr750/EmailDuplicateCleaner.git
    cd EmailDuplicateCleaner
    ```

2.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

#### Web Interface

```bash
python app.py
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

This project is licensed under the GPL3 License.

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

## GUI Structure

- **GUI (`email_cleaner_gui.py`)**: A user-friendly graphical interface built with Tkinter. It provides an intuitive way to select email clients, scan folders, and manage duplicates.
- **CLI (`email_cleaner_cli.py`)**: A command-line interface for users who prefer working in the terminal.
- **Web (`app.py`)**: A web-based interface built with Flask, accessible from any browser.

### Auxiliary Modules (`struttura/`)

The `struttura/` directory contains all the auxiliary modules that support the GUI, such as dialog windows and the menu.

- **`menu.py`**: Manages the creation and functionality of the main menu bar, keeping the main GUI file clean and focused on its core layout.
- **`about.py`**, **`help.py`**, **`sponsor.py`**: Define the `About`, `Help`, and `Sponsor` dialog windows, each encapsulated in its own class.
- **`log_viewer.py`**: A simple log viewer to display application logs.

## GUI Features

- **Intuitive Interface**: A clean and easy-to-use graphical interface for managing email accounts and scanning for duplicates.
- **Multi-selection**: Use `Shift+Arrow Keys` and `Ctrl+Arrow Keys` to select multiple mailboxes and folders.
- **Multi-language Support**: Available in English and Italian.

### Command-Line Interface (CLI)

- **Help**: Shows usage information
- **Demo Mode**: Runs with test emails
- **GUI Mode**: Launches desktop interface
- **Web Mode**: Starts web server

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip
- Supported OS: Windows, macOS, Linux

## Social Links

- [GitHub](https://github.com/sponsors/Nsfr750)
- [Paypal](https://paypal.me/3dmega)
