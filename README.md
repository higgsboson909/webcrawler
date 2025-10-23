# Web Crawler
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

## Project Architecture

The project is structured into three main Python files: `main.py`, `crawl.py`, and `csv_report.py`.

### `main.py`

This is the entry point of the application.

-   **`main()`**:
    -   Parses command-line arguments: `base_url`, `max_concurrency`, and `max_pages`.
    -   Calls `crawl_site_async` from `crawl.py` to start the crawling process.
    -   Calls `write_csv_report` from `csv_report.py` to save the results.

### `crawl.py`

This file contains the core crawling logic.

-   **`normalize_url(url)`**: Normalizes a URL to avoid crawling the same page multiple times.
-   **`get_h1_from_html(html)`**: Extracts the H1 tag from a given HTML content.
-   **`get_first_paragraph_from_html(html)`**: Extracts the first paragraph from a given HTML content.
-   **`get_urls_from_html(html, base_url)`**: Extracts all the links from a given HTML content.
-   **`get_images_from_html(html, base_url)`**: Extracts all the image sources from a given HTML content.
-   **`extract_page_data(html, page_url)`**: Gathers all the data for a single page using the helper functions above.
-   **`AsyncCrawler` class**: The main class for the asynchronous crawler.
    -   **`crawl_page(current_url)`**: The core recursive crawling logic for a single page.
    -   **`crawl()`**: The entry point for the `AsyncCrawler` instance.
-   **`crawl_site_async(base_url, max_concurrency, max_pages)`**: A function that instantiates and runs the `AsyncCrawler`.

### `csv_report.py`

This file is responsible for generating the CSV report.

-   **`write_csv_report(page_data, filename)`**: Takes the crawled data and writes it to a CSV file.

## Running Tests

To run the unit tests, use the following command:

```bash
python -m unittest test_crawl.py
```