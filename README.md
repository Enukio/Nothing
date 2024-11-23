
# JavaScript File Fetcher

This Python script is designed to fetch JavaScript file paths from a specified base URL and save the filenames to a text file. It is particularly useful for analyzing airdrop bot pages on Telegram, as it identifies and extracts JavaScript filenames often used in such contexts. The script includes error handling, retry mechanisms, and color coded logging for enhanced usability.

## Features

- Fetches JavaScript file paths from the `src` attributes of HTML pages.
- Saves unique filenames to an output file.
- Uses retry logic for robust HTTP request handling.
- Provides color coded logging for better readability.

## Requirements

- Python 3.7 or higher
- `requests`
- `colorama`

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Enukio/Update-Index.git
   ```
   ```bash
   cd Update-Index
   ```

2. Install the required dependencies:

   ```bash
   pip install requests colorama
   ```

## Usage

1. Open the `Index.py` file.

2. Locate the following lines:

   ```python
   BASE_URL = "https://example.com"  # Replace with the actual URL to test
   OUTPUT_FILE = "./cgi"  # Save all filenames to this file
   ```

3. Replace `https://example.com` with your desired URL. For example:

   ```python
   BASE_URL = "https://target-airdrop-bot.com"
   ```

4. Run the script:

   ```bash
   python Index.py
   ```

5. The script will fetch JavaScript filenames and save them to the specified output file (default: `./cgi`).

## Example Output

When run with a valid URL containing JavaScript files, the script will find `<script>` tags with `src` attributes like:

```html
<script src="/assets/index-abc123.js"></script>
```

### The resulting list will include:

```
index-abc123.js
```

These filenames are stored in the output file specified by `OUTPUT_FILE`.

## Customization

- To change the base URL dynamically, modify the `BASE_URL` variable in the script.
- To change the output file location, update the `OUTPUT_FILE` variable.

## Logging

The script uses a custom logging format with color coded log levels:

- **INFO**: Cyan
- **WARNING**: Magenta
- **ERROR**: Yellow
- **CRITICAL**: Bright Red

Logs are displayed in the terminal and include the name of the bot for easy identification.

## License

This project is licensed under the [MIT License](LICENSE).
