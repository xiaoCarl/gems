"""
错误处理工具模块
"""

import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from gems.exceptions import (
    AgentError,
    APIRateLimitError,
    APITimeoutError,
    CacheError,
    DataSourceError,
    FinancialDataError,
    InvalidSymbolError,
    ValidationError,
)
from gems.logging import get_logger


def handle_data_source_errors(max_retries: int = 3, retry_delay: float = 1.0):
    """
    数据源错误处理装饰器

    Args:
        max_retries: 最大重试次数
        retry_delay: 重试延迟（秒）

    Returns:
        装饰器函数
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = get_logger("error_handling")

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except APIRateLimitError as e:
                    if attempt < max_retries:
                        wait_time = getattr(e, "retry_after", retry_delay)
                        logger.warning(
                            f"API频率限制，第{attempt + 1}次重试，等待{wait_time}秒",
                            source=e.context.get("source"),
                            retry_after=wait_time,
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error(
                            "API频率限制，达到最大重试次数",
                            source=e.context.get("source"),
                            max_retries=max_retries,
                        )
                        raise

                except APITimeoutError as e:
                    if attempt < max_retries:
                        logger.warning(
                            f"API超时，第{attempt + 1}次重试",
                            source=e.context.get("source"),
                            timeout=e.context.get("timeout"),
                        )
                        time.sleep(retry_delay)
                        continue
                    else:
                        logger.error(
                            "API超时，达到最大重试次数",
                            source=e.context.get("source"),
                            max_retries=max_retries,
                        )
                        raise

                except InvalidSymbolError as e:
                    logger.error(
                        "无效股票代码",
                        symbol=e.context.get("symbol"),
                        source=e.context.get("source"),
                    )
                    raise

                except FinancialDataError as e:
                    logger.error(
                        "财务数据错误", symbol=e.context.get("symbol"), error=e.message
                    )
                    raise

                except DataSourceError as e:
                    if attempt < max_retries:
                        logger.warning(
                            f"数据源错误，第{attempt + 1}次重试",
                            source=e.context.get("source"),
                            error=e.message,
                        )
                        time.sleep(retry_delay)
                        continue
                    else:
                        logger.error(
                            "数据源错误，达到最大重试次数",
                            source=e.context.get("source"),
                            max_retries=max_retries,
                        )
                        raise

                except Exception as e:
                    logger.error("未知数据源错误", error=str(e), function=func.__name__)
                    raise DataSourceError(
                        f"数据源处理失败: {str(e)}",
                        source=getattr(e, "context", {}).get("source", "unknown"),
                        function=func.__name__,
                    )

            # 理论上不会执行到这里
            raise DataSourceError("未知错误")

        return wrapper

    return decorator


def handle_validation_errors(func: Callable) -> Callable:
    """
    数据验证错误处理装饰器
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger = get_logger("error_handling")

        try:
            return func(*args, **kwargs)

        except ValidationError as e:
            logger.error(
                "数据验证失败",
                field=e.context.get("field"),
                value=e.context.get("value"),
                error=e.message,
            )
            raise

        except Exception as e:
            logger.error("验证过程中发生未知错误", error=str(e), function=func.__name__)
            raise ValidationError(f"数据验证失败: {str(e)}", function=func.__name__)

    return wrapper


def handle_cache_errors(func: Callable) -> Callable:
    """
    缓存错误处理装饰器
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger = get_logger("error_handling")

        try:
            return func(*args, **kwargs)

        except CacheError as e:
            logger.error(
                "缓存操作失败",
                cache_type=e.context.get("cache_type"),
                key=e.context.get("key"),
                error=e.message,
            )
            # 缓存错误通常不抛出，而是降级到直接获取数据
            logger.info("缓存失败，降级到直接数据获取")
            return None

        except Exception as e:
            logger.error("缓存过程中发生未知错误", error=str(e), function=func.__name__)
            # 缓存错误通常不抛出
            return None

    return wrapper


def handle_agent_errors(func: Callable) -> Callable:
    """
    智能体错误处理装饰器
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger = get_logger("error_handling")

        try:
            return func(*args, **kwargs)

        except AgentError as e:
            logger.error(
                "智能体执行失败",
                task=e.context.get("task"),
                step=e.context.get("step"),
                error=e.message,
            )
            raise

        except Exception as e:
            logger.error(
                "智能体执行过程中发生未知错误", error=str(e), function=func.__name__
            )
            raise AgentError(f"智能体执行失败: {str(e)}", function=func.__name__)

    return wrapper


def safe_execute(
    func: Callable,
    exception_types: tuple | None = None,
    default_return: Any = None,
    log_error: bool = True,
) -> Any:
    """
    安全执行函数，捕获指定异常

    Args:
        func: 要执行的函数
        exception_types: 要捕获的异常类型元组，默认为所有异常
        default_return: 异常发生时的默认返回值
        log_error: 是否记录错误日志

    Returns:
        函数执行结果或默认返回值
    """
    if exception_types is None:
        exception_types = (Exception,)

    logger = get_logger("error_handling")

    try:
        return func()

    except exception_types as e:
        if log_error:
            logger.error(
                "安全执行失败",
                function=func.__name__,
                error=str(e),
                exception_type=type(e).__name__,
            )
        return default_return


def retry_on_failure(
    max_retries: int = 3,
    retry_delay: float = 1.0,
    exception_types: tuple = (Exception,),
    backoff_factor: float = 1.0,
) -> Callable:
    """
    失败重试装饰器

    Args:
        max_retries: 最大重试次数
        retry_delay: 初始重试延迟（秒）
        exception_types: 触发重试的异常类型
        backoff_factor: 退避因子，每次重试延迟乘以该因子

    Returns:
        装饰器函数
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = get_logger("error_handling")

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except exception_types as e:
                    if attempt < max_retries:
                        current_delay = retry_delay * (backoff_factor**attempt)
                        logger.warning(
                            f"执行失败，第{attempt + 1}次重试，等待{current_delay:.2f}秒",
                            function=func.__name__,
                            error=str(e),
                            attempt=attempt + 1,
                        )
                        time.sleep(current_delay)
                        continue
                    else:
                        logger.error(
                            "执行失败，达到最大重试次数",
                            function=func.__name__,
                            error=str(e),
                            max_retries=max_retries,
                        )
                        raise

            # 理论上不会执行到这里
            raise Exception("重试机制异常")

        return wrapper

    return decorator
