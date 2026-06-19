import sqlite3


class DBManager:

    def __init__(self):
        self.conn = None

    def open(self, path: str):
        self.conn = sqlite3.connect(path)

    def cursor(self):
        if not self.conn:
            raise RuntimeError("Database not opened")
        return self.conn.cursor()

    def query(self, sql, params=None):
        cur = self.cursor()
        cur.execute(sql, params or [])
        rows = cur.fetchall()
        headers = [d[0] for d in cur.description] if cur.description else []
        return rows, headers

    def execute(self, sql, params=None):
        cur = self.cursor()
        cur.execute(sql, params or [])
        self.conn.commit()
        return cur.fetchall()

    def get_tables(self):
        rows = self.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        return [r[0] for r in rows]

    def get_columns(self, table: str):
        rows = self.execute(f"PRAGMA table_info('{table}')")
        return [r[1] for r in rows]

    def table_exists(self, table: str):
        rows = self.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            [table]
        )
        return len(rows) > 0