"""
数据源基类定义
"""

from abc import ABC, abstractmethod
from typing import Any


class DataSource(ABC):
    """数据源基类"""

    def __init__(self):
        self.name = ""
        self.description = ""

    @abstractmethod
    def is_available(self) -> bool:
        """检查数据源是否可用"""
        pass

    @abstractmethod
    def get_realtime_data(self, symbol: str) -> dict[str, Any]:
        """获取实时数据"""
        pass

    @abstractmethod
    def get_financial_data(self, symbol: str, period: str) -> dict[str, Any]:
        """获取财务数据"""
        pass

    @abstractmethod
    def get_historical_data(self, symbol: str, period: str) -> dict[str, Any]:
        """获取历史数据"""
        pass
