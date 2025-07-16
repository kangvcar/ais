# 贡献指南

感谢您对 AIS 项目的关注和贡献！本文档将指导您如何参与项目开发，确保代码质量和项目的持续发展。

## 🤝 参与方式

### 贡献类型
- **🐛 Bug 修复**: 修复已知问题
- **✨ 新功能**: 添加新的功能特性
- **📝 文档改进**: 改进或翻译文档
- **🧪 测试增强**: 增加测试覆盖率
- **🎨 UI/UX 改进**: 改善用户体验
- **🔧 性能优化**: 优化代码性能

### 贡献流程
1. **Fork 项目** - 创建您的项目副本
2. **创建分支** - 基于 `main` 分支创建功能分支
3. **开发实现** - 实现您的功能或修复
4. **测试验证** - 确保代码通过所有测试
5. **提交 PR** - 提交拉取请求等待审查

## 🚀 开发环境设置

### 环境要求
- Python 3.8+
- Git
- 支持的操作系统：Linux、macOS

### 快速设置
```bash
# 1. Fork 并克隆项目
git clone https://github.com/YOUR_USERNAME/ais.git
cd ais

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 3. 安装开发依赖
pip install -e ".[dev]"

# 4. 验证安装
pytest tests/ -v
```

### 开发工具配置
```bash
# 安装代码质量工具
pip install black flake8 autopep8 mypy

# 配置 Git 钩子
pre-commit install

# 验证环境
ais --version
```

## 📝 代码规范

### 代码风格
- **PEP 8**: 遵循 Python 官方代码风格
- **行长度**: 最大 79 字符
- **命名规范**: 
  - 类名：`CamelCase`
  - 函数名：`snake_case`
  - 常量：`UPPER_CASE`
  - 私有成员：`_leading_underscore`

### 代码格式化
```bash
# 自动格式化代码
black src/ tests/
autopep8 --in-place --aggressive --aggressive --max-line-length=79 src/ tests/ -r

# 检查代码风格
flake8 src/ tests/ --max-line-length=79

# 类型检查
mypy src/ais/
```

### 导入规范
```python
# 标准库导入
import os
import sys
from pathlib import Path

# 第三方库导入
import click
from rich.console import Console

# 本地导入
from ais.core.config import Config
from ais.utils.logger import logger
```

## 🧪 测试要求

### 测试策略
- **单元测试**: 测试单个函数和类
- **集成测试**: 测试组件交互
- **端到端测试**: 测试完整用户场景
- **覆盖率目标**: 80%+

### 测试编写
```python
# 测试文件命名: test_*.py
# 测试函数命名: test_*

import pytest
from unittest.mock import Mock, patch
from ais.commands.ask import AskCommand

class TestAskCommand:
    def test_ask_command_basic(self):
        """测试基本问答功能"""
        cmd = AskCommand()
        result = cmd.execute("test question")
        assert result is not None
        
    @patch('ais.ai.client.OpenAIClient')
    def test_ask_command_with_mock(self, mock_client):
        """测试带模拟的问答功能"""
        mock_client.return_value.chat.return_value = "test response"
        cmd = AskCommand()
        result = cmd.execute("test question")
        assert result == "test response"
```

### 运行测试
```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_commands.py

# 运行特定测试
pytest tests/test_commands.py::TestAskCommand::test_ask_command_basic

# 运行覆盖率测试
pytest tests/ --cov=src/ais --cov-report=html
```

## 📋 提交规范

### 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 提交类型
- **feat**: 新功能
- **fix**: Bug 修复
- **docs**: 文档更新
- **style**: 代码风格修改
- **refactor**: 代码重构
- **test**: 测试相关
- **chore**: 构建/工具相关

### 提交示例
```bash
# 好的提交信息
feat(ask): 添加流式输出支持

添加了 AI 问答的流式输出功能，提升用户体验：
- 实时显示 AI 处理进度
- 支持三种显示模式
- 可通过配置开启/关闭

Closes #123

# 避免的提交信息
fix bug
update code
```

## 🔄 拉取请求流程

### PR 准备清单
- [ ] 代码通过所有测试
- [ ] 代码符合风格规范
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] 提交信息符合规范

