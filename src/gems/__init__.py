# Gems Analyzer - AI价值投资分析工具

import logging

# 禁用httpx的HTTP请求日志
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

__version__ = "2.0.0"
