#!/usr/bin/env python3
"""
详细调试股票确认功能
"""

import os
import sys
from pathlib import Path

# 设置测试模式环境变量
os.environ["GEMS_TEST_MODE"] = "true"

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 手动设置一些环境变量用于测试
os.environ["DEEPSEEK_API_KEY"] = "test_key"

from gems.agent import Agent
from gems.model import call_llm
from gems.prompts import STOCK_CONFIRMATION_PROMPT
from gems.schemas import StockConfirmation


def test_stock_confirmation_debug():
    """详细调试股票确认功能"""
    print("🔍 详细调试股票确认功能...")

    # 测试查询
    test_query = "分析600519.SH"
    print(f"\n📊 测试查询: {test_query}")

    confirmation_prompt = f"""
    用户查询: "{test_query}"

    请确认股票信息并输出确认信息。
    """

    print("\n1. 测试LLM调用...")
    print(f"  系统提示: {STOCK_CONFIRMATION_PROMPT[:100]}...")
    print(f"  用户提示: {confirmation_prompt}")

    try:
        # 直接测试LLM调用
        print("\n2. 直接调用LLM...")
        confirmation = call_llm(
            confirmation_prompt,
            system_prompt=STOCK_CONFIRMATION_PROMPT,
            output_schema=StockConfirmation,
        )
        print("  ✅ LLM调用成功")
        print(f"  股票名称: {confirmation.stock_name}")
        print(f"  股票代码: {confirmation.stock_code}")
        print(f"  分析类型: {confirmation.analysis_type}")
        print(f"  分析维度: {confirmation.analysis_dimensions}")
        print(f"  需要澄清: {confirmation.clarification_needed}")

    except Exception as e:
        print(f"  ❌ LLM调用失败: {e}")
        import traceback

        print(f"  详细错误: {traceback.format_exc()}")

    # 测试Agent的确认方法
    print("\n3. 测试Agent._confirm_stock_info方法...")
    agent = Agent()
    try:
        confirmed = agent._confirm_stock_info(test_query)
        print(f"  确认结果: {confirmed}")
    except Exception as e:
        print(f"  ❌ 确认方法失败: {e}")
        import traceback

        print(f"  详细错误: {traceback.format_exc()}")


if __name__ == "__main__":
    test_stock_confirmation_debug()
