ads = dict(
    drop="DROP TABLE IF EXISTS ads",
    create="CREATE TABLE IF NOT EXISTS ads (id INTEGER PRIMARY KEY, data JSON)",
    insert="INSERT INTO ads (id, data) VALUES (?, ?)",
    select="SELECT * FROM ads",
)