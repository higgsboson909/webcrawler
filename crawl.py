from unittest import main
from bs4 import BeautifulSoup
from urllib.parse import urlparse


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

    print(soup.findAll("a"))
    print(soup.findAll("img"))


get_urls_from_html(
    """<html>
  <body>
    <a href="https://blog.boot.dev">Go to Boot.dev</a>
    <img src="/logo.png" alt="Boot.dev Logo" />
  </body>
</html>""",
    "https://blog.boot.dev",
)
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
