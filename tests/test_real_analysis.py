"""
使用真实LLM进行股票分析测试
"""

import os
import sys
from dotenv import load_dotenv

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 加载环境变量
load_dotenv()

print("🚀 使用真实LLM进行股票分析测试")
print("=" * 50)

try:
    from gems.agent_fixed import Agent
    
    # 创建代理实例
    agent = Agent()
    
    # 测试简单的查询
    test_query = "分析茅台股份的投资价值"
    print(f"测试查询: {test_query}")
    
    # 运行分析
    result = agent.run(test_query)
    
    print("\n✅ 真实LLM分析成功！")
    print(f"结果类型: {type(result)}")
    if result:
        print(f"结果长度: {len(result)} 字符")
        print("\n分析结果预览:")
        print(result[:500] + "..." if len(result) > 500 else result)
    
    print("\n🎉 真实LLM模式工作正常！")
    
except Exception as e:
    print(f"\n❌ 分析失败: {e}")
    import traceback
    traceback.print_exc()