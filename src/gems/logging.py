"""
统一日志记录模块
"""
import logging
import sys
from typing import Optional
from gems.config import config


class Logger:
    """统一日志记录器"""
    
    def __init__(self, name: str = "gems"):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """配置日志记录器"""
        # 设置日志级别
        log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 创建格式化器
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # 创建控制台处理器
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
    
    def debug(self, message: str, **kwargs) -> None:
        """记录调试信息"""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message: str, **kwargs) -> None:
        """记录一般信息"""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs) -> None:
        """记录警告信息"""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, **kwargs) -> None:
        """记录错误信息"""
        self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, **kwargs) -> None:
        """记录严重错误信息"""
        self.logger.critical(self._format_message(message, **kwargs))
    
    def _format_message(self, message: str, **kwargs) -> str:
        """格式化消息"""
        if kwargs:
            extra_info = " ".join([f"{k}={v}" for k, v in kwargs.items()])
            return f"{message} [{extra_info}]"
        return message


# 全局日志记录器实例
logger = Logger()


def get_logger(name: Optional[str] = None) -> Logger:
    """获取指定名称的日志记录器"""
    if name:
        return Logger(name)
    return logger