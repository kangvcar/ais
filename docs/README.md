# AIS - AI智能终端助手

<div align="center">

**让命令行更智能，让学习更高效**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../LICENSE)
[![Package Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/kangvcar/ais)

[📖 主项目README](../README.md) · [🛠️ 安装指南](INSTALLATION.md) · [🐳 Docker指南](DOCKER_GUIDE.md) · [🏢 部署指南](DEPLOYMENT_GUIDE.md)

</div>

---

## 概述

AIS（AI-powered terminal assistant）是一个革命性的命令行工具，通过AI技术为终端用户提供智能错误分析、学习指导和操作建议。当命令执行失败时，AIS会自动分析原因并提供解决方案，帮助用户快速解决问题并学习相关知识。

## ✨ 核心功能

### 🔍 智能错误分析
- **自动检测** - 命令失败时自动分析错误原因
- **上下文感知** - 结合当前目录、Git状态、项目类型等环境信息  
- **个性化建议** - 基于用户技能水平提供针对性解决方案
- **安全等级** - 每个建议都标注风险等级，确保操作安全

### 📚 智能学习系统
- **交互式教学** - 解释"为什么"而不只是"怎么做"
- **主题学习** - 深入学习Git、Docker、Vim等专题知识
- **渐进式内容** - 根据用户水平调整教学深度
- **实践导向** - 提供可执行的命令示例和最佳实践

### 🎯 多模式交互
- **问答模式** - `ais ask` 快速获取问题答案
- **学习模式** - `ais learn` 系统学习命令行知识
- **分析模式** - 自动或手动分析命令错误

### 🔌 强大的集成能力
- **Shell集成** - 支持Bash、Zsh、PowerShell自动错误捕获
- **多AI支持** - 兼容OpenAI、Ollama、Claude等多种AI服务
- **隐私保护** - 本地数据存储，敏感信息自动过滤
- **跨平台** - 支持Linux、macOS、Windows

## 🚀 快速开始

### 安装

AIS 提供多种安装方式，请根据使用场景选择：

#### 🎯 个人使用（推荐）
```bash
# 安装pipx（如果没有）
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# 安装AIS（仅当前用户可用）
pipx install ais-terminal

# 设置shell集成
ais setup
```
> ✨ **最佳实践**：安全隔离，无需sudo，符合Python标准

#### 🌐 多用户环境 - pipx全局（推荐）
```bash
# 安装pipx（如果没有）
sudo apt install pipx  # 或 sudo pip install pipx

# 全局安装AIS（所有用户可用）
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal

# 每个用户设置shell集成
ais setup
```
> 🎯 **推荐**：既有pipx的隔离优势，又支持多用户

#### 🏢 多用户/运维环境
```bash
# 全局安装（所有用户可用）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
```
> 🔧 **适用于**：服务器、开发机、CI/CD环境

#### 🧪 开发/测试环境
```bash
# 项目虚拟环境中
pip install ais-terminal
```

#### 📋 安装方式对比

| 方式 | 安全性 | 多用户 | 管理难度 | 权限需求 | 适用场景 |
|------|--------|--------|----------|----------|----------|
| **pipx用户级** | 🟢 高 | ❌ 否 | 🟢 简单 | 普通用户 | 个人开发 |
| **pipx全局** | 🟢 高 | ✅ 是 | 🟢 简单 | sudo | 多用户环境 |
| **系统全局** | 🟡 中 | ✅ 是 | 🟡 中等 | sudo | 运维环境 |
| **项目级** | 🟢 高 | ❌ 否 | 🟢 简单 | 普通用户 | 测试开发 |

### 使用示例

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

你也可以手动使用各种功能：

```bash
# AI问答
ais ask "如何查看系统内存使用情况？"

# 主题学习
ais learn git

# 查看历史记录
ais history

# 配置管理
ais config
ais provider-list
```

## 📖 完整文档

- [📖 主项目README](../README.md) - 完整的项目介绍和使用指南
- [🛠️ 安装指南](INSTALLATION.md) - 详细的安装说明和故障排除
- [🐳 Docker指南](DOCKER_GUIDE.md) - 容器化部署方案
- [🏢 部署指南](DEPLOYMENT_GUIDE.md) - 生产环境部署指南
- [🔧 开发指南](DEVELOPMENT.md) - 开发环境设置和贡献代码
- [📊 更新日志](CHANGELOG.md) - 版本更新记录

## 🆘 获取帮助

### 自助资源
```bash
# 一键诊断
ais doctor

# 详细调试
ais --debug --version

# 查看所有帮助
ais help-all
```

### 社区支持
- 💬 [GitHub Discussions](https://github.com/kangvcar/ais/discussions) - 交流讨论
- 🐛 [GitHub Issues](https://github.com/kangvcar/ais/issues) - 问题反馈
- 📧 [邮件支持](mailto:ais@example.com) - 直接联系

## 🤝 贡献

我们欢迎所有形式的贡献！请查看[贡献指南](DEVELOPMENT.md)了解详细信息。

1. Fork 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 [MIT 许可证](../LICENSE) - 查看文件了解详情。

---

<div align="center">

**🎉 让AI成为你的终端伙伴，让命令行学习变得简单而有趣！**

[回到顶部](#ais---ai智能终端助手)

</div>