"""Tests for AI module."""

import json
from unittest.mock import patch, Mock

import pytest
import httpx

from ais.core.ai import (
    _build_context_summary,
    _make_api_request,
    ask_ai,
    analyze_error,
)


class TestContextSummary:
    """Test context summary building."""

    def test_build_context_summary_basic(self):
        """Test building basic context summary."""
        context = {"cwd": "/home/user/project", "user": "testuser"}

        summary = _build_context_summary(context)

        assert "📁 当前目录: /home/user/project" in summary
        assert "👤 用户: testuser" in summary

    def test_build_context_summary_git_info(self):
        """Test building context summary with git info."""
        context = {
            "git_info": {
                "in_repo": True,
                "current_branch": "main",
                "has_changes": True,
                "changed_files": 3,
            }
        }

        summary = _build_context_summary(context)

        assert "🔄 Git仓库: main分支" in summary
        assert "(有3个文件变更)" in summary

    def test_build_context_summary_project_type(self):
        """Test building context summary with project type."""
        context = {
            "current_dir_files": {
                "project_type": "python",
                "key_files": ["requirements.txt", "setup.py", "main.py"],
            }
        }

        summary = _build_context_summary(context)

        assert "🚀 项目类型: python" in summary
        assert "requirements.txt, setup.py, main.py" in summary

    def test_build_context_summary_system_status(self):
        """Test building context summary with system status."""
        context = {
            "system_status": {"cpu_percent": 85.5, "memory": {"percent": 67.2}}
        }

        summary = _build_context_summary(context)

        assert "⚡ 系统状态: CPU 85.5%" in summary
        assert "内存 67.2%" in summary

    def test_build_context_summary_work_pattern(self):
        """Test building context summary with work pattern."""
        context = {
            "work_pattern": {"activities": ["git", "docker", "python", "npm"]}
        }

        summary = _build_context_summary(context)

        assert "🎯 最近操作: git, docker, python" in summary

    def test_build_context_summary_network_offline(self):
        """Test building context summary with offline network."""
        context = {"network_info": {"internet_available": False}}

        summary = _build_context_summary(context)

        assert "🌐 网络: 离线状态" in summary

    def test_build_context_summary_empty(self):
        """Test building context summary with empty context."""
        context = {}

        summary = _build_context_summary(context)

        assert summary == "📋 基本环境信息"


class TestApiRequest:
    """Test API request functionality."""

    def test_make_api_request_success(self):
        """Test successful API request."""
        config = {
            "default_provider": "test_provider",
            "providers": {
                "test_provider": {
                    "base_url": "http://test.com/chat",
                    "model_name": "test_model",
                    "api_key": "test_key",
                }
            },
        }

        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }

        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = (
                mock_response
            )

            messages = [{"role": "user", "content": "Test message"}]
            result = _make_api_request(messages, config)

            assert result == "Test response"

    def test_make_api_request_no_api_key(self):
        """Test API request without API key."""
        config = {
            "default_provider": "test_provider",
            "providers": {
                "test_provider": {
                    "base_url": "http://test.com/chat",
                    "model_name": "test_model",
                }
            },
        }

        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }

        with patch("httpx.Client") as mock_client:
            mock_client_instance = (
                mock_client.return_value.__enter__.return_value
            )
            mock_client_instance.post.return_value = mock_response

            messages = [{"role": "user", "content": "Test message"}]
            result = _make_api_request(messages, config)

            # Verify headers don't include Authorization
            call_args = mock_client_instance.post.call_args
            headers = call_args[1]["headers"]
            assert "Authorization" not in headers
            assert result == "Test response"

    def test_make_api_request_provider_not_found(self):
        """Test API request with non-existent provider."""
        config = {"default_provider": "nonexistent", "providers": {}}

        messages = [{"role": "user", "content": "Test message"}]

        with pytest.raises(
            ValueError, match="Provider 'nonexistent' not found"
        ):
            _make_api_request(messages, config)

    def test_make_api_request_incomplete_config(self):
        """Test API request with incomplete provider configuration."""
        config = {
            "default_provider": "test_provider",
            "providers": {
                "test_provider": {
                    "base_url": "http://test.com/chat"
                    # Missing model_name
                }
            },
        }

        messages = [{"role": "user", "content": "Test message"}]

        with pytest.raises(
            ValueError, match="Incomplete provider configuration"
        ):
            _make_api_request(messages, config)

    def test_make_api_request_connection_error(self):
        """Test API request with connection error."""
        config = {
            "default_provider": "test_provider",
            "providers": {
                "test_provider": {
                    "base_url": "http://test.com/chat",
                    "model_name": "test_model",
                }
            },
        }

        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.side_effect = httpx.RequestError(
                "Connection failed"
            )

            messages = [{"role": "user", "content": "Test message"}]

            with pytest.raises(
                ConnectionError, match="Failed to connect to AI service"
            ):
                _make_api_request(messages, config)

    def test_make_api_request_http_error(self):
        """Test API request with HTTP error."""
        config = {
            "default_provider": "test_provider",
            "providers": {
                "test_provider": {
                    "base_url": "http://test.com/chat",
                    "model_name": "test_model",
                }
            },
        }

        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"

        with patch("httpx.Client") as mock_client:
            mock_client_instance = (
                mock_client.return_value.__enter__.return_value
            )
            mock_client_instance.post.side_effect = httpx.HTTPStatusError(
                "Bad Request", request=Mock(), response=mock_response
            )

            messages = [{"role": "user", "content": "Test message"}]

            with pytest.raises(
                ConnectionError, match="AI service returned error 400"
            ):
                _make_api_request(messages, config)

    def test_make_api_request_empty_response(self):
        """Test API request with empty response."""
        config = {
            "default_provider": "test_provider",
            "providers": {
                "test_provider": {
                    "base_url": "http://test.com/chat",
                    "model_name": "test_model",
                }
            },
        }

        mock_response = Mock()
        mock_response.json.return_value = {"choices": []}

        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = (
                mock_response
            )

            messages = [{"role": "user", "content": "Test message"}]
            result = _make_api_request(messages, config)

            assert result is None


