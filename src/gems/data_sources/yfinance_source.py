"""
yfinance数据源实现
"""
import yfinance as yf
import time
from typing import Dict, Any
from gems.exceptions import DataSourceError, APIRateLimitError, InvalidSymbolError
from .base import DataSource


class YFinanceDataSource(DataSource):
    """yfinance数据源（主要用于港股）"""
    
    def __init__(self):
        self.name = "yfinance"
        self._available = True
        self._last_request_time = 0.0
        self._min_request_interval = 1.0  # 最小请求间隔（秒）
    
    def _rate_limit(self) -> None:
        """频率限制控制"""
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        
        if time_since_last_request < self._min_request_interval:
            sleep_time = self._min_request_interval - time_since_last_request
            time.sleep(sleep_time)
        
        self._last_request_time = time.time()
    
    def get_realtime_data(self, symbol: str) -> Dict[str, Any]:
        """获取实时数据"""
        try:
            self._rate_limit()
            
            # 港股处理
            if symbol.endswith('.HK'):
                clean_symbol = symbol.split('.')[0].lstrip('0') + '.HK'
                
                ticker = yf.Ticker(clean_symbol)
                
                # 获取历史数据
                hist = ticker.history(period="1d", interval="1m")
                
                if hist.empty:
                    hist = ticker.history(period="1d")
                
                if not hist.empty:
                    latest_data = hist.iloc[-1]
                    
                    # 获取基本信息
                    try:
                        info = ticker.info
                        current_price = info.get('currentPrice', latest_data['Close'])
                        prev_close = info.get('previousClose', latest_data['Close'])
                        company_name = info.get('longName', '')
                    except:
                        current_price = latest_data['Close']
                        prev_close = latest_data['Open'] if len(hist) > 1 else latest_data['Close']
                        company_name = ''
                    
                    change = current_price - prev_close
                    change_percent = (change / prev_close * 100) if prev_close > 0 else 0
                    
                    return {
                        "symbol": symbol,
                        "name": company_name,
                        "current_price": round(current_price, 2),
                        "prev_close": round(prev_close, 2),
                        "open": round(latest_data['Open'], 2),
                        "high": round(latest_data['High'], 2),
                        "low": round(latest_data['Low'], 2),
                        "volume": int(latest_data['Volume']),
                        "turnover": 0,  # yfinance不直接提供成交额
                        "change": round(change, 2),
                        "change_percent": round(change_percent, 2),
                        "timestamp": hist.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
                        "market": "港股",
                        "data_source": "yfinance"
                    }
                else:
                    raise InvalidSymbolError(f"未找到港股数据: {symbol}")
            else:
                raise InvalidSymbolError(f"yfinance仅支持港股: {symbol}")
                
        except InvalidSymbolError:
            raise
        except Exception as e:
            if "Too Many Requests" in str(e):
                raise APIRateLimitError(f"yfinance频率限制: {e}")
            raise DataSourceError(f"获取yfinance实时数据失败: {e}")
    
    def get_financial_data(self, symbol: str, period: str) -> Dict[str, Any]:
        """获取财务数据 - yfinance不支持中国股票财务数据"""
        raise DataSourceError("yfinance不支持中国股票财务数据，请使用AkShare")
    
    def get_historical_data(self, symbol: str, period: str) -> Dict[str, Any]:
        """获取历史数据"""
        # yfinance 不提供中国股票历史数据，抛出异常
        raise DataSourceError("yfinance数据源不支持中国股票历史数据获取")
    
    def is_available(self) -> bool:
        """检查数据源是否可用"""
        if self._available is None:
            from .availability import availability_tester
            self._available, _ = availability_tester.test_yfinance_availability()
        return self._available