from util.cache import cache
from typing import Callable


def caching(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Callable:
        data = cache.get(args[1])
        if data is not None:
            return func(*args, **kwargs, memory=data)
        return func(*args, **kwargs)
    return wrapper
