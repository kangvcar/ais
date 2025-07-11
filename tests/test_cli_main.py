"""Tests for CLI main module."""

import json
from unittest.mock import patch, Mock, call

import pytest
from click.testing import CliRunner

from ais.cli.main import (
    main,
    ask,
    config,
    on,
    off,
    add_provider_cmd,
    remove_provider_cmd,
    use_provider_cmd,
    list_provider,
    analyze_error,
    show_history,
    show_history_detail,
    suggest_command,
    learn_command,
    setup_shell,
    test_integration,
    which_command,
    help_all,
    _handle_error,
    _toggle_auto_analysis,
    _handle_provider_operation
)


class TestCliBasics:
    """Test basic CLI functionality."""
    
    def test_main_command_help(self):
        """Test main command help."""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert 'AIS - AI-powered terminal assistant' in result.output
    
    def test_main_command_version(self):
        """Test main command version."""
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])
        
        assert result.exit_code == 0
        assert '0.1.0' in result.output


class TestErrorHandling:
    """Test error handling functions."""
    
    def test_handle_error(self):
        """Test error handling function."""
        with patch('ais.cli.main.console') as mock_console:
            _handle_error('Test error message')
            
            mock_console.print.assert_called_once_with('[red]错误: Test error message[/red]')
    
    def test_toggle_auto_analysis_on(self):
        """Test turning auto analysis on."""
        with patch('ais.cli.main.set_config') as mock_set:
            with patch('ais.cli.main.console') as mock_console:
                _toggle_auto_analysis(True)
                
                mock_set.assert_called_once_with('auto_analysis', True)
                mock_console.print.assert_called_once()
                assert '已开启' in mock_console.print.call_args[0][0]
    
    def test_toggle_auto_analysis_off(self):
        """Test turning auto analysis off."""
        with patch('ais.cli.main.set_config') as mock_set:
            with patch('ais.cli.main.console') as mock_console:
                _toggle_auto_analysis(False)
                
                mock_set.assert_called_once_with('auto_analysis', False)
                mock_console.print.assert_called_once()
                assert '已关闭' in mock_console.print.call_args[0][0]
    
    def test_toggle_auto_analysis_error(self):
        """Test auto analysis toggle with error."""
        with patch('ais.cli.main.set_config', side_effect=Exception('Config error')):
            with patch('ais.cli.main._handle_error') as mock_handle:
                _toggle_auto_analysis(True)
                
                mock_handle.assert_called_once_with('Config error')
    
    def test_handle_provider_operation_success(self):
        """Test successful provider operation."""
        mock_operation = Mock()
        
        with patch('ais.cli.main.console') as mock_console:
            _handle_provider_operation(
                mock_operation, 'test_provider', 'Success message', 'Error prefix', 'arg1', 'arg2'
            )
            
            mock_operation.assert_called_once_with('test_provider', 'arg1', 'arg2')
            mock_console.print.assert_called_once()
            assert 'Success message: test_provider' in mock_console.print.call_args[0][0]
    
    def test_handle_provider_operation_error(self):
        """Test provider operation with error."""
        mock_operation = Mock(side_effect=Exception('Operation failed'))
        
        with patch('ais.cli.main.console') as mock_console:
            _handle_provider_operation(
                mock_operation, 'test_provider', 'Success message', 'Error prefix'
            )
            
            mock_console.print.assert_called_once()
            assert 'Error prefix失败' in mock_console.print.call_args[0][0]


