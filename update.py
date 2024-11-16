import os
import re
import requests
import logging
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Custom logging formatter with colors
class ColorFormatter(logging.Formatter):
    def format(self, record):
        # Define color styles for log levels
        level_color = {
            'INFO': Fore.CYAN,          # INFO: Cyan
            'WARNING': Fore.MAGENTA,    # WARNING: Magenta
            'ERROR': Fore.YELLOW,       # ERROR: Yellow
            'CRITICAL': Fore.RED + Style.BRIGHT  # CRITICAL: Bright Red
        }.get(record.levelname, Fore.WHITE)  # Default to white
        
        # Add color to the log level and message
        record.levelname = f"{level_color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{Style.BRIGHT}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

# Configure logger
formatter = ColorFormatter('%(asctime)s - MyScript - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger('MyScript')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def download_js_file(url, output_dir):
    """
    Download a JavaScript file from the given URL and save it to the specified directory.

    :param url: The URL of the JavaScript file.
    :param output_dir: The directory where the file should be saved.
    """
    try:
        logger.info(f"Attempting to download file from: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        filename = os.path.basename(url)
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        logger.info(f"Successfully downloaded and saved: {file_path}")
    except requests.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")

def get_main_js_format(base_url, output_dir="./"):
    """
    Scrape the base page to find JavaScript files matching the pattern and download them.

    :param base_url: The URL of the webpage to scrape.
    :param output_dir: The directory to save the downloaded JavaScript files.
    :return: A list of URLs of downloaded JavaScript files or None if no matches are found.
    """
    try:
        logger.info(f"Fetching base URL: {base_url}")
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        content = response.text

        # Use regex to find JavaScript file paths
        matches = re.findall(r'src="(/.*?/index.*?\.js)"', content)
        if matches:
            logger.info(f"Found {len(matches)} JavaScript files matching the pattern.")
            matches = sorted(set(matches), key=len, reverse=True)  # Remove duplicates and sort
            downloaded_files = []

            for match in matches:
                full_url = f"https://notpx.app{match}"
                download_js_file(full_url, output_dir)
                downloaded_files.append(full_url)
            
            return downloaded_files
        else:
            logger.warning("No matching JavaScript files found.")
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching the base URL: {e}")
        return None

def test_logging():
    """
    Function to demonstrate colored log levels.
    """
    logger.info("INFO message.")
    logger.warning("WARNING message.")
    logger.error("ERROR message.")
    logger.critical("CRITICAL message.")

# Main block for execution
if __name__ == "__main__":
    # Test log levels with colors
    test_logging()

    # Simulate the JavaScript file download process
    BASE_URL = "https://app.notpx.app"
    OUTPUT_DIR = "./js_files"
    downloaded_files = get_main_js_format(BASE_URL, OUTPUT_DIR)
    if downloaded_files:
        logger.info(f"Downloaded files: {downloaded_files}")
    else:
        logger.info("No files were downloaded.")
