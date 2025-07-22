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
  --key YOUR_OPENAI_API_KEY

# 使用 GPT-4 模型
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-4 \
  --key YOUR_OPENAI_API_KEY
```

### 添加 Claude 提供商
```bash
# 基本配置
ais provider-add claude \
  --url https://api.anthropic.com/v1/messages \
  --model claude-3-sonnet-20240229 \
  --key YOUR_ANTHROPIC_API_KEY

# 使用其他 Claude 模型
ais provider-add claude \
  --url https://api.anthropic.com/v1/messages \
  --model claude-3-opus-20240229 \
  --key YOUR_ANTHROPIC_API_KEY
```

### 添加 Ollama 提供商
```bash
# 基本本地配置
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

# 添加不同的本地模型
ais provider-add ollama-code \
  --url http://localhost:11434/v1/chat/completions \
  --model codellama

# 连接远程 Ollama 服务
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
  --key YOUR_API_KEY
```

## 📋 提供商管理

### 查看提供商
```bash
# 列出所有提供商
ais provider-list

# 查看提供商配置
ais provider-list
```

### 切换提供商
```bash
# 切换到指定提供商
ais provider-use openai

# 切换到其他提供商
ais provider-use claude
ais provider-use ollama
```

### 删除提供商
```bash
# 删除指定提供商
ais provider-remove openai
ais provider-remove claude
```

## ⚙️ 配置管理

### 查看当前配置
```bash
# 查看完整配置
ais config

# 查看特定配置项
ais config --get default_provider

# 查看所有提供商配置
ais provider-list
```

### 配置设置
```bash
# 设置默认提供商（与 provider-use 相同）
ais config --set default_provider=openai

# 设置上下文收集级别
ais config --set ask.context_level=standard

# 设置自动分析
ais config --set advanced.auto_analysis=true
```

## 🔒 安全最佳实践

### API 密钥安全
- 使用环境变量存储 API 密钥
- 定期轮换 API 密钥
- 不要在代码中硬编码密钥

### 网络安全
- 使用 HTTPS 连接
- 在企业环境中注意防火墙配置
- 优先考虑使用本地模型（Ollama）保护数据隐私

## 📋 配置模板

### 开发环境配置
```bash
# 开发环境推荐配置
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --key $OPENAI_API_KEY

ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model codellama

ais provider-use openai
```

### 生产环境配置
```bash
# 生产环境推荐配置
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-4 \
  --key $OPENAI_API_KEY

ais provider-add claude \
  --url https://api.anthropic.com/v1/messages \
  --model claude-3-sonnet-20240229 \
  --key $ANTHROPIC_API_KEY

ais provider-use openai
```

### 隐私保护配置
```bash
# 隐私保护推荐配置（仅使用本地模型）
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

ais provider-add ollama-code \
  --url http://localhost:11434/v1/chat/completions \
  --model codellama

ais provider-use ollama
```

## 🛠️ 故障排除

### 常见问题

#### 提供商连接失败
```bash
# 检查提供商配置
ais provider-list

# 测试网络连接
ping api.openai.com

# 检查 API 密钥有效性
# (通过尝试简单问答)
ais ask "test"
```

#### Ollama 连接问题
```bash
# 检查 Ollama 服务状态
curl http://localhost:11434/api/version

# 启动 Ollama 服务
ollama serve

# 拉取模型
ollama pull llama2
```

#### 配置文件问题
```bash
# 查看配置文件位置
echo ~/.config/ais/config.toml

# 备份并重置配置
cp ~/.config/ais/config.toml ~/.config/ais/config.toml.backup
rm ~/.config/ais/config.toml
ais setup
```

### 配置验证
```bash
# 验证配置
ais config

# 测试提供商工作
ais ask "Hello, can you respond?"

# 切换提供商测试
ais provider-use claude
ais ask "Test question"
```

---

## 下一步

- [基本配置](../configuration/basic-config) - 配置基础设置
- [隐私设置](../configuration/privacy-settings) - 配置隐私保护  
- [AI 问答](./ai-chat) - 使用 AI 问答功能

---

::: tip 提示
建议配置多个提供商，这样可以根据不同场景选择最适合的模型。
:::

::: info 成本控制
使用外部 AI 服务时，请注意 API 调用成本。可以先使用免费的本地模型（Ollama）进行测试。
:::

::: warning 注意
API 密钥是敏感信息，请妥善保管。建议使用环境变量来管理密钥，避免在命令行中直接输入。
:::