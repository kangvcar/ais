---
layout: home

hero:
  name: "AIS"
  text: "上下文感知的错误分析学习助手"
  tagline: "让每次报错都是成长，让每个错误都是学习"
  image:
    src: /logo-robot.png
    alt: AIS Logo
  actions:
    - theme: brand
      text: 🚀 立即体验
      link: /getting-started/quick-start
    - theme: alt
      text: 📖 了解更多
      link: /features/
    - theme: alt
      text: 💻 GitHub
      link: https://github.com/kangvcar/ais

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

# 国内用户可使用Gitee镜像（更快更稳定）
curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/install.sh | bash

# 或手动安装
pipx install ais-terminal
```


## 🔍 智能错误分析演示

当命令执行失败时，AIS会自动分析并提供解决方案：

<div id="error-analysis-demo" data-termynal data-ty-typeDelay="40" data-ty-lineDelay="700">
    <span data-ty="input">docker run hello-world</span>
    <span data-ty style="color: #ff6b6b;">docker: Error response from daemon: Unable to find image 'hello-world:latest' locally</span>
    <span data-ty="progress"></span>
    <span data-ty>🔍 发现相似的历史错误</span>
    <span data-ty>  1. docker pull ubuntu (12-15 14:30) - 已解决</span>
    <span data-ty>  2. docker run nginx (12-15 14:25) - 已分析</span>
    <span data-ty></span>
    <span data-ty>🤖 AI 错误分析</span>
    <span data-ty>🔍 问题诊断:</span>
    <span data-ty>您遇到了Docker镜像未找到的问题。Docker尝试运行hello-world镜像，但本地没有该镜像。</span>
    <span data-ty></span>
    <span data-ty>📚 知识扩展:</span>
    <span data-ty>Docker采用分层存储机制，镜像需要先下载到本地才能运行。</span>
    <span data-ty></span>
    <span data-ty>🎯 解决思路:</span>
    <span data-ty>1. 先手动拉取镜像到本地</span>
    <span data-ty>2. 检查网络连接和Docker服务状态</span>
    <span data-ty></span>
    <span data-ty>💡 AI 基于你的使用习惯和当前环境推荐</span>
    <span data-ty>#  命令                          风险  说明</span>
    <span data-ty>1  docker pull hello-world       🟢   拉取hello-world镜像到本地</span>
    <span data-ty>2  docker images                 🟢   查看已下载的镜像列表</span>
    <span data-ty>3  systemctl status docker       🟢   检查Docker服务状态</span>
    <span data-ty="input" data-ty-prompt="Select an action (1-3/e/q/x): ">1</span>
    <span data-ty="input">docker pull hello-world</span>
    <span data-ty>Using default tag: latest</span>
    <span data-ty>latest: Pulling from library/hello-world</span>
    <span data-ty>Status: Downloaded newer image for hello-world:latest</span>
    <span data-ty>✓ 问题解决！镜像已成功下载，现在可以运行容器了。</span>
</div>


## 💬 智能问答演示

使用 `ais ask` 获得即时专业答案：

<div id="qa-demo" data-termynal data-ty-typeDelay="40" data-ty-lineDelay="700">
    <span data-ty="input">ais ask "什么是Docker容器？"</span>
    <span data-ty>🤖 正在思考您的问题...</span>
    <span data-ty="progress"></span>
    <span data-ty></span>
    <span data-ty>## Docker容器是什么？</span>
    <span data-ty>Docker容器是一种轻量级的、可移植的、自包含的软件运行环境。</span>
    <span data-ty></span>
    <span data-ty>### 🏗️ 核心概念</span>
    <span data-ty>- 隔离性: 每个容器都有独立的文件系统、进程空间和网络接口</span>
    <span data-ty>- 轻量级: 比传统虚拟机更少的资源消耗</span>
    <span data-ty>- 可移植性: 一次构建，到处运行</span>
    <span data-ty></span>
    <span data-ty>### 🔧 主要特点</span>
    <span data-ty>1. 快速启动: 秒级启动时间</span>
    <span data-ty>2. 资源高效: 共享主机内核，无需完整操作系统</span>
    <span data-ty>3. 版本控制: 镜像分层存储，支持版本管理</span>
    <span data-ty></span>
    <span data-ty>💡 想了解更多？试试 ais learn docker 获得系统化学习路径！</span>
    <span data-ty></span>
    <span data-ty="input">ais ask "如何优化Docker镜像大小？"</span>
    <span data-ty>🤖 正在分析最佳实践...</span>
    <span data-ty="progress"></span>
    <span data-ty></span>
    <span data-ty>## Docker镜像优化技巧</span>
    <span data-ty>### 🎯 核心策略</span>
    <span data-ty>1. 使用多阶段构建 (Multi-stage builds)</span>
    <span data-ty>2. 选择合适的基础镜像 (如 alpine)</span>
    <span data-ty>3. 合并RUN指令减少层数</span>
    <span data-ty>4. 清理缓存和临时文件</span>
    <span data-ty></span>
    <span data-ty>### 📝 实践示例</span>
    <span data-ty>FROM alpine:3.18 AS builder</span>
    <span data-ty>RUN apk add --no-cache build-dependencies && \</span>
    <span data-ty>    build-app && \</span>
    <span data-ty>    apk del build-dependencies</span>
    <span data-ty></span>
    <span data-ty>✨ 这样可以将镜像从500MB减少到50MB！</span>
</div>

## 📊 学习报告演示

运行 `ais report` 获得个性化学习分析：

<div id="report-demo" data-termynal data-ty-typeDelay="40" data-ty-lineDelay="700">
    <span data-ty="input">ais report</span>
    <span data-ty>🔍 正在分析您的学习数据...</span>
    <span data-ty="progress"></span>
    <span data-ty></span>
    <span data-ty># 📊 AIS 学习成长报告</span>
    <span data-ty>分析周期: 最近30天 | 生成时间: 2025-01-15 10:30:45</span>
    <span data-ty></span>
    <span data-ty>## 🔍 错误概览</span>
    <span data-ty>- 总错误数: 23 次</span>
    <span data-ty>- 最常出错的命令: git (8次), docker (5次), npm (4次)</span>
    <span data-ty>- 最常见的错误类型: Git操作错误, Docker操作错误, 权限不足</span>
    <span data-ty></span>
    <span data-ty>## 💪 技能评估</span>
    <span data-ty>- 当前水平: 中级用户</span>
    <span data-ty>- 优势领域: 基础命令, 文件操作</span>
    <span data-ty>- 需要改进: Git版本控制, Docker容器</span>
    <span data-ty></span>
    <span data-ty>## 💡 改进洞察</span>
    <span data-ty>🔥 git 命令需要重点关注</span>
    <span data-ty>你在 git 命令上出现了 8 次错误，占总错误的 34.8%</span>
    <span data-ty></span>
    <span data-ty>## 🎯 学习建议</span>
    <span data-ty>1. 🔥 深入学习 git 命令</span>
    <span data-ty>   类型: 命令掌握 | 优先级: 高</span>
    <span data-ty>   学习路径:</span>
    <span data-ty>   - 学习Git基础概念（工作区、暂存区、仓库）</span>
    <span data-ty>   - 掌握常用Git命令（add, commit, push, pull）</span>
    <span data-ty>   - 了解分支操作和合并冲突解决</span>
    <span data-ty></span>
    <span data-ty>2. 🐳 提升 Docker 操作技能</span>
    <span data-ty>   类型: 容器化技术 | 优先级: 中</span>
    <span data-ty>   学习路径:</span>
    <span data-ty>   - 掌握Docker基础命令和概念</span>
    <span data-ty>   - 学习Dockerfile编写和镜像构建</span>
    <span data-ty>   - 了解容器网络和数据卷管理</span>
    <span data-ty></span>
    <span data-ty>## 📈 进步趋势</span>
    <span data-ty>本月相比上月错误率下降了 15% 🎉</span>
    <span data-ty>最常解决的问题类型: 权限问题</span>
    <span data-ty>新掌握的技能: npm包管理, 文件权限管理</span>
    <span data-ty></span>
    <span data-ty>💡 提示: 使用 ais learn <主题> 深入学习特定主题</span>
    <span data-ty>📚 帮助: 使用 ais ask <问题> 获取即时答案</span>
    <span data-ty></span>
    <span data-ty="input">ais learn git</span>
    <span data-ty>🎓 正在为您生成Git学习计划...</span>
    <span data-ty>✓ 已生成个性化Git学习路径，包含15个实战练习！</span>
</div>


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

  <div class="testimonial-card">
    <div class="testimonial-content">
      <div class="quote-icon">💬</div>
      <p class="testimonial-text">
        "作为新手，AIS的学习引导功能太棒了！每次报错都能学到新知识，从恐惧命令行到现在的熟练使用。"
      </p>
      <div class="testimonial-author">
        <div class="author-avatar">👩‍💻</div>
        <div class="author-info">
          <div class="author-name">小雨</div>
          <div class="author-role">前端开发实习生</div>
        </div>
      </div>
    </div>
  </div>

  <div class="testimonial-card">
    <div class="testimonial-content">
      <div class="quote-icon">💬</div>
      <p class="testimonial-text">
        "团队引入AIS后，初级开发者的上手速度明显提升。错误分析和学习建议帮助大家快速成长。"
      </p>
      <div class="testimonial-author">
        <div class="author-avatar">👨‍🏫</div>
        <div class="author-info">
          <div class="author-name">刘老师</div>
          <div class="author-role">技术团队负责人</div>
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