class TestAskCommand:
    """Test ask command."""
    
    def test_ask_command_success(self):
        """Test successful ask command."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_config') as mock_config:
            with patch('ais.cli.main.ask_ai') as mock_ask:
                mock_config.return_value = {'test': 'config'}
                mock_ask.return_value = 'AI response'
                
                result = runner.invoke(ask, ['What is Docker?'])
                
                assert result.exit_code == 0
                mock_ask.assert_called_once_with('What is Docker?', {'test': 'config'})
    
    def test_ask_command_no_question(self):
        """Test ask command without question."""
        runner = CliRunner()
        result = runner.invoke(ask, [])
        
        assert result.exit_code == 0
        assert '错误: 请提供要询问的问题' in result.output
    
    def test_ask_command_help_detail(self):
        """Test ask command help detail."""
        runner = CliRunner()
        result = runner.invoke(ask, ['--help-detail'])
        
        assert result.exit_code == 0
        assert 'ais ask 命令详细使用说明' in result.output
    
    def test_ask_command_no_response(self):
        """Test ask command with no AI response."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_config') as mock_config:
            with patch('ais.cli.main.ask_ai') as mock_ask:
                mock_config.return_value = {'test': 'config'}
                mock_ask.return_value = None
                
                result = runner.invoke(ask, ['Test question'])
                
                assert result.exit_code == 0
                assert 'Failed to get AI response' in result.output
    
    def test_ask_command_exception(self):
        """Test ask command with exception."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_config', side_effect=Exception('Config error')):
            result = runner.invoke(ask, ['Test question'])
            
            assert result.exit_code == 0
            # Should handle the error gracefully


class TestConfigCommand:
    """Test config command."""
    
    def test_config_command_display(self):
        """Test config command display."""
        runner = CliRunner()
        
        mock_config = {
            'default_provider': 'test_provider',
            'auto_analysis': True,
            'context_level': 'standard',
            'sensitive_dirs': ['~/.ssh', '~/.config']
        }
        
        with patch('ais.cli.main.get_config', return_value=mock_config):
            result = runner.invoke(config, [])
            
            assert result.exit_code == 0
            assert '当前配置' in result.output
            assert 'test_provider' in result.output
            assert '✅ 开启' in result.output
    
    def test_config_command_set_valid(self):
        """Test config command set valid value."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_config') as mock_get:
            with patch('ais.cli.main.set_config') as mock_set:
                mock_get.return_value = {}
                
                result = runner.invoke(config, ['--set', 'auto_analysis=true'])
                
                assert result.exit_code == 0
                mock_set.assert_called_once_with('auto_analysis', True)
    
    def test_config_command_set_context_level(self):
        """Test config command set context level."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_config') as mock_get:
            with patch('ais.cli.main.set_config') as mock_set:
                mock_get.return_value = {}
                
                result = runner.invoke(config, ['--set', 'context_level=detailed'])
                
                assert result.exit_code == 0
                mock_set.assert_called_once_with('context_level', 'detailed')
    
    def test_config_command_set_invalid_context_level(self):
        """Test config command set invalid context level."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_config') as mock_get:
            mock_get.return_value = {}
            
            result = runner.invoke(config, ['--set', 'context_level=invalid'])
            
            assert result.exit_code == 0
            assert 'context_level 必须是 minimal, standard 或 detailed' in result.output
    
    def test_config_command_set_invalid_format(self):
        """Test config command set invalid format."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_config') as mock_get:
            mock_get.return_value = {}
            
            result = runner.invoke(config, ['--set', 'invalid_format'])
            
            assert result.exit_code == 0
            assert '格式错误，请使用 key=value 格式' in result.output
    
    def test_config_command_get(self):
        """Test config command get value."""
        runner = CliRunner()
        
        mock_config = {'test_key': 'test_value'}
        
        with patch('ais.cli.main.get_config', return_value=mock_config):
            result = runner.invoke(config, ['--get', 'test_key'])
            
            assert result.exit_code == 0
            assert 'test_key: test_value' in result.output
    
    def test_config_command_get_missing(self):
        """Test config command get missing value."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_config', return_value={}):
            result = runner.invoke(config, ['--get', 'missing_key'])
            
            assert result.exit_code == 0
            assert 'missing_key: 未设置' in result.output
    
    def test_config_command_list_providers(self):
        """Test config command list providers."""
        runner = CliRunner()
        
        mock_config = {
            'default_provider': 'test_provider',
            'providers': {
                'test_provider': {'model_name': 'test_model'},
                'other_provider': {'model_name': 'other_model'}
            }
        }
        
        with patch('ais.cli.main.get_config', return_value=mock_config):
            result = runner.invoke(config, ['--list-providers'])
            
            assert result.exit_code == 0
            assert '可用的 AI 服务商' in result.output
            assert 'test_provider' in result.output
            assert 'other_provider' in result.output
    
    def test_config_command_help_context(self):
        """Test config command help context."""
        runner = CliRunner()
        result = runner.invoke(config, ['--help-context'])
        
        assert result.exit_code == 0
        assert '上下文收集级别配置帮助' in result.output


class TestOnOffCommands:
    """Test on/off commands."""
    
    def test_on_command(self):
        """Test on command."""
        runner = CliRunner()
        
        with patch('ais.cli.main._toggle_auto_analysis') as mock_toggle:
            result = runner.invoke(on, [])
            
            assert result.exit_code == 0
            mock_toggle.assert_called_once_with(True)
    
    def test_off_command(self):
        """Test off command."""
        runner = CliRunner()
        
        with patch('ais.cli.main._toggle_auto_analysis') as mock_toggle:
            result = runner.invoke(off, [])
            
            assert result.exit_code == 0
            mock_toggle.assert_called_once_with(False)


