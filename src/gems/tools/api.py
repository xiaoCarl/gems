from langchain.tools import tool
from typing import Literal, Optional
from pydantic import BaseModel, Field

####################################
# Tools
####################################

class FinancialStatementsInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol to fetch financial statements for. For Chinese stocks, use format like '000001.SZ' for A-shares.")
    period: Literal["annual", "quarterly"] = Field(description="The reporting period for the financial statements. 'annual' for yearly, 'quarterly' for quarterly. Note: 'ttm' not supported with AkShare.")
    limit: int = Field(default=10, description="The number of past financial statements to retrieve.")
    report_period_gt: Optional[str] = Field(default=None, description="Optional fitler to retrieve financial statements greater than the specified report period.")
    report_period_gte: Optional[str] = Field(default=None, description="Optional fitler to retrieve financial statements greater than or equal to the specified report period.")
    report_period_lt: Optional[str] = Field(default=None, description="Optional fitler to retrieve financial statements less than the specified report period.")
    report_period_lte: Optional[str] = Field(default=None, description="Optional fitler to retrieve financial statements less than or equal to the specified report period.")


@tool(args_schema=FinancialStatementsInput)
def get_income_statements(
    ticker: str,
    period: Literal["annual", "quarterly"],
    limit: int = 10,
    report_period_gt: Optional[str] = None,
    report_period_gte: Optional[str] = None,
    report_period_lt: Optional[str] = None,
    report_period_lte: Optional[str] = None
) -> dict:
    """
    Fetches a company's income statements,
    detailing its revenues, expenses, net income, etc. over a reporting period.
    Useful for evaluating a company's profitability and operational efficiency.

    Now uses AkShare for Chinese stocks. Supports A-share format like '000001.SZ'.
    """
    from gems.api import get_stock_financials
    data = get_stock_financials(ticker, period)
    return {"income_statements": data["income_statements"][:limit]}

@tool(args_schema=FinancialStatementsInput)
def get_balance_sheets(
    ticker: str,
    period: Literal["annual", "quarterly"],
    limit: int = 10,
    report_period_gt: Optional[str] = None,
    report_period_gte: Optional[str] = None,
    report_period_lt: Optional[str] = None,
    report_period_lte: Optional[str] = None
) -> dict:
    """
    Retrieves a company's balance sheets, providing a snapshot of
    its assets, liabilities, shareholders' equity, etc. at a specific point in time.
    Useful for assessing a company's financial position.

    Now uses AkShare for Chinese stocks. Supports A-share format like '000001.SZ'.
    """
    from gems.api import get_stock_financials
    data = get_stock_financials(ticker, period)
    return {"balance_sheets": data["balance_sheets"][:limit]}

@tool(args_schema=FinancialStatementsInput)
def get_cash_flow_statements(
    ticker: str,
    period: Literal["annual", "quarterly"],
    limit: int = 10,
    report_period_gt: Optional[str] = None,
    report_period_gte: Optional[str] = None,
    report_period_lt: Optional[str] = None,
    report_period_lte: Optional[str] = None
) -> dict:
    """
    Retrieves a company's cash flow statements,
    showing how cash is generated and used across
    operating, investing, and financing activities.
    Useful for understanding a company's liquidity and solvency.

    Now uses AkShare for Chinese stocks. Supports A-share format like '000001.SZ'.
    """
    from gems.api import get_stock_financials
    data = get_stock_financials(ticker, period)
    return {"cash_flow_statements": data["cash_flow_statements"][:limit]}


class RealtimeDataInput(BaseModel):
    ticker: str = Field(description="股票代码，A股格式如'000001.SZ'，港股格式如'00700.HK'")


@tool(args_schema=RealtimeDataInput)
def get_realtime_stock_quote(ticker: str) -> dict:
    """
    获取A股或港股最近一个交易日的实时数据。
    
    返回包含以下信息的实时交易数据：
    - 当前价格
    - 涨跌额和涨跌幅
    - 成交量、成交额
    - 最高价、最低价、开盘价
    - 前收盘价
    - 时间戳
    - 市场类型（A股/港股）
    
    支持：
    - A股：格式如'000001.SZ', '600000.SH'
    - 港股：格式如'00700.HK', '00941.HK'
    """
    try:
        from gems.api import get_realtime_stock_data
        realtime_data = get_realtime_stock_data(ticker)
        return {"realtime_quote": realtime_data}
    except Exception as e:
        return {"error": f"获取实时数据失败: {str(e)}"}


class ValuationDataInput(BaseModel):
    ticker: str = Field(description="股票代码，A股格式如'000001.SZ'，港股格式如'00700.HK'")


@tool(args_schema=ValuationDataInput)
def get_stock_valuation(ticker: str) -> dict:
    """
    获取股票最新估值数据，包括PE、PB、股息率等指标。
    
    注意：此工具是获取估值数据的主要工具，直接基于财务数据和实时股价计算。
    不需要调用其他估值分析工具。
    
    返回包含以下估值数据的字典：
    - PE Ratio：市盈率
    - PB Ratio：市净率  
    - Dividend Yield：股息率
    - Market Cap：总市值
    - 数据来源和时间戳
    
    支持：
    - A股：格式如'000001.SZ', '600000.SH'
    - 港股：格式如'00700.HK', '00941.HK'
    """
    try:
        from gems.api import get_stock_valuation_data
        valuation_data = get_stock_valuation_data(ticker)
        return {"stock_valuation": valuation_data}
    except Exception as e:
        return {"error": f"获取估值数据失败: {str(e)}"}