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

# 3. 从源码安装
cd /path/to/ais
source .venv/bin/activate && python3 -m pip install -e .

# 4. 重新加载 shell 配置
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
python3.9 -m pip install -e .

# 4. 创建虚拟环境
python3.9 -m venv ais-env
source ais-env/bin/activate
pip install -e .
```

### 问题：依赖安装失败
```bash
# 错误信息
ERROR: Failed building wheel for some-package
```

**解决方案**：
```bash
# 1. 更新 pip
pip install --upgrade pip

# 2. 安装构建依赖
sudo apt-get install build-essential python3-dev

# 3. 清理缓存重新安装
pip cache purge
pip install -e .

# 4. 安装HTML可视化依赖
pip install -e .[html]
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
  --key YOUR_ACTUAL_API_KEY

# 3. 验证提供商配置
ais provider-list

# 4. 切换到正确的提供商
ais provider-use openai
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
```

### 问题：AI 响应超时
```bash
# 错误信息
Request timeout
```

**解决方案**：
```bash
# 1. 检查网络连接
ping api.openai.com

# 2. 切换到其他提供商
ais provider-use claude

# 3. 使用本地模型
ais provider-use ollama

# 4. 检查提供商状态
ais provider-list
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

# 3. 检查集成是否开启
ais config --get advanced.auto_analysis

# 4. 开启自动分析
ais on

# 5. 检查 shell 配置文件
cat ~/.bashrc | grep ais
cat ~/.zshrc | grep ais
```

### 问题：重复分析同一个错误
```bash
# 同一个错误被重复分析
```

**解决方案**：
```bash
# 1. 检查分析冷却时间
ais config --get advanced.analysis_cooldown

# 2. 调整冷却时间（秒）
ais config --set advanced.analysis_cooldown=120

# 3. 检查是否正常工作
# 快速连续执行同一个错误命令，应该只分析第一次
```

## 💾 数据和配置问题

### 问题：配置文件损坏
```bash
# 错误信息
Error: Invalid configuration file
```

**解决方案**：
```bash
# 1. 查看配置文件位置
echo ~/.config/ais/config.toml

# 2. 检查配置文件语法
cat ~/.config/ais/config.toml

# 3. 备份并重新初始化
cp ~/.config/ais/config.toml ~/.config/ais/config.toml.bak
rm ~/.config/ais/config.toml
ais setup

# 4. 重新配置提供商
ais provider-add openai --url https://api.openai.com/v1/chat/completions --model gpt-3.5-turbo --key YOUR_KEY
```

### 问题：历史记录为空
```bash
# 历史记录为空或不完整
```

**解决方案**：
```bash
# 1. 检查历史记录
ais history

# 2. 检查数据库文件
ls -la ~/.local/share/ais/database.db

# 3. 检查权限
ls -la ~/.local/share/ais/

# 4. 执行一些命令产生错误，然后检查是否记录
ls /nonexistent 2>&1
ais history --limit 1
```

### 问题：上下文级别配置无效
```bash
# 设置的上下文级别不生效
```

**解决方案**：
```bash
# 1. 检查当前配置
ais config

# 2. 正确设置上下文级别
ais config --set ask.context_level=standard

# 3. 验证设置
ais config --get ask.context_level

# 4. 查看上下文帮助
ais config --help-context
```

## 🌐 网络问题

### 问题：网络连接超时
```bash
# 错误信息
Connection timeout
```

**解决方案**：
```bash
# 1. 检查网络连接
ping 8.8.8.8
curl -I https://api.openai.com

# 2. 使用本地AI避免网络问题
ais provider-use ollama

# 3. 检查防火墙
sudo ufw status
```

### 问题：SSL 证书错误
```bash
# 错误信息
SSL certificate verify failed
```

**解决方案**：
```bash
# 1. 更新证书
sudo apt update && sudo apt install ca-certificates

# 2. 检查系统时间
date
sudo ntpdate -s time.nist.gov
```

## 🔒 权限问题

### 问题：访问被拒绝
```bash
# 错误信息
Permission denied
```

**解决方案**：
```bash
# 1. 检查文件权限
ls -la ~/.config/ais/
ls -la ~/.local/share/ais/

# 2. 修复权限
chmod 755 ~/.config/ais/
chmod 644 ~/.config/ais/config.toml

# 3. 重新创建目录
rm -rf ~/.config/ais/
ais setup

# 4. 检查磁盘空间
df -h
```

## 📊 HTML报告问题

### 问题：HTML报告生成失败
```bash
# 错误信息
ImportError: 需要安装plotly库
```

**解决方案**：
```bash
# 1. 安装HTML依赖
pip install plotly numpy

# 2. 或者安装完整HTML功能
pip install -e .[html]

# 3. 验证安装
python -c "import plotly; print('Plotly installed successfully')"

# 4. 测试HTML报告
ais report --html
```

### 问题：HTML报告图表为空
```bash
# HTML报告生成但图表为空
```

**解决方案**：
```bash
# 1. 确保有足够的历史数据
ais history

# 2. 产生一些错误数据用于测试
ls /nonexistent 2>&1
docker invalidcommand 2>&1
git invalidcommand 2>&1

# 3. 等待几分钟后重新生成报告
ais report --html
```

## 🛠️ 调试技巧

### 启用详细输出
```bash
# 查看详细帮助
ais help-all

# 查看特定命令详细帮助
ais ask --help-detail
ais learn --help-detail
```

### 测试功能
```bash
# 测试Shell集成
ais test-integration

# 测试AI问答
ais ask "测试连接"

# 查看配置
ais config

# 查看提供商状态
ais provider-list
```

### 重置到默认状态
```bash
# 删除配置文件重新开始
rm -rf ~/.config/ais/
rm -rf ~/.local/share/ais/
ais setup
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

# 查看所有命令详细帮助
ais help-all
```

### 社区支持
- **GitHub Issues**: 报告 Bug 和功能请求
- **文档**: 查看完整文档
- **讨论区**: 技术讨论和问答

### 文件位置
```bash
# 配置文件
~/.config/ais/config.toml

# 数据库文件
~/.local/share/ais/database.db

# 日志文件
~/.local/share/ais/logs/
```

---

## 下一步

- [常见问答](./faq) - 查看更多问答
- [基本配置](../configuration/basic-config) - 配置 AIS 设置
- [提供商管理](../features/provider-management) - 管理 AI 提供商

---

::: tip 提示
遇到问题时，首先尝试 `ais test-integration` 和 `ais help-all` 命令进行诊断。
:::

::: info 调试
如果问题持续，可以删除配置文件重新初始化：`rm -rf ~/.config/ais/ && ais setup`
:::

::: warning 注意
修改配置文件前，建议先备份，避免配置损坏。
:::