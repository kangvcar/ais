# 基本配置

AIS 的基本配置通过 TOML 格式的配置文件进行管理，支持多种自定义选项以满足不同用户的需求。

## 📍 配置文件位置

### 配置文件路径
```bash
# 配置文件位置
~/.config/ais/config.toml

# 数据库位置
~/.local/share/ais/history.db

# 查看当前配置
ais config
```

### 配置文件结构
```toml
# 默认配置文件内容
default_provider = "default_free"
auto_analysis = true
context_level = "detailed"
sensitive_dirs = ["~/.ssh", "~/.config/ais", "~/.aws"]

[providers.default_free]
base_url = "https://api.deepbricks.ai/v1/chat/completions"
model_name = "gpt-4o-mini"
api_key = "sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg"

[ui]
enable_colors = true
max_history_display = 10

[advanced]
max_context_length = 4000
async_analysis = true
cache_analysis = true
```

## 🔄 自动分析设置

### 全局开关
```bash
# 开启自动分析
ais on

# 关闭自动分析
ais off

# 查看当前状态
ais config
```

### 配置自动分析
```bash
# 设置自动分析开关
ais config --set auto_analysis=true

# 查看配置状态
ais config --get auto_analysis
```


## 🧠 上下文收集

### 收集级别
```bash
# 最小收集
ais config --set context_level=minimal

# 标准收集（推荐）
ais config --set context_level=standard

# 详细收集（默认）
ais config --set context_level=detailed

# 查看配置帮助
ais config --help-context
```

### 收集级别说明

#### minimal（最小）
- 基本信息（命令、退出码、目录）
- 性能最好，隐私性最强

#### standard（标准）
- 基本信息 + 命令历史、文件列表、Git状态
- 平衡性能和分析精度

#### detailed（详细）
- 标准信息 + 系统信息、环境变量、完整目录
- 分析最精准，但会收集更多信息

## 🔧 AI 提供商管理

### 查看提供商
```bash
# 列出所有提供商
ais provider-list

# 查看详细帮助
ais provider-list --help-detail
```

### 添加提供商
```bash
# 添加 OpenAI 提供商
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-4o-mini \
  --key YOUR_API_KEY

# 添加本地 Ollama 提供商
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama3

# 查看添加帮助
ais provider-add --help-detail
```

### 切换提供商
```bash
# 切换到指定提供商
ais provider-use openai

# 切换到本地提供商
ais provider-use ollama

# 切换回默认免费服务
ais provider-use default_free
```

## 💾 数据存储

### 存储位置
```bash
# 配置文件：~/.config/ais/config.toml
# 数据库：~/.local/share/ais/history.db
# 缓存：~/.cache/ais/

# 查看历史记录
ais history

# 查看特定记录详情
ais history 1
```

### 历史记录管理
```bash
# 查看最近10条记录
ais history

# 查看最近20条记录
ais history -n 20

# 只查看失败的命令
ais history --failed-only

# 按命令过滤
ais history --command-filter git
```

## 🛡️ 隐私和安全

### 敏感数据保护
```bash
# 查看敏感目录配置
ais config

# 敏感目录已默认配置：
# - ~/.ssh （SSH密钥）
# - ~/.config/ais （AIS配置）
# - ~/.aws （AWS凭证）
```

### 本地化选项
```bash
# 使用本地AI模型（完全离线）
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama3

ais provider-use ollama

# 所有数据本地存储
# 配置文件：~/.config/ais/
# 数据库：~/.local/share/ais/
```

## 🔧 高级设置

### 系统集成测试
```bash
# 测试系统集成
ais test-integration

# 手动设置Shell集成
ais setup

# 查看完整帮助
ais help-all
```

### 学习和分析功能
```bash
# 生成学习报告
ais report

# 学习特定主题
ais learn git
ais learn docker
ais learn vim

# 查看学习帮助
ais learn --help-detail
```

## 📋 配置模板

### 开发者配置
```bash
# 适合开发者的配置
ais config --set context_level=detailed
ais config --set auto_analysis=true
ais provider-add openai --url ... --model gpt-4o-mini --key YOUR_KEY
```

### 隐私保护配置
```bash
# 适合隐私敏感用户的配置
ais config --set context_level=minimal
ais provider-add ollama --url http://localhost:11434/v1/chat/completions --model llama3
ais provider-use ollama
```

### 学习者配置
```bash
# 适合学习者的配置
ais config --set context_level=standard
ais config --set auto_analysis=true
# 使用默认免费服务即可
```

## 🔍 配置验证

### 验证配置
```bash
# 查看当前配置
ais config

# 测试系统集成
ais test-integration

# 查看提供商状态
ais provider-list
```

### 实际使用测试
```bash
# 测试AI问答
ais ask "什么是AIS？"

# 测试错误分析（故意触发错误）
nonexistent-command

# 测试学习功能
ais learn git

# 测试历史记录
ais history
```

---

## 下一步

- [Shell 集成](./shell-integration) - 配置 Shell 集成
- [隐私设置](./privacy-settings) - 配置隐私保护
- [提供商管理](../features/provider-management) - 管理 AI 提供商
- [故障排除](../troubleshooting/common-issues) - 解决常见问题

---

::: tip 提示
建议定期备份配置文件，特别是在进行大量定制化配置后。
:::

::: info 配置优先级
命令行参数 > 环境变量 > 配置文件 > 默认值
:::

::: warning 注意
某些配置修改后需要重启 AIS 或重新加载 Shell 配置才能生效。
:::