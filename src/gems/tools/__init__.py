from typing_extensions import Callable
from typing import Any

# 导入财务工具
from .api import (
    get_income_statements,
    get_balance_sheets,
    get_cash_flow_statements,
    get_realtime_stock_quote,
    get_stock_valuation
)

# 导入分析工具
from .analysis import (
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