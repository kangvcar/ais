# 🧠 智能环境感知问答

AIS 的智能问答功能通过深度环境感知，提供基于实际系统状态的精准技术建议。AI不仅了解你的问题，更了解你的环境。

## 🤖 核心特性 (v2.4.0+)

### 🔍 **智能上下文感知**
- **系统状态感知**：自动检测CPU、内存、网络、服务状态
- **项目环境识别**：智能识别技术栈、Git状态、项目类型  
- **三级配置系统**：minimal/standard/detailed可配置收集级别
- **环境感知回答**：基于实际配置提供针对性优化建议

### 🚀 **传统问答功能**
- **即时问答**：快速获取技术问题的答案
- **多模型支持**：支持 OpenAI、Claude、Ollama 等多种 AI 模型
- **流式输出**：实时显示 AI 处理进度
- **历史记录**：保存问答历史，便于回顾

## 🚀 基本使用

### 🖥️ **智能环境感知问答** (新特性)
```bash
# 系统状态感知问答
ais ask "我的系统配置如何？硬件性能怎么样？"
# AI会自动分析CPU、内存、磁盘等硬件信息

ais ask "我的网络连接正常吗？有什么安全建议？"  
# AI会检测网络连通性和开放端口安全性

ais ask "当前系统开放了哪些端口？这些端口安全吗？"
# AI会分析监听端口和运行服务的安全性

# 项目环境感知问答
ais ask "基于我当前的系统环境，如何优化这个Python项目？"
# AI会结合硬件配置、项目类型提供优化建议

ais ask "我在什么分支？有什么修改吗？"
# AI会自动读取Git状态并回答
```

### 📚 **传统技术问答** (仍然支持)
```bash
# 基本问答
ais ask "如何使用 Docker 创建容器？"

# 询问编程问题
ais ask "Python 中如何处理异常？"

# 询问系统问题
ais ask "如何查看 Linux 系统的内存使用情况？"
```

### ⚙️ **上下文级别配置**
```bash
# 配置ask问答的上下文收集级别
ais config --set context_level=minimal   # 基础：系统信息+网络+服务
ais config --set context_level=standard  # 标准：+项目类型+Git状态
ais config --set context_level=detailed  # 详细：+权限信息+完整环境

# 查看当前配置
ais config

# 查看ask详细帮助
ais ask --help-detail
```

## 🎯 高级功能

### 多轮对话
```bash
# 开始对话
ais ask "什么是 Kubernetes？"

# 继续对话
ais ask "如何部署应用到 Kubernetes？"

# 深入探讨
ais ask "Kubernetes 和 Docker 有什么区别？"
```

### 技术领域问答
```bash
# 前端开发
ais ask "React 中如何实现状态管理？"

# 后端开发
ais ask "如何设计 RESTful API？"

# 数据库
ais ask "MySQL 和 PostgreSQL 有什么区别？"

# 运维
ais ask "如何监控服务器性能？"
```

## 🧠 智能上下文感知系统

### 📊 **系统基础信息** (minimal级别包含)
AIS 会自动收集丰富的系统环境信息：

```bash
# 系统详情
✓ 操作系统发行版和内核版本 (uname -a)
✓ CPU核心数和详细型号
✓ 内存使用状态 (总内存/已用/可用)
✓ 磁盘使用情况和系统负载

# 网络状态  
✓ 互联网连通性检测 (ping 8.8.8.8)
✓ 监听端口列表和安全分析
✓ 运行的系统服务信息

# 项目环境
✓ 当前工作目录和用户信息
✓ Git分支和状态信息  
✓ 项目类型自动识别 (Python/Node.js/Docker等)
```

### 📈 **三级上下文收集**

| 级别 | 包含信息 | 适用场景 |
|------|----------|----------|
| **minimal** | 系统状态、网络、服务、基础Git | 性能优先，基础环境感知 |
| **standard** | +项目详情、文件列表、命令历史 | 平衡性能与功能，推荐设置 |
| **detailed** | +权限信息、详细网络、完整环境 | 完整诊断，深度分析需求 |

