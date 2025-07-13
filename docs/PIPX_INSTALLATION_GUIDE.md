# AIS pipx 安装完整指南

## 🎯 pipx安装选项

### 1. 个人使用（用户级安装）
```bash
# 安装pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# 安装AIS（仅当前用户可用）
pipx install ais-terminal

# 设置shell集成
ais setup
```

**特点：**
- ✅ 安全隔离，无需sudo
- ✅ 版本管理简单
- ❌ 仅当前用户可用
- ❌ 其他用户需要各自安装

### 2. 多用户环境（pipx全局安装）
```bash
# 安装pipx（如果没有）
sudo apt install pipx  # Ubuntu/Debian
# 或
sudo python3 -m pip install pipx

# 设置全局路径
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx ensurepath

# 全局安装AIS（所有用户可用）
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal

# 为当前用户设置shell集成
ais setup
```

**特点：**
- ✅ 所有用户都可以使用
- ✅ 保持虚拟环境隔离
- ✅ 比系统级pip安装更安全
- ⚠️ 需要sudo权限

### 3. 混合模式（推荐）
```bash
# 系统管理员全局安装基础版本
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal

# 个人用户可以安装自己的版本（如果需要特定版本）
pipx install ais-terminal==specific-version
```

## 🔄 多用户使用场景

### 场景1：开发团队（每人自己安装）
```bash
# 团队成员A
alice@dev:~$ pipx install ais-terminal
alice@dev:~$ ais setup

# 团队成员B  
bob@dev:~$ pipx install ais-terminal
bob@dev:~$ ais setup

# 优势：每人可以使用不同版本，互不干扰
```

### 场景2：服务器环境（全局安装）
```bash
# 系统管理员安装
admin@server:~$ sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal

# 所有用户都可以使用
user1@server:~$ ais --version  ✅
user2@server:~$ ais ask "help"  ✅
user3@server:~$ mkdirr test    ✅ (自动分析)
```

### 场景3：CI/CD环境
```bash
# 在Docker/CI中使用全局安装
RUN python3 -m pip install pipx && \
    PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal && \
    PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx ensurepath

# 或使用常规pip在容器中
RUN pip install ais-terminal
```

## 🛠️ pipx vs 其他安装方式对比

| 特性 | pipx用户级 | pipx全局 | pip全局 | 系统安装脚本 |
|------|------------|----------|---------|-------------|
| **隔离性** | 🟢 完全 | 🟢 完全 | ❌ 无 | 🟡 部分 |
| **多用户** | ❌ 否 | ✅ 是 | ✅ 是 | ✅ 是 |
| **权限要求** | 🟢 普通用户 | ⚠️ sudo | ⚠️ sudo | ⚠️ sudo |
| **版本管理** | 🟢 简单 | 🟢 简单 | ❌ 复杂 | ❌ 复杂 |
| **安全性** | 🟢 高 | 🟡 中高 | ❌ 低 | 🟡 中 |
| **卸载难度** | 🟢 简单 | 🟢 简单 | ❌ 困难 | ❌ 困难 |

## 💡 推荐策略

### 个人开发者
```bash
pipx install ais-terminal
```

### 企业/团队环境
```bash
# 选择1：统一全局安装
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal

# 选择2：每人自己安装（推荐）
# 在团队文档中说明安装方法
echo "pipx install ais-terminal" > team-setup.sh
```

### 服务器运维
```bash
# 如果需要最高安全性
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal

# 如果需要深度系统集成
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
```

## 🔧 故障排除

### 问题1：pipx命令不存在
```bash
# 解决方案
python3 -m pip install --user pipx
python3 -m pipx ensurepath
# 重新启动终端或 source ~/.bashrc
```

### 问题2：全局安装权限问题
```bash
# 确保pipx全局路径设置
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx ensurepath

# 检查路径
echo $PATH | grep "/usr/local/bin"
```

### 问题3：多版本冲突
```bash
# 查看已安装版本
pipx list

# 卸载重装
pipx uninstall ais-terminal
pipx install ais-terminal
```

## 📋 总结

**pipx的核心优势：**
- 🔒 虚拟环境隔离，避免依赖冲突
- 🎯 专为CLI应用设计
- 🛡️ 比系统级pip安装更安全
- 🔄 支持用户级和全局级安装
- 🧹 卸载干净，不留残留

**推荐使用pipx的场景：**
- ✅ 个人开发环境
- ✅ 需要版本隔离的团队
- ✅ 安全要求较高的环境
- ✅ 符合Python最佳实践的项目