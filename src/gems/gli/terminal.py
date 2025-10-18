"""
GLI Terminal implementation inspired by TradingAgents CLI.
Provides multi-panel real-time interface for financial analysis.
"""

import sys
import datetime
from typing import List, Dict, Any, Optional, Deque
from collections import deque
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.spinner import Spinner
from rich.markdown import Markdown
from rich.columns import Columns
from rich import box
from rich.align import Align


class MessageBuffer:
    """Buffer for storing messages and tool calls with timestamps."""
    
    def __init__(self, max_length: int = 100):
        self.messages: Deque[tuple] = deque(maxlen=max_length)
        self.tool_calls: Deque[tuple] = deque(maxlen=max_length)
        self.current_report: Optional[str] = None
        self.final_report: Optional[str] = None
        
    def add_message(self, message_type: str, content: str):
        """Add a message with timestamp."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.messages.append((timestamp, message_type, content))
        
    def add_tool_call(self, tool_name: str, args: str):
        """Add a tool call with timestamp."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.tool_calls.append((timestamp, tool_name, args))


class GLITerminal:
    """
    GLI Terminal providing TradingAgents-style multi-panel interface.
    """
    
    def __init__(self):
        self.console = Console()
        self.message_buffer = MessageBuffer()
        self.layout = self._create_layout()
        self.live: Optional[Live] = None
        self.is_interactive = sys.stdin.isatty()
        
        # Report sections
        self.report_sections = {
            "task_plan": None,
            "tool_executions": None,
            "value_analysis": None,
            "final_answer": None,
        }
        
    def _create_layout(self) -> Layout:
        """Create the three-panel layout: top row (1/3) with planning + execution, bottom (2/3) with analysis."""
        layout = Layout()
        
        # Three-panel layout: top row (1/3) + bottom row (2/3)
        layout.split_column(
            Layout(name="top_row", ratio=1),
            Layout(name="analysis", ratio=2)
        )
        
        # Top row: planning panel + execution panel
        layout["top_row"].split_row(
            Layout(name="planning", ratio=1),
            Layout(name="execution", ratio=1)
        )
        
        return layout
    
    def _update_display(self):
        """Update the three-panel display layout."""
        # Planning panel - show task planning only (vertical layout)
        planning_content = []
        
        # Add task planning information
        if self.report_sections.get("task_plan"):
            planning_content.append(self.report_sections["task_plan"])
        else:
            planning_content.append("等待任务规划...")
        
        self.layout["planning"].update(
            Panel(
                Markdown("\n".join(planning_content)) if "#" in "\n".join(planning_content) else "\n".join(planning_content),
                title="📋 计划任务",
                border_style="blue",
                padding=(1, 1),
            )
        )
        
        # Execution panel - show task execution process (without tool call details)
        execution_content = []
        
        # Add reasoning messages (planning process)
        reasoning_messages = []
        for timestamp, msg_type, content in self.message_buffer.messages:
            if msg_type in ["推理", "信息", "系统"]:
                content_str = str(content)
                if len(content_str) > 80:
                    content_str = content_str[:77] + "..."
                reasoning_messages.append(f"[{timestamp}] {content_str}")
        
        if reasoning_messages:
            execution_content.append("## 规划过程")
            execution_content.extend(reasoning_messages[-10:])  # Show last 10 reasoning messages
        
        # Add tool results only (no tool call details)
        tool_results = []
        for timestamp, msg_type, content in self.message_buffer.messages:
            if msg_type == "工具结果":
                content_str = str(content)
                if len(content_str) > 60:
                    content_str = content_str[:57] + "..."
                tool_results.append(f"[{timestamp}] 📋 {content_str}")
        
        if tool_results:
            execution_content.append("\n## 执行结果")
            execution_content.extend(tool_results[-8:])  # Show last 8 tool results
        
        if not execution_content:
            execution_content.append("等待执行过程...")
            
        self.layout["execution"].update(
            Panel(
                Markdown("\n".join(execution_content)) if "#" in "\n".join(execution_content) else "\n".join(execution_content),
                title="⚡ 计划执行过程",
                border_style="magenta",
                padding=(1, 1),
            )
        )
        
        # Analysis panel - show final analysis conclusions
        if self.message_buffer.current_report:
            analysis_content = self.message_buffer.current_report
        else:
            analysis_content = "等待分析结果结论..."
            
        self.layout["analysis"].update(
            Panel(
                Markdown(analysis_content) if "#" in analysis_content else analysis_content,
                title="🎯 最终分析结果结论",
                border_style="green",
                padding=(1, 1),
            )
        )
    
    def start_live_display(self):
        """Start the live display."""
        self.live = Live(self.layout, refresh_per_second=4, console=self.console)
        self.live.start()
        self._update_display()
        
    def stop_live_display(self):
        """Stop the live display."""
        if self.live:
            self.live.stop()
            self.live = None
    
    def show_welcome(self):
        """Display welcome screen."""
        welcome_content = """
╔══════════════════════════════════════════════════╗
║                   价值投资分析                    ║
╚══════════════════════════════════════════════════╝

      Great Enterprises at Moderate Prices 
    
    ██████╗    ███████╗  ███╗   ███╗  ███████╗
    ██╔════╝   ██╔════╝  ████╗ ████║  ██╔════╝
    ██║  ███╗  █████╗    ██╔████╔██║  ███████╗
    ██║   ██║  ██╔══╝    ██║╚██╔╝██║  ╚════██║
    ╚██████╔╝  ███████╗  ██║ ╚═╝ ██║  ███████║
     ╚═════╝   ╚══════╝  ╚═╝     ╚═╝  ╚══════╝
    
              好生意，好价格，长期持有   
        
您的AI金融分析助手。
请提出任何问题。输入'exit'或'quit'退出。
        """
        
        welcome_box = Panel(
            welcome_content,
            border_style="green",
            padding=(1, 2),
            title="🎯 Gems Agent - 价值投资分析",
            subtitle="多智能体金融分析框架",
        )
        self.console.print(Align.center(welcome_box))
        self.console.print()
    
    def show_query(self, query: str):
        """Display user query."""
        self.console.print()
        self.console.print(
            Panel(
                f"👤 {query}",
                title="[bold]用户查询[/bold]",
                border_style="blue",
                padding=(1, 2),
            )
        )
        self.console.print()
        
        # Add to message buffer
        self.message_buffer.add_message("用户", query)
        
    def update_report_section(self, section_name: str, content: str):
        """Update a report section."""
        if section_name in self.report_sections:
            self.report_sections[section_name] = content
            self.message_buffer.current_report = content
            self._update_display()
            
    def add_tool_execution(self, tool_name: str, args: str, result: str):
        """Add tool execution to display."""
        # Add to tool calls
        self.message_buffer.add_tool_call(tool_name, args)
        
        # Add result as message
        result_display = str(result)[:300] + "..." if len(str(result)) > 300 else str(result)
        self.message_buffer.add_message("工具结果", result_display)
        
        self._update_display()
        
    def add_reasoning_message(self, content: str):
        """Add reasoning message from LLM."""
        self.message_buffer.add_message("推理", content)
        self._update_display()
        
    def show_final_answer(self, answer: str):
        """Display final answer."""
        # Update final report
        self.report_sections["final_answer"] = answer
        self.message_buffer.current_report = answer
        
        # Add final message
        self.message_buffer.add_message("系统", "分析完成")
        
        self._update_display()
        
        # Also print the final answer in a nice panel
        self.console.print()
        if any(keyword in answer for keyword in ["好生意", "好价格", "长期持有风险"]):
            # Value investment format
            self.console.print(
                Panel(
                    Markdown(answer),
                    title="🎯 价值投资分析报告",
                    border_style="green",
                    padding=(1, 2),
                )
            )
        else:
            # General format
            self.console.print(
                Panel(
                    answer,
                    title="📊 分析结果",
                    border_style="blue",
                    padding=(1, 2),
                )
            )
    
    def show_error(self, message: str):
        """Display error message."""
        self.message_buffer.add_message("错误", message)
        self._update_display()
        
    def show_info(self, message: str):
        """Display info message."""
        self.message_buffer.add_message("信息", message)
        self._update_display()


# Global GLI instance for easy access
_gli_instance: Optional[GLITerminal] = None


def get_gli() -> GLITerminal:
    """Get or create the global GLI instance."""
    global _gli_instance
    if _gli_instance is None:
        _gli_instance = GLITerminal()
    return _gli_instance


def set_gli(gli: GLITerminal):
    """Set the global GLI instance."""
    global _gli_instance
    _gli_instance = gli