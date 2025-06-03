from datetime import datetime, timedelta
from dataclasses import dataclass, replace
import time
import requests

from util import period, paginate


URL = "https://jobsearch.api.jobtechdev.se/search"


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def query(offset: int, limit: int, start: datetime, end: datetime = None):
    params = {
        "offset": offset,
        "limit": limit,
        "published-after": format_datetime(start),
    }
    if end:
        params["published-before"] = format_datetime(end)
    return params


def do_request(**kwargs):
    time.sleep(0.3)  # naive rate limit
    resp = requests.get(URL, query(**kwargs))
    resp.raise_for_status()
    return resp.json()


def page_request(offset=0, limit=100, **kwargs):
    while True:
        data = do_request(offset=offset, limit=limit, **kwargs)
        yield data
        offset = paginate.next_offset(
            offset, limit, data.get("total", {}).get("value", 0)
        )
        if not offset:
            break


def fetch_ads(start: datetime):
    for start, end in period.split_by_hour(start, datetime.now()):
        for data in page_request(start=start, end=end):
            for ad in data["hits"]:
                yield ad
