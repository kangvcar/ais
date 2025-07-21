"""Tests for interactive module."""

from unittest.mock import patch, Mock
import pytest

from ais.cli.interactive import (
    execute_command,
    confirm_dangerous_command,
    show_command_details,
    ask_follow_up_question,
    edit_command,
    show_interactive_menu,
    show_simple_menu,
)


class TestExecuteCommand:
    """Test command execution."""

    def test_execute_command_success(self):
        """Test successful command execution."""
        mock_result = Mock()
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            with patch("builtins.print") as mock_print:
                result = execute_command("echo test")

                assert result is True
                mock_run.assert_called_once()
                # Check that success message is printed
                success_calls = [
                    call for call in mock_print.call_args_list if "✓  命令执行成功" in str(call)
                ]
                assert len(success_calls) > 0

    def test_execute_command_failure(self):
        """Test failed command execution."""
        mock_result = Mock()
        mock_result.returncode = 1

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            with patch("builtins.print") as mock_print:
                result = execute_command("false")

                assert result is False
                mock_run.assert_called_once()
                # Check that failure message is printed
                failure_calls = [
                    call for call in mock_print.call_args_list if "✗  命令执行失败" in str(call)
                ]
                assert len(failure_calls) > 0

    def test_execute_command_exception(self):
        """Test command execution with exception."""
        with patch("subprocess.run", side_effect=Exception("Command error")):
            with patch("builtins.print") as mock_print:
                result = execute_command("invalid_command")

                assert result is False
                # Check that error message is printed
                error_calls = [
                    call for call in mock_print.call_args_list if "✗  执行命令时出错" in str(call)
                ]
                assert len(error_calls) > 0


class TestConfirmDangerousCommand:
    """Test dangerous command confirmation."""

    def test_confirm_dangerous_command_yes(self):
        """Test confirming dangerous command with yes."""
        with patch("builtins.input", return_value="yes"):
            with patch("builtins.print"):
                result = confirm_dangerous_command("rm -rf /")

                assert result is True

    def test_confirm_dangerous_command_y(self):
        """Test confirming dangerous command with y."""
        with patch("builtins.input", return_value="y"):
            with patch("builtins.print"):
                result = confirm_dangerous_command("rm -rf /")

                assert result is True

    def test_confirm_dangerous_command_no(self):
        """Test rejecting dangerous command with no."""
        with patch("builtins.input", return_value="no"):
            with patch("builtins.print"):
                result = confirm_dangerous_command("rm -rf /")

                assert result is False

    def test_confirm_dangerous_command_n(self):
        """Test rejecting dangerous command with n."""
        with patch("builtins.input", return_value="n"):
            with patch("builtins.print"):
                result = confirm_dangerous_command("rm -rf /")

                assert result is False

    def test_confirm_dangerous_command_invalid_then_yes(self):
        """Test invalid input then yes."""
        with patch("builtins.input", side_effect=["invalid", "maybe", "yes"]):
            with patch("builtins.print"):
                result = confirm_dangerous_command("rm -rf /")

                assert result is True


class TestShowCommandDetails:
    """Test showing command details."""

    def test_show_command_details_safe(self):
        """Test showing details for safe command."""
        suggestion = {
            "command": "ls -la",
            "risk_level": "safe",
            "description": "List files",
            "explanation": "Shows file details",
        }

        mock_console = Mock()

        show_command_details(suggestion, mock_console)

        # Verify console.print was called multiple times
        assert mock_console.print.call_count > 0

        # Check that command and risk level are displayed
        calls = [str(call) for call in mock_console.print.call_args_list]
        command_displayed = any("ls -la" in call for call in calls)
        risk_displayed = any("🟢 安全操作" in call for call in calls)

        assert command_displayed
        assert risk_displayed

    def test_show_command_details_dangerous(self):
        """Test showing details for dangerous command."""
        suggestion = {
            "command": "rm -rf /",
            "risk_level": "dangerous",
            "description": "Delete everything",
            "explanation": "Removes all files",
        }

        mock_console = Mock()

        show_command_details(suggestion, mock_console)

        calls = [str(call) for call in mock_console.print.call_args_list]
        risk_displayed = any("🔴 危险操作" in call for call in calls)

        assert risk_displayed

    def test_show_command_details_moderate(self):
        """Test showing details for moderate risk command."""
        suggestion = {
            "command": "chmod 777 file.txt",
            "risk_level": "moderate",
            "description": "Change permissions",
            "explanation": "Makes file world-writable",
        }

        mock_console = Mock()

        show_command_details(suggestion, mock_console)

        calls = [str(call) for call in mock_console.print.call_args_list]
        risk_displayed = any("🟡 需要谨慎" in call for call in calls)

        assert risk_displayed


