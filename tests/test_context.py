"""Tests for context module."""

import os
import subprocess
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from ais.core.context import (
    is_sensitive_path,
    filter_sensitive_data,
    run_safe_command,
    collect_core_context,
    _collect_git_info,
    collect_standard_context,
    collect_detailed_context,
    collect_context,
)


class TestSensitivePath:
    """Test sensitive path detection."""

    def test_is_sensitive_path_true(self):
        """Test detecting sensitive path."""
        sensitive_dirs = ["~/.ssh", "~/.config/ais"]

        with patch("pathlib.Path.expanduser") as mock_expand:
            with patch("pathlib.Path.resolve") as mock_resolve:
                # Mock path resolution
                mock_expand.return_value.resolve.return_value = Path(
                    "/home/user/.ssh/keys"
                )
                mock_resolve.return_value = Path("/home/user/.ssh")

                # Mock relative_to to succeed (meaning path is under sensitive dir)
                mock_expand.return_value.resolve.return_value.relative_to = (
                    Mock(return_value=Path("keys"))
                )

                result = is_sensitive_path(
                    "/home/user/.ssh/keys", sensitive_dirs
                )

                # Should be True since path is under .ssh
                assert result is True

    def test_is_sensitive_path_false(self):
        """Test detecting non-sensitive path."""
        sensitive_dirs = ["~/.ssh", "~/.config/ais"]

        with patch("pathlib.Path.expanduser") as mock_expand:
            with patch("pathlib.Path.resolve") as mock_resolve:
                # Mock path resolution
                test_path = Path("/home/user/project")
                mock_expand.return_value.resolve.return_value = test_path

                # Mock relative_to to raise ValueError (meaning path is not under sensitive dir)
                test_path.relative_to = Mock(
                    side_effect=ValueError("Not relative")
                )

                result = is_sensitive_path(
                    "/home/user/project", sensitive_dirs
                )

                assert result is False


class TestFilterSensitiveData:
    """Test sensitive data filtering."""

    def test_filter_password(self):
        """Test filtering password."""
        text = "password=mysecretpass"
        result = filter_sensitive_data(text)
        assert "mysecretpass" not in result
        assert "password ***" in result

    def test_filter_api_key(self):
        """Test filtering API key."""
        text = "API_KEY=sk-abcdef123456789012345678"
        result = filter_sensitive_data(text)
        assert "sk-abcdef123456789012345678" not in result
        assert "API_KEY ***" in result

    def test_filter_token(self):
        """Test filtering token."""
        text = "token: myaccesstoken123"
        result = filter_sensitive_data(text)
        assert "myaccesstoken123" not in result
        assert "token ***" in result

    def test_filter_openai_key(self):
        """Test filtering OpenAI key format."""
        text = "sk-1234567890abcdefghijklmnop"
        result = filter_sensitive_data(text)
        assert "sk-1234567890abcdefghijklmnop" not in result

    def test_filter_no_sensitive_data(self):
        """Test filtering text with no sensitive data."""
        text = "This is normal text with no secrets"
        result = filter_sensitive_data(text)
        assert result == text


