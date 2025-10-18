"""
Logger class that uses the new opencode-style UI system.
"""

from typing import List, Dict, Any
from gems.ui.terminal import get_ui


class Logger:
    """Logger that uses the new opencode-style interactive UI system."""
    
    def __init__(self):
        self.ui = get_ui()
        self.log: List[str] = []

    def _log(self, msg: str):
        """Print immediately and keep in log."""
        print(msg, flush=True)
        self.log.append(msg)

    def log_header(self, msg: str):
        """Log a header message."""
        self.ui.show_info(msg)
    
    def log_user_query(self, query: str):
        """Log the user's query."""
        self.ui.show_query(query)

    def log_task_list(self, tasks: List[Dict[str, Any]]):
        """Log the planned task list."""
        self.ui.show_task_planning(tasks)

    def log_task_start(self, task_desc: str):
        """Log when a task starts."""
        self.ui.show_progress_start(f"开始执行: {task_desc}")

    def log_task_done(self, task_desc: str):
        """Log when a task is completed."""
        self.ui.show_progress_complete(f"完成: {task_desc}")

    def log_tool_run(self, tool: str, result: str = ""):
        """Log when a tool is executed."""
        self.ui.show_tool_execution(tool, "", str(result))

    def log_risky(self, tool: str, input_str: str):
        """Log risky actions."""
        self.ui.show_warning(f"风险操作 {tool}({input_str}) — 已自动确认")

    def log_summary(self, summary: str):
        """Log the final summary/answer."""
        # Detect if this is a value investment analysis
        if any(keyword in summary for keyword in ["好生意", "好价格", "长期持有风险"]):
            self.ui.show_answer(summary, "value_investment")
        else:
            self.ui.show_answer(summary, "general")
    
    def progress(self, message: str, success_message: str = ""):
        """Show progress for an operation."""
        self.ui.show_progress_start(message)
        if success_message:
            self.ui.show_progress_complete(success_message)
