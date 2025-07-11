#!/bin/bash
# AIS 系统级全局安装脚本
# 支持所有用户使用，无权限问题

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
print_step() { echo -e "${BLUE}📋 第$1步: $2${NC}"; }

# 检查是否以root权限运行
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "此脚本需要 root 权限运行"
        print_info "请使用: sudo $0"
        exit 1
    fi
}

# 检查并安装系统依赖
install_system_deps() {
    print_info "检查系统依赖..."
    
    if command -v apt-get >/dev/null 2>&1; then
        apt-get update
        apt-get install -y python3 python3-pip python3-venv git curl
    elif command -v yum >/dev/null 2>&1; then
        yum install -y python3 python3-pip git curl
    elif command -v pacman >/dev/null 2>&1; then
        pacman -Sy --noconfirm python python-pip git curl
    else
        print_warning "未知包管理器，请手动安装 Python 3.8+, pip, git, curl"
    fi
    
    print_success "系统依赖检查完成"
}

# 创建系统用户和目录结构
setup_system_structure() {
    print_info "设置系统目录结构..."
    
    # 创建系统目录
    mkdir -p /opt/ais
    mkdir -p /usr/local/share/ais
    mkdir -p /etc/ais
    
    # 创建ais系统用户（如果不存在）
    if ! id "ais" >/dev/null 2>&1; then
        useradd -r -d /opt/ais -s /bin/false -c "AIS System User" ais
        print_info "创建系统用户: ais"
    fi
    
    print_success "系统目录结构创建完成"
}

# 安装AIS到系统位置
install_ais_system() {
    print_info "安装 AIS 到系统位置..."
    
    # 创建虚拟环境
    cd /opt/ais
    python3 -m venv venv
    source venv/bin/activate
    
    # 安装依赖
    pip install --upgrade pip
    
    # 从当前目录安装（如果存在pyproject.toml）或从GitHub安装
    if [ -f "$OLDPWD/pyproject.toml" ]; then
        print_info "从本地源码安装..."
        pip install -e "$OLDPWD"
        # 复制shell集成脚本
        cp -r "$OLDPWD/shell" /usr/local/share/ais/
    else
        print_info "从GitHub安装..."
        pip install git+https://github.com/kangvcar/ais.git
        # 下载shell集成脚本
        curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/shell/integration.sh \
            -o /usr/local/share/ais/integration.sh
    fi
    
    # 设置权限
    chown -R ais:ais /opt/ais
    chmod -R 755 /opt/ais
    
    print_success "AIS 系统安装完成"
}

# 创建全局启动脚本
create_global_wrapper() {
    print_info "创建全局启动脚本..."
    
    cat > /usr/local/bin/ais << 'EOF'
#!/bin/bash
# AIS 全局启动脚本

# 激活虚拟环境并运行ais
export AIS_SYSTEM_INSTALL=1
cd /opt/ais
source venv/bin/activate
exec ais "$@"
EOF
    
    chmod +x /usr/local/bin/ais
    
    # 验证全局命令
    if command -v ais >/dev/null 2>&1; then
        print_success "全局命令创建成功: $(which ais)"
    else
        print_error "全局命令创建失败"
        exit 1
    fi
}

# 创建系统级配置模板
create_system_config() {
    print_info "创建系统级配置..."
    
    cat > /etc/ais/config.toml << 'EOF'
# AIS 系统级默认配置
# 用户级配置位于 ~/.config/ais/config.toml

default_provider = "default_free"
auto_analysis = true
context_level = "standard"
sensitive_dirs = ["~/.ssh", "~/.config/ais", "~/.aws", "/etc/passwd", "/etc/shadow"]

[ui]
enable_colors = true
enable_streaming = true
max_history_display = 10

[providers.default_free]
base_url = "https://api.deepbricks.ai/v1/chat/completions"
model_name = "gpt-4o-mini"
api_key = "sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg"

[advanced]
max_context_length = 4000
async_analysis = false
cache_analysis = true
EOF
    
    chmod 644 /etc/ais/config.toml
    print_success "系统级配置创建完成"
}

# 配置所有用户的shell集成
setup_global_shell_integration() {
    print_info "配置全局shell集成..."
    
    # 创建profile.d脚本（对所有用户生效）
    cat > /etc/profile.d/ais.sh << 'EOF'
# AIS - AI 智能终端助手全局集成
# 自动对所有用户启用

# 确保ais命令在PATH中
export PATH="/usr/local/bin:$PATH"

# 加载AIS shell集成
if [ -f "/usr/local/share/ais/shell/integration.sh" ]; then
    source "/usr/local/share/ais/shell/integration.sh"
elif [ -f "/usr/local/share/ais/integration.sh" ]; then
    source "/usr/local/share/ais/integration.sh"
fi
EOF
    
    chmod 644 /etc/profile.d/ais.sh
    
    print_success "全局shell集成配置完成"
    print_info "所有新登录的用户都将自动启用AIS"
}

# 主安装函数
main() {
    echo "================================================"
    echo "      AIS - AI 智能终端助手 系统级安装器"
    echo "================================================"
    echo "此脚本将为所有用户安装AIS，需要root权限"
    echo
    
    check_root
    
    print_step 1 "检查系统环境"
    install_system_deps
    
    print_step 2 "设置系统目录结构"
    setup_system_structure
    
    print_step 3 "安装AIS到系统位置"
    install_ais_system
    
    print_step 4 "创建全局命令"
    create_global_wrapper
    
    print_step 5 "创建系统配置"
    create_system_config
    
    print_step 6 "配置全局Shell集成"
    setup_global_shell_integration
    
    print_step 7 "验证安装"
    
    # 测试ais命令
    if ais --version >/dev/null 2>&1; then
        version=$(ais --version 2>/dev/null | head -n1)
        print_success "AIS 系统安装成功: $version"
    else
        print_error "AIS 命令测试失败"
        exit 1
    fi
    
    echo
    print_success "🎉 AIS 系统级安装完成！"
    echo
    print_info "📋 安装详情:"
    print_info "  • 可执行文件: /usr/local/bin/ais"
    print_info "  • 程序目录: /opt/ais"
    print_info "  • 配置文件: /etc/ais/config.toml"
    print_info "  • Shell集成: /etc/profile.d/ais.sh"
    echo
    print_info "🔧 使用说明:"
    print_info "  • 所有用户可直接使用 'ais' 命令"
    print_info "  • 新用户登录后自动启用错误分析"
    print_info "  • 用户个人配置: ~/.config/ais/config.toml"
    echo
    print_warning "⚠️  重要:"
    print_warning "  1. 重新登录或运行: source /etc/profile.d/ais.sh"
    print_warning "  2. 测试: mkdirr /tmp/test (故意输错)"
    echo
    print_info "📚 管理命令:"
    print_info "  systemctl status ais      - 查看状态(如果配置了服务)"
    print_info "  ais config                - 查看配置"
    print_info "  ais --help               - 查看帮助"
    echo
}

# 运行主函数
main "$@"