"""
统一API接口模块
"""

from typing import Any

from gems.config import config
from gems.data_sources.manager import data_source_manager
from gems.exceptions import FinancialDataError
from gems.output.core import get_output_engine


def get_realtime_stock_data(
    symbol: str, data_source: str | None = None
) -> dict[str, Any]:
    """
    获取A股和港股实时数据

    Args:
        symbol: 股票代码
            A股格式: '000001.SZ', '600000.SH'
            港股格式: '00700.HK', '00941.HK'
        data_source: 数据源，'tdx' 或 'akshare'，默认使用配置的优先数据源

    Returns:
        包含实时交易数据的字典
    """
    return data_source_manager.get_realtime_data(symbol, data_source)


def get_stock_financials(symbol: str, period: str) -> dict[str, Any]:
    """
    获取股票财务数据

    Args:
        symbol: 股票代码 (e.g., '000001.SZ' for A-shares, '00700.HK' for H-shares)
        period: 'annual' or 'quarter'

    Returns:
        包含利润表、资产负债表、现金流量表的字典
    """
    return data_source_manager.get_financial_data(symbol, period)


def get_stock_valuation_data(symbol: str) -> dict[str, Any]:
    """
    获取股票估值数据，基于财务数据和实时股价计算估值指标

    Args:
        symbol: 股票代码 (A股: '000001.SZ', 港股: '00700.HK')

    Returns:
        包含PE、PB等估值指标的字典
    """
    output = get_output_engine()

    try:
        # 1. 获取并验证财务数据
        financial_data = _get_and_validate_financial_data(symbol, output)

        # 2. 提取关键财务指标
        financial_metrics = _extract_financial_metrics(financial_data, output)

        # 3. 获取当前股价
        current_price = _get_current_price(symbol, output)

        # 4. 计算估值指标
        valuation_metrics = _calculate_valuation_metrics(
            financial_metrics, current_price, output
        )

        # 5. 计算股息率
        dividend_yield = _calculate_dividend_yield(
            financial_data, financial_metrics["total_shares"], current_price, output
        )

        # 6. 验证计算结果
        _validate_valuation_results(valuation_metrics)

        # 7. 返回完整结果
        return _build_valuation_result(
            symbol, current_price, financial_metrics, valuation_metrics, dividend_yield
        )

    except Exception as e:
        raise FinancialDataError(f"获取估值数据失败: {e}")


def _get_and_validate_financial_data(symbol: str, output) -> dict[str, Any]:
    """获取并验证财务数据"""
    financial_data = get_stock_financials(symbol, "annual")

    if not financial_data["income_statements"] or not financial_data["balance_sheets"]:
        raise FinancialDataError("财务数据为空，无法计算估值")

    return financial_data


def _extract_financial_metrics(
    financial_data: dict[str, Any], output
) -> dict[str, float]:
    """从财务数据中提取关键指标"""
    # 查找最新的年度数据
    latest_income = _find_latest_annual_data(financial_data["income_statements"])
    latest_balance = _find_latest_annual_data(financial_data["balance_sheets"])

    # 如果没有找到年度数据，使用最新数据
    if not latest_income:
        latest_income = financial_data["income_statements"][0]
    if not latest_balance:
        latest_balance = financial_data["balance_sheets"][0]

    output.show_progress(
        f"使用财务报告数据 - 利润表: {latest_income.get('报告日', '未知')}, "
        f"资产负债表: {latest_balance.get('报告日', '未知')}"
    )

    # 提取关键财务指标
    net_profit = _extract_net_profit(latest_income)
    total_equity = _extract_total_equity(latest_balance)
    total_shares = _extract_total_shares(latest_balance)

    # 验证关键数据
    _validate_financial_metrics(net_profit, total_equity, total_shares)

    return {
        "net_profit": net_profit,
        "total_equity": total_equity,
        "total_shares": total_shares,
    }


def _find_latest_annual_data(statements: list[dict]) -> dict | None:
    """查找最新的年度数据（12月31日）"""
    for statement in statements:
        report_date = statement.get("报告日", "")
        # 港股数据格式
        if "REPORT_DATE" in statement:
            report_date = statement.get("REPORT_DATE", "")

        # A股格式: 20241231, 港股格式: 2024-12-31 00:00:00
        if report_date and (report_date.endswith("1231") or "12-31" in report_date):  # 年度报告
            return statement
    return None


def _extract_net_profit(income_statement: dict[str, Any]) -> float:
    """从利润表中提取净利润"""
    # 港股数据格式
    if "HOLDER_PROFIT" in income_statement:
        return income_statement.get("HOLDER_PROFIT", 0)
    # A股数据格式
    return income_statement.get(
        "归属于母公司所有者的净利润", 0
    ) or income_statement.get("净利润", 0)


def _extract_total_equity(balance_sheet: dict[str, Any]) -> float:
    """从资产负债表中提取股东权益"""
    # 港股数据格式 - 通过每股净资产和已发行股本计算
    if "每股净资产(元)" in balance_sheet and "已发行股本(股)" in balance_sheet:
        bvps = balance_sheet.get("每股净资产(元)", 0)
        shares = balance_sheet.get("已发行股本(股)", 0)
        if bvps > 0 and shares > 0:
            return bvps * shares

    # A股数据格式
    return (
        balance_sheet.get("归属于母公司股东权益合计", 0)
        or balance_sheet.get("归属于母公司股东的权益", 0)
        or balance_sheet.get("股东权益合计", 0)
        or balance_sheet.get("所有者权益合计", 0)
    )


