"""Configuration management for AIS."""

import os
import toml
from pathlib import Path
from typing import Any, Dict


def get_config_path() -> Path:
    """Get the configuration file path."""
    config_dir = Path.home() / ".config" / "ais"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.toml"


def get_default_config() -> Dict[str, Any]:
    """Get the default configuration."""
    return {
        "default_provider": "default_free",
        "auto_analysis": True,
        "context_level": "standard",
        "sensitive_dirs": ["~/.ssh", "~/.config/ais", "~/.aws"],
        "ui": {
            "enable_colors": True,
            "enable_streaming": True,
            "max_history_display": 10,
        },
        "providers": {
            "default_free": {
                "base_url": "https://api.deepbricks.ai/v1/chat/completions",
                "model_name": "gpt-4o-mini",
                "api_key": "sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg",
            }
        },
        "advanced": {
            "max_context_length": 4000,
            "async_analysis": True,
            "cache_analysis": True,
        }
    }


def get_config() -> Dict[str, Any]:
    """Get the current configuration."""
    config_path = get_config_path()
    
    if not config_path.exists():
        config = get_default_config()
        save_config(config)
        return config
    
    try:
        with open(config_path, "r") as f:
            config = toml.load(f)
        
        # Merge with defaults to ensure all keys exist
        default_config = get_default_config()
        for key, value in default_config.items():
            if key not in config:
                config[key] = value
        
        return config
    except Exception:
        return get_default_config()


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    config_path = get_config_path()
    
    with open(config_path, "w") as f:
        toml.dump(config, f)


def set_config(key: str, value: Any) -> None:
    """Set a configuration value."""
    config = get_config()
    config[key] = value
    save_config(config)