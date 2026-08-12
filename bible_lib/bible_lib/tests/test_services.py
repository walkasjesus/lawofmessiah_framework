from pathlib import Path
from unittest import TestCase

from bible_lib.bible_api.services import Services


class TestServices(TestCase):
    def test_single_cache(self):
        """" Because we do not want every new client to begin its own cache
        and disrupt other caches, the services to let every one who wants
        to share a client."""
        cache_1 = Services().cache
        cache_2 = Services().cache

        cache_1.temp_var = 1
        cache_2.temp_var = 2

        self.assertEqual(cache_1.temp_var, cache_2.temp_var)

    def test_cache_path_is_stable_and_absolute(self):
        cache_path = Services().cache.cache_path

        self.assertTrue(cache_path.is_absolute())
        self.assertIn('lawofmessiah_website', str(cache_path))
        self.assertTrue(Path(cache_path).parent.exists())

    def test_default_cache_ttl_is_30_days(self):
        self.assertEqual(Services().cache.ttl_seconds, 60 * 60 * 24 * 30)
