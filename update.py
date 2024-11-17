from tqdm import tqdm

def download_js_file(url, output_dir):
    """
    Download a JavaScript file from the given URL and save it to the specified directory,
    with a simple progress bar (no speed or ETA).
    
    :param url: The URL of the JavaScript file.
    :param output_dir: The directory where the file should be saved.
    """
    try:
        logger.info(f"Attempting to download file from: {url}")
        
        # Send HTTP request with stream=True for large file support
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        # Get filename and prepare output directory
        filename = os.path.basename(url)
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        
        # Total file size for progress bar
        total_size = int(response.headers.get('content-length', 0))
        
        # Write the file with a simple progress bar
        with open(file_path, 'wb') as f, tqdm(
            total=total_size, unit='B', unit_scale=True, desc=filename, 
            bar_format="{desc}: |{bar}| {percentage:3.0f}%", ncols=80
        ) as pbar:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
                pbar.update(len(chunk))
        
        logger.info(f"Successfully downloaded and saved: {file_path}")
    except requests.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
