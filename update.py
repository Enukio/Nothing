import logging

# Utility function to wrap text with ANSI color codes
def color_text(text, color_code):
    return f"{color_code}{text}\033[0m"

# ANSI color codes as constants
class Colors:
    DEBUG = "\033[94m"    # Blue
    INFO = "\033[92m"     # Green
    WARNING = "\033[93m"  # Yellow
    ERROR = "\033[91m"    # Red
    CRITICAL = "\033[95m" # Magenta
    RESET = "\033[0m"     # Reset

# Custom logging formatter
class TermuxColorFormatter(logging.Formatter):
    """
    Formatter that adds colors to logging output.
    """
    LEVEL_COLORS = {
        logging.DEBUG: Colors.DEBUG,
        logging.INFO: Colors.INFO,
        logging.WARNING: Colors.WARNING,
        logging.ERROR: Colors.ERROR,
        logging.CRITICAL: Colors.CRITICAL,
    }

    def format(self, record):
        # Get the color for the log level
        color = self.LEVEL_COLORS.get(record.levelno, Colors.RESET)
        
        # Apply color formatting
        formatted_message = color_text(f"{record.asctime} - {record.levelname} - {record.message}", color)
        
        # Define the log format
        formatter = logging.Formatter(fmt="%(message)s", datefmt='%Y-%m-%d')
        record.message = formatted_message
        return formatter.format(record)

# Set up logger
logger = logging.getLogger("TermuxLogger")
handler = logging.StreamHandler()
handler.setFormatter(TermuxColorFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Test logging messages
logger.debug("This is a DEBUG message")
logger.info("This is an INFO message")
logger.warning("This is a WARNING message")
logger.error("This is an ERROR message")
logger.critical("This is a CRITICAL message")
