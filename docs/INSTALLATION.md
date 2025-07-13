# AIS 安装指南

本文档按用户类型提供 AIS（AI-powered terminal assistant）的最佳安装方式。

## 系统要求

- **Python**: 3.8+ （推荐 3.11+）
- **操作系统**: Linux, macOS, Windows
- **网络**: 需要网络连接以下载依赖和AI服务
- **空间**: 至少 100MB 可用空间

## 👤 按用户类型选择安装方式

### 👨‍💻 个人开发者（最佳实践）

**特点**: 只需要个人使用，注重安全性和简单性

**推荐安装方式**: pipx 用户级安装

```bash
# 一键安装（智能检测）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

# 或手动安装
# 1. 安装pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# 2. 安装AIS
pipx install ais-terminal

# 3. 设置shell集成
ais setup
```

**优势**:
- ✅ 最高安全性，独立虚拟环境
- ✅ 无需sudo权限
- ✅ 简单升级和卸载
- ✅ 不影响系统环境

### 🏢 团队/企业环境（推荐）

**特点**: 多人使用，需要统一管理

**推荐安装方式**: pipx 全局安装

```bash
# 一键安装（管理员执行）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system

# 或手动安装
# 1. 安装pipx
sudo apt install pipx  # Ubuntu/Debian
# 或 sudo yum install python3-pipx  # CentOS/RHEL

# 2. 全局安装AIS
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal

# 3. 用户设置shell集成
ais setup  # 每个用户都需要执行
```

**优势**:
- ✅ 所有用户可用
- ✅ 保持安全隔离
- ✅ 集中管理和更新
- ✅ 版本一致性

### 🐳 容器/云环境

**特点**: Docker容器、K8s集群或云平台

**推荐安装方式**: Docker 容器化部署

```bash
# Docker 安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/docker-install.sh | bash

# 或直接使用Docker
docker run -it --rm ais-terminal:latest

# Docker Compose
wget https://raw.githubusercontent.com/kangvcar/ais/main/docker-compose.yml
docker-compose up -d ais
```

**优势**:
- ✅ 环境一致性
- ✅ 快速部署
- ✅ 易于扩展
- ✅ 完全隔离

### 🔧 开发者/贡献者

**特点**: 需要修改代码或测试新功能

**推荐安装方式**: 源码安装

```bash
# 克隆仓库
git clone https://github.com/kangvcar/ais.git
cd ais

# 使用pipx开发模式安装
pipx install -e .

# 或使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -e .

# 设置开发环境
pip install -e ".[dev]"
pre-commit install
```

**优势**:
- ✅ 实时修改效果
- ✅ 完整开发工具链
- ✅ 代码质量检查
- ✅ 易于调试

## 🚀 快速开始

### 一键智能安装（推荐）

自动检测环境并选择最佳安装方式：

```bash
# 智能安装（推荐）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
```

该脚本会：
- 🔍 检测当前环境（用户/管理员/容器）
- 🎯 自动选择最佳安装方式
- 🛠️ 安装pipx（如果需要）
- 📦 安装AIS
- 🔧 设置shell集成
- 🔍 执行健康检查

### 手动指定安装模式

```bash
# 用户级安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --user

# 系统级安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system

# 容器安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/docker-install.sh | bash
```

## 📊 安装方式对比

| 用户类型 | 推荐方式 | 安全性 | 简单度 | 权限需求 | 推荐指数 |
|---------|---------|-------|-------|---------|----------|
| 👨‍💻 **个人开发者** | pipx用户级 | 🟢 最高 | 🟢 最简单 | 普通用户 | ⭐⭐⭐⭐⭐ |
| 🏢 **团队企业** | pipx全局 | 🟢 高 | 🟢 简单 | sudo | ⭐⭐⭐⭐⭐ |
| 🐳 **容器部署** | Docker | 🟢 高 | 🟢 简单 | docker | ⭐⭐⭐⭐⭐ |
| 🔧 **开发贡献** | 源码安装 | 🟡 中等 | 🟡 中等 | 看情况 | ⭐⭐⭐⭐ |
| 🛠️ **运维管理** | 系统全局 | 🟡 中等 | 🟡 中等 | root | ⭐⭐⭐ |

