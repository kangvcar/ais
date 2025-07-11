# AIS 安装指南

本文档提供了AIS（AI-powered terminal assistant）的详细安装指南，适用于不同操作系统和使用场景。

## 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: Linux, macOS, Windows
- **网络**: 需要网络连接以下载依赖和AI服务

## 安装方法

### 1. PyPI 安装（推荐）

最简单的安装方式，适用于所有平台：

```bash
# 使用 pip 安装
pip install ais

# 或使用 pipx（推荐，避免依赖冲突）
pipx install ais
```

**优点**：
- 一键安装，快速便捷
- 自动处理依赖关系
- 支持自动更新

**注意事项**：
- 需要确保 Python 和 pip 已正确安装
- 如果遇到权限问题，可以使用 `--user` 参数

### 2. Homebrew 安装（macOS/Linux）

适用于 macOS 和 Linux 用户：

```bash
# 安装 Homebrew（如果尚未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 AIS
brew install ais
```

**优点**：
- 系统级包管理
- 自动处理依赖和更新
- 与系统环境良好集成

**注意事项**：
- 需要先安装 Homebrew
- 首次发布后才可使用

### 3. Windows PowerShell 安装

Windows 用户的专用安装方式：

```powershell
# 方法1: 一键安装（推荐）
iwr -useb https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.ps1 | iex

# 方法2: 下载后运行
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.ps1" -OutFile "install.ps1"
.\install.ps1

# 方法3: 带参数安装
.\install.ps1 -InstallMethod pip -GlobalInstall
```

**安装选项**：
- `-InstallMethod`: 安装方式（pip/source/local）
- `-GlobalInstall`: 全局安装（需要管理员权限）
- `-NoShellIntegration`: 跳过 PowerShell 集成

**特色功能**：
- 自动检测 Python 环境
- 智能处理权限问题
- 自动配置 PowerShell 集成

### 4. 一键安装脚本（Linux/macOS）

适用于 Linux 和 macOS 的快速安装：

```bash
# 标准安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

# 从源码安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --from-source

# 本地安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --local
```

**安装选项**：
- `--from-source`: 从 GitHub 源码安装
- `--local`: 本地开发安装
- `--no-shell-integration`: 跳过 Shell 集成

### 5. 手动安装

适用于开发者或需要定制安装的用户：

```bash
# 克隆仓库
git clone https://github.com/kangvcar/ais.git
cd ais

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -e .

# 测试安装
ais --version
```

## 安装后配置

### Shell 集成

AIS 支持自动错误分析，需要配置 Shell 集成：

#### Bash 集成

```bash
# 添加到 ~/.bashrc
echo 'source /path/to/ais/scripts/shell/integration.sh' >> ~/.bashrc
source ~/.bashrc
```

#### Zsh 集成

```bash
# 添加到 ~/.zshrc
echo 'source /path/to/ais/scripts/shell/integration.sh' >> ~/.zshrc
source ~/.zshrc
```

#### PowerShell 集成

PowerShell 集成会在安装过程中自动配置。如需手动配置：

```powershell
# 编辑 PowerShell 配置文件
notepad $PROFILE

# 添加以下内容
. (Join-Path (Split-Path $PROFILE) "ais_integration.ps1")
```

### 初始配置

首次使用需要配置 AI 服务：

```bash
# 运行配置向导
ais config

# 或手动设置
ais config set ai_provider openai
ais config set api_key your_api_key
```

## 验证安装

运行以下命令验证安装是否成功：

```bash
# 检查版本
ais --version

# 查看帮助
ais --help

# 测试基本功能
ais ask "如何使用 git"

# 测试错误分析（故意输入错误命令）
nonexistent_command
```

## 常见问题

### Python 版本问题

**问题**: `ModuleNotFoundError: No module named 'ais'`

**解决方案**:
```bash
# 检查 Python 版本
python --version

# 确保使用正确的 Python
python3 -m pip install ais
```

### 权限问题

**问题**: `Permission denied` 或 `Access denied`

**解决方案**:
```bash
# Linux/macOS
sudo pip install ais
# 或
pip install --user ais-cli

# Windows
# 以管理员身份运行 PowerShell
```

### 网络问题

**问题**: 安装时网络连接失败

**解决方案**:
```bash
# 使用国内镜像
pip install -i https://mirrors.aliyun.com/pypi/simple/ ais-cli

# 或配置代理
pip install --proxy http://proxy.example.com:8080 ais-cli
```

### Shell 集成问题

**问题**: 错误分析功能不工作

**解决方案**:
1. 检查 Shell 集成是否正确配置
2. 重新启动终端
3. 检查 AIS 是否在 PATH 中
4. 运行 `ais config` 检查配置

## 卸载

如需卸载 AIS：

```bash
# PyPI 安装的卸载
pip uninstall ais

# Homebrew 安装的卸载
brew uninstall ais

# 使用卸载脚本
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/uninstall.sh | bash
```

## 更新

更新到最新版本：

```bash
# PyPI 更新
pip install --upgrade ais

# Homebrew 更新
brew upgrade ais

# 检查更新
ais --version
```

## 获取帮助

如果遇到安装问题，可以通过以下方式获取帮助：

1. 查看 [常见问题](https://github.com/kangvcar/ais/issues)
2. 提交 [Issue](https://github.com/kangvcar/ais/issues/new)
3. 参与 [讨论](https://github.com/kangvcar/ais/discussions)

## 下一步

安装完成后，建议阅读：
- [用户指南](README.md)
- [配置说明](CONFIG.md)
- [部署指南](DEPLOYMENT_GUIDE.md)