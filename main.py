from crawl import get_html
from crawl import crawl_page
import sys


def main():
    print("Hello from webcrawler!")

    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("Too many arguments provided")
        sys.exit(1)

    print("Script name: ", sys.argv[0])
    print("Argument: ", sys.argv[1])

    # print(get_html(sys.argv[1]))

    page_data = crawl_page(sys.argv[1])
    # for data in page_data:
    # print(f"- {data.get('url')}: {data['outgoing_links']} links")
    # print(data)
    print(f"Found {len(page_data)} pages:")
    for page in page_data.values():
        print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links")
    sys.exit(0)


if __name__ == "__main__":
    main()