## 🔧 安装后配置

### 健康检查

安装脚本会自动执行健康检查，也可手动验证：

```bash
# 检查AIS是否正常安装
ais --version

# 测试基本功能
ais config --help
ais ask "Hello AIS"

# 测试自动错误分析
mkdirr /tmp/test  # 故意输错命令
```

### Shell集成设置

大多数安装方式会自动设置shell集成，如需手动设置：

```bash
# 自动设置shell集成
ais setup

# 立即生效（可选）
source ~/.bashrc  # Bash
source ~/.zshrc   # Zsh

# 或重新打开终端
```

### 初始配置

```bash
# 查看当前配置
ais config

# 初始化配置（可选）
ais config init

# 设置API提供商（可选）
ais config set provider openai
```

## 🛠️ 故障排除

### 常见问题

#### 1. 安装失败
```bash
# 检查Python版本
python3 --version  # 需要 >= 3.8

# 检查网络连接
curl -I https://pypi.org/simple/ais-terminal/

# 重新安装pipx
python3 -m pip install --user --force-reinstall pipx
python3 -m pipx ensurepath
```

#### 2. 命令找不到
```bash
# 检查ais是否安装
which ais
pipx list | grep ais

# 重新加载PATH
source ~/.bashrc
# 或重新打开终端

# 手动添加到PATH
export PATH="$HOME/.local/bin:$PATH"  # pipx用户级
export PATH="/usr/local/bin:$PATH"    # pipx全局
```

#### 3. 容器问题
```bash
# 检查Docker环境
docker --version
docker info

# 重新构建镜像
docker build -t ais-terminal:latest .

# 检查容器日志
docker logs <container_id>
```

#### 4. 权限问题
```bash
# Docker权限
sudo usermod -aG docker $USER
# 重新登录或执行: newgrp docker

# 系统安装权限
sudo -v  # 检查sudo权限
```

### 诊断命令

```bash
# 全面诊断
ais --debug --version

# 检查配置
ais config show

# 检查环境
echo "Python: $(python3 --version)"
echo "pipx: $(pipx --version 2>/dev/null || echo 'Not installed')"
echo "Docker: $(docker --version 2>/dev/null || echo 'Not installed')"
echo "PATH: $PATH"
```

### 重新安装

```bash
# 完全清理并重新安装
# 1. 卸载
pipx uninstall ais-terminal  # 或使用其他卸载方式

# 2. 清理配置
rm -rf ~/.config/ais

# 3. 重新安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
```

### 卸载

```bash
# pipx安装的卸载
pipx uninstall ais-terminal  # 用户级
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx uninstall ais-terminal  # 全局

# Docker卸载
docker stop ais-daemon && docker rm ais-daemon
docker rmi ais-terminal:latest

# 系统级安装卸载
# （使用专用卸载脚本）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/uninstall.sh | bash
```

## 📚 更多资源

- [🐳 Docker部署指南](DOCKER_GUIDE.md)
- [🛠️ 开发环境设置](DEVELOPMENT.md)
- [🏢 企业部署指南](DEPLOYMENT_GUIDE.md)
- [🔧 配置指南](CONFIGURATION.md)
- [📊 性能优化](PERFORMANCE.md)

## 🆘 获得帮助

### 自助诊断
```bash
# 一键诊断
ais doctor  # 自动检查常见问题

# 详细诊断
ais --debug --version
ais config doctor
```

### 社区支持
1. 💬 [GitHub Discussions](https://github.com/kangvcar/ais/discussions) - 交流和问答
2. 🐛 [GitHub Issues](https://github.com/kangvcar/ais/issues) - 报告bug
3. 📚 [Wiki](https://github.com/kangvcar/ais/wiki) - 详细文档
4. 📧 [Email Support](mailto:ais@example.com) - 直接联系

### 报告问题时请提供
- 操作系统和版本
- Python版本 (`python3 --version`)
- AIS版本 (`ais --version`)
- 安装方式（pipx/Docker/源码）
- 完整错误信息
- 复现步骤

---

🎉 **快乐使用 AIS！** 如果觉得有用，请给我们点个⭐️！