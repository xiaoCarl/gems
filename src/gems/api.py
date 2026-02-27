"""
统一API接口模块
"""

from typing import Any

from gems.data_sources.manager import data_source_manager
from gems.exceptions import FinancialDataError


def get_realtime_stock_data(symbol: str, data_source: str | None = None) -> dict[str, Any]:
    """
    获取A股和港股实时数据
    
    Args:
        symbol: 股票代码（如：600519.SH, 00700.HK）
        data_source: 数据源（可选）
    
    Returns:
        包含实时交易数据的字典
    """
    return data_source_manager.get_realtime_data(symbol, data_source)


def get_stock_financials(symbol: str, period: str = "annual") -> dict[str, Any]:
    """
    获取股票财务数据
    
    Args:
        symbol: 股票代码
        period: 报表周期（annual/quarter）
    
    Returns:
        包含财务报表的字典
    """
    return data_source_manager.get_financial_data(symbol, period)


def get_stock_valuation_data(symbol: str) -> dict[str, Any]:
    """
    获取股票估值数据
    
    Args:
        symbol: 股票代码
    
    Returns:
        包含PE、PB、ROE等估值指标的字典
    """
    try:
        # 获取财务数据
        financial_data = get_stock_financials(symbol, "annual")
        
        # 获取实时价格
        realtime_data = get_realtime_stock_data(symbol)
        current_price = realtime_data.get("current_price", 0)
        
        # 提取关键财务指标（简化计算）
        income = financial_data.get("income_statements", [{}])[0]
        balance = financial_data.get("balance_sheets", [{}])[0]
        
        # 计算估值指标
        net_profit = income.get("归属于母公司所有者的净利润", income.get("净利润", 0))
        total_equity = balance.get("归属于母公司股东权益合计", 0)
        total_shares = balance.get("实收资本(或股本)", balance.get("股本", 1))
        
        if total_shares == 0:
            total_shares = 1
        
        eps = net_profit / total_shares if total_shares > 0 else 0
        bvps = total_equity / total_shares if total_shares > 0 else 0
        
        pe_ratio = current_price / eps if eps > 0 else 0
        pb_ratio = current_price / bvps if bvps > 0 else 0
        roe = (net_profit / total_equity * 100) if total_equity > 0 else 0
        
        return {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "pe_ratio": round(pe_ratio, 2),
            "pb_ratio": round(pb_ratio, 2),
            "roe": round(roe, 2),
            "eps": round(eps, 4),
            "bvps": round(bvps, 4),
            "dividend_yield": 0.0,  # 简化处理
        }
        
    except Exception as e:
        raise FinancialDataError(f"获取估值数据失败: {e}")
