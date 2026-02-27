"""
命令行接口
"""

import sys

from gems.agent import Agent
from gems.config import get_config


def print_banner():
    """打印欢迎信息"""
    print("""
╔════════════════════════════════════════╗
║     💎 Gems Analyzer - AI价值投资分析工具 ║
║                                        ║
║  支持A股、港股的价值投资分析            ║
║  基于巴菲特投资理念                     ║
╚════════════════════════════════════════╝

输入股票代码或名称开始分析，输入 help 查看帮助，输入 exit 退出。
""")


def print_help():
    """打印帮助信息"""
    print("""
可用命令：
  <股票代码>    分析股票（如：600519, 00700.HK）
  <股票名称>    按名称分析（如：茅台, 腾讯）
  help          显示此帮助
  exit/quit     退出程序

示例：
  600519        分析贵州茅台
  00700.HK      分析腾讯控股
  对比茅台五粮液  对比分析两只股票
""")


def main():
    """主函数"""
    # 初始化配置
    get_config()
    
    # 打印欢迎信息
    print_banner()
    
    # 创建Agent
    agent = Agent(use_web_output=False)
    
    # 主循环
    while True:
        try:
            # 获取用户输入
            user_input = input("\n📝 请输入股票代码/名称 (或 help/exit): ").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            if user_input.lower() in ["exit", "quit", "q"]:
                print("\n👋 感谢使用 Gems Analyzer！")
                break
            
            if user_input.lower() == "help":
                print_help()
                continue
            
            # 执行分析
            print("\n🔍 正在分析，请稍候...\n")
            result = agent.run(user_input)
            print(result)
            
        except KeyboardInterrupt:
            print("\n\n👋 感谢使用 Gems Analyzer！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")


if __name__ == "__main__":
    main()
