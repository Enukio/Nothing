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
        record.enukio = f"{Fore.RED}[Enukio]{Style.RESET_ALL}"
        record.msg = f"{Style.BRIGHT}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

# Configure logger
formatter = ColorFormatter('%(enukio)s - %(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger('[Enukio]')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def download_file_as_cgi(url, output_dir):
    """
    Download a file and save it with a .cgi extension.

    :param url: The URL of the file to download.
    :param output_dir: The directory where the file should be saved.
    """
    try:
        if not url.endswith('.js'):
            logger.warning(f"URL does not point to a JavaScript file: {url}")
            return

        logger.info(f"Attempting to download file from: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Extract filename and change extension to .cgi
        filename = os.path.basename(url).replace('.js', '.cgi')
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        with open(file_path, 'wb') as f:
            f.write(response.content)
        logger.info(f"Successfully downloaded and saved as CGI: {file_path}")
    except requests.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")

def get_js_files_and_save_as_cgi(base_url, output_dir="./"):
    """
    Scrape the base page to find JavaScript files, download them, and save as .cgi files.

    :param base_url: The URL of the webpage to scrape.
    :param output_dir: The directory to save the downloaded CGI files.
    """
    try:
        logger.info(f"Fetching base URL: {base_url}")
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        content = response.text

        # Use regex to find JavaScript file paths
        matches = re.findall(r'src="(.*?\.js)"', content)
        if matches:
            logger.info(f"Found {len(matches)} JavaScript files.")
            downloaded_files = []

            for match in matches:
                if match.startswith('http'):
                    full_url = match
                else:
                    full_url = f"{base_url.rstrip('/')}/{match.lstrip('/')}"

                download_file_as_cgi(full_url, output_dir)
                downloaded_files.append(full_url)

            return downloaded_files
        else:
            logger.warning("No JavaScript files found.")
            return []
    except requests.RequestException as e:
        logger.error(f"Error fetching the base URL: {e}")
        return []

# Main execution block
if __name__ == "__main__":
    BASE_URL = "https://app.notpx.app"
    OUTPUT_DIR = "./cgi_files"
    downloaded_files = get_js_files_and_save_as_cgi(BASE_URL, OUTPUT_DIR)
    if not downloaded_files:
        logger.info("No files were downloaded.")
