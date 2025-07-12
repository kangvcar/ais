source .venv/bin/activate && python3 -m pip install -e .

# Rules
1. 如果有新功能或者修复了程序请必须更新CHANGELOG.md
2. 每次改动后尽可能提交一个详细的 git commit
3. 每次 git commit 前运行测试和代码格式化：
```
python -m pytest tests/ -v
black src/ tests/
flake8 src/ tests/
```