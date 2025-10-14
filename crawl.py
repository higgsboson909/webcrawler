from urllib.parse import urlparse


def normalize_url(url):
    parsed_obj = urlparse(url)
    # if parsed_obj.path == "":

    return parsed_obj.netloc + parsed_obj.path
