"""
配置管理模块
"""

import os


class Config:
    """统一配置类"""

    def __init__(self):
        # LLM API配置
        self.deepseek_api_key: str = self._get_env("DEEPSEEK_API_KEY")
        self.use_qwen: bool = self._get_env_bool("USE_QWEN", default=False)
        self.dashscope_api_key: str | None = self._get_env("DASHSCOPE_API_KEY")
        
        # 数据源配置
        self.preferred_data_source: str = self._get_env("PREFERRED_DATA_SOURCE", "akshare")
        self.request_timeout: int = self._get_env_int("REQUEST_TIMEOUT", 30)
        self.max_retries: int = self._get_env_int("MAX_RETRIES", 3)
        
        # 日志配置
        self.log_level: str = self._get_env("LOG_LEVEL", "info")
        
        # 缓存配置
        self.cache_enabled: bool = self._get_env_bool("CACHE_ENABLED", True)
        self.cache_ttl_realtime: int = self._get_env_int("CACHE_TTL_REALTIME", 300)
        self.cache_ttl_financial: int = self._get_env_int("CACHE_TTL_FINANCIAL", 3600)
        self.cache_ttl_analysis: int = self._get_env_int("CACHE_TTL_ANALYSIS", 86400)
        
        # 验证配置
        self._validate_config()
    
    def _get_env(self, key: str, default: str | None = None) -> str | None:
        """获取环境变量"""
        return os.getenv(key, default)
    
    def _get_env_int(self, key: str, default: int) -> int:
        """获取整数环境变量"""
        value = os.getenv(key)
        return int(value) if value is not None else default
    
    def _get_env_bool(self, key: str, default: bool) -> bool:
        """获取布尔环境变量"""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")
    
    def _validate_config(self):
        """验证配置"""
        # 验证数据源
        valid_sources = ["tdx", "akshare", "yfinance"]
        if self.preferred_data_source not in valid_sources:
            raise ValueError(f"数据源必须是以下之一: {', '.join(valid_sources)}")


# 全局配置实例（延迟初始化）
_config_instance = None


def get_config() -> Config:
    """获取全局配置实例"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


# 全局配置引用
config = get_config()
