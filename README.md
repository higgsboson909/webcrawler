# Web Crawler

This is a simple asynchronous web crawler built with Python. It's designed to efficiently crawl a website, extracting key information from each page.

## Features

*   **Asynchronous Crawling**: Utilizes `asyncio` and `aiohttp` for high-performance, non-blocking network requests.
*   **Data Extraction**: Extracts the following information from each page:
    *   H1 Tag
    *   First Paragraph
    *   All Outgoing Links
    *   All Image URLs
*   **Concurrency Control**: Manages the number of concurrent requests to avoid overloading the server.
*   **URL Normalization**: Normalizes URLs to avoid crawling the same page multiple times.
*   **Unit Tested**: Comes with a suite of unit tests to ensure the core functionality is working correctly.

## Getting Started

### Prerequisites

*   Python 3.7+
*   uv (or pip)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/webcrawler.git
    cd webcrawler
    ```
2.  Install the dependencies:
    ```bash
    uv pip install -r requirements.txt
    ```

## Usage

To crawl a website, run the `main.py` script with the URL of the website as a command-line argument:

```bash
python main.py https://example.com
```

The crawler will then start crawling the website and print the number of outgoing links found on each page.

## Running Tests

To run the unit tests, use the following command:

```bash
python -m unittest test_crawl.py
```
