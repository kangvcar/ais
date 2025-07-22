# 常见问答

本文档回答了用户最常问的问题，帮助您更好地了解和使用 AIS。

## 🤔 基本问题

### AIS 是什么？
AIS (AI Shell) 是一个**上下文感知的错误分析学习助手**。它通过深度 Shell 集成自动捕获命令执行错误，使用 AI 技术分析错误原因并提供解决方案，同时帮助用户系统性地学习和提升技能。

### AIS 的核心功能有哪些？
1. **智能错误分析**：自动捕获和分析命令执行错误
2. **AI 问答助手**：快速获取技术问题的答案，支持上下文感知
3. **系统化学习**：提供结构化的技术学习内容
4. **学习成长报告**：分析学习进步和技能提升，支持 HTML 可视化报告
5. **多 AI 提供商支持**：支持 OpenAI、Claude、Ollama 等

### AIS 是否免费？
AIS 本身是开源免费的，但某些 AI 服务（如 OpenAI、Claude）需要付费。您可以：
- 使用免费的本地 AI 模型（如 Ollama）
- 使用免费额度的云端 AI 服务
- 根据需要购买 AI 服务

## 🔧 安装和配置

### 支持哪些操作系统？
- **Linux**: Ubuntu 18.04+, CentOS 7+, Debian 10+ 等
- **macOS**: macOS 10.14+
- **Windows**: 通过 WSL 支持

### 需要什么依赖？
- **Python**: 3.8 或更高版本
- **Shell**: Bash 4.0+, Zsh 5.0+
- **网络**: 用于 AI 服务（本地 AI 除外）

### 如何安装 AIS？
```bash
# 从源码安装
cd /path/to/ais
source .venv/bin/activate && python3 -m pip install -e .

# 验证安装
ais --version
```

### 首次使用需要做什么？
```bash
# 1. 配置 Shell 集成
ais setup

# 2. 添加 AI 提供商
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --key YOUR_API_KEY

# 3. 开启自动分析
ais on

# 4. 测试功能
ais ask "AIS 使用测试"
```

## 🤖 AI 服务相关

### 支持哪些 AI 服务？
- **OpenAI**: GPT-3.5, GPT-4 等
- **Anthropic**: Claude 3 系列
- **Ollama**: Llama 2, Code Llama, Mistral 等本地模型
- **自定义**: 支持兼容 OpenAI API 的服务

### 如何选择 AI 提供商？
**开发学习**：OpenAI GPT-3.5-turbo（性价比高）
**深度分析**：Claude 3 Sonnet（分析能力强）
**隐私保护**：Ollama Llama 2（本地部署）
**企业使用**：根据安全要求选择

### 本地 AI 如何设置？
```bash
# 1. 安装 Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. 启动 Ollama
ollama serve

# 3. 拉取模型
ollama pull llama2

# 4. 配置 AIS
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

# 5. 设置为默认
ais provider-use ollama
```

## 🐚 Shell 集成

### Shell 集成是如何工作的？
AIS 通过 Shell 钩子（hooks）机制监听命令执行：
- **Bash**: 使用 `trap` 和 `ERR` 信号
- **Zsh**: 使用 `preexec` 和 `precmd` 钩子

### 集成会影响性能吗？
不会。AIS 的集成机制：
- 只在命令失败时触发
- 分析在后台异步进行
- 不会阻塞正常命令执行

### 如何暂时禁用集成？
```bash
# 临时禁用
ais off

# 重新启用
ais on
```

## 💾 数据和隐私

### 数据存储在哪里？
- **配置文件**: `~/.config/ais/config.toml`
- **数据库**: `~/.local/share/ais/database.db`
- **日志**: `~/.local/share/ais/logs/`

### 我的数据安全吗？
是的，AIS 重视数据安全：
- 所有数据存储在本地
- 自动过滤敏感信息（密码、API 密钥）
- 支持本地 AI 模型（完全离线）
- 可配置的隐私级别

### 如何保护隐私？
```bash
# 1. 使用本地 AI
ais provider-use ollama

# 2. 最小化上下文收集
ais config --set ask.context_level=minimal

# 3. 查看隐私配置
ais config --help-context
```

## 🎓 学习功能

### 学习功能支持哪些主题？
AIS 目前支持以下内置学习主题：
- **git** - Git 版本控制系统
- **ssh** - SSH 远程连接和配置
- **docker** - Docker 容器化技术
- **vim** - Vim 编辑器使用技巧
- **grep** - 文本搜索和正则表达式
- **find** - 文件查找命令
- **permissions** - Linux 文件权限管理
- **process** - 进程管理和监控
- **network** - 网络诊断和配置

### 如何使用学习功能？
```bash
# 查看所有可用主题
ais learn

# 学习特定主题
ais learn git
ais learn docker
ais learn vim
```

## 📊 报告功能

### 学习报告包含什么内容？
- **错误统计**: 最常见的错误类型和命令
- **技能评估**: 基于历史数据的技能水平
- **学习建议**: 个性化的学习路径推荐
- **进步趋势**: 技能提升和学习进度
- **AI智能洞察**: 深度个性化分析总结

### 如何生成报告？
```bash
# 生成文本格式报告
ais report

# 生成 HTML 可视化报告
ais report --html

# 指定输出文件名
ais report --html -o my-report.html

# 生成后自动打开浏览器
ais report --html --open
```

## 📝 历史记录

### 如何查看命令历史？
```bash
# 查看最近的历史记录
ais history

# 限制显示数量
ais history --limit 10

# 只查看失败的命令
ais history --failed-only

# 按命令过滤
ais history --command-filter "docker"
```

## 🔧 配置管理

### 如何管理配置？
```bash
# 查看当前配置
ais config

# 设置配置项
ais config --set ask.context_level=standard

# 获取配置项
ais config --get ask.context_level

# 查看提供商列表
ais config --list-providers
```

## 🤝 多 AI 提供商支持

### 如何管理多个 AI 提供商？
```bash
# 添加提供商
ais provider-add openai --url https://api.openai.com/v1/chat/completions --model gpt-3.5-turbo --key KEY
ais provider-add claude --url https://api.anthropic.com/v1/messages --model claude-3-sonnet --key KEY

# 查看所有提供商
ais provider-list

# 切换提供商
ais provider-use openai

# 删除提供商
ais provider-remove claude
```

## 🛠️ 故障排除

### 常见错误如何解决？
参考 [常见问题](./common-issues) 文档中的详细解决方案。

### 如何测试 Shell 集成？
```bash
# 测试集成是否正常工作
ais test-integration
```

### 如何获取详细帮助？
```bash
# 查看所有命令的详细帮助
ais help-all

# 查看特定命令的详细帮助
ais ask --help-detail
ais learn --help-detail
```

## 📚 更多资源

### 文档
- [安装指南](../getting-started/installation)
- [快速开始](../getting-started/quick-start)
- [功能特性](../features/)
- [配置指南](../configuration/)

### 社区
- **GitHub**: https://github.com/kangvcar/ais
- **Issues**: 报告问题和建议
- **讨论区**: 技术交流

---

## 没有找到答案？

如果您的问题没有在这里找到答案，请：

1. 查看 [常见问题](./common-issues) 文档
2. 搜索 [GitHub Issues](https://github.com/kangvcar/ais/issues)
3. 提交新的 Issue 或问题

---

::: tip 提示
大多数功能问题都可以通过 `ais help-all` 和 `ais test-integration` 命令检测和解决。
:::

::: info 更新
FAQ 会定期更新，建议关注项目动态获取最新信息。
:::

::: warning 注意
使用前请确保已阅读和理解隐私政策和使用条款。
:::