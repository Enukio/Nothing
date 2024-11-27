
# JavaScript Filename Extractor

This project provides a Python script for extracting and saving filenames of JavaScript files (`index.js`) from a given webpage. It leverages the `requests` library for making HTTP requests and `loguru` for enhanced logging.

---

## Features

- **URL Validation**: Ensures the provided base URL is valid.
- **Retry Mechanism**: Automatically retries failed HTTP requests.
- **JavaScript Filename Extraction**: Uses regular expressions to locate JavaScript files in the HTML source of a webpage.
- **Storage Support**: Saves extracted filenames to a specified file.
- **Customizable Base URL and Output File**: The script allows configuring the base URL and output file path.

## Prerequisites

Ensure the following Python packages are installed:

- `requests`
- `loguru`

Install them via pip:

```bash
pip install requests loguru
```

## Usage

1. Clone this repository:

```bash
git clone https://github.com/Enukio/Update-Index.git
```
```bash
cd Update-Index
```

2. Edit the script to set the correct `BASE_URL` and `OUTPUT_FILE` in the `Index.py` file:

```python
BASE_URL = "https://example.com"  # Replace with your target URL
OUTPUT_FILE = "./cgi"  # File where filenames will be saved
```

3. Run the script:

```bash
python Index.py
```

4. Output files will be saved to the specified `OUTPUT_FILE` path.

---

## Example Output

When run with a valid URL containing JavaScript files, the script will find `<script>` tags with `src` attributes like:

```html
<script src="/assets/index-abc123.js"></script>
```

### The resulting list will include:

```
index-abc123.js
```

---

## Logging

The script outputs detailed logs with colored formatting, including:

- The number of JavaScript files found.
- Success or error messages for file-saving operations.
- Issues with fetching the webpage or unexpected content types.

## Limitations

- Assumes JavaScript filenames match the pattern `/index*.js`.
- Designed for basic extraction and may require adjustments for complex or dynamically loaded webpages.

## License

This project is licensed under the [MIT License](LICENSE).
