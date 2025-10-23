"""
自定义异常类
"""

from typing import Any


class GemsError(Exception):
    """基础异常类"""

    def __init__(self, message: str, context: dict[str, Any] | None = None):
        self.message = message
        self.context = context or {}
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """格式化错误消息"""
        base_message = self.message
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{base_message} [{context_str}]"
        return base_message

    def add_context(self, key: str, value: Any) -> None:
        """添加上下文信息"""
        self.context[key] = value


class DataSourceError(GemsError):
    """数据源异常"""

    def __init__(self, message: str, source: str | None = None, **kwargs):
        context = {"source": source} if source else {}
        context.update(kwargs)
        super().__init__(message, context)


class APIRateLimitError(DataSourceError):
    """API频率限制异常"""

    def __init__(self, source: str, retry_after: int | None = None, **kwargs):
        message = f"数据源 {source} 频率限制"
        if retry_after:
            message += f"，建议等待 {retry_after} 秒"

        context = {"source": source}
        if retry_after:
            context["retry_after"] = retry_after
        context.update(kwargs)

        super().__init__(message, source, **context)


class APITimeoutError(DataSourceError):
    """API超时异常"""

    def __init__(self, source: str, timeout: int, **kwargs):
        message = f"数据源 {source} 请求超时 ({timeout}秒)"
        context = {"source": source, "timeout": timeout}
        context.update(kwargs)
        super().__init__(message, source, **context)


class InvalidSymbolError(DataSourceError):
    """无效股票代码异常"""

    def __init__(self, symbol: str, source: str | None = None, **kwargs):
        message = f"无效的股票代码: {symbol}"
        context = {"symbol": symbol}
        if source:
            context["source"] = source
        context.update(kwargs)
        super().__init__(message, source, **context)


class FinancialDataError(DataSourceError):
    """财务数据异常"""

    def __init__(self, message: str, symbol: str | None = None, **kwargs):
        context = {"symbol": symbol} if symbol else {}
        context.update(kwargs)
        super().__init__(message, **context)


class ConfigurationError(GemsError):
    """配置异常"""

    def __init__(self, message: str, config_key: str | None = None, **kwargs):
        context = {"config_key": config_key} if config_key else {}
        context.update(kwargs)
        super().__init__(message, context)


class ValidationError(GemsError):
    """数据验证异常"""

    def __init__(
        self, message: str, field: str | None = None, value: Any = None, **kwargs
    ):
        context = {}
        if field:
            context["field"] = field
        if value is not None:
            context["value"] = value
        context.update(kwargs)
        super().__init__(message, context)


class CacheError(GemsError):
    """缓存异常"""

    def __init__(
        self,
        message: str,
        cache_type: str | None = None,
        key: str | None = None,
        **kwargs,
    ):
        context = {}
        if cache_type:
            context["cache_type"] = cache_type
        if key:
            context["key"] = key
        context.update(kwargs)
        super().__init__(message, context)


class AgentError(GemsError):
    """智能体异常"""

    def __init__(
        self,
        message: str,
        task: str | None = None,
        step: int | None = None,
        **kwargs,
    ):
        context = {}
        if task:
            context["task"] = task
        if step is not None:
            context["step"] = step
        context.update(kwargs)
        super().__init__(message, context)


class ModelError(GemsError):
    """模型异常"""

    def __init__(self, message: str, model: str | None = None, **kwargs):
        context = {"model": model} if model else {}
        context.update(kwargs)
        super().__init__(message, context)
