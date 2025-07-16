# 常见问题

本文档收集了 AIS 使用过程中最常见的问题及其解决方案，帮助您快速解决遇到的问题。

## 🔧 安装问题

### 问题：ais 命令未找到
```bash
# 错误信息
bash: ais: command not found
```

**解决方案**：
```bash
# 1. 检查 PATH 环境变量
echo $PATH

# 2. 查找 ais 安装位置
which ais
whereis ais

# 3. 重新安装
pip install --upgrade ais-terminal

# 4. 如果使用 pipx
pipx install ais-terminal
pipx ensurepath

# 5. 重新加载 shell 配置
source ~/.bashrc  # 或 ~/.zshrc
```

### 问题：Python 版本不兼容
```bash
# 错误信息
ERROR: Package 'ais-terminal' requires Python '>=3.8'
```

**解决方案**：
```bash
# 1. 检查 Python 版本
python --version
python3 --version

# 2. 升级 Python（Ubuntu/Debian）
sudo apt update
sudo apt install python3.9 python3.9-pip

# 3. 使用特定 Python 版本安装
python3.9 -m pip install ais-terminal

# 4. 创建虚拟环境
python3.9 -m venv ais-env
source ais-env/bin/activate
pip install ais-terminal
```

### 问题：权限被拒绝
```bash
# 错误信息
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**解决方案**：
```bash
# 1. 使用用户安装（推荐）
pip install --user ais-terminal

# 2. 使用 pipx（推荐）
pipx install ais-terminal

# 3. 使用虚拟环境
python -m venv venv
source venv/bin/activate
pip install ais-terminal

# 4. 使用 sudo（不推荐）
sudo pip install ais-terminal
```

## 🤖 AI 提供商问题

### 问题：OpenAI API 密钥无效
```bash
# 错误信息
Error: Invalid API key provided
```

**解决方案**：
```bash
# 1. 检查 API 密钥格式
# OpenAI API 密钥格式：sk-...

# 2. 重新设置 API 密钥
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --api-key YOUR_ACTUAL_API_KEY

# 3. 从环境变量读取
export OPENAI_API_KEY="your-api-key"
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --api-key $OPENAI_API_KEY

# 4. 测试连接
ais provider-test openai
```

### 问题：Ollama 连接失败
```bash
# 错误信息
Error: Failed to connect to Ollama server
```

**解决方案**：
```bash
# 1. 检查 Ollama 是否运行
curl http://localhost:11434/api/version

# 2. 启动 Ollama
ollama serve

# 3. 检查端口
netstat -tuln | grep 11434

# 4. 重新配置提供商
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

# 5. 拉取模型
ollama pull llama2

# 6. 测试连接
ais provider-test ollama
```

### 问题：AI 响应超时
```bash
# 错误信息
Error: Request timeout
```

**解决方案**：
```bash
# 1. 增加超时时间
ais config set request-timeout 60

# 2. 检查网络连接
ping api.openai.com

# 3. 检查代理设置
ais config set proxy http://proxy.example.com:8080

# 4. 切换到其他提供商
ais provider-use claude

# 5. 使用本地模型
ais provider-use ollama
```

## 🐚 Shell 集成问题

### 问题：Shell 集成不工作
```bash
# 命令失败但没有自动分析
```

**解决方案**：
```bash
# 1. 检查集成状态
ais test-integration

# 2. 重新设置集成
ais setup

# 3. 检查 shell 配置文件
cat ~/.bashrc | grep ais
cat ~/.zshrc | grep ais

# 4. 手动添加集成
echo 'eval "$(ais shell-integration bash)"' >> ~/.bashrc
source ~/.bashrc

# 5. 检查钩子函数
type __ais_trap  # Bash
type __ais_precmd  # Zsh
```

### 问题：集成导致 Shell 变慢
```bash
# Shell 启动或命令执行变慢
```

**解决方案**：
```bash
# 1. 检查异步处理
ais config set async-analysis true

# 2. 减少上下文收集
ais config set context-level minimal

# 3. 增加分析延迟
ais config set analysis-delay 2

# 4. 暂时禁用
ais off

# 5. 调试性能
ais config set debug true
```

### 问题：在某些 Shell 中不工作
```bash
# 在 Fish 或其他 Shell 中不工作
```

**解决方案**：
```bash
# 1. 检查 Shell 类型
echo $SHELL

# 2. 手动配置 Fish
echo 'eval (ais shell-integration fish)' >> ~/.config/fish/config.fish

# 3. 重启 Fish
exec fish

# 4. 测试集成
ais test-integration --shell fish
```

## 💾 数据和配置问题

### 问题：配置文件损坏
```bash
# 错误信息
Error: Invalid configuration file
```

**解决方案**：
```bash
# 1. 检查配置文件
ais config validate

# 2. 查看配置文件位置
ais config show config-file

# 3. 备份并重置配置
cp ~/.config/ais/config.yaml ~/.config/ais/config.yaml.bak
ais config reset

# 4. 修复配置文件
ais config repair

# 5. 重新配置
ais setup
```

### 问题：数据库错误
```bash
# 错误信息
Error: Database is locked
```

**解决方案**：
```bash
# 1. 检查数据库状态
ais data diagnose

