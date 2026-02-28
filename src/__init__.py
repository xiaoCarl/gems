"""
Gems - A股和港股价值投资分析工具
简化版，无需外部依赖
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .data_sources import DataManager
from .analysis import ValueInvestingAnalyzer, AnalysisResult, Recommendation
from .utils import setup_logger

__all__ = [
    "DataManager",
    "ValueInvestingAnalyzer",
    "AnalysisResult",
    "Recommendation",
    "setup_logger"
]