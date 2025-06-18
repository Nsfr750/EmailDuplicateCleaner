import os
import re
import datetime
import pytest
from struttura import logger

LOG_FILE = 'traceback.log'

def clean_log():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

def read_log():
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def test_log_info_and_warning_and_error():
    clean_log()
    logger.log_info('info test')
    logger.log_warning('warn test')
    logger.log_error('error test')
    contents = read_log()
    assert '[INFO] info test' in contents
    assert '[WARNING] warn test' in contents
    assert '[ERROR] error test' in contents

def test_log_exception():
    clean_log()
    try:
        raise ValueError('test exception')
    except Exception as e:
        logger.log_exception(type(e), e, e.__traceback__)
    contents = read_log()
    assert 'Uncaught exception:' in contents
    assert 'ValueError: test exception' in contents

def test_setup_global_exception_logging(monkeypatch):
    clean_log()
    logger.setup_global_exception_logging()
    # Simulate uncaught exception
    code = 'import struttura.logger\nstruttura.logger.setup_global_exception_logging()\nraise RuntimeError(\'uncaught!\')'
    import subprocess
    result = subprocess.run(['python', '-c', code], capture_output=True, text=True)
    # Should log the uncaught exception
    assert os.path.exists(LOG_FILE)
    contents = read_log()
    assert 'Uncaught exception:' in contents
    assert 'RuntimeError: uncaught!' in contents
