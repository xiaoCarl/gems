#!/usr/bin/env python3
"""
详细调试缓存功能
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
from gems.cache.manager import cache_manager


def test_cache_debug_detailed():
    """详细调试缓存功能"""
    print("🔍 详细调试缓存功能...")

    # 创建Agent实例
    agent = Agent()

    # 测试查询
    test_query = "分析600519.SH"
    symbol = "600519.SH"
    test_result = "这是测试的分析结果"

    print(f"\n📊 测试查询: {test_query}")
    print(f"  期望股票代码: {symbol}")
    print(f"  测试结果: {test_result}")

    # 1. 测试股票代码提取
    print("\n1. 测试股票代码提取...")
    extracted_symbol = agent._extract_stock_symbol(test_query)
    print(f"  提取的股票代码: {extracted_symbol}")
    if extracted_symbol == symbol:
        print("  ✅ 股票代码提取正确")
    else:
        print("  ❌ 股票代码提取错误")

    # 首先清空缓存，确保测试环境干净
    cache_manager.clear()
    print("\n  🔄 已清空缓存")

    # 2. 直接设置缓存
    print("\n2. 直接设置缓存...")
    cache_manager.set_analysis_result(symbol, test_query, test_result)
    print("  ✅ 缓存设置成功")

    # 3. 直接获取缓存
    print("\n3. 直接获取缓存...")
    cached_result = cache_manager.get_analysis_result(symbol, test_query)
    if cached_result == test_result:
        print("  ✅ 缓存获取成功")
        print(f"  缓存结果: {cached_result}")
    else:
        print("  ❌ 缓存获取失败")
        print(f"  期望: {test_result}")
        print(f"  实际: {cached_result}")

    # 4. 模拟Agent.run()中的缓存检查逻辑
    print("\n4. 模拟Agent.run()中的缓存检查逻辑...")
    symbol_check = agent._extract_stock_symbol(test_query)
    print(f"  提取的股票代码: {symbol_check}")
    if symbol_check:
        cached_result_check = cache_manager.get_analysis_result(
            symbol_check, test_query
        )
        print(f"  缓存检查结果: {cached_result_check}")
        if cached_result_check:
            print("  ✅ 缓存检查应该命中")
        else:
            print("  ❌ 缓存检查未命中")
    else:
        print("  ❌ 无法提取股票代码")

    # 5. 测试通过Agent.run()获取缓存
    print("\n5. 测试通过Agent.run()获取缓存...")
    result = agent.run(test_query)
    print(f"  结果长度: {len(result)} 字符")
    print(f"  结果内容: {result}")

    # 检查是否从缓存返回
    if result == test_result:
        print("  ✅ Agent.run() 成功从缓存返回结果")
    else:
        print("  ❌ Agent.run() 没有从缓存返回结果")
        print(f"  期望: {test_result}")
        print(f"  实际: {result}")

    # 显示缓存统计
    print("\n📈 缓存统计:")
    print(f"  缓存启用: {cache_manager.enabled}")
    print(f"  分析缓存TTL: {cache_manager.cache_ttl.get('analysis', 'N/A')} 秒")


if __name__ == "__main__":
    test_cache_debug_detailed()