class TestProviderCommands:
    """Test provider management commands."""
    
    def test_add_provider_command_success(self):
        """Test add provider command success."""
        runner = CliRunner()
        
        with patch('ais.cli.main._handle_provider_operation') as mock_handle:
            result = runner.invoke(add_provider_cmd, [
                'test_provider', 
                '--url', 'http://test.com',
                '--model', 'test_model',
                '--key', 'test_key'
            ])
            
            assert result.exit_code == 0
            mock_handle.assert_called_once()
    
    def test_add_provider_command_missing_args(self):
        """Test add provider command with missing arguments."""
        runner = CliRunner()
        
        result = runner.invoke(add_provider_cmd, ['test_provider'])
        
        assert result.exit_code == 0
        assert '错误: 缺少必需参数' in result.output
    
    def test_add_provider_command_help_detail(self):
        """Test add provider command help detail."""
        runner = CliRunner()
        result = runner.invoke(add_provider_cmd, ['--help-detail'])
        
        assert result.exit_code == 0
        assert 'ais add-provider 命令详细使用说明' in result.output
    
    def test_remove_provider_command(self):
        """Test remove provider command."""
        runner = CliRunner()
        
        with patch('ais.cli.main._handle_provider_operation') as mock_handle:
            result = runner.invoke(remove_provider_cmd, ['test_provider'])
            
            assert result.exit_code == 0
            mock_handle.assert_called_once()
    
    def test_use_provider_command(self):
        """Test use provider command."""
        runner = CliRunner()
        
        with patch('ais.cli.main._handle_provider_operation') as mock_handle:
            result = runner.invoke(use_provider_cmd, ['test_provider'])
            
            assert result.exit_code == 0
            mock_handle.assert_called_once()
    
    def test_list_provider_command(self):
        """Test list provider command."""
        runner = CliRunner()
        
        mock_config = {
            'default_provider': 'test_provider',
            'providers': {
                'test_provider': {
                    'model_name': 'test_model',
                    'base_url': 'http://test.com',
                    'api_key': 'test_key'
                }
            }
        }
        
        with patch('ais.cli.main.get_config', return_value=mock_config):
            result = runner.invoke(list_provider, [])
            
            assert result.exit_code == 0
            assert '可用的 AI 服务商' in result.output
            assert 'test_provider' in result.output
    
    def test_list_provider_command_empty(self):
        """Test list provider command with no providers."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_config', return_value={'providers': {}}):
            result = runner.invoke(list_provider, [])
            
            assert result.exit_code == 0
            assert '没有配置任何 AI 服务商' in result.output
    
    def test_list_provider_help_detail(self):
        """Test list provider help detail."""
        runner = CliRunner()
        result = runner.invoke(list_provider, ['--help-detail'])
        
        assert result.exit_code == 0
        assert 'ais list-provider 命令详细使用说明' in result.output


class TestAnalyzeCommand:
    """Test analyze command."""
    
    def test_analyze_error_command(self):
        """Test analyze error command."""
        runner = CliRunner()
        
        with patch('ais.cli.main.collect_context') as mock_context:
            with patch('ais.cli.main.get_config') as mock_config:
                with patch('ais.cli.main.analyze_error') as mock_analyze:
                    with patch('ais.cli.main.save_command_log') as mock_save:
                        with patch('ais.cli.main.get_similar_commands') as mock_similar:
                            mock_context.return_value = {'cwd': '/test'}
                            mock_config.return_value = {'test': 'config'}
                            mock_analyze.return_value = {
                                'explanation': 'Test explanation',
                                'suggestions': [{'command': 'test cmd', 'risk_level': 'safe'}]
                            }
                            mock_similar.return_value = []
                            
                            result = runner.invoke(analyze_error, [
                                '--exit-code', '1',
                                '--command', 'test command',
                                '--stderr', 'test error'
                            ])
                            
                            assert result.exit_code == 0
                            mock_analyze.assert_called_once()


class TestHistoryCommands:
    """Test history commands."""
    
    def test_show_history_command(self):
        """Test show history command."""
        runner = CliRunner()
        
        mock_log = Mock()
        mock_log.timestamp.strftime.return_value = '07-11 10:30'
        mock_log.original_command = 'ls -la'
        mock_log.exit_code = 0
        mock_log.ai_explanation = 'Test explanation'
        
        with patch('ais.cli.main.get_recent_logs', return_value=[mock_log]):
            result = runner.invoke(show_history, [])
            
            assert result.exit_code == 0
            assert '最近的命令历史' in result.output
    
    def test_show_history_command_help_detail(self):
        """Test show history command help detail."""
        runner = CliRunner()
        result = runner.invoke(show_history, ['--help-detail'])
        
        assert result.exit_code == 0
        assert 'ais history 命令详细使用说明' in result.output
    
    def test_show_history_detail_command(self):
        """Test show history detail command."""
        runner = CliRunner()
        
        mock_log = Mock()
        mock_log.timestamp = 'test_time'
        mock_log.username = 'test_user'
        mock_log.original_command = 'test_command'
        mock_log.exit_code = 1
        mock_log.stderr_output = 'test_error'
        mock_log.context_json = '{"cwd": "/test"}'
        mock_log.ai_explanation = 'Test explanation'
        mock_log.ai_suggestions_json = '[{"command": "test"}]'
        
        with patch('ais.cli.main.get_recent_logs', return_value=[mock_log]):
            result = runner.invoke(show_history_detail, ['1'])
            
            assert result.exit_code == 0
            assert '命令详细信息' in result.output
    
    def test_show_history_detail_invalid_index(self):
        """Test show history detail with invalid index."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_recent_logs', return_value=[]):
            result = runner.invoke(show_history_detail, ['999'])
            
            assert result.exit_code == 0
            assert '索引超出范围' in result.output


