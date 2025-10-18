"""
Main layout manager for organizing UI components.
"""

from rich.layout import Layout
from rich.console import Console


class MainLayout:
    """Main layout manager for organizing terminal UI components."""
    
    def __init__(self):
        self.layout = Layout()
        self.console = Console()
        self._setup_layout()
    
    def _setup_layout(self):
        """Setup the main layout structure."""
        # Split the layout into main areas
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=1)
        )
        
        # Split main area into content and sidebar
        self.layout["main"].split_row(
            Layout(name="content"),
            Layout(name="sidebar", size=30)
        )
    
    def update_header(self, content):
        """Update header content."""
        self.layout["header"].update(content)
    
    def update_content(self, content):
        """Update main content area."""
        self.layout["content"].update(content)
    
    def update_sidebar(self, content):
        """Update sidebar content."""
        self.layout["sidebar"].update(content)
    
    def update_footer(self, content):
        """Update footer content."""
        self.layout["footer"].update(content)
    
    def render(self):
        """Render the complete layout."""
        self.console.print(self.layout)
    
    def clear(self):
        """Clear the layout."""
        self._setup_layout()
