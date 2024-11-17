import os
import re
import requests
import logging
import time
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

        # Add color to the log level and "[Enukio]"
        record.levelname = f"{level_color}{record.levelname}{Style.RESET_ALL}"
        record.enukio = f"{Fore.RED}[Enukio]{Style.RESET_ALL}"  # [Enukio] in red
        record.msg = f"{Style.BRIGHT}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

# Configure logger
formatter = ColorFormatter('%(enukio)s - %(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger('[Enukio]')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def progress_bar(duration, width=30):
    """
    Display a progress bar for a specified duration.

    :param duration: Duration in seconds for the progress bar.
    :param width: Width of the progress bar in characters.
    """
    print(Fore.GREEN + "Processing... ", end='', flush=True)
    for i in range(width + 1):
        percent = int((i / width) * 100)
        bar = f"[{'#' * i}{'.' * (width - i)}] {percent:3d}%"
        print(Fore.GREEN + bar, end='\r', flush=True)
        time.sleep(duration / width)
    print(Fore.GREEN + f"[{'#' * width}] 100% - Processing complete!\n", flush=True)

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

        # Trigger progress bar after successful download
        progress_bar(3, width=40)  # 3-second progress bar
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

            for match in matches:
                full_url = f"https://notpx.app{match}"
                download_js_file(full_url, output_dir)
        else:
            logger.warning("No matching JavaScript files found.")
    except requests.RequestException as e:
        logger.error(f"Error fetching the base URL: {e}")

# Main block for execution
if __name__ == "__main__":
    # Simulate the JavaScript file download process
    BASE_URL = "https://app.notpx.app"
    OUTPUT_DIR = "./js_files"
    get_main_js_format(BASE_URL, OUTPUT_DIR)
