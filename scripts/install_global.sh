#!/bin/bash
# AIS 智能终端助手 - 改进的全局安装脚本
# 解决用户权限和全局可用性问题

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# 获取当前用户信息
CURRENT_USER=${SUDO_USER:-$USER}
CURRENT_HOME=$(eval echo "~$CURRENT_USER")

echo "================================================"
echo "      AIS - AI 智能终端助手 全局安装器"
echo "================================================"
echo "解决虚拟环境限制，实现真正的全局安装"
echo

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
    print_error "此脚本需要 root 权限以实现全局安装"
    print_info "请使用: sudo $0"
    exit 1
fi

print_info "开始全局安装 AIS..."
print_info "目标用户: $CURRENT_USER"
print_info "用户主目录: $CURRENT_HOME"

# 1. 检查并安装系统依赖
print_info "步骤 1/7: 检查系统依赖..."
if command -v apt-get >/dev/null 2>&1; then
    apt-get update >/dev/null 2>&1
    apt-get install -y python3 python3-pip python3-venv curl >/dev/null 2>&1
elif command -v yum >/dev/null 2>&1; then
    yum install -y python3 python3-pip curl >/dev/null 2>&1
elif command -v pacman >/dev/null 2>&1; then
    pacman -Sy --noconfirm python python-pip curl >/dev/null 2>&1
fi
print_success "系统依赖检查完成"

# 2. 创建系统目录结构
print_info "步骤 2/7: 创建系统目录结构..."
mkdir -p /opt/ais
mkdir -p /usr/local/share/ais
mkdir -p /etc/ais

# 3. 安装AIS到系统位置
print_info "步骤 3/7: 安装 AIS 到系统位置..."
cd /opt/ais

# 创建系统级虚拟环境
python3 -m venv venv
source venv/bin/activate

# 升级pip并安装AIS
pip install --upgrade pip >/dev/null 2>&1

# 从PyPI安装最新版本
if pip install ais-terminal >/dev/null 2>&1; then
    print_success "从 PyPI 安装 AIS 成功"
else
    print_warning "PyPI 安装失败，尝试从本地安装..."
    if [ -f "$OLDPWD/pyproject.toml" ]; then
        pip install -e "$OLDPWD" >/dev/null 2>&1
        print_success "从本地源码安装成功"
    else
        print_error "无法安装 AIS"
        exit 1
    fi
fi

# 4. 创建全局启动脚本
print_info "步骤 4/7: 创建全局命令..."
cat > /usr/local/bin/ais << 'EOF'
#!/bin/bash
# AIS 全局启动脚本 - 无虚拟环境限制

# 设置环境变量
export AIS_SYSTEM_INSTALL=1
export PYTHONPATH="/opt/ais/venv/lib/python*/site-packages:$PYTHONPATH"

# 直接执行ais（使用系统Python环境）
exec /opt/ais/venv/bin/ais "$@"
EOF

chmod +x /usr/local/bin/ais

# 验证全局命令
if command -v ais >/dev/null 2>&1; then
    print_success "全局命令创建成功: $(which ais)"
else
    print_error "全局命令创建失败"
    exit 1
fi

# 5. 创建系统级配置
print_info "步骤 5/7: 创建系统配置..."
cat > /etc/ais/config.toml << 'EOF'
# AIS 系统级默认配置
default_provider = "default_free"
auto_analysis = true
context_level = "standard"
sensitive_dirs = ["~/.ssh", "~/.config/ais", "~/.aws"]

[providers.default_free]
base_url = "https://api.deepbricks.ai/v1/chat/completions"
model_name = "gpt-4o-mini"
api_key = "sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg"
EOF

chmod 644 /etc/ais/config.toml

# 6. 设置Shell集成脚本
print_info "步骤 6/7: 配置 Shell 集成..."

# 运行ais setup-shell来创建集成脚本
/usr/local/bin/ais setup-shell >/dev/null 2>&1 || true

# 创建全局Shell集成
cat > /etc/profile.d/ais.sh << 'EOF'
# AIS - AI 智能终端助手全局集成

