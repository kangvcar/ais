# 基本使用

本指南将介绍 AIS 的基本使用方法，帮助您快速上手并掌握核心功能。

## 核心功能概览

AIS 提供以下核心功能：

- **自动错误分析**：命令失败时自动分析并提供解决方案
- **AI 问答**：快速获得技术问题的答案
- **系统化学习**：深入学习特定技术主题
- **历史记录**：查看和分析命令执行历史
- **配置管理**：管理 AI 服务提供商和系统设置

## 1. 自动错误分析

这是 AIS 的核心功能，当命令执行失败时自动触发分析。

### 启用自动分析

```bash
# 启用自动错误分析
ais on

# 检查状态
ais config

# 如果需要关闭
ais off
```

### 体验自动分析

```bash
# 尝试执行一个会失败的命令
mkdir /root/protected_dir

# 如果失败，AIS 会自动分析错误原因并提供解决方案
```

### 手动分析错误

如果您想手动分析特定错误：

```bash
# 手动分析上一个失败的命令
ais analyze --exit-code 1 --command "mkdir /root/protected_dir"

# 包含错误输出的分析
ais analyze --exit-code 1 --command "npm install" --stderr "permission denied"
```

## 2. AI 问答功能

使用 `ais ask` 命令快速获得技术问题的答案。

### 基本问答

```bash
# 询问概念性问题
ais ask "什么是 Docker 容器？"

# 询问具体的技术问题
ais ask "如何解决 Git 合并冲突？"

# 询问最佳实践
ais ask "Python 虚拟环境的最佳实践是什么？"
```

### 问答技巧

```bash
# 使用引号包围问题，避免 shell 解析问题
ais ask "如何在 Linux 中查找大文件？"

# 可以询问很具体的问题
ais ask "npm ERR! code EACCES 错误如何解决？"

# 询问工具使用方法
ais ask "grep 命令的常用参数有哪些？"
```

### 获取详细帮助

```bash
# 查看 ask 命令的详细帮助
ais ask --help-detail
```

## 3. 系统化学习

使用 `ais learn` 命令进行系统化的技术学习。

### 查看可学习主题

```bash
# 显示所有可学习的主题
ais learn
```

### 学习特定主题

```bash
# 学习 Git 版本控制
ais learn git

# 学习 Docker 容器化
ais learn docker

# 学习 SSH 远程连接
ais learn ssh

# 学习 Linux 权限管理
ais learn permissions
```

### 自定义学习主题

```bash
# 可以学习任何主题，即使不在预定义列表中
ais learn kubernetes

# 学习编程语言
ais learn python

# 学习工具使用
ais learn vim
```

### 获取学习帮助

```bash
# 查看 learn 命令的详细帮助
ais learn --help-detail
```

## 4. 历史记录管理

AIS 会记录所有的命令执行历史，您可以查看和分析这些记录。

### 查看历史记录

```bash
# 显示最近的命令历史
ais history

# 显示更多历史记录
ais history --limit 20

# 只显示失败的命令
ais history --failed-only

# 按命令名称过滤
ais history --command-filter git
```

### 查看详细信息

```bash
# 查看特定记录的详细信息
ais history 1

# 查看第 3 条记录的详细分析
ais history 3
```

### 历史记录功能

```bash
# 查看 history 命令的详细帮助
ais history --help-detail
```

## 5. 配置管理

### 查看当前配置

```bash
# 显示当前配置
ais config

# 获取特定配置项
ais config --get auto_analysis

# 查看所有 AI 服务提供商
ais provider-list
```

### 修改配置

```bash
# 启用/关闭自动分析
ais config --set auto_analysis=true
ais config --set auto_analysis=false

# 设置上下文收集级别
ais config --set context_level=detailed
ais config --set context_level=standard
ais config --set context_level=minimal

# 查看上下文配置帮助
ais config --help-context
```

### AI 服务提供商管理

```bash
# 列出所有提供商
ais provider-list

# 添加新的提供商
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-4 \
  --key your_api_key

# 切换提供商
ais provider-use openai

# 删除提供商
ais provider-remove openai

# 查看提供商管理帮助
ais provider-add --help-detail
```

## 6. 学习成长报告

AIS 会分析您的使用历史，生成学习成长报告。

```bash
# 生成学习报告
ais report
```

报告包含：
- 错误概览统计
- 最常见的错误类型
- 学习进度分析
- 技能提升建议

## 7. 系统管理

### 设置和测试

```bash
# 设置 Shell 集成
ais setup

# 测试集成是否正常工作
ais test-integration

# 查看所有命令的详细帮助
ais help-all
```

### 开关功能

```bash
# 快速开启自动分析
ais on

# 快速关闭自动分析
ais off
```

## 实际使用示例

### 示例 1: 日常开发工作流

```bash
# 1. 启用自动分析
ais on

# 2. 正常工作，当命令失败时自动分析
git push origin main
# 如果失败，自动显示分析结果

# 3. 主动询问问题
ais ask "如何解决 Git 推送被拒绝的问题？"

# 4. 查看历史记录
ais history --failed-only

# 5. 生成学习报告
ais report
```

### 示例 2: 学习新技术

```bash
# 1. 系统学习 Docker
ais learn docker

# 2. 询问具体问题
ais ask "Docker 容器和镜像的区别是什么？"

# 3. 实践过程中遇到错误时自动分析
docker run -d nginx
# 如果失败，自动分析

# 4. 查看学习历史
ais history --command-filter docker
```

### 示例 3: 解决复杂问题

```bash
# 1. 遇到复杂错误时的分析
npm install
# 自动分析错误

# 2. 查看详细的历史分析
ais history 1

# 3. 针对性学习
ais learn npm

# 4. 询问解决方案
ais ask "npm 权限错误的解决方案有哪些？"
```

## 最佳实践

### 1. 配置优化

```bash
# 使用详细的上下文收集级别
ais config --set context_level=detailed

# 保持自动分析开启
ais on
```

### 2. 有效提问

- 使用具体和清晰的问题描述
- 包含相关的错误信息
- 指明您的操作系统和工具版本

### 3. 学习策略

- 定期查看学习报告
- 系统学习感兴趣的主题
- 结合实际问题进行学习

### 4. 历史记录利用

- 定期查看失败的命令历史
- 分析错误模式
- 学习从历史错误中获得的经验

## 常见问题

### Q: 自动分析不工作怎么办？

```bash
# 检查配置
ais config

# 测试集成
ais test-integration

# 重新设置
ais setup
```

### Q: 如何获得更准确的分析？

- 使用 `detailed` 上下文级别
- 确保网络连接正常
- 使用性能更好的 AI 服务提供商

### Q: 如何保护隐私？

- 数据全部存储在本地
- 可以配置敏感目录过滤
- 可以随时关闭自动分析

## 下一步

掌握基本使用后，您可以：

1. 深入了解[功能特性](../features/)
2. 查看[功能特性](../features/)
3. 学习[高级配置](../configuration/)

---

::: tip 提示
建议每天使用 AIS 进行工作，让错误分析成为您学习和成长的自然过程。
:::

::: warning 注意
如果遇到任何问题，可以随时使用 `ais ask` 命令寻求帮助。
:::