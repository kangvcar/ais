# AIS - 智能终端助手

[![PyPI version](https://badge.fury.io/py/ais-terminal.svg)](https://badge.fury.io/py/ais-terminal)
[![Python Support](https://img.shields.io/pypi/pyversions/ais-terminal.svg)](https://pypi.org/project/ais-terminal/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AIS (AI-powered Shell) 是一个智能终端助手，能够自动分析命令错误并提供修复建议。当你的命令执行失败时，AIS 会自动分析错误信息并给出智能的解决方案。

## ✨ 核心功能

- 🔍 **自动错误分析**：命令失败时自动分析错误原因
- 🤖 **AI 智能建议**：基于 AI 提供精准的修复建议
- ⚡ **零配置启动**：安装后自动设置，无需手动配置
- 🛡️ **安全防护**：危险命令执行前会进行确认
- 📊 **上下文感知**：理解当前目录、项目类型等环境信息
- 🔧 **多 AI 提供商**：支持多种 AI 服务，灵活配置

## 🚀 快速开始

### 安装

**方式一：Python 包管理器**
```bash
pip install ais-terminal
```

**方式二：一键安装脚本**
```bash
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
```

### 使用

安装完成后，AIS 会自动开始工作。当你的命令执行失败时，它会自动分析并提供建议：

```bash
$ ls /nonexistent-directory
ls: cannot access '/nonexistent-directory': No such file or directory

🤖 AIS 错误分析：
错误原因：目录 '/nonexistent-directory' 不存在
建议操作：
1. 检查路径是否正确
2. 创建目录：mkdir -p /nonexistent-directory
3. 查看当前目录内容：ls -la
```

你也可以手动分析任何命令：

```bash
# 分析指定命令的错误
ais analyze "ls /nonexistent" --exit-code=2 --stderr="No such file or directory"

# 查看配置
ais config

# 设置 AI 提供商
ais config set provider openai --api-key your-key
```

## 📖 详细文档

- [安装指南](INSTALLATION.md)
- [部署指南](DEPLOYMENT_GUIDE.md)
- [更新日志](CHANGELOG.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 [MIT 许可证](../LICENSE)。