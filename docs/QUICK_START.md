# AIS 快速开始指南

5分钟快速上手 AIS - AI智能终端助手！

## 🚀 30秒安装

### 🎯 一键安装（推荐）
```bash
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
```

**就这么简单！** 脚本会自动：
- 🔍 检测你的环境
- 📦 选择最佳安装方式  
- ⚡ 完成安装和配置

### 🐳 容器用户
```bash
docker run -it --rm ais-terminal:latest
```

### 👨‍💻 Python用户
```bash
pipx install ais-terminal
ais setup
```

## ✅ 验证安装

```bash
# 检查版本
ais --version

# 测试基本功能  
ais ask "你好"

# 测试错误分析（故意输错命令）
mkdirr /tmp/test
```

## 🎮 立即体验

### 1. 智能错误分析
```bash
# 输入错误命令，AIS会自动分析
pytho --version        # 拼写错误
ls /not/exist/path    # 路径不存在
git statuss           # 命令错误
```

### 2. AI对话
```bash
# 向AI提问
ais ask "如何查看系统内存使用情况？"
ais ask "Docker容器如何挂载目录？"
ais ask "解释一下这个错误: Permission denied"
```

### 3. 命令建议
```bash
# 获取命令建议
ais suggest "我想压缩一个文件夹"
ais suggest "如何查找大文件"
```

## ⚙️ 基础配置

### 查看当前配置
```bash
ais config
```

### 设置API提供商（可选）
```bash
# 使用OpenAI
ais config set provider openai
ais config set api_key "your-api-key"

# 使用其他提供商
ais config set provider anthropic
ais config set base_url "https://api.anthropic.com"
```

### 调整分析级别
```bash
# 设置分析详细程度
ais config set analysis_level detailed  # detailed/standard/simple
```

## 🔧 Shell集成

AIS安装后会自动设置shell集成，启用以下功能：

### 1. 自动错误分析
命令执行失败时自动显示AI分析：
```bash
$ mkdirr test
bash: mkdirr: command not found

🤖 AIS分析：
看起来你想创建目录，但命令拼写错误。
建议使用：mkdir test
```

### 2. 历史命令增强
```bash
# 分析最近的错误命令
ais analyze-last

# 分析指定历史命令
ais analyze-history 5
```

### 3. 快捷别名
```bash
# 这些别名会自动创建
a="ais ask"           # 快速提问
aa="ais analyze-last" # 分析上次错误
as="ais suggest"      # 获取建议
```

## 📚 常用命令速查

### 核心功能
```bash
ais ask "问题"              # AI对话
ais suggest "需求描述"       # 命令建议  
ais analyze "错误信息"       # 错误分析
ais explain "命令"          # 命令解释
```

### 配置管理
```bash
ais config                 # 查看配置
ais config set key value   # 设置配置
ais config reset          # 重置配置
ais setup                 # 重新设置shell集成
```

### 实用工具
```bash
ais doctor               # 健康检查
ais --debug             # 调试模式
ais --help              # 帮助信息
ais --version           # 版本信息
```

## 🎯 使用场景示例

### 场景1：命令行新手
```bash
# 不知道如何操作时
$ ais ask "如何复制文件夹到另一个位置？"

🤖 回答：使用 cp 命令：
cp -r source_folder destination_folder

参数说明：
-r: 递归复制（包含子目录）
```

### 场景2：错误排查
```bash
# 命令执行失败
$ docker run nginx
docker: Error response from daemon: pull access denied

$ ais analyze-last
🤖 分析：Docker镜像拉取权限被拒绝
可能原因：
1. 镜像名称不完整，尝试：docker run nginx:latest
2. 需要登录：docker login
3. 镜像不存在或权限不足
```

### 场景3：学习新技术
```bash
# 学习新命令
$ ais ask "Kubernetes的基本命令有哪些？"

🤖 回答：Kubernetes常用命令：
kubectl get pods          # 查看Pod
kubectl describe pod xxx   # 查看Pod详情
kubectl logs pod-name     # 查看日志
kubectl apply -f file.yaml # 应用配置
```

## 🛡️ 隐私和安全

### 默认安全设置
- ✅ 敏感目录自动排除（~/.ssh, ~/.aws等）
- ✅ 个人信息脱敏处理
- ✅ 本地配置文件加密存储

### 隐私控制
```bash
# 禁用自动分析
ais config set auto_analysis false

# 设置敏感目录
ais config set sensitive_dirs "~/.secret,~/private"

# 查看隐私设置
ais config privacy
```

## 🆘 遇到问题？

### 常见问题快速解决
```bash
# 一键诊断
ais doctor

# 重新安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

# 查看详细日志
ais --debug ask "test"
```

### 获取帮助
- 📖 [完整文档](INSTALLATION.md)
- 🐛 [报告问题](https://github.com/kangvcar/ais/issues)
- 💬 [社区讨论](https://github.com/kangvcar/ais/discussions)
- 📧 [邮件支持](mailto:ais@example.com)

## 🎉 下一步

恭喜！你已经掌握了AIS的基本用法。接下来可以：

1. 📚 阅读 [高级配置指南](CONFIGURATION.md)
2. 🐳 尝试 [Docker部署](DOCKER_GUIDE.md)  
3. 🔧 参与 [开发贡献](DEVELOPMENT.md)
4. ⭐ 给项目 [点个星](https://github.com/kangvcar/ais)

---

🚀 **开始你的AI终端之旅吧！** 任何问题都可以直接问AIS：`ais ask "你的问题"`