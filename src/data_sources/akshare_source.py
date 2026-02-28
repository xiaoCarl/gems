"""
akshare数据源 - 无依赖版
用于获取港股数据（模拟数据）
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class AkshareSource:
    """akshare数据源类 - 无依赖版"""

    def __init__(self):
        """初始化akshare数据源"""
        logger.info("akshare数据源初始化完成（无依赖版）")

    def get_hk_stock_basic(self) -> list:
        """
        获取港股基本信息 - 无依赖版

        Returns:
            包含港股基本信息的列表
        """
        try:
            logger.info("获取港股基本信息（模拟数据）")

            # 模拟数据
            data = [
                {
                    '代码': '00700',
                    '名称': '腾讯控股',
                    '最新价': 350.5,
                    '涨跌额': 2.5,
                    '涨跌幅': 0.72,
                    '成交量': 1000000,
                    '成交额': 350500000,
                    '振幅': 1.5,
                    '最高': 352.0,
                    '最低': 348.0,
                    '今开': 349.0,
                    '昨收': 348.0,
                    '市盈率-动态': 25.5,
                    '市净率': 6.8,
                    '总市值': 3500000000000,
                    '流通市值': 2800000000000
                },
                {
                    '代码': '00939',
                    '名称': '建设银行',
                    '最新价': 5.2,
                    '涨跌额': 0.1,
                    '涨跌幅': 1.96,
                    '成交量': 5000000,
                    '成交额': 26000000,
                    '振幅': 0.8,
                    '最高': 5.25,
                    '最低': 5.15,
                    '今开': 5.18,
                    '昨收': 5.1,
                    '市盈率-动态': 4.2,
                    '市净率': 0.6,
                    '总市值': 1500000000000,
                    '流通市值': 1200000000000
                },
                {
                    '代码': '01398',
                    '名称': '工商银行',
                    '最新价': 3.9,
                    '涨跌额': -0.05,
                    '涨跌幅': -1.27,
                    '成交量': 8000000,
                    '成交额': 31200000,
                    '振幅': 0.6,
                    '最高': 3.95,
                    '最低': 3.85,
                    '今开': 3.92,
                    '昨收': 3.95,
                    '市盈率-动态': 3.8,
                    '市净率': 0.5,
                    '总市值': 1800000000000,
                    '流通市值': 1440000000000
                }
            ]

            return data
        except Exception as e:
            logger.error(f"获取港股基本信息失败: {e}")
            return []

    def get_hk_valuation_indicators(self, symbol: str) -> Dict[str, Any]:
        """
        获取港股估值指标 - 无依赖版

        Args:
            symbol: 港股代码

        Returns:
            包含估值指标的字典
        """
        try:
            logger.info(f"获取港股{symbol}估值指标（模拟数据）")

            # 模拟数据 - 根据股票代码返回不同的估值
            if symbol == "00700":
                indicators = {
                    "pe": 25.5,
                    "pb": 6.8,
                    "ps": 8.2,
                    "dividend_yield": 0.8,
                    "market_cap": 3500000000000  # 3.5万亿
                }
            elif symbol == "00939":
                indicators = {
                    "pe": 4.2,
                    "pb": 0.6,
                    "ps": 1.5,
                    "dividend_yield": 6.5,
                    "market_cap": 1500000000000  # 1.5万亿
                }
            elif symbol == "01398":
                indicators = {
                    "pe": 3.8,
                    "pb": 0.5,
                    "ps": 1.3,
                    "dividend_yield": 7.2,
                    "market_cap": 1800000000000  # 1.8万亿
                }
            else:
                # 默认值
                indicators = {
                    "pe": 15.0,
                    "pb": 2.5,
                    "ps": 4.0,
                    "dividend_yield": 3.0,
                    "market_cap": 50000000000  # 500亿
                }

            return indicators
        except Exception as e:
            logger.error(f"获取港股估值指标失败: {e}")
            return {}