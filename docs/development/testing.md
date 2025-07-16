# 测试指南

AIS 项目采用全面的测试策略，确保代码质量和功能稳定性。本文档介绍测试框架、测试类型和最佳实践。

## 🧪 测试框架

### 主要工具
- **pytest**: 测试框架
- **unittest.mock**: 模拟对象
- **pytest-cov**: 覆盖率测试
- **pytest-asyncio**: 异步测试支持
- **pytest-xdist**: 并行测试

### 测试环境设置
```bash
# 安装测试依赖
pip install -e ".[test]"

# 安装完整开发依赖
pip install -e ".[dev]"

# 验证安装
pytest --version
```

## 📊 测试类型

### 单元测试
测试单个函数或类的功能。

```python
# tests/test_utils.py
import pytest
from ais.utils.text import sanitize_text

class TestTextUtils:
    def test_sanitize_text_basic(self):
        """测试基本文本清理功能"""
        text = "Hello, World!"
        result = sanitize_text(text)
        assert result == "Hello, World!"
        
    def test_sanitize_text_with_secrets(self):
        """测试敏感信息过滤"""
        text = "password=secret123"
        result = sanitize_text(text)
        assert "secret123" not in result
        
    @pytest.mark.parametrize("input_text,expected", [
        ("normal text", "normal text"),
        ("api_key=abc123", "api_key=***"),
        ("token:xyz789", "token:***"),
    ])
    def test_sanitize_text_parametrized(self, input_text, expected):
        """参数化测试"""
        result = sanitize_text(input_text)
        assert result == expected
```

### 集成测试
测试组件间的交互。

```python
# tests/test_integration.py
import pytest
from unittest.mock import Mock, patch
from ais.commands.ask import AskCommand
from ais.core.config import Config

class TestAskIntegration:
    @pytest.fixture
    def mock_config(self):
        """配置模拟对象"""
        config = Mock(spec=Config)
        config.get_ai_provider.return_value = "openai"
        config.get_language.return_value = "zh-CN"
        return config
        
    @pytest.fixture
    def ask_command(self, mock_config):
        """创建测试命令对象"""
        with patch('ais.commands.ask.get_config', return_value=mock_config):
            return AskCommand()
            
    @patch('ais.ai.openai_client.OpenAIClient')
    def test_ask_command_with_openai(self, mock_client, ask_command):
        """测试与 OpenAI 的集成"""
        mock_client.return_value.chat.return_value = "Test response"
        
        result = ask_command.execute("test question")
        
        assert result == "Test response"
        mock_client.return_value.chat.assert_called_once()
```

### 端到端测试
测试完整的用户场景。

```python
# tests/test_e2e.py
import pytest
import subprocess
import tempfile
import os

class TestE2E:
    def test_full_workflow(self):
        """测试完整的用户工作流"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 设置测试环境
            env = os.environ.copy()
            env['AIS_CONFIG_DIR'] = tmpdir
            
            # 1. 初始化配置
            result = subprocess.run(
                ['ais', 'config', 'set', 'language', 'zh-CN'],
                env=env,
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
            
            # 2. 测试 AI 问答
            result = subprocess.run(
                ['ais', 'ask', 'test question'],
                env=env,
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
            assert "test" in result.stdout.lower()
```

## 🎯 测试最佳实践

### 测试文件组织
```
tests/
├── unit/                    # 单元测试
│   ├── test_commands.py
│   ├── test_utils.py
│   └── test_ai.py
├── integration/            # 集成测试
│   ├── test_shell_integration.py
│   └── test_ai_integration.py
├── e2e/                   # 端到端测试
│   └── test_workflows.py
├── fixtures/              # 测试数据
│   ├── sample_config.yaml
│   └── sample_responses.json
└── conftest.py           # 共享配置
```

### 测试命名规范
```python
# 类名：Test + 被测试的类名
class TestAskCommand:
    pass

# 方法名：test_ + 功能描述
def test_ask_command_returns_response(self):
    pass
    
def test_ask_command_handles_empty_input(self):
    pass
    
def test_ask_command_raises_error_on_invalid_provider(self):
    pass
```

### 测试数据管理
```python
# conftest.py
import pytest
import json
from pathlib import Path

@pytest.fixture
def sample_config():
    """提供示例配置"""
    return {
        "language": "zh-CN",
        "ai_provider": "openai",
        "context_level": "standard"
    }

@pytest.fixture
def sample_responses():
    """提供示例响应数据"""
    fixtures_dir = Path(__file__).parent / "fixtures"
    with open(fixtures_dir / "sample_responses.json") as f:
        return json.load(f)
```

## 🔧 测试工具和技巧

