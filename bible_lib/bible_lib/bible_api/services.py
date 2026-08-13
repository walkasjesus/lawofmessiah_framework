import os
from pathlib import Path

from bible_lib.simple_cache import SimpleCache


def _project_cache_path() -> Path:
    root = Path(__file__).resolve().parents[3]
    cache_dir = root / 'lawofmessiah_website'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / 'bible_api_cache.json'


def _cache_ttl_seconds() -> int:
    try:
        from django.conf import settings

        value = getattr(settings, 'BIBLE_API_CACHE_TIMEOUT_SECONDS', None)
        if value is not None:
            return int(value)
    except Exception:
        pass

    return int(os.getenv('BIBLE_API_CACHE_TTL_SECONDS', os.getenv('BIBLE_API_CACHE_TIMEOUT_SECONDS', 60 * 60 * 24 * 30)))


class Services:
    cache = SimpleCache(_project_cache_path(), ttl_seconds=_cache_ttl_seconds())
