"""
Header component for displaying welcome screens and queries.
"""

from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

from gems.ui.themes.base import BaseTheme


class HeaderComponent:
    """Component for rendering headers and welcome screens."""
    
    def __init__(self, theme: BaseTheme):
        self.theme = theme
        self.console = Console()
    
    def render_welcome(self):
        """Render the welcome screen with Gems branding."""
        # Create ASCII art banner
        banner = Text()
        banner.append("\n")
        banner.append("╔══════════════════════════════════════════════════╗\n", style=self.theme.get_style("border"))
        banner.append("║", style=self.theme.get_style("border"))
        banner.append("                    ", style=self.theme.get_style("border"))
        banner.append("价值投资分析", style=f"bold {self.theme.get_color('primary')}")
        banner.append("                    ║\n", style=self.theme.get_style("border"))
        banner.append("╚══════════════════════════════════════════════════╝\n", style=self.theme.get_style("border"))
        
        # Gems ASCII art
        gems_art = """
      Great Enterprises at Moderate Prices 
    
    ██████╗    ███████╗  ███╗   ███╗  ███████╗
    ██╔════╝   ██╔════╝  ████╗ ████║  ██╔════╝
    ██║  ███╗  █████╗    ██╔████╔██║  ███████╗
    ██║   ██║  ██╔══╝    ██║╚██╔╝██║  ╚════██║
    ╚██████╔╝  ███████╗  ██║ ╚═╝ ██║  ███████║
     ╚═════╝   ╚══════╝  ╚═╝     ╚═╝  ╚══════╝
    
              好生意，好价格，长期持有   
        """
        
        banner.append(gems_art, style=f"bold {self.theme.get_color('primary')}")
        banner.append("\n")
        banner.append("您的AI金融分析助手。", style=self.theme.get_style("subheader"))
        banner.append("\n")
        banner.append("请提出任何问题。输入'exit'或'quit'退出。", style=self.theme.get_style("info"))
        banner.append("\n")
        
        self.console.print(banner)
    
    def render_query(self, query: str):
        """Render the user's query in a styled format."""
        panel = Panel(
            query,
            title=f"[{self.theme.get_color('primary')}]您[/{self.theme.get_color('primary')}]",
            title_align="left",
            border_style=self.theme.get_color("primary"),
            padding=(0, 2)
        )
        self.console.print(panel)
    
    def render_section_header(self, title: str, subtitle: Optional[str] = None):
        """Render a section header."""
        text = Text()
        text.append(f"{self.theme.get_symbol('arrow')} ", style=self.theme.get_color("primary"))
        text.append(title, style=self.theme.get_style("header"))
        
        if subtitle:
            text.append("\n")
            text.append(subtitle, style=self.theme.get_style("subheader"))
        
        self.console.print(text)
        self.console.print()