class TestAskFollowUpQuestion:
    """Test asking follow-up questions."""

    def test_ask_follow_up_question_predefined(self):
        """Test asking predefined follow-up question."""
        predefined_questions = ["What is Git?", "How does Docker work?"]

        mock_console = Mock()

        with patch("builtins.input", return_value="1"):
            with patch("ais.cli.interactive.ask_ai") as mock_ask:
                with patch("ais.cli.interactive.get_config") as mock_config:
                    mock_ask.return_value = "AI response"
                    mock_config.return_value = {"test": "config"}

                    ask_follow_up_question(mock_console, predefined_questions)

                    mock_ask.assert_called_once()
                    # Verify the question was used
                    call_args = mock_ask.call_args[0][0]
                    assert "What is Git?" in call_args

    def test_ask_follow_up_question_custom(self):
        """Test asking custom follow-up question."""
        predefined_questions = ["Predefined question"]

        mock_console = Mock()

        with patch("builtins.input", side_effect=["2", "Custom question"]):
            with patch("ais.cli.interactive.ask_ai") as mock_ask:
                with patch("ais.cli.interactive.get_config") as mock_config:
                    mock_ask.return_value = "AI response"
                    mock_config.return_value = {"test": "config"}

                    ask_follow_up_question(mock_console, predefined_questions)

                    mock_ask.assert_called_once()
                    call_args = mock_ask.call_args[0][0]
                    assert "Custom question" in call_args

    def test_ask_follow_up_question_skip(self):
        """Test skipping follow-up question."""
        mock_console = Mock()

        with patch("builtins.input", return_value=""):
            with patch("ais.cli.interactive.ask_ai") as mock_ask:
                ask_follow_up_question(mock_console)

                mock_ask.assert_not_called()

    def test_ask_follow_up_question_invalid_choice(self):
        """Test invalid choice for follow-up question."""
        predefined_questions = ["Question 1"]

        mock_console = Mock()

        with patch("builtins.input", return_value="999"):
            with patch("ais.cli.interactive.ask_ai") as mock_ask:
                ask_follow_up_question(mock_console, predefined_questions)

                mock_ask.assert_not_called()

    def test_ask_follow_up_question_no_predefined(self):
        """Test asking follow-up question without predefined questions."""
        mock_console = Mock()

        with patch("builtins.input", return_value="Custom question"):
            with patch("ais.cli.interactive.ask_ai") as mock_ask:
                with patch("ais.cli.interactive.get_config") as mock_config:
                    mock_ask.return_value = "AI response"
                    mock_config.return_value = {"test": "config"}

                    ask_follow_up_question(mock_console)

                    mock_ask.assert_called_once()

    def test_ask_follow_up_question_ai_error(self):
        """Test follow-up question with AI error."""
        mock_console = Mock()

        with patch("builtins.input", return_value="Test question"):
            with patch("ais.cli.interactive.ask_ai", side_effect=Exception("AI error")):
                with patch("ais.cli.interactive.get_config") as mock_config:
                    mock_config.return_value = {"test": "config"}

                    ask_follow_up_question(mock_console)

                    # Should handle error gracefully
                    error_calls = [
                        call
                        for call in mock_console.print.call_args_list
                        if "✗  处理问题时出错" in str(call)
                    ]
                    assert len(error_calls) > 0


class TestEditCommand:
    """Test command editing."""

    def test_edit_command_with_changes(self):
        """Test editing command with changes."""
        with patch("builtins.input", return_value="new command"):
            with patch("builtins.print"):
                result = edit_command("old command")

                assert result == "new command"

    def test_edit_command_no_changes(self):
        """Test editing command without changes."""
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                result = edit_command("original command")

                assert result == "original command"


class TestShowSimpleMenu:
    """Test simple menu display."""

    def test_show_simple_menu(self):
        """Test showing simple menu."""
        suggestions = [
            {
                "command": "ls -la",
                "description": "List files",
                "risk_level": "safe",
                "explanation": "Shows file details",
            },
            {
                "command": "rm file.txt",
                "description": "Remove file",
                "risk_level": "moderate",
            },
        ]

        mock_console = Mock()

        show_simple_menu(suggestions, mock_console)

        # Verify console.print was called
        assert mock_console.print.call_count > 0

        # Check that suggestions are displayed
        calls = [str(call) for call in mock_console.print.call_args_list]
        ls_displayed = any("ls -la" in call for call in calls)
        rm_displayed = any("rm file.txt" in call for call in calls)

        assert ls_displayed
        assert rm_displayed


