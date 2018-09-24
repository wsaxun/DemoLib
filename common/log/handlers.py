import inspect
import os
import logging

_AUDIT = logging.INFO + 1
_TRACE = 5

def _get_binary_name():
    return os.path.basename(inspect.stack()[-1][1])

class ColorHandler(logging.StreamHandler):
    """Log handler that sets the 'color' key based on the level

    To use, include a '%(color)s' entry in the logging_context_format_string.
    There is also a '%(reset_color)s' key that can be used to manually reset
    the color within a log line.
    """
    LEVEL_COLORS = {
        _TRACE: '\033[00;35m',  # MAGENTA
        logging.DEBUG: '\033[00;32m',  # GREEN
        logging.INFO: '\033[00;36m',  # CYAN
        _AUDIT: '\033[01;36m',  # BOLD CYAN
        logging.WARN: '\033[01;33m',  # BOLD YELLOW
        logging.ERROR: '\033[01;31m',  # BOLD RED
        logging.CRITICAL: '\033[01;31m',  # BOLD RED
    }

    def format(self, record):
        record.color = self.LEVEL_COLORS[record.levelno]
        record.reset_color = '\033[00m'
        return logging.StreamHandler.format(self, record) + record.reset_color
