# 配置指南

AIS 提供了配置选项，帮助您根据需要定制工具行为。所有配置都通过 `ais config` 命令进行管理。

## 🔧 配置系统概览

### 配置文件位置
- **Linux/macOS**: `~/.config/ais/config.toml`

### 配置管理命令
```bash
# 查看所有配置
ais config

# 查看特定配置
ais config --get ask.context_level

# 设置配置
ais config --set ask.context_level=standard

# 查看提供商列表
ais config --list-providers

# 查看上下文帮助
ais config --help-context
```

## 🚀 快速配置

### 基本配置
```bash
# 设置上下文收集级别
ais config --set ask.context_level=standard

# 设置自动分析冷却时间
ais config --set advanced.analysis_cooldown=60

# 开启自动分析
ais on
```

### AI 提供商配置
```bash
# 添加 OpenAI 提供商
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --key YOUR_API_KEY

# 设置默认提供商
ais provider-use openai
```

## 📋 配置分类

### 核心配置
| 配置项 | 描述 | 链接 |
|--------|------|------|
| [基本配置](./basic-config) | 基础设置和配置选项 | ⚙️ |
| [Shell 集成](./shell-integration) | Shell 钩子配置和集成设置 | 🐚 |
| [隐私设置](./privacy-settings) | 数据收集和隐私保护 | 🔒 |

### 功能配置
- **AI 提供商管理**：在 [功能特性 > 提供商管理](../features/provider-management) 中了解详细配置
- **学习系统**：在 [功能特性 > 学习系统](../features/learning-system) 中了解学习功能
- **错误分析**：在 [功能特性 > 错误分析](../features/error-analysis) 中了解分析功能

## 🛠️ 配置文件示例

### 实际配置文件格式（TOML）
```toml
# 基本设置
[ui]
history_limit = 50

[ask]
context_level = "standard"

[advanced]
auto_analysis = true
analysis_cooldown = 60

# AI 提供商配置
[ai_providers]
default_provider = "openai"

[ai_providers.openai]
base_url = "https://api.openai.com/v1/chat/completions"
model_name = "gpt-3.5-turbo"
api_key = "sk-xxx"

[ai_providers.ollama]
base_url = "http://localhost:11434/v1/chat/completions"
model_name = "llama2"

# 敏感目录配置
[privacy]
sensitive_directories = [
    "~/.ssh",
    "~/.gnupg"
]
```

## 🔍 配置验证

### 检查配置
```bash
# 查看当前配置
ais config

# 测试 Shell 集成
ais test-integration

# 检查AI提供商
ais provider-list

# 测试AI连接
ais ask "test"
```

### 常见问题解决
```bash
# 重新初始化配置
rm ~/.config/ais/config.toml
ais setup

# 重新配置提供商
ais provider-add openai --url https://api.openai.com/v1/chat/completions --model gpt-3.5-turbo --key YOUR_KEY
```

## 🚀 配置最佳实践

### 推荐配置
```bash
# 1. 基础设置
ais config --set ask.context_level=standard
ais config --set advanced.analysis_cooldown=60

# 2. 配置AI提供商
ais provider-add openai --url https://api.openai.com/v1/chat/completions --model gpt-3.5-turbo --key $OPENAI_API_KEY
ais provider-use openai

# 3. 启用功能
ais on
ais setup
```

### 不同场景配置
```bash
# 隐私保护场景（使用本地AI）
ais provider-add ollama --url http://localhost:11434/v1/chat/completions --model llama2
ais provider-use ollama
ais config --set ask.context_level=minimal

# 开发场景（详细上下文）
ais config --set ask.context_level=detailed
ais provider-use openai

# 生产场景（标准配置）
ais config --set ask.context_level=standard
ais config --set advanced.analysis_cooldown=120
```

---

## 下一步

- [基本配置](./basic-config) - 配置基础设置
- [Shell 集成](./shell-integration) - 配置 Shell 集成
- [隐私设置](./privacy-settings) - 配置隐私保护
- [提供商管理](../features/provider-management) - 管理 AI 提供商

---

::: tip 提示
建议首次使用时运行 `ais setup` 进行基础配置，然后根据实际需要调整设置。
:::

::: info 配置格式
AIS 使用 TOML 格式的配置文件，配置修改后会立即生效，无需重启。
:::

::: warning 注意
某些 Shell 集成设置可能需要重新加载 Shell 配置才能生效：`source ~/.bashrc`
:::