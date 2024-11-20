import os
import re
import requests
import logging
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Custom logging formatter with colors
class ColorFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, name="Bot Name"):
        super().__init__(fmt, datefmt)
        self.name = name  # Set custom name
    def format(self, record):
        # Define color styles for log levels
        level_color = {
            'INFO': Fore.CYAN,          # INFO: Cyan
            'WARNING': Fore.MAGENTA,    # WARNING: Magenta
            'ERROR': Fore.YELLOW,       # ERROR: Yellow
            'CRITICAL': Fore.RED + Style.BRIGHT  # CRITICAL: Bright Red
        }.get(record.levelname, Fore.WHITE)  # Default to white

        # Add color to the log level
        record.levelname = f"{level_color}{record.levelname}{Style.RESET_ALL}"
        record.botname = f"{Fore.RED}[{self.name}]{Style.RESET_ALL}"
        record.msg = f"{Style.BRIGHT}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

# Configure logger
formatter = ColorFormatter('%(botname)s | %(asctime)s | %(levelname)s | %(message)s', '%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger('[{self.name}]')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def storage(filenames, output_file):
    
    try:
        with open(output_file, 'w') as f:
            for filename in filenames:
                f.write(filename + '\n')  # Write each filename on a new line
        logger.info(f"Saved {len(filenames)} filenames to {Fore.GREEN}{output_file}{Style.RESET_ALL} in specific order.")
    except Exception as e:
        logger.error(f"Failed to save filenames to {Fore.RED}{output_file}{Style.RESET_ALL}: {Fore.YELLOW}{e}{Style.RESET_ALL}")
        
def get_main_js_format(base_url, output_file="./cgi"):
    
    try:
        logger.info(f"Fetching base URL: {Fore.GREEN}{base_url}{Style.RESET_ALL}")
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        content = response.text

        # Use regex to find JavaScript file paths
        matches = re.findall(r'src="(/.*?/index.*?\.js)"', content)
        if matches:
            logger.info(f"Found {len(matches)} JavaScript files matching the pattern.")
            matches = sorted(set(matches), key=len, reverse=True)  # Remove duplicates and sort
            filenames = []

            for match in matches:
                # Extract the filename with .js extension
                filename = os.path.basename(match)
                filenames.append(filename)

            # Save the filenames to the output file in the specified order
            storage(filenames, output_file)
            return filenames
        else:
            logger.warning("No matching JavaScript files found.")
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching the base URL: {e}")
        return None

# Main block for execution
if __name__ == "__main__":
    # Simulate the JavaScript file fetching process
    BASE_URL = "https://example.com"  # Replace with your target URL
    OUTPUT_FILE = "./cgi"  # Save all filenames to this px file
    filenames = get_main_js_format(BASE_URL, OUTPUT_FILE)
    if not filenames:
        logger.info(f"{Fore.YELLOW}No filenames were saved.{Style.RESET_ALL}")