#!/usr/bin/env python3
"""
股票搜索脚本 - 根据名称搜索股票代码
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_PATH / "src"))


def search_stock(name: str) -> list[dict]:
    """搜索股票"""
    try:
        import akshare as ak
        
        # 搜索A股
        results = []
        try:
            a_shares = ak.stock_zh_a_spot_em()
            if isinstance(a_shares, list):
                a_shares = ak.pd.DataFrame(a_shares)
            a_matches = a_shares[a_shares["名称"].str.contains(name, na=False, case=False)]
            
            for _, row in a_matches.head(10).iterrows():
                code = row.get("代码", "")
                name_val = row.get("名称", "")
                if code and name_val:
                    suffix = ".SH" if code.startswith("6") else ".SZ"
                    results.append({
                        "code": f"{code}{suffix}",
                        "name": name_val,
                        "market": "A股",
                        "price": row.get("最新价", "-"),
                        "change": row.get("涨跌幅", "-")
                    })
        except Exception as e:
            print(f"A股搜索出错: {e}", file=sys.stderr)
        
        # 搜索港股
        try:
            hk_shares = ak.stock_hk_ggt_components_em()
            if isinstance(hk_shares, list):
                hk_shares = ak.pd.DataFrame(hk_shares)
            hk_matches = hk_shares[hk_shares["名称"].str.contains(name, na=False, case=False)]
            
            for _, row in hk_matches.head(10).iterrows():
                code = row.get("代码", "")
                name_val = row.get("名称", "")
                if code and name_val:
                    results.append({
                        "code": f"{code}.HK",
                        "name": name_val,
                        "market": "港股",
                        "price": row.get("最新价", "-"),
                        "change": row.get("涨跌幅", "-")
                    })
        except Exception as e:
            print(f"港股搜索出错: {e}", file=sys.stderr)
        
        return results
        
    except ImportError:
        print("错误：akshare未安装，请运行: pip install akshare", file=sys.stderr)
        return []
    except Exception as e:
        print(f"搜索失败：{e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(description="搜索股票代码")
    parser.add_argument("name", help="股票名称关键词")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    
    args = parser.parse_args()
    
    results = search_stock(args.name)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print(f"未找到包含'{args.name}'的股票")
        else:
            print(f"找到 {len(results)} 只相关股票：\n")
            print(f"{'代码':<15} {'名称':<12} {'市场':<8} {'最新价':<10} {'涨跌幅':<8}")
            print("-" * 60)
            for item in results:
                print(f"{item['code']:<15} {item['name']:<12} {item['market']:<8} "
                      f"{item['price']:<10} {item['change']:<8}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
