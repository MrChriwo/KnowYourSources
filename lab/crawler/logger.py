import logging
import sys


class logger:
    def __init__(self, logfile, level=logging.INFO, name='[logger]'):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)

        # Create file handler
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.INFO)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter(name + '%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
