def drop(cursor):
    cursor.execute("DROP TABLE IF EXISTS ads")

def create(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS ads (id INTEGER PRIMARY KEY, data JSON)")

def insert(cursor, id, data):
    cursor.execute("INSERT OR IGNORE INTO ads (id, data) VALUES (?, ?)", (id, data))