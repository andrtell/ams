from src import db
from urllib.parse import urlparse

def populate(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    for row in c.fetchall():
        match row[1]:
            case "application_details.url":
                if row[2] != "":
                    print(row[2])
                    uri = urlparse(row[2])
                    base = f"{uri.scheme}://{uri.netloc}/"
                    c.execute("INSERT OR IGNORE INTO site (uri, example) VALUES (?, ?)", (base,row[2]))
    conn.commit()

if __name__ == "__main__":
    conn = db.connect()
    populate(conn)
    db.close(conn)