def _extract_total_shares(balance_sheet: dict[str, Any]) -> float:
    """从资产负债表中提取总股本"""
    # 港股数据格式
    if "已发行股本(股)" in balance_sheet:
        return balance_sheet.get("已发行股本(股)", 0)
    # A股数据格式
    return (
        balance_sheet.get("实收资本(或股本)", 0)
        or balance_sheet.get("股本", 0)
        or balance_sheet.get("实收资本", 0)
    )


def _validate_financial_metrics(
    net_profit: float, total_equity: float, total_shares: float
):
    """验证财务指标有效性"""
    if net_profit <= 0:
        raise FinancialDataError(f"净利润数据无效: {net_profit}")
    if total_equity <= 0:
        raise FinancialDataError(f"股东权益数据无效: {total_equity}")
    if total_shares <= 0:
        raise FinancialDataError(f"总股本数据无效: {total_shares}")


def _get_current_price(symbol: str, output) -> float:
    """获取当前股价，包含降级策略"""
    try:
        realtime_data = get_realtime_stock_data(symbol)
        current_price = realtime_data.get("current_price", 0.0)

        if current_price <= 0:
            current_price = realtime_data.get("prev_close", 0.0)
            if current_price <= 0:
                raise FinancialDataError("实时股价和前收盘价都无效")
            output.show_progress(f"使用前收盘价: {current_price}")
        else:
            output.show_progress(f"使用实时股价: {current_price}")

        return current_price

    except Exception as e:
        output.show_progress(f"获取实时股价失败: {str(e)}")
        return _get_fallback_price(symbol, output)


def _get_fallback_price(symbol: str, output) -> float:
    """获取降级价格（典型价格）"""
    current_price = config.get_typical_price(symbol)
    output.show_progress(f"使用典型价格进行计算: {current_price}")
    return current_price


def _calculate_valuation_metrics(
    financial_metrics: dict[str, float], current_price: float, output
) -> dict[str, float]:
    """计算估值指标"""
    net_profit = financial_metrics["net_profit"]
    total_equity = financial_metrics["total_equity"]
    total_shares = financial_metrics["total_shares"]

    eps = net_profit / total_shares
    bvps = total_equity / total_shares

    pe_ratio = current_price / eps if eps > 0 else 0
    pb_ratio = current_price / bvps if bvps > 0 else 0
    roe = (net_profit / total_equity) * 100

    return {
        "pe_ratio": pe_ratio,
        "pb_ratio": pb_ratio,
        "roe": roe,
        "eps": eps,
        "bvps": bvps,
    }


def _calculate_dividend_yield(
    financial_data: dict[str, Any], total_shares: float, current_price: float, output
) -> float:
    """计算股息率"""
    try:
        latest_cash_flow = _find_latest_annual_data(
            financial_data["cash_flow_statements"]
        )

        if not latest_cash_flow:
            latest_cash_flow = financial_data["cash_flow_statements"][0]

        dividends_paid = latest_cash_flow.get("分配股利、利润或偿付利息所支付的现金", 0)

        if dividends_paid > 0 and total_shares > 0:
            dividend_per_share = dividends_paid / total_shares
            dividend_yield = (dividend_per_share / current_price) * 100
            return dividend_yield

        return 0.0

    except Exception as e:
        output.show_progress(f"计算股息率失败: {str(e)}")
        return 0.0


def _validate_valuation_results(valuation_metrics: dict[str, float]):
    """验证估值计算结果"""
    pe_ratio = valuation_metrics["pe_ratio"]
    pb_ratio = valuation_metrics["pb_ratio"]

    if pe_ratio <= 0 or pb_ratio <= 0:
        raise FinancialDataError(f"估值计算结果异常: PE={pe_ratio}, PB={pb_ratio}")


def _build_valuation_result(
    symbol: str,
    current_price: float,
    financial_metrics: dict[str, float],
    valuation_metrics: dict[str, float],
    dividend_yield: float,
) -> dict[str, Any]:
    """构建完整的估值结果"""
    return {
        "symbol": symbol,
        "market": "A股" if symbol.endswith((".SZ", ".SH")) else "港股",
        "current_price": round(current_price, 2),
        "pe_ratio": round(valuation_metrics["pe_ratio"], 2),
        "pb_ratio": round(valuation_metrics["pb_ratio"], 2),
        "roe": round(valuation_metrics["roe"], 2),
        "eps": round(valuation_metrics["eps"], 4),
        "bvps": round(valuation_metrics["bvps"], 4),
        "dividend_yield": round(dividend_yield, 2),
        "net_profit": financial_metrics["net_profit"],
        "total_equity": financial_metrics["total_equity"],
        "total_shares": financial_metrics["total_shares"],
        "data_source": "AkShare财务数据 + 实时股价",
        "calculation_method": "基于财务数据和实时股价计算",
        "calculation_details": {
            "pe_formula": "PE = 当前股价 / 每股收益(EPS)",
            "pb_formula": "PB = 当前股价 / 每股净资产(BVPS)",
            "eps_formula": "EPS = 净利润 / 总股本",
            "bvps_formula": "BVPS = 归属于母公司股东的权益 / 总股本",
            "dividend_yield_formula": "股息率 = (每股分红 / 当前股价) × 100%",
        },
    }
