from urllib.parse import urlparse


def site_uri(uri):
    uri = urlparse(uri)
    return f"{uri.scheme}://{uri.netloc}/"