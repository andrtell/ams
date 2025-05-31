import json
import database


# Model


def id_from_data(ad_data):
    return ad_data["id"]


def status_from_data(ad_data):
    return "new"


def url_from_data(ad_data):
    url = ad_data.get("application_details", {}).get("url")
    if url:
        return url
    return ad_data.get("webpage_url", "")


def date_from_data(ad_data):
    return ad_data["publication_date"]


def city_from_data(ad_data):
    return ad_data.get("workplace_address", {}).get("municipality", "none")


def region_from_data(ad_data):
    return ad_data.get("workplace_address", {}).get("region", "none")


def from_data(ad_data):
    return {
        "id": id_from_data(ad_data),
        "status": status_from_data(ad_data),
        "date": date_from_data(ad_data),
        "city": city_from_data(ad_data),
        "region": region_from_data(ad_data),
        "url": url_from_data(ad_data),
        "data": ad_data,
    }


# Database


def to_params(ad):
    return {**ad, "data": json.dumps(ad["data"])}


def insert(conn, ad):
    database.execute(
        conn,
        """
        INSERT OR IGNORE INTO ads (
            id, 
            status, 
            date, 
            city, 
            region, 
            url, 
            data
        ) VALUES (:id, :status, :date, :city, :region, :url, :data)
        """,
        to_params(ad),
    )


def create_table(conn):
    database.execute(
        conn,
        """
        CREATE TABLE IF NOT EXISTS ads (
            id TEXT PRIMARY KEY, 
            status TEXT, 
            date TEXT,
            city TEXT,
            region TEXT,
            url TEXT,
            data TEXT
        )
        """,
    )


def drop_table(conn):
    database.execute(
        conn,
        "DROP TABLE IF EXISTS ads",
    )
