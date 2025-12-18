import logging
import sys


import logging
import sys

def setup_logger(name=__name__):
    """
    Sets up a logger that writes to console and a log file.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    #Writing into the console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


    #Writing into a file
    file_handler = logging.FileHandler('application.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger