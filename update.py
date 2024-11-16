import os
import re
import requests
import logging

# Configure logging with custom name and format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - MyScript - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('MyScript')

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
        logger.warning(f"Error fetching the base URL: {e}")
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
