#!/usr/bin/env python3
"""
价值投资分析演示脚本
"""

import os
import sys
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis.value_investing import ValueInvestingAnalyzer
from src.utils.logger import setup_logger

logger = setup_logger()


def demo_basic_analysis():
    """基本分析演示"""
    print("=" * 60)
    print("Gems 价值投资分析工具演示")
    print("=" * 60)

    # 初始化分析器
    tushare_token = os.getenv("TUSHARE_TOKEN")
    analyzer = ValueInvestingAnalyzer(tushare_token)

    # 演示1: A股分析
    print("\n1. A股股票分析演示")
    print("-" * 40)

    a_stocks = ["000001", "000002", "600519"]  # 平安银行、万科A、贵州茅台

    for symbol in a_stocks:
        try:
            result = analyzer.analyze_stock(symbol, market="A")
            print(f"{symbol}: {result.name}")
            print(f"  评分: {result.overall_score:.1f} - {result.recommendation.value}")
            print(f"  PE: {result.pe:.1f}, PB: {result.pb:.1f}, 股息率: {result.dividend_yield:.1f}%")
        except Exception as e:
            print(f"{symbol}: 分析失败 - {e}")

    # 演示2: 港股分析
    print("\n2. 港股股票分析演示")
    print("-" * 40)

    hk_stocks = ["00700", "00939"]  # 腾讯控股、建设银行

    for symbol in hk_stocks:
        try:
            result = analyzer.analyze_stock(symbol, market="HK")
            print(f"{symbol}: {result.name}")
            print(f"  评分: {result.overall_score:.1f} - {result.recommendation.value}")
            print(f"  PE: {result.pe:.1f}, PB: {result.pb:.1f}, 股息率: {result.dividend_yield:.1f}%")
        except Exception as e:
            print(f"{symbol}: 分析失败 - {e}")

    # 演示3: 批量分析
    print("\n3. 批量分析演示")
    print("-" * 40)

    try:
        results = analyzer.batch_analyze(a_stocks, market="A")
        print(f"共分析 {len(results)} 只A股:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.name} ({result.symbol}): {result.overall_score:.1f}分")
    except Exception as e:
        print(f"批量分析失败: {e}")

    # 演示4: 生成报告
    print("\n4. 报告生成演示")
    print("-" * 40)

    try:
        result = analyzer.analyze_stock("000001", market="A")

        # 文本报告
        print("文本报告摘要:")
        print(result.summary())

        # JSON报告
        print("\nJSON格式数据:")
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False)[:500] + "...")

        # HTML报告
        html_report = analyzer.generate_report(result, "html")
        report_file = "demo_report.html"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(html_report)
        print(f"\nHTML报告已保存到: {report_file}")

    except Exception as e:
        print(f"报告生成失败: {e}")

    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


def demo_advanced_features():
    """高级功能演示"""
    print("\n" + "=" * 60)
    print("高级功能演示")
    print("=" * 60)

    # 初始化分析器
    tushare_token = os.getenv("TUSHARE_TOKEN")
    analyzer = ValueInvestingAnalyzer(tushare_token)

    # 演示自定义分析
    print("\n1. 自定义股票分析")
    print("-" * 40)

    while True:
        symbol = input("请输入股票代码（输入q退出）: ").strip()
        if symbol.lower() == 'q':
            break

        market = input("请输入市场类型（A/HK）: ").strip().upper()
        if market not in ['A', 'HK']:
            market = 'A'

        try:
            result = analyzer.analyze_stock(symbol, market)
            print("\n分析结果:")
            print(result.summary())
        except Exception as e:
            print(f"分析失败: {e}")


def main():
    """主函数"""
    print("Gems 价值投资分析工具演示")
    print("版本: 1.0.0 (简化版)")
    print("说明: 此版本使用模拟数据，实际使用时需要配置真实数据源")
    print()

    while True:
        print("\n请选择演示模式:")
        print("1. 基本分析演示")
        print("2. 高级功能演示")
        print("3. 退出")

        choice = input("请输入选择 (1-3): ").strip()

        if choice == '1':
            demo_basic_analysis()
        elif choice == '2':
            demo_advanced_features()
        elif choice == '3':
            print("感谢使用，再见！")
            break
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main()