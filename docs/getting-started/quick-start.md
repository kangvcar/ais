# 快速开始

欢迎使用 AIS！本指南将帮助您在 5 分钟内完成 AIS 的安装和基本配置，快速体验智能错误分析的强大功能。

## 🚀 5 分钟快速上手

### 第 1 步：安装 AIS
```bash
# 使用 pipx 安装（推荐）
pipx install ais-terminal

# 或使用 pip 安装
pip install ais-terminal

# 验证安装
ais --version
```

### 第 2 步：配置 Shell 集成
```bash
# 自动配置 Shell 集成
ais setup

# 重启终端或重新加载配置
source ~/.bashrc  # Bash 用户
source ~/.zshrc   # Zsh 用户
exec fish        # Fish 用户
```

### 第 3 步：配置 AI 提供商
```bash
# 选择一个 AI 提供商（三选一）

# 选项 1: OpenAI（需要 API 密钥）
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --api-key YOUR_OPENAI_API_KEY

# 选项 2: Ollama（本地免费）
# 先安装 Ollama: curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull llama2
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

# 选项 3: Claude（需要 API 密钥）
ais provider-add claude \
  --url https://api.anthropic.com/v1/messages \
  --model claude-3-sonnet-20240229 \
  --api-key YOUR_ANTHROPIC_API_KEY

# 设置默认提供商
ais provider-use openai  # 或 ollama、claude
```

### 第 4 步：启用自动分析
```bash
# 开启自动错误分析
ais on

# 验证配置
ais status
```

### 第 5 步：测试功能
```bash
# 测试 AI 问答
ais ask "如何使用 Docker 创建容器？"

# 测试错误分析（故意触发错误）
nonexistent-command
# AIS 会自动分析并提供解决方案

# 测试学习功能
ais learn git
```

## 🎯 核心功能快速体验

### 智能错误分析
```bash
# 1. 触发一个常见错误
docker run hello-world
# 如果 Docker 未安装，AIS 会自动分析并提供安装建议

# 2. 触发权限错误
sudo systemctl start nonexistent-service
# AIS 会分析服务不存在的问题并提供解决方案

# 3. 触发网络错误
curl https://nonexistent-domain.com
# AIS 会分析网络问题并提供诊断建议
```

### AI 问答助手
```bash
# 日常技术问题
ais ask "如何查看 Linux 系统的内存使用情况？"

# 编程相关问题
ais ask "Python 中如何处理异常？"

# 工具使用问题
ais ask "Git 如何回退到上一个版本？"

# 复杂问题
ais ask "如何优化 Web 应用的性能？"
```

### 系统化学习
```bash
# 学习 Docker 基础
ais learn docker

# 学习 Git 版本控制
ais learn git

# 学习 Python 编程
ais learn python

# 学习 Linux 系统管理
ais learn linux
```

### 学习报告
```bash
# 生成学习报告
ais report

# 查看错误统计
ais report --error-stats

# 查看技能评估
ais report --skill-assessment
```

## 📚 常用命令速查

### 基本操作
```bash
# 查看帮助
ais --help

# 查看版本
ais --version

# 查看状态
ais status

# 开启/关闭自动分析
ais on
ais off
```

### AI 功能
```bash
# AI 问答
ais ask "你的问题"

# 错误分析
ais analyze

# 学习功能
ais learn 主题

# 生成报告
ais report
```

### 配置管理
```bash
# 查看配置
ais config show

# 设置配置
ais config set 键 值

# 重置配置
ais config reset
```

### 提供商管理
```bash
# 列出提供商
ais provider-list

# 切换提供商
ais provider-use 提供商名称

# 测试提供商
ais provider-test 提供商名称
```

## 🔧 个性化配置

### 基本设置
```bash
# 设置语言
ais config set language zh-CN

# 设置上下文收集级别
ais config set context-level standard

# 设置输出格式
ais config set output-format rich
```

### 隐私设置
```bash
# 添加敏感信息过滤
ais config add-sensitive-pattern "*password*"
ais config add-sensitive-pattern "*token*"

# 添加排除目录
ais config add-excluded-dir ~/.ssh
ais config add-excluded-dir ~/.aws
```

### 学习偏好
```bash
# 设置学习级别
ais config set learning-level intermediate

# 设置学习格式
ais config set learning-format markdown

# 启用学习进度跟踪
ais config set track-learning-progress true
```

## 🎨 界面美化

### 启用 Rich 输出
```bash
# 启用彩色输出
ais config set output-format rich

# 启用进度条
ais config set show-progress true

# 启用表格格式
ais config set table-format fancy
```

### 流式输出
```bash
# 启用流式输出
ais config set enable-streaming true

# 设置流式输出模式
ais config set stream-mode progressive
```

## 💡 使用技巧

### 提高效率
1. **使用别名**：为常用命令创建别名
   ```bash
   alias aa='ais ask'
   alias al='ais learn'
   alias ar='ais report'
   ```

2. **配置多个提供商**：为不同用途配置不同的 AI 提供商
   ```bash
   ais config set ask-provider openai
   ais config set analyze-provider claude
   ais config set learn-provider ollama
   ```

3. **启用缓存**：加速重复查询
   ```bash
   ais config set enable-cache true
   ais config set cache-ttl 3600
   ```

### 学习建议
1. **从错误中学习**：遇到错误时，先让 AIS 分析，再学习相关主题
2. **定期查看报告**：了解自己的学习进度和技能提升
3. **主动提问**：多使用 `ais ask` 来获取技术知识

### 隐私保护
1. **使用本地 AI**：Ollama 提供完全本地化的 AI 服务
2. **配置敏感信息过滤**：自动过滤密码和密钥
3. **定期清理数据**：删除不需要的历史记录

## 🔍 故障排除

### 常见问题
```bash
# 如果命令未找到
export PATH="$PATH:$HOME/.local/bin"

# 如果 Shell 集成不工作
ais setup --force

# 如果 AI 提供商连接失败
ais provider-test 提供商名称
```

### 获取帮助
```bash
# 查看详细帮助
ais command --help

# 生成诊断报告
ais diagnose

# 查看日志
tail -f ~/.local/share/ais/ais.log
```

## 🎉 成功！

恭喜您完成了 AIS 的快速配置！现在您可以：

✅ 自动分析命令执行错误
✅ 使用 AI 问答解决技术问题
✅ 系统化学习各种技术主题
✅ 跟踪学习进度和技能提升

## 📚 下一步

根据您的需求，建议继续阅读：

- [基本使用](./basic-usage) - 详细的使用指南
- [错误分析](../features/error-analysis) - 深入了解错误分析功能
- [AI 问答](../features/ai-chat) - 掌握 AI 问答技巧
- [学习系统](../features/learning-system) - 系统化学习指南
- [配置指南](../configuration/) - 个性化配置选项

---

::: tip 提示
AIS 会随着使用变得更加智能。建议在日常工作中持续使用，让 AIS 更好地了解您的需求。
:::

::: info 本地 AI
如果您担心隐私问题，强烈推荐使用 Ollama 本地 AI 模型，既免费又保护隐私。
:::

::: warning 注意
首次使用 AI 功能时，响应可能稍慢。这是正常现象，后续使用会更加流畅。
:::