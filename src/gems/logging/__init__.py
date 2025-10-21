"""
统一日志模块

提供统一的日志配置和管理，支持结构化日志输出。
"""

from .core import Logger, get_logger

__all__ = ["Logger", "get_logger"]