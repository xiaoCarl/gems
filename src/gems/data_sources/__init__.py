"""
数据源抽象层
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class DataSource(ABC):
    """数据源抽象基类"""
    
    @abstractmethod
    def get_realtime_data(self, symbol: str) -> Dict[str, Any]:
        """获取实时数据"""
        pass
    
    @abstractmethod
    def get_financial_data(self, symbol: str, period: str) -> Dict[str, Any]:
        """获取财务数据"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查数据源是否可用"""
        pass