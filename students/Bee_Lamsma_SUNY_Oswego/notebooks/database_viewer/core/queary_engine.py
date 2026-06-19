from filters import build_where


class QueryEngine:

    def __init__(self, db):
        self.db = db

    # ---------------- BASIC QUERY ----------------

    def select(self, table, columns="*", where=None, params=None, limit=None):

        sql = f'SELECT {columns} FROM "{table}"'

        if where:
            sql += f" {where}"

        if limit:
            sql += f" LIMIT {limit}"

        return self.db.query(sql, params)

    # ---------------- FILTER QUERY ----------------

    def filtered(self, table, filters=None, limit=500):

        where, params = build_where(filters or [])

        sql = f'SELECT * FROM "{table}" {where} LIMIT {limit}'

        return self.db.query(sql, params)

    # ---------------- JOIN QUERY ----------------

    def join(self, tables, on_clause, columns="*", where=None, params=None):

        sql = f"SELECT {columns} FROM {tables[0]}"

        for t in tables[1:]:
            sql += f" JOIN {t} ON {on_clause}"

        if where:
            sql += f" {where}"

        return self.db.query(sql, params)

    # ---------------- COUNT ----------------

    def count(self, table, where=None, params=None):

        sql = f'SELECT COUNT(*) FROM "{table}"'

        if where:
            sql += f" {where}"

        rows, _ = self.db.query(sql, params)
        return rows[0][0]