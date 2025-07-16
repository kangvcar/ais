# 安装指南

AIS 支持多种安装方式，推荐使用 `pipx` 进行安装以获得最佳的依赖隔离效果。

## 📦 安装方式

### 方式 1: 使用 pipx 安装（推荐）

```bash
# 安装 pipx（如果尚未安装）
pip install pipx

# 使用 pipx 安装 AIS
pipx install ais-terminal

# 验证安装
ais --version
```

### 方式 2: 使用 pip 安装

```bash
# 全局安装
pip install ais-terminal

# 用户安装
pip install --user ais-terminal
```

### 方式 3: 从源码安装

```bash
# 克隆仓库
git clone https://github.com/kangvcar/ais.git
cd ais

# 安装依赖
pip install -e .

# 验证安装
ais --version
```

### 方式 4: 使用 Docker

```bash
# 拉取镜像
docker pull kangvcar/ais:latest

# 运行容器
docker run -it kangvcar/ais:latest
```

## 🔧 系统要求

### 支持的操作系统
- **Linux**: Ubuntu 18.04+, CentOS 7+, Debian 10+
- **macOS**: macOS 10.14+
- **Windows**: Windows 10+ (通过 WSL)

### 依赖要求
- **Python**: 3.8 或更高版本
- **Shell**: Bash 4.0+, Zsh 5.0+, Fish 3.0+

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
```

## ⚙️ 初始配置

### 1. 配置 AI 服务提供商

AIS 需要 AI 服务才能正常工作，支持多种提供商：

#### OpenAI
```bash
# 添加 OpenAI 提供商
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --api-key YOUR_OPENAI_API_KEY

# 设置为默认提供商
ais provider-use openai
```

#### Ollama（本地 AI）
```bash
# 确保 Ollama 正在运行
ollama serve

# 添加 Ollama 提供商
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

# 设置为默认提供商
ais provider-use ollama
```

#### 自定义提供商
```bash
# 添加自定义提供商
ais provider-add custom \
  --url https://your-api-endpoint.com/v1/chat/completions \
  --model your-model \
  --api-key YOUR_API_KEY
```

### 2. 配置 Shell 集成

Shell 集成是 AIS 的核心功能，用于自动捕获命令错误：

```bash
# 自动配置 Shell 集成
ais setup

# 手动配置（如果自动配置失败）
echo 'eval "$(ais shell-integration bash)"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 基本配置

```bash
# 查看当前配置
ais config show

# 设置上下文收集级别
ais config set context-level standard

# 开启自动分析
ais on

# 设置语言
ais config set language zh-CN
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
ais test-integration --verbose

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
# 使用 pipx 卸载
pipx uninstall ais-terminal

# 使用 pip 卸载
pip uninstall ais-terminal

# 清理配置文件（可选）
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
首次使用前，请确保配置至少一个 AI 服务提供商，否则 AIS 无法正常工作。
:::