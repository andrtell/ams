import sqlite3
import json

DB_FILE = "ads.db"


def connect():
    return sqlite3.connect(DB_FILE)


def close(conn):
    conn.close()


def execute(conn, sql, params={}):
    c = conn.cursor()
    c.execute(sql, params)
    conn.commit()