# 学习系统

AIS 的学习系统提供结构化的技术学习体验，通过 AI 生成个性化的学习内容，帮助您系统性地掌握各种技术知识。

## 📚 功能概览

### 核心特性
- **主题学习**：支持 Git、Docker、Vim、SSH 等主题的深度学习
- **渐进式内容**：根据用户水平调整教学深度
- **结构化输出**：使用 Markdown 格式提供易读的学习内容
- **个性化推荐**：基于用户历史行为的智能建议
- **学习进度跟踪**：记录学习历史和进度

## 🚀 基本使用

### 主题学习
```bash
# 学习 Git 基础
ais learn git

# 学习 Docker 容器化
ais learn docker

# 学习 Vim 编辑器
ais learn vim

# 学习 SSH 远程连接
ais learn ssh
```

### 指定学习级别
```bash
# 初级学习
ais learn git --level beginner

# 中级学习
ais learn docker --level intermediate

# 高级学习
ais learn kubernetes --level advanced
```

### 指定学习格式
```bash
# Markdown 格式（默认）
ais learn git --format markdown

# 交互式教程
ais learn vim --format interactive

# 简要概述
ais learn ssh --format summary
```

## 🎯 支持的学习主题

### 版本控制
```bash
# Git 版本控制
ais learn git
ais learn git-advanced
ais learn github

# SVN 版本控制
ais learn svn
```

### 容器化技术
```bash
# Docker 基础
ais learn docker
ais learn docker-compose

# Kubernetes 编排
ais learn kubernetes
ais learn k8s-deployment
```

### 编程语言
```bash
# Python 编程
ais learn python
ais learn python-advanced

# JavaScript 编程
ais learn javascript
ais learn nodejs

# Shell 脚本
ais learn bash
ais learn shell-scripting
```

### 系统管理
```bash
# Linux 系统
ais learn linux
ais learn linux-admin

# 网络配置
ais learn networking
ais learn ssh-config
```

### 开发工具
```bash
# 编辑器
ais learn vim
ais learn emacs

# 构建工具
ais learn makefile
ais learn cmake
```

## 📊 个性化学习

### 基于历史的推荐
```bash
# AIS 会基于您的错误历史推荐学习内容
ais learn --recommended

# 查看推荐理由
ais learn --recommended --explain
```

### 自适应难度
```bash
# AIS 会根据您的技能水平自动调整内容深度
ais learn docker
# 初次学习时提供基础内容
# 再次学习时提供进阶内容
```

### 学习路径
```bash
# 查看学习路径
ais learn-path web-development

# 跟随学习路径
ais learn-path web-development --follow
```

## 🎨 学习内容格式

### 结构化内容
学习内容包含以下部分：

```markdown
# 主题标题

## 📖 概述
- 技术简介
- 应用场景
- 核心概念

## 🚀 快速开始
- 安装配置
- 基本使用
- 常用命令

## 🔧 进阶技巧
- 高级功能
- 最佳实践
- 性能优化

## 📚 实践练习
- 动手实验
- 项目案例
- 常见问题

## 🔗 延伸阅读
- 官方文档
- 推荐资源
- 相关主题
```

### 交互式元素
```bash
# 代码示例
git clone https://github.com/example/repo.git
cd repo
git status

# 实践练习
[练习] 创建一个新的 Git 仓库并提交第一个文件

# 检查点
[检查] 你是否理解了 Git 的基本工作流程？
```

## 📈 学习进度管理

### 查看学习历史
```bash
# 查看所有学习记录
ais learn-history

# 查看特定主题的学习记录
ais learn-history --topic git

# 查看学习统计
ais learn-stats
```

### 学习进度跟踪
```bash
# 标记学习完成
ais learn git --mark-completed

# 标记学习进度
ais learn docker --progress 50

# 重置学习进度
ais learn kubernetes --reset
```

### 学习计划
```bash
# 创建学习计划
ais learn-plan create "DevOps 技能提升"

# 添加学习主题到计划
ais learn-plan add "DevOps 技能提升" docker kubernetes

# 开始学习计划
ais learn-plan start "DevOps 技能提升"
```