class TestShowInteractiveMenu:
    """Test interactive menu display."""

    def test_show_interactive_menu_not_tty(self):
        """Test interactive menu when not in TTY."""
        suggestions = [{"command": "test", "description": "test", "risk_level": "safe"}]
        mock_console = Mock()

        with patch("sys.stdin.isatty", return_value=False):
            with patch("ais.cli.interactive.show_simple_menu") as mock_simple:
                show_interactive_menu(suggestions, mock_console)

                mock_simple.assert_called_once_with(suggestions, mock_console, None)

    def test_show_interactive_menu_no_questionary(self):
        """Test interactive menu when questionary is not available."""
        suggestions = [{"command": "test", "description": "test", "risk_level": "safe"}]
        mock_console = Mock()

        with patch("sys.stdin.isatty", return_value=True):
            with patch("ais.cli.interactive.show_simple_menu") as mock_simple:
                # Mock import error for questionary
                with patch(
                    "builtins.__import__",
                    side_effect=ImportError("No questionary"),
                ):
                    show_interactive_menu(suggestions, mock_console)

                    mock_simple.assert_called_once()

    def test_show_interactive_menu_exit(self):
        """Test interactive menu with exit choice."""
        suggestions = [{"command": "test", "description": "test", "risk_level": "safe"}]
        mock_console = Mock()

        with patch("sys.stdin.isatty", return_value=True):
            try:
                import questionary  # noqa: F401

                mock_questionary = Mock()
                mock_questionary.select.return_value.ask.return_value = "exit"

                with patch("ais.cli.interactive.questionary", mock_questionary):
                    show_interactive_menu(suggestions, mock_console)

                    # Should call questionary.select
                    mock_questionary.select.assert_called()

            except ImportError:
                # Skip test if questionary not available
                pytest.skip("questionary not available")

    def test_show_interactive_menu_execute_safe_command(self):
        """Test interactive menu executing safe command."""
        suggestions = [
            {
                "command": "echo test",
                "description": "test",
                "risk_level": "safe",
            }
        ]
        mock_console = Mock()

        with patch("sys.stdin.isatty", return_value=True):
            try:
                import questionary  # noqa: F401

                mock_questionary = Mock()
                mock_questionary.select.return_value.ask.side_effect = [
                    "execute_0",
                    "exit",
                ]
                mock_questionary.confirm.return_value.ask.return_value = False

                with patch("ais.cli.interactive.questionary", mock_questionary):
                    with patch("ais.cli.interactive.execute_command") as mock_execute:
                        with patch("ais.cli.interactive.show_command_details"):
                            mock_execute.return_value = True

                            show_interactive_menu(suggestions, mock_console)

                            mock_execute.assert_called_once_with("echo test")

            except ImportError:
                pytest.skip("questionary not available")

    def test_show_interactive_menu_execute_dangerous_command_confirmed(self):
        """Test interactive menu executing dangerous command confirmed."""
        suggestions = [
            {
                "command": "rm -rf /",
                "description": "dangerous",
                "risk_level": "dangerous",
            }
        ]
        mock_console = Mock()

        with patch("sys.stdin.isatty", return_value=True):
            try:
                import questionary  # noqa: F401

                mock_questionary = Mock()
                mock_questionary.select.return_value.ask.side_effect = [
                    "execute_0",
                    "exit",
                ]
                mock_questionary.confirm.return_value.ask.return_value = False

                with patch("ais.cli.interactive.questionary", mock_questionary):
                    with patch("ais.cli.interactive.execute_command") as mock_execute:
                        with patch("ais.cli.interactive.show_command_details"):
                            with patch(
                                "ais.cli.interactive." "confirm_dangerous_command",
                                return_value=True,
                            ):
                                mock_execute.return_value = True

                                show_interactive_menu(suggestions, mock_console)

                                mock_execute.assert_called_once_with("rm -rf /")

            except ImportError:
                pytest.skip("questionary not available")

    def test_show_interactive_menu_execute_dangerous_command_cancelled(self):
        """Test interactive menu cancelling dangerous command."""
        suggestions = [
            {
                "command": "rm -rf /",
                "description": "dangerous",
                "risk_level": "dangerous",
            }
        ]
        mock_console = Mock()

        with patch("sys.stdin.isatty", return_value=True):
            try:
                import questionary  # noqa: F401

                mock_questionary = Mock()
                mock_questionary.select.return_value.ask.side_effect = [
                    "execute_0",
                    "exit",
                ]

                with patch("ais.cli.interactive.questionary", mock_questionary):
                    with patch("ais.cli.interactive.execute_command") as mock_execute:
                        with patch("ais.cli.interactive.show_command_details"):
                            with patch(
                                "ais.cli.interactive." "confirm_dangerous_command",
                                return_value=False,
                            ):
                                show_interactive_menu(suggestions, mock_console)

                                mock_execute.assert_not_called()

            except ImportError:
                pytest.skip("questionary not available")
