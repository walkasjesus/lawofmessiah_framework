import json
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

from bible_lib.simple_cache import SimpleCache


class TestSimpleCache(TestCase):
    cache_path = Path('cache.json')

    def tearDown(self):
        # Clean up file
        if self.cache_path.exists():
            self.cache_path.unlink()

    def test_get(self):
        cache = SimpleCache()
        method = Mock(return_value='my_value')

        for i in range(5):
            cached_value = cache.get(method, 'arg')

        self.assertEqual(cached_value, 'my_value')
        self.assertEqual(method.call_count, 1)

    def test_get_with_lambda_notation(self):
        cache = SimpleCache()
        cached_value = cache.get(lambda f: f * f, 5)
        self.assertEqual(cached_value, 25)

    def test_load_and_store(self):
        cache = SimpleCache(self.cache_path)
        cache.get(lambda f: f, 'test')
        cache.get(lambda f: f, 'another_value')
        cache.get(lambda f: f*f, 5)

        cache_before_load = cache._cache
        cache.store_state()

        # Make a new cache to really test restore mechanism
        cache = SimpleCache(self.cache_path)
        cache.load_state()
        cache_after_load = cache._cache

        self.assertEqual(cache_before_load, cache_after_load)

    def test_get_persists_to_disk_immediately(self):
        cache = SimpleCache(self.cache_path)
        if self.cache_path.exists():
            self.cache_path.unlink()

        cache.get(lambda value: {'result': value}, 'persisted-value')

        self.assertTrue(self.cache_path.exists())
        with self.cache_path.open() as file:
            saved = json.load(file)

        self.assertIn('persisted-value', saved)

    def test_get_ignores_permission_errors_when_storing_to_disk(self):
        cache = SimpleCache(self.cache_path)

        with patch.object(Path, 'open', side_effect=PermissionError('permission denied')):
            cached_value = cache.get(lambda value: value, 'permission-test')

        self.assertEqual(cached_value, 'permission-test')
        self.assertEqual(cache.get_value('permission-test'), None)
