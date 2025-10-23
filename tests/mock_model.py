"""
模拟LLM模型

提供模拟的LLM调用，用于在没有API密钥的情况下进行测试。
"""

import time
from typing import Any

from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool
from pydantic import BaseModel


class MockLLM:
    """模拟LLM类"""

    def __init__(self):
        self.model = "mock-deepseek-chat"
        self.temperature = 0

    def with_structured_output(
        self, output_schema: type[BaseModel], method: str = "function_calling"
    ):
        """模拟结构化输出"""
        return self

    def bind_tools(self, tools: list[BaseTool]):
        """模拟工具绑定"""
        return self

    def invoke(self, input_data: dict) -> Any:
        """模拟调用"""
        prompt = input_data.get("prompt", "")

        # 模拟处理时间
        time.sleep(0.5)

        # 根据提示内容返回不同的模拟响应
        if "plan" in prompt.lower() or "task" in prompt.lower():
            # 模拟任务规划响应
            return {
                "tasks": [
                    {"id": 1, "description": "获取公司基本信息", "done": False},
                    {"id": 2, "description": "分析财务数据", "done": False},
                    {"id": 3, "description": "评估估值水平", "done": False},
                ]
            }
        elif "done" in prompt.lower():
            # 模拟任务完成检查
            return {"done": True}
        elif "optimize" in prompt.lower():
            # 模拟参数优化
            return {"arguments": {"symbol": "AAPL", "period": "annual", "limit": 5}}
        elif "answer" in prompt.lower() or "analysis" in prompt.lower():
            # 模拟价值投资分析响应
            return {
                "answer": """
# 价值投资分析报告 - 苹果公司 (AAPL)

## 1. 好生意 (Good Business)

### 护城河分析
- **品牌护城河**: 极强 - 苹果是全球最具价值的品牌之一
- **生态系统护城河**: 极强 - iOS生态系统形成强大锁定效应
- **技术护城河**: 强 - 芯片设计和软件集成能力

### 管理层质量
- 蒂姆·库克领导团队稳定，执行力强
- 创新文化持续，但产品迭代速度有所放缓

### 业务简单易懂
- 主要收入来源清晰：iPhone、服务、Mac、iPad
- 商业模式简单：硬件销售 + 服务订阅

### 自由现金流
- 2023年自由现金流：$1000亿美元
- 现金流生成能力极强，持续回购和分红

## 2. 好价格 (Good Price)

### 市盈率估值
- 当前PE：28倍
- 历史PE区间：10-35倍
- 相对于历史估值处于中高位

### 市净率估值
- 当前PB：35倍
- 资产质量优秀，但估值偏高

### 资本回报率
- ROE：147%
- ROIC：57%
- 资本配置效率极高

### 安全边际
- 当前价格安全边际：中等偏低
- 建议等待更好的买入时机

## 投资建议

**总体评估**: 优秀的企业，但当前估值偏高

**建议操作**:
- 长期持有者可继续持有
- 新投资者建议等待回调至PE 20-25倍区间
- 建议仓位：现有持仓维持，新增仓位等待

**关键风险**:
- 智能手机市场饱和
- 监管风险增加
- 创新速度放缓
"""
            }
        else:
            # 默认模拟工具调用响应
            return AIMessage(
                content="分析进行中...",
                tool_calls=[
                    {
                        "id": "call_001",
                        "name": "get_company_info",
                        "args": {"symbol": "AAPL"},
                    }
                ],
            )


# 创建模拟LLM实例
mock_llm = MockLLM()


def call_llm(
    prompt: str,
    system_prompt: str | None = None,
    output_schema: type[BaseModel] | None = None,
    tools: list[BaseTool] | None = None,
) -> Any:
    """
    模拟LLM调用函数

    在没有真实API密钥的情况下提供模拟响应。
    """
    print("🔧 使用模拟LLM进行测试...")

    # 使用模拟LLM
    runnable = mock_llm

    if output_schema:
        runnable = mock_llm.with_structured_output(output_schema)
    elif tools:
        runnable = mock_llm.bind_tools(tools)

    # 模拟调用
    result = runnable.invoke({"prompt": prompt})

    return result
