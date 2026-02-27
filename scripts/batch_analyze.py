#!/usr/bin/env python3
"""
批量分析脚本 - 同时分析多只股票并生成对比报告
"""

import argparse
import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_PATH / "src"))


def analyze_single(symbol: str) -> dict:
    """分析单只股票"""
    try:
        from gems.agent import Agent
        from gems.config import get_config
        
        get_config()
        agent = Agent(use_web_output=False)
        
        query = f"简要分析股票{symbol}的核心指标（PE、PB、ROE、护城河）"
        result = agent.run(query)
        
        return {
            "symbol": symbol,
            "status": "success",
            "result": result
        }
    except Exception as e:
        return {
            "symbol": symbol,
            "status": "error",
            "error": str(e)
        }


def batch_analyze(symbols: list[str], max_workers: int = 2) -> list[dict]:
    """批量分析股票"""
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_symbol = {
            executor.submit(analyze_single, symbol): symbol 
            for symbol in symbols
        }
        
        for future in as_completed(future_to_symbol):
            result = future.result()
            results.append(result)
            
            symbol = result["symbol"]
            if result["status"] == "success":
                print(f"✓ {symbol} 分析完成", file=sys.stderr)
            else:
                print(f"✗ {symbol} 分析失败：{result.get('error', '未知错误')}", file=sys.stderr)
    
    return results


def generate_comparison_report(results: list[dict]) -> str:
    """生成对比报告"""
    success_results = [r for r in results if r["status"] == "success"]
    
    report = ["# 股票批量分析报告\n"]
    report.append(f"分析股票数：{len(results)}\n")
    report.append(f"成功：{len(success_results)} | 失败：{len(results) - len(success_results)}\n")
    report.append("=" * 60 + "\n\n")
    
    for result in success_results:
        report.append(f"## {result['symbol']}\n")
        report.append(result["result"])
        report.append("\n---\n\n")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="批量分析多只股票")
    parser.add_argument("symbols", nargs="+", help="股票代码列表（空格分隔）")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--workers", type=int, default=2, help="并发数（默认2）")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    print(f"开始批量分析 {len(args.symbols)} 只股票...\n", file=sys.stderr)
    
    results = batch_analyze(args.symbols, max_workers=args.workers)
    
    if args.json:
        output = json.dumps(results, ensure_ascii=False, indent=2)
    else:
        output = generate_comparison_report(results)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n报告已保存至：{args.output}", file=sys.stderr)
    else:
        print(output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
