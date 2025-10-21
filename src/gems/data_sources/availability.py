"""
数据源可用性测试模块

提供独立的数据源连接测试功能，用于在程序启动时检查所有数据源的可用性。
"""

import time
from typing import Dict, List, Tuple
from gems.output.core import get_output_engine
from gems.exceptions import DataSourceError

from .tdx_source import TDXDataSource
from .akshare_source import AkShareDataSource
from .yfinance_source import YFinanceDataSource


class DataSourceAvailabilityTester:
    """数据源可用性测试器"""
    
    def __init__(self):
        self.output = get_output_engine()
        self.test_symbols = {
            "A股": "000001.SZ",  # 平安银行
            "港股": "00700.HK",   # 腾讯控股
        }
        self.timeout = 10  # 测试超时时间（秒）
    
    def test_tdx_availability(self) -> Tuple[bool, str]:
        """测试通达信数据源可用性"""
        try:
            from gems.tools.tdx_api import test_tdx_connection
            
            start_time = time.time()
            available = test_tdx_connection()
            elapsed = time.time() - start_time
            
            if available:
                return True, f"通达信数据源可用 (响应时间: {elapsed:.2f}s)"
            else:
                return False, "通达信数据源不可用"
                
        except Exception as e:
            return False, f"通达信数据源测试失败: {str(e)}"
    
    def test_akshare_availability(self) -> Tuple[bool, str]:
        """测试AkShare数据源可用性"""
        try:
            import akshare as ak
            
            start_time = time.time()
            
            # 测试A股数据获取
            test_symbol = self.test_symbols["A股"]
            clean_symbol = test_symbol.split('.')[0]
            
            # 尝试获取A股实时数据
            stock_data = ak.stock_zh_a_spot_em()
            
            # 检查数据是否有效
            if stock_data is None or stock_data.empty:
                return False, "AkShare返回空数据"
            
            # 检查是否能找到测试股票
            filtered_data = stock_data[stock_data['代码'] == clean_symbol]
            
            elapsed = time.time() - start_time
            
            if not filtered_data.empty:
                return True, f"AkShare数据源可用 (响应时间: {elapsed:.2f}s)"
            else:
                return False, f"AkShare无法找到测试股票 {test_symbol}"
                
        except ImportError:
            return False, "AkShare库未安装"
        except Exception as e:
            return False, f"AkShare数据源测试失败: {str(e)}"
    
    def test_yfinance_availability(self) -> Tuple[bool, str]:
        """测试yfinance数据源可用性"""
        try:
            import yfinance as yf
            
            start_time = time.time()
            
            # 测试港股数据获取
            test_symbol = self.test_symbols["港股"]
            clean_symbol = test_symbol.split('.')[0].lstrip('0') + '.HK'
            
            # 尝试获取港股数据
            ticker = yf.Ticker(clean_symbol)
            hist = ticker.history(period="1d")
            
            elapsed = time.time() - start_time
            
            if not hist.empty:
                return True, f"yfinance数据源可用 (响应时间: {elapsed:.2f}s)"
            else:
                return False, f"yfinance无法获取测试股票 {test_symbol} 的数据"
                
        except ImportError:
            return False, "yfinance库未安装"
        except Exception as e:
            return False, f"yfinance数据源测试失败: {str(e)}"
    
    def test_all_sources(self) -> Dict[str, Dict[str, any]]:
        """测试所有数据源可用性"""
        self.output.show_progress("开始数据源可用性测试...")
        
        results = {}
        
        # 测试通达信
        self.output.show_progress("测试通达信数据源...")
        tdx_available, tdx_message = self.test_tdx_availability()
        results["tdx"] = {
            "available": tdx_available,
            "message": tdx_message,
            "priority": "high"  # 主要实时数据源
        }
        
        # 测试AkShare
        self.output.show_progress("测试AkShare数据源...")
        akshare_available, akshare_message = self.test_akshare_availability()
        results["akshare"] = {
            "available": akshare_available,
            "message": akshare_message,
            "priority": "high"  # 主要财务数据源
        }
        
        # 测试yfinance
        self.output.show_progress("测试yfinance数据源...")
        yfinance_available, yfinance_message = self.test_yfinance_availability()
        results["yfinance"] = {
            "available": yfinance_available,
            "message": yfinance_message,
            "priority": "medium"  # 备用港股数据源
        }
        
        # 显示测试结果
        self.output.show_progress("数据源可用性测试完成:")
        for source_name, result in results.items():
            status = "✓ 可用" if result["available"] else "✗ 不可用"
            self.output.show_progress(f"  {source_name}: {status} - {result['message']}")
        
        return results
    
    def get_available_sources_summary(self) -> str:
        """获取可用数据源摘要"""
        results = self.test_all_sources()
        
        available_sources = []
        unavailable_sources = []
        
        for source_name, result in results.items():
            if result["available"]:
                available_sources.append(source_name)
            else:
                unavailable_sources.append(source_name)
        
        summary = f"可用数据源: {', '.join(available_sources) if available_sources else '无'}"
        if unavailable_sources:
            summary += f" | 不可用数据源: {', '.join(unavailable_sources)}"
        
        return summary


# 全局可用性测试器实例
availability_tester = DataSourceAvailabilityTester()