## 🔧 配置选项

### 学习偏好设置
```bash
# 设置默认学习级别
ais config set learning-level intermediate

# 设置学习语言
ais config set learning-language zh-CN

# 设置学习格式
ais config set learning-format markdown
```

### 内容定制
```bash
# 启用实践练习
ais config set include-exercises true

# 启用代码示例
ais config set include-code-examples true

# 启用相关链接
ais config set include-links true
```

## 📊 学习报告

### 生成学习报告
```bash
# 生成学习报告
ais learn-report

# 生成特定时间段的报告
ais learn-report --from 2024-01-01 --to 2024-01-31

# 生成特定主题的报告
ais learn-report --topic docker
```

### 学习统计
```bash
# 查看学习统计
ais learn-stats

# 学习时间统计
ais learn-stats --time

# 学习主题统计
ais learn-stats --topics
```

## 🤝 与其他功能集成

### 与错误分析集成
```bash
# 基于错误分析生成学习建议
ais analyze --command "docker run failed"
# 会提示: "建议学习 Docker 基础知识"

# 直接从错误分析进入学习
ais analyze --learn
```

### 与 AI 问答集成
```bash
# 从问答转入学习
ais ask "什么是 Kubernetes？" --learn

# 学习后继续问答
ais learn kubernetes
ais ask "如何部署应用到 Kubernetes？"
```

## 🎓 学习最佳实践

### 学习策略
```bash
# 1. 先了解概述
ais learn docker --section overview

# 2. 实践基础操作
ais learn docker --section quickstart

# 3. 深入高级功能
ais learn docker --section advanced

# 4. 解决实际问题
ais learn docker --section troubleshooting
```

### 学习笔记
```bash
# 导出学习内容为笔记
ais learn git --export notes.md

# 添加个人笔记
ais learn-note add git "个人理解和总结"

# 查看学习笔记
ais learn-note show git
```

## 🔍 高级功能

### 自定义学习主题
```bash
# 创建自定义学习主题
ais learn-custom create "公司内部工具"

# 添加自定义内容
ais learn-custom add "公司内部工具" content.md

# 学习自定义主题
ais learn "公司内部工具"
```

### 学习小组
```bash
# 创建学习小组
ais learn-group create "DevOps 学习小组"

# 加入学习小组
ais learn-group join "DevOps 学习小组"

# 分享学习进度
ais learn-group share docker
```

## 📚 学习资源

### 内置主题库
AIS 内置了丰富的学习主题：

- **开发工具**: Git, Docker, Kubernetes, Vim
- **编程语言**: Python, JavaScript, Go, Rust
- **系统管理**: Linux, SSH, 网络配置
- **数据库**: MySQL, PostgreSQL, MongoDB
- **云服务**: AWS, Azure, Google Cloud

### 扩展资源
```bash
# 查看可用的扩展主题
ais learn-topics --available

# 安装扩展主题
ais learn-topics install advanced-python

# 更新主题库
ais learn-topics update
```

## 🔒 离线学习

### 离线模式
```bash
# 启用离线模式
ais config set offline-mode true

# 下载学习内容
ais learn docker --download

# 离线学习
ais learn docker --offline
```

### 内容缓存
```bash
# 预缓存学习内容
ais learn-cache preload docker kubernetes

# 查看缓存状态
ais learn-cache status

# 清理缓存
ais learn-cache clear
```

---

## 下一步

- [学习报告](./learning-reports) - 查看学习成长报告
- [AI 问答](./ai-chat) - 智能问答助手
- [错误分析](./error-analysis) - 从错误中学习

---

::: tip 提示
学习系统会记录您的学习历史，建议定期查看学习报告来跟踪进度。
:::

::: info 个性化学习
AIS 会根据您的技能水平和学习历史自动调整学习内容的深度和重点。
:::

::: warning 注意
某些高级主题可能需要先掌握基础知识，建议按照推荐的学习路径进行学习。
:::