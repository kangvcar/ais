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
autopep8 --in-place --aggressive --aggressive --max-line-length=79 src/ tests/ -r
```

## 标准代码检查流程
每次 git commit 前运行以下命令：
```bash
# 运行测试
python -m pytest tests/ -v

# 代码格式化（如果没有用 autopep8）
black src/ tests/

# 代码质量检查
flake8 src/ tests/ --max-line-length=79
```
