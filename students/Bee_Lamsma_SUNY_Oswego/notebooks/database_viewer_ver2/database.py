import sqlite3


class DatabaseManager:

    def __init__(self):
        self.conn = None
        self.path = None

    def open(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
    #
    # Internal helper
    #

    def cursor(self):
        if self.conn is None:
            raise RuntimeError(
                "Database not opened"
            )

        return self.conn.cursor()

    #
    # Generic queries
    #

    def execute(
        self,
        sql,
        params=None
    ):
        cur = self.cursor()

        cur.execute(
            sql,
            params or []
        )

        return cur.fetchall()

    def query(
        self,
        sql,
        params=None
    ):
        cur = self.cursor()

        cur.execute(
            sql,
            params or []
        )

        rows = cur.fetchall()

        headers = [
            d[0]
            for d in cur.description
        ] if cur.description else []

        return rows, headers

    def scalar(
        self,
        sql,
        params=None
    ):
        cur = self.cursor()

        cur.execute(
            sql,
            params or []
        )

        row = cur.fetchone()

        return row[0] if row else None

    #
    # Schema helpers
    #

    def get_tables(self):

        rows = self.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
            """
        )

        return [r[0] for r in rows]

    def get_columns(
        self,
        table_name
    ):
        rows = self.execute(
            f'PRAGMA table_info("{table_name}")'
        )

        return [r[1] for r in rows]

    def table_exists(
        self,
        table_name
    ):
        return bool(
            self.scalar(
                """
                SELECT COUNT(*)
                FROM sqlite_master
                WHERE type='table'
                AND name=?
                """,
                [table_name]
            )
        )

    #
    # Convenience helpers
    #

    def count(
        self,
        table_name
    ):
        return self.scalar(
            f'SELECT COUNT(*) FROM "{table_name}"'
        )

    def max(
        self,
        table_name,
        column
    ):
        return self.scalar(
            f'''
            SELECT MAX("{column}")
            FROM "{table_name}"
            '''
        )

    def avg(
        self,
        table_name,
        column
    ):
        return self.scalar(
            f'''
            SELECT AVG("{column}")
            FROM "{table_name}"
            '''
        )

    def close(self):

        if self.conn:
            self.conn.close()
            self.conn = None