class TestSuggestCommand:
    """Test suggest command."""
    
    def test_suggest_command_success(self):
        """Test suggest command success."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_config') as mock_config:
            with patch('ais.cli.main.ask_ai') as mock_ask:
                mock_config.return_value = {'test': 'config'}
                mock_ask.return_value = 'Suggestion response'
                
                result = runner.invoke(suggest_command, ['compress files'])
                
                assert result.exit_code == 0
                mock_ask.assert_called_once()
    
    def test_suggest_command_no_task(self):
        """Test suggest command without task."""
        runner = CliRunner()
        result = runner.invoke(suggest_command, [])
        
        assert result.exit_code == 0
        assert '错误: 请提供任务描述' in result.output
    
    def test_suggest_command_help_detail(self):
        """Test suggest command help detail."""
        runner = CliRunner()
        result = runner.invoke(suggest_command, ['--help-detail'])
        
        assert result.exit_code == 0
        assert 'ais suggest 命令详细使用说明' in result.output


class TestLearnCommand:
    """Test learn command."""
    
    def test_learn_command_list_topics(self):
        """Test learn command list topics."""
        runner = CliRunner()
        result = runner.invoke(learn_command, [])
        
        assert result.exit_code == 0
        assert '可学习的主题' in result.output
        assert 'git - Git 版本控制基础' in result.output
    
    def test_learn_command_specific_topic(self):
        """Test learn command with specific topic."""
        runner = CliRunner()
        
        with patch('ais.cli.main.get_config') as mock_config:
            with patch('ais.cli.main.ask_ai') as mock_ask:
                mock_config.return_value = {'test': 'config'}
                mock_ask.return_value = 'Learning content'
                
                result = runner.invoke(learn_command, ['git'])
                
                assert result.exit_code == 0
                mock_ask.assert_called_once()
    
    def test_learn_command_help_detail(self):
        """Test learn command help detail."""
        runner = CliRunner()
        result = runner.invoke(learn_command, ['--help-detail'])
        
        assert result.exit_code == 0
        assert 'ais learn 命令详细使用说明' in result.output


class TestUtilityCommands:
    """Test utility commands."""
    
    def test_setup_shell_command(self):
        """Test setup shell command."""
        runner = CliRunner()
        
        with patch.dict('os.environ', {'SHELL': '/bin/bash'}):
            with patch('os.path.exists', return_value=True):
                result = runner.invoke(setup_shell, [])
                
                assert result.exit_code == 0
                assert 'Shell 集成' in result.output
    
    def test_test_integration_command(self):
        """Test integration test command."""
        runner = CliRunner()
        
        with patch('ais.cli.main.collect_context') as mock_context:
            with patch('ais.cli.main.get_config') as mock_config:
                with patch('ais.cli.main.analyze_error') as mock_analyze:
                    with patch('ais.cli.main.save_command_log') as mock_save:
                        mock_context.return_value = {'test': 'context'}
                        mock_config.return_value = {'test': 'config'}
                        mock_analyze.return_value = {'explanation': 'test'}
                        mock_save.return_value = 123
                        
                        result = runner.invoke(test_integration, [])
                        
                        assert result.exit_code == 0
    
    def test_which_command(self):
        """Test which command."""
        runner = CliRunner()
        result = runner.invoke(which_command, [])
        
        assert result.exit_code == 0
        assert '不知道用哪个命令？' in result.output
    
    def test_help_all_command(self):
        """Test help all command."""
        runner = CliRunner()
        result = runner.invoke(help_all, [])
        
        assert result.exit_code == 0
        assert 'AIS - AI 智能终端助手 详细帮助汇总' in result.output