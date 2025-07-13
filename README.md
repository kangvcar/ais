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

### ⚡ 一键安装（推荐）

```bash
# 智能安装 - 自动检测环境并选择最佳方式
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
```

**安装脚本会自动：**
- 🔍 检测当前环境（个人/团队/容器）
- 🎯 选择最佳安装方式（pipx用户级/系统级/容器化）
- 📦 安装pipx和AIS
- 🔧 配置shell集成
- ✅ 执行健康检查

### 🎯 按需求选择安装方式

#### 👨‍💻 个人开发者
```bash
# 用户级安装（最安全）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --user

# 或手动安装
pipx install ais-terminal
ais setup
```

#### 🏢 团队/企业环境
```bash
# 系统级安装（所有用户可用）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system
```

#### 🐳 容器/云环境
```bash
# Docker容器化安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/docker-install.sh | bash

# 或直接运行
docker run -it --rm ais-terminal:latest
```

#### 🔧 开发者/贡献者
```bash
# 源码安装
git clone https://github.com/kangvcar/ais.git
cd ais
pipx install -e .
```

### 📊 安装方式对比

| 用户类型 | 推荐方式 | 安全性 | 简单度 | 权限需求 | 推荐指数 |
|---------|---------|-------|-------|---------|----------|
| 👨‍💻 **个人开发者** | pipx用户级 | 🟢 最高 | 🟢 最简单 | 普通用户 | ⭐⭐⭐⭐⭐ |
| 🏢 **团队企业** | pipx全局 | 🟢 高 | 🟢 简单 | sudo | ⭐⭐⭐⭐⭐ |
| 🐳 **容器部署** | Docker | 🟢 高 | 🟢 简单 | docker | ⭐⭐⭐⭐⭐ |
| 🔧 **开发贡献** | 源码安装 | 🟡 中等 | 🟡 中等 | 看情况 | ⭐⭐⭐⭐ |

### ✅ 验证安装

```bash
# 检查版本
ais --version

# 测试基本功能
ais ask "你好，AIS！"

# 测试自动错误分析（故意输错命令）
mkdirr /tmp/test
```

### ⚙️ 基础配置

```bash
# 查看当前配置
ais config

# 设置API提供商（可选）
ais config set provider openai
ais config set api_key "your-api-key"

# 调整分析级别
ais config set analysis_level detailed
```

### 🎮 立即体验

```bash
# AI对话
ais ask "如何查看系统内存使用情况？"
ais ask "Docker容器如何挂载目录？"

# 智能错误分析
pytho --version        # 拼写错误
ls /not/exist         # 路径不存在
git statuss           # 命令错误

# 命令建议
ais suggest "我想压缩一个文件夹"
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
python3 -m venv .venv
source .venv/bin/activate

# 安装开发版本和依赖
pip install -e ".[dev]"

# 设置pre-commit
pre-commit install

# 运行测试
python -m pytest tests/ -v

# 代码质量检查
source .venv/bin/activate && black src/ tests/
source .venv/bin/activate && flake8 src/ tests/ --max-line-length=79
source .venv/bin/activate && autopep8 --in-place --aggressive --aggressive --max-line-length=79 src/ tests/ -r
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

## 📚 文档导航

- 📖 [快速开始指南](docs/QUICK_START.md) - 5分钟上手
- 🛠️ [完整安装指南](docs/INSTALLATION.md) - 详细安装说明
- 🐳 [Docker部署指南](docs/DOCKER_GUIDE.md) - 容器化部署
- 🏢 [企业部署指南](docs/DEPLOYMENT_GUIDE.md) - 生产环境
- 🔧 [配置指南](docs/CONFIGURATION.md) - 高级配置
- 👨‍💻 [开发指南](docs/DEVELOPMENT.md) - 贡献代码

## 🆘 获取帮助

### 自助资源
```bash
# 一键诊断
ais doctor

# 详细调试
ais --debug --version
```

### 社区支持
- 📚 [完整文档](docs/)
- 💬 [GitHub Discussions](https://github.com/kangvcar/ais/discussions) - 交流讨论
- 🐛 [GitHub Issues](https://github.com/kangvcar/ais/issues) - 问题反馈
- 📧 [邮件支持](mailto:ais@example.com) - 直接联系

## 🎉 鸣谢

感谢所有为这个项目做出贡献的开发者们！

---

---

🎉 **让AI成为你的终端伙伴，让命令行学习变得简单而有趣！**

如果觉得有用，请给我们点个 ⭐️ 支持！

[![Stars](https://img.shields.io/github/stars/kangvcar/ais?style=social)](https://github.com/kangvcar/ais/stargazers)
[![Forks](https://img.shields.io/github/forks/kangvcar/ais?style=social)](https://github.com/kangvcar/ais/network/members)