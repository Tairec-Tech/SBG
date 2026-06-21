"""
Simple in-memory TTL (Time-To-Live) cache for database queries.
"""
from time import time

class QueryCache:
    def __init__(self, ttl_seconds=300):
        self._cache = {}
        self.ttl_seconds = ttl_seconds

    def get(self, key):
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time() - timestamp < self.ttl_seconds:
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key, value):
        self._cache[key] = (value, time())

    def clear(self):
        self._cache.clear()

# Global instances
kpi_cache = QueryCache(ttl_seconds=300) # 5 minutes TTL
