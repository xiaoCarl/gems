"""
GLI Logger class that uses the new TradingAgents-style interface.
"""

from typing import List, Dict, Any
from gems.gli.terminal import get_gli


class GLILogger:
    """Logger that uses the GLI interface for real-time display."""
    
    def __init__(self):
        self.gli = get_gli()
        self.log: List[str] = []

    def _log(self, msg: str):
        """Print immediately and keep in log."""
        print(msg, flush=True)
        self.log.append(msg)

    def log_header(self, msg: str):
        """Log a header message."""
        self.gli.show_info(msg)
    
    def log_info(self, msg: str):
        """Log an info message."""
        self.gli.show_info(msg)

    def log_user_query(self, query: str):
        """Log the user's query."""
        self.gli.show_query(query)

    def log_task_list(self, tasks: List[Dict[str, Any]]):
        """Log the planned task list."""
        # Convert tasks to readable format
        task_descriptions = [task.get('description', str(task)) for task in tasks]
        task_text = "\n".join([f"• {desc}" for desc in task_descriptions])
        
        self.gli.update_report_section("task_plan", f"## 计划任务\n\n{task_text}")
        self.gli.add_reasoning_message(f"任务规划完成: 已规划 {len(tasks)} 个任务")

    def log_task_start(self, task_desc: str):
        """Log when a task starts."""
        self.add_reasoning_message(f"开始执行: {task_desc}")

    def log_task_done(self, task_desc: str):
        """Log when a task is completed."""
        self.add_reasoning_message(f"完成: {task_desc}")

    def log_tool_run(self, tool: str, result: str = ""):
        """Log when a tool is executed."""
        # Only log tool results, not tool call details
        if result:
            self.gli.add_reasoning_message(f"工具执行完成: {tool}")

    def log_risky(self, tool: str, input_str: str):
        """Log risky actions."""
        self.gli.show_info(f"风险操作 {tool}({input_str}) — 已自动确认")

    def log_summary(self, summary: str):
        """Log the final summary/answer."""
        self.gli.show_final_answer(summary)
    
    def progress(self, message: str, success_message: str = ""):
        """Show progress for an operation."""
        self.add_reasoning_message(message)
        if success_message:
            self.add_reasoning_message(success_message)
    
    def add_reasoning_message(self, content: str):
        """Add reasoning message from LLM."""
        self.gli.add_reasoning_message(content)