source .venv/bin/activate && python3 -m pip install -e .

# Rules
1. 如果有新功能或者修复了程序请必须更新CHANGELOG.md
2. 每次改动后尽可能提交一个详细的 git commit

# 代码质量检查和格式化最佳实践

## 自动代码格式化（推荐）
使用 autopep8 进行自动化代码格式化，这是最高效的方法：
```bash
# 安装 autopep8
pip install autopep8

# 自动修复所有代码格式问题
source .venv/bin/activate && autopep8 --in-place --aggressive --aggressive --max-line-length=79 src/ tests/ -r
```

## 标准代码检查流程
每次 git commit 前运行以下命令：
```bash
# 运行测试
python -m pytest tests/ -v

# 代码格式化
source .venv/bin/activate && black src/ tests/

# 代码质量检查
source .venv/bin/activate && flake8 src/ tests/ --max-line-length=79
```

## 代码质量工具说明
- **autopep8**: 自动修复 PEP 8 代码风格违规（推荐优先使用）
- **black**: Python 代码格式化工具，统一代码风格
- **flake8**: 代码质量检查工具，检查语法错误和风格问题
- **pytest**: 运行单元测试，确保代码功能正确

## 最佳实践建议
1. **优先使用自动化工具**：使用 autopep8 替代手动修复格式问题
2. **设置最大行长度**：统一使用 79 字符限制
3. **批量处理**：使用 `-r` 参数递归处理所有文件
4. **激进修复**：使用 `--aggressive --aggressive` 修复更多问题
