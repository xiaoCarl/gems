#!/usr/bin/env python3
"""
A股和港股股票分析脚本 - 简化版
"""

import os
import sys
import argparse
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis.value_investing import ValueInvestingAnalyzer
from src.utils.logger import setup_logger

logger = setup_logger()


def analyze_single_stock(symbol: str, market: str = "A", output_format: str = "text"):
    """
    分析单只股票

    Args:
        symbol: 股票代码
        market: 市场类型，A表示A股，HK表示港股
        output_format: 输出格式，text或json
    """
    try:
        logger.info(f"开始分析股票: {symbol} ({market})")

        # 初始化分析器
        tushare_token = os.getenv("TUSHARE_TOKEN")
        analyzer = ValueInvestingAnalyzer(tushare_token)

        # 分析股票
        result = analyzer.analyze_stock(symbol, market)

        if output_format == "text":
            print(result.summary())
        elif output_format == "json":
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        else:
            raise ValueError(f"不支持的输出格式: {output_format}")

        return result

    except Exception as e:
        logger.error(f"分析股票失败: {e}")
        raise


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="A股和港股股票分析脚本（简化版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --symbol 000001 --market A
  %(prog)s --symbol 00700 --market HK --format json
        """
    )

    parser.add_argument("--symbol", required=True, help="股票代码")
    parser.add_argument("--market", choices=["A", "HK"], default="A",
                       help="市场类型，A表示A股，HK表示港股")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                       help="输出格式")

    args = parser.parse_args()

    try:
        analyze_single_stock(args.symbol, args.market, args.format)
    except Exception as e:
        logger.error(f"执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()