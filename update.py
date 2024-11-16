import os
import re
import requests
import logging
from colorama import Fore, Style

# Configure logging with color-coded levels
class CustomFormatter(logging.Formatter):
    """
    Custom logging formatter to add colors to specific log levels.
    """
    FORMATS = {
        logging.DEBUG: f"{Style.BRIGHT}{Fore.BLUE}%(asctime)s - MyScript - DEBUG - %(message)s{Style.RESET_ALL}",
        logging.INFO: f"{Style.BRIGHT}{Fore.GREEN}%(asctime)s - MyScript - INFO - %(message)s{Style.RESET_ALL}",
        logging.WARNING: f"{Style.BRIGHT}{Fore.YELLOW}%(asctime)s - MyScript - WARNING - %(message)s{Style.RESET_ALL}",
        logging.ERROR: f"{Style.BRIGHT}{Fore.RED}%(asctime)s - MyScript - ERROR - %(message)s{Style.RESET_ALL}",
        logging.CRITICAL: f"{Style.BRIGHT}{Fore.MAGENTA}%(asctime)s - MyScript - CRITICAL - %(message)s{Style.RESET_ALL}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, "%(message)s")
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

# Set up logger with the custom formatter
logger = logging.getLogger('MyScript')
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)  # Set the desired log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

def download_js_file(url, output_dir):
    """
    Download a JavaScript file from the given URL and save it to the specified directory.

    :param url: The URL of the JavaScript file.
    :param output_dir: The directory where the file should be saved.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        filename = os.path.basename(url)
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        logger.info(f"Downloaded and saved: {file_path}")
    except requests.RequestException as e:
        logger.warning(f"Failed to download {url}: {e}")

def get_main_js_format(base_url, output_dir="./"):
    """
    Scrape the base page to find JavaScript files matching the pattern and download them.

    :param base_url: The URL of the webpage to scrape.
    :param output_dir: The directory to save the downloaded JavaScript files.
    :return: A list of URLs of downloaded JavaScript files or None if no matches are found.
    """
    try:
        # Fetch the main page content
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
            logger.info("No matching JavaScript files found.")
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching the base URL: {e}")
        return None

# Example usage
if __name__ == "__main__":
    BASE_URL = "https://app.notpx.app"
    OUTPUT_DIR = "./js_files"
    downloaded_files = get_main_js_format(BASE_URL, OUTPUT_DIR)
    if downloaded_files:
        logger.info(f"Downloaded files: {downloaded_files}")
    else:
        logger.info("No files downloaded.")
