from unittest import main
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def normalize_url(url):
    parsed_obj = urlparse(url)
    path = parsed_obj.path.rstrip("/")
    return parsed_obj.netloc + path


def get_h1_from_html(html):
    soup = BeautifulSoup(html)

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
    print(urls)
    return urls


def extract_page_data(html, page_url):
    data = {
        "url": None,
        "h1": None,
        "first_paragraph": None,
        "outgoing_links": [],
        "image_urls": [],
    }

    data["url"] = page_url
    data["h1"] = get_h1_from_html(html)
    data["first_paragraph"] = get_first_paragraph_from_html(html)
    data["outgoing_links"] = get_urls_from_html(html, page_url)
    data["image_urls"] = get_images_from_html(html, page_url)

    return data


#
# get_urls_from_html(
#     """<html>
#   <body>
#     <a href="https://blog.boot.dev">Go to Boot.dev</a>
#     <img src="/logo.png" alt="Boot.dev Logo" />
#     <a href="blog.boot.dev">Go to Boot.dev</a>
#   </body>
#     <img src="/logo.png" alt="Boot.dev Logo" />
#
#     <a href="boot.dev">Go to Boot.dev</a>
# </html>""",
#     "https://blog.boot.dev",
# )

get_images_from_html(
    """<html>
  <body>
    <a href="https://blog.boot.dev">Go to Boot.dev</a>
    <img src="/logo.png" alt="Boot.dev Logo" />
    <a href="blog.boot.dev">Go to Boot.dev</a>
  </body>
    <img src="/logo.png" alt="Boot.dev Logo" />

    <a href="boot.dev">Go to Boot.dev</a>
</html>""",
    "https://blog.boot.dev",
)
#
#
#
# print(normalize_url("book.me/"))
# print(
#     get_first_paragraph_from_html("""<html>
#   <body>
#   <p>Hi</p>
#     <main>
#
#   <p>Inside Hi</p>
#     <h1>hi</h1>
#     </main>
#   </body>
# </html>""")
# )
