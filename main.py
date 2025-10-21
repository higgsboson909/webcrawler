import time
import asyncio
from crawl import crawl_site_async
import sys
from csv_report import write_csv_report


async def main():
    print("Hello from webcrawler!")

    if len(sys.argv) < 4:
        print("usage python main.py <base_url> <max_concurrency> <max_pages>")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("Too many arguments provided")
        sys.exit(1)

    print("Script name: ", sys.argv[0])
    print("Argument: ", sys.argv[1])

    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])
    print("Max Concurrency: ", max_concurrency)
    print("Max Pages: ", max_pages)

    start_time = time.time()
    print(f"Starting async crawl of: {sys.argv[1]}")

    page_data = await crawl_site_async(sys.argv[1], max_concurrency, max_pages)

    for page in page_data.values():
        print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")

    end_time = time.time()

    print(f"time {end_time - start_time}")

    write_csv_report(page_data)
    print("Genereated a csv report")

    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
