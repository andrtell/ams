#! /usr/bin/env python3
import json
import db, jobsearch
from table import ads
from util import past


def up():
    with db.cursor() as c:
        ads.create(c)


def down():
    with db.cursor() as c:
        ads.drop(c)


def fetch():
    with db.cursor() as c:
        for ad in jobsearch.fetch_ads(start=past.day(1)):
            ads.insert(c, id=ad["id"], data=json.dumps(ad))



# def populate():
#     pass
#     # conn = connect("data.db")
#     # with conn:
#     #     SiteTable.populate(conn)
#     #     AdTable.populate(conn)
#     # conn.close()
