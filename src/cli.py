"""
命令行接口 - 简化版
"""

import argparse
import sys
import os
from typing import List
import json

from .utils.logger import setup_logger
from .analysis.value_investing import ValueInvestingAnalyzer

logger = setup_logger()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="A股和港股价值投资分析工具（简化版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s analyze 000001 --market A
  %(prog)s batch-analyze 000001 000002 600519 --market A
  %(prog)s report 000001 --market A --output report.html
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="命令")

    # analyze命令
    analyze_parser = subparsers.add_parser("analyze", help="分析单只股票")
    analyze_parser.add_argument("symbol", help="股票代码")
    analyze_parser.add_argument("--market", choices=["A", "HK"], default="A",
                               help="市场类型，A表示A股，HK表示港股")
    analyze_parser.add_argument("--output", help="输出文件路径")
    analyze_parser.add_argument("--format", choices=["text", "json", "html"],
                               default="text", help="输出格式")

    # batch-analyze命令
    batch_parser = subparsers.add_parser("batch-analyze", help="批量分析股票")
    batch_parser.add_argument("symbols", nargs="+", help="股票代码列表")
    batch_parser.add_argument("--market", choices=["A", "HK"], default="A",
                             help="市场类型")
    batch_parser.add_argument("--output", help="输出文件路径")
    batch_parser.add_argument("--format", choices=["json", "text"], default="json",
                             help="输出格式")

    # report命令
    report_parser = subparsers.add_parser("report", help="生成分析报告")
    report_parser.add_argument("symbol", help="股票代码")
    report_parser.add_argument("--market", choices=["A", "HK"], default="A",
                              help="市场类型")
    report_parser.add_argument("--output", required=True, help="输出文件路径")
    report_parser.add_argument("--format", choices=["html"], default="html",
                              help="报告格式")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        # 初始化分析器
        tushare_token = os.getenv("TUSHARE_TOKEN")
        analyzer = ValueInvestingAnalyzer(tushare_token)

        if args.command == "analyze":
            analyze_stock(analyzer, args)
        elif args.command == "batch-analyze":
            batch_analyze(analyzer, args)
        elif args.command == "report":
            generate_report(analyzer, args)
        else:
            parser.print_help()

    except Exception as e:
        logger.error(f"执行命令失败: {e}")
        sys.exit(1)


def analyze_stock(analyzer: ValueInvestingAnalyzer, args):
    """分析单只股票"""
    logger.info(f"分析股票: {args.symbol} ({args.market})")

    try:
        result = analyzer.analyze_stock(args.symbol, args.market)

        if args.format == "text":
            output = result.summary()
        elif args.format == "json":
            output = json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
        elif args.format == "html":
            output = analyzer.generate_report(result, "html")
        else:
            raise ValueError(f"不支持的格式: {args.format}")

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            logger.info(f"结果已保存到: {args.output}")
        else:
            print(output)

    except Exception as e:
        logger.error(f"分析股票失败: {e}")
        raise


def batch_analyze(analyzer: ValueInvestingAnalyzer, args):
    """批量分析股票"""
    logger.info(f"批量分析 {len(args.symbols)} 只股票")

    try:
        results = analyzer.batch_analyze(args.symbols, args.market)

        if args.format == "json":
            output = json.dumps(
                [result.to_dict() for result in results],
                indent=2,
                ensure_ascii=False
            )
        elif args.format == "text":
            output = ""
            for i, result in enumerate(results, 1):
                output += f"{i}. {result.name} ({result.symbol}): {result.overall_score:.1f}分 - {result.recommendation.value}\n"
                output += f"   PE: {result.pe:.1f}, PB: {result.pb:.1f}, 股息率: {result.dividend_yield:.1f}%\n\n"
        else:
            raise ValueError(f"不支持的格式: {args.format}")

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            logger.info(f"结果已保存到: {args.output}")
        else:
            print(output)

        # 打印摘要
        print(f"\n分析完成，共分析 {len(results)} 只股票")
        print("Top 3 推荐股票:")
        for i, result in enumerate(results[:3], 1):
            print(f"{i}. {result.name} ({result.symbol}): {result.overall_score:.1f}分 - {result.recommendation.value}")

    except Exception as e:
        logger.error(f"批量分析失败: {e}")
        raise


def generate_report(analyzer: ValueInvestingAnalyzer, args):
    """生成分析报告"""
    logger.info(f"生成报告: {args.symbol} ({args.market})")

    try:
        result = analyzer.analyze_stock(args.symbol, args.market)

        if args.format == "html":
            report = analyzer.generate_report(result, "html")
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
            logger.info(f"HTML报告已保存到: {args.output}")
        else:
            raise ValueError(f"不支持的格式: {args.format}")

    except Exception as e:
        logger.error(f"生成报告失败: {e}")
        raise


if __name__ == "__main__":
    main()