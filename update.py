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

def download_js_file(url, output_dir):
    """
    Download a JavaScript file from the given URL and save it to the specified directory.

    :param url: The URL of the JavaScript file.
    :param output_dir: The directory where the file should be saved.
    """
    try:
        logger.info(f"Attempting to download file from: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        # Extract the filename from the URL
        filename = os.path.basename(url)
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the file to the output directory
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"Successfully downloaded and saved: {file_path}")
    except requests.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")

def get_main_js_format(base_url, output_dir="./output_files"):
    """
    Scrape the base page to find JavaScript files matching the pattern and download them.

    :param base_url: The URL of the webpage to scrape.
    :param output_dir: The directory to save the downloaded JavaScript files.
    :return: A list of filenames or None if no matches are found.
    """
    try:
        logger.info(f"Fetching base URL: {base_url}")
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        content = response.text

        # Use regex to find JavaScript file paths in the HTML
        matches = re.findall(r'src="(/.*?/index.*?\.js)"', content)
        if matches:
            logger.info(f"Found {len(matches)} JavaScript files matching the pattern.")
            matches = sorted(set(matches), key=len, reverse=True)  # Remove duplicates and sort
            
            # Download each JavaScript file
            for match in matches:
                # Construct the full URL
                full_url = f"https://notpx.app{match}"
                download_js_file(full_url, output_dir)
            return matches
        else:
            logger.warning("No matching JavaScript files found.")
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching the base URL: {e}")
        return None

# Main block for execution
if __name__ == "__main__":
    # Base URL of the webpage to scrape
    BASE_URL = "https://app.notpx.app"  # Replace with your target URL
    
    # Output directory where the files will be saved
    OUTPUT_DIR = "./uhuk"
    
    # Start the scraping and downloading process
    js_files = get_main_js_format(BASE_URL, OUTPUT_DIR)
    
    if not js_files:
        logger.info("No JavaScript files were downloaded.")
