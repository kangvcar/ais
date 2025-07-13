# AIS - AI终端助手 🤖

> **智能终端助手** - 让命令行更聪明，让学习更高效

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Package Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/kangvcar/ais)

AIS（AI-powered terminal assistant）是一个革命性的命令行工具，通过AI技术为终端用户提供智能错误分析、学习指导和操作建议。当命令执行失败时，AIS会自动分析原因并提供解决方案，帮助用户快速解决问题并学习相关知识。

![AIS Demo](docs/images/demo.gif)

## ✨ 核心特性

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

### 安装方式

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

#### 🌐 多用户环境 - 系统级安装（推荐）
```bash
# 方法1: 使用系统包管理器安装pipx后再安装AIS
sudo apt install pipx  # Ubuntu/Debian
# sudo yum install pipx  # CentOS/RHEL
# sudo brew install pipx  # macOS

# 安装AIS到系统位置（所有用户可用）
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal

# 方法2: 使用我们的全局安装脚本（更简单）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

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
| **pipx系统级** | 🟢 高 | ✅ 是 | 🟡 中等 | sudo | 多用户环境 |
| **系统全局** | 🟡 中 | ✅ 是 | 🟡 中等 | sudo | 运维环境 |
| **项目级** | 🟢 高 | ❌ 否 | 🟢 简单 | 普通用户 | 测试开发 |

### 智能安装脚本
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

# Windows PowerShell 安装
iwr -useb https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.ps1 | iex
```

### 快速配置

```bash
# 查看配置选项
ais config

# 添加AI服务商（以OpenAI为例）
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-4 \
  --key your_api_key

# 设置默认提供商
ais provider-use openai

# 设置Shell集成
ais setup
```

### 立即体验

```bash
# 向AI提问
ais ask "什么是Docker容器？"

# 学习Git知识
ais learn git

# 学习命令行知识
ais learn "git"

# 故意输入错误命令体验自动分析
nonexistent_command
```

## 📖 详细功能

### 智能问答 - `ais ask`

快速获取技术问题的答案，支持编程、运维、工具使用等各类问题：

```bash
ais ask "Git合并冲突如何解决？"
ais ask "Linux文件权限755表示什么？"
ais ask "如何优化Python脚本性能？"
```


### 知识学习 - `ais learn`

系统学习命令行工具和概念：

```bash
ais learn git      # 学习Git版本控制
ais learn docker   # 学习容器化技术
ais learn vim      # 学习文本编辑器
ais learn ssh      # 学习远程连接
```

### 历史管理

完整的命令历史记录和分析查看：

```bash
ais history                    # 查看最近的命令记录
ais history --failed-only     # 只显示失败的命令
ais history 3                 # 查看第3条记录的详细分析
```

### AI服务商管理

支持多种AI服务商，灵活切换：

```bash
# 查看可用服务商
ais provider-list

# 添加本地Ollama服务
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama3

# 切换服务商
ais provider-use ollama
```

## 🛠️ 高级配置

### Shell集成配置

AIS支持自动错误分析，需要配置Shell集成：

```bash
# 自动配置
ais setup

# 手动配置 - 添加到 ~/.bashrc 或 ~/.zshrc
source /path/to/ais/scripts/shell/integration.sh
```

### 上下文收集设置

控制错误分析时收集的上下文信息量：

```bash
# 设置上下文级别
ais config --set context_level=minimal    # 基本信息
ais config --set context_level=standard   # 标准信息（默认）
ais config --set context_level=detailed   # 详细信息

# 控制自动分析
ais config --set auto_analysis=true       # 开启自动分析
ais config --set auto_analysis=false      # 关闭自动分析
```

### 隐私和安全

AIS重视用户隐私和数据安全：

- **本地存储** - 所有数据存储在本地SQLite数据库
- **敏感信息过滤** - 自动过滤密码、密钥等敏感信息
- **可配置的上下文级别** - 用户可控制信息收集范围
- **开源透明** - 完全开源，代码公开透明

## 📁 项目结构

```
ais/
├── src/ais/              # 主要源代码
│   ├── cli/              # CLI界面模块
│   │   ├── main.py       # 主CLI入口
│   │   └── interactive.py # 交互式菜单
│   ├── core/             # 核心功能模块
│   │   ├── ai.py         # AI交互模块
│   │   ├── config.py     # 配置管理
│   │   ├── context.py    # 上下文收集
│   │   └── database.py   # 数据库操作
│   └── utils/            # 工具函数
├── scripts/              # 安装和部署脚本
│   ├── install.sh        # Linux/macOS安装脚本
│   ├── install.ps1       # Windows PowerShell安装脚本
│   ├── uninstall.sh      # 卸载脚本
│   └── shell/
│       └── integration.sh # Shell集成脚本
├── tests/                # 测试文件
├── docs/                 # 文档目录
│   ├── INSTALLATION.md   # 安装指南
│   ├── DEPLOYMENT_GUIDE.md # 部署指南
│   └── CHANGELOG.md      # 变更日志
└── pyproject.toml        # 项目配置
```

## 🔧 开发指南

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/kangvcar/ais.git
cd ais

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装开发版本
pip install -e .

# 运行测试
python -m pytest tests/ -v

# 代码格式化
black src/ tests/
flake8 src/ tests/
```

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行覆盖率测试
pytest --cov=ais tests/

# 测试特定模块
pytest tests/test_ai.py -v
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何参与

1. **Fork** 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 **Pull Request**

### 开发规范

- 遵循 [PEP 8](https://pep8.org/) 代码风格
- 为新功能添加测试用例
- 更新相关文档
- 提交信息使用清晰的描述

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 获取帮助

- 📚 [文档](docs/)
- 🐛 [问题反馈](https://github.com/kangvcar/ais/issues)
- 💬 [讨论区](https://github.com/kangvcar/ais/discussions)
- 📧 联系我们：ais@example.com

## 🎉 鸣谢

感谢所有为这个项目做出贡献的开发者们！

---

**让AI成为你的终端伙伴，让命令行学习变得简单而有趣！** 🚀