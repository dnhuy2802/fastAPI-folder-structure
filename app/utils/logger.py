import logging
import os
import pytz
import traceback
from datetime import datetime

from config import CoreCFG


def exception_logging(exctype, value, tb):
    """
    Log exception by using the root logger.
    """
    write_val = {'exception_type': exctype.__name__,
                 'message': str(value) + " Traceback: " + str(traceback.format_tb(tb, 10))}
    logger.error(str(write_val))


def check_and_create_tmp_folder():
    """
    Check if tmp folder exists, create if not.
    """
    tmp_dir = "tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        print(f"Created directory: {tmp_dir}")
    return tmp_dir


def check_and_rotate_log_file(log_file_path, max_size_mb=10):
    """
    Check if log file exceeds max size and rotate if necessary.
    """
    max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
    
    if os.path.exists(log_file_path):
        file_size = os.path.getsize(log_file_path)
        if file_size >= max_size_bytes:
            # Remove the old log file
            os.remove(log_file_path)
            print(f"Log file {log_file_path} exceeded {max_size_mb}MB, removed and will create new one")


class CustomFormatter(logging.Formatter):

    green = "\x1b[0;32m"
    grey = "\x1b[38;5;248m"
    yellow = "\x1b[38;5;229m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[38;5;31m"
    white = "\x1b[38;5;255m"
    reset = "\x1b[38;5;15m"
    
    base_format = (f"{grey}%(asctime)s | %(threadName)s | {{level_color}}%(levelname)-3s{grey} | {blue}%(module)s:%(lineno)d{grey} - {white}%(message)s")
    
    FORMATS = {
        logging.INFO: base_format.format(level_color=green),
        logging.WARNING: base_format.format(level_color=yellow),
        logging.ERROR: base_format.format(level_color=red),
        logging.CRITICAL: base_format.format(level_color=bold_red),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class PlainFormatter(logging.Formatter):
    """
    Plain formatter for file logging without color codes.
    """
    def __init__(self):
        super().__init__(
            fmt="%(asctime)s | %(threadName)s | %(levelname)-8s | %(module)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )


def custom_logger(app_name="APP"):
    logger_r = logging.getLogger(name=app_name)
    
    # Clear existing handlers to avoid duplicates
    logger_r.handlers.clear()
    
    tz = pytz.timezone(CoreCFG.time_zone)
    logging.Formatter.converter = lambda *args: datetime.now(tz).timetuple()

    # Create tmp folder if it doesn't exist
    tmp_dir = check_and_create_tmp_folder()
    
    # Set up log file path
    log_file_path = os.path.join(tmp_dir, "fastapi_server.log")
    
    # Check and rotate log file if necessary
    check_and_rotate_log_file(log_file_path)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(CoreCFG.log_level)
    ch.setFormatter(CustomFormatter())

    # File handler
    fh = logging.FileHandler(log_file_path, encoding='utf-8')
    fh.setLevel(CoreCFG.log_level)
    fh.setFormatter(PlainFormatter())

    logger_r.setLevel(CoreCFG.log_level)
    logger_r.addHandler(ch)
    logger_r.addHandler(fh)

    return logger_r


logger = custom_logger(app_name=CoreCFG.app_name)

logger.info('Logger initiated')