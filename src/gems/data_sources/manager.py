"""
数据源管理器
"""
from typing import Dict, Any, Optional, List
from gems.config import config
from gems.exceptions import DataSourceError
from gems.output.core import get_output_engine
from .base import DataSource
from .akshare_source import AkShareDataSource
from .yfinance_source import YFinanceDataSource
from .tdx_source import TDXDataSource


class DataSourceManager:
    """数据源管理器"""
    
    def __init__(self):
        self.sources = {
            "akshare": AkShareDataSource(),
            "yfinance": YFinanceDataSource(),
            "tdx": TDXDataSource(),
        }
        self.output = get_output_engine()
        self._initialize_sources()
    
    def _initialize_sources(self) -> None:
        """初始化数据源"""
        # 检查各数据源可用性
        for name, source in self.sources.items():
            try:
                available = source.is_available()
                self.output.show_progress(f"数据源 {name}: {'可用' if available else '不可用'}")
            except Exception as e:
                self.output.show_progress(f"检查数据源 {name} 可用性失败: {str(e)}")
    
    def get_realtime_data(self, symbol: str, preferred_source: Optional[str] = None) -> Dict[str, Any]:
        """获取实时数据"""
        if preferred_source is None:
            preferred_source = config.PREFERRED_DATA_SOURCE
        
        # 根据股票类型选择数据源策略
        if symbol.endswith('.HK'):
            # 港股优先使用通达信，其次yfinance
            sources_order = ["yfinance", "akshare"]
        else:
            # A股优先使用通达信，其次使用配置的优先数据源
            sources_order = ["tdx", preferred_source, "akshare"]
        
        last_error = None
        
        for source_name in sources_order:
            if source_name in self.sources:
                source = self.sources[source_name]
                try:
                    if source.is_available():
                        data = source.get_realtime_data(symbol)
                        self.output.show_progress(f"使用数据源: {source_name} - 股票: {symbol}")
                        return data
                except Exception as e:
                    last_error = e
                    self.output.show_progress(f"数据源 {source_name} 失败 - 股票: {symbol}, 错误: {str(e)}")
        
        if last_error:
            raise DataSourceError(f"所有数据源都失败，最后错误: {last_error}")
        else:
            raise DataSourceError("没有可用的数据源")
    
    def get_financial_data(self, symbol: str, period: str) -> Dict[str, Any]:
        """获取财务数据"""
        # 财务数据主要使用AkShare
        if "akshare" in self.sources:
            source = self.sources["akshare"]
            if source.is_available():
                return source.get_financial_data(symbol, period)
        
        raise DataSourceError("AkShare数据源不可用，无法获取财务数据")
    
    def get_available_sources(self) -> List[str]:
        """获取可用数据源列表"""
        available = []
        for name, source in self.sources.items():
            if source.is_available():
                available.append(name)
        return available


# 全局数据源管理器实例
data_source_manager = DataSourceManager()