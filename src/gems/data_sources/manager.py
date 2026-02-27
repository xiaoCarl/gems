"""
数据源管理器
"""

from typing import Any

from gems.cache.manager import cache_manager
from gems.config import config
from gems.exceptions import DataSourceError


class DataSourceManager:
    """数据源管理器"""
    
    def __init__(self):
        self._akshare = None
        self._yfinance = None
    
    def _get_akshare(self):
        """获取AkShare实例"""
        if self._akshare is None:
            import akshare as ak
            self._akshare = ak
        return self._akshare
    
    def get_realtime_data(self, symbol: str, data_source: str | None = None) -> dict[str, Any]:
        """获取实时数据"""
        # 检查缓存
        cached = cache_manager.get_realtime_data(symbol)
        if cached:
            return cached
        
        # 解析市场
        if "." in symbol:
            code, market = symbol.split(".")
        else:
            code = symbol
            market = "SH" if symbol.startswith("6") else "SZ"
        
        try:
            ak = self._get_akshare()
            
            if market in ["SH", "SZ"]:
                # A股
                df = ak.stock_zh_a_spot_em()
                row = df[df["代码"] == code]
                if len(row) == 0:
                    raise DataSourceError(f"股票 {symbol} 未找到")
                
                row = row.iloc[0]
                result = {
                    "symbol": symbol,
                    "name": row.get("名称", ""),
                    "current_price": float(row.get("最新价", 0)),
                    "open": float(row.get("今开", 0)),
                    "high": float(row.get("最高", 0)),
                    "low": float(row.get("最低", 0)),
                    "prev_close": float(row.get("昨收", 0)),
                    "volume": int(row.get("成交量", 0)),
                    "change_percent": float(row.get("涨跌幅", 0)),
                }
            else:
                # 港股
                df = ak.stock_hk_ggt_components_em()
                row = df[df["代码"] == code]
                if len(row) == 0:
                    raise DataSourceError(f"股票 {symbol} 未找到")
                
                row = row.iloc[0]
                result = {
                    "symbol": symbol,
                    "name": row.get("名称", ""),
                    "current_price": float(row.get("最新价", 0)),
                    "open": float(row.get("今开", 0)),
                    "high": float(row.get("最高", 0)),
                    "low": float(row.get("最低", 0)),
                    "prev_close": float(row.get("昨收", 0)),
                    "volume": int(row.get("成交量", 0)),
                    "change_percent": float(row.get("涨跌幅", 0)),
                }
            
            # 缓存结果
            cache_manager.set_realtime_data(symbol, result)
            return result
            
        except Exception as e:
            raise DataSourceError(f"获取实时数据失败: {e}")
    
    def get_financial_data(self, symbol: str, period: str = "annual") -> dict[str, Any]:
        """获取财务数据"""
        # 检查缓存
        cached = cache_manager.get_financial_data(symbol, period)
        if cached:
            return cached
        
        try:
            ak = self._get_akshare()
            
            if "." in symbol:
                code, market = symbol.split(".")
            else:
                code = symbol
                market = "SH" if symbol.startswith("6") else "SZ"
            
            if market in ["SH", "SZ"]:
                # A股财务数据
                income = ak.stock_financial_report_sina(stock="profit", symbol=code)
                balance = ak.stock_financial_report_sina(stock="balance", symbol=code)
                cashflow = ak.stock_financial_report_sina(stock="cashflow", symbol=code)
            else:
                # 港股财务数据
                income = ak.stock_financial_hk_report_em(stock="00700", symbol=code, indicator="年度报表")
                balance = ak.stock_financial_hk_report_em(stock="00700", symbol=code, indicator="年度报表")
                cashflow = ak.stock_financial_hk_report_em(stock="00700", symbol=code, indicator="年度报表")
            
            result = {
                "income_statements": income.to_dict("records") if hasattr(income, "to_dict") else income,
                "balance_sheets": balance.to_dict("records") if hasattr(balance, "to_dict") else balance,
                "cash_flow_statements": cashflow.to_dict("records") if hasattr(cashflow, "to_dict") else cashflow,
            }
            
            # 缓存结果
            cache_manager.set_financial_data(symbol, period, result)
            return result
            
        except Exception as e:
            raise DataSourceError(f"获取财务数据失败: {e}")


# 全局数据源管理器
data_source_manager = DataSourceManager()
