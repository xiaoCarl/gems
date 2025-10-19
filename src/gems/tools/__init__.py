from typing_extensions import Callable
from typing import Any
from gems.tools.financials import get_income_statements
from gems.tools.financials import get_balance_sheets
from gems.tools.financials import get_cash_flow_statements
from gems.tools.financials import get_realtime_stock_quote
from gems.tools.financials import get_stock_valuation

# 导入分析工具
from gems.tools.analysis import (
    analyze_moat_characteristics,
    evaluate_management_quality,
    calculate_free_cash_flow_metrics,
    compute_valuation_ratios,
    assess_business_simplicity
)

TOOLS: list[Any] = [
    get_income_statements,
    get_balance_sheets,
    get_cash_flow_statements,
    get_realtime_stock_quote,
    get_stock_valuation,
    analyze_moat_characteristics,
    evaluate_management_quality,
    calculate_free_cash_flow_metrics,
    compute_valuation_ratios,
    assess_business_simplicity,
]