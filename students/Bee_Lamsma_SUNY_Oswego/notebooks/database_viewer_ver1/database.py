import sqlite3


class DatabaseManager:

    def __init__(self):
        self.conn = None
        self.path = None

    def open(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)

    def query(self, sql, params=None):
        cur = self.conn.cursor()
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        rows = cur.fetchall()
        headers = [d[0] for d in cur.description]
        return rows, headers

    def execute(self, sql, params=None):
        cur = self.conn.cursor()
        cur.execute(sql, params or [])
        return cur.fetchall()

    def scalar(self, sql, params=None):
        rows = self.execute(sql, params)
    
        if rows:
            return rows[0][0]
    
        return None
    
    def get_tables(self):
        rows = self.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [r[0] for r in rows]

    def get_columns(self, table):
        rows = self.execute(f"PRAGMA table_info('{table}')")
        return [r[1] for r in rows]

    def count_rows(self, table):
        return self.execute(f"SELECT COUNT(*) FROM '{table}'")[0][0]

    def query_dataframe(self, sql, params=None):
        cur = self.conn.cursor()
        cur.execute(sql, params or [])
    
        rows = cur.fetchall()
        headers = [d[0] for d in cur.description]
    
        return headers, rows