class TestAskAi:
    """Test ask AI functionality."""

    def test_ask_ai_success(self):
        """Test successful ask AI."""
        config = {"test": "config"}

        with patch("ais.core.ai._make_api_request") as mock_request:
            mock_request.return_value = "AI response"

            result = ask_ai("Test question", config)

            assert result == "AI response"
            mock_request.assert_called_once()
            messages = mock_request.call_args[0][0]
            assert messages[0]["content"] == "Test question"


class TestAnalyzeError:
    """Test error analysis functionality."""

    def test_analyze_error_success_json(self):
        """Test successful error analysis with JSON response."""
        command = "ls /nonexistent"
        exit_code = 2
        stderr = "No such file or directory"
        context = {"cwd": "/home/user"}
        config = {"test": "config"}

        expected_response = {
            "explanation": "Test explanation",
            "suggestions": [
                {"command": "mkdir /nonexistent", "risk_level": "safe"}
            ],
            "follow_up_questions": ["Want to learn more?"],
        }

        with patch("ais.core.ai._make_api_request") as mock_request:
            mock_request.return_value = json.dumps(expected_response)

            result = analyze_error(command, exit_code, stderr, context, config)

            assert result == expected_response

    def test_analyze_error_json_in_markdown(self):
        """Test error analysis with JSON in markdown code block."""
        command = "ls /nonexistent"
        exit_code = 2
        stderr = "No such file or directory"
        context = {"cwd": "/home/user"}
        config = {"test": "config"}

        expected_response = {
            "explanation": "Test explanation",
            "suggestions": [],
            "follow_up_questions": [],
        }

        markdown_response = f"""Here's the analysis:
```json
{json.dumps(expected_response)}
```
"""

        with patch("ais.core.ai._make_api_request") as mock_request:
            mock_request.return_value = markdown_response

            result = analyze_error(command, exit_code, stderr, context, config)

            assert result == expected_response

    def test_analyze_error_partial_json(self):
        """Test error analysis with partial JSON in response."""
        command = "ls /nonexistent"
        exit_code = 2
        stderr = "No such file or directory"
        context = {"cwd": "/home/user"}
        config = {"test": "config"}

        expected_response = {"explanation": "Test explanation"}

        response_with_text = f"""Some text before
{json.dumps(expected_response)}
Some text after"""

        with patch("ais.core.ai._make_api_request") as mock_request:
            mock_request.return_value = response_with_text

            result = analyze_error(command, exit_code, stderr, context, config)

            assert result == expected_response

    def test_analyze_error_invalid_json(self):
        """Test error analysis with invalid JSON response."""
        command = "ls /nonexistent"
        exit_code = 2
        stderr = "No such file or directory"
        context = {"cwd": "/home/user"}
        config = {"test": "config"}

        with patch("ais.core.ai._make_api_request") as mock_request:
            mock_request.return_value = "Invalid JSON response"

            result = analyze_error(command, exit_code, stderr, context, config)

            assert result["explanation"] == "Invalid JSON response"
            assert result["suggestions"] == []
            assert result["follow_up_questions"] == []

    def test_analyze_error_no_response(self):
        """Test error analysis with no response from AI."""
        command = "ls /nonexistent"
        exit_code = 2
        stderr = "No such file or directory"
        context = {"cwd": "/home/user"}
        config = {"test": "config"}

        with patch("ais.core.ai._make_api_request") as mock_request:
            mock_request.return_value = None

            result = analyze_error(command, exit_code, stderr, context, config)

            assert result["explanation"] == "No response from AI service"
            assert result["suggestions"] == []
            assert result["follow_up_questions"] == []

    def test_analyze_error_api_exception(self):
        """Test error analysis with API exception."""
        command = "ls /nonexistent"
        exit_code = 2
        stderr = "No such file or directory"
        context = {"cwd": "/home/user"}
        config = {"test": "config"}

        with patch("ais.core.ai._make_api_request") as mock_request:
            mock_request.side_effect = Exception("API Error")

            result = analyze_error(command, exit_code, stderr, context, config)

            assert (
                "Error communicating with AI service" in result["explanation"]
            )
            assert result["suggestions"] == []
            assert result["follow_up_questions"] == []

    def test_analyze_error_empty_stderr(self):
        """Test error analysis with empty stderr."""
        command = "ls /nonexistent"
        exit_code = 2
        stderr = ""
        context = {"cwd": "/home/user"}
        config = {"test": "config"}

        with patch("ais.core.ai._make_api_request") as mock_request:
            mock_request.return_value = '{"explanation": "test"}'

            analyze_error(command, exit_code, stderr, context, config)

            # Verify the prompt includes note about no stderr
            call_args = mock_request.call_args[0]
            messages = call_args[0]
            user_message = messages[1]["content"]
            assert "No stderr captured" in user_message
