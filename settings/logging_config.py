import logging
from dotenv import load_dotenv
import os
import re

def setup_logging():
    load_dotenv()
    level = os.getenv("LOGGING_LEVEL", "INFO").upper()
    level = re.sub(r'\W+', '', level)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler('app.log')
    # Console handler
    console_handler = logging.StreamHandler()

    # Set log levels
    log_level = logging.DEBUG if level == "DEBUG" else logging.INFO
    file_handler.setLevel(log_level)
    console_handler.setLevel(log_level)

    formatter = logging.Formatter('%(levelname)s - %(asctime)s - | %(filename)s | - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
