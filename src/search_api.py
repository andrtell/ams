import requests
import time
from pprint import pprint

from src import query

API_URL = "https://jobsearch.api.jobtechdev.se/search"


def headers():
    return {
        "Accept": "application/json",
        # "X-Fields": "total{value}, hits{id, headline}",
    }


def make_request(q):
    time.sleep(0.6)  # naive rate limit
    pprint(q)
    response = requests.get(API_URL, q, headers=headers())
    response.raise_for_status()
    return response.json()


def make_paginated_request(q):
    q = query.update_query(q, offset=0, limit=100)
    data = make_request(q)
    yield data
    total = data["total"]["value"]
    q = query.next_page(q)
    while q["offset"] < total:
        yield make_request(q)
        q = query.next_page(q)


def fetch(q):
    for response_data in make_paginated_request(q):
        for ad_data in response_data["hits"]:
            yield ad_data