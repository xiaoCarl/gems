"""
缓存模块
"""

from .base import Cache
from .manager import CacheManager, cache_manager
from .storage import MemoryCache, DiskCache

__all__ = ["Cache", "CacheManager", "MemoryCache", "DiskCache", "cache_manager"]