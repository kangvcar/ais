# 首次配置

安装 AIS 后，您需要进行一些基本配置才能开始使用。本指南将帮助您完成首次配置过程。

## 配置流程概览

首次配置包括以下步骤：

1. 配置 AI 服务提供商
2. 设置 Shell 集成
3. 配置上下文收集级别
4. 启用自动错误分析
5. 验证配置

## 1. 配置 AI 服务提供商

AIS 需要连接到 AI 服务才能提供智能分析。系统默认配置了一个免费的 AI 服务提供商。

### 使用默认配置

```bash
# 查看当前配置
ais config

# 如果需要，设置默认提供商
ais config --set default_provider=default_free
```

### 添加自定义 AI 服务提供商

如果您有自己的 AI 服务（如 OpenAI、Azure OpenAI 等），可以添加：

```bash
# 添加 OpenAI 服务
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-4 \
  --key your_api_key_here

# 添加本地 Ollama 服务
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama3

# 切换到新的提供商
ais provider-use openai
```

### 查看所有可用提供商

```bash
# 列出所有配置的提供商
ais provider-list

# 查看详细的提供商信息
ais provider-list --help-detail
```

## 2. 设置 Shell 集成

Shell 集成是 AIS 的核心功能，它允许 AIS 自动捕获和分析命令错误。

### 自动设置

```bash
# 运行自动设置
ais setup
```

这将：
- 检测您的 Shell 类型（Bash 或 Zsh）
- 创建集成脚本
- 提供配置指导

### 手动设置

如果自动设置失败，您可以手动添加配置：

#### 对于 Bash 用户

在 `~/.bashrc` 中添加：

```bash
# AIS Shell 集成
if [ -f "/path/to/ais/shell/integration.sh" ]; then
    source "/path/to/ais/shell/integration.sh"
fi
```

#### 对于 Zsh 用户

在 `~/.zshrc` 中添加：

```bash
# AIS Shell 集成
if [ -f "/path/to/ais/shell/integration.sh" ]; then
    source "/path/to/ais/shell/integration.sh"
fi
```

### 重新加载配置

```bash
# 重新加载 Shell 配置
source ~/.bashrc  # 或 ~/.zshrc

# 或者重新打开终端
```

## 3. 配置上下文收集级别

AIS 支持三种上下文收集级别，您可以根据需要进行选择：

### 可用级别

- **minimal**: 只收集基本信息（命令、退出码、当前目录）
- **standard**: 收集标准信息（+ 命令历史、文件列表、Git 状态）
- **detailed**: 收集详细信息（+ 系统信息、环境变量、完整目录结构）

### 设置收集级别

```bash
# 设置为详细级别（推荐）
ais config --set context_level=detailed

# 设置为标准级别
ais config --set context_level=standard

# 设置为最小级别
ais config --set context_level=minimal

# 查看上下文配置帮助
ais config --help-context
```

## 4. 启用自动错误分析

```bash
# 启用自动错误分析
ais on

# 验证状态
ais config

# 如果需要关闭
ais off
```

## 5. 验证配置

### 测试基本功能

```bash
# 测试 AI 问答
ais ask "Hello AIS"

# 测试学习功能
ais learn git

# 查看配置状态
ais config
```

### 测试 Shell 集成

```bash
# 测试集成是否正常工作
ais test-integration

# 故意执行一个错误命令来测试自动分析
nonexistent_command
```

如果 Shell 集成配置正确，执行错误命令时应该会自动显示 AI 分析结果。

## 高级配置选项

### 敏感目录配置

您可以配置 AIS 避免收集敏感目录的信息：

```bash
# 查看当前敏感目录配置
ais config --get sensitive_dirs

# 添加敏感目录（在配置文件中手动编辑）
# 编辑 ~/.config/ais/config.toml
```

### 配置文件位置

AIS 的配置文件位于：

```bash
# 配置文件路径
~/.config/ais/config.toml

# 数据库文件路径
~/.config/ais/ais.db
```

### 示例配置文件

```toml
# ~/.config/ais/config.toml

# 默认 AI 服务提供商
default_provider = "default_free"

# 自动错误分析
auto_analysis = true

# 上下文收集级别
context_level = "detailed"

# 敏感目录列表
sensitive_dirs = [
    "~/.ssh",
    "~/.config/ais",
    "~/.aws",
    "~/.kube"
]

# AI 服务提供商配置
[providers.default_free]
base_url = "https://api.deepbricks.ai/v1/chat/completions"
model_name = "gpt-4o-mini"
api_key = "your_api_key_here"

[providers.openai]
base_url = "https://api.openai.com/v1/chat/completions"
model_name = "gpt-4"
api_key = "your_openai_api_key"
```

## 常见问题

### Shell 集成不工作

如果自动错误分析不工作：

1. 检查是否正确加载了集成脚本
2. 确认自动分析已启用：`ais config`
3. 重新加载 Shell 配置：`source ~/.bashrc`
4. 运行集成测试：`ais test-integration`

### AI 服务连接失败

如果 AI 服务连接失败：

1. 检查网络连接
2. 验证 API 密钥是否正确
3. 确认服务 URL 是否正确
4. 查看错误日志

### 配置文件权限问题

如果遇到配置文件权限问题：

```bash
# 修复配置目录权限
chmod 755 ~/.config/ais
chmod 644 ~/.config/ais/config.toml
```

## 完成配置

配置完成后，您可以：

1. 阅读[基本使用教程](./basic-usage.md)
2. 查看[功能特性详解](../features/)
3. 参考[基本使用](./basic-usage)

---

::: tip 提示
建议在配置完成后运行 `ais test-integration` 来验证所有功能是否正常工作。
:::

::: warning 注意
请妥善保管您的 API 密钥，不要在公共场所或代码仓库中暴露它们。
:::