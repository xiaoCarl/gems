# This file makes the directory a Python package

import logging

# 禁用httpx的HTTP请求日志
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
