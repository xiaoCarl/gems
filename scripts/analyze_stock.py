#!/usr/bin/env python3
"""
Gems Analyzer - 股票分析入口脚本
支持A股和港股的快速价值投资分析
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 项目路径
PROJECT_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_PATH / "src"))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv(PROJECT_PATH / ".env")


def normalize_symbol(symbol: str) -> str:
    """标准化股票代码"""
    symbol = symbol.strip().upper()
    
    # 已带后缀
    if "." in symbol:
        return symbol
    
    # 港股（5位数字）
    if len(symbol) == 5 and symbol.isdigit():
        return f"{symbol}.HK"
    
    # A股判断
    if symbol.isdigit():
        if symbol.startswith("6"):
            return f"{symbol}.SH"
        elif symbol.startswith(("0", "3")):
            return f"{symbol}.SZ"
    
    return symbol


def analyze_stock(symbol: str, use_cache: bool = True, output_json: bool = False) -> dict:
    """分析单只股票"""
    symbol = normalize_symbol(symbol)
    
    # 导入Agent
    from gems.agent import Agent
    from gems.config import get_config
    
    # 确保配置初始化
    get_config()
    
    # 创建Agent并运行分析
    agent = Agent(use_web_output=False)
    
    query = f"分析股票{symbol}的投资价值"
    
    try:
        result = agent.run(query)
        return {
            "symbol": symbol,
            "result": result,
            "cached": False
        }
    except Exception as e:
        return {
            "symbol": symbol,
            "error": str(e),
            "cached": False
        }


def main():
    parser = argparse.ArgumentParser(
        description="Gems Analyzer - AI价值投资分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s 600519           # 分析贵州茅台
  %(prog)s 00700.HK         # 分析腾讯控股
  %(prog)s 600519 --json    # 输出JSON格式
  %(prog)s 600519 --force   # 强制重新分析（忽略缓存）
        """
    )
    
    parser.add_argument("symbol", help="股票代码（如：600519, 00700.HK）")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--force", action="store_true", help="强制重新分析，忽略缓存")
    parser.add_argument("--source", choices=["tdx", "akshare", "yfinance"],
                       help="指定数据源")
    
    args = parser.parse_args()
    
    # 执行分析
    result = analyze_stock(
        args.symbol,
        use_cache=not args.force,
        output_json=args.json
    )
    
    # 输出结果
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if "error" in result:
            print(f"❌ 分析失败：{result['error']}")
            sys.exit(1)
        else:
            print(result["result"])
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
