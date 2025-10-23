from collections.abc import Callable
from typing import Any

# 导入分析工具
from .analysis import (
    analyze_moat_characteristics,
    assess_business_simplicity,
    calculate_free_cash_flow_metrics,
    compute_valuation_ratios,
    evaluate_management_quality,
)

# 导入财务工具
from .api import (
    get_balance_sheets,
    get_cash_flow_statements,
    get_income_statements,
    get_realtime_stock_quote,
    get_stock_valuation,
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
