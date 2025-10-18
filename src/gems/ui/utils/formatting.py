"""
Utility functions for text formatting and styling.
"""

from typing import Any
from rich.text import Text
from rich.console import Console


def format_table_data(data: Any, max_length: int = 50) -> str:
    """Format data for table display with truncation."""
    if data is None:
        return "-"
    
    text = str(data)
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def create_progress_text(current: int, total: int, message: str = "") -> Text:
    """Create progress text with percentage."""
    text = Text()
    
    if total > 0:
        percentage = (current / total) * 100
        text.append(f"{percentage:.1f}%", style="green")
        text.append(" ", style="dim")
    
    text.append(message)
    return text


def truncate_middle(text: str, max_length: int = 60) -> str:
    """Truncate text from the middle if too long."""
    if len(text) <= max_length:
        return text
    
    half = (max_length - 3) // 2
    return text[:half] + "..." + text[-half:]


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable format."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def create_status_indicator(status: str, message: str) -> Text:
    """Create a status indicator with colored icon."""
    text = Text()
    
    if status == "success":
        text.append("✓ ", style="green")
    elif status == "error":
        text.append("✗ ", style="red")
    elif status == "warning":
        text.append("⚠ ", style="yellow")
    elif status == "info":
        text.append("ℹ ", style="blue")
    elif status == "progress":
        text.append("⏳ ", style="cyan")
    else:
        text.append("• ", style="dim")
    
    text.append(message)
    return text
