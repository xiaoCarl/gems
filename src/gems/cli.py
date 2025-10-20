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
from gems.output.core import get_output_engine


def show_welcome():
    """显示欢迎界面"""
    output = get_output_engine()
    output.show_welcome()


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
            result = agent.run(query)
            
            # 如果需要重新输入，继续循环
            if result == "需要重新输入股票信息":
                continue
            
        except (KeyboardInterrupt, EOFError):
            print("\n 再见!")
            break
        except Exception as e:
            print(f" 发生错误: {e}")
            continue


if __name__ == "__main__":
    main()