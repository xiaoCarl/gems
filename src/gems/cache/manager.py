"""
缓存管理器
"""

from typing import Any

from .storage import DiskCache, MemoryCache


class CacheManager:
    """缓存管理器"""

    def __init__(self):
        # 延迟初始化配置
        self._config = None
        self.enabled = False
        self.memory_cache = None
        self.disk_cache = None
        self.cache_ttl = {}
        self._initialized = False

    def _ensure_initialized(self):
        """确保缓存管理器已初始化"""
        if not self._initialized:
            from gems.config import get_config

            self._config = get_config()
            self.enabled = self._config.cache_enabled
            self.memory_cache = MemoryCache(max_size=self._config.cache_max_size)
            self.disk_cache = DiskCache()

            # 缓存策略配置
            self.cache_ttl = {
                "realtime": self._config.cache_ttl_realtime,
                "financial": self._config.cache_ttl_financial,
                "historical": self._config.cache_ttl_historical,
                "analysis": self._config.cache_ttl_analysis,
            }
            self._initialized = True

    def _generate_key(
        self, data_type: str, symbol: str, period: str | None = None, **kwargs: Any
    ) -> str:
        """生成缓存键"""
        key_parts = [data_type, symbol]

        if period:
            key_parts.append(period)

        # 添加额外参数
        if kwargs:
            param_str = "&".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
            key_parts.append(param_str)

        return ":".join(key_parts)

    def get(
        self, data_type: str, symbol: str, period: str | None = None, **kwargs: Any
    ) -> Any | None:
        """获取缓存数据"""
        self._ensure_initialized()
        if not self.enabled:
            return None

        key = self._generate_key(data_type, symbol, period, **kwargs)

        # 优先从内存缓存获取
        cached_data = self.memory_cache.get(key)
        if cached_data is not None:
            return cached_data

        # 内存缓存未命中，尝试磁盘缓存
        cached_data = self.disk_cache.get(key)
        if cached_data is not None:
            # 将磁盘缓存数据加载到内存缓存
            ttl = self.cache_ttl.get(data_type)
            self.memory_cache.set(key, cached_data, ttl)
            return cached_data

        return None

    def set(
        self,
        data_type: str,
        symbol: str,
        value: Any,
        period: str | None = None,
        **kwargs: Any,
    ) -> None:
        """设置缓存数据"""
        self._ensure_initialized()
        if not self.enabled:
            return

        key = self._generate_key(data_type, symbol, period, **kwargs)
        ttl = self.cache_ttl.get(data_type)

        # 同时设置内存缓存和磁盘缓存
        self.memory_cache.set(key, value, ttl)
        self.disk_cache.set(key, value, ttl)

    def delete(
        self, data_type: str, symbol: str, period: str | None = None, **kwargs: Any
    ) -> None:
        """删除缓存数据"""
        self._ensure_initialized()
        if not self.enabled:
            return

        key = self._generate_key(data_type, symbol, period, **kwargs)

        self.memory_cache.delete(key)
        self.disk_cache.delete(key)

    def clear(self) -> None:
        """清空所有缓存"""
        self._ensure_initialized()
        if not self.enabled:
            return

        self.memory_cache.clear()
        self.disk_cache.clear()

    def get_realtime_data(self, symbol: str) -> Any | None:
        """获取实时数据缓存"""
        return self.get("realtime", symbol)

    def set_realtime_data(self, symbol: str, value: Any) -> None:
        """设置实时数据缓存"""
        self.set("realtime", symbol, value)

    def get_financial_data(self, symbol: str, period: str) -> Any | None:
        """获取财务数据缓存"""
        return self.get("financial", symbol, period)

    def set_financial_data(self, symbol: str, period: str, value: Any) -> None:
        """设置财务数据缓存"""
        self.set("financial", symbol, value, period)

    def get_historical_data(self, symbol: str, period: str) -> Any | None:
        """获取历史数据缓存"""
        return self.get("historical", symbol, period)

    def set_historical_data(self, symbol: str, period: str, value: Any) -> None:
        """设置历史数据缓存"""
        self.set("historical", symbol, value, period)

    def get_analysis_result(self, symbol: str) -> str | None:
        """获取分析结果缓存"""
        self._ensure_initialized()
        if not self.enabled:
            return None

        return self.get("analysis", symbol)

    def set_analysis_result(self, symbol: str, result: str) -> None:
        """设置分析结果缓存"""
        if not self.enabled:
            return

        self.set("analysis", symbol, result)


# 全局缓存管理器实例
cache_manager = CacheManager()
