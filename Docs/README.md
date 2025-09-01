# EmailDuplicateCleaner Documentation

Welcome to the EmailDuplicateCleaner documentation! This guide will help you understand, install, and use the application effectively.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

EmailDuplicateCleaner is a powerful tool designed to help you manage and clean up duplicate emails in your mailbox. It supports various email providers and offers both GUI and command-line interfaces.

## Features

- **Duplicate Detection**: Find and manage duplicate emails efficiently
- **Multiple Email Providers**: Support for various email services
- **Flexible Filtering**: Advanced filtering options to fine-tune your search
- **Safe Operations**: Preview changes before applying them
- **User-friendly Interface**: Both GUI and CLI interfaces available

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Required system dependencies (see [PREREQUISITES.md](PREREQUISITES.md))

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Nsfr750/EmailDuplicateCleaner.git
   cd EmailDuplicateCleaner
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix/macOS
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Mode

```bash
python email_cleaner_gui.py
```

### Command Line Mode

```bash
python email_duplicate_cleaner.py [options]
```

### Web Interface

```bash
python email_cleaner_web.py
```

## Configuration

Configuration can be done through the GUI or by editing the `config.ini` file in the application directory.

## Troubleshooting

Common issues and solutions are documented in the [Troubleshooting Guide](TROUBLESHOOTING.md).

## Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

---

© 2025 Nsfr750. All rights reserved.
