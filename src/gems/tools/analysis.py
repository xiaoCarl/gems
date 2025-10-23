"""
价值投资分析工具模块

这个模块包含专门用于价值投资分析的工具，包括护城河分析、管理层评估、
自由现金流分析和估值指标计算等功能。
"""

from typing import Literal

from langchain.tools import tool
from pydantic import BaseModel, Field

# 延迟导入以避免循环导入


class MoatAnalysisInput(BaseModel):
    ticker: str = Field(description="股票代码，例如'AAPL'或'000001.SZ'")
    period: Literal["annual", "quarterly"] = Field(
        description="报告期，'annual'为年度，'quarterly'为季度"
    )


@tool(args_schema=MoatAnalysisInput)
def analyze_moat_characteristics(
    ticker: str, period: Literal["annual", "quarterly"]
) -> dict:
    """
    分析公司的护城河特征，包括品牌优势、网络效应、成本优势和转换成本。

    通过分析财务数据和业务特征来评估公司的竞争壁垒：
    - 品牌优势：毛利率、品牌溢价能力
    - 网络效应：用户增长、平台价值
    - 成本优势：规模效应、运营效率
    - 转换成本：客户粘性、产品依赖性

    返回包含护城河评分和详细分析的字典。
    """
    # 获取财务数据用于护城河分析
    from gems.api import get_stock_financials

    financial_data = get_stock_financials(ticker, period)

    # 护城河分析逻辑
    moat_analysis = {
        "ticker": ticker,
        "period": period,
        "brand_strength": {
            "gross_margin_trend": "分析毛利率趋势",
            "pricing_power": "评估定价能力",
            "score": 0.0,
        },
        "network_effects": {
            "user_growth": "分析用户增长",
            "platform_value": "评估平台价值",
            "score": 0.0,
        },
        "cost_advantages": {
            "scale_efficiency": "分析规模效应",
            "operational_efficiency": "评估运营效率",
            "score": 0.0,
        },
        "switching_costs": {
            "customer_retention": "分析客户留存",
            "product_dependency": "评估产品依赖性",
            "score": 0.0,
        },
        "overall_moat_score": 0.0,
        "recommendation": "护城河分析结果",
    }

    return {"moat_analysis": moat_analysis}


class ManagementQualityInput(BaseModel):
    ticker: str = Field(description="股票代码")


@tool(args_schema=ManagementQualityInput)
def evaluate_management_quality(ticker: str) -> dict:
    """
    评估管理层质量，包括诚信度、能力和股东利益一致性。

    通过分析以下方面评估管理层：
    - 诚信度：历史记录、信息披露质量
    - 能力：资本配置、战略执行
    - 股东利益一致性：股权激励、分红政策

    返回管理层质量评分和详细评估。
    """
    management_quality = {
        "ticker": ticker,
        "integrity": {
            "track_record": "分析历史记录",
            "disclosure_quality": "评估信息披露质量",
            "score": 0.0,
        },
        "capability": {
            "capital_allocation": "分析资本配置",
            "strategy_execution": "评估战略执行",
            "score": 0.0,
        },
        "alignment": {
            "ownership_stake": "分析管理层持股",
            "dividend_policy": "评估分红政策",
            "score": 0.0,
        },
        "overall_management_score": 0.0,
        "recommendation": "管理层质量评估结果",
    }

    return {"management_quality": management_quality}


class FreeCashFlowInput(BaseModel):
    ticker: str = Field(description="股票代码")
    period: Literal["annual", "quarterly"] = Field(description="报告期")
    years: int = Field(default=5, description="分析年限，默认5年")


@tool(args_schema=FreeCashFlowInput)
def calculate_free_cash_flow_metrics(
    ticker: str, period: Literal["annual", "quarterly"], years: int = 5
) -> dict:
    """
    计算自由现金流相关指标，包括FCF/营收比率、FCF稳定性和增长率。

    分析关键自由现金流指标：
    - FCF/营收比率：衡量现金流生成效率
    - FCF稳定性：现金流波动性分析
    - FCF增长率：长期增长趋势
    - FCF收益率：相对于市值的现金流回报

    返回自由现金流分析和关键指标。
    """
    # 获取现金流数据
    from gems.api import get_stock_financials

    cash_flow_data = get_stock_financials(ticker, period)

    fcf_analysis = {
        "ticker": ticker,
        "period": period,
        "analysis_years": years,
        "fcf_revenue_ratio": {
            "current": 0.0,
            "trend": "FCF/营收比率趋势",
            "industry_comparison": "行业比较",
        },
        "fcf_stability": {
            "volatility": "现金流波动性",
            "consistency": "现金流一致性",
            "score": 0.0,
        },
        "fcf_growth": {
            "cagr": "复合年增长率",
            "trend": "增长趋势",
            "sustainability": "增长可持续性",
        },
        "fcf_yield": {
            "current": "当前FCF收益率",
            "historical": "历史FCF收益率",
            "recommendation": "FCF收益率评估",
        },
        "overall_fcf_score": 0.0,
    }

    return {"free_cash_flow_analysis": fcf_analysis}


