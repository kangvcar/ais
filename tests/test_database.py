"""Tests for database module."""

import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, Mock

import pytest
from sqlmodel import Session, create_engine

from ais.core.database import (
    CommandLog,
    get_database_path,
    get_engine,
    init_database,
    save_command_log,
    get_recent_logs,
    get_log_by_id,
    get_similar_commands,
    _execute_query
)


class TestDatabasePath:
    """Test database path functions."""
    
    def test_get_database_path(self):
        """Test getting database file path."""
        with patch('pathlib.Path.home') as mock_home:
            mock_home.return_value = Path('/home/test')
            
            db_path = get_database_path()
            
            assert db_path == Path('/home/test/.local/share/ais/history.db')


class TestDatabaseEngine:
    """Test database engine functions."""
    
    def test_get_engine(self):
        """Test getting database engine."""
        with patch('ais.core.database.get_database_path') as mock_path:
            mock_path.return_value = Path('/tmp/test.db')
            
            engine = get_engine()
            
            assert 'sqlite:////tmp/test.db' in str(engine.url)


class TestCommandLogModel:
    """Test CommandLog model."""
    
    def test_command_log_creation(self):
        """Test creating CommandLog instance."""
        log = CommandLog(
            username='testuser',
            original_command='ls -la',
            exit_code=0,
            stderr_output='',
            context_json='{"test": "context"}',
            ai_explanation='Test explanation',
            ai_suggestions_json='[{"command": "test"}]'
        )
        
        assert log.username == 'testuser'
        assert log.original_command == 'ls -la'
        assert log.exit_code == 0
        assert log.stderr_output == ''
        assert log.context_json == '{"test": "context"}'
        assert log.ai_explanation == 'Test explanation'
        assert log.ai_suggestions_json == '[{"command": "test"}]'
        assert isinstance(log.timestamp, datetime)


class TestDatabaseOperations:
    """Test database operations."""
    
    def setUp(self):
        """Set up test database."""
        self.engine = create_engine("sqlite:///:memory:")
        
    def test_init_database(self):
        """Test database initialization."""
        with patch('ais.core.database.get_engine') as mock_get_engine:
            mock_engine = Mock()
            mock_get_engine.return_value = mock_engine
            
            with patch('sqlmodel.SQLModel.metadata.create_all') as mock_create:
                init_database()
                
                mock_create.assert_called_once_with(mock_engine)
    
    def test_save_command_log_minimal(self):
        """Test saving command log with minimal data."""
        with patch('ais.core.database.init_database'):
            with patch('ais.core.database.get_engine') as mock_get_engine:
                mock_engine = create_engine("sqlite:///:memory:")
                mock_get_engine.return_value = mock_engine
                
                # Initialize the database
                from sqlmodel import SQLModel
                SQLModel.metadata.create_all(mock_engine)
                
                with patch('ais.core.database.Session', return_value=Session(mock_engine)) as mock_session_class:
                    log_id = save_command_log(
                        username='testuser',
                        command='ls -la',
                        exit_code=0
                    )
                    
                    assert isinstance(log_id, int)
    
    def test_save_command_log_full(self):
        """Test saving command log with full data."""
        with patch('ais.core.database.init_database'):
            with patch('ais.core.database.get_engine') as mock_get_engine:
                mock_engine = create_engine("sqlite:///:memory:")
                mock_get_engine.return_value = mock_engine
                
                from sqlmodel import SQLModel
                SQLModel.metadata.create_all(mock_engine)
                
                context = {'cwd': '/home/user', 'files': ['test.txt']}
                suggestions = [{'command': 'ls', 'risk_level': 'safe'}]
                
                with patch('ais.core.database.Session', return_value=Session(mock_engine)):
                    log_id = save_command_log(
                        username='testuser',
                        command='ls /nonexistent',
                        exit_code=2,
                        stderr='No such file or directory',
                        context=context,
                        ai_explanation='File not found',
                        ai_suggestions=suggestions
                    )
                    
                    assert isinstance(log_id, int)
    
    def test_execute_query(self):
        """Test executing database query."""
        mock_session = Mock()
        mock_result = Mock()
        mock_result.all.return_value = ['result1', 'result2']
        mock_session.exec.return_value = mock_result
        
        with patch('ais.core.database.init_database'):
            with patch('ais.core.database.get_engine'):
                with patch('ais.core.database.Session', return_value=mock_session):
                    statement = Mock()
                    result = _execute_query(statement)
                    
                    assert result == ['result1', 'result2']
                    mock_session.exec.assert_called_once_with(statement)
    
    def test_get_recent_logs(self):
        """Test getting recent logs."""
        mock_logs = [Mock(), Mock(), Mock()]
        
        with patch('ais.core.database._execute_query') as mock_execute:
            mock_execute.return_value = mock_logs
            
            result = get_recent_logs(limit=3)
            
            assert result == mock_logs
            mock_execute.assert_called_once()
    
    def test_get_log_by_id_found(self):
        """Test getting log by ID when found."""
        mock_log = Mock()
        mock_session = Mock()
        mock_session.get.return_value = mock_log
        
        with patch('ais.core.database.init_database'):
            with patch('ais.core.database.get_engine'):
                with patch('ais.core.database.Session', return_value=mock_session):
                    result = get_log_by_id(123)
                    
                    assert result == mock_log
                    mock_session.get.assert_called_once_with(CommandLog, 123)
    
    def test_get_log_by_id_not_found(self):
        """Test getting log by ID when not found."""
        mock_session = Mock()
        mock_session.get.return_value = None
        
        with patch('ais.core.database.init_database'):
            with patch('ais.core.database.get_engine'):
                with patch('ais.core.database.Session', return_value=mock_session):
                    result = get_log_by_id(999)
                    
                    assert result is None
    
    def test_get_similar_commands_found(self):
        """Test getting similar commands when found."""
        # Create mock logs
        mock_log1 = Mock()
        mock_log1.original_command = 'git status'
        mock_log2 = Mock() 
        mock_log2.original_command = 'git commit'
        mock_log3 = Mock()
        mock_log3.original_command = 'ls -la'
        
        all_logs = [mock_log1, mock_log2, mock_log3]
        
        with patch('ais.core.database._execute_query') as mock_execute:
            mock_execute.return_value = all_logs
            
            result = get_similar_commands('git push', limit=2)
            
            # Should find git-related commands
            assert len(result) == 2
            assert mock_log1 in result
            assert mock_log2 in result
            assert mock_log3 not in result
    
    def test_get_similar_commands_not_found(self):
        """Test getting similar commands when none found."""
        mock_log = Mock()
        mock_log.original_command = 'completely different command'
        
        with patch('ais.core.database._execute_query') as mock_execute:
            mock_execute.return_value = [mock_log]
            
            result = get_similar_commands('git push', limit=2)
            
            assert len(result) == 0
    
    def test_get_similar_commands_exact_limit(self):
        """Test getting similar commands respects limit."""
        # Create many similar mock logs
        mock_logs = []
        for i in range(10):
            mock_log = Mock()
            mock_log.original_command = f'git command-{i}'
            mock_logs.append(mock_log)
        
        with patch('ais.core.database._execute_query') as mock_execute:
            mock_execute.return_value = mock_logs
            
            result = get_similar_commands('git push', limit=3)
            
            # Should respect the limit
            assert len(result) == 3