### PR 模板
```markdown
## 变更类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 重构
- [ ] 性能优化

## 变更描述
简要描述此次变更的内容和目的。

## 测试
- [ ] 添加了新的测试
- [ ] 所有测试通过
- [ ] 手动测试通过

## 相关问题
Closes #123
```

### 审查流程
1. **自动检查**: CI/CD 自动运行测试
2. **代码审查**: 维护者审查代码质量
3. **功能验证**: 验证功能是否正常
4. **文档检查**: 确保文档完整性
5. **合并**: 通过审查后合并到主分支

## 📖 文档贡献

### 文档类型
- **用户文档**: 使用指南和教程
- **API 文档**: 代码接口文档
- **开发文档**: 开发者指南

### 文档规范
- **语言**: 中文为主，英文为辅
- **格式**: Markdown 格式
- **结构**: 清晰的层次结构
- **示例**: 包含实际可运行的示例

### 文档构建
```bash
# 进入文档目录
cd docs

# 安装依赖
npm install

# 本地预览
npm run dev

# 构建静态文件
npm run build
```

## 🐛 问题报告

### 问题类型
- **Bug 报告**: 软件错误或异常
- **功能请求**: 新功能建议
- **性能问题**: 性能相关问题
- **文档问题**: 文档错误或缺失

### 问题模板
```markdown
## 问题描述
清晰描述遇到的问题。

## 重现步骤
1. 运行命令 `ais ask "test"`
2. 观察输出结果
3. 发现错误信息

## 预期行为
描述预期的正常行为。

## 实际行为
描述实际发生的行为。

## 环境信息
- OS: Ubuntu 22.04
- Python: 3.9.7
- AIS: 0.3.2

## 日志信息
粘贴相关的错误日志。
```

## 🎯 开发指南

### 新功能开发
```bash
# 1. 创建功能分支
git checkout -b feature/new-feature

# 2. 实现功能
# 编写代码...

# 3. 添加测试
# 编写测试...

# 4. 运行测试
pytest tests/

# 5. 提交变更
git add .
git commit -m "feat: 添加新功能"

# 6. 推送分支
git push origin feature/new-feature
```

### Bug 修复
```bash
# 1. 创建修复分支
git checkout -b fix/bug-description

# 2. 重现问题
# 编写测试用例重现 bug

# 3. 修复问题
# 修改代码...

# 4. 验证修复
pytest tests/

# 5. 提交修复
git commit -m "fix: 修复特定问题"
```

## 📊 代码质量

### 质量指标
- **测试覆盖率**: 目标 80%+
- **代码复杂度**: 控制在合理范围
- **静态检查**: 通过 flake8 和 mypy
- **安全检查**: 通过 bandit 扫描

### 质量检查工具
```bash
# 代码覆盖率
pytest tests/ --cov=src/ais --cov-report=term-missing

# 代码复杂度
radon cc src/ --min C

# 安全检查
bandit -r src/

# 依赖检查
safety check
```

## 🚀 发布流程

### 版本号规范
- **主版本**: 重大变更，不兼容更新
- **次版本**: 新功能，向后兼容
- **修订版本**: Bug 修复，向后兼容

### 发布步骤
1. 更新版本号
2. 更新 CHANGELOG.md
3. 运行完整测试
4. 创建发布标签
5. 推送到远程仓库
6. 触发 CI/CD 流程

## 🎉 贡献者认可

### 贡献者列表
所有贡献者都会在 README.md 中得到认可。

### 贡献统计
- **代码贡献**: 按提交数量和代码行数
- **文档贡献**: 按文档页数和质量
- **问题解决**: 按解决问题数量和复杂度

---

## 联系方式

- **GitHub Issues**: 报告问题和建议
- **讨论区**: 技术讨论和问答
- **邮件**: 项目相关询问

---

::: tip 提示
新贡献者建议从标记为 "good first issue" 的问题开始，逐步熟悉项目结构。
:::

::: info 代码审查
所有代码都需要经过审查，这是确保代码质量的重要步骤。
:::

::: warning 注意
请确保您的代码符合项目的许可证要求，不要包含版权争议的代码。
:::