# API Reference

This document provides detailed information about the EmailDuplicateCleaner API for developers and integrators.

## Table of Contents

1. [Core Modules](#core-modules)
2. [Email Processing](#email-processing)
3. [Duplicate Detection](#duplicate-detection)
4. [Storage](#storage)
5. [Utilities](#utilities)
6. [Web API](#web-api)

## Core Modules

### `email_duplicate_cleaner.py`
Main entry point for the application.

**Functions:**
- `main()`: Application entry point
- `process_emails()`: Main processing function
- `load_config()`: Load configuration
- `save_config()`: Save configuration

### `email_analyzer.py`
Core email analysis functionality.

**Classes:**
- `EmailAnalyzer`: Main analysis class
  - `__init__(config)`: Initialize with configuration
  - `analyze_emails(emails)`: Process list of emails
  - `find_duplicates()`: Find duplicate emails
  - `get_stats()`: Get analysis statistics

## Email Processing

### `email_processor.py`
Handles email retrieval and processing.

**Classes:**
- `EmailProcessor`: Main processing class
  - `connect(server, username, password)`: Connect to email server
  - `fetch_emails(folder, criteria)`: Fetch emails matching criteria
  - `process_email(email)`: Process single email
  - `batch_process(emails)`: Process multiple emails

## Duplicate Detection

### `duplicate_detector.py`
Implements duplicate detection algorithms.

**Classes:**
- `DuplicateDetector`: Main detection class
  - `__init__(sensitivity=0.8)`: Initialize with sensitivity
  - `compare_emails(email1, email2)`: Compare two emails
  - `find_duplicate_groups(emails)`: Find groups of duplicates
  - `calculate_similarity(email1, email2)`: Calculate similarity score

## Storage

### `models.py`
Database models and data structures.

**Classes:**
- `Email`: Email data model
- `EmailAccount`: Email account configuration
- `ScanResult`: Results of a scan operation
- `UserSettings`: User preferences and settings

## Utilities

### `logging.py`
Logging configuration and utilities.

**Functions:**
- `setup_logging(config)`: Configure logging
- `get_logger(name)`: Get logger instance
- `log_error(message, exc_info=True)`: Log error with exception info

### `config_manager.py`
Configuration management.

**Classes:**
- `ConfigManager`: Manages application configuration
  - `load_config()`: Load configuration from file
  - `save_config()`: Save configuration to file
  - `get_setting(key, default=None)`: Get configuration setting
  - `set_setting(key, value)`: Update configuration setting

## Web API

### `email_cleaner_web.py`
RESTful API endpoints.

**Endpoints:**
- `GET /api/emails`: List emails
- `POST /api/emails/scan`: Start email scan
- `GET /api/emails/{id}`: Get email details
- `DELETE /api/emails/{id}`: Delete email
- `GET /api/duplicates`: List duplicate groups
- `POST /api/duplicates/resolve`: Resolve duplicates

### Authentication
All API endpoints require authentication. Include the API key in the `Authorization` header:
```
Authorization: Bearer YOUR_API_KEY
```

### Error Responses
Standard error responses include:
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid API key
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Rate Limiting
API is rate limited to 1000 requests per hour per API key.
