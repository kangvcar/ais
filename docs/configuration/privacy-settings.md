# 隐私设置

AIS 非常重视用户隐私，提供了隐私保护机制。所有数据都存储在本地，您可以控制数据的收集和使用。

## 🔒 隐私原则

### 数据本地化
- 所有数据存储在本地 SQLite 数据库
- 不向外部服务器发送敏感信息
- 用户完全控制数据的收集和删除

### 敏感信息过滤
- 自动过滤密码、API 密钥等敏感信息
- 在发送给 AI 之前进行数据清洗

## 🔍 上下文收集控制

### 收集级别配置
```bash
# 最小收集（推荐隐私敏感用户）
ais config --set ask.context_level=minimal

# 标准收集（默认）
ais config --set ask.context_level=standard

# 详细收集（开发调试用）
ais config --set ask.context_level=detailed

# 查看当前设置
ais config --get ask.context_level

# 查看上下文帮助
ais config --help-context
```

### 收集级别详情

#### minimal（最小）
- 基本系统信息（OS、CPU、内存）
- 命令和退出码
- 基础网络连通性检测
- 监听端口和服务信息
- 基本Git状态

#### standard（标准）
- minimal级别的所有信息
- 项目类型检测和文件列表
- 命令历史记录
- 更详细的环境信息

#### detailed（详细）
- standard级别的所有信息
- 完整的环境变量
- 详细的权限信息
- 网络诊断信息

## 🌐 网络隐私

### 使用本地 AI 模型（推荐）
```bash
# 安装和配置 Ollama
ollama serve
ollama pull llama2

# 添加本地 AI 提供商
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

# 设置为默认提供商
ais provider-use ollama

# 验证本地模型工作
ais ask "这是本地AI测试"
```

### 避免使用外部 AI 服务
如果必须使用外部 AI 服务，请注意：
- 使用最小化的上下文收集级别
- 定期检查发送给 AI 的数据内容
- 使用可信的 AI 提供商

## 📊 数据管理

### 数据存储位置
```bash
# 配置文件位置
~/.config/ais/config.toml

# 数据库文件位置
~/.local/share/ais/database.db

# 日志文件位置
~/.local/share/ais/logs/
```

### 查看和清理数据
```bash
# 查看历史记录
ais history

# 查看配置
ais config

# 清理历史记录（如需要）
# 注意：没有内置的清理命令，需要手动删除数据库文件
rm ~/.local/share/ais/database.db
```

## 🚫 控制功能

### 自动分析控制
```bash
# 禁用自动分析
ais off

# 启用自动分析
ais on

# 调整分析冷却时间
ais config --set advanced.analysis_cooldown=120
```

### 敏感目录保护
AIS 内置了敏感目录保护机制，会自动避免收集某些敏感目录的信息。

## 📋 隐私配置推荐

### 高隐私模式
```bash
# 适合隐私敏感用户的配置
ais config --set ask.context_level=minimal

# 使用本地 AI 模型
ais provider-add ollama --url http://localhost:11434/v1/chat/completions --model llama2
ais provider-use ollama

# 禁用自动分析（如需要）
ais off
```

### 开发者模式
```bash
# 适合开发者的配置（平衡隐私和功能）
ais config --set ask.context_level=standard

# 配置可信的外部 AI 提供商
ais provider-add openai --url https://api.openai.com/v1/chat/completions --model gpt-3.5-turbo --key YOUR_KEY
```

## 🔒 隐私最佳实践

### 定期检查
- 定期查看 `ais config` 了解当前设置
- 检查 `ais provider-list` 确认使用的 AI 提供商
- 查看 `ais history` 了解记录的数据

### 安全建议
- 优先使用本地 AI 模型（Ollama）
- 使用最小必要的上下文收集级别
- 定期清理不需要的历史数据
- 注意 API 密钥的安全存储

## 🛠️ 数据位置和管理

### 完全重置
如果需要完全清理所有数据：
```bash
# 删除所有配置和数据
rm -rf ~/.config/ais/
rm -rf ~/.local/share/ais/

# 重新初始化
ais setup
```

### 备份重要配置
```bash
# 备份配置文件
cp ~/.config/ais/config.toml ~/ais-config-backup.toml

# 备份数据库
cp ~/.local/share/ais/database.db ~/ais-data-backup.db
```

---

## 下一步

- [提供商管理](../features/provider-management) - 配置本地 AI 提供商
- [故障排除](../troubleshooting/common-issues) - 解决隐私相关问题
- [基本配置](./basic-config) - 了解其他配置选项

---

::: tip 提示
推荐使用本地 AI 模型（如 Ollama）来最大化隐私保护，避免向外部服务发送数据。
:::

::: info 透明度
AIS 的所有数据收集和处理都是透明的，您可以通过 `ais config` 和 `ais history` 查看相关信息。
:::

::: warning 注意
修改隐私设置后，建议测试功能是否正常工作，特别是 AI 问答功能。
:::