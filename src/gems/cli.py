"""
简单CLI入口 - 重构版本

使用重构后的简单输出系统，移除rich依赖。
"""

import sys
import logging
from dotenv import load_dotenv

# Load environment variables BEFORE importing any gems modules
load_dotenv()

# 禁用httpx的HTTP请求日志
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

from gems.agent import Agent


def show_welcome():
    """显示欢迎界面"""
    welcome_text = """
🎯 Gems Agent - 价值投资分析

╔══════════════════════════════════════════════════╗
║        AI金融分析助手 --- 价值投资分析            ║
╚══════════════════════════════════════════════════╝

       Great Enterprises at Moderate Prices 

    ██████╗    ███████╗  ███╗   ███╗  ███████╗
    ██╔════╝   ██╔════╝  ████╗ ████║  ██╔════╝
    ██║  ███╗  █████╗    ██╔████╔██║  ███████╗
    ██║   ██║  ██╔══╝    ██║╚██╔╝██║  ╚════██║
    ╚██████╔╝  ███████╗  ██║ ╚═╝ ██║  ███████║
    ╚═════╝   ╚══════╝  ╚═╝     ╚═╝  ╚══════╝

                     好生意，好价格   

请输入股票名称或者代码，或者输入'exit'或'quit'退出。
"""
    print(welcome_text)


def main():
    """主函数"""
    # Show welcome screen
    show_welcome()
    
    # Initialize agent
    agent = Agent()

    while True:
        try:
            # Get user input
            query = input("\n>> ").strip()
            
            if query.lower() in ["exit", "quit", "退出"]:
                print("再见!")
                break
            
            if not query:
                continue
            
            # Process the query
            agent.run(query)
            
        except (KeyboardInterrupt, EOFError):
            print("\n 再见!")
            break
        except Exception as e:
            print(f"✗ 发生错误: {e}")
            continue


if __name__ == "__main__":
    main()