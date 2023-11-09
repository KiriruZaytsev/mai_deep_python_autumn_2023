from lru_cache import LRUCache
from unittest import TestCase

class test_LRU_cache(TestCase):

    cache = LRUCache(limit = 2)

    def test_set(self):
        self.cache.set('k1', 'val1')
        self.cache.set('k2', 'val2')
        self.assertEqual(self.cache.get('k1'), 'val1')
        self.assertEqual(self.cache.get('k2'), 'val2')
        
    def test_overflowed_cache(self):
        self.cache.set('k1', 'val1')
        self.cache.set('k2', 'val2')
        self.cache.set('k3', 'val3')
        self.assertIsNone(self.cache.get('key1'))
        self.assertEqual(self.cache.get('k2'), 'val2')
        self.assertEqual(self.cache.get('k3'), 'val3')

    def test_overflowed_and_rewrited(self):
        self.cache.set('k1', 'val1')
        self.cache.set('k2', 'val2')
        self.cache.set('k1', 'val4')
        self.cache.set('k3', 'val3')
        self.assertIsNone(self.cache.get('key2'))
        self.assertEqual(self.cache.get('k1'), 'val4')
        self.assertEqual(self.cache.get('k3'), 'val3')

    def test_overflowed_after_get(self):
        self.cache.set('k1', 'val1')
        self.cache.set('k2', 'val2')
        self.assertEqual(self.cache.get('k1'), 'val1')
        self.cache.set('k3', 'val3')
        self.assertIsNone(self.cache.get('key2'))
        self.assertEqual(self.cache.get('k1'), 'val1')
        self.assertEqual(self.cache.get('k3'), 'val3')
