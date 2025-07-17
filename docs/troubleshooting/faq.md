# 常见问答

本文档回答了用户最常问的问题，帮助您更好地了解和使用 AIS。

## 🤔 基本问题

### AIS 是什么？
AIS (AI Shell) 是一个**上下文感知的错误分析学习助手**。它通过深度 Shell 集成自动捕获命令执行错误，使用 AI 技术分析错误原因并提供解决方案，同时帮助用户系统性地学习和提升技能。

### AIS 的核心功能有哪些？
1. **智能错误分析**：自动捕获和分析命令执行错误
2. **AI 问答助手**：快速获取技术问题的答案
3. **系统化学习**：提供结构化的技术学习内容
4. **学习成长报告**：分析学习进步和技能提升
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
- **Shell**: Bash 4.0+, Zsh 5.0+, Fish 3.0+
- **网络**: 用于 AI 服务（本地 AI 除外）

### 如何安装 AIS？
```bash
# 一键安装（推荐）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

# 国内用户可使用Gitee镜像
curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/install.sh | bash

# 或手动安装
pipx install ais-terminal

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
  --api-key YOUR_API_KEY

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

### AI 响应不准确怎么办？
1. **检查上下文收集**：`ais config set context-level detailed`
2. **更换模型**：尝试更高级的模型（如 GPT-4）
3. **添加更多信息**：在问题中包含更多背景信息
4. **调整温度**：`ais config set temperature 0.3`（更保守）

## 🐚 Shell 集成

### Shell 集成是如何工作的？
AIS 通过 Shell 钩子（hooks）机制监听命令执行：
- **Bash**: 使用 `trap` 和 `ERR` 信号
- **Zsh**: 使用 `preexec` 和 `precmd` 钩子
- **Fish**: 使用事件系统

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

# 查看状态
ais status
```

### 某些命令不想被分析怎么办？
```bash
# 添加忽略的命令
ais config add-ignored-command "grep"
ais config add-ignored-command "find"

# 添加忽略的错误模式
ais config add-ignored-pattern "Permission denied"
```

## 💾 数据和隐私

### 数据存储在哪里？
- **配置文件**: `~/.config/ais/config.yaml`
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
ais config set context-level minimal

# 3. 添加敏感信息过滤
ais config add-sensitive-pattern "*password*"

# 4. 排除敏感目录
ais config add-excluded-dir ~/.ssh
```

### 可以删除历史数据吗？
```bash
# 清空所有历史
ais history clear

# 删除特定类型
ais history clear --type analyze

# 删除所有数据
ais data clear --all
```

## 🎓 学习功能

### 学习功能支持哪些主题？
- **版本控制**: Git, GitHub, SVN
- **容器化**: Docker, Kubernetes
- **编程语言**: Python, JavaScript, Go
- **系统管理**: Linux, SSH, 网络
- **开发工具**: Vim, Make, CMake

### 如何查看支持的学习主题？
```bash
# 查看所有主题
ais learn --list

# 搜索主题
ais learn --search docker

# 查看主题详情
ais learn --info docker
```

### 学习内容可以自定义吗？
```bash
# 指定学习级别
ais learn docker --level beginner

# 指定学习格式
ais learn docker --format interactive

# 指定学习深度
ais learn docker --depth basic
```

### 学习进度如何跟踪？
```bash
# 查看学习历史
ais learn-history

# 查看学习统计
ais learn-stats

# 生成学习报告
ais learn-report
```

## 📊 报告功能

### 学习报告包含什么内容？
- **错误统计**: 最常见的错误类型和命令
- **技能评估**: 基于历史数据的技能水平
- **学习建议**: 个性化的学习路径推荐
- **进步趋势**: 技能提升和学习进度

### 如何生成报告？
```bash
# 生成综合报告
ais report

# 生成特定时间段报告
ais report --days 30

# 生成特定主题报告
ais report --topic docker
```

### 报告可以导出吗？
```bash
# 导出为 HTML
ais report --export html report.html

# 导出为 PDF
ais report --export pdf report.pdf

# 导出为 Markdown
ais report --export md report.md
```

## 🔧 高级使用

### 如何配置多个 AI 提供商？
```bash
# 添加多个提供商
ais provider-add openai --api-key KEY1 --model gpt-3.5-turbo
ais provider-add claude --api-key KEY2 --model claude-3-sonnet
ais provider-add ollama --url http://localhost:11434/v1/chat/completions --model llama2

# 设置优先级
ais provider-priority set openai 1
ais provider-priority set claude 2
ais provider-priority set ollama 3

# 启用故障转移
ais config set auto-failover true
```

### 如何为不同功能使用不同的 AI？
```bash
# 为问答使用 OpenAI
ais config set ask-provider openai

# 为分析使用 Claude
ais config set analyze-provider claude

# 为学习使用本地模型
ais config set learn-provider ollama
```

### 如何在团队中使用 AIS？
```bash
# 创建团队配置
ais team-config create "dev-team"

# 设置团队默认配置
ais team-config set "dev-team" provider openai
ais team-config set "dev-team" context-level standard

# 应用团队配置
ais team-config apply "dev-team"
```

## 🚀 性能优化

### 如何提高响应速度？
1. **使用更快的模型**：GPT-3.5-turbo 比 GPT-4 快
2. **减少上下文**：`ais config set context-level minimal`
3. **启用缓存**：`ais config set enable-cache true`
4. **使用本地模型**：Ollama 响应更快
5. **优化网络**：配置代理和 DNS

### 如何减少成本？
1. **使用免费模型**：Ollama 完全免费
2. **设置使用限制**：`ais provider-limit set openai 100 --daily`
3. **只在需要时使用**：按需开启/关闭功能
4. **选择合适的模型**：根据任务选择性价比最高的模型

## 🛠️ 故障排除

### 常见错误如何解决？
参考 [常见问题](./common-issues) 文档中的详细解决方案。

### 如何获取调试信息？
```bash
# 启用调试模式
ais config set debug true

# 查看调试日志
tail -f ~/.local/share/ais/debug.log

# 生成诊断报告
ais diagnose
```

### 如何重置 AIS？
```bash
# 重置配置
ais config reset

# 重置所有数据
ais reset --all

# 重新初始化
ais setup
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

### 联系方式
- **邮件**: 项目相关问题
- **GitHub Issues**: Bug 报告和功能请求

---

## 没有找到答案？

如果您的问题没有在这里找到答案，请：

1. 查看 [常见问题](./common-issues) 文档
2. 搜索 [GitHub Issues](https://github.com/kangvcar/ais/issues)
3. 提交新的 Issue 或问题

---

::: tip 提示
大多数问题都可以通过 `ais diagnose` 命令自动检测和解决。
:::

::: info 更新
FAQ 会定期更新，建议关注项目动态获取最新信息。
:::

::: warning 注意
使用前请确保已阅读和理解隐私政策和使用条款。
:::