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
    details: 命令失败时自动触发AI分析，收集系统状态、项目信息等多维度环境信息，提供精准的问题诊断和解决方案
  - icon: 🎯
    title: 上下文感知诊断
    details: 智能检测网络、权限、文件系统、Git状态等环境信息，基于当前工作目录和项目类型提供个性化建议
  - icon: 📚
    title: 系统化学习路径
    details: 基于错误历史生成个性化学习建议，提供结构化的技术知识学习路径，将每次错误转化为成长机会
  - icon: 🤖
    title: 自动错误分析
    details: Shell集成自动捕获命令执行错误，无需手动操作，智能过滤内部命令和特殊情况，专注于真正的问题分析
  - icon: 💬
    title: 智能问答系统
    details: 支持实时流式输出的AI问答，可询问任何编程、运维、工具使用相关问题，获得专业的中文回答和实用建议
  - icon: 📖
    title: 多领域学习模块
    details: 覆盖基础命令、文件操作、系统管理、Git版本控制、Docker容器、包管理等多个技能领域的系统化学习
  - icon: 📊
    title: 个性化学习报告
    details: 分析最近30天的错误历史，生成详细的技能评估、改进洞察和学习建议，跟踪技能提升进度
  - icon: ⚡
    title: 零学习成本
    details: 一键安装脚本自动检测环境，支持用户级、系统级、容器化多种安装方式，自动配置Shell集成
  - icon: 🔒
    title: 隐私保护
    details: 本地SQLite数据库存储，敏感数据过滤，支持本地AI模型（Ollama），可完全离线使用
---

## ⚡ 一键安装

```bash
# 推荐：一键安装脚本（自动检测环境）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

# 或手动安装
pipx install ais-terminal
```

安装脚本会自动：
- 检测运行环境（用户/系统/容器）
- 选择最佳安装方式（pipx/pip）
- 配置Shell集成（Bash/Zsh/Fish）
- 设置PATH环境变量
- 验证安装成功

## 🔍 智能错误分析演示

当命令执行失败时，AIS会自动分析并提供解决方案：

```bash
$ docker run hello-world
docker: Error response from daemon: Unable to find image 'hello-world:latest' locally

🔍 发现相似的历史错误
  1. docker pull ubuntu (12-15 14:30) - 已解决
  2. docker run nginx (12-15 14:25) - 已分析

🤖 AI 错误分析
🔍 问题诊断:
您遇到了Docker镜像未找到的问题。Docker尝试运行hello-world镜像，但本地没有该镜像。

📚 知识扩展:
Docker采用分层存储机制，镜像需要先下载到本地才能运行。

🎯 解决思路:
1. 先手动拉取镜像到本地
2. 检查网络连接和Docker服务状态

💡 AI 基于你的使用习惯和当前环境推荐

#  命令                          风险  说明
1  docker pull hello-world       🟢   拉取hello-world镜像到本地
2  docker images                 🟢   查看已下载的镜像列表
3  systemctl status docker       🟢   检查Docker服务状态

Select an action (1-3/e/q/x): █
```

## 💬 智能问答演示

使用 `ais ask` 获得即时专业答案：

```bash
$ ais ask "什么是Docker容器？"

🤖 正在思考您的问题...

## Docker容器是什么？

Docker容器是一种轻量级的、可移植的、自包含的软件运行环境。

### 🏗️ 核心概念
- **隔离性**: 每个容器都有独立的文件系统、进程空间和网络接口
- **轻量级**: 比传统虚拟机更少的资源消耗
- **可移植性**: 一次构建，到处运行

### 🔧 主要特点
1. **快速启动**: 秒级启动时间
2. **资源高效**: 共享主机内核，无需完整操作系统
3. **版本控制**: 镜像分层存储，支持版本管理

想了解更多？试试 `ais learn docker` 获得系统化学习路径！
```

## 📊 学习报告演示

运行 `ais report` 获得个性化学习分析：

```bash
$ ais report

# 📊 AIS 学习成长报告

**分析周期**: 最近30天 | **生成时间**: 2024-01-15 10:30:45

## 🔍 错误概览
- **总错误数**: 23 次
- **最常出错的命令**: git (8次), docker (5次), npm (4次)
- **最常见的错误类型**: Git操作错误, Docker操作错误, 权限不足

## 💪 技能评估
- **当前水平**: 中级用户
- **优势领域**: 基础命令, 文件操作
- **需要改进**: Git版本控制, Docker容器

## 💡 改进洞察
🔥 git 命令需要重点关注
你在 git 命令上出现了 8 次错误，占总错误的 34.8%

## 🎯 学习建议
1. 🔥 深入学习 git 命令
   类型: 命令掌握 | 优先级: 高
   学习路径:
   - 学习Git基础概念（工作区、暂存区、仓库）
   - 掌握常用Git命令（add, commit, push, pull）
   - 了解分支操作和合并冲突解决

💡 提示: 使用 `ais learn <主题>` 深入学习特定主题
📚 帮助: 使用 `ais ask <问题>` 获取即时答案
```


## 🌟 用户评价

