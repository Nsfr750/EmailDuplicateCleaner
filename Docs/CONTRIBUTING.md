# Contributing to Email Duplicate Cleaner

## Welcome Contributors!

We appreciate your interest in contributing to Email Duplicate Cleaner. This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Nsfr750/EmailDuplicateCleaner.git
   cd EmailDuplicateCleaner
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Contribution Workflow

1. **Fork the Repository**
2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Follow PEP 8 style guidelines
   - Write clear, concise code
   - Add/update tests for new functionality

4. **Run Tests**
   ```bash
   pytest
   ```

5. **Commit Changes**
   - Use descriptive commit messages
   - Reference issue numbers if applicable

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help maintain a welcoming community

## Reporting Issues

- Use GitHub Issues
- Provide detailed information
- Include steps to reproduce
- Attach relevant logs or screenshots

## Development Guidelines

- Use type hints
- Write docstrings for all functions
- Maintain modular architecture
- Keep dependencies up to date

## Codebase Structure

The project is organized into a clean and modular structure to promote maintainability and ease of development. Key components include:

- **`email_duplicate_cleaner.py`**: The core logic for duplicate detection.
- **`email_cleaner_gui.py`**: The main file for the Tkinter-based GUI. It is responsible for the main window layout and coordinating UI events.
- **`struttura/`**: This directory contains all auxiliary GUI modules:
  - `menu.py`: Manages the main menu bar. To add or modify menu items, edit this file.
  - `about.py`, `help.py`, `sponsor.py`: These files define the dialog windows. Each window is a self-contained class.
  - `log_viewer.py`: A simple log viewer utility.
- **`lang/`**: Contains language files for internationalization.
- **`tests/`**: Unit and integration tests.

When contributing to the GUI, please follow the existing modular structure. New dialogs or complex UI components should be created in their own files within the `struttura/` directory.

## Areas of Contribution

- Bug fixes
- Performance improvements
- New email client support
- UI/UX enhancements
- Documentation

## Questions?

Open an issue or contact the maintainers.

Thank you for contributing!
