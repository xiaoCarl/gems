"""
重构后的API模块测试
"""

import os
import sys
from unittest.mock import Mock, patch

import pytest

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from gems.api import (
    _build_valuation_result,
    _calculate_dividend_yield,
    _calculate_valuation_metrics,
    _extract_net_profit,
    _extract_total_equity,
    _extract_total_shares,
    _find_latest_annual_data,
    _get_and_validate_financial_data,
    _get_current_price,
    _validate_financial_metrics,
    _validate_valuation_results,
    get_stock_valuation_data,
)
from gems.exceptions import FinancialDataError


class TestAPIRefactored:
    """重构后API模块的单元测试"""

    @pytest.fixture
    def mock_output(self):
        """模拟输出引擎"""
        output = Mock()
        output.show_progress = Mock()
        return output

    @pytest.fixture
    def sample_financial_data(self):
        """示例财务数据"""
        return {
            "income_statements": [
                {
                    "报告日": "20231231",
                    "归属于母公司所有者的净利润": 1000000000.0,
                    "净利润": 1000000000.0,
                }
            ],
            "balance_sheets": [
                {
                    "报告日": "20231231",
                    "归属于母公司股东权益合计": 5000000000.0,
                    "实收资本(或股本)": 100000000.0,
                }
            ],
            "cash_flow_statements": [
                {
                    "报告日": "20231231",
                    "分配股利、利润或偿付利息所支付的现金": 200000000.0,
                }
            ],
        }

    def test_find_latest_annual_data(self):
        """测试查找最新年度数据"""
        statements = [
            {"报告日": "20230630"},
            {"报告日": "20231231"},
            {"报告日": "20220630"},
        ]

        result = _find_latest_annual_data(statements)
        assert result["报告日"] == "20231231"

    def test_find_latest_annual_data_no_annual(self):
        """测试没有年度数据时返回None"""
        statements = [{"报告日": "20230630"}, {"报告日": "20220630"}]

        result = _find_latest_annual_data(statements)
        assert result is None

    def test_extract_net_profit(self):
        """测试提取净利润"""
        income_statement = {"归属于母公司所有者的净利润": 1000000.0, "净利润": 900000.0}

        result = _extract_net_profit(income_statement)
        assert result == 1000000.0

    def test_extract_net_profit_fallback(self):
        """测试净利润回退提取"""
        income_statement = {"净利润": 900000.0}

        result = _extract_net_profit(income_statement)
        assert result == 900000.0

    def test_extract_total_equity(self):
        """测试提取股东权益"""
        balance_sheet = {
            "归属于母公司股东权益合计": 5000000.0,
            "归属于母公司股东的权益": 4500000.0,
            "股东权益合计": 4000000.0,
            "所有者权益合计": 3500000.0,
        }

        result = _extract_total_equity(balance_sheet)
        assert result == 5000000.0

    def test_extract_total_shares(self):
        """测试提取总股本"""
        balance_sheet = {
            "实收资本(或股本)": 1000000.0,
            "股本": 900000.0,
            "实收资本": 800000.0,
        }

        result = _extract_total_shares(balance_sheet)
        assert result == 1000000.0

    def test_validate_financial_metrics_valid(self):
        """测试验证有效的财务指标"""
        # 应该不会抛出异常
        _validate_financial_metrics(1000000.0, 5000000.0, 1000000.0)

    def test_validate_financial_metrics_invalid_net_profit(self):
        """测试验证无效的净利润"""
        with pytest.raises(FinancialDataError, match="净利润数据无效"):
            _validate_financial_metrics(0.0, 5000000.0, 1000000.0)

    def test_validate_financial_metrics_invalid_total_equity(self):
        """测试验证无效的股东权益"""
        with pytest.raises(FinancialDataError, match="股东权益数据无效"):
            _validate_financial_metrics(1000000.0, 0.0, 1000000.0)

    def test_validate_financial_metrics_invalid_total_shares(self):
        """测试验证无效的总股本"""
        with pytest.raises(FinancialDataError, match="总股本数据无效"):
            _validate_financial_metrics(1000000.0, 5000000.0, 0.0)

    def test_calculate_valuation_metrics(self):
        """测试计算估值指标"""
        financial_metrics = {
            "net_profit": 1000000.0,
            "total_equity": 5000000.0,
            "total_shares": 1000000.0,
        }
        current_price = 10.0

        result = _calculate_valuation_metrics(financial_metrics, current_price, Mock())

        assert result["eps"] == 1.0
        assert result["bvps"] == 5.0
        assert result["pe_ratio"] == 10.0
        assert result["pb_ratio"] == 2.0
        assert result["roe"] == 20.0

    def test_validate_valuation_results_valid(self):
        """测试验证有效的估值结果"""
        valuation_metrics = {"pe_ratio": 15.0, "pb_ratio": 2.0}

        # 应该不会抛出异常
        _validate_valuation_results(valuation_metrics)

    def test_validate_valuation_results_invalid(self):
        """测试验证无效的估值结果"""
        valuation_metrics = {"pe_ratio": 0.0, "pb_ratio": 2.0}

        with pytest.raises(FinancialDataError, match="估值计算结果异常"):
            _validate_valuation_results(valuation_metrics)

    def test_build_valuation_result(self):
        """测试构建估值结果"""
        symbol = "600519.SH"
        current_price = 1600.0
        financial_metrics = {
            "net_profit": 1000000000.0,
            "total_equity": 5000000000.0,
            "total_shares": 100000000.0,
        }
        valuation_metrics = {
            "pe_ratio": 16.0,
            "pb_ratio": 3.2,
            "roe": 20.0,
            "eps": 10.0,
            "bvps": 50.0,
        }
        dividend_yield = 1.5

        result = _build_valuation_result(
            symbol, current_price, financial_metrics, valuation_metrics, dividend_yield
        )

        assert result["symbol"] == symbol
        assert result["market"] == "A股"
        assert result["current_price"] == 1600.0
        assert result["pe_ratio"] == 16.0
        assert result["pb_ratio"] == 3.2
        assert result["roe"] == 20.0
        assert result["eps"] == 10.0
        assert result["bvps"] == 50.0
        assert result["dividend_yield"] == 1.5

    @patch("gems.api.get_stock_financials")
    def test_get_and_validate_financial_data_valid(
        self, mock_get_financials, sample_financial_data
    ):
        """测试获取和验证有效的财务数据"""
        mock_get_financials.return_value = sample_financial_data

        result = _get_and_validate_financial_data("600519.SH", Mock())

        assert result == sample_financial_data

    @patch("gems.api.get_stock_financials")
    def test_get_and_validate_financial_data_empty(self, mock_get_financials):
        """测试获取空财务数据时抛出异常"""
        mock_get_financials.return_value = {
            "income_statements": [],
            "balance_sheets": [],
        }

        with pytest.raises(FinancialDataError, match="财务数据为空"):
            _get_and_validate_financial_data("600519.SH", Mock())

    @patch("gems.api.get_realtime_stock_data")
    def test_get_current_price_success(self, mock_get_realtime):
        """测试成功获取当前股价"""
        mock_get_realtime.return_value = {"current_price": 100.0, "prev_close": 95.0}

        result = _get_current_price("600519.SH", Mock())

        assert result == 100.0

    @patch("gems.api.get_realtime_stock_data")
    def test_get_current_price_fallback_to_prev_close(self, mock_get_realtime):
        """测试回退到前收盘价"""
        mock_get_realtime.return_value = {"current_price": 0.0, "prev_close": 95.0}

        result = _get_current_price("600519.SH", Mock())

        assert result == 95.0

    @patch("gems.api.get_realtime_stock_data")
    def test_get_current_price_fallback_to_typical(self, mock_get_realtime):
        """测试回退到典型价格"""
        mock_get_realtime.side_effect = Exception("API错误")

        result = _get_current_price("600519.SH", Mock())

        assert result == 1600.0  # 贵州茅台的典型价格

    def test_calculate_dividend_yield_success(self, sample_financial_data):
        """测试成功计算股息率"""
        total_shares = 100000000.0
        current_price = 1600.0

        result = _calculate_dividend_yield(
            sample_financial_data, total_shares, current_price, Mock()
        )

        # 200000000 / 100000000 = 2.0, 2.0 / 1600.0 * 100 = 0.125
        assert result == 0.125

    def test_calculate_dividend_yield_no_dividends(self, sample_financial_data):
        """测试没有分红时股息率为0"""
        sample_financial_data["cash_flow_statements"][0][
            "分配股利、利润或偿付利息所支付的现金"
        ] = 0
        total_shares = 100000000.0
        current_price = 1600.0

        result = _calculate_dividend_yield(
            sample_financial_data, total_shares, current_price, Mock()
        )

        assert result == 0.0

    @patch("gems.api._get_and_validate_financial_data")
    @patch("gems.api._extract_financial_metrics")
    @patch("gems.api._get_current_price")
    @patch("gems.api._calculate_valuation_metrics")
    @patch("gems.api._calculate_dividend_yield")
    @patch("gems.api._validate_valuation_results")
    @patch("gems.api._build_valuation_result")
    def test_get_stock_valuation_data_integration(
        self,
        mock_build,
        mock_validate,
        mock_dividend,
        mock_valuation,
        mock_price,
        mock_metrics,
        mock_financial,
    ):
        """测试完整的估值数据获取流程"""
        # 设置模拟返回值
        mock_financial.return_value = {"test": "financial_data"}
        mock_metrics.return_value = {
            "net_profit": 1000000.0,
            "total_equity": 5000000.0,
            "total_shares": 1000000.0,
        }
        mock_price.return_value = 10.0
        mock_valuation.return_value = {
            "pe_ratio": 10.0,
            "pb_ratio": 2.0,
            "roe": 20.0,
            "eps": 1.0,
            "bvps": 5.0,
        }
        mock_dividend.return_value = 1.5
        mock_build.return_value = {"symbol": "600519.SH", "pe_ratio": 10.0}

        result = get_stock_valuation_data("600519.SH")

        # 验证所有步骤都被调用
        mock_financial.assert_called_once()
        mock_metrics.assert_called_once()
        mock_price.assert_called_once()
        mock_valuation.assert_called_once()
        mock_dividend.assert_called_once()
        mock_validate.assert_called_once()
        mock_build.assert_called_once()

        assert result["symbol"] == "600519.SH"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
