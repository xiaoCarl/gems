"""
Rich-based UI components for Gems agent.
Provides beautiful terminal output using Rich library.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import print as rprint


class RichUI:
    """Interactive UI for displaying agent progress and results using Rich."""
    
    def __init__(self):
        self.console = Console()
    
    def print_header(self, text: str):
        """Print a section header."""
        self.console.print(f"\n[bold blue]╭─ {text}[/bold blue]")
    
    def print_user_query(self, query: str):
        """Print the user's query."""
        self.console.print(f"\n[bold cyan]您:[/bold cyan] {query}\n")
    
    def print_task_list(self, tasks):
        """Print a clean list of planned tasks using Rich Table."""
        if not tasks:
            return
            
        table = Table(show_header=True, header_style="bold blue", box=None)
        table.add_column("状态", width=8, justify="center")
        table.add_column("任务描述")
        
        for task in tasks:
            status = "[green]✓[/green]" if task.get('done', False) else "[yellow]⏳[/yellow]"
            desc = task.get('description', str(task))
            table.add_row(status, desc)
        
        self.console.print("\n[bold blue]计划任务[/bold blue]")
        self.console.print(table)
    
    def print_task_start(self, task_desc: str):
        """Print when starting a task."""
        self.console.print(f"\n[bold cyan]▶ 任务:[/bold cyan] {task_desc}")
    
    def print_task_done(self, task_desc: str):
        """Print when a task is completed."""
        self.console.print(f"[green]  ✓ 完成[/green] [dim]│ {task_desc}[/dim]")
    
    def print_tool_run(self, tool_name: str, args: str = ""):
        """Print when a tool is executed."""
        args_display = f" [dim]({args[:50]}...)[/dim]" if args and len(args) > 0 else ""
        self.console.print(f"  [yellow]⚡[/yellow] {tool_name}{args_display}")
    
    def print_answer(self, answer: str):
        """Print the final answer in a beautiful panel."""
        # 检测是否为价值投资分析格式
        if any(keyword in answer for keyword in ["好生意", "好价格", "长期持有风险"]):
            self._print_value_investment_answer(answer)
        else:
            self._print_general_answer(answer)
    
    def _print_general_answer(self, answer: str):
        """Print general answers in a panel."""
        panel = Panel(
            answer,
            title="[bold blue]答案[/bold blue]",
            title_align="center",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    def _print_value_investment_answer(self, answer: str):
        """Print value investment analysis in a structured format."""
        # 解析价值投资三方面分析
        sections = self._parse_value_investment_sections(answer)
        
        content_parts = []
        
        # 好生意部分
        if sections.get('good_business'):
            content_parts.append("[bold cyan]1. 好生意（商业模式分析）[/bold cyan]")
            content_parts.append(sections['good_business'])
            content_parts.append("")
        
        # 好价格部分
        if sections.get('good_price'):
            content_parts.append("[bold cyan]2. 好价格（估值分析）[/bold cyan]")
            content_parts.append(sections['good_price'])
            content_parts.append("")
        
        # 长期持有风险部分
        if sections.get('long_term_risk'):
            content_parts.append("[bold cyan]3. 长期持有风险（风险评估）[/bold cyan]")
            content_parts.append(sections['long_term_risk'])
            content_parts.append("")
        
        # 综合建议
        if sections.get('recommendation'):
            content_parts.append("[bold green]综合建议[/bold green]")
            content_parts.append(sections['recommendation'])
        
        content = "\n".join(content_parts)
        
        panel = Panel(
            content,
            title="[bold green]价值投资分析报告[/bold green]",
            title_align="center",
            border_style="green",
            padding=(1, 3)
        )
        self.console.print(panel)
    
    def _parse_value_investment_sections(self, answer: str):
        """Parse value investment analysis into sections."""
        sections = {}
        lines = answer.split('\n')
        
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            # 检测章节标题
            if "好生意" in line and "商业模式" in line:
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'good_business'
                current_content = []
            elif "好价格" in line and "估值" in line:
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'good_price'
                current_content = []
            elif "长期持有风险" in line and "风险" in line:
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'long_term_risk'
                current_content = []
            elif "综合建议" in line or "建议" in line:
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'recommendation'
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # 处理最后一个章节
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def print_info(self, message: str):
        """Print an info message."""
        self.console.print(f"[dim]{message}[/dim]")
    
    def print_error(self, message: str):
        """Print an error message."""
        self.console.print(f"[red]✗ 错误:[/red] {message}")
    
    def print_warning(self, message: str):
        """Print a warning message."""
        self.console.print(f"[yellow]⚠ 警告:[/yellow] {message}")


def show_progress(message: str, success_message: str = ""):
    """Decorator to show progress spinner while a function executes."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            ui = RichUI()
            ui.console.print(f"[cyan]⏳ {message}[/cyan]")
            try:
                result = func(*args, **kwargs)
                if success_message:
                    ui.console.print(f"[green]✓ {success_message}[/green]")
                return result
            except Exception as e:
                ui.console.print(f"[red]✗ 失败: {str(e)}[/red]")
                raise
        return wrapper
    return decorator