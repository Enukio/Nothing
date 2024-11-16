import os
import requests

# Base URL of the API
BASE_URL = "https://notpx.app/api/v1/"
# Directory to save downloaded files
DOWNLOAD_DIR = "downloads"
# Example authentication token (if required)
AUTH_TOKEN = None  # Replace with your token if required

def list_files():
    """Fetches the list of available files from the API."""
    url = f"{BASE_URL}list-files"  # Replace with the actual listing endpoint
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()  # Assumes the response is a JSON list of file names
    except requests.exceptions.RequestException as e:
        print(f"Error fetching file list: {e}")
        return []

def download_file(file_name):
    """Downloads a file from the API."""
    url = f"{BASE_URL}{file_name}"
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}
    
    try:
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()
        
        # Create download directory if not exists
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        
        file_path = os.path.join(DOWNLOAD_DIR, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_name}: {e}")

def main():
    # Fetch the list of files
    file_list = list_files()
    
    if not file_list:
        print("No files available for download.")
        return

    print(f"Found {len(file_list)} files. Starting download...")
    
    # Download each file
    for file_name in file_list:
        download_file(file_name)

if __name__ == "__main__":
    main()
