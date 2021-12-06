import sqlite3
from db_operations import DBOperations


class DBCM:
    """
    Simple CM for sqlite3 databases. Commits everything at exit.
    """

    def __init__(self, db_name):
        self.name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.name)
        return self.conn

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()


myDb = DBOperations()

with DBCM("temp_data.sqlite") as f:
    cusr = f.cursor()
    print(myDb.fetch_data("2000-11-02", "2001-10-01", cusr))
