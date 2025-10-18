"""
Tool output component for displaying tool execution details and results.
"""

from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

from gems.ui.themes.base import BaseTheme


class ToolOutputComponent:
    """Component for rendering tool execution information and results."""
    
    def __init__(self, theme: BaseTheme):
        self.theme = theme
        self.console = Console()
    
    def render(self, tool_name: str, args: str, result: str):
        """Render tool execution with arguments and results."""
        # Create the main content
        content = Text()
        
        # Tool name and execution indicator
        content.append(f"{self.theme.get_symbol('arrow')} ", style=self.theme.get_color('primary'))
        content.append("执行工具: ", style=self.theme.get_style("subheader"))
        content.append(tool_name, style=self.theme.get_style("header"))
        content.append("\n")
        
        # Arguments (truncated if too long)
        if args:
            args_display = str(args)[:100] + "..." if len(str(args)) > 100 else str(args)
            content.append("  参数: ", style=self.theme.get_style("subheader"))
            content.append(args_display, style=self.theme.get_color("muted"))
            content.append("\n")
        
        # Results (truncated and formatted)
        if result:
            result_display = self._format_result(result)
            content.append("  结果: ", style=self.theme.get_style("subheader"))
            content.append("\n")
            content.append(result_display, style=self.theme.get_color("info"))
        
        # Create panel
        panel = Panel(
            content,
            title=f"[{self.theme.get_color('primary')}]工具执行[/{self.theme.get_color('primary')}]",
            border_style=self.theme.get_color("primary"),
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    def _format_result(self, result: str) -> str:
        """Format the result for display."""
        # Truncate very long results
        if len(result) > 500:
            return result[:500] + "... [结果已截断]"
        
        # Try to format as JSON if it looks like JSON
        if result.strip().startswith('{') or result.strip().startswith('['):
            try:
                import json
                parsed = json.loads(result)
                return json.dumps(parsed, indent=2, ensure_ascii=False)
            except:
                pass
        
        return result
    
    def render_simple(self, tool_name: str, args: Optional[str] = None):
        """Render a simple tool execution indicator."""
        args_display = f" [{self.theme.get_color('muted')}]({str(args)[:50]}...)[/{self.theme.get_color('muted')}]" if args and len(str(args)) > 0 else ""
        self.console.print(f"  [{self.theme.get_color('primary')}]{self.theme.get_symbol('arrow')}[/{self.theme.get_color('primary')}] {tool_name}{args_display}")
