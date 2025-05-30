#! /usr/bin/env python3

import requests
from pprint import pprint
import json
import os
from datetime import datetime, timedelta
import time

API_URL = "https://jobsearch.api.jobtechdev.se/search"

ADS_DB = "db.json"


# JSON


def read_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def write_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


# Database


def new_database():
    return {
        "count": 0,
        "publication_date": None,
        "objects": [],
    }


def insert_objects(db, new_objects):
    db["objects"].extend(new_objects)


def compact_objects(db):
    seen = {}
    for ad in db["objects"]:
        seen[ad["id"]] = ad
    db["objects"] = list(seen.values())


def update_count(db):
    db["count"] = len(db["objects"])


def update_publication_date(db):
    d = max(
        datetime.fromisoformat(ad["publication_date"]) for ad in db["objects"]
    )
    db["publication_date"] = format_datetime(d)


def tidy_database(db):
    compact_objects(db)
    update_count(db)
    update_publication_date(db)


def read_db(path):
    return read_json(path)


def write_db(path, db):
    write_json(path, db)


def ensure_db(path):
    if not os.path.exists(path):
        write_json(path, new_database())
    return read_db(path)


# Time


def now():
    return datetime.now()


def past_hour():
    return now() - timedelta(hours=1)


def past_day():
    return now() - timedelta(days=1)


def past_week():
    return now() - timedelta(weeks=1)


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def date_range(after, before, intv):
    diff = (before - after) / intv
    for i in range(intv):
        yield (after + diff * i)
    yield before


# API


def new_headers():
    return {
        "Accept": "application/json",
        # "X-Fields": "total{value}, hits{id, headline}",
    }


def new_query(q):
    default = {
        "q": "",
        "limit": 100,
        "offset": 0,
    }
    return {**default, **q}


def split_query_by_time(q, before, after, intv):
    ranges = list(date_range(after, before, intv))
    deltas = zip(ranges, ranges[1:])
    for after, before in deltas:
        yield {
            **q,
            "published-after": format_datetime(after),
            "published-before": format_datetime(before),
        }


def request_ads(q):
    time.sleep(0.3)  # naive rate limit
    pprint(q)
    response = requests.get(API_URL, q)
    response.raise_for_status()
    return response.json()


def request_ads_paginated(q):
    q = {**q}
    data = request_ads(q)
    yield data
    total = data["total"]["value"]
    q["offset"] += q["limit"]
    while q["offset"] < total:
        yield request_ads(q)
        q["offset"] += q["limit"]


def request_ads_by_time(q, before, after, intv):
    queries = split_query_by_time(q, before, after, intv)
    for q in queries:
        for data in request_ads_paginated(q):
            yield data


def get_ads(q, before, after, intv):
    return [
        ad
        for data in request_ads_by_time(q, before, after, intv)
        for ad in data["hits"]
    ]


# Main


def main():
    ads = get_ads(new_query({"q": ""}), now(), past_day(), 24)

    db = ensure_db(ADS_DB)

    insert_objects(db, ads)
    tidy_database(db)

    write_db(ADS_DB, db)


if __name__ == "__main__":
    main()