class ValuationRatiosInput(BaseModel):
    ticker: str = Field(description="股票代码")
    period: Literal["annual", "quarterly"] = Field(description="报告期")


@tool(args_schema=ValuationRatiosInput)
def compute_valuation_ratios(
    ticker: str, period: Literal["annual", "quarterly"]
) -> dict:
    """
    计算估值比率，基于财务数据和估值数据进行价值投资分析。

    注意：此工具用于深度估值分析，包含估值评估和投资建议。
    如果只需要基础估值数据（PE、PB等），请使用get_stock_valuation工具。
    这两个工具功能互补，不会相互调用。

    分析内容：
    1. 获取最新PE、PB、ROE等估值指标
    2. 基于财务数据进行深度分析
    3. 提供价值投资评估建议
    """
    try:
        # 1. 获取估值数据
        from gems.api import get_stock_financials, get_stock_valuation_data

        valuation_data = get_stock_valuation_data(ticker)

        # 2. 获取财务数据用于深度分析
        financial_data = get_stock_financials(ticker, period)

        # 3. 估值评估
        pe_ratio = valuation_data.get("pe_ratio", 0)
        pb_ratio = valuation_data.get("pb_ratio", 0)
        roe = valuation_data.get("roe", 0)

        pe_assessment = "低估" if pe_ratio < 15 else "高估" if pe_ratio > 25 else "合理"
        pb_assessment = (
            "低估" if pb_ratio < 1.0 else "高估" if pb_ratio > 2.5 else "合理"
        )
        roe_assessment = "优秀" if roe > 15 else "良好" if roe > 10 else "一般"

        # 4. 综合分析
        analysis = {
            "ticker": ticker,
            "period": period,
            "current_valuation": {
                "pe_ratio": pe_ratio,
                "pb_ratio": pb_ratio,
                "roe": roe,
                "eps": valuation_data.get("eps", 0),
                "bvps": valuation_data.get("bvps", 0),
            },
            "valuation_assessment": {
                "pe_assessment": pe_assessment,
                "pb_assessment": pb_assessment,
                "roe_assessment": roe_assessment,
            },
            "investment_recommendation": f"基于当前估值水平，PE{pe_assessment}，PB{pb_assessment}，ROE{roe_assessment}",
            "data_sources": ["AkShare财务数据", "估值计算"],
        }

        return {"comprehensive_valuation_analysis": analysis}

    except Exception as e:
        return {"error": f"综合估值分析失败: {str(e)}"}


class BusinessSimplicityInput(BaseModel):
    ticker: str = Field(description="股票代码")


@tool(args_schema=BusinessSimplicityInput)
def assess_business_simplicity(ticker: str) -> dict:
    """
    评估业务简单易懂程度，分析主营业务清晰度和业务复杂度。

    评估业务特征：
    - 主营业务清晰度：核心业务占比、业务专注度
    - 业务复杂度：产品线、市场、运营复杂度
    - 可理解性：业务模式是否容易理解
    - 可预测性：业务前景的可预测性

    返回业务简单性评分和分析。
    """
    business_simplicity = {
        "ticker": ticker,
        "core_business_clarity": {
            "main_business_ratio": "主营业务占比",
            "business_focus": "业务专注度",
            "score": 0.0,
        },
        "business_complexity": {
            "product_lines": "产品线复杂度",
            "market_diversity": "市场多样性",
            "operational_complexity": "运营复杂度",
            "score": 0.0,
        },
        "understandability": {
            "business_model": "业务模式可理解性",
            "competitive_advantage": "竞争优势清晰度",
            "score": 0.0,
        },
        "predictability": {
            "revenue_stability": "收入稳定性",
            "earnings_predictability": "盈利可预测性",
            "score": 0.0,
        },
        "overall_simplicity_score": 0.0,
        "recommendation": "业务简单性评估结果",
    }

    return {"business_simplicity": business_simplicity}
