from asyncio import Lock, all_tasks
import asyncio
import aiohttp
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


def safe_get_html(url):
    try:
        return get_html(url)
    except Exception as e:
        print(f"{e}")
        return None


class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.max_pages = max_pages
        self.should_stop = False
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None

        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop is True:
                return False

            if normalized_url in self.page_data:
                return False
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached Maximux page limit")
                for task in self.all_tasks:
                    if not task.done():
                        task.cancel()
                return False
            else:
                return True

    async def get_html(self, url):
        try:
            async with self.session.get(
                url, headers={"User-Agent": "BootCrawler/1.0"}
            ) as response:
                if response.status > 399:
                    print(f"Got HTTP error: {response.status} {response.reason}")

                    return None
                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    print(f"Got HTTP error {content_type}")
                    return None

                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            print(f"Error {e}")
            return None

    async def crawl_page(self, current_url):
        if self.should_stop is True:
            return
        current_url_obj = urlparse(current_url)
        if current_url_obj.netloc != self.base_domain:
            return

        normalized_url = normalize_url(current_url)

        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return

        async with self.semaphore:
            print(
                f"crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})"
            )
            html = await self.get_html(current_url)
            if html is None:
                return

            page_info = extract_page_data(html, current_url)

            async with self.lock:
                self.page_data[normalized_url] = page_info

        if self.should_stop:
            return
        next_urls = get_urls_from_html(html, self.base_url)

        tasks = []
        for next_url in next_urls:
            task = asyncio.create_task(self.crawl_page(next_url))
            tasks.append(task)
            self.all_tasks.add(task)
        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for task in tasks:
                    self.all_tasks.discard(task)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(base_url, max_concurrency=3, max_pages=20):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()
