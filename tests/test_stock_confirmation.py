#!/usr/bin/env python3
"""
测试修改后的股票确认功能
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


def test_stock_confirmation():
    """测试股票确认功能"""
    print("🧪 测试修改后的股票确认功能...")

    # 创建Agent实例
    agent = Agent()

    # 测试查询
    test_queries = ["分析600519.SH", "分析贵州茅台", "分析000001.SZ", "分析腾讯控股"]

    for query in test_queries:
        print(f"\n📊 测试查询: {query}")

        # 测试股票确认
        confirmed = agent._confirm_stock_info(query)

        if confirmed:
            print("  ✅ 股票确认成功")
        else:
            print("  ❌ 股票确认失败，需要重新输入")


if __name__ == "__main__":
    test_stock_confirmation()
