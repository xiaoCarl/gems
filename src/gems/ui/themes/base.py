"""
Base theme class for UI styling.
Defines color schemes and symbols for consistent theming.
"""

from typing import Dict, Any


class BaseTheme:
    """Base theme class providing default colors and symbols."""
    
    COLORS: Dict[str, str] = {
        "primary": "blue",
        "secondary": "cyan", 
        "success": "green",
        "warning": "yellow",
        "error": "red",
        "info": "dim",
        "accent": "magenta",
        "muted": "bright_black"
    }
    
    SYMBOLS: Dict[str, str] = {
        "task": "•",
        "success": "✓",
        "error": "✗", 
        "warning": "⚠",
        "info": "ℹ",
        "progress": "⏳",
        "arrow": "→",
        "check": "✓",
        "cross": "✗"
    }
    
    STYLES: Dict[str, str] = {
        "header": "bold",
        "subheader": "bold dim",
        "emphasis": "italic",
        "code": "bright_white on black",
        "highlight": "reverse"
    }
    
    def get_color(self, color_name: str) -> str:
        """Get color by name."""
        return self.COLORS.get(color_name, "white")
    
    def get_symbol(self, symbol_name: str) -> str:
        """Get symbol by name."""
        return self.SYMBOLS.get(symbol_name, "•")
    
    def get_style(self, style_name: str) -> str:
        """Get style by name."""
        return self.STYLES.get(style_name, "")
