"""
Answer panel component for displaying final answers and analysis results.
"""

from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from gems.ui.themes.base import BaseTheme


class AnswerPanel:
    """Component for rendering final answers in beautiful panels."""
    
    def __init__(self, theme: BaseTheme):
        self.theme = theme
        self.console = Console()
    
    def render_general_answer(self, answer: str):
        """Render a general answer in a panel."""
        panel = Panel(
            answer,
            title=f"[{self.theme.get_color('success')}]答案[/{self.theme.get_color('success')}]",
            title_align="center",
            border_style=self.theme.get_color("success"),
            padding=(1, 3)
        )
        self.console.print(panel)
    
    def render_value_investment(self, answer: str):
        """Render value investment analysis in a structured format."""
        sections = self._parse_value_investment_sections(answer)
        
        content_parts = []
        
        # 好生意部分
        if sections.get('good_business'):
            content_parts.append(f"[{self.theme.get_color('primary')}]1. 好生意（商业模式分析）[/{self.theme.get_color('primary')}]")
            content_parts.append(sections['good_business'])
            content_parts.append("")
        
        # 好价格部分
        if sections.get('good_price'):
            content_parts.append(f"[{self.theme.get_color('primary')}]2. 好价格（估值分析）[/{self.theme.get_color('primary')}]")
            content_parts.append(sections['good_price'])
            content_parts.append("")
        
        # 长期持有风险部分
        if sections.get('long_term_risk'):
            content_parts.append(f"[{self.theme.get_color('primary')}]3. 长期持有风险（风险评估）[/{self.theme.get_color('primary')}]")
            content_parts.append(sections['long_term_risk'])
            content_parts.append("")
        
        # 综合建议
        if sections.get('recommendation'):
            content_parts.append(f"[{self.theme.get_color('success')}]综合建议[/{self.theme.get_color('success')}]")
            content_parts.append(sections['recommendation'])
        
        content = "\n".join(content_parts)
        
        panel = Panel(
            content,
            title=f"[{self.theme.get_color('success')}]🎯 价值投资分析报告[/{self.theme.get_color('success')}]",
            title_align="center",
            border_style=self.theme.get_color("success"),
            padding=(1, 3)
        )
        self.console.print(panel)
    
    def _parse_value_investment_sections(self, answer: str) -> Dict[str, str]:
        """Parse value investment analysis into sections."""
        sections: Dict[str, str] = {}
        lines = answer.split('\n')
        
        current_section: Optional[str] = None
        current_content: list[str] = []
        
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
    
    def render_markdown_answer(self, answer: str):
        """Render answer as markdown."""
        markdown = Markdown(answer)
        panel = Panel(
            markdown,
            title=f"[{self.theme.get_color('success')}]答案[/{self.theme.get_color('success')}]",
            border_style=self.theme.get_color("success"),
            padding=(1, 2)
        )
        self.console.print(panel)
