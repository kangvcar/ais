# 安装指南

AIS 支持多种安装方式，推荐使用一键安装脚本自动检测环境并选择最佳安装方式。

## 🚀 一键安装（推荐）

### 国内外通用安装
```bash
# 推荐：一键安装脚本（自动检测环境）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

# 国内用户可使用Gitee镜像（更快更稳定）
curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/install.sh | bash
```

### 特定安装模式
```bash
# 用户级安装（推荐）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --user

# 系统级安装（需要sudo权限）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system
```

**一键安装脚本特性：**
- 🔍 自动检测操作系统和Python版本
- 📦 智能选择最佳安装方式（pipx/pip/编译）
- 🛠️ 自动处理依赖安装和环境配置
- 🚀 自动设置Shell集成
- 📊 支持20+种Linux发行版
- 🏗️ 自动编译Python（CentOS 7.x/Kylin Linux）

## 📦 手动安装方式

### 方式 1: 使用 pipx 安装（推荐）

```bash
# 安装 pipx（如果尚未安装）
pip install pipx

# 基础安装
pipx install ais-terminal

# 或完整安装（包含HTML可视化报告功能）
pipx install "ais-terminal[html]"

# 验证安装
ais --version

# 验证HTML功能（如果安装了html扩展）
ais report --html --help
```

### 方式 2: 使用 pip 安装

```bash
# 基础安装
pip install ais-terminal

# 完整安装（包含HTML可视化报告功能）
pip install "ais-terminal[html]"

# 用户安装
pip install --user "ais-terminal[html]"
```

### 方式 3: 从源码安装

```bash
# 克隆仓库
git clone https://github.com/kangvcar/ais.git
cd ais

# 创建虚拟环境并安装
python3 -m venv .venv
source .venv/bin/activate

# 基础安装
python3 -m pip install -e .

# 或完整安装（包含开发工具和HTML可视化功能）
python3 -m pip install -e ".[dev,html]"

# 验证安装
ais --version
ais report --html --help  # 如果安装了html扩展
```

### 方式 4: 使用 Docker

```bash
# 使用Docker快速安装脚本
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/docker-install.sh | bash

# 或手动拉取镜像
docker pull kangvcar/ais:latest
docker run -it kangvcar/ais:latest
```

## 🔧 系统要求

### 支持的操作系统
- **Linux**: Ubuntu 18.04+, CentOS 7+, Debian 10+, Rocky Linux 8+, openEuler 22+, Kylin Linux V10
- **macOS**: macOS 10.14+
- **Windows**: Windows 10+ (通过 WSL)

### 依赖要求
- **Python**: 3.8 或更高版本（一键安装脚本会自动处理旧版本）
- **Shell**: Bash 4.0+, Zsh 5.0+

### 支持的Linux发行版
**自动检测和适配的发行版：**
- Ubuntu 20.04/22.04/24.04
- CentOS 7.x/8.x/9.x
- Rocky Linux 8.x/9.x
- CentOS Stream 8/9
- Fedora 33-41
- Debian 11.x/12.x
- openEuler 22.x/24.x
- Kylin Linux Advanced Server V10

**特殊处理：**
- CentOS 7.x: 自动编译Python 3.10.9（含OpenSSL 1.1补丁）
- Kylin Linux V10: 自动编译Python 3.10.9（优化编译）
- Ubuntu 24.04/Debian 12: 自动使用pipx（避免externally-managed-environment错误）

### 必要依赖
```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip curl

# CentOS/RHEL
sudo yum install python3 python3-pip curl

# macOS
brew install python3 curl
```

## 🚀 快速验证

### 检查安装
```bash
# 检查 AIS 版本
ais --version

# 检查系统兼容性
ais test-integration

# 查看帮助信息
ais --help
```

### 基本功能测试
```bash
# 测试 AI 问答功能
ais ask "什么是 AIS？"

# 测试配置功能
ais config show

# 测试历史记录
ais history --limit 5

# 测试学习报告功能
ais report

# 测试HTML可视化报告（如果安装了html扩展）
ais report --html -o test_report.html
```

