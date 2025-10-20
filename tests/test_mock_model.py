"""
测试模拟LLM模型
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

# 现在可以导入mock_model
from mock_model import call_llm


def test_mock_llm():
    """测试模拟LLM的基本功能"""
    print("测试模拟LLM...")
    
    # 测试任务规划
    print("\n1. 测试任务规划:")
    result = call_llm("请为分析苹果公司制定任务计划")
    print(f"任务规划结果: {result}")
    
    # 测试任务完成检查
    print("\n2. 测试任务完成检查:")
    result = call_llm("任务是否完成?")
    print(f"任务完成检查: {result}")
    
    # 测试参数优化
    print("\n3. 测试参数优化:")
    result = call_llm("优化工具参数")
    print(f"参数优化结果: {result}")
    
    # 测试价值投资分析
    print("\n4. 测试价值投资分析:")
    result = call_llm("请分析苹果公司的价值投资价值")
    print(f"分析结果: {result}")
    
    print("\n✅ 所有模拟LLM测试完成!")


if __name__ == "__main__":
    test_mock_llm()