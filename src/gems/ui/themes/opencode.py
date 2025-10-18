"""
OpenCode style theme implementation.
Mimics the visual style of opencode.ai terminal interface.
"""

from .base import BaseTheme


class OpenCodeTheme(BaseTheme):
    """OpenCode style theme with distinctive green color scheme."""
    
    COLORS = {
        "primary": "#00D4AA",      # OpenCode green
        "secondary": "#6B7280",    # Gray
        "success": "#10B981",      # Success green
        "warning": "#F59E0B",      # Warning amber
        "error": "#EF4444",        # Error red
        "info": "#9CA3AF",         # Info gray
        "accent": "#8B5CF6",       # Accent purple
        "muted": "#6B7280"         # Muted gray
    }
    
    SYMBOLS = {
        "task": "•",
        "success": "✓",
        "error": "✗", 
        "warning": "⚠",
        "info": "ℹ",
        "progress": "⏳",
        "arrow": "→",
        "check": "✓",
        "cross": "✗",
        "spinner": "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    }
    
    STYLES = {
        "header": "bold #00D4AA",
        "subheader": "bold #6B7280",
        "emphasis": "italic #9CA3AF",
        "code": "bright_white on #1F2937",
        "highlight": "reverse #00D4AA",
        "border": "#00D4AA",
        "panel": "#00D4AA"
    }
    
    def __init__(self):
        super().__init__()
        # Override with OpenCode specific values
        self.COLORS.update(self.COLORS)
        self.SYMBOLS.update(self.SYMBOLS)
        self.STYLES.update(self.STYLES)
