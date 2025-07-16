# 常见问题解答

本文档收集了用户在使用 AIS 过程中遇到的常见问题及其解决方案。

## 安装相关问题

### Q: 安装时出现权限错误怎么办？

```bash
# 错误示例
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied

# 解决方案 1：使用 --user 参数
pip install --user ais-terminal

# 解决方案 2：使用虚拟环境
python -m venv ais-env
source ais-env/bin/activate
pip install ais-terminal
```

### Q: Python 版本不兼容怎么办？

```bash
# 检查 Python 版本
python --version

# 如果版本过低，使用 python3
python3 --version
python3 -m pip install ais-terminal

# 或者升级 Python 版本
```

### Q: 安装后找不到 ais 命令？

```bash
# 检查是否在 PATH 中
which ais

# 如果使用 --user 安装，需要确保用户 bin 目录在 PATH 中
export PATH="$HOME/.local/bin:$PATH"

# 将上述命令添加到 ~/.bashrc 或 ~/.zshrc
```

## 配置相关问题

### Q: Shell 集成不工作怎么办？

**检查集成是否正确配置：**

```bash
# 测试集成
ais test-integration

# 重新设置集成
ais setup

# 手动检查集成脚本
ls -la ~/.config/ais/
```

**常见解决方案：**

1. 重新加载 Shell 配置
```bash
source ~/.bashrc  # 或 ~/.zshrc
```

2. 检查集成脚本是否存在
```bash
find /usr/local/lib/python*/site-packages/ais/ -name "integration.sh"
```

3. 手动添加集成配置
```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
source "/path/to/ais/shell/integration.sh"
```

### Q: AI 服务连接失败怎么办？

**检查网络连接：**

```bash
# 测试网络连接
ping api.deepbricks.ai

# 测试 API 连接
curl -s https://api.deepbricks.ai/v1/chat/completions
```

**检查配置：**

```bash
# 查看当前配置
ais config

# 检查提供商配置
ais provider-list
```

**常见解决方案：**

1. 检查 API 密钥是否正确
2. 确认服务 URL 是否可访问
3. 尝试使用其他 AI 服务提供商

### Q: 如何配置代理？

如果您在企业网络或需要代理访问：

```bash
# 设置环境变量
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=https://proxy.company.com:8080

# 或者在配置文件中设置
# 编辑 ~/.config/ais/config.toml
```

## 使用相关问题

### Q: 自动分析不准确怎么办？

**优化分析准确性：**

```bash
# 使用详细的上下文收集
ais config --set context_level=detailed

# 使用更好的 AI 模型
ais provider-use openai  # 如果有 OpenAI 账户

# 提供更多错误信息
ais analyze --exit-code 1 --command "your_command" --stderr "error_output"
```

### Q: 如何提高响应速度？

```bash
# 使用本地 AI 服务（如 Ollama）
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama3

# 使用较快的 AI 服务
ais provider-add fast-api \
  --url https://fast-api.example.com/v1/chat/completions \
  --model gpt-3.5-turbo
```

### Q: 历史记录太多怎么清理？

```bash
# 查看数据库位置
ls -la ~/.config/ais/

# 清理历史记录（需要手动删除数据库文件）
rm ~/.config/ais/ais.db

# 重新启动 AIS 会创建新的数据库
ais config
```

## 功能相关问题

### Q: 某些命令不会自动分析？

**可能的原因：**

1. 命令退出码为 0（成功）
2. 命令被过滤（如内部命令）
3. 自动分析被关闭

**解决方案：**

```bash
# 检查自动分析状态
ais config

# 启用自动分析
ais on

# 手动分析特定命令
ais analyze --exit-code 1 --command "your_command"
```

### Q: 如何学习自定义主题？

```bash
# 可以学习任何主题
ais learn kubernetes
ais learn react
ais learn "machine learning"

# 询问具体问题
ais ask "如何使用 Kubernetes 部署应用？"
```

### Q: 如何查看详细的错误分析？

```bash
# 查看历史记录
ais history

# 查看特定记录的详细信息
ais history 1

# 查看更多历史记录
ais history -n 50
```

## 性能相关问题

### Q: AIS 占用太多系统资源怎么办？

**优化建议：**

```bash
# 使用最小上下文收集
ais config --set context_level=minimal

# 在不需要时关闭自动分析
ais off

# 使用更轻量的 AI 服务
```

### Q: 响应时间太慢怎么办？

**提升响应速度：**

1. 使用本地 AI 服务（Ollama）
2. 选择更快的 AI 模型
3. 优化网络连接
4. 使用缓存机制

```bash
# 使用本地 AI 服务
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama3:latest

ais provider-use ollama
```

## 错误处理

### Q: 遇到程序崩溃怎么办？

**收集错误信息：**

```bash
# 查看详细错误信息
ais --help

# 运行诊断
ais test-integration

# 检查日志文件
ls -la ~/.config/ais/
```

**报告问题：**

1. 收集错误信息
2. 记录重现步骤
3. 在 GitHub 上提交 Issue
4. 提供系统信息

### Q: 如何重置配置？

```bash
# 备份当前配置
cp ~/.config/ais/config.toml ~/.config/ais/config.toml.bak

# 删除配置文件
rm ~/.config/ais/config.toml

# 重新运行 AIS 会创建默认配置
ais config
```

## 高级问题

### Q: 如何自定义 AI 服务提供商？

```bash
# 添加自定义提供商
ais provider-add custom \
  --url https://your-api.example.com/v1/chat/completions \
  --model your-model \
  --key your-api-key

# 切换到自定义提供商
ais provider-use custom
```

### Q: 如何贡献到 AIS 项目？

1. Fork 项目仓库
2. 创建功能分支
3. 提交代码更改
4. 发起 Pull Request
5. 参与代码审查

详情请参考[贡献指南](../development/contributing)。

### Q: 如何报告安全漏洞？

如果您发现安全漏洞：

1. 不要在公开场所报告
2. 发送邮件到项目维护者
3. 提供详细的漏洞信息
4. 等待安全修复发布

## 获取更多帮助

如果以上 FAQ 没有解决您的问题：

1. 查看[基本使用](./basic-usage)
2. 查看[故障排除](../troubleshooting/common-issues)
3. 在 [GitHub Issues](https://github.com/kangvcar/ais/issues) 中搜索
4. 提交新的 Issue
5. 加入社区讨论

---

::: tip 提示
遇到问题时，首先尝试 `ais test-integration` 命令来诊断系统状态。
:::

::: warning 注意
在报告问题时，请移除任何敏感信息（如 API 密钥、个人数据等）。
:::