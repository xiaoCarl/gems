"""
Task list component for displaying planned tasks in a structured table.
"""

from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.text import Text

from gems.ui.themes.base import BaseTheme


class TaskListComponent:
    """Component for rendering task lists in a structured table format."""
    
    def __init__(self, theme: BaseTheme):
        self.theme = theme
        self.console = Console()
    
    def render(self, tasks: List[Dict[str, Any]]):
        """Render the task list as a table."""
        if not tasks:
            return
        
        table = Table(
            show_header=True,
            header_style=f"bold {self.theme.get_color('primary')}",
            box=None,
            show_lines=True
        )
        
        table.add_column("状态", width=8, justify="center")
        table.add_column("任务描述", width=60)
        table.add_column("进度", width=12, justify="center")
        
        for task in tasks:
            status = self._get_status_icon(task.get('done', False))
            description = task.get('description', str(task))
            progress = self._render_progress_bar(task.get('progress', 0))
            
            table.add_row(status, description, progress)
        
        self.console.print(f"\n[{self.theme.get_color('primary')}]计划任务[/{self.theme.get_color('primary')}]")
        self.console.print(table)
    
    def _get_status_icon(self, is_done: bool) -> str:
        """Get the status icon for a task."""
        if is_done:
            return f"[{self.theme.get_color('success')}]{self.theme.get_symbol('success')} 完成[/{self.theme.get_color('success')}]"
        else:
            return f"[{self.theme.get_color('warning')}]待执行[/{self.theme.get_color('warning')}]"
    
    def _render_progress_bar(self, progress: float) -> str:
        """Render a simple text-based progress bar."""
        if progress >= 1.0:
            return f"[{self.theme.get_color('success')}]100%[/{self.theme.get_color('success')}]"
        elif progress > 0:
            percentage = int(progress * 100)
            return f"[{self.theme.get_color('primary')}]{percentage}%[/{self.theme.get_color('primary')}]"
        else:
            return f"[{self.theme.get_color('muted')}]0%[/{self.theme.get_color('muted')}]"
    
    def render_simple_list(self, tasks: List[Dict[str, Any]]):
        """Render a simple bullet list of tasks."""
        if not tasks:
            return
        
        self.console.print(f"\n[{self.theme.get_color('primary')}]计划任务:[/{self.theme.get_color('primary')}]")
        for i, task in enumerate(tasks, 1):
            status = self._get_status_icon(task.get('done', False))
            description = task.get('description', str(task))
            self.console.print(f"  {status} {description}")
