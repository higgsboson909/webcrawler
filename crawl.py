from urllib.parse import urlparse


def normalize_url(url):
    parsed_obj = urlparse(url)
    path = parsed_obj.path.rstrip("/")
    return parsed_obj.netloc + path


print(normalize_url("book.me/"))
