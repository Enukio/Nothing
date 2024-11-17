import os
import re
import sys
import time
import requests
import logging
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Custom logging formatter with colors
class ColorFormatter(logging.Formatter):
    def format(self, record):
        level_color = {
            'INFO': Fore.CYAN,
            'WARNING': Fore.MAGENTA,
            'ERROR': Fore.YELLOW,
            'CRITICAL': Fore.RED + Style.BRIGHT
        }.get(record.levelname, Fore.WHITE)

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

def loading_bar(total_size, chunk_size, url):
    """
    Display a loading bar during download.
    :param total_size: Total file size in bytes.
    :param chunk_size: Size of each downloaded chunk in bytes.
    :param url: URL being downloaded (for logging).
    """
    bar_length = 30
    print(f"{Fore.GREEN}Downloading {url}{Style.RESET_ALL}")
    for progress in range(0, total_size, chunk_size):
        time.sleep(0.1)  # Simulate delay for each chunk
        percent = (progress + chunk_size) / total_size * 100
        bar = '#' * int((progress / total_size) * bar_length)
        sys.stdout.write(
            f"\r{Fore.YELLOW}[{bar:<30}] {percent:.2f}% {Style.RESET_ALL}"
        )
        sys.stdout.flush()
    print("\nDownload complete!")

def download_js_file(url, output_dir):
    """
    Download a JavaScript file from the given URL and save it to the specified directory.

    :param url: The URL of the JavaScript file.
    :param output_dir: The directory where the file should be saved.
    """
    try:
        logger.info(f"Attempting to download file from: {url}")
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        filename = os.path.basename(url)
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        total_size = int(response.headers.get('Content-Length', 0))  # Get total file size
        chunk_size = 1024  # Size of each chunk
        downloaded_size = 0

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    loading_bar(total_size, chunk_size, url)  # Update loading bar

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

        matches = re.findall(r'src="(/.*?/index.*?\.js)"', content)
        if matches:
            logger.info(f"Found {len(matches)} JavaScript files matching the pattern.")
            matches = sorted(set(matches), key=len, reverse=True)
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

# Main block for execution
if __name__ == "__main__":
    BASE_URL = "https://app.notpx.app"
    OUTPUT_DIR = "./js_files"
    downloaded_files = get_main_js_format(BASE_URL, OUTPUT_DIR)
    if downloaded_files:
        logger.info(f"Downloaded files: {downloaded_files}")
    else:
        logger.info("No files were downloaded.")
