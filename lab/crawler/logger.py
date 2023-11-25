import logging
import sys

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'ERROR': '\033[91m',  # Red
        'WARNING': '\033[93m',  # Orange
        'INFO': '\033[94m',  # Blue
        'RESET': '\033[0m'  # Reset color
    }

    def format(self, record):
        log_message = super().format(record)
        log_level = record.levelname

        if log_level in self.COLORS:
            return f"{self.COLORS[log_level]}{log_message}{self.COLORS['RESET']}"
        else:
            return log_message
        

class Logger:
    def __init__(self, logfile, level=logging.INFO, name='logger'):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)
        self.name = name

        # Create file handler
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.WARNING)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Create formatter and add it to the handlers
        file_formatter = logging.Formatter(f'[{self.name}' + ' %(levelname)s] %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        file_handler.setFormatter(file_formatter)

        console_formatter = ColoredFormatter(f'[{self.name}' + ' %(levelname)s] %(asctime)s %(message)s\n', datefmt='%m/%d/%Y %I:%M:%S %p')
        console_handler.setFormatter(console_formatter)

        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
