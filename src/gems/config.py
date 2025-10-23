"""
配置管理模块
"""

import os


class Config:
    """统一配置类"""

    def __init__(self):
        # LLM API配置
        self.deepseek_api_key: str = self._get_env(
            "DEEPSEEK_API_KEY", required=os.getenv("GEMS_TEST_MODE") != "true"
        )
        self.use_qwen: bool = self._get_env_bool("USE_QWEN", default=False)
        self.dashscope_api_key: str | None = self._get_env("DASHSCOPE_API_KEY")

        # 数据源配置
        self.preferred_data_source: str = self._get_env("PREFERRED_DATA_SOURCE", "tdx")
        self.request_timeout: int = self._get_env_int("REQUEST_TIMEOUT", 30)
        self.max_retries: int = self._get_env_int("MAX_RETRIES", 3)
        self.retry_delay: float = self._get_env_float("RETRY_DELAY", 1.0)

        # 日志配置
        self.log_level: str = self._get_env("LOG_LEVEL", "info")
        self.log_to_console: bool = self._get_env_bool("LOG_TO_CONSOLE", False)
        self.log_file_path: str = self._get_env("LOG_FILE_PATH", "logs/gems.log")
        self.log_max_bytes: int = self._get_env_int("LOG_MAX_BYTES", 10_485_760)  # 10MB
        self.log_backup_count: int = self._get_env_int("LOG_BACKUP_COUNT", 5)

        # 缓存配置
        self.cache_enabled: bool = self._get_env_bool("CACHE_ENABLED", True)
        self.cache_ttl_realtime: int = self._get_env_int(
            "CACHE_TTL_REALTIME", 300
        )  # 5分钟
        self.cache_ttl_financial: int = self._get_env_int(
            "CACHE_TTL_FINANCIAL", 3600
        )  # 1小时
        self.cache_ttl_historical: int = self._get_env_int(
            "CACHE_TTL_HISTORICAL", 86400
        )  # 24小时
        self.cache_ttl_analysis: int = self._get_env_int(
            "CACHE_TTL_ANALYSIS", 86400
        )  # 24小时
        self.cache_max_size: int = self._get_env_int("CACHE_MAX_SIZE", 1000)

        # 业务配置 - 典型股票价格（用于降级策略）
        self.typical_stock_prices: dict[str, float] = {
            "600519.SH": 1600.0,  # 贵州茅台
            "000001.SZ": 12.0,  # 平安银行
            "600036.SH": 35.0,  # 招商银行
        }
        self.default_typical_price: float = 10.0

        # 数据源可用性标志（运行时动态设置）
        self.tdx_available: bool = True

        # 验证配置
        self._validate_config()

    def _get_env(
        self, key: str, default: str | None = None, required: bool = False
    ) -> str:
        """获取环境变量"""
        value = os.getenv(key, default)
        if required and value is None:
            raise ValueError(f"环境变量 {key} 是必需的")
        return value

    def _get_env_int(self, key: str, default: int) -> int:
        """获取整数环境变量"""
        value = os.getenv(key)
        return int(value) if value is not None else default

    def _get_env_float(self, key: str, default: float) -> float:
        """获取浮点数环境变量"""
        value = os.getenv(key)
        return float(value) if value is not None else default

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

        # 验证超时
        if self.request_timeout <= 0:
            raise ValueError("请求超时必须为正数")

        # 验证重试次数
        if self.max_retries < 0:
            raise ValueError("最大重试次数必须为非负数")

        # 验证缓存配置
        if self.cache_ttl_realtime <= 0:
            raise ValueError("实时数据缓存TTL必须为正数")
        if self.cache_ttl_financial <= 0:
            raise ValueError("财务数据缓存TTL必须为正数")
        if self.cache_ttl_historical <= 0:
            raise ValueError("历史数据缓存TTL必须为正数")
        if self.cache_max_size <= 0:
            raise ValueError("缓存最大大小必须为正数")

        # 验证日志配置
        if self.log_max_bytes <= 0:
            raise ValueError("日志最大字节数必须为正数")
        if self.log_backup_count < 0:
            raise ValueError("日志备份数量必须为非负数")

        # 验证典型价格
        if self.default_typical_price <= 0:
            raise ValueError("默认典型价格必须为正数")

    def get_typical_price(self, symbol: str) -> float:
        """获取股票的典型价格"""
        return self.typical_stock_prices.get(symbol, self.default_typical_price)

    def update_typical_price(self, symbol: str, price: float) -> None:
        """更新股票的典型价格"""
        if price <= 0:
            raise ValueError("典型价格必须为正数")
        self.typical_stock_prices[symbol] = price


# 全局配置实例（延迟初始化）
_config_instance = None


def get_config() -> Config:
    """获取全局配置实例"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


# 为了向后兼容，保留config变量，但在测试环境中延迟初始化
if os.getenv("GEMS_TEST_MODE") != "true":
    config = get_config()
else:
    # 在测试环境中，config变量为None，需要显式调用get_config()
    config = None
