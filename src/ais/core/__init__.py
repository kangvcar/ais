"""Core functionality modules for AIS."""

from .ai import ask_ai, analyze_error
from .config import (
    get_config,
    set_config,
    add_provider,
    remove_provider,
    use_provider,
)
from .context import collect_context
from .database import save_command_log, get_recent_logs, get_similar_commands

__all__ = [
    "ask_ai",
    "analyze_error",
    "get_config",
    "set_config",
    "add_provider",
    "remove_provider",
    "use_provider",
    "collect_context",
    "save_command_log",
    "get_recent_logs",
    "get_similar_commands",
]
