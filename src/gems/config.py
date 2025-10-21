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
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    #LOG_ENABLE_DEBUG: bool = os.getenv("LOG_ENABLE_DEBUG", "false").lower() == "true"
    LOG_TO_CONSOLE: bool = False
    LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", "logs/gems.log")
    LOG_MAX_BYTES: int = int(os.getenv("LOG_MAX_BYTES", "10485760"))  # 10MB
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    
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
        
        if cls.LOG_MAX_BYTES <= 0:
            raise ValueError("LOG_MAX_BYTES must be positive")
        
        if cls.LOG_BACKUP_COUNT < 0:
            raise ValueError("LOG_BACKUP_COUNT must be non-negative")


# 全局配置实例
config = Config()