## ⚙️ 初始配置

### 1. 配置 AI 服务提供商

AIS 内置了免费的AI服务，开箱即用。也支持配置自定义AI服务提供商：

#### 内置免费服务（开箱即用）
```bash
# 查看当前配置（包含内置免费服务）
ais config

# 内置服务已配置：
# - 提供商：default_free
# - 模型：gpt-4o-mini
# - 免费API密钥：已内置
```

#### 添加 OpenAI 服务
```bash
# 添加 OpenAI 提供商
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-4o-mini \
  --key YOUR_OPENAI_API_KEY

# 设置为默认提供商
ais provider-use openai
```

#### 添加 Ollama（本地 AI）
```bash
# 确保 Ollama 正在运行
ollama serve

# 添加 Ollama 提供商
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama3

# 设置为默认提供商
ais provider-use ollama
```

#### 添加自定义提供商
```bash
# 添加自定义提供商
ais provider-add custom \
  --url https://your-api-endpoint.com/v1/chat/completions \
  --model your-model \
  --key YOUR_API_KEY
```

### 2. Shell 集成（自动配置）

Shell 集成是 AIS 的核心功能，用于自动捕获命令错误：

**一键安装脚本会自动配置Shell集成，无需手动操作。**

```bash
# 检查Shell集成状态
ais test-integration

# 手动配置（如果自动配置失败）
ais setup

# 重新加载Shell配置
source ~/.bashrc  # 或 source ~/.zshrc
```

### 3. 基本配置

```bash
# 查看当前配置
ais config

# 设置上下文收集级别
ais config --set context_level=standard

# 开启自动分析（默认已开启）
ais on

# 查看可用的配置选项
ais config --help-context
```

## 🔍 故障排除

### 常见问题

#### 1. 命令未找到
```bash
# 检查 PATH 环境变量
echo $PATH

# 重新安装并检查
pip install --upgrade ais-terminal
which ais
```

#### 2. Python 版本问题
```bash
# 检查 Python 版本
python3 --version

# 使用特定 Python 版本安装
python3.9 -m pip install ais-terminal
```

#### 3. 权限问题
```bash
# 使用用户安装
pip install --user ais-terminal

# 或者使用 sudo（不推荐）
sudo pip install ais-terminal
```

#### 4. 网络问题
```bash
# 使用镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple ais-terminal

# 或者使用代理
pip install --proxy http://proxy.example.com:8080 ais-terminal
```

### 获取帮助

```bash
# 查看详细帮助
ais --help

# 查看特定命令帮助
ais ask --help

# 查看系统信息
ais test-integration

# 查看日志
ais config show | grep log
```

## 🔄 升级和卸载

### 升级 AIS
```bash
# 使用 pipx 升级
pipx upgrade ais-terminal

# 使用 pip 升级
pip install --upgrade ais-terminal

# 从源码升级
git pull origin main
pip install -e .
```

### 卸载 AIS
```bash
# 使用智能卸载脚本（推荐）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/uninstall.sh | bash

# 或手动卸载
# 使用 pipx 卸载
pipx uninstall ais-terminal

# 使用 pip 卸载
pip uninstall ais-terminal

# 清理配置文件
rm -rf ~/.config/ais
rm -rf ~/.local/share/ais
```

## 📚 下一步

安装完成后，建议按以下顺序进行：

1. [快速开始](./quick-start.md) - 5 分钟快速上手
2. [基本使用](./basic-usage.md) - 了解基本功能
3. [Shell 集成](../configuration/shell-integration.md) - 配置 Shell 集成
4. [基本配置](../configuration/basic-config.md) - 个性化配置

---

::: tip 提示
推荐使用 pipx 安装，它能提供更好的依赖隔离，避免与系统 Python 包冲突。
:::

::: info 本地 AI
如果您担心隐私问题，可以使用 Ollama 等本地 AI 服务，无需将数据发送到外部服务器。
:::

::: warning 注意
AIS 内置了免费的AI服务，安装后即可使用。如需使用自定义AI服务，请参考上面的配置说明。
:::