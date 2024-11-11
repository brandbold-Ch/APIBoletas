from cachetools import TTLCache, cached

cache = TTLCache(maxsize=100, ttl=10)
