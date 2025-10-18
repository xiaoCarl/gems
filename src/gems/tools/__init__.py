from typing_extensions import Callable
from typing import Any
from gems.tools.financials import get_income_statements
from gems.tools.financials import get_balance_sheets
from gems.tools.financials import get_cash_flow_statements
from gems.tools.filings import get_filings
from gems.tools.filings import get_10K_filing_items
from gems.tools.filings import get_10Q_filing_items
from gems.tools.filings import get_8K_filing_items

TOOLS: list[Any] = [
    get_income_statements,
    get_balance_sheets,
    get_cash_flow_statements,
    get_10K_filing_items,
    get_10Q_filing_items,
    get_8K_filing_items,
    get_filings,
]
