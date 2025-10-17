from unittest import main
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# used for: do we crawled the page beforehand
def normalize_url(url):
    parsed_obj = urlparse(url)
    path = parsed_obj.path.rstrip("/")
    return parsed_obj.netloc + path


def get_h1_from_html(html):
    soup = BeautifulSoup(html, "html.parser")

    h1_tag = soup.find("h1")
    if h1_tag is not None:
        return h1_tag.get_text()
    else:
        return ""


def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html)
    paragraph_tag = soup.find("p")

    main_tag = soup.find("main")

    if main_tag is not None and main_tag.find("p") is not None:
        paragraph_tag = main_tag.find("p")

    if paragraph_tag is not None:
        return paragraph_tag.get_text()
    else:
        return ""


def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html)
    urls = []
    anchor_tags = soup.findAll("a")
    if anchor_tags is not None:
        for a_tag in anchor_tags:
            anchor_link = a_tag.get("href")
            if anchor_link is not None:
                urls.append(urljoin(base_url, anchor_link))
    return urls


def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html)
    urls = []
    img_tags = soup.findAll("img")
    if img_tags is not None:
        for img_tag in img_tags:
            if img_tag.get("src") is not None:
                urls.append(urljoin(base_url, img_tag.get("src")))
    return urls


def extract_page_data(html, page_url):
    return {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }


def get_html(url):
    try:
        response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except Exception as e:
        raise Exception(f"Network error while fetching {url}: {e}")
    if response.status_code > 399:
        raise Exception(f"Got HTTP error: {response.status_code} {response.reason}")

    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type:
        raise Exception(f"Got HTTP error {content_type}")

    return response.text


def safe_get_html(url):
    try:
        return get_html(url)
    except Exception as e:
        print(f"{e}")
        return None


def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}

    base_url_obj = urlparse(base_url)
    current_url_obj = urlparse(current_url)
    if current_url_obj.netloc != base_url_obj.netloc:
        return page_data

    normalized_url = normalize_url(current_url)

    if normalized_url in page_data:
        return page_data

    print(f"crawling {current_url}")
    html = safe_get_html(current_url)
    if html is None:
        return page_data

    page_info = extract_page_data(html, current_url)
    page_data[normalized_url] = page_info

    next_urls = get_urls_from_html(html, base_url)
    for next_url in next_urls:
        page_data = crawl_page(base_url, next_url, page_data)

    return page_data
