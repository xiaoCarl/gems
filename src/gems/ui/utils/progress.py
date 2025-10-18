"""
Progress decorator for showing operation progress with new UI system.
"""

from functools import wraps
from typing import Callable, Any
from gems.ui import get_ui


def show_progress(message: str, success_message: str = ""):
    """
    Decorator to show progress spinner while a function executes.
    Uses the new opencode-style UI system.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            ui = get_ui()
            ui.show_progress_start(message)
            try:
                result = func(*args, **kwargs)
                if success_message:
                    ui.show_progress_complete(success_message)
                return result
            except Exception as e:
                ui.show_error(f"失败: {str(e)}")
                raise
        return wrapper
    return decorator


def with_spinner(message: str):
    """
    Context manager for showing a spinner during an operation.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            ui = get_ui()
            ui.progress.show_spinner(message)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ui.show_error(f"失败: {str(e)}")
                raise
        return wrapper
    return decorator
