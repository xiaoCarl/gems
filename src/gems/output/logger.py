"""
简单日志接口

提供最基本的日志功能，移除所有rich依赖。
"""

from typing import List, Dict, Any, Optional


class SimpleLogger:
    """
    简单日志器
    
    提供最基本的日志功能，使用简单print语句。
    """
    
    def __init__(self):
        self.log: List[str] = []
    
    def _log(self, msg: str):
        """立即打印并记录到日志"""
        print(msg, flush=True)
        self.log.append(msg)
    
    def log_header(self, msg: str):
        """记录标题消息"""
        print(f"ℹ {msg}")
    
    def log_user_query(self, query: str):
        """记录用户查询"""
        print()
        print("您")
        print()
        print(query)
        print()
    
    def log_task_list(self, tasks: List[Dict[str, Any]]):
        """记录任务列表"""
        if not tasks:
            print("暂无计划任务")
            return
        
        print()
        print("计划任务")
        print("-" * 40)
        for i, task in enumerate(tasks, 1):
            status = "✅" if task.get('done', False) else "⏳"
            desc = task.get('description', str(task))
            print(f"{status} {i}. {desc}")
        print()
    
    def log_task_start(self, task_desc: str):
        """记录任务开始"""
        print(f"→ 开始执行: {task_desc}")
    
    def log_task_done(self, task_desc: str):
        """记录任务完成"""
        print(f"→ 完成: {task_desc}")
    
    def log_tool_run(self, tool: str, result: str = ""):
        """记录工具执行"""
        if result:
            print(f"→ 工具执行完成: {tool}")
    
    def log_risky(self, tool: str, input_str: str):
        """记录风险操作"""
        print(f"⚠ 风险操作 {tool}({input_str}) — 已自动确认")
    
    def log_summary(self, summary: str):
        """记录最终总结/答案"""
        # 检测是否为价值投资分析
        if any(keyword in summary for keyword in ["好生意", "好价格", "长期持有风险"]):
            print()
            print("🎯 价值投资分析报告")
        else:
            print()
            print("📊 分析结果")
        print()
        
        # 格式化长文本
        formatted_summary = self._format_long_text(summary)
        print(formatted_summary)
        print()
    
    def progress(self, message: str, success_message: str = ""):
        """显示操作进度"""
        print(f"→ {message}")
        if success_message:
            print(f"→ {success_message}")
    
    def add_reasoning_message(self, content: str):
        """添加推理消息"""
        print(f"→ {content}")
    
    def _format_long_text(self, text: str, max_width: int = 80) -> str:
        """
        格式化长文本，确保在终端中正确显示
        """
        import re
        
        wrapped_lines = []
        
        # 按段落分割
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                wrapped_lines.append('')
                continue
                
            # 按行分割
            lines = paragraph.split('\n')
            for line in lines:
                if len(line) <= max_width:
                    wrapped_lines.append(line)
                else:
                    # 智能换行处理
                    current_line = ""
                    words = re.split(r'(\s+)', line)  # 按空格分割，保留空格
                    
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
            wrapped_lines.append('')
        
        # 移除最后的空行
        if wrapped_lines and not wrapped_lines[-1]:
            wrapped_lines.pop()
            
        return '\n'.join(wrapped_lines)


# 全局日志器实例
_logger_instance: Optional[SimpleLogger] = None


def get_logger() -> SimpleLogger:
    """获取或创建全局日志器实例"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = SimpleLogger()
    return _logger_instance


def set_logger(logger: SimpleLogger):
    """设置全局日志器实例"""
    global _logger_instance
    _logger_instance = logger