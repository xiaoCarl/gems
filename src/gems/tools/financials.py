from langchain.tools import tool
from typing import Literal, Optional
from pydantic import BaseModel, Field
from gems.tools.api import call_api, call_akshare_stock_financials

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


def _create_params(
    symbol: str,
    freq: Literal["annual", "quarterly"],
    statement: str,
    limit: int = 10
) -> dict:
    """Helper function to create params dict for FinnHub API calls."""
    params = {"symbol": symbol, "freq": freq, "statement": statement}
    return params

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
    data = call_akshare_stock_financials(ticker, period)
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
    data = call_akshare_stock_financials(ticker, period)
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
    data = call_akshare_stock_financials(ticker, period)
    return {"cash_flow_statements": data["cash_flow_statements"][:limit]}
