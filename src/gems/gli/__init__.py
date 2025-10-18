"""
GLI (Graphical Line Interface) module for Gems agent.
Provides TradingAgents-style interactive terminal interface.
"""

from gems.gli.terminal import GLITerminal, get_gli, set_gli
from gems.gli.logger import GLILogger

__all__ = [
    "GLITerminal",
    "get_gli", 
    "set_gli",
    "GLILogger"
]