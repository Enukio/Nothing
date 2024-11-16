import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

def fetch_index_file(base_url, use_selenium=False, download_path="downloads", headers=None):
    """
    Fetch an index file (e.g., index-XXX.js) from a website.

    :param base_url: URL of the website to fetch from.
    :param use_selenium: Whether to use Selenium for dynamic content.
    :param download_path: Directory to save the file.
    :param headers: Optional headers for requests.
    """
    try:
        if not use_selenium:
            # Use `requests` for static scraping
            print(f"Connecting to {base_url} with requests...")
            response = requests.get(base_url, headers=headers, timeout=10)
            response.raise_for_status()

            # Find matching JavaScript files
            js_files = re.findall(r'src=["\'](index-[\w\d]+\.js)["\']', response.text)
            if not js_files:
                print("No matching index files found in static HTML.")
                return

            js_url = urljoin(base_url, js_files[0])
            print(f"Static: Found file: {js_url}")
            download_file(js_url, download_path, headers)

        else:
            # Use Selenium for dynamic scraping
            print(f"Connecting to {base_url} with Selenium...")
            service = Service("path/to/chromedriver")  # Update with your ChromeDriver path
            driver = webdriver.Chrome(service=service)
            driver.get(base_url)

            # Wait for page load and find script tags
            driver.implicitly_wait(10)
            scripts = driver.find_elements(By.TAG_NAME, "script")
            js_files = [script.get_attribute("src") for script in scripts if script.get_attribute("src")]
            js_files = [file for file in js_files if "index-" in file]

            if not js_files:
                print("No matching index files found dynamically.")
                return

            js_url = js_files[0]
            print(f"Dynamic: Found file: {js_url}")
            download_file(js_url, download_path, headers)

    except Exception as e:
        print(f"Error occurred: {e}")

def download_file(file_url, download_path, headers=None):
    """
    Downloads a file from a URL.

    :param file_url: URL of the file to download.
    :param download_path: Directory to save the file.
    :param headers: Optional headers for requests.
    """
    try:
        print(f"Downloading file: {file_url}")
        os.makedirs(download_path, exist_ok=True)
        file_name = os.path.basename(file_url)

        response = requests.get(file_url, headers=headers, timeout=10)
        response.raise_for_status()

        file_path = os.path.join(download_path, file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)

        print(f"File successfully downloaded to: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download file: {e}")

if __name__ == "__main__":
    base_url = "https://app.notpx.app"

    # Adjust options based on your need
    use_selenium = True  # Set to False if JavaScript isn't required
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    fetch_index_file(base_url, use_selenium=use_selenium, headers=headers)
