# 配置指南

AIS 提供了丰富的配置选项，帮助您根据需要定制工具行为。所有配置都通过 `ais config` 命令进行管理。

## 🔧 配置系统概览

### 配置文件位置
- **Linux**: `~/.config/ais/config.yaml`
- **macOS**: `~/Library/Application Support/ais/config.yaml`

### 配置管理命令
```bash
# 查看所有配置
ais config show

# 查看特定配置
ais config show auto-analysis

# 设置配置
ais config set context-level standard

# 重置配置
ais config reset
```

## 🚀 快速配置

### 基本配置
```bash
# 设置语言
ais config set language zh-CN

# 设置上下文收集级别
ais config set context-level standard

# 开启自动分析
ais on
```

### AI 提供商配置
```bash
# 添加 OpenAI 提供商
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --api-key YOUR_API_KEY

# 设置默认提供商
ais provider-use openai
```

## 📋 配置分类

### 核心配置
| 配置项 | 描述 | 链接 |
|--------|------|------|
| [基本配置](./basic-config) | 语言、主题、输出格式等基础设置 | ⚙️ |
| [Shell 集成](./shell-integration) | Shell 钩子配置和集成设置 | 🐚 |
| [隐私设置](./privacy-settings) | 数据收集和敏感信息过滤 | 🔒 |

### 高级配置
- **AI 提供商管理**：在 [功能特性 > 提供商管理](../features/provider-management) 中了解详细配置
- **学习系统配置**：在 [功能特性 > 学习系统](../features/learning-system) 中了解学习相关配置
- **错误分析配置**：在 [功能特性 > 错误分析](../features/error-analysis) 中了解分析相关配置

## 🛠️ 配置文件示例

### 完整配置文件
```yaml
# 基本设置
language: zh-CN
theme: auto
output_format: rich

# 自动分析
auto_analysis:
  enabled: true
  context_level: standard
  
# 隐私设置
privacy:
  excluded_dirs:
    - /home/user/secrets
    - ~/.ssh
  excluded_patterns:
    - "*.key"
    - "*.pem"
    - "*password*"
    
# AI 提供商
providers:
  openai:
    url: https://api.openai.com/v1/chat/completions
    model: gpt-3.5-turbo
    api_key: sk-xxx
  default: openai
  
# 学习系统
learning:
  difficulty_level: intermediate
  preferred_format: markdown
  
# Shell 集成
shell:
  integration_enabled: true
  hooks:
    - bash
    - zsh
```

## 🔍 配置验证

### 检查配置
```bash
# 验证配置文件
ais config validate

# 测试 AI 提供商连接
ais provider-test

# 测试 Shell 集成
ais test-integration
```

### 故障排除
```bash
# 重置所有配置
ais config reset

# 修复配置文件
ais config repair

# 备份配置
ais config backup
```

## 🚀 配置最佳实践

### 推荐配置
```bash
# 1. 基础配置
ais config set language zh-CN
ais config set context-level standard
ais config set output-format rich

# 2. 隐私配置
ais config add-excluded-dir ~/.ssh
ais config add-excluded-pattern "*.key"

# 3. 启用功能
ais on
ais setup
```

### 环境特定配置
```bash
# 开发环境
ais config set context-level detailed
ais config set auto-analysis true

# 生产环境
ais config set context-level minimal
ais config set auto-analysis false
```

---

## 下一步

- [基本配置](./basic-config) - 配置基础设置
- [Shell 集成](./shell-integration) - 配置 Shell 集成
- [隐私设置](./privacy-settings) - 配置隐私保护
- [提供商管理](../features/provider-management) - 管理 AI 提供商

---

::: tip 提示
建议首次使用时按照推荐配置进行设置，然后根据实际需要调整。
:::

::: info 配置同步
AIS 配置文件是纯文本格式，可以通过版本控制系统进行管理和同步。
:::

::: warning 注意
修改配置后，某些设置可能需要重启终端或重新加载 Shell 配置才能生效。
:::