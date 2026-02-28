"""
tushare数据源 - 无依赖版
用于获取A股数据（模拟数据）
"""

import os
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class TushareSource:
    """tushare数据源类 - 无依赖版"""

    def __init__(self, token: Optional[str] = None):
        """
        初始化tushare数据源

        Args:
            token: tushare token，如果为None则从环境变量读取
        """
        self.token = token or os.getenv("TUSHARE_TOKEN")
        if not self.token:
            logger.warning("未设置TUSHARE_TOKEN环境变量，使用模拟数据")

        logger.info("tushare数据源初始化完成（无依赖版）")

    def get_stock_basic(self, market: str = "A") -> list:
        """
        获取股票基本信息 - 无依赖版

        Args:
            market: 市场类型，A表示A股

        Returns:
            包含股票基本信息的列表
        """
        try:
            logger.info(f"获取{market}股基本信息（模拟数据）")

            # 模拟数据
            data = [
                {
                    'ts_code': '000001.SZ',
                    'symbol': '000001',
                    'name': '平安银行',
                    'area': '深圳',
                    'industry': '银行',
                    'market': '主板',
                    'list_date': '19910403'
                },
                {
                    'ts_code': '000002.SZ',
                    'symbol': '000002',
                    'name': '万科A',
                    'area': '深圳',
                    'industry': '房地产',
                    'market': '主板',
                    'list_date': '19910129'
                },
                {
                    'ts_code': '600519.SH',
                    'symbol': '600519',
                    'name': '贵州茅台',
                    'area': '贵州',
                    'industry': '白酒',
                    'market': '主板',
                    'list_date': '20010827'
                }
            ]

            # 过滤A股
            if market == "A":
                data = [item for item in data if item['ts_code'].endswith(('.SH', '.SZ'))]

            return data
        except Exception as e:
            logger.error(f"获取股票基本信息失败: {e}")
            return []

    def get_valuation_indicators(self, symbol: str) -> Dict[str, Any]:
        """
        获取估值指标 - 无依赖版

        Args:
            symbol: 股票代码

        Returns:
            包含估值指标的字典
        """
        try:
            logger.info(f"获取{symbol}估值指标（模拟数据）")

            # 模拟数据 - 根据股票代码返回不同的估值
            if symbol == "000001":
                indicators = {
                    "pe": 5.5,
                    "pb": 0.6,
                    "ps": 1.2,
                    "dividend_yield": 5.8,
                    "market_cap": 300000000000  # 3000亿
                }
            elif symbol == "000002":
                indicators = {
                    "pe": 8.2,
                    "pb": 1.1,
                    "ps": 2.3,
                    "dividend_yield": 4.5,
                    "market_cap": 200000000000  # 2000亿
                }
            elif symbol == "600519":
                indicators = {
                    "pe": 32.5,
                    "pb": 12.8,
                    "ps": 25.3,
                    "dividend_yield": 1.2,
                    "market_cap": 2500000000000  # 2.5万亿
                }
            else:
                # 默认值
                indicators = {
                    "pe": 15.5,
                    "pb": 2.1,
                    "ps": 3.2,
                    "dividend_yield": 2.8,
                    "market_cap": 10000000000  # 100亿
                }

            return indicators
        except Exception as e:
            logger.error(f"获取估值指标失败: {e}")
            return {}