### 个性化回答
```bash
# 基于您的技能水平调整回答深度
ais ask "如何学习 Docker？"
# 回答会根据您的历史问题和错误分析调整复杂度

# 基于您的项目环境提供针对性建议
ais ask "如何优化这个应用？"
# 回答会考虑您的项目类型、技术栈和配置
```

## 🔧 配置选项

### 基本配置
```bash
# 查看当前配置
ais config

# 设置上下文收集级别
ais config --set context_level=standard

# 查看配置帮助
ais config --help-context
```

## 🎨 输出格式

### Rich 格式输出
```bash
# 默认使用 Rich 格式，包含：
- 彩色语法高亮
- 代码块美化
- 表格和列表格式化
- 进度条和状态提示
```

### 流式输出
AIS 问答支持流式输出，您可以实时看到 AI 回答的生成过程，提供更好的交互体验。

## 📚 使用场景

### 开发者
```bash
# 调试帮助
ais ask "这个错误是什么意思：ImportError: No module named 'requests'"

# 代码优化
ais ask "如何优化这段 Python 代码的性能？"

# 架构设计
ais ask "如何设计一个高并发的 Web 服务？"
```

### 系统管理员
```bash
# 系统诊断
ais ask "服务器 CPU 使用率过高怎么办？"

# 配置管理
ais ask "如何配置 Nginx 反向代理？"

# 安全问题
ais ask "如何加强 Linux 服务器的安全性？"
```

### 学习者
```bash
# 概念理解
ais ask "什么是微服务架构？"

# 技术选型
ais ask "Python 和 Java 哪个更适合后端开发？"

# 最佳实践
ais ask "Web 开发有哪些最佳实践？"
```

## 🔍 问答历史

### 查看历史
```bash
# 查看最近的历史记录
ais history --limit 10

# 搜索历史记录
ais history --command-filter "docker"

# 查看失败的命令
ais history --failed-only
```

## 🤝 多 AI 提供商支持

### OpenAI
```bash
# 配置 OpenAI
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --key YOUR_API_KEY

# 使用 OpenAI
ais provider-use openai
ais ask "测试 OpenAI 连接"
```

### Claude
```bash
# 配置 Claude
ais provider-add claude \
  --url https://api.anthropic.com/v1/messages \
  --model claude-3-sonnet-20240229 \
  --key YOUR_API_KEY

# 使用 Claude
ais provider-use claude
ais ask "测试 Claude 连接"
```

### Ollama（本地）
```bash
# 配置 Ollama
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

# 使用 Ollama
ais provider-use ollama
ais ask "测试本地 AI 连接"
```

## 🔒 隐私保护

### 敏感信息过滤
AIS 会自动过滤敏感信息，如 API 密钥、密码等，确保您的隐私安全。

### 本地 AI 使用
```bash
# 使用本地 AI 模型保护隐私
ais provider-use ollama
ais ask "这样就不会向外部服务发送数据"
```

## 🎓 学习集成

### 与学习系统结合
```bash
# 基于问答生成学习内容
ais ask "什么是 Docker？"
# 然后运行: ais learn docker

# 先问后学的学习模式
ais ask "Kubernetes 有哪些核心概念？"
ais learn kubernetes
```

---

## 下一步

- [学习系统](./learning-system) - 系统化学习技术知识
- [错误分析](./error-analysis) - 智能错误分析功能
- [提供商管理](./provider-management) - 管理 AI 提供商

---

::: tip 提示
AI 问答功能会随着使用变得更加智能，建议开启上下文感知以获得更好的体验。
:::

::: info 上下文感知
AIS 会自动收集环境信息来提供更准确的回答，您可以在配置中调整收集级别。
:::

::: warning 注意
使用外部 AI 服务时，请注意数据隐私。推荐使用本地 AI 模型处理敏感信息。
:::