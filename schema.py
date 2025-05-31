#! /usr/bin/env python3

from src import ad_model
from src import database


def migrate_up(conn):
    ad_model.create_table(conn)


def migrate_down(conn):
    ad_model.drop_table(conn)


if __name__ == "__main__":
    conn = database.connect()
    migrate_down(conn)
    migrate_up(conn)
    database.close(conn)