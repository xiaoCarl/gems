"""
统一输出框架

提供简洁、易维护的命令行输出解决方案。
"""

from gems.output.core import SimpleOutputEngine, get_output_engine, set_output_engine

__all__ = [
    "SimpleOutputEngine",
    "get_output_engine", 
    "set_output_engine"
]