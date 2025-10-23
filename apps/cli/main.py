"""
Gems CLI 命令行接口
提供命令行交互功能
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.gems.cli import main as cli_main
from src.gems.logging import get_logger

def main():
    """CLI入口点"""
    logger = get_logger("cli")
    logger.info("启动Gems CLI")

    try:
        cli_main()
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        print("\n👋 感谢使用Gems投资分析助手！")
    except Exception as e:
        logger.error(f"CLI执行错误: {e}")
        print(f"❌ 发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()