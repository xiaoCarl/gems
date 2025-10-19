"""
通达信API模块 - 专门用于获取实时行情数据

参考 tdx_utils.md 文档实现，使用通达信API作为主要实时数据源。
"""

import os
import time
import logging
from typing import Optional, Dict, Any
from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TDXProvider:
    """通达信数据提供器"""
    
    def __init__(self):
        self.api = None
        self.ex_api = None
        self.connected = False
        self.ex_connected = False
        
        # 通达信服务器配置（参考文档）
        self.servers = [
            ("115.238.56.198", 7709),
            ("115.238.90.165", 7709),
            ("180.153.18.170", 7709),
            ("119.147.212.81", 7709)
        ]
        
        # 扩展行情服务器（港股等）
        self.ex_servers = [
            ("112.74.214.43", 7727),   # 港股服务器
            ("120.27.164.69", 7727),   # 港股服务器
        ]
    
    def connect(self) -> bool:
        """连接通达信行情服务器"""
        for server_ip, server_port in self.servers:
            try:
                self.api = TdxHq_API()
                if self.api.connect(server_ip, server_port):
                    self.connected = True
                    # 连接成功，不显示日志
                    return True
            except Exception as e:
                logger.warning(f"连接通达信服务器 {server_ip}:{server_port} 失败: {e}")
                continue
        
        logger.error("所有通达信服务器连接失败")
        return False
    
    def connect_ex(self) -> bool:
        """连接通达信扩展行情服务器（港股）"""
        for server_ip, server_port in self.ex_servers:
            try:
                self.ex_api = TdxExHq_API()
                if self.ex_api.connect(server_ip, server_port):
                    self.ex_connected = True
                    logger.info(f"通达信扩展行情连接成功: {server_ip}:{server_port}")
                    return True
            except Exception as e:
                logger.warning(f"连接通达信扩展行情服务器 {server_ip}:{server_port} 失败: {e}")
                continue
        
        logger.error("所有通达信扩展行情服务器连接失败")
        return False
    
    def disconnect(self):
        """断开连接"""
        if self.api and self.connected:
            self.api.disconnect()
            self.connected = False
        if self.ex_api and self.ex_connected:
            self.ex_api.disconnect()
            self.ex_connected = False
    
    def is_connected(self) -> bool:
        """检查连接状态"""
        return self.connected
    
    def get_real_time_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        获取股票实时行情数据
        
        Args:
            symbol: 股票代码，格式: '000001.SZ', '600000.SH', '00700.HK'
            
        Returns:
            实时行情数据字典，包含价格、成交量、涨跌幅等信息
        """
        if not self.connected and not self.connect():
            return None
        
        try:
            # A股处理
            if symbol.endswith(('.SZ', '.SH')):
                market = 0 if symbol.endswith('.SZ') else 1
                clean_symbol = symbol.split('.')[0]
                
                # 获取实时行情
                if self.api is None:
                    return None
                data = self.api.get_security_quotes([(market, clean_symbol)])
                if data and len(data) > 0:
                    return self._parse_a_stock_data(data[0], symbol)
            
            # 港股处理
            elif symbol.endswith('.HK'):
                if not self.ex_connected and not self.connect_ex():
                    return None
                
                clean_symbol = symbol.split('.')[0]
                # 港股市场代码为4
                if self.ex_api is None:
                    return None
                data = self.ex_api.get_instrument_quote(4, clean_symbol)
                if data:
                    return self._parse_hk_stock_data(data, symbol)
            
        except Exception as e:
            logger.error(f"获取通达信实时数据失败: {e}")
            return None
        
        return None
    
    def _parse_a_stock_data(self, data: Dict[str, Any], symbol: str) -> Dict[str, Any]:
        """解析A股实时数据"""
        current_price = data.get('price', 0)
        prev_close = data.get('last_close', 0)
        change = current_price - prev_close
        change_percent = (change / prev_close * 100) if prev_close > 0 else 0
        
        return {
            "symbol": symbol,
            "name": "",  # 通达信API不直接提供名称
            "current_price": current_price,
            "prev_close": prev_close,
            "open": data.get('open', 0),
            "high": data.get('high', 0),
            "low": data.get('low', 0),
            "volume": data.get('vol', 0),
            "turnover": data.get('amount', 0),
            "change": change,
            "change_percent": change_percent,
            "bid_prices": [data.get(f'bid{i}', 0) for i in range(1, 6)],
            "bid_volumes": [data.get(f'bid_vol{i}', 0) for i in range(1, 6)],
            "ask_prices": [data.get(f'ask{i}', 0) for i in range(1, 6)],
            "ask_volumes": [data.get(f'ask_vol{i}', 0) for i in range(1, 6)],
            "timestamp": int(time.time()),
            "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "market": "A股",
            "data_source": "通达信"
        }
    
    def _parse_hk_stock_data(self, data: Dict[str, Any], symbol: str) -> Dict[str, Any]:
        """解析港股实时数据"""
        current_price = data.get('price', 0)
        prev_close = data.get('last_close', 0)
        change = current_price - prev_close
        change_percent = (change / prev_close * 100) if prev_close > 0 else 0
        
        return {
            "symbol": symbol,
            "name": "",  # 通达信API不直接提供名称
            "current_price": current_price,
            "prev_close": prev_close,
            "open": data.get('open', 0),
            "high": data.get('high', 0),
            "low": data.get('low', 0),
            "volume": data.get('vol', 0),
            "turnover": data.get('amount', 0),
            "change": change,
            "change_percent": change_percent,
            "timestamp": int(time.time()),
            "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "market": "港股",
            "data_source": "通达信"
        }


# 全局通达信提供器实例
_tdx_provider = None


def get_tdx_provider() -> TDXProvider:
    """获取通达信提供器实例（单例模式）"""
    global _tdx_provider
    if _tdx_provider is None:
        _tdx_provider = TDXProvider()
    return _tdx_provider


def get_tdx_realtime_data(symbol: str) -> Optional[Dict[str, Any]]:
    """
    通过通达信API获取实时行情数据
    
    Args:
        symbol: 股票代码
        
    Returns:
        实时行情数据字典，如果失败返回None
    """
    provider = get_tdx_provider()
    return provider.get_real_time_data(symbol)


def test_tdx_connection() -> bool:
    """测试通达信连接"""
    provider = get_tdx_provider()
    return provider.connect()


def get_china_market_overview() -> str:
    """
    获取主要指数实时数据
    
    Returns:
        市场概览字符串
    """
    provider = get_tdx_provider()
    if not provider.is_connected() and not provider.connect():
        return "通达信连接失败，无法获取市场概览"
    
    try:
        # 主要指数代码
        indices = [
            ("000001", "上证指数"),
            ("399001", "深证成指"),
            ("399006", "创业板指"),
            ("000688", "科创50")
        ]
        
        overview = []
        for code, name in indices:
            data = provider.get_real_time_data(f"{code}.SH")
            if data:
                overview.append(f"{name}: {data['current_price']} ({data['change_percent']:.2f}%)")
        
        return "\n".join(overview) if overview else "无法获取市场数据"
        
    except Exception as e:
        logger.error(f"获取市场概览失败: {e}")
        return f"获取市场概览失败: {e}"