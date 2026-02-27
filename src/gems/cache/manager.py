"""
缓存管理器
"""

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

from gems.config import config

CACHE_DIR = Path(".cache")


class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        self.cache_dir = CACHE_DIR
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, prefix: str, identifier: str) -> str:
        """生成缓存键"""
        key = f"{prefix}:{identifier}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """获取缓存文件路径"""
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, prefix: str, identifier: str, ttl: int) -> Any:
        """获取缓存数据"""
        if not config.cache_enabled:
            return None
        
        cache_key = self._get_cache_key(prefix, identifier)
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 检查是否过期
            if time.time() - data.get("timestamp", 0) > ttl:
                return None
            
            return data.get("value")
        except Exception:
            return None
    
    def set(self, prefix: str, identifier: str, value: Any):
        """设置缓存数据"""
        if not config.cache_enabled:
            return
        
        cache_key = self._get_cache_key(prefix, identifier)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump({
                    "timestamp": time.time(),
                    "value": value
                }, f, ensure_ascii=False, default=str)
        except Exception:
            pass
    
    def get_analysis_result(self, symbol: str) -> str | None:
        """获取分析结果缓存"""
        return self.get("analysis", symbol, config.cache_ttl_analysis)
    
    def set_analysis_result(self, symbol: str, result: str):
        """设置分析结果缓存"""
        self.set("analysis", symbol, result)
    
    def get_realtime_data(self, symbol: str) -> dict | None:
        """获取实时数据缓存"""
        return self.get("realtime", symbol, config.cache_ttl_realtime)
    
    def set_realtime_data(self, symbol: str, data: dict):
        """设置实时数据缓存"""
        self.set("realtime", symbol, data)
    
    def get_financial_data(self, symbol: str, period: str) -> dict | None:
        """获取财务数据缓存"""
        return self.get("financial", f"{symbol}:{period}", config.cache_ttl_financial)
    
    def set_financial_data(self, symbol: str, period: str, data: dict):
        """设置财务数据缓存"""
        self.set("financial", f"{symbol}:{period}", data)


# 全局缓存实例
cache_manager = CacheManager()
