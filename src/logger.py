"""
This module handles the logging configuration for the application.
It logs messages to both the console and a file named 'application.log'.
"""

import logging
import sys


def setup_logger(name=__name__):
    """
    Sets up a logger that writes to console and a log file.

    :param name: Name of the logger instance.
    :return: Configured logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if they already exist
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. File Handler
    file_handler = logging.FileHandler("application.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
