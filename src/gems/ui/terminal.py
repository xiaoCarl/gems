"""
Terminal UI implementation mimicking opencode/Claudecode style.
Provides modern, interactive terminal interface for the Gems agent.
"""

import sys
from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.layout import Layout

from gems.ui.themes.base import BaseTheme
from gems.ui.themes.opencode import OpenCodeTheme
from gems.ui.layouts.main import MainLayout
from gems.ui.components.header import HeaderComponent
from gems.ui.components.progress import ProgressIndicator
from gems.ui.components.task_list import TaskListComponent
from gems.ui.components.tool_output import ToolOutputComponent
from gems.ui.components.answer_panel import AnswerPanel


class TerminalUI:
    """
    Main terminal interface class providing opencode/Claudecode style UI.
    """
    
    def __init__(self, theme: str = "opencode"):
        self.console = Console()
        self.theme = self._load_theme(theme)
        self.layout = MainLayout()
        self.header = HeaderComponent(self.theme)
        self.progress = ProgressIndicator(self.theme)
        self.task_list = TaskListComponent(self.theme)
        self.tool_output = ToolOutputComponent(self.theme)
        self.answer_panel = AnswerPanel(self.theme)
        self.is_interactive = sys.stdin.isatty()
        
    def _load_theme(self, theme_name: str) -> BaseTheme:
        """Load the specified theme."""
        if theme_name == "opencode":
            return OpenCodeTheme()
        elif theme_name == "claudecode":
            # TODO: Implement ClaudeCode theme
            return OpenCodeTheme()  # Fallback for now
        else:
            return OpenCodeTheme()  # Default to opencode
    
    def show_welcome(self):
        """Display the welcome screen with branding."""
        self.console.clear()
        self.header.render_welcome()
        self.console.print()
    
    def show_query(self, query: str):
        """Display the user's query in a styled format."""
        self.console.print()
        self.header.render_query(query)
        self.console.print()
    
    def show_task_planning(self, tasks: List[Dict[str, Any]]):
        """Display the planned tasks in a structured table."""
        self.console.print()
        self.task_list.render(tasks)
        self.console.print()
    
    def show_progress_start(self, message: str):
        """Start showing progress for an operation."""
        self.progress.start_task(message)
    
    def show_progress_update(self, progress: float, message: str):
        """Update progress for current operation."""
        self.progress.update_progress(progress, message)
    
    def show_progress_complete(self, message: str):
        """Mark current operation as complete."""
        self.progress.complete_task(message)
    
    def show_tool_execution(self, tool_name: str, args: str, result: str):
        """Display tool execution with arguments and results."""
        self.tool_output.render(tool_name, args, result)
    
    def show_answer(self, answer: str, analysis_type: str = "general"):
        """Display the final answer in a beautiful panel."""
        self.console.print()
        if analysis_type == "value_investment":
            self.answer_panel.render_value_investment(answer)
        else:
            self.answer_panel.render_general_answer(answer)
        self.console.print()
    
    def show_error(self, message: str):
        """Display an error message."""
        self.console.print(f"\n[{self.theme.COLORS['error']}]✗ 错误:[/{self.theme.COLORS['error']}] {message}")
    
    def show_warning(self, message: str):
        """Display a warning message."""
        self.console.print(f"\n[{self.theme.COLORS['warning']}]⚠ 警告:[/{self.theme.COLORS['warning']}] {message}")
    
    def show_info(self, message: str):
        """Display an informational message."""
        self.console.print(f"\n[{self.theme.COLORS['info']}]ℹ {message}[/{self.theme.COLORS['info']}]")
    
    def clear_screen(self):
        """Clear the terminal screen."""
        self.console.clear()
    
    def get_user_input(self, prompt: str = ">> ") -> str:
        """Get input from the user with a styled prompt."""
        if self.is_interactive:
            return input(f"[{self.theme.COLORS['primary']}]{prompt}[/{self.theme.COLORS['primary']}]")
        else:
            return input(prompt)


# Global UI instance for easy access
_ui_instance: Optional[TerminalUI] = None


def get_ui(theme: str = "opencode") -> TerminalUI:
    """Get or create the global UI instance."""
    global _ui_instance
    if _ui_instance is None:
        _ui_instance = TerminalUI(theme)
    return _ui_instance


def set_ui(ui: TerminalUI):
    """Set the global UI instance."""
    global _ui_instance
    _ui_instance = ui