<div class="testimonials">
  <div class="testimonial-card">
    <div class="testimonial-content">
      <div class="quote-icon">💬</div>
      <p class="testimonial-text">
        "AIS 完全改变了我的命令行体验。以前遇到错误只能盲目搜索，现在每次错误都能得到针对性的解决方案和学习建议。"
      </p>
      <div class="testimonial-author">
        <div class="author-avatar">👨‍💻</div>
        <div class="author-info">
          <div class="author-name">张开发者</div>
          <div class="author-role">后端工程师</div>
        </div>
      </div>
    </div>
  </div>

  <div class="testimonial-card">
    <div class="testimonial-content">
      <div class="quote-icon">💬</div>
      <p class="testimonial-text">
        "作为运维工程师，AIS 帮我快速诊断各种系统问题。特别是上下文感知功能，能根据当前项目和环境给出最合适的建议。"
      </p>
      <div class="testimonial-author">
        <div class="author-avatar">👨‍🔧</div>
        <div class="author-info">
          <div class="author-name">李运维</div>
          <div class="author-role">DevOps工程师</div>
        </div>
      </div>
    </div>
  </div>

  <div class="testimonial-card">
    <div class="testimonial-content">
      <div class="quote-icon">💬</div>
      <p class="testimonial-text">
        "学习报告功能让我清楚地看到自己在哪些方面需要提升。30天的数据分析很有价值，学习路径也很实用。"
      </p>
      <div class="testimonial-author">
        <div class="author-avatar">👨‍🎓</div>
        <div class="author-info">
          <div class="author-name">王同学</div>
          <div class="author-role">计算机专业</div>
        </div>
      </div>
    </div>
  </div>

  <div class="testimonial-card">
    <div class="testimonial-content">
      <div class="quote-icon">💬</div>
      <p class="testimonial-text">
        "隐私保护做得很好，本地存储让我放心使用。支持Ollama本地模型，完全不用担心数据泄露。"
      </p>
      <div class="testimonial-author">
        <div class="author-avatar">👨‍💼</div>
        <div class="author-info">
          <div class="author-name">陈架构师</div>
          <div class="author-role">技术总监</div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
.testimonials {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin: 3rem 0;
}

.testimonial-card {
  background: var(--vp-c-bg-soft);
  border-radius: 16px;
  padding: 0;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid var(--vp-c-divider);
  position: relative;
}

.testimonial-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.testimonial-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--vp-c-brand), var(--vp-c-brand-light));
}

.testimonial-content {
  padding: 2rem;
}

.quote-icon {
  font-size: 2rem;
  color: var(--vp-c-brand);
  margin-bottom: 1rem;
}

.testimonial-text {
  color: var(--vp-c-text-1);
  line-height: 1.6;
  margin-bottom: 1.5rem;
  font-size: 1rem;
  font-style: italic;
  position: relative;
}

.testimonial-text::before {
  content: '"';
  position: absolute;
  left: -0.5rem;
  top: -0.2rem;
  font-size: 1.5rem;
  color: var(--vp-c-brand);
  font-weight: bold;
}

.testimonial-text::after {
  content: '"';
  position: absolute;
  right: -0.3rem;
  bottom: -0.2rem;
  font-size: 1.5rem;
  color: var(--vp-c-brand);
  font-weight: bold;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--vp-c-divider);
}

.author-avatar {
  font-size: 2.5rem;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--vp-c-brand-soft);
  border-radius: 50%;
  flex-shrink: 0;
}

.author-info {
  flex: 1;
}

.author-name {
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: 0.2rem;
}

.author-role {
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
}

/* 深色模式优化 */
.dark .testimonial-card {
  background: var(--vp-c-bg-alt);
  border-color: var(--vp-c-divider);
}

.dark .testimonial-card:hover {
  box-shadow: 0 8px 32px rgba(255, 255, 255, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .testimonials {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .testimonial-content {
    padding: 1.5rem;
  }
  
  .testimonial-text {
    font-size: 0.95rem;
  }
  
  .author-avatar {
    font-size: 2rem;
    width: 2.5rem;
    height: 2.5rem;
  }
}

/* 添加动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.testimonial-card {
  animation: fadeInUp 0.6s ease-out;
}

.testimonial-card:nth-child(1) {
  animation-delay: 0.1s;
}

.testimonial-card:nth-child(2) {
  animation-delay: 0.2s;
}

.testimonial-card:nth-child(3) {
  animation-delay: 0.3s;
}

.testimonial-card:nth-child(4) {
  animation-delay: 0.4s;
}

/* 星级装饰 */
.testimonial-card::after {
  content: '⭐⭐⭐⭐⭐';
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 0.8rem;
  opacity: 0.7;
}
</style>

## 🚀 立即开始

准备好提升你的终端体验了吗？

- [快速开始](./getting-started/quick-start.md) - 5分钟快速上手
- [功能特性](./features/) - 了解 AIS 的强大功能
- [配置指南](./configuration/) - 个性化配置设置

---

::: tip 简单易用
一键安装脚本自动检测环境，支持多种安装方式，无需复杂配置。
:::

::: info 隐私保护
本地数据存储，支持本地AI模型，敏感数据过滤，保护您的隐私安全。
:::

::: warning 系统要求
需要 Python 3.8+ 和兼容的 Shell 环境（Bash/Zsh/Fish）。
:::