### 模拟对象
```python
from unittest.mock import Mock, patch, MagicMock

# 模拟函数
@patch('ais.utils.network.check_internet_connection')
def test_with_mocked_network(mock_check):
    mock_check.return_value = True
    # 测试代码...

# 模拟类
@patch('ais.ai.openai_client.OpenAIClient')
def test_with_mocked_client(mock_client_class):
    mock_instance = Mock()
    mock_client_class.return_value = mock_instance
    mock_instance.chat.return_value = "mocked response"
    # 测试代码...

# 模拟属性
@patch.object(Config, 'get_ai_provider', return_value='openai')
def test_with_mocked_config(mock_get_provider):
    # 测试代码...
```

### 异步测试
```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    """测试异步函数"""
    result = await some_async_function()
    assert result is not None

@pytest.mark.asyncio
async def test_async_with_timeout():
    """测试带超时的异步函数"""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_async_function(), timeout=1.0)
```

### 临时文件和目录
```python
import tempfile
import pytest
from pathlib import Path

@pytest.fixture
def temp_dir():
    """创建临时目录"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

def test_file_operations(temp_dir):
    """测试文件操作"""
    test_file = temp_dir / "test.txt"
    test_file.write_text("test content")
    
    # 测试代码...
    assert test_file.read_text() == "test content"
```

## 📊 覆盖率测试

### 运行覆盖率测试
```bash
# 基本覆盖率测试
pytest tests/ --cov=src/ais

# 生成详细报告
pytest tests/ --cov=src/ais --cov-report=html

# 显示缺失的行
pytest tests/ --cov=src/ais --cov-report=term-missing

# 设置覆盖率阈值
pytest tests/ --cov=src/ais --cov-fail-under=80
```

### 覆盖率配置
```ini
# .coveragerc
[run]
source = src/ais
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */settings/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

## 🚀 性能测试

### 基准测试
```python
import pytest
import time

@pytest.mark.benchmark
def test_performance_benchmark(benchmark):
    """性能基准测试"""
    def function_to_test():
        # 被测试的函数
        return expensive_operation()
    
    result = benchmark(function_to_test)
    assert result is not None

@pytest.mark.slow
def test_slow_operation():
    """标记为慢速测试"""
    start_time = time.time()
    result = slow_operation()
    end_time = time.time()
    
    assert end_time - start_time < 10  # 不应超过10秒
    assert result is not None
```

### 内存使用测试
```python
import pytest
import tracemalloc

def test_memory_usage():
    """测试内存使用"""
    tracemalloc.start()
    
    # 执行操作
    result = memory_intensive_operation()
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # 验证内存使用在合理范围内
    assert peak < 100 * 1024 * 1024  # 不超过100MB
```

## 🔍 测试调试

### 调试技巧
```python
# 使用 pytest 的调试功能
pytest tests/test_commands.py::test_specific_function -vv -s

# 进入调试模式
pytest --pdb tests/test_commands.py

# 在失败时进入调试
pytest --pdb-trace tests/test_commands.py

# 只运行失败的测试
pytest --lf tests/
```

### 日志测试
```python
import logging
from unittest.mock import patch

def test_logging_output(caplog):
    """测试日志输出"""
    with caplog.at_level(logging.INFO):
        function_that_logs()
    
    assert "Expected log message" in caplog.text
    assert caplog.records[0].levelname == "INFO"
```

## 🎨 测试自动化

### 持续集成配置
```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[test]"
    
    - name: Run tests
      run: pytest tests/ --cov=src/ais --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1
```

### 预提交钩子
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: pytest tests/
        language: system
        pass_filenames: false
        always_run: true
```

## 📋 测试检查清单

### 新功能测试
- [ ] 单元测试覆盖核心逻辑
- [ ] 集成测试验证组件交互
- [ ] 边界条件测试
- [ ] 错误处理测试
- [ ] 性能测试（如适用）

### 测试质量检查
- [ ] 测试名称清晰描述功能
- [ ] 测试独立且可重复
- [ ] 使用适当的断言
- [ ] 清理测试数据
- [ ] 覆盖率达到要求

### 代码审查检查
- [ ] 测试逻辑正确
- [ ] 模拟对象使用恰当
- [ ] 测试数据合理
- [ ] 性能影响可接受
- [ ] 文档完整

---

## 下一步

- [架构设计](./architecture) - 了解项目架构
- [贡献指南](./contributing) - 参与项目贡献
- [故障排除](../troubleshooting/common-issues) - 解决测试问题

---

::: tip 提示
编写测试时，先考虑测试场景，再编写实现代码，这样能确保代码的可测试性。
:::

::: info 测试策略
遵循测试金字塔原则：大量单元测试，适量集成测试，少量端到端测试。
:::

::: warning 注意
避免过度模拟，确保测试仍然能够捕获真实的问题。
:::