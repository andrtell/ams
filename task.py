#! /usr/bin/env python3
import json
import db, table, jobsearch
from util import past


def up():
    with db.open() as cursor:
        cursor.execute(table.ads["create"])


def down():
    with db.open() as cursor:
        cursor.execute(table.ads["drop"])


def fetch():
    with db.open() as cursor:
        for data in jobsearch.fetch_ads(start=past.hour(1)):
            cursor.execute(table.ads["insert"], (data["id"], json.dumps(data)))


# def populate():
#     pass
#     # conn = connect("data.db")
#     # with conn:
#     #     SiteTable.populate(conn)
#     #     AdTable.populate(conn)
#     # conn.close()
