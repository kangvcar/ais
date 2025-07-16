---
layout: home

hero:
  name: "AIS"
  text: "上下文感知的错误分析学习助手"
  tagline: "让每次报错都是成长，让每个错误都是学习"
  image:
    src: /logo.png
    alt: AIS
  actions:
    - theme: brand
      text: 快速开始
      link: /getting-started/installation
    - theme: alt
      text: 功能特性
      link: /features/
    - theme: alt
      text: 在 GitHub 上查看
      link: https://github.com/kangvcar/ais

features:
  - icon: 🧠
    title: 智能错误分析
    details: 基于AI的深度错误分析，自动识别问题根源，提供精准的解决方案和详细的解释，让错误处理变得高效且有学习价值。
  - icon: 🎯
    title: 上下文感知
    details: 多维度收集执行环境信息，包括系统状态、Git状态、项目类型、网络环境等，提供最贴近实际情况的分析结果。
  - icon: 🚀
    title: 深度Shell集成
    details: 无缝集成到终端环境，自动捕获命令错误并实时分析，无需手动操作，让错误分析成为工作流程的自然延伸。
  - icon: 📚
    title: 系统化学习
    details: 提供结构化的知识学习功能，涵盖Git、Docker、Linux等主题，从基础概念到高级技巧，系统性提升技能水平。
  - icon: 🔍
    title: 智能历史记录
    details: 记录和分析命令执行历史，发现相似错误模式，提供基于历史经验的个性化建议，避免重复犯错。
  - icon: ⚙️
    title: 灵活配置
    details: 支持多种AI服务提供商，可自定义上下文收集级别、敏感目录保护等，满足不同用户和环境的需求。
---

## 🎯 核心价值

AIS (AI Shell) 不仅仅是一个错误分析工具，更是一个智能学习伙伴。通过深度集成到Shell环境，AIS能够：

- **自动错误捕获**：命令执行失败时自动触发分析，无需手动操作
- **智能上下文收集**：收集系统状态、项目信息、Git状态等多维度信息
- **精准问题定位**：结合AI分析和上下文信息，快速定位问题根源
- **个性化学习建议**：基于用户技能水平和使用模式，提供针对性的学习指导
- **持续技能提升**：通过错误分析和系统学习，持续提升命令行使用技能

## 🚀 快速体验

### 安装 AIS

```bash
# 使用 pip 安装
pip install ais-terminal

# 或者使用 uv（推荐）
uv pip install ais-terminal
```

### 基本使用

```bash
# 配置 AI 服务
ais config --set default_provider=default_free

# 启用自动错误分析
ais on

# 设置 Shell 集成
ais setup

# 开始使用 - 当命令失败时自动分析
mkdir /root/test  # 如果失败会自动分析

# 主动询问问题
ais ask "什么是Docker容器？"

# 学习特定主题
ais learn git

# 查看历史记录
ais history

# 生成学习报告
ais report
```

## 💡 使用场景

### 🔧 开发过程中的错误处理

```bash
# 当 Git 操作失败时
git push origin main
# AIS 自动分析：权限问题、网络问题、或配置问题

# 当包安装失败时
npm install some-package
# AIS 自动分析：依赖冲突、网络问题、或版本兼容性

# 当构建失败时
docker build -t my-app .
# AIS 自动分析：Dockerfile语法、依赖问题、或环境配置
```

### 📚 系统化学习

```bash
# 学习 Git 版本控制
ais learn git

# 学习 Docker 容器化
ais learn docker

# 学习 Linux 权限管理
ais learn permissions

# 学习 SSH 远程连接
ais learn ssh
```

### 🎯 个性化问答

```bash
# 快速解答具体问题
ais ask "如何解决端口被占用的问题？"

# 寻求最佳实践建议
ais ask "Docker容器部署的最佳实践是什么？"

# 了解工具使用技巧
ais ask "如何使用grep进行高级文本搜索？"
```

## 🌟 核心优势

### 🎯 智能化

- **AI驱动分析**：基于大语言模型的智能错误分析
- **上下文感知**：收集多维度环境信息进行精准诊断
- **学习模式识别**：分析用户技能水平和使用模式

### 🚀 自动化

- **无缝集成**：深度集成到Shell环境，无需手动触发
- **自动捕获**：命令失败时自动启动分析流程
- **持续学习**：基于使用历史持续优化建议质量

### 📈 成长导向

- **错误变学习**：每次错误都是学习和成长的机会
- **系统化知识**：提供结构化的学习路径和知识体系
- **个性化指导**：根据用户水平提供适合的学习建议

### 🔒 安全可靠

- **隐私保护**：本地数据存储，保护用户隐私
- **敏感信息过滤**：自动过滤敏感目录和信息
- **安全建议**：提供安全级别评估和风险提示

## 📊 功能特性

| 功能 | 描述 | 使用场景 |
|------|------|----------|
| 自动错误分析 | 命令失败时自动触发AI分析 | 日常开发和运维工作 |
| 上下文感知 | 收集系统、项目、Git等上下文信息 | 复杂环境问题诊断 |
| 智能问答 | 基于AI的即时问答服务 | 快速获取技术答案 |
| 系统学习 | 结构化的技术知识学习 | 技能提升和知识积累 |
| 历史记录 | 智能的命令历史记录和分析 | 经验积累和模式识别 |
| 多AI支持 | 支持多种AI服务提供商 | 灵活的服务配置 |
| Shell集成 | 深度集成到终端环境 | 无缝的工作流程 |

## 🛠️ 技术架构

AIS 采用模块化设计，主要组件包括：

- **CLI 接口**：用户交互的命令行界面
- **AI 集成**：支持多种AI服务提供商的统一接口
- **上下文收集**：多维度环境信息收集系统
- **智能分析**：基于AI和上下文的智能分析引擎
- **数据存储**：本地SQLite数据库存储历史记录
- **Shell 集成**：深度集成到Bash/Zsh等Shell环境

## 📈 发展路线图

### 近期计划

- [ ] 支持更多AI服务提供商
- [ ] 增强上下文收集能力
- [ ] 优化分析结果的准确性
- [ ] 添加更多学习主题

### 长期规划

- [ ] 支持团队协作功能
- [ ] 开发Web界面
- [ ] 增加插件系统
- [ ] 支持多语言界面

## 🤝 社区参与

AIS 是一个开源项目，我们欢迎所有形式的贡献：

- 🐛 报告Bug和问题
- 💡 提出功能建议
- 📖 改进文档
- 🔧 贡献代码
- 🌟 给项目加星

## 📞 获取帮助

如果您在使用过程中遇到问题，可以通过以下方式获取帮助：

- 📖 查看[用户指南](/guide/)
- 🔧 参考[故障排除](/guide/troubleshooting)
- 💬 在[GitHub Issues](https://github.com/kangvcar/ais/issues)中提问
- 📧 发送邮件至项目维护者

---

<div style="text-align: center; margin-top: 2rem; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
  <h3>🚀 现在就开始您的智能终端之旅</h3>
  <p>让 AIS 成为您的命令行学习伙伴，将每次错误转化为成长的机会</p>
  <a href="/getting-started/installation" style="display: inline-block; padding: 12px 24px; background: white; color: #667eea; text-decoration: none; border-radius: 6px; font-weight: bold; margin-top: 1rem;">立即开始</a>
</div>