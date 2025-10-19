"""
自定义异常类
"""


class GemsError(Exception):
    """基础异常类"""
    pass


class DataSourceError(GemsError):
    """数据源异常"""
    pass


class APIRateLimitError(DataSourceError):
    """API频率限制异常"""
    pass


class APITimeoutError(DataSourceError):
    """API超时异常"""
    pass


class InvalidSymbolError(DataSourceError):
    """无效股票代码异常"""
    pass


class FinancialDataError(DataSourceError):
    """财务数据异常"""
    pass


class ConfigurationError(GemsError):
    """配置异常"""
    pass


class ValidationError(GemsError):
    """数据验证异常"""
    pass