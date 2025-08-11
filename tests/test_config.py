"""Tests for config module."""

from pathlib import Path
from unittest.mock import patch, mock_open
import toml
import pytest

from ais.core.config import (
    get_config_path,
    get_default_config,
    get_config,
    save_config,
    set_config,
    add_provider,
    remove_provider,
    use_provider,
    _validate_provider_exists,
)


class TestConfigPath:
    """Test configuration path functions."""

    def test_get_config_path(self):
        """Test getting configuration file path."""
        with patch("pathlib.Path.home") as mock_home:
            mock_home.return_value = Path("/home/test")

            config_path = get_config_path()

            assert config_path == Path("/home/test/.config/ais/config.toml")


class TestDefaultConfig:
    """Test default configuration."""

    def test_get_default_config(self):
        """Test getting default configuration."""
        config = get_default_config()

        assert isinstance(config, dict)
        assert config["default_provider"] == "free"
        assert config["auto_analysis"] is True
        assert config["context_level"] == "standard"
        assert "providers" in config
        assert "free" in config["providers"]


class TestConfigOperations:
    """Test configuration operations."""

    def test_save_config(self):
        """Test saving configuration."""
        test_config = {"test": "value"}

        with patch("ais.core.config.get_config_path") as mock_path:
            mock_path.return_value = Path("/tmp/test_config.toml")

            with patch("builtins.open", mock_open()) as mock_file:
                save_config(test_config)

                mock_file.assert_called_once_with(Path("/tmp/test_config.toml"), "w")

    def test_get_config_existing_file(self):
        """Test getting configuration from existing file."""
        test_config = {"existing": "config"}

        with patch("ais.core.config.get_config_path") as mock_path:
            mock_path.return_value = Path("/tmp/existing_config.toml")

            with patch("pathlib.Path.exists", return_value=True):
                with patch(
                    "builtins.open",
                    mock_open(read_data=toml.dumps(test_config)),
                ):
                    config = get_config()

                    # Should merge with defaults
                    assert "existing" in config
                    assert "default_provider" in config  # from defaults

    def test_get_config_no_file(self):
        """Test getting configuration when no file exists."""
        with patch("ais.core.config.get_config_path") as mock_path:
            mock_path.return_value = Path("/tmp/nonexistent_config.toml")

            with patch("pathlib.Path.exists", return_value=False):
                with patch("ais.core.config.save_config") as mock_save:
                    config = get_config()

                    # Should return defaults and save them
                    assert config == get_default_config()
                    mock_save.assert_called_once()

    def test_get_config_file_error(self):
        """Test getting configuration when file reading fails."""
        with patch("ais.core.config.get_config_path") as mock_path:
            mock_path.return_value = Path("/tmp/error_config.toml")

            with patch("pathlib.Path.exists", return_value=True):
                with patch("builtins.open", side_effect=Exception("Read error")):
                    with patch("ais.core.config.save_config") as mock_save:
                        config = get_config()

                        # Should fallback to defaults
                        assert config == get_default_config()
                        mock_save.assert_called_once()

    def test_set_config(self):
        """Test setting configuration value."""
        with patch("ais.core.config.get_config") as mock_get:
            with patch("ais.core.config.save_config") as mock_save:
                mock_get.return_value = {"existing": "value"}

                set_config("new_key", "new_value")

                mock_save.assert_called_once()
                saved_config = mock_save.call_args[0][0]
                assert saved_config["new_key"] == "new_value"


class TestProviderOperations:
    """Test provider management operations."""

    def test_validate_provider_exists_success(self):
        """Test validating existing provider."""
        config = {"providers": {"test_provider": {}}}

        # Should not raise exception
        _validate_provider_exists(config, "test_provider")

    def test_validate_provider_exists_failure(self):
        """Test validating non-existent provider."""
        config = {"providers": {}}

        with pytest.raises(ValueError, match="提供商 'nonexistent' 不存在"):
            _validate_provider_exists(config, "nonexistent")

    def test_add_provider_basic(self):
        """Test adding basic provider."""
        with patch("ais.core.config.get_config") as mock_get:
            with patch("ais.core.config.save_config") as mock_save:
                mock_get.return_value = {"providers": {}}

                add_provider("test_provider", "http://test.com", "test_model")

                mock_save.assert_called_once()
                saved_config = mock_save.call_args[0][0]
                provider = saved_config["providers"]["test_provider"]
                assert provider["base_url"] == "http://test.com"
                assert provider["model_name"] == "test_model"
                assert "api_key" not in provider

    def test_add_provider_with_key(self):
        """Test adding provider with API key."""
        with patch("ais.core.config.get_config") as mock_get:
            with patch("ais.core.config.save_config") as mock_save:
                mock_get.return_value = {"providers": {}}

                add_provider(
                    "test_provider",
                    "http://test.com",
                    "test_model",
                    "test_key",
                )

                saved_config = mock_save.call_args[0][0]
                provider = saved_config["providers"]["test_provider"]
                assert provider["api_key"] == "test_key"

    def test_add_provider_no_providers_key(self):
        """Test adding provider when providers key doesn't exist."""
        with patch("ais.core.config.get_config") as mock_get:
            with patch("ais.core.config.save_config") as mock_save:
                mock_get.return_value = {}

                add_provider("test_provider", "http://test.com", "test_model")

                saved_config = mock_save.call_args[0][0]
                assert "providers" in saved_config
                assert "test_provider" in saved_config["providers"]

    def test_remove_provider_success(self):
        """Test removing provider successfully."""
        config = {
            "providers": {"test_provider": {}, "other_provider": {}},
            "default_provider": "other_provider",
        }

        with patch("ais.core.config.get_config", return_value=config):
            with patch("ais.core.config.save_config") as mock_save:
                remove_provider("test_provider")

                saved_config = mock_save.call_args[0][0]
                assert "test_provider" not in saved_config["providers"]
                assert "other_provider" in saved_config["providers"]

    def test_remove_provider_nonexistent(self):
        """Test removing non-existent provider."""
        config = {"providers": {}}

        with patch("ais.core.config.get_config", return_value=config):
            with pytest.raises(ValueError, match="提供商 'nonexistent' 不存在"):
                remove_provider("nonexistent")

    def test_remove_provider_default(self):
        """Test removing default provider."""
        config = {
            "providers": {"default_provider": {}},
            "default_provider": "default_provider",
        }

        with patch("ais.core.config.get_config", return_value=config):
            with pytest.raises(ValueError, match="不能删除当前使用的默认提供商"):
                remove_provider("default_provider")

    def test_use_provider_success(self):
        """Test switching to existing provider."""
        config = {"providers": {"test_provider": {}}}

        with patch("ais.core.config.get_config", return_value=config):
            with patch("ais.core.config.save_config") as mock_save:
                use_provider("test_provider")

                saved_config = mock_save.call_args[0][0]
                assert saved_config["default_provider"] == "test_provider"

    def test_use_provider_nonexistent(self):
        """Test switching to non-existent provider."""
        config = {"providers": {}}

        with patch("ais.core.config.get_config", return_value=config):
            with pytest.raises(ValueError, match="提供商 'nonexistent' 不存在"):
                use_provider("nonexistent")
