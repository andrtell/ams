import sqlite3


def execute(conn: sqlite3.Connection, sql, params=[]):
    cursor = conn.cursor()
    cursor.execute(sql, params)
    return cursor


def executemany(conn: sqlite3.Connection, sql, params=[]):
    cursor = conn.cursor()
    cursor.executemany(sql, params)
    return cursor


class DataTable:
    name = "data"

    @staticmethod
    def drop(conn: sqlite3.Connection):
        q = f"DROP TABLE IF EXISTS {DataTable.name}"
        execute(conn, q)

    @staticmethod
    def create(conn: sqlite3.Connection):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {DataTable.name} (
            id INTEGER NOT NULL, 
            key TEXT NOT NULL, 
            value TEXT NOT NULL,
            PRIMARY KEY(id, key)
        )
        """
        execute(conn, sql)

    @staticmethod
    def insert(conn: sqlite3.Connection, vals_list=[]):
        sql = f"INSERT OR IGNORE INTO {DataTable.name} (id, key, value) VALUES (?, ?, ?)"
        executemany(conn, sql, vals_list)
