"""
数据模式定义
"""

from pydantic import BaseModel


class Task(BaseModel):
    """任务"""
    id: int
    description: str
    done: bool = False


class TaskList(BaseModel):
    """任务列表"""
    tasks: list[Task]


class IsDone(BaseModel):
    """是否完成"""
    done: bool


class Answer(BaseModel):
    """答案"""
    answer: str


class StockConfirmation(BaseModel):
    """股票确认"""
    stock_name: str | None = None
    stock_code: str | None = None
    clarification_needed: str | None = None


class OptimizedToolArgs(BaseModel):
    """优化的工具参数"""
    arguments: dict
