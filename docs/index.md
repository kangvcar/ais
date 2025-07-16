---
layout: home

hero:
  name: "AIS"
  text: "AI Shell 智能终端助手"
  tagline: "让每次报错都是成长，让每个错误都是学习"
  image:
    src: /logo.png
    alt: AIS Logo
  actions:
    - theme: brand
      text: 立即体验
      link: /getting-started/quick-start
    - theme: alt
      text: 了解更多
      link: /features/

features:
  - icon: 🧠
    title: 智能错误分析
    details: 命令失败时自动触发AI分析，快速定位问题根源并提供解决方案
  - icon: 🎯
    title: 上下文感知
    details: 收集系统状态、项目信息等多维度环境信息，提供精准诊断
  - icon: 📚
    title: 系统化学习
    details: 将每次错误转化为学习机会，提供结构化的技术知识学习
  - icon: 🤖
    title: 自动错误分析
    details: 命令执行失败时自动触发AI分析，无需手动操作
  - icon: 💬
    title: 智能问答
    details: 随时询问技术问题，获得个性化的专业解答
  - icon: 📖
    title: 系统学习
    details: 结构化学习Docker、Git、Linux等技术知识
  - icon: 📊
    title: 学习报告
    details: 跟踪技能提升进度，获得个性化学习建议
  - icon: ⚡
    title: 零学习成本
    details: 一键安装，自动配置，无需复杂设置
  - icon: 🔒
    title: 隐私保护
    details: 本地数据存储，支持本地AI模型
---

## ⚡ 一键安装

快速开始使用 AIS，支持多种安装方式：

### 推荐安装方式
```bash
# 使用 pipx 安装（推荐）
pipx install ais-terminal

# 或使用 pip 安装
pip install ais-terminal
```

### 快速配置
```bash
# 配置 AI 服务提供商
ais provider-add openai --url https://api.openai.com/v1/chat/completions --model gpt-3.5-turbo --api-key YOUR_API_KEY

# 配置 Shell 集成
ais setup

# 开始使用
ais on
```

## 💻 使用演示

```bash
$ docker run hello-world
docker: Error response from daemon: Unable to find image

🤖 AIS 正在分析错误...
📋 问题诊断: Docker镜像未找到
💡 解决方案:
  1. 拉取镜像: docker pull hello-world
  2. 检查网络连接
  3. 验证Docker服务状态

🎯 学习建议: 运行 'ais learn docker' 了解容器基础
```

## 🚀 立即开始

- [快速开始](./getting-started/quick-start.md) - 5分钟快速上手
- [功能特性](./features/) - 了解 AIS 的强大功能
- [配置指南](./configuration/) - 个性化配置设置

---

::: tip 简单易用
一键安装，自动配置，无需复杂设置即可开始使用。
:::

::: info 隐私保护
本地数据存储，支持本地AI模型，保护您的隐私安全。
:::

::: warning 系统要求
需要 Python 3.8+ 和兼容的 Shell 环境（Bash/Zsh/Fish）。
:::