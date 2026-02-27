"""
财务数据工具
"""

from langchain_core.tools import tool

from gems.api import get_realtime_stock_data, get_stock_financials as _get_financials
from gems.api import get_stock_valuation_data


@tool
def get_stock_realtime(symbol: str) -> dict:
    """
    获取股票实时行情数据
    
    Args:
        symbol: 股票代码（如：600519.SH, 00700.HK）
    
    Returns:
        实时行情数据字典
    """
    return get_realtime_stock_data(symbol)


@tool
def get_stock_financials(symbol: str, period: str = "annual") -> dict:
    """
    获取股票财务数据
    
    Args:
        symbol: 股票代码
        period: 报表周期（annual-年报，quarter-季报）
    
    Returns:
        财务数据字典
    """
    return _get_financials(symbol, period)


@tool
def get_stock_valuation(symbol: str) -> dict:
    """
    获取股票估值数据（PE、PB、ROE等）
    
    Args:
        symbol: 股票代码
    
    Returns:
        估值指标字典
    """
    return get_stock_valuation_data(symbol)
