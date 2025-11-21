from django.core.cache import cache


def _cache_key(prefix: str, identifier: str) -> str:
    return f"rate:{prefix}:{identifier}"


def is_rate_limited(prefix: str, identifier: str, limit: int, window: int) -> bool:
    """
    Check if the identifier has exceeded the rate limit within the time window.

    Args:
        prefix: A string prefix for the cache key (e.g., "login", "register")
        identifier: Unique identifier (typically email address)
        limit: Maximum number of requests allowed
        window: Time window in seconds

    Returns:
        True if rate limit exceeded, False otherwise
    """
    key = _cache_key(prefix, identifier)
    current = cache.get(key, 0)
    if current >= limit:
        return True
    # Increment counter before returning False
    cache.set(key, current + 1, window)
    return False
