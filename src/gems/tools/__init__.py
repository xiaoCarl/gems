"""
工具模块
"""

from .financials import get_stock_realtime, get_stock_financials, get_stock_valuation

TOOLS = [
    get_stock_realtime,
    get_stock_financials,
    get_stock_valuation,
]
