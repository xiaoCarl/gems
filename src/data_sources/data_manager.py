"""
数据管理器 - 无依赖版
统一管理A股和港股数据源
"""

import os
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from .tushare_source import TushareSource
from .akshare_source import AkshareSource

logger = logging.getLogger(__name__)


class DataManager:
    """数据管理器类 - 无依赖版"""

    def __init__(self, tushare_token: Optional[str] = None):
        """
        初始化数据管理器

        Args:
            tushare_token: tushare token
        """
        self.tushare_source = TushareSource(tushare_token)
        self.akshare_source = AkshareSource()

        logger.info("数据管理器初始化完成（无依赖版）")

    def get_stock_basic(self, market: str = "A") -> list:
        """
        获取股票基本信息

        Args:
            market: 市场类型，A表示A股，HK表示港股

        Returns:
            包含股票基本信息的列表
        """
        try:
            if market == "A":
                return self.tushare_source.get_stock_basic(market)
            elif market == "HK":
                return self.akshare_source.get_hk_stock_basic()
            else:
                raise ValueError(f"不支持的市场类型: {market}")
        except Exception as e:
            logger.error(f"获取股票基本信息失败: {e}")
            return []

    def get_valuation_indicators(self, symbol: str, market: str) -> Dict[str, Any]:
        """
        获取估值指标

        Args:
            symbol: 股票代码
            market: 市场类型，A表示A股，HK表示港股

        Returns:
            包含估值指标的字典
        """
        try:
            if market == "A":
                return self.tushare_source.get_valuation_indicators(symbol)
            elif market == "HK":
                return self.akshare_source.get_hk_valuation_indicators(symbol)
            else:
                raise ValueError(f"不支持的市场类型: {market}")
        except Exception as e:
            logger.error(f"获取估值指标失败: {e}")
            return {}

    def get_stock_info(self, symbol: str, market: str) -> Dict[str, Any]:
        """
        获取股票综合信息 - 无依赖版

        Args:
            symbol: 股票代码
            market: 市场类型，A表示A股，HK表示港股

        Returns:
            包含股票综合信息的字典
        """
        try:
            logger.info(f"获取股票综合信息: {symbol} ({market}) - 无依赖版")

            # 获取基本信息
            basic_info = self._get_basic_info(symbol, market)

            # 获取估值指标
            valuation = self.get_valuation_indicators(symbol, market)

            # 组合所有信息
            stock_info = {
                "symbol": symbol,
                "market": market,
                "basic_info": basic_info,
                "valuation": valuation,
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            return stock_info
        except Exception as e:
            logger.error(f"获取股票综合信息失败: {e}")
            return {}

    def _get_basic_info(self, symbol: str, market: str) -> Dict[str, Any]:
        """获取基本信息 - 无依赖版"""
        try:
            if market == "A":
                # 获取A股基本信息
                basic_data = self.tushare_source.get_stock_basic("A")
                if not basic_data:
                    return {}

                # 查找指定股票
                if symbol.endswith(('.SH', '.SZ')):
                    search_symbol = symbol
                else:
                    if symbol.startswith('6'):
                        search_symbol = f"{symbol}.SH"
                    else:
                        search_symbol = f"{symbol}.SZ"

                for item in basic_data:
                    if item.get("ts_code") == search_symbol:
                        return {
                            "name": item.get("name", f"股票{symbol}"),
                            "industry": item.get("industry", "未知"),
                            "area": item.get("area", "中国"),
                            "market": item.get("market", "A"),
                            "list_date": item.get("list_date", "20000101")
                        }

                # 如果没有找到，返回默认信息
                return {
                    "name": f"股票{symbol}",
                    "industry": "未知",
                    "area": "中国",
                    "market": "A",
                    "list_date": "20000101"
                }
            elif market == "HK":
                # 获取港股基本信息
                basic_data = self.akshare_source.get_hk_stock_basic()
                if not basic_data:
                    return {}

                # 查找指定股票
                for item in basic_data:
                    if item.get("代码") == symbol:
                        return {
                            "name": item.get("名称", f"港股{symbol}"),
                            "industry": "未知",
                            "area": "香港",
                            "market": "HK",
                            "list_date": ""
                        }

                # 如果没有找到，返回默认信息
                return {
                    "name": f"港股{symbol}",
                    "industry": "未知",
                    "area": "香港",
                    "market": "HK",
                    "list_date": ""
                }
            else:
                return {}
        except Exception as e:
            logger.error(f"获取基本信息失败: {e}")
            return {}