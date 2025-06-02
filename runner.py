#! /usr/bin/env python3
from sqlite3 import connect
from jobsearch import JobSearchClient, JobSearchQuery
from utils import flatten, hours_ago, days_ago
from db import DataTable
from pprint import pprint


def db_up():
    conn = connect("data.db")
    with conn:
        DataTable.create(conn)
    conn.close()


def db_down():
    conn = connect("data.db")
    with conn:
        DataTable.drop(conn)
    conn.close()


def fetch():
    client = JobSearchClient()
    conn = connect("data.db")
    with conn:
        for data in client.get_ads(JobSearchQuery(after=days_ago(1))):
            vals = [(data["id"], *tup) for tup in flatten(data) if tup[1]]
            DataTable.insert(conn, vals)

    conn.close()
