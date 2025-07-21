"""Basic tests for AIS."""

import subprocess
from unittest.mock import patch

import ais


def test_version():
    """Test that version is defined."""
    assert hasattr(ais, "__version__")
    assert isinstance(ais.__version__, str)
    assert len(ais.__version__) > 0


def test_cli_version():
    """Test CLI version command."""
    result = subprocess.run(["ais", "--version"], capture_output=True, text=True)
    assert result.returncode == 0
    assert ais.__version__ in result.stdout


def test_cli_help():
    """Test CLI help command."""
    result = subprocess.run(["ais", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "AIS - 上下文感知的错误分析学习助手" in result.stdout


@patch("ais.core.config.get_config")
def test_config_command(mock_get_config):
    """Test config command."""
    mock_get_config.return_value = {
        "default_provider": "test",
        "auto_analysis": True,
        "context_level": "standard",
        "sensitive_dirs": [],
    }

    result = subprocess.run(["ais", "config"], capture_output=True, text=True)
    assert result.returncode == 0


def test_import_modules():
    """Test that all modules can be imported."""
    import ais.cli.main
    import ais.core.config
    import ais.core.ai
    import ais.core.database
    import ais.core.context
    import ais.cli.interactive

    # Basic smoke test - modules should import without errors
    assert hasattr(ais.cli.main, "main")
    assert hasattr(ais.core.config, "get_config")
    assert hasattr(ais.core.ai, "ask_ai")
