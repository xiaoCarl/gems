"""
配置管理模块
"""
import os
from typing import Optional


class Config:
    """全局配置类"""
    
    # API Keys
    FINNHUB_API_KEY: Optional[str] = os.getenv("FINNHUB_API_KEY")
    
    # 数据源配置
    #PREFERRED_DATA_SOURCE: str = os.getenv("PREFERRED_DATA_SOURCE", "tdx")
    
    # 请求配置
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: float = float(os.getenv("RETRY_DELAY", "1.0"))
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "WARNING")
    
    # 数据源可用性标志
    TDX_AVAILABLE: bool = True  # 在运行时动态检查
    
    # 缓存配置
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL_REALTIME: int = int(os.getenv("CACHE_TTL_REALTIME", "300"))    # 5分钟
    CACHE_TTL_FINANCIAL: int = int(os.getenv("CACHE_TTL_FINANCIAL", "3600"))  # 1小时
    CACHE_TTL_HISTORICAL: int = int(os.getenv("CACHE_TTL_HISTORICAL", "86400"))  # 24小时
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "1000"))
    
    @classmethod
    def validate(cls) -> None:
        """验证配置"""
#        if cls.PREFERRED_DATA_SOURCE not in ["tdx", "akshare"]:
#            raise ValueError("PREFERRED_DATA_SOURCE must be 'tdx' or 'akshare'")
        
        if cls.REQUEST_TIMEOUT <= 0:
            raise ValueError("REQUEST_TIMEOUT must be positive")
        
        if cls.MAX_RETRIES < 0:
            raise ValueError("MAX_RETRIES must be non-negative")
        
        if cls.CACHE_TTL_REALTIME <= 0:
            raise ValueError("CACHE_TTL_REALTIME must be positive")
        
        if cls.CACHE_TTL_FINANCIAL <= 0:
            raise ValueError("CACHE_TTL_FINANCIAL must be positive")
        
        if cls.CACHE_TTL_HISTORICAL <= 0:
            raise ValueError("CACHE_TTL_HISTORICAL must be positive")
        
        if cls.CACHE_MAX_SIZE <= 0:
            raise ValueError("CACHE_MAX_SIZE must be positive")


# 全局配置实例
config = Config()