# 2. 关闭其他 AIS 进程
ps aux | grep ais
kill -9 <PID>

# 3. 修复数据库
ais data repair

# 4. 重建数据库
ais data rebuild

# 5. 恢复备份
ais data restore backup.db
```

### 问题：历史记录丢失
```bash
# 历史记录为空或不完整
```

**解决方案**：
```bash
# 1. 检查历史记录
ais history --limit 10

# 2. 检查数据库
ais data stats

# 3. 恢复历史记录
ais data restore-history

# 4. 检查权限
ls -la ~/.local/share/ais/

# 5. 重新启用历史记录
ais config set history-enabled true
```

## 🌐 网络问题

### 问题：网络连接超时
```bash
# 错误信息
Error: Connection timeout
```

**解决方案**：
```bash
# 1. 检查网络连接
ping 8.8.8.8
curl -I https://api.openai.com

# 2. 配置代理
ais config set proxy http://proxy.example.com:8080

# 3. 检查防火墙
sudo ufw status

# 4. 使用不同的 DNS
ais config set dns 8.8.8.8

# 5. 增加重试次数
ais config set retry-attempts 5
```

### 问题：SSL 证书错误
```bash
# 错误信息
Error: SSL certificate verify failed
```

**解决方案**：
```bash
# 1. 更新证书
sudo apt update && sudo apt install ca-certificates

# 2. 临时跳过验证（不推荐）
ais config set verify-ssl false

# 3. 使用自定义证书
ais config set ca-cert-path /path/to/cert.pem

# 4. 检查系统时间
date
sudo ntpdate -s time.nist.gov
```

## 🔒 权限问题

### 问题：访问被拒绝
```bash
# 错误信息
Error: Permission denied
```

**解决方案**：
```bash
# 1. 检查文件权限
ls -la ~/.config/ais/
ls -la ~/.local/share/ais/

# 2. 修复权限
chmod 755 ~/.config/ais/
chmod 644 ~/.config/ais/config.yaml

# 3. 重新创建目录
rm -rf ~/.config/ais/
ais setup

# 4. 检查磁盘空间
df -h
```

### 问题：无法写入日志
```bash
# 错误信息
Error: Cannot write to log file
```

**解决方案**：
```bash
# 1. 检查日志目录权限
ls -la ~/.local/share/ais/logs/

# 2. 创建日志目录
mkdir -p ~/.local/share/ais/logs/
chmod 755 ~/.local/share/ais/logs/

# 3. 更改日志位置
ais config set log-file /tmp/ais.log

# 4. 禁用日志
ais config set logging false
```

## 🚀 性能问题

### 问题：响应速度慢
```bash
# AI 分析或问答响应很慢
```

**解决方案**：
```bash
# 1. 使用更快的模型
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo  # 而不是 gpt-4

# 2. 减少上下文信息
ais config set context-level minimal

# 3. 启用缓存
ais config set enable-cache true

# 4. 使用本地模型
ais provider-use ollama

# 5. 优化网络
ais config set request-timeout 30
```

### 问题：内存使用过高
```bash
# AIS 进程占用大量内存
```

**解决方案**：
```bash
# 1. 检查内存使用
ps aux | grep ais
top -p $(pgrep ais)

# 2. 清理缓存
ais config clear-cache

# 3. 限制历史记录
ais config set max-history 100

# 4. 减少并发数
ais config set max-concurrent 1

# 5. 重启 AIS
ais restart
```

## 🛠️ 调试技巧

### 启用调试模式
```bash
# 启用详细调试
ais config set debug true
ais config set log-level debug

# 查看调试日志
tail -f ~/.local/share/ais/debug.log

# 调试特定命令
ais ask "test" --debug
ais analyze --debug
```

### 收集诊断信息
```bash
# 生成诊断报告
ais diagnose

# 检查系统兼容性
ais test-integration --verbose

# 收集系统信息
ais system-info

# 验证配置
ais config validate --verbose
```

### 重置到默认状态
```bash
# 完全重置
ais reset --all

# 保留数据的重置
ais reset --config-only

# 重新初始化
ais setup --force
```

## 📞 获取帮助

### 内置帮助
```bash
# 查看命令帮助
ais --help
ais ask --help
ais config --help

# 查看版本信息
ais --version

# 查看系统信息
ais system-info
```

### 社区支持
- **GitHub Issues**: 报告 Bug 和功能请求
- **文档**: 查看完整文档
- **讨论区**: 技术讨论和问答

### 日志文件位置
```bash
# 配置文件
~/.config/ais/config.yaml

# 数据文件
~/.local/share/ais/database.db

# 日志文件
~/.local/share/ais/logs/ais.log

# 调试日志
~/.local/share/ais/debug.log
```

---

## 下一步

- [常见问答](./faq) - 查看更多问答
- [基本配置](../configuration/basic-config) - 配置 AIS 设置
- [提供商管理](../features/provider-management) - 管理 AI 提供商

---

::: tip 提示
遇到问题时，首先尝试 `ais diagnose` 命令，它会自动检测常见问题。
:::

::: info 调试
启用调试模式可以帮助您更好地理解问题的根本原因。
:::

::: warning 注意
修改配置文件前，建议先备份，避免配置损坏。
:::