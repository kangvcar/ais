# AIS 安装指南

本文档提供了AIS（AI-powered terminal assistant）的详细安装指南，涵盖所有安装方式和使用场景。

## 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: Linux, macOS, Windows
- **网络**: 需要网络连接以下载依赖和AI服务

## 🎯 推荐安装方式

### 个人使用（最佳实践）

使用pipx进行用户级安装，安全且符合Python最佳实践：

```bash
# 1. 安装pipx（如果没有）
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# 2. 安装AIS
pipx install ais-terminal

# 3. 设置shell集成
ais setup-shell
```

**优势：**
- ✅ 安全隔离，独立虚拟环境
- ✅ 无需sudo权限
- ✅ 版本管理简单
- ✅ 符合Python生态标准

### 多用户环境（推荐）

使用pipx全局安装，兼顾安全性和多用户支持：

```bash
# 1. 安装pipx（如果没有）
sudo apt install pipx  # Ubuntu/Debian
# 或 sudo yum install python3-pipx  # CentOS/RHEL
# 或 sudo pip install pipx  # 通用方式

# 2. 全局安装AIS
sudo pipx install --global ais-terminal

# 3. 每个用户设置shell集成
ais setup-shell
```

**优势：**
- ✅ 所有用户都可以使用
- ✅ 保持虚拟环境隔离
- ✅ 比系统级安装更安全
- ✅ 管理和升级简单

## 🔧 其他安装方式

### 智能安装脚本

自动检测环境并提供最佳安装选择：

```bash
# 运行智能安装脚本
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

# 脚本会检测pipx并提供选择：
# 1. pipx用户级安装
# 2. pipx全局安装（推荐）
# 3. 传统系统级安装
```

### 系统级安装（运维环境）

适用于深度系统集成的场景：

```bash
# 全局安装脚本（传统方式）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system-install
```

### 开发环境安装

在项目虚拟环境中安装：

```bash
# 在已激活的虚拟环境中
pip install ais-terminal
```

### 从源码安装

开发者或需要最新功能：

```bash
# 克隆仓库
git clone https://github.com/kangvcar/ais.git
cd ais

# 使用pipx安装
pipx install -e .

# 或在虚拟环境中安装
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -e .
```

## 📊 安装方式对比

| 安装方式 | 安全性 | 多用户 | 管理难度 | 权限需求 | 推荐度 | 适用场景 |
|---------|-------|-------|---------|---------|--------|----------|
| **pipx用户级** | 🟢 最高 | ❌ 否 | 🟢 最简单 | 普通用户 | ⭐⭐⭐⭐⭐ | 个人开发 |
| **pipx全局** | 🟢 高 | ✅ 是 | 🟢 简单 | sudo | ⭐⭐⭐⭐⭐ | 多用户环境 |
| **系统全局** | 🟡 中等 | ✅ 是 | 🟡 中等 | sudo | ⭐⭐⭐ | 运维环境 |
| **项目级** | 🟢 高 | ❌ 否 | 🟢 简单 | 普通用户 | ⭐⭐⭐ | 开发测试 |
| **源码安装** | 🟡 中等 | 看情况 | 🟡 复杂 | 看情况 | ⭐⭐ | 开发贡献 |

## 🔧 安装后配置

### Shell集成设置

无论使用哪种安装方式，都建议设置shell集成以启用自动错误分析：

```bash
# 自动设置shell集成
ais setup-shell

# 手动加载（可选）
source ~/.bashrc  # Bash
source ~/.zshrc   # Zsh
```

### 验证安装

```bash
# 检查版本
ais --version

# 测试基本功能
ais ask "Hello"

# 测试自动错误分析
mkdirr /tmp/test  # 故意输错命令
```

## 🛠️ 故障排除

### 常见问题

#### 1. pipx命令不存在
```bash
# 安装pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# 重新加载shell配置
source ~/.bashrc
```

#### 2. ais命令找不到
```bash
# 检查PATH
echo $PATH

# pipx用户级安装
export PATH="$HOME/.local/bin:$PATH"

# pipx全局安装
echo $PATH | grep "/usr/local/bin"
```

#### 3. 权限问题
```bash
# 避免使用sudo pip
# 使用pipx或--user参数
python3 -m pip install --user ais-terminal
```

#### 4. 依赖冲突
```bash
# 使用pipx解决依赖冲突
pipx install ais-terminal

# 或创建独立虚拟环境
python3 -m venv ais-env
source ais-env/bin/activate
pip install ais-terminal
```

### 卸载

#### pipx安装的卸载
```bash
# 用户级
pipx uninstall ais-terminal

# 全局级
sudo pipx uninstall --global ais-terminal
```

#### 系统级安装的卸载
```bash
# 使用卸载脚本
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/uninstall.sh | bash
```

## 📚 更多资源

- [pipx安装详细指南](PIPX_INSTALLATION_GUIDE.md)
- [安装策略分析](INSTALLATION_STRATEGY.md)
- [多用户配置](../README.md#多用户环境)
- [开发环境设置](../CONTRIBUTING.md)

## 🆘 获得帮助

如果遇到安装问题：

1. 查看 [GitHub Issues](https://github.com/kangvcar/ais/issues)
2. 运行 `ais --debug` 获取诊断信息
3. 提交issue时请包含：
   - 操作系统和版本
   - Python版本
   - 安装方式
   - 错误信息