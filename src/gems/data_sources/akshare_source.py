"""
AkShare数据源实现
"""
import akshare as ak
from typing import Dict, Any, List
from gems.exceptions import DataSourceError, InvalidSymbolError
from .base import DataSource


class AkShareDataSource(DataSource):
    """AkShare数据源"""
    
    def __init__(self):
        self.name = "AkShare"
        self._available = True
    
    def get_realtime_data(self, symbol: str) -> Dict[str, Any]:
        """获取实时数据"""
        try:
            # A股处理
            if symbol.endswith(('.SZ', '.SH')):
                clean_symbol = symbol.split('.')[0]
                stock_data = ak.stock_zh_a_spot_em()
                filtered_data = stock_data[stock_data['代码'] == clean_symbol]
                
                if not filtered_data.empty:
                    data = filtered_data.iloc[0].to_dict()
                    return {
                        "symbol": symbol,
                        "current_price": data.get('最新价', 0),
                        "change": data.get('涨跌额', 0),
                        "change_percent": data.get('涨跌幅', 0),
                        "volume": data.get('成交量', 0),
                        "turnover": data.get('成交额', 0),
                        "high": data.get('最高', 0),
                        "low": data.get('最低', 0),
                        "open": data.get('今开', 0),
                        "prev_close": data.get('昨收', 0),
                        "timestamp": data.get('时间', ''),
                        "market": "A股",
                        "data_source": "AkShare"
                    }
                else:
                    raise InvalidSymbolError(f"未找到A股数据: {symbol}")
            
            # 港股处理
            elif symbol.endswith('.HK'):
                clean_symbol = symbol.split('.')[0]
                hk_data = ak.stock_hk_spot_em()
                filtered_data = hk_data[hk_data['代码'] == clean_symbol]
                
                if not filtered_data.empty:
                    data = filtered_data.iloc[0].to_dict()
                    return {
                        "symbol": symbol,
                        "current_price": data.get('最新价', 0),
                        "change": data.get('涨跌额', 0),
                        "change_percent": data.get('涨跌幅', 0),
                        "volume": data.get('成交量', 0),
                        "turnover": data.get('成交额', 0),
                        "high": data.get('最高', 0),
                        "low": data.get('最低', 0),
                        "open": data.get('今开', 0),
                        "prev_close": data.get('昨收', 0),
                        "timestamp": data.get('时间', ''),
                        "market": "港股",
                        "data_source": "AkShare"
                    }
                else:
                    raise InvalidSymbolError(f"未找到港股数据: {symbol}")
            
            else:
                raise InvalidSymbolError(f"不支持的股票代码格式: {symbol}")
                
        except InvalidSymbolError:
            raise
        except Exception as e:
            raise DataSourceError(f"获取AkShare实时数据失败: {e}")
    
    def get_financial_data(self, symbol: str, period: str) -> Dict[str, Any]:
        """获取财务数据"""
        try:
            clean_symbol = symbol.split('.')[0] if '.' in symbol else symbol
            
            # 港股处理
            if symbol.endswith('.HK'):
                hk_analysis_df = ak.stock_financial_hk_analysis_indicator_em(symbol=clean_symbol)
                hk_financial_df = ak.stock_hk_financial_indicator_em(symbol=clean_symbol)
                
                income_statements = hk_analysis_df.to_dict('records')
                balance_sheets = hk_financial_df.to_dict('records')
                cash_flow_statements: List[Dict] = []
                
                return {
                    "income_statements": income_statements,
                    "balance_sheets": balance_sheets,
                    "cash_flow_statements": cash_flow_statements,
                    "market": "港股",
                    "data_source": "AkShare港股财务指标"
                }
            else:
                # A股处理
                income_df = ak.stock_financial_report_sina(stock=clean_symbol, symbol="利润表")
                balance_df = ak.stock_financial_report_sina(stock=clean_symbol, symbol="资产负债表")
                cash_flow_df = ak.stock_financial_report_sina(stock=clean_symbol, symbol="现金流量表")
                
                income_statements = income_df.to_dict('records')
                balance_sheets = balance_df.to_dict('records')
                cash_flow_statements = cash_flow_df.to_dict('records')
                
                return {
                    "income_statements": income_statements,
                    "balance_sheets": balance_sheets,
                    "cash_flow_statements": cash_flow_statements,
                    "market": "A股",
                    "data_source": "AkShare新浪财经"
                }
                
        except Exception as e:
            raise DataSourceError(f"获取AkShare财务数据失败: {e}")
    
    def get_historical_data(self, symbol: str, period: str) -> Dict[str, Any]:
        """获取历史数据"""
        # AkShare 不提供历史数据，抛出异常
        raise DataSourceError("AkShare数据源不支持历史数据获取")
    
    def is_available(self) -> bool:
        """检查数据源是否可用"""
        return self._available