# AIS - AI 智能终端助手

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg" alt="Platform">
</p>

**AIS (AI-powered terminal assistant)** 是一个智能终端助手，通过 AI 技术帮助用户：

- 🤖 **自动错误分析** - 命令执行失败时自动分析原因并提供解决方案
- 💡 **智能建议** - 基于错误类型提供多种修复方案，按安全等级排序
- 📚 **学习功能** - 提供命令行知识教学，帮助用户理解命令原理
- 📖 **历史记录** - 记录和分析命令执行历史，提供类似错误的参考
- 🎯 **交互体验** - 提供友好的交互式菜单，支持命令编辑和执行

## 🚀 快速安装

### 方法1: PyPI 安装（推荐）

```bash
# 使用 pip 安装
pip install ais-terminal

# 或使用 pipx (推荐)
pipx install ais-terminal
```

### 方法2: 一键安装脚本

```bash
# Linux/macOS 快速安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

# 从源码安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --from-source
```

### 方法3: Windows PowerShell 安装

```powershell
# 管理员模式运行 PowerShell
iwr -useb https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.ps1 | iex
```

### 方法4: 手动安装

```bash
# 克隆仓库
git clone https://github.com/kangvcar/ais.git
cd ais

# 安装依赖并构建
pip install -e .
```

## 🏁 开始使用

安装完成后，请重新加载 shell 配置：

```bash
source ~/.bashrc  # 或 ~/.zshrc
```

### 测试自动错误分析

故意输错一个命令：

```bash
mkdirr /tmp/test  # 注意是 mkdirr 不是 mkdir
```

AIS 会自动检测到错误并提供分析和建议：

```
🤖 AI 错误分析

命令 mkdirr 是拼写错误，正确的命令应该是 mkdir...

? Select an action:
  ▸ 1. mkdir /tmp/test          ✅ (使用正确命令创建目录)
    2. Edit a command...
    3. Ask follow-up question  
    4. Exit
```

### 手动提问

```bash
ais ask "如何使用 docker 创建容器？"
```

### 学习命令行知识

```bash
ais learn git        # 学习 Git 命令
ais learn docker     # 学习 Docker 基础
ais learn            # 查看所有可学习主题
```

### 查看历史记录

```bash
ais history          # 查看最近的命令历史
ais history-detail 1 # 查看第1条记录的详细分析
```

## ⚙️ 配置

### 查看当前配置

```bash
ais config
```

### 开启/关闭自动分析

```bash
ais on               # 开启自动错误分析
ais off              # 关闭自动错误分析
```

### 配置 AI 服务商

AIS 内置免费的 AI 服务，也支持自定义服务商：

```bash
# 添加自定义 OpenAI 服务
ais add-provider my-openai --url https://api.openai.com/v1/chat/completions --model gpt-4 --key YOUR_API_KEY

# 添加本地 Ollama 服务
ais add-provider ollama --url http://localhost:11434/v1 --model llama3

# 切换服务商
ais use-provider my-openai

# 查看所有服务商
ais list-provider
```

### 高级配置

编辑配置文件：`~/.config/ais/config.toml`

```toml
# 自动错误分析开关
auto_analysis = true

# 上下文收集级别：minimal, standard, detailed
context_level = "standard"

# 敏感目录黑名单（不会收集这些目录的信息）
sensitive_dirs = ["~/.ssh", "~/.config/ais", "~/.aws"]
```

## 📋 所有命令

| 命令 | 说明 |
|------|------|
| `ais ask <问题>` | 向 AI 提问 |
| `ais analyze` | 手动分析上一个失败的命令 |
| `ais history` | 查看命令历史 |
| `ais history-detail <索引>` | 查看历史详情 |
| `ais learn [主题]` | 学习命令行知识 |
| `ais suggest <任务>` | 根据任务获取命令建议 |
| `ais config` | 查看配置 |
| `ais on/off` | 开启/关闭自动分析 |
| `ais add-provider` | 添加 AI 服务商 |
| `ais remove-provider` | 删除 AI 服务商 |
| `ais use-provider` | 切换 AI 服务商 |
| `ais list-provider` | 列出所有 AI 服务商 |
| `ais setup-shell` | 重新配置 shell 集成 |

## 🔧 故障排除

### AIS 命令找不到

```bash
# 检查是否在 PATH 中
echo $PATH | grep -q ".local/bin" || echo "PATH 配置有问题"

# 手动添加到 PATH
export PATH="$HOME/.local/bin:$PATH"

# 或重新安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/install.sh | bash
```

### 自动分析不工作

```bash
# 检查是否开启
ais config

# 如果显示关闭，手动开启
ais on

# 重新配置 shell 集成
ais setup-shell
source ~/.bashrc
```

### Python 版本问题

AIS 需要 Python 3.8 或更高版本：

```bash
python3 --version  # 检查版本

# Ubuntu/Debian 升级 Python
sudo apt update && sudo apt install python3.8 python3.8-pip

# macOS 通过 Homebrew 升级
brew install python@3.8
```

## 🔒 隐私和安全

- **本地优先** - 所有历史记录存储在本地数据库
- **敏感信息过滤** - 自动过滤密码、密钥等敏感信息
- **可配置上下文** - 可以控制收集的上下文信息级别
- **开源透明** - 所有代码开源，可审查数据处理逻辑

## 🗑️ 卸载

```bash
# 下载并运行卸载脚本
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/uninstall.sh | bash

# 或手动卸载
pipx uninstall ais-terminal
# 然后手动删除 ~/.bashrc 中的 AIS 集成部分
```

## 🤝 贡献

欢迎贡献代码！请查看 [贡献指南](CONTRIBUTING.md)。

### 开发环境设置

```bash
git clone https://github.com/kangvcar/ais.git
cd ais
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢所有贡献者的努力
- 基于 [Click](https://click.palletsprojects.com/) 构建 CLI 界面
- 使用 [Rich](https://rich.readthedocs.io/) 提供美观的终端输出
- 使用 [Questionary](https://questionary.readthedocs.io/) 实现交互式菜单

---

**🌟 如果 AIS 对你有帮助，请给我们一个 Star！**