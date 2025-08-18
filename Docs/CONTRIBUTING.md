# Contributing to Email Duplicate Cleaner

Thank you for your interest in contributing to Email Duplicate Cleaner! We appreciate your time and effort in helping improve this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Development Environment Setup](#development-environment-setup)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [License](#license)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

1. **Check for existing issues** - Before creating a new issue, please check if a similar issue already exists.
2. **Create a new issue** - If you find a bug, please create an issue with a clear title and description.
3. **Provide details** - Include steps to reproduce, expected behavior, actual behavior, and any relevant screenshots or error messages.

### Suggesting Enhancements

1. **Check for existing suggestions** - Before suggesting an enhancement, check if it has already been suggested.
2. **Create a feature request** - Use the feature request template to describe your suggestion.
3. **Be specific** - Explain why this enhancement would be useful and how it should work.

### Your First Code Contribution

1. **Find an issue** - Look for issues labeled "good first issue" or "help wanted".
2. **Comment on the issue** - Let others know you're working on it.
3. **Follow the development setup** - See the [Development Environment Setup](#development-environment-setup) section.

### Pull Requests

1. **Fork the repository** and create your branch from `main`.
2. **Make your changes** following the coding standards.
3. **Test your changes** thoroughly.
4. **Update documentation** if necessary.
5. **Submit a pull request** with a clear title and description.

## Development Environment Setup

1. Fork and clone the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development dependencies
   ```
4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all new code
- Write docstrings for all public functions and classes
- Keep functions small and focused on a single task
- Write unit tests for new functionality

## Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

Example:
```
feat(ui): add dark mode support

Add a new dark mode theme option in the settings panel.

Closes #123
```

## License

By contributing, you agree that your contributions will be licensed under its GPL-3.0 License.
