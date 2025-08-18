# Prerequisites

Before you can run or develop the Email Duplicate Cleaner, you'll need to have the following software installed on your system:

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux
- **Python**: 3.8 or higher
- **Pip**: Latest version
- **Git**: For version control

## Python Dependencies

All required Python packages are listed in `requirements.txt`. To install them, run:

```bash
pip install -r requirements.txt
```

### Development Dependencies (Optional)

For development, you might also want to install these additional tools:

- **Black**: For code formatting
  ```bash
  pip install black
  ```

- **Pylint**: For code linting
  ```bash
  pip install pylint
  ```

- **pytest**: For running tests
  ```bash
  pip install pytest
  ```

## Database

This application uses SQLite by default, which is included with Python. No additional setup is required for the database.

## Virtual Environment (Recommended)

It's recommended to use a virtual environment to manage dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

## Building from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/Nsfr750/EmailDuplicateCleaner.git
   cd EmailDuplicateCleaner
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Troubleshooting

If you encounter any issues during setup, please check the following:

1. Ensure Python 3.8+ is installed and in your PATH
2. Verify pip is up to date: `pip install --upgrade pip`
3. Check the [GitHub Issues](https://github.com/Nsfr750/EmailDuplicateCleaner/issues) for similar problems
4. If the issue persists, please open a new issue with details about your environment and the error message
