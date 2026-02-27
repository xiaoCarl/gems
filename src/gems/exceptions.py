"""
自定义异常类
"""


class GemsError(Exception):
    """基础异常"""
    pass


class DataSourceError(GemsError):
    """数据源错误"""
    pass


class FinancialDataError(GemsError):
    """财务数据错误"""
    pass


class ConfigurationError(GemsError):
    """配置错误"""
    pass
