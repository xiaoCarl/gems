"""
统一日志核心模块

提供统一的日志配置和管理，支持结构化日志输出。
"""

import logging
import logging.handlers
import os
from enum import Enum
from typing import Any

from gems.config import get_config


class LogLevel(Enum):
    """日志级别枚举"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Logger:
    """
    统一日志管理器

    提供结构化的日志输出，支持工具调用和LLM调用的详细日志记录。
    """

    def __init__(self, name: str = "gems"):
        self.name = name
        self.logger = logging.getLogger(name)
        self._setup_logger()

    def _setup_logger(self):
        """设置日志器配置"""
        # 清除现有的处理器
        self.logger.handlers.clear()

        # 设置日志级别
        config = get_config()
        log_level = getattr(logging, config.log_level.upper(), logging.WARNING)
        self.logger.setLevel(log_level)

        # 创建格式化器
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        # 启用文件日志，添加文件处理器
        self._add_file_handler(formatter)

    def _add_file_handler(self, formatter: logging.Formatter):
        """添加文件日志处理器"""
        try:
            config = get_config()
            # 确保日志目录存在
            log_dir = os.path.dirname(config.log_file_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            # 创建轮转文件处理器
            file_handler = logging.handlers.RotatingFileHandler(
                config.log_file_path,
                maxBytes=config.log_max_bytes,
                backupCount=config.log_backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(
                getattr(logging, config.log_level.upper(), logging.WARNING)
            )
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
        except Exception as e:
            # 如果文件日志设置失败，只使用控制台日志
            print(f"文件日志设置失败: {e}，将只使用控制台日志")

    def debug(self, message: str, **kwargs: Any) -> None:
        """调试级别日志"""
        if kwargs:
            message = f"{message} | {self._format_kwargs(kwargs)}"
        self.logger.debug(message)

    def info(self, message: str, **kwargs: Any) -> None:
        """信息级别日志"""
        if kwargs:
            message = f"{message} | {self._format_kwargs(kwargs)}"
        self.logger.info(message)

    def warning(self, message: str, **kwargs: Any) -> None:
        """警告级别日志"""
        if kwargs:
            message = f"{message} | {self._format_kwargs(kwargs)}"
        self.logger.warning(message)

    def error(self, message: str, **kwargs: Any) -> None:
        """错误级别日志"""
        if kwargs:
            message = f"{message} | {self._format_kwargs(kwargs)}"
        self.logger.error(message)

    def _format_kwargs(self, kwargs: dict[str, Any]) -> str:
        """格式化关键字参数"""
        formatted = []
        for key, value in kwargs.items():
            # 对长字符串进行截断
            if isinstance(value, str) and len(value) > 100:
                value = value[:100] + "..."
            formatted.append(f"{key}={value}")
        return ", ".join(formatted)

    def log_tool_call_start(self, tool_name: str, args: dict[str, Any]) -> None:
        """记录工具调用开始"""
        self.debug(
            f"工具调用开始: {tool_name}",
            tool_name=tool_name,
            args=self._sanitize_args(args),
        )

    def log_tool_call_end(self, tool_name: str, result: Any, duration: float) -> None:
        """记录工具调用结束"""
        self.debug(
            f"工具调用完成: {tool_name}",
            tool_name=tool_name,
            duration=f"{duration:.2f}s",
            result_type=type(result).__name__,
        )

    def log_tool_call_error(
        self, tool_name: str, error: Exception, duration: float
    ) -> None:
        """记录工具调用错误"""
        self.error(
            f"工具调用失败: {tool_name}",
            tool_name=tool_name,
            error=str(error),
            duration=f"{duration:.2f}s",
        )

    def log_llm_call_start(
        self, prompt: str, system_prompt: str | None = None
    ) -> None:
        """记录LLM调用开始"""
        self.debug(
            "LLM调用开始",
            prompt_length=len(prompt),
            system_prompt_length=len(system_prompt) if system_prompt else 0,
        )

    def log_llm_call_end(self, response: Any, duration: float) -> None:
        """记录LLM调用结束"""
        response_type = type(response).__name__
        response_str = (
            str(response)[:200] + "..." if len(str(response)) > 200 else str(response)
        )

        self.debug(
            "LLM调用完成",
            response_type=response_type,
            response_preview=response_str,
            duration=f"{duration:.2f}s",
        )

    def log_llm_call_error(self, error: Exception, duration: float) -> None:
        """记录LLM调用错误"""
        self.error("LLM调用失败", error=str(error), duration=f"{duration:.2f}s")

    def log_task_start(self, task_description: str) -> None:
        """记录任务开始"""
        self.debug("任务开始执行", task_description=task_description)

    def log_task_end(self, task_description: str, success: bool) -> None:
        """记录任务结束"""
        status = "成功" if success else "失败"
        self.debug(
            f"任务执行{status}", task_description=task_description, success=success
        )

    def _sanitize_args(self, args: dict[str, Any]) -> dict[str, Any]:
        """清理敏感参数"""
        sanitized = {}
        for key, value in args.items():
            # 对敏感信息进行脱敏
            if any(
                sensitive in key.lower()
                for sensitive in ["key", "token", "password", "secret"]
            ):
                sanitized[key] = "***"
            elif isinstance(value, str) and len(value) > 50:
                sanitized[key] = value[:50] + "..."
            else:
                sanitized[key] = value
        return sanitized


# 全局日志器实例
_logger: Logger | None = None


def get_logger(name: str = "gems") -> Logger:
    """获取或创建全局日志器实例"""
    global _logger
    if _logger is None:
        _logger = Logger(name)
    return _logger
