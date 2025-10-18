import time
import asyncio
from crawl import crawl_site_async
import sys


async def main():
    print("Hello from webcrawler!")

    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("Too many arguments provided")
        sys.exit(1)

    print("Script name: ", sys.argv[0])
    print("Argument: ", sys.argv[1])

    start_time = time.time()
    print(f"Starting async crawl of: {sys.argv[1]}")

    page_data = await crawl_site_async(sys.argv[1])

    for page in page_data.values():
        print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")

    end_time = time.time()
    print(f"time {end_time - start_time}")

    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
