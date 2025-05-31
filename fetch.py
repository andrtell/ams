#! /usr/bin/env python3

from src import ad_model
from src import database
from src import query
from src import search_api


def main():
    conn = database.connect()

    for q in query.past_hours(hours=24, search=""):
        for ad_data in search_api.fetch(q):
            ad_model.insert(conn, ad_model.from_data(ad_data))

    database.close(conn)

if __name__ == "__main__":
    main()
