import os
import requests
import akshare as ak

####################################
# API Configuration
####################################

finnhub_api_key = os.getenv("FINNHUB_API_KEY")


def call_api(endpoint: str, params: dict) -> dict:
    """Helper function to call the FinnHub API."""
    base_url = "https://finnhub.io/api/v1"
    url = f"{base_url}{endpoint}"
    # FinnHub uses token parameter instead of headers
    params_with_token = {**params, "token": finnhub_api_key}
    response = requests.get(url, params=params_with_token)
    response.raise_for_status()
    return response.json()


def call_akshare_stock_financials(symbol: str, period: str) -> dict:
    """
    Fetch financial statements for a Chinese stock using AkShare.
    
    Args:
        symbol: Stock symbol (e.g., '000001.SZ')
        period: 'annual' or 'quarter'
    
    Returns:
        Dictionary containing income statements, balance sheets, and cash flow statements
    """
    try:
        # Clean symbol format (remove .SZ/.SH suffix if present)
        clean_symbol = symbol.split('.')[0] if '.' in symbol else symbol
        
        # Fetch income statements (利润表)
        income_df = ak.stock_financial_report_sina(stock=clean_symbol, symbol="利润表")
        
        # Fetch balance sheets (资产负债表)
        balance_df = ak.stock_financial_report_sina(stock=clean_symbol, symbol="资产负债表")
        
        # Fetch cash flow statements (现金流量表)
        cash_flow_df = ak.stock_financial_report_sina(stock=clean_symbol, symbol="现金流量表")
        
        # Convert DataFrames to dictionaries
        income_statements = income_df.to_dict('records')
        balance_sheets = balance_df.to_dict('records')
        cash_flow_statements = cash_flow_df.to_dict('records')
        
        return {
            "income_statements": income_statements,
            "balance_sheets": balance_sheets,
            "cash_flow_statements": cash_flow_statements
        }
        
    except Exception as e:
        raise ValueError(f"Failed to fetch data from AkShare: {e}")

