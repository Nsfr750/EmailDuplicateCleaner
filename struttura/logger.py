import datetime
import sys
import threading

LOG_FILE = 'traceback.log'
LOG_LEVELS = ("INFO", "WARNING", "ERROR")

_log_lock = threading.Lock()

def _write_log(level, message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    with _log_lock:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)

def log_info(message):
    _write_log("INFO", message)

def log_warning(message):
    _write_log("WARNING", message)

def log_error(message):
    _write_log("ERROR", message)

def log_exception(exc_type, exc_value, exc_tb):
    import traceback
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with _log_lock:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n[{timestamp}] [ERROR] Uncaught exception:\n")
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)

def setup_global_exception_logging():
    sys.excepthook = log_exception
