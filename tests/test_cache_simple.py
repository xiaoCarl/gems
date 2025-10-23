#!/usr/bin/env python3
"""
简单测试缓存管理器功能
"""

import os
import sys
from pathlib import Path

# 设置测试模式环境变量
os.environ["GEMS_TEST_MODE"] = "true"

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gems.cache.manager import cache_manager


def test_cache_manager():
    """测试缓存管理器功能"""
    print("🧪 测试缓存管理器功能...")

    # 测试基本缓存操作
    symbol = "600519.SH"
    query = "分析贵州茅台"
    test_result = "这是测试的分析结果"

    print(f"  测试股票: {symbol}")
    print(f"  测试查询: {query}")
    print(f"  测试结果: {test_result}")

    # 1. 设置缓存
    print("\n  1. 设置缓存...")
    cache_manager.set_analysis_result(symbol, test_result)
    print("  ✅ 缓存设置成功")

    # 2. 获取缓存
    print("\n  2. 获取缓存...")
    cached_result = cache_manager.get_analysis_result(symbol)
    if cached_result == test_result:
        print("  ✅ 缓存获取成功")
        print(f"  缓存结果: {cached_result}")
    else:
        print("  ❌ 缓存获取失败")

    # 3. 测试不同的股票
    print("\n  3. 测试不同股票的缓存...")
    symbol2 = "000001.SZ"
    cached_result2 = cache_manager.get_analysis_result(symbol2)
    if cached_result2 is None:
        print("  ✅ 不同股票的缓存隔离正常")
    else:
        print("  ❌ 不同股票的缓存隔离异常")

    # 强制初始化缓存管理器以获取最新状态
    cache_manager._ensure_initialized()

    # 显示缓存配置
    print("\n📈 缓存配置:")
    print(f"  缓存启用: {cache_manager.enabled}")
    print(f"  分析缓存TTL: {cache_manager.cache_ttl.get('analysis', 'N/A')} 秒")
    print(f"  缓存策略: {list(cache_manager.cache_ttl.keys())}")


if __name__ == "__main__":
    test_cache_manager()
