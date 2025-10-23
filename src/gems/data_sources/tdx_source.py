"""
通达信数据源 - 专门用于获取实时行情数据

使用通达信API作为主要实时数据源，支持A股和港股实时行情。
"""

from typing import Any

from gems.exceptions import DataSourceError
from gems.output.core import get_output_engine
from gems.tools.tdx_api import get_tdx_realtime_data, test_tdx_connection

from .base import DataSource


class TDXDataSource(DataSource):
    """通达信数据源"""

    def __init__(self):
        self.name = "tdx"
        self.description = "通达信实时行情数据源"
        self.output = get_output_engine()
        self._available = None

    def is_available(self) -> bool:
        """检查通达信数据源是否可用"""
        if self._available is None:
            try:
                self._available = test_tdx_connection()
                if self._available:
                    self.output.show_progress("通达信数据源可用")
                else:
                    self.output.show_progress("通达信数据源不可用")
            except Exception as e:
                self.output.show_progress(f"通达信数据源检查失败: {str(e)}")
                self._available = False
        return self._available

    def get_realtime_data(self, symbol: str) -> dict[str, Any]:
        """
        获取股票实时行情数据

        Args:
            symbol: 股票代码 (A股: '000001.SZ', 港股: '00700.HK')

        Returns:
            实时行情数据字典

        Raises:
            DataSourceError: 当获取数据失败时
        """
        try:
            self.output.show_progress(f"通过通达信获取实时数据 - 股票: {symbol}")

            data = get_tdx_realtime_data(symbol)
            if not data:
                raise DataSourceError(f"通达信获取实时数据失败: {symbol}")

            # 验证关键数据
            if data.get("current_price", 0) <= 0:
                raise DataSourceError(
                    f"通达信返回的价格数据无效: {data.get('current_price')}"
                )

            self.output.show_progress(
                f"通达信实时数据获取成功 - 股票: {symbol}, 价格: {data.get('current_price')}, 涨跌幅: {data.get('change_percent')}"
            )

            return data

        except DataSourceError:
            raise
        except Exception as e:
            raise DataSourceError(f"通达信获取实时数据失败: {str(e)}")

    def get_financial_data(self, symbol: str, period: str) -> dict[str, Any]:
        """
        通达信不提供财务数据，抛出异常

        Args:
            symbol: 股票代码
            period: 报告期

        Raises:
            DataSourceError: 通达信不支持财务数据
        """
        raise DataSourceError("通达信数据源不支持财务数据获取")

    def get_historical_data(self, symbol: str, period: str) -> dict[str, Any]:
        """
        通达信不提供历史数据，抛出异常

        Args:
            symbol: 股票代码
            period: 时间周期

        Raises:
            DataSourceError: 通达信不支持历史数据
        """
        raise DataSourceError("通达信数据源不支持历史数据获取")
