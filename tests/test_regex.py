#!/usr/bin/env python3
"""
测试股票代码提取的正则表达式
"""

import re


def test_stock_symbol_regex():
    """测试股票代码提取的正则表达式"""
    print("🧪 测试股票代码提取的正则表达式...")

    # 从agent.py复制的正则表达式模式（修复后）
    a_share_pattern = r"([0-9]{6})\.(SH|SZ)"
    hk_share_pattern = r"([0-9]{5})\.HK"
    us_share_pattern = r"\b([A-Z]{1,5})\b"

    test_queries = [
        "分析600519.SH",
        "分析000001.SZ",
        "分析00700.HK",
        "分析AAPL",
        "分析贵州茅台",
        "分析腾讯控股",
    ]

    for query in test_queries:
        print(f"\n📊 测试查询: {query}")
        query_upper = query.upper()

        # 尝试匹配A股
        a_match = re.search(a_share_pattern, query_upper)
        if a_match:
            symbol = f"{a_match.group(1)}.{a_match.group(2)}"
            print(f"  ✅ A股匹配: {symbol}")
            continue

        # 尝试匹配港股
        hk_match = re.search(hk_share_pattern, query_upper)
        if hk_match:
            symbol = f"{hk_match.group(1)}.HK"
            print(f"  ✅ 港股匹配: {symbol}")
            continue

        # 尝试匹配美股
        us_match = re.search(us_share_pattern, query_upper)
        if us_match:
            # 检查是否是常见的股票名称
            common_stocks = [
                "AAPL",
                "MSFT",
                "GOOGL",
                "AMZN",
                "TSLA",
                "META",
                "NVDA",
                "NFLX",
            ]
            symbol = us_match.group(1)
            if symbol in common_stocks:
                print(f"  ✅ 美股匹配: {symbol}")
                continue
            else:
                print(f"  ⚠️  美股匹配但不在常见列表: {symbol}")

        print("  ❌ 未匹配任何股票代码模式")


if __name__ == "__main__":
    test_stock_symbol_regex()
