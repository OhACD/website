from django.core.cache import cache


def _cache_key(prefix: str, identifier: str) -> str:
    return f"rate:{prefix}:{identifier}"


def is_rate_limited(prefix: str, identifier: str, limit: int, window: int) -> bool:
    """
    Returns True when the identifier exceeded the limit within the window (seconds).
    """
    key = _cache_key(prefix, identifier)
    current = cache.get(key, 0)
    if current >= limit:
        return True
    cache.set(key, current + 1, window)
    return False
