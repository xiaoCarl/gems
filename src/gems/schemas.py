from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Task(BaseModel):
    """Represents a single task in a task list."""
    id: int = Field(..., description="Unique identifier for the task.")
    description: str = Field(..., description="The description of the task.")
    done: bool = Field(False, description="Whether the task is completed.")

class TaskList(BaseModel):
    """Represents a list of tasks."""
    tasks: List[Task] = Field(..., description="The list of tasks.")

class IsDone(BaseModel):
    """Represents the boolean status of a task."""
    done: bool = Field(..., description="Whether the task is done or not.")

class Answer(BaseModel):
    """Represents an answer to the user's query."""
    answer: str = Field(..., description="A comprehensive answer to the user's query, including relevant numbers, data, reasoning, and insights.")

class OptimizedToolArgs(BaseModel):
    """Represents optimized arguments for a tool call."""
    arguments: Dict[str, Any] = Field(..., description="The optimized arguments dictionary for the tool call.")

class ValueInvestmentAssessment(BaseModel):
    """Represents a comprehensive value investment assessment."""
    good_business: str = Field(..., description="Assessment of whether it's a good business, including moat, profitability, and business model analysis.")
    good_price: str = Field(..., description="Assessment of whether it's a good price, including valuation metrics, safety margin, and comparison analysis.")
    long_term_risk: str = Field(..., description="Assessment of long-term holding risks, including industry outlook, competition, and management quality.")
    overall_recommendation: str = Field(..., description="Overall investment recommendation based on the three dimensions.")

class ValueInvestmentAnswer(BaseModel):
    """Represents a comprehensive value investment answer."""
    assessment: ValueInvestmentAssessment = Field(..., description="The value investment assessment across three dimensions.")
    summary: str = Field(..., description="A concise summary of the investment analysis.")
    key_metrics: Dict[str, Any] = Field(default_factory=dict, description="Key financial metrics used in the analysis.")

class StockConfirmation(BaseModel):
    """Represents stock information confirmation."""
    stock_name: str = Field(..., description="Confirmed stock name or code.")
    analysis_type: str = Field(..., description="Type of analysis to be performed.")
    analysis_dimensions: List[str] = Field(..., description="Key dimensions for analysis.")
    clarification_needed: str = Field("", description="Any clarification needed from user.")