class TestRunSafeCommand:
    """Test safe command execution."""

    def test_run_safe_command_success(self):
        """Test successful command execution."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Command output\n"

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            result = run_safe_command("echo test")

            assert result == "Command output"
            mock_run.assert_called_once()
            args = mock_run.call_args
            assert args[0][0] == "echo test"
            assert args[1]["shell"] is True
            assert args[1]["capture_output"] is True
            assert args[1]["text"] is True
            assert args[1]["timeout"] == 5

    def test_run_safe_command_failure(self):
        """Test failed command execution."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = "Error output\n"

        with patch("subprocess.run", return_value=mock_result):
            result = run_safe_command("false")

            assert result is None

    def test_run_safe_command_exception(self):
        """Test command execution with exception."""
        with patch(
            "subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 5)
        ):
            result = run_safe_command("sleep 10", timeout=1)

            assert result is None

    def test_run_safe_command_custom_timeout(self):
        """Test command execution with custom timeout."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "output"

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            run_safe_command("echo test", timeout=10)

            args = mock_run.call_args
            assert args[1]["timeout"] == 10


class TestCollectCoreContext:
    """Test core context collection."""

    def test_collect_core_context(self):
        """Test collecting core context."""
        with patch("ais.core.context.run_safe_command") as mock_run:
            mock_run.return_value = "2023-07-11 10:30:00"

            result = collect_core_context("ls -la", 0, "", "/home/user")

            assert result["command"] == "ls -la"
            assert result["exit_code"] == 0
            assert result["stderr"] == ""
            assert result["cwd"] == "/home/user"
            assert result["timestamp"] == "2023-07-11 10:30:00"


class TestCollectGitInfo:
    """Test git information collection."""

    def test_collect_git_info_in_repo(self):
        """Test collecting git info in repository."""
        with patch("ais.core.context.run_safe_command") as mock_run:
            mock_run.side_effect = [
                " M file1.txt\n A file2.txt",  # git status
                "main",  # git branch
            ]

            result = _collect_git_info()

            assert "git_status" in result
            assert "git_branch" in result
            assert result["git_branch"] == "main"

    def test_collect_git_info_not_in_repo(self):
        """Test collecting git info outside repository."""
        with patch("ais.core.context.run_safe_command") as mock_run:
            mock_run.return_value = None  # git commands fail

            result = _collect_git_info()

            assert result == {}


class TestCollectStandardContext:
    """Test standard context collection."""

    def test_collect_standard_context(self):
        """Test collecting standard context."""
        config = {}

        with patch("ais.core.context.run_safe_command") as mock_run:
            with patch("pathlib.Path.cwd") as mock_cwd:
                with patch("pathlib.Path.iterdir") as mock_iterdir:
                    # Mock command history
                    mock_run.return_value = (
                        "  100  ls\n  101  pwd\n  102  git status"
                    )

                    # Mock current directory files
                    mock_file1 = Mock()
                    mock_file1.name = "file1.txt"
                    mock_file1.is_file.return_value = True
                    mock_file2 = Mock()
                    mock_file2.name = "file2.py"
                    mock_file2.is_file.return_value = True

                    mock_cwd.return_value.iterdir.return_value = [
                        mock_file1,
                        mock_file2,
                    ]

                    with patch(
                        "ais.core.context._collect_git_info"
                    ) as mock_git:
                        mock_git.return_value = {"git_branch": "main"}

                        result = collect_standard_context(config)

                        assert "recent_history" in result
                        assert "current_files" in result
                        assert "git_branch" in result
                        assert len(result["recent_history"]) == 3
                        assert "file1.txt" in result["current_files"]
                        assert "file2.py" in result["current_files"]

    def test_collect_standard_context_file_error(self):
        """Test collecting standard context with file listing error."""
        config = {}

        with patch("ais.core.context.run_safe_command") as mock_run:
            with patch("pathlib.Path.cwd") as mock_cwd:
                # Mock command history
                mock_run.return_value = "  100  ls"

                # Mock directory listing error
                mock_cwd.return_value.iterdir.side_effect = PermissionError(
                    "Access denied"
                )

                with patch("ais.core.context._collect_git_info") as mock_git:
                    mock_git.return_value = {}

                    result = collect_standard_context(config)

                    assert "recent_history" in result
                    assert (
                        "current_files" not in result
                    )  # Should be skipped due to error


class TestCollectDetailedContext:
    """Test detailed context collection."""

    def test_collect_detailed_context(self):
        """Test collecting detailed context."""
        config = {}

        with patch("ais.core.context.run_safe_command") as mock_run:
            mock_run.side_effect = [
                "Linux hostname 5.4.0 #1 SMP x86_64 GNU/Linux",  # uname
                "total 16\n-rw-r--r-- 1 user user 1234 Jul 11 10:30 file.txt",  # ls -la
            ]

            with patch.dict(
                os.environ, {"HOME": "/home/user", "PATH": "/usr/bin"}
            ):
                result = collect_detailed_context(config)

                assert "system_info" in result
                assert "environment" in result
                assert "directory_listing" in result
                assert (
                    result["system_info"]
                    == "Linux hostname 5.4.0 #1 SMP x86_64 GNU/Linux"
                )
                assert "HOME" in result["environment"]
                assert "PATH" in result["environment"]

    def test_collect_detailed_context_filter_sensitive_env(self):
        """Test collecting detailed context filters sensitive environment variables."""
        config = {}

        with patch("ais.core.context.run_safe_command") as mock_run:
            mock_run.side_effect = [None, None]  # Commands fail

            with patch.dict(
                os.environ,
                {
                    "HOME": "/home/user",
                    "API_KEY": "secret123",
                    "PASSWORD": "password123",
                    "SECRET_TOKEN": "token123",
                    "NORMAL_VAR": "normal_value",
                },
            ):
                result = collect_detailed_context(config)

                env_vars = result.get("environment", {})
                assert "HOME" in env_vars
                assert "NORMAL_VAR" in env_vars
                assert "API_KEY" not in env_vars
                assert "PASSWORD" not in env_vars
                assert "SECRET_TOKEN" not in env_vars


class TestCollectContext:
    """Test main context collection function."""

    def test_collect_context_minimal(self):
        """Test collecting context with minimal level."""
        config = {"context_level": "minimal", "sensitive_dirs": []}

        with patch(
            "pathlib.Path.cwd", return_value=Path("/home/user/project")
        ):
            with patch(
                "ais.core.context.is_sensitive_path", return_value=False
            ):
                with patch(
                    "ais.core.context.collect_core_context"
                ) as mock_core:
                    mock_core.return_value = {
                        "command": "test",
                        "cwd": "/home/user/project",
                    }

                    result = collect_context("test command", 0, "", config)

                    assert result["command"] == "test"
                    assert result["cwd"] == "/home/user/project"

    def test_collect_context_standard(self):
        """Test collecting context with standard level."""
        config = {"context_level": "standard", "sensitive_dirs": []}

        with patch(
            "pathlib.Path.cwd", return_value=Path("/home/user/project")
        ):
            with patch(
                "ais.core.context.is_sensitive_path", return_value=False
            ):
                with patch(
                    "ais.core.context.collect_core_context"
                ) as mock_core:
                    with patch(
                        "ais.core.context.collect_standard_context"
                    ) as mock_standard:
                        mock_core.return_value = {"command": "test"}
                        mock_standard.return_value = {"git_branch": "main"}

                        result = collect_context("test command", 0, "", config)

                        assert result["command"] == "test"
                        assert result["git_branch"] == "main"

    def test_collect_context_detailed(self):
        """Test collecting context with detailed level."""
        config = {"context_level": "detailed", "sensitive_dirs": []}

        with patch(
            "pathlib.Path.cwd", return_value=Path("/home/user/project")
        ):
            with patch(
                "ais.core.context.is_sensitive_path", return_value=False
            ):
                with patch(
                    "ais.core.context.collect_core_context"
                ) as mock_core:
                    with patch(
                        "ais.core.context.collect_standard_context"
                    ) as mock_standard:
                        with patch(
                            "ais.core.context.collect_detailed_context"
                        ) as mock_detailed:
                            mock_core.return_value = {"command": "test"}
                            mock_standard.return_value = {"git_branch": "main"}
                            mock_detailed.return_value = {
                                "system_info": "Linux"
                            }

                            result = collect_context(
                                "test command", 0, "", config
                            )

                            assert result["command"] == "test"
                            assert result["git_branch"] == "main"
                            assert result["system_info"] == "Linux"

    def test_collect_context_sensitive_directory(self):
        """Test collecting context in sensitive directory."""
        config = {"sensitive_dirs": ["~/.ssh"]}

        with patch("pathlib.Path.cwd", return_value=Path("/home/user/.ssh")):
            with patch(
                "ais.core.context.is_sensitive_path", return_value=True
            ):
                result = collect_context("test command", 0, "", config)

                assert result["error"] == "位于敏感目录，跳过上下文收集"
                assert result["command"] == "test command"
                assert result["exit_code"] == 0

    def test_collect_context_no_config(self):
        """Test collecting context without config."""
        with patch("ais.core.context.get_config") as mock_get_config:
            mock_get_config.return_value = {
                "context_level": "minimal",
                "sensitive_dirs": [],
            }

            with patch(
                "pathlib.Path.cwd", return_value=Path("/home/user/project")
            ):
                with patch(
                    "ais.core.context.is_sensitive_path", return_value=False
                ):
                    with patch(
                        "ais.core.context.collect_core_context"
                    ) as mock_core:
                        mock_core.return_value = {"command": "test"}

                        result = collect_context("test command", 0)

                        assert result["command"] == "test"
                        mock_get_config.assert_called_once()

    def test_collect_context_filter_sensitive_data(self):
        """Test that context collection filters sensitive data."""
        config = {"context_level": "minimal", "sensitive_dirs": []}

        with patch(
            "pathlib.Path.cwd", return_value=Path("/home/user/project")
        ):
            with patch(
                "ais.core.context.is_sensitive_path", return_value=False
            ):
                with patch(
                    "ais.core.context.collect_core_context"
                ) as mock_core:
                    mock_core.return_value = {
                        "command": "test",
                        "output": "password=secret123",
                        "history": ["token=abc123", "ls -la"],
                    }

                    result = collect_context("test command", 0, "", config)

                    # Sensitive data should be filtered
                    assert "secret123" not in result["output"]
                    assert "abc123" not in str(result["history"])
