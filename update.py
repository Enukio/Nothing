def download_js_file_with_progress(url, output_dir):
    """
    Download a JavaScript file from the given URL and save it to the specified directory
    with a progress bar indicating download progress.

    :param url: The URL of the JavaScript file.
    :param output_dir: The directory where the file should be saved.
    """
    try:
        logger.info(f"Starting download: {url}")
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        filename = os.path.basename(url)
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        chunk_size = 1024  # 1 KB chunks
        progress_width = 50  # Width of the progress bar

        print(Fore.GREEN + f"Downloading {filename}... ", end='', flush=True)
        with open(file_path, 'wb') as f:
            if total_size == 0:
                # Handle unknown content-length
                chunks_processed = 0
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        chunks_processed += 1
                        bar = f"[{'#' * (chunks_processed % progress_width):{progress_width}}] Chunks: {chunks_processed}"
                        print(Fore.GREEN + bar, end='\r', flush=True)
                print(Fore.GREEN + f"[{'#' * progress_width}] Download complete!\n", flush=True)
            else:
                # Handle known content-length
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        percent = int((downloaded_size / total_size) * 100)
                        bar = f"[{'#' * (percent * progress_width // 100)}{'.' * (progress_width - (percent * progress_width // 100))}] {percent:3d}%"
                        print(Fore.GREEN + bar, end='\r', flush=True)
                print(Fore.GREEN + f"[{'#' * progress_width}] 100% - Download complete!\n", flush=True)

        logger.info(f"Successfully downloaded and saved: {file_path}")
    except requests.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
