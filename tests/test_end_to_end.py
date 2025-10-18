"""
端到端测试脚本

测试重构后的简单输出系统是否能正常工作。
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gems.agent import Agent


def test_agent_basic():
    """测试代理基本功能"""
    print("🧪 开始端到端测试...")
    
    # 创建代理实例
    agent = Agent()
    
    # 测试简单的查询
    test_query = "分析苹果公司(AAPL)的投资价值"
    print(f"\n测试查询: {test_query}")
    
    try:
        result = agent.run(test_query)
        print(f"\n✅ 测试成功！代理返回了结果")
        print(f"结果类型: {type(result)}")
        if result:
            print(f"结果长度: {len(result)} 字符")
        return True
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_planning():
    """测试代理任务规划功能"""
    print("\n🧪 测试任务规划...")
    
    agent = Agent()
    
    try:
        tasks = agent.plan_tasks("分析微软的投资价值")
        print(f"✅ 任务规划成功！生成了 {len(tasks)} 个任务")
        for i, task in enumerate(tasks, 1):
            print(f"  任务 {i}: {task.description}")
        return True
    except Exception as e:
        print(f"❌ 任务规划失败: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Gems Agent 端到端测试")
    print("=" * 50)
    
    success1 = test_agent_planning()
    success2 = test_agent_basic()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 所有测试通过！重构成功！")
    else:
        print("⚠ 部分测试失败，需要进一步调试")