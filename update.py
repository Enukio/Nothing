import os
import re
import requests
from urllib.parse import urljoin

def download_index_file(base_url, download_path="downloads"):
    """
    Downloads a JavaScript index file (e.g., index-D2JmPGMg.js) from the specified URL.

    :param base_url: The base URL to scrape and download from.
    :param download_path: The directory to save the downloaded file.
    """
    try:
        print(f"Connecting to {base_url}...")
        # Send a GET request to fetch the HTML content
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()  # Check for HTTP request errors

        # Extract JavaScript file links matching 'index-*.js' pattern
        js_files = re.findall(r'src=["\'](index-[\w\d]+\.js)["\']', response.text)
        if not js_files:
            print("No matching index files found on the page.")
            return

        # Use the first match (you can modify to download all matches if needed)
        js_file = js_files[0]
        js_url = urljoin(base_url, js_file)  # Construct the full URL
        print(f"Found file: {js_file}")
        print(f"Full URL: {js_url}")

        # Ensure the download directory exists
        os.makedirs(download_path, exist_ok=True)

        # Download the JavaScript file
        print("Downloading the file...")
        file_response = requests.get(js_url, timeout=10)
        file_response.raise_for_status()

        # Save the file locally
        file_path = os.path.join(download_path, js_file)
        with open(file_path, "wb") as file:
            file.write(file_response.content)

        print(f"File successfully downloaded to: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Base URL of the website
    base_url = "https://app.notpx.app"

    # Run the script
    download_index_file(base_url)
