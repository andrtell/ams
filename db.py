from sqlite3 import connect
from contextlib import contextmanager

DB = "data.db"

@contextmanager
def cursor():
    conn = connect(DB)
    try:
        cur = conn.cursor()
        yield cur
    except Exception as e:
        conn.rollback()
        raise e
    else:
        conn.commit()
    finally:
        conn.close()