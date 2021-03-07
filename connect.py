import sqlite3

class db:
    def __init__(self, db):
        self.con = sqlite3.connect(db)

    def query(self, sql):
        self.cur = self.con.cursor()
        self.cur.execute(sql)
        self.con.commit()
        return self.cur

    def __del__(self):
        self.con.close()