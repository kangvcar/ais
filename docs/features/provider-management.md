# 提供商管理

AIS 支持多种 AI 服务提供商，让您可以根据需要选择最适合的 AI 模型。提供商管理功能让您轻松配置、切换和管理不同的 AI 服务。

## 🤖 支持的提供商

### OpenAI
- **模型**: GPT-3.5-turbo, GPT-4, GPT-4-turbo
- **特点**: 强大的通用能力，广泛的知识覆盖
- **适用场景**: 日常问答、代码分析、学习辅导

### Anthropic Claude
- **模型**: Claude-3-Sonnet, Claude-3-Opus, Claude-3-Haiku
- **特点**: 安全可靠，深度分析能力强
- **适用场景**: 复杂问题分析、技术深度讨论

### Ollama (本地)
- **模型**: Llama 2, Code Llama, Mistral, Qwen
- **特点**: 本地部署，隐私保护，无网络依赖
- **适用场景**: 隐私敏感环境、离线使用

### 自定义提供商
- **支持**: 兼容 OpenAI API 格式的服务
- **扩展性**: 可配置任何符合标准的 API 端点

## 🔧 提供商配置

### 添加 OpenAI 提供商
```bash
# 基本配置
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --api-key YOUR_OPENAI_API_KEY

# 高级配置
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-4 \
  --api-key YOUR_OPENAI_API_KEY \
  --max-tokens 4096 \
  --temperature 0.7
```

### 添加 Claude 提供商
```bash
# 基本配置
ais provider-add claude \
  --url https://api.anthropic.com/v1/messages \
  --model claude-3-sonnet-20240229 \
  --api-key YOUR_ANTHROPIC_API_KEY

# 指定版本
ais provider-add claude \
  --url https://api.anthropic.com/v1/messages \
  --model claude-3-opus-20240229 \
  --api-key YOUR_ANTHROPIC_API_KEY \
  --max-tokens 4096
```

### 添加 Ollama 提供商
```bash
# 基本配置
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

# 指定不同模型
ais provider-add ollama-codellama \
  --url http://localhost:11434/v1/chat/completions \
  --model codellama

# 远程 Ollama 服务
ais provider-add ollama-remote \
  --url http://remote-server:11434/v1/chat/completions \
  --model llama2
```

### 添加自定义提供商
```bash
# 自定义 API 端点
ais provider-add custom \
  --url https://your-api.example.com/v1/chat/completions \
  --model your-model \
  --api-key YOUR_API_KEY \
  --headers "Custom-Header: value"
```

## 📋 提供商管理

### 查看提供商
```bash
# 列出所有提供商
ais provider-list

# 查看当前提供商
ais provider-current

# 查看提供商详情
ais provider-show openai
```

### 切换提供商
```bash
# 切换到指定提供商
ais provider-use openai

# 临时使用提供商
ais ask "test question" --provider claude

# 为特定功能设置提供商
ais config set analyze-provider openai
ais config set learn-provider claude
```

### 测试提供商
```bash
# 测试提供商连接
ais provider-test openai

# 测试所有提供商
ais provider-test --all

# 详细测试
ais provider-test openai --verbose
```

## ⚙️ 高级配置

### 提供商优先级
```bash
# 设置提供商优先级
ais provider-priority set openai 1
ais provider-priority set claude 2
ais provider-priority set ollama 3

# 查看优先级
ais provider-priority list

# 自动故障转移
ais config set auto-failover true
```

### 负载均衡
```bash
# 启用负载均衡
ais config set load-balancing true

# 设置负载均衡策略
ais config set balance-strategy round-robin  # 轮询
ais config set balance-strategy least-load   # 最少负载
ais config set balance-strategy random       # 随机

# 设置权重
ais provider-weight set openai 0.5
ais provider-weight set claude 0.3
ais provider-weight set ollama 0.2
```

### 功能专用提供商
```bash
# 为不同功能设置专用提供商
ais config set ask-provider openai      # 问答功能
ais config set analyze-provider claude  # 错误分析
ais config set learn-provider ollama    # 学习功能
ais config set report-provider openai   # 报告生成
```

## 🔒 安全配置

