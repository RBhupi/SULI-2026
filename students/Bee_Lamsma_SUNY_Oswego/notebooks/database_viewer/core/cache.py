class QueryCache:

    def __init__(self, max_size=128):
        self.max_size = max_size
        self.cache = {}

    def _key(self, sql, params):
        return (sql, tuple(params or []))

    def get(self, sql, params):
        return self.cache.get(self._key(sql, params))

    def set(self, sql, params, result):
        if len(self.cache) >= self.max_size:
            self.cache.pop(next(iter(self.cache)))

        self.cache[self._key(sql, params)] = result