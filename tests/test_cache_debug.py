#!/usr/bin/env python3
"""
调试缓存配置问题
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

from gems.cache.manager import cache_manager
from gems.config import get_config


def debug_cache_config():
    """调试缓存配置"""
    print("🔍 调试缓存配置...")

    # 测试配置加载
    print("\n1. 测试配置加载...")
    try:
        config = get_config()
        print("  ✅ 配置加载成功")
        print(f"  缓存启用: {config.cache_enabled}")
        print(f"  分析缓存TTL: {config.cache_ttl_analysis}")
    except Exception as e:
        print(f"  ❌ 配置加载失败: {e}")

    # 测试缓存管理器初始化
    print("\n2. 测试缓存管理器初始化...")
    try:
        # 强制初始化
        cache_manager._ensure_initialized()
        print("  ✅ 缓存管理器初始化成功")
        print(f"  缓存启用: {cache_manager.enabled}")
        print(f"  缓存策略: {cache_manager.cache_ttl}")
    except Exception as e:
        print(f"  ❌ 缓存管理器初始化失败: {e}")

    # 测试基本缓存操作
    print("\n3. 测试基本缓存操作...")
    symbol = "600519.SH"
    query = "分析贵州茅台"
    test_result = "这是测试的分析结果"

    try:
        # 设置缓存
        cache_manager.set_analysis_result(symbol, query, test_result)
        print("  ✅ 缓存设置成功")

        # 获取缓存
        cached_result = cache_manager.get_analysis_result(symbol, query)
        if cached_result == test_result:
            print("  ✅ 缓存获取成功")
        else:
            print(f"  ❌ 缓存获取失败，期望: {test_result}, 实际: {cached_result}")
    except Exception as e:
        print(f"  ❌ 缓存操作失败: {e}")


if __name__ == "__main__":
    debug_cache_config()
