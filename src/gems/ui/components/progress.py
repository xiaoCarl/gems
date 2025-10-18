"""
Progress indicator component for showing task progress and loading states.
"""

import time
from typing import Optional
from rich.console import Console
from rich.text import Text

from gems.ui.themes.base import BaseTheme


class ProgressIndicator:
    """Component for displaying progress indicators and loading animations."""
    
    def __init__(self, theme: BaseTheme):
        self.theme = theme
        self.console = Console()
        
    def start_task(self, message: str):
        """Start showing progress for a task."""
        self.show_simple_progress(message)
    
    def update_progress(self, progress: float, message: Optional[str] = None):
        """Update progress for the current task."""
        if message:
            self.show_simple_progress(f"{message} ({int(progress * 100)}%)")
    
    def complete_task(self, message: str):
        """Mark the current task as complete."""
        self.show_simple_progress(message, f"完成: {message}")
    
    def show_spinner(self, message: str):
        """Show a simple spinner for short operations."""
        with self.console.status(f"[{self.theme.get_color('primary')}]{self.theme.get_symbol('progress')} {message}[/{self.theme.get_color('primary')}]"):
            # This will show the spinner until the context manager exits
            pass
    
    def show_simple_progress(self, message: str, success_message: str = ""):
        """Show a simple progress message without full progress bar."""
        self.console.print(f"[{self.theme.get_color('primary')}]{self.theme.get_symbol('progress')} {message}[/{self.theme.get_color('primary')}]")
        if success_message:
            self.console.print(f"[{self.theme.get_color('success')}]{self.theme.get_symbol('success')} {success_message}[/{self.theme.get_color('success')}]")
    
    def stop_all(self):
        """Stop all progress indicators."""
        # No-op for simple implementation
        pass