### API 密钥管理
```bash
# 设置 API 密钥
ais provider-key set openai YOUR_API_KEY

# 从环境变量读取
ais provider-key set openai --env OPENAI_API_KEY

# 从文件读取
ais provider-key set openai --file /path/to/keyfile

# 加密存储
ais config set encrypt-keys true
```

### 网络安全
```bash
# 启用 SSL 验证
ais config set verify-ssl true

# 设置代理
ais config set proxy http://proxy.example.com:8080

# 设置超时
ais config set request-timeout 30

# 设置重试策略
ais config set retry-attempts 3
ais config set retry-delay 1
```

## 📊 监控和统计

### 使用统计
```bash
# 查看提供商使用统计
ais provider-stats

# 查看成本统计
ais provider-costs

# 查看性能统计
ais provider-performance
```

### 监控配置
```bash
# 启用使用监控
ais config set monitor-usage true

# 设置使用限制
ais provider-limit set openai 1000 --daily

# 设置成本限制
ais provider-limit set openai 10.00 --daily --currency USD

# 设置警告阈值
ais provider-alert set openai 80% --usage
```

## 🌐 企业配置

### 团队管理
```bash
# 创建团队配置
ais team-config create "development-team"

# 为团队设置提供商
ais team-config set "development-team" provider openai

# 应用团队配置
ais team-config apply "development-team"
```

### 策略管理
```bash
# 创建使用策略
ais policy create "corporate-policy"

# 设置策略规则
ais policy set "corporate-policy" max-tokens 2048
ais policy set "corporate-policy" allowed-providers "openai,claude"

# 应用策略
ais policy apply "corporate-policy"
```

## 🔧 故障排除

### 常见问题
```bash
# 检查提供商状态
ais provider-diagnose openai

# 检查网络连接
ais provider-ping openai

# 检查 API 密钥
ais provider-validate openai
```

### 调试模式
```bash
# 启用调试模式
ais config set debug true

# 查看详细日志
ais provider-test openai --debug

# 查看请求详情
ais ask "test" --provider openai --debug
```

### 错误处理
```bash
# 查看错误日志
ais provider-errors openai

# 清除错误记录
ais provider-errors clear

# 设置错误处理策略
ais config set error-handling retry
ais config set error-handling fallback
ais config set error-handling fail
```

## 📋 配置模板

### 开发环境配置
```bash
# 开发环境推荐配置
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --api-key $OPENAI_API_KEY \
  --temperature 0.7

ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model codellama

ais provider-use openai
ais config set auto-failover true
```

### 生产环境配置
```bash
# 生产环境推荐配置
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-4 \
  --api-key $OPENAI_API_KEY \
  --max-tokens 2048 \
  --temperature 0.3

ais provider-add claude \
  --url https://api.anthropic.com/v1/messages \
  --model claude-3-sonnet-20240229 \
  --api-key $ANTHROPIC_API_KEY

ais provider-priority set openai 1
ais provider-priority set claude 2
ais config set auto-failover true
ais config set load-balancing true
```

### 隐私保护配置
```bash
# 隐私保护推荐配置
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

ais provider-add ollama-code \
  --url http://localhost:11434/v1/chat/completions \
  --model codellama

ais provider-use ollama
ais config set data-local-only true
```

## 🔄 备份和恢复

### 配置备份
```bash
# 备份提供商配置
ais provider-backup providers.json

# 恢复提供商配置
ais provider-restore providers.json

# 导出特定提供商
ais provider-export openai openai-config.json
```

### 迁移配置
```bash
# 从旧版本迁移
ais provider-migrate --from-version 0.2.0

# 迁移到新环境
ais provider-migrate --to-env production
```

---

## 下一步

- [基本配置](../configuration/basic-config) - 配置基础设置
- [隐私设置](../configuration/privacy-settings) - 配置隐私保护
- [AI 问答](./ai-chat) - 使用 AI 问答功能

---

::: tip 提示
建议配置多个提供商作为备份，并启用自动故障转移以确保服务的连续性。
:::

::: info 成本控制
使用外部 AI 服务时，建议设置使用限制和成本警告，避免意外的高额费用。
:::

::: warning 注意
API 密钥是敏感信息，请妥善保管。建议使用环境变量或加密存储来管理密钥。
:::