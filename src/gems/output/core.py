"""
简单输出核心模块

提供最基本的输出功能，移除所有rich依赖，使用简单print语句。
"""

from typing import Any


class SimpleOutputEngine:
    """
    简单输出引擎

    提供最基本的输出功能，使用简单print语句。
    """

    def __init__(self):
        # 移除所有rich依赖，使用简单输出
        pass

    def show_welcome(self):
        """显示欢迎界面"""
        welcome_text = """
🎯 Gems Agent - 价值投资分析

╔══════════════════════════════════════════════════╗
║        AI金融分析助手 --- 价值投资分析             ║
╚══════════════════════════════════════════════════╝

       Great Enterprises at Moderate Prices 

    ██████╗    ███████╗  ███╗   ███╗  ███████╗
    ██╔════╝   ██╔════╝  ████╗ ████║  ██╔════╝
    ██║  ███╗  █████╗    ██╔████╔██║  ███████╗
    ██║   ██║  ██╔══╝    ██║╚██╔╝██║  ╚════██║
    ╚██████╔╝  ███████╗  ██║ ╚═╝ ██║  ███████║
    ╚═════╝   ╚══════╝  ╚═╝     ╚═╝  ╚══════╝

                 好生意       好价格   

请输入股票名称或者代码，或者输入'exit'或'quit'退出。
"""
        print(welcome_text)

    def show_tasks(self, tasks: list[dict[str, Any]]):
        """显示任务列表"""
        if not tasks:
            print("暂无计划任务")
            return

        print()
        print("计划任务")
        print("-" * 40)
        for i, task in enumerate(tasks, 1):
            status = "✅" if task.get("done", False) else "【】"
            desc = task.get("description", str(task))
            print(f"{status} {i}. {desc}")
        print()

    def show_progress(self, message: str):
        """显示进度信息"""
        print(f"→ {message}")

    def show_answer(self, answer: str, answer_type: str = "general"):
        """显示答案"""
        print()
        if answer_type == "value_investment":
            print("🎯 价值投资分析报告")
        else:
            print("📊 分析结果")
        print()

        # 格式化长文本
        formatted_answer = self._format_long_text(answer)
        print(formatted_answer)
        print()

    def _format_long_text(self, text: str, max_width: int = 80) -> str:
        """
        格式化长文本，确保在终端中正确显示
        """
        import re

        wrapped_lines = []

        # 按段落分割
        paragraphs = text.split("\n\n")

        for paragraph in paragraphs:
            if not paragraph.strip():
                wrapped_lines.append("")
                continue

            # 按行分割
            lines = paragraph.split("\n")
            for line in lines:
                if len(line) <= max_width:
                    wrapped_lines.append(line)
                else:
                    # 智能换行处理
                    current_line = ""
                    words = re.split(r"(\s+)", line)  # 按空格分割，保留空格

                    for word in words:
                        if not word:
                            continue

                        # 如果当前行加上新单词不超过最大宽度
                        if len(current_line) + len(word) <= max_width:
                            current_line += word
                        else:
                            # 当前行已满，开始新行
                            if current_line:
                                wrapped_lines.append(current_line.rstrip())
                            current_line = word.lstrip()

                    # 添加最后一行
                    if current_line:
                        wrapped_lines.append(current_line.rstrip())

            # 段落之间添加空行
            wrapped_lines.append("")

        # 移除最后的空行
        if wrapped_lines and not wrapped_lines[-1]:
            wrapped_lines.pop()

        return "\n".join(wrapped_lines)


# 全局输出引擎实例
_output_engine: SimpleOutputEngine | None = None


def get_output_engine() -> SimpleOutputEngine:
    """获取或创建全局输出引擎实例"""
    global _output_engine
    if _output_engine is None:
        _output_engine = SimpleOutputEngine()
    return _output_engine


def set_output_engine(engine: SimpleOutputEngine):
    """设置全局输出引擎实例"""
    global _output_engine
    _output_engine = engine
