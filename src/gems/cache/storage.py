"""
缓存存储实现
"""

import json
import os
from collections import OrderedDict
from typing import Any

from gems.cache.base import Cache, CacheEntry


class MemoryCache(Cache):
    """内存缓存实现"""

    def __init__(self, max_size: int = 1000):
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.max_size = max_size

    def get(self, key: str) -> Any | None:
        """获取缓存值"""
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if entry.is_expired():
            self.delete(key)
            return None

        # 移动到最近使用位置
        self._cache.move_to_end(key)
        return entry.value

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """设置缓存值"""
        # 如果达到最大大小，移除最旧的条目
        if len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)

        self._cache[key] = CacheEntry(value, ttl)
        # 移动到最近使用位置
        self._cache.move_to_end(key)

    def delete(self, key: str) -> None:
        """删除缓存值"""
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()

    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        if key not in self._cache:
            return False

        entry = self._cache[key]
        if entry.is_expired():
            self.delete(key)
            return False

        return True


class DiskCache(Cache):
    """磁盘缓存实现"""

    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_file_path(self, key: str) -> str:
        """获取缓存文件路径"""
        # 使用哈希避免文件名冲突
        import hashlib

        key_hash = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{key_hash}.json")

    def get(self, key: str) -> Any | None:
        """获取缓存值"""
        file_path = self._get_file_path(key)

        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            entry = CacheEntry(data["value"], data.get("ttl"))

            if entry.is_expired():
                self.delete(key)
                return None

            return entry.value
        except (OSError, json.JSONDecodeError, KeyError):
            # 文件损坏时删除
            self.delete(key)
            return None

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """设置缓存值"""
        file_path = self._get_file_path(key)

        try:
            entry = CacheEntry(value, ttl)
            data = {
                "value": value,
                "ttl": ttl,
                "created_at": entry.created_at.isoformat(),
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            # 写入失败，忽略
            pass

    def delete(self, key: str) -> None:
        """删除缓存值"""
        file_path = self._get_file_path(key)

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                # 删除失败，忽略
                pass

    def clear(self) -> None:
        """清空缓存"""
        for filename in os.listdir(self.cache_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.cache_dir, filename)
                try:
                    os.remove(file_path)
                except OSError:
                    # 删除失败，忽略
                    pass

    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        file_path = self._get_file_path(key)

        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            entry = CacheEntry(data["value"], data.get("ttl"))

            if entry.is_expired():
                self.delete(key)
                return False

            return True
        except (OSError, json.JSONDecodeError, KeyError):
            self.delete(key)
            return False
