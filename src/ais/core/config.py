"""Configuration management for AIS."""

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
                "api_key": (
                    "sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg"
                ),
            }
        },
        "advanced": {
            "max_context_length": 4000,
            "async_analysis": True,
            "cache_analysis": True,
        },
    }


def get_config() -> Dict[str, Any]:
    """Get the current configuration."""
    config_path = get_config_path()

    try:
        if config_path.exists():
            with open(config_path, "r") as f:
                config = toml.load(f)

            # Merge with defaults
            default_config = get_default_config()
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config
    except Exception:
        pass

    # Fallback to default and save
    config = get_default_config()
    save_config(config)
    return config


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    config_path = get_config_path()

    with open(config_path, "w") as f:
        toml.dump(config, f)


def set_config(key: str, value: Any) -> None:
    """设置配置项。"""
    config = get_config()
    config[key] = value
    save_config(config)


def _validate_provider_exists(config: Dict[str, Any], name: str) -> None:
    """验证提供商是否存在。"""
    if name not in config.get("providers", {}):
        raise ValueError(f"提供商 '{name}' 不存在")


def add_provider(
    name: str, base_url: str, model_name: str, api_key: str = None
) -> None:
    """添加新的 AI 服务商。"""
    config = get_config()

    if "providers" not in config:
        config["providers"] = {}

    provider = {"base_url": base_url, "model_name": model_name}
    if api_key:
        provider["api_key"] = api_key

    config["providers"][name] = provider
    save_config(config)


def remove_provider(name: str) -> None:
    """删除 AI 服务商。"""
    config = get_config()
    _validate_provider_exists(config, name)

    if name == config.get("default_provider"):
        raise ValueError("不能删除当前使用的默认提供商")

    del config["providers"][name]
    save_config(config)


def use_provider(name: str) -> None:
    """切换默认 AI 服务商。"""
    config = get_config()
    _validate_provider_exists(config, name)
    config["default_provider"] = name
    save_config(config)
