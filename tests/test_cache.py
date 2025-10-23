#!/usr/bin/env python3
"""
测试分析结果缓存功能
"""

import os
import sys
from pathlib import Path

# 设置测试模式环境变量
os.environ["GEMS_TEST_MODE"] = "true"

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gems.agent import Agent
from gems.cache.manager import cache_manager


def test_cache_functionality():
    """测试缓存功能"""
    print("🧪 测试分析结果缓存功能...")

    # 创建Agent实例
    agent = Agent()

    # 测试查询
    test_queries = ["分析贵州茅台", "分析600519.SH", "分析腾讯控股"]

    for query in test_queries:
        print(f"\n📊 测试查询: {query}")

        # 第一次查询 - 应该进行完整分析
        print("  第一次查询 (应该进行完整分析)...")
        result1 = agent.run(query)
        print(f"  结果长度: {len(result1)} 字符")

        # 第二次查询 - 应该从缓存返回
        print("  第二次查询 (应该从缓存返回)...")
        result2 = agent.run(query)
        print(f"  结果长度: {len(result2)} 字符")

        # 验证结果是否相同
        if result1 == result2:
            print("  ✅ 缓存功能正常: 两次结果相同")
        else:
            print("  ❌ 缓存功能异常: 两次结果不同")

    # 显示缓存统计
    print("\n📈 缓存统计:")
    print(f"  缓存启用: {cache_manager.enabled}")
    print(f"  分析缓存TTL: {cache_manager.cache_ttl.get('analysis', 'N/A')} 秒")


if __name__ == "__main__":
    test_cache_functionality()
