import sqlite3
from pprint import pprint
from utils import site_uri


def connect(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def execute(conn: sqlite3.Connection, sql, params=[]):
    cursor = conn.cursor()
    cursor.execute(sql, params)
    return cursor


def executemany(conn: sqlite3.Connection, sql, params=[]):
    cursor = conn.cursor()
    cursor.executemany(sql, params)
    return cursor


class DataTable:
    table = "data"

    @staticmethod
    def drop(conn: sqlite3.Connection):
        q = f"DROP TABLE IF EXISTS {DataTable.table}"
        execute(conn, q)

    @staticmethod
    def create(conn: sqlite3.Connection):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {DataTable.table} (
            id INTEGER NOT NULL, 
            key TEXT NOT NULL, 
            value TEXT NOT NULL,
            PRIMARY KEY(id, key)
        )
        """
        execute(conn, sql)

    @staticmethod
    def insert(conn: sqlite3.Connection, vals_list=[]):
        sql = (
            f"INSERT OR IGNORE INTO {DataTable.table} (id, key, value) VALUES (?, ?, ?)"
        )
        executemany(conn, sql, vals_list)

    @staticmethod
    def select_all(conn: sqlite3.Connection):
        return execute(conn, f"SELECT * FROM {DataTable.table}").fetchall()


class SiteTable:
    name = "site"

    @staticmethod
    def drop(conn: sqlite3.Connection):
        q = f"DROP TABLE IF EXISTS {SiteTable.name}"
        execute(conn, q)

    @staticmethod
    def create(conn: sqlite3.Connection):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {SiteTable.name} (
            id INTEGER NOT NULL, 
            uri TEXT NOT NULL, 
            example TEXT NOT NULL,
            PRIMARY KEY(id),
            UNIQUE(uri)
        )
        """
        execute(conn, sql)

    @staticmethod
    def insert(conn: sqlite3.Connection, vals_list=[]):
        sql = f"INSERT OR IGNORE INTO {SiteTable.name} (uri, example) VALUES (?, ?)"
        executemany(conn, sql, vals_list)

    @staticmethod
    def populate(conn: sqlite3.Connection):
        sites = []
        for row in DataTable.select_all(conn):
            match row["key"]:
                case "application_details.url":
                    if row["value"]:
                        uri = site_uri(row["value"])
                        sites.append((uri, row["value"]))
        SiteTable.insert(conn, sites)

    @staticmethod
    def select_all(conn: sqlite3.Connection):
        return execute(conn, f"SELECT * FROM {SiteTable.name}").fetchall()


class StepTable:
    name = "step"

    @staticmethod
    def drop(conn: sqlite3.Connection):
        q = f"DROP TABLE IF EXISTS {StepTable.name}"
        execute(conn, q)

    @staticmethod
    def create(conn: sqlite3.Connection):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {StepTable.name} (
            site_id INTEGER NOT NULL, 
            step INTEGER NOT NULL,
            action TEXT NOT NULL,
            selector TEXT NOT NULL,
            value TEXT NOT NULL,
            PRIMARY KEY(site_id, step),
            FOREIGN KEY(site_id) REFERENCES site(id)
        )
        """
        execute(conn, sql)

    @staticmethod
    def insert(conn: sqlite3.Connection, vals_list=[]):
        sql = f"INSERT OR IGNORE INTO {StepTable.name} (site_id, step, selector, action, value) VALUES (?, ?, ?, ?, ?)"
        executemany(conn, sql, vals_list)


class AdTable:
    name = "ad"

    @staticmethod
    def drop(conn: sqlite3.Connection):
        q = f"DROP TABLE IF EXISTS {AdTable.name}"
        execute(conn, q)

    @staticmethod
    def create(conn: sqlite3.Connection):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {AdTable.name} (
            id INTEGER NOT NULL,
            site_id INTEGER,
            title TEXT,
            uri TEXT,
            city TEXT,
            region TEXT,
            description TEXT,
            PRIMARY KEY(id),
            FOREIGN KEY(site_id) REFERENCES site(id)
        )
        """
        execute(conn, sql)

    @staticmethod
    def insert(conn: sqlite3.Connection, vals_list=[]):
        sql = f"""
        INSERT OR IGNORE INTO {AdTable.name} 
        (id, site_id, title, uri, city, region, description) 
        VALUES (:id, :site_id, :title, :uri, :city, :region, :description)
        """
        executemany(conn, sql, vals_list)

    @staticmethod
    def populate(conn: sqlite3.Connection):
        ads = {}

        datums = [d for d in DataTable.select_all(conn) if d["value"]]

        for d in datums:
            if d["id"] not in ads:
                ads[d["id"]] = {
                    "id": d["id"],
                    "site_id": None,
                    "uri": None,
                    "title": None,
                    "description": None,
                    "city": None,
                    "region": None,
                }

        for d in datums:
            id = d["id"]
            val = d["value"]
            match d["key"]:
                case "application_details.url":
                    ads[id]["uri"] = val
                case "webpage_url":
                    if not ads[id].get("uri", None):
                        ads[id]["uri"] = val
                case "headline":
                    ads[id]["title"] = val
                case "description.text":
                    ads[id]["description"] = val
                case "workplace_address.municipality":
                    ads[id]["city"] = val
                case "workplace_address.region":
                    ads[id]["region"] = val

        sites = SiteTable.select_all(conn)

        for k in ads.keys():
            for site in sites:
                if ads[k]["uri"] and ads[k]["uri"].startswith(site["uri"]):
                    ads[k]["site_id"] = site["id"]

        AdTable.insert(conn, list(ads.values()))
