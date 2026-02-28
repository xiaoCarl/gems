"""
日志工具 - 简化版
"""

import os
import logging
from typing import Optional


def setup_logger(name: str = "gems",
                 log_level: Optional[str] = None,
                 log_file: Optional[str] = None) -> logging.Logger:
    """
    设置日志记录器 - 简化版

    Args:
        name: 日志记录器名称
        log_level: 日志级别，默认从环境变量读取
        log_file: 日志文件路径，默认从环境变量读取

    Returns:
        配置好的日志记录器
    """
    # 获取配置
    if log_level is None:
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # 清除现有的处理器
    logger.handlers.clear()

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 创建文件处理器（如果指定了日志文件）
    if log_file:
        try:
            # 确保日志目录存在
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"创建文件日志处理器失败: {e}")

    return logger