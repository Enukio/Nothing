import os
import re
import requests

# Function to fetch and parse the target file name
def get_dynamic_file(base_url, api_endpoint, file_pattern, headers=None):
    """
    Fetch the API or webpage content to extract the file name dynamically.

    :param base_url: Base URL of the website.
    :param api_endpoint: API endpoint or page path to fetch file details.
    :param file_pattern: Regex pattern to match the file name.
    :param headers: Optional HTTP headers (e.g., for authentication).
    :return: Extracted file name or None.
    """
    try:
        # Fetch the API or page content
        url = f"{base_url}{api_endpoint}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.text
        
        # Use regex to find the desired file name
        match = re.search(file_pattern, content)
        if not match:
            print("File name not found in the response.")
            return None
        
        return match.group(0)  # Return the matched file name
    except requests.RequestException as e:
        print(f"Error fetching the API content: {e}")
        return None

# Function to download the file
def download_file(base_url, file_name, save_directory, headers=None):
    """
    Download the file from the given URL and save it locally.

    :param base_url: Base URL of the website.
    :param file_name: Name of the file to be downloaded.
    :param save_directory: Local directory to save the downloaded file.
    :param headers: Optional HTTP headers (e.g., for authentication).
    """
    try:
        # Construct the file URL
        file_url = f"{base_url}/{file_name}"
        print(f"Downloading from: {file_url}")
        
        # Send the GET request to download the file
        response = requests.get(file_url, headers=headers, stream=True)
        response.raise_for_status()
        
        # Save the file locally
        os.makedirs(save_directory, exist_ok=True)
        file_path = os.path.join(save_directory, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded successfully: {file_path}")
    except requests.RequestException as e:
        print(f"Error downloading the file: {e}")

# Main script
if __name__ == "__main__":
    # Configuration
    base_url = "https://notpx.app"
    api_endpoint = "/api/v1/"
    file_pattern = r"index-[A-Za-z0-9]+\.js"  # Regex for dynamic file names
    save_directory = "downloads"
    
    # Optional headers (e.g., for API tokens or custom headers)
    headers = {
        "User-Agent": "PythonDownloader/1.0",
        # Add other headers if needed (e.g., 'Authorization': 'Bearer <token>')
    }
    
    # Fetch the dynamic file name
    file_name = get_dynamic_file(base_url, api_endpoint, file_pattern, headers=headers)
    
    # If the file name is found, download the file
    if file_name:
        download_file(base_url, file_name, save_directory, headers=headers)
