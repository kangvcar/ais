# 安装指南

本文档将指导您完成 AIS 的安装过程。AIS 支持多种安装方式，您可以根据自己的需求选择最适合的方案。

## 系统要求

在开始安装之前，请确保您的系统满足以下要求：

### 操作系统
- **Linux**: Ubuntu 18.04+, CentOS 7+, Debian 10+, 或其他现代 Linux 发行版
- **macOS**: macOS 10.15+ (Catalina)
- **Windows**: Windows 10+ (通过 WSL2)

### Python 版本
- Python 3.8 或更高版本
- pip 包管理器

### Shell 环境
- Bash 4.0+ 或 Zsh 5.0+
- 终端支持 ANSI 颜色代码

## 安装方法

### 方法一：使用 pip 安装（推荐）

这是最简单和推荐的安装方式：

```bash
# 安装 AIS
pip install ais-terminal

# 验证安装
ais --version
```

### 方法二：使用 uv 安装（推荐，速度更快）

如果您使用 uv 包管理器，可以获得更快的安装速度：

```bash
# 如果还没有安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 使用 uv 安装 AIS
uv pip install ais-terminal

# 验证安装
ais --version
```

### 方法三：从源码安装

如果您想使用最新的开发版本：

```bash
# 克隆仓库
git clone https://github.com/kangvcar/ais.git
cd ais

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或者在 Windows 上: .venv\Scripts\activate

# 安装依赖并安装 AIS
pip install -e .

# 验证安装
ais --version
```

### 方法四：使用 Docker

如果您熟悉 Docker，可以使用容器方式运行：

```bash
# 拉取 Docker 镜像
docker pull kangvcar/ais:latest

# 运行 AIS 容器
docker run -it --rm kangvcar/ais:latest

# 或者使用 docker-compose
git clone https://github.com/kangvcar/ais.git
cd ais
docker-compose up -d
```

## 验证安装

安装完成后，您可以通过以下命令验证 AIS 是否正确安装：

```bash
# 检查版本
ais --version

# 查看帮助信息
ais --help

# 测试基本功能
ais ask "Hello AIS"
```

如果看到版本信息和帮助信息，说明安装成功！

## 常见问题

### 权限问题

如果在安装过程中遇到权限问题：

```bash
# 使用 --user 标志安装到用户目录
pip install --user ais-terminal

# 或者使用 sudo（不推荐）
sudo pip install ais-terminal
```

### Python 版本问题

如果系统默认 Python 版本过低：

```bash
# 检查 Python 版本
python --version
python3 --version

# 使用 python3 和 pip3
python3 -m pip install ais-terminal
```

### 网络问题

如果遇到网络连接问题：

```bash
# 使用国内镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple ais-terminal

# 或者使用阿里云镜像
pip install -i https://mirrors.aliyun.com/pypi/simple ais-terminal
```

### 虚拟环境问题

建议在虚拟环境中安装 AIS：

```bash
# 创建虚拟环境
python -m venv ais-env

# 激活虚拟环境
source ais-env/bin/activate  # Linux/macOS
# ais-env\Scripts\activate  # Windows

# 在虚拟环境中安装
pip install ais-terminal
```

## 升级和卸载

### 升级 AIS

```bash
# 升级到最新版本
pip install --upgrade ais-terminal

# 或者使用 uv
uv pip install --upgrade ais-terminal
```

### 卸载 AIS

```bash
# 卸载 AIS
pip uninstall ais-terminal

# 清理配置文件（可选）
rm -rf ~/.config/ais
```

## 下一步

安装完成后，建议您：

1. 阅读[首次配置指南](./initial-setup.md)
2. 查看[基本使用教程](./basic-usage.md)
3. 了解[常见问题解答](./faq.md)

## 获取帮助

如果在安装过程中遇到问题，可以：

- 查看[故障排除指南](../guide/troubleshooting.md)
- 在 [GitHub Issues](https://github.com/kangvcar/ais/issues) 中提问
- 查看[常见问题解答](./faq.md)

---

::: tip 提示
建议在安装后立即进行[首次配置](./initial-setup.md)，这将帮助您快速开始使用 AIS。
:::

::: warning 注意
请确保您的系统满足所有系统要求，否则可能会遇到兼容性问题。
:::