"""
Logging module for the Email Duplicate Cleaner application.

This module provides a thread-safe logging system with PySide6 integration
for displaying logs in the GUI and saving them to a file.
"""

import datetime
import logging
import logging.handlers
import os
import queue
import sys
import threading
from pathlib import Path
from typing import Optional, Tuple

from PySide6.QtCore import QObject, Signal, QThread, QMutex, QMutexLocker, QTimer

# Constants
LOG_DIR = Path('logs')
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

# Thread-safe logging
_log_lock = threading.Lock()

class LogSignal(QObject):
    """Signals for thread-safe logging in the GUI."""
    log_message = Signal(str, str)  # message, level
    error_occurred = Signal(str, str)  # message, details

class ThreadSafeLogger:
    """Thread-safe logger with file and GUI output support."""
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ThreadSafeLogger, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._log_signal = LogSignal()
        self._mutex = QMutex()
        self._current_date = datetime.date.today()
        self._log_file = self._get_log_file_path()
        self._setup_logging()
        self._setup_daily_rotation()
        self._initialized = True

    def __del__(self):
        """Clean up resources without touching Qt objects that may be deleted.

        We intentionally avoid accessing QTimer or other Qt objects here to
        prevent RuntimeError when the underlying C++ objects have already been
        destroyed during application shutdown.
        """
        try:
            logging.shutdown()
        except Exception:
            # Best-effort cleanup; ignore errors during interpreter shutdown
            pass

    def _get_log_file_path(self) -> Path:
        """Generate log file path with current date."""
        date_str = datetime.date.today().strftime('%Y-%m-%d')
        return LOG_DIR / f'email_duplicate_cleaner_{date_str}.log'

    def _setup_logging(self):
        """Set up the logging configuration."""
        # Ensure log directory exists
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Get the root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Clear any existing handlers to prevent duplicate logs
        if root_logger.handlers:
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)
                handler.close()
        
        # Create formatter
        formatter = logging.Formatter(LOG_FORMAT)
        
        # Create file handler with current date
        file_handler = logging.FileHandler(self._log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Add handlers to the root logger
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        # Log the start of a new log file
        logging.info(f"{'='*50}")
        logging.info(f"Starting new log file: {self._log_file.name}")
        logging.info(f"Log level: {logging.getLevelName(root_logger.getEffectiveLevel())}")
        logging.info(f"{'='*50}")
    
    def _setup_daily_rotation(self):
        """Set up a timer to check for log rotation at midnight."""
        # Calculate time until midnight
        now = datetime.datetime.now()
        tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        msec_until_midnight = (tomorrow - now).total_seconds() * 1000
        
        # Set up timer to check for rotation
        self._rotation_timer = QTimer()
        self._rotation_timer.timeout.connect(self._check_log_rotation)
        self._rotation_timer.start(msec_until_midnight)
    
    def _check_log_rotation(self):
        """Check if we need to rotate the log file based on date change."""
        today = datetime.date.today()
        if today != self._current_date:
            with QMutexLocker(self._mutex):
                self._current_date = today
                self._log_file = self._get_log_file_path()
                self._setup_logging()
                
            # Reset the timer for next midnight
            self._setup_daily_rotation()

    def _write_log(self, level: str, message: str):
        """Thread-safe log writing."""
        with QMutexLocker(self._mutex):
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"[{timestamp}] [{level}] {message}"
            
            # Log to file and console
            logger = logging.getLogger()
            if level == 'DEBUG':
                logger.debug(message)
            elif level == 'INFO':
                logger.info(message)
            elif level == 'WARNING':
                logger.warning(message)
            elif level == 'ERROR':
                logger.error(message)
            elif level == 'CRITICAL':
                logger.critical(message)
            
            # Emit signal for GUI updates
            self._log_signal.log_message.emit(log_entry, level)

    def debug(self, message: str):
        """Log a debug message."""
        self._write_log('DEBUG', message)

    def info(self, message: str):
        """Log an info message."""
        self._write_log('INFO', message)

    def warning(self, message: str):
        """Log a warning message."""
        self._write_log('WARNING', message)

    def error(self, message: str, exc_info=None):
        """Log an error message with optional exception info."""
        if exc_info:
            import traceback
            message = f"{message}\n{traceback.format_exc()}"
        self._write_log('ERROR', message)
        self._log_signal.error_occurred.emit("An error occurred", message)

    def critical(self, message: str):
        """Log a critical error message."""
        self._write_log('CRITICAL', message)
        self._log_signal.error_occurred.emit("Critical error", message)

    def exception(self, message: str):
        """Log an exception with traceback."""
        import traceback
        self._write_log('ERROR', f"{message}\n{traceback.format_exc()}")
        self._log_signal.error_occurred.emit("Exception occurred", message)

# Global logger instance
logger = ThreadSafeLogger()

# Backward compatibility functions
def log_info(message: str):
    """Log an info message (legacy compatibility)."""
    logger.info(message)

def log_warning(message: str):
    """Log a warning message (legacy compatibility)."""
    logger.warning(message)

def log_error(message: str):
    """Log an error message (legacy compatibility)."""
    logger.error(message)

def log_exception(exc_type, exc_value, exc_tb):
    """Log an uncaught exception (legacy compatibility)."""
    import traceback
    logger.error(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_tb)
    )

def setup_global_exception_logging():
    """Set up global exception handling (legacy compatibility)."""
    sys.excepthook = log_exception

class LogWorker(QThread):
    """Worker thread for handling log messages in the background."""
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue
        self.running = True

    def run(self):
        """Process log messages from the queue."""
        while self.running:
            try:
                record = self.log_queue.get(timeout=0.1)
                if record is None:  # Shutdown signal
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in log worker: {e}")

    def stop(self):
        """Stop the log worker thread."""
        self.running = False
        self.wait()

def setup_logging(log_level=logging.INFO):
    """
    Set up logging for the application.
    
    This function is now a compatibility layer that ensures the global logger
    is properly initialized. The actual logging configuration is handled by
    the ThreadSafeLogger class.
    
    Args:
        log_level: Minimum logging level (for backward compatibility)
        
    Returns:
        tuple: (None, None) as the queue-based logging is now handled internally
    """
    # Just ensure the global logger is initialized
    # The actual logging setup is handled by ThreadSafeLogger._setup_logging()
    return None, None