# 确保ais命令在PATH中
export PATH="/usr/local/bin:$PATH"

# 加载AIS shell集成（尝试多个可能的位置）
AIS_INTEGRATION_PATHS=(
    "/opt/ais/venv/lib/python*/site-packages/ais/shell/integration.sh"
    "/usr/local/share/ais/integration.sh"
    "~/.local/share/ais/integration.sh"
)

for path in "${AIS_INTEGRATION_PATHS[@]}"; do
    # 展开通配符和用户目录
    for expanded_path in $(eval echo $path); do
        if [ -f "$expanded_path" ]; then
            source "$expanded_path"
            break 2
        fi
    done
done
EOF

chmod 644 /etc/profile.d/ais.sh

# 7. 为当前用户设置Shell集成
print_info "步骤 7/7: 为用户 $CURRENT_USER 设置 Shell 集成..."

# 检测用户使用的Shell
USER_SHELL=$(getent passwd "$CURRENT_USER" | cut -d: -f7)
SHELL_NAME=$(basename "$USER_SHELL")

# 为用户的shell配置文件添加集成
case "$SHELL_NAME" in
    "bash")
        CONFIG_FILE="$CURRENT_HOME/.bashrc"
        ;;
    "zsh")
        CONFIG_FILE="$CURRENT_HOME/.zshrc"
        ;;
    *)
        CONFIG_FILE="$CURRENT_HOME/.bashrc"
        ;;
esac

# 移除旧的集成配置
if [ -f "$CONFIG_FILE" ]; then
    sed -i '/# START AIS INTEGRATION/,/# END AIS INTEGRATION/d' "$CONFIG_FILE" 2>/dev/null || true
fi

# 添加新的集成配置
cat >> "$CONFIG_FILE" << 'EOF'

# START AIS INTEGRATION
# AIS - AI 智能终端助手
if [ -f "/etc/profile.d/ais.sh" ]; then
    source "/etc/profile.d/ais.sh"
fi
# END AIS INTEGRATION
EOF

# 修改文件所有者为实际用户
chown "$CURRENT_USER:$(id -gn "$CURRENT_USER")" "$CONFIG_FILE" 2>/dev/null || true

# 8. 测试安装
print_info "测试安装结果..."

# 测试ais命令
if /usr/local/bin/ais --version >/dev/null 2>&1; then
    VERSION=$(/usr/local/bin/ais --version 2>/dev/null | head -n1)
    print_success "AIS 命令测试成功: $VERSION"
else
    print_error "AIS 命令测试失败"
    exit 1
fi

# 设置正确的权限
chown -R root:root /opt/ais
chmod -R 755 /opt/ais
chmod 755 /usr/local/bin/ais

echo
print_success "🎉 AIS 全局安装完成！"
echo
print_info "📋 安装详情:"
print_info "  • 全局命令: /usr/local/bin/ais"
print_info "  • 程序目录: /opt/ais"
print_info "  • 系统配置: /etc/ais/config.toml"
print_info "  • Shell集成: /etc/profile.d/ais.sh"
print_info "  • 用户配置: $CONFIG_FILE"
echo
print_info "🔧 立即生效:"
print_info "  重新加载Shell配置: source $CONFIG_FILE"
print_info "  或者重新打开终端"
echo
print_warning "🧪 测试自动分析:"
print_warning "  执行错误命令: mkdirr /tmp/test"
print_warning "  应该会自动显示AI分析"
echo
print_info "📚 常用命令:"
print_info "  ais config                - 查看配置"
print_info "  ais ask '你的问题'        - 向AI提问"
print_info "  ais setup-shell           - 重新设置Shell集成"
print_info "  ais --help               - 查看完整帮助"
echo

# 为当前会话加载配置（如果可能）
if [ -n "$SUDO_USER" ]; then
    print_info "💡 提示: 当前会话需要手动加载配置："
    print_info "  su - $SUDO_USER  # 切换到用户"
    print_info "  source $CONFIG_FILE  # 加载配置"
fi

print_success "安装完成！现在所有用户都可以使用 'ais' 命令了。"