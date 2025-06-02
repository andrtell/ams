from datetime import datetime, timedelta
from dataclasses import dataclass, replace
import time
import requests


API_URL = "https://jobsearch.api.jobtechdev.se/search"


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


@dataclass
class JobSearchQuery:
    offset: int = 0
    limit: int = 100
    after: datetime = datetime.now() - timedelta(hours=1)
    before: datetime = None

    def next_page(self, total):
        next_offset = self.offset + self.limit
        return replace(self, offset=next_offset) if next_offset < total else None

    def split_by_hour(self):
        before = self.before or datetime.now()
        delta = before - self.after
        hours = (delta.days * 24) + (delta.seconds // 3600)
        timestamps = [self.after + timedelta(hours=hour) for hour in range(hours)]
        timestamps.append(before)
        intervals = zip(timestamps, timestamps[1:])
        return [replace(self, after=start, before=end) for start, end in intervals]

    def to_params(self) -> dict:
        params = {
            "offset": self.offset,
            "limit": self.limit,
            "published-after": format_datetime(self.after),
        }
        if self.before:
            params["published-before"] = format_datetime(self.before)
        return params


@dataclass
class JobSearchClient:
    url: str = API_URL

    def fetch(self, q):
        time.sleep(0.3) # naive rate limit
        resp = requests.get(self.url, q.to_params())
        resp.raise_for_status()
        return resp.json()

    def paginate(self, q):
        while True:
            data = self.fetch(q)
            yield data
            q = q.next_page(data["total"]["value"])
            if not q:
                break

    def get_ads(self, q: JobSearchQuery):
        for q in q.split_by_hour():
            for data in self.paginate(q):
                for job_ad in data["hits"]:
                    yield job_ad
