source .venv/bin/activate && python3 -m pip install -e .

# Rules
1. 如果有新功能或者修复了程序请安装[Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)最佳实践更新CHANGELOG.md
2. 每次改动后提交一个详细的 git commit

# 代码质量检查和格式化最佳实践

## 自动代码格式化（推荐）
使用 autopep8 进行自动化代码格式化，这是最高效的方法：
```bash
# 安装 autopep8 black flake8
pip install autopep8 black flake8

# 自动修复所有代码格式问题
source .venv/bin/activate && black src/ tests/ && autopep8 --in-place --aggressive --aggressive --max-line-length=100 src/ tests/ -r && flake8 src/ tests/ --max-line-length=100
```

## 标准代码检查流程
每次 git commit 前运行以下命令：
```bash
# 运行测试
python -m pytest tests/ -v

# 代码格式化
source .venv/bin/activate && black src/ tests/

# 代码质量检查
source .venv/bin/activate && flake8 src/ tests/ --max-line-length=100
```

## 代码质量工具说明
- **autopep8**: 自动修复 PEP 8 代码风格违规（推荐优先使用）
- **black**: Python 代码格式化工具，统一代码风格
- **flake8**: 代码质量检查工具，检查语法错误和风格问题
- **pytest**: 运行单元测试，确保代码功能正确

## 最佳实践建议
1. **优先使用自动化工具**：使用 autopep8 替代手动修复格式问题
2. **设置最大行长度**：统一使用 100 字符限制
3. **批量处理**：使用 `-r` 参数递归处理所有文件
4. **激进修复**：使用 `--aggressive --aggressive` 修复更多问题

git commit 中不要包含以下内容：
```
🤖 Generated with Claude Code

Co-Authored-By: Claude noreply@anthropic.com
```

# 发布流程规范
## Package Release工作流注意事项
1. **发布前同步**：确保本地修改已推送到远程
   ```bash
   git pull origin main
   git push origin main
   ```
2. **发布后同步**：拉取工作流的自动提交
   ```bash
   git pull origin main  # 拉取工作流自动更新的CHANGELOG.md
   ```
3. **避免冲突**：不要在触发Package Release工作流的同时修改CHANGELOG.md