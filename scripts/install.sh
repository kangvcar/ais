#!/bin/bash
# AIS - AI智能终端助手
# 智能安装脚本 - 统一推荐pipx安装
# 
# 推荐安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
# 用户安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --user
# 系统安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system
# 
# GitHub: https://github.com/kangvcar/ais

set -e  # 遇到错误立即退出

# 版本信息
AIS_VERSION="latest"
GITHUB_REPO="kangvcar/ais"

# 安装选项
NON_INTERACTIVE=0
INSTALL_MODE="auto"  # auto, user, system, container
SKIP_CHECKS=0

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印彩色消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检测系统环境
detect_environment() {
    if [ -n "${CONTAINER}" ] || [ -n "${container}" ] || [ -f /.dockerenv ]; then
        echo "container"
    elif [ "$EUID" -eq 0 ] && [ -n "$SUDO_USER" ]; then
        echo "sudo"
    elif [ "$EUID" -eq 0 ]; then
        echo "root"
    else
        echo "user"
    fi
}

# 安装pipx
install_pipx() {
    print_info "📦 安装pipx..."
    
    if command_exists pipx; then
        print_success "pipx已安装"
        return 0
    fi
    
    # 根据系统安装pipx
    if command_exists apt-get; then
        if [ "$(detect_environment)" = "user" ]; then
            sudo apt update && sudo apt install -y python3-pipx
        else
            apt update && apt install -y python3-pipx
        fi
    elif command_exists yum; then
        if [ "$(detect_environment)" = "user" ]; then
            sudo yum install -y python3-pipx
        else
            yum install -y python3-pipx
        fi
    elif command_exists brew; then
        brew install pipx
    else
        # 使用pip安装pipx
        if [ "$(detect_environment)" = "user" ]; then
            python3 -m pip install --user pipx
        else
            python3 -m pip install pipx
        fi
    fi
    
    # 确保pipx在PATH中
    python3 -m pipx ensurepath >/dev/null 2>&1 || true
    
    if command_exists pipx; then
        print_success "pipx安装成功"
    else
        print_error "pipx安装失败"
        return 1
    fi
}

# 健康检查
health_check() {
    print_info "🔍 执行安装后健康检查..."
    
    # 检查ais命令
    if ! command_exists ais; then
        print_error "ais命令未找到"
        return 1
    fi
    
    # 检查版本
    VERSION=$(ais --version 2>/dev/null | head -n1) || {
        print_error "无法获取ais版本信息"
        return 1
    }
    
    print_success "ais命令可用: $VERSION"
    
    # 测试基本功能
    if ais config --help >/dev/null 2>&1; then
        print_success "基本功能测试通过"
    else
        print_warning "基本功能测试失败，但安装可能仍然成功"
    fi
    
    return 0
}

# 用户级安装
install_user_mode() {
    print_info "👤 开始用户级pipx安装..."
    
    # 安装pipx
    install_pipx || exit 1
    
    # 安装AIS
    print_info "📦 安装ais-terminal..."
    pipx install ais-terminal
    
    # 设置shell集成
    print_info "🔧 设置shell集成..."
    ais setup >/dev/null 2>&1 || print_warning "shell集成设置可能需要手动完成"
    
    print_success "✅ 用户级安装完成！"
    print_info "💡 如需为其他用户安装，请使用: $0 --system"
}

# 系统级安装
install_system_mode() {
    print_info "🏢 开始系统级pipx安装..."
    
    # 安装pipx
    install_pipx || exit 1
    
    # 创建系统级pipx环境
    export PIPX_HOME=/opt/pipx
    export PIPX_BIN_DIR=/usr/local/bin
    
    # 安装AIS
    print_info "📦 安装ais-terminal到系统位置..."
    if [ "$(detect_environment)" = "user" ]; then
        sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal
    else
        pipx install ais-terminal
    fi
    
    # 确保所有用户可访问
    if [ "$(detect_environment)" = "user" ]; then
        sudo chmod +x /usr/local/bin/ais 2>/dev/null || true
    else
        chmod +x /usr/local/bin/ais 2>/dev/null || true
    fi
    
    print_success "✅ 系统级安装完成！所有用户都可以使用ais命令"
    print_info "💡 用户可以运行: ais setup 来设置shell集成"
}

# 容器化安装
install_container_mode() {
    print_info "🐳 开始容器化安装..."
    
    # 在容器中使用简单的pip安装
    print_info "📦 在容器中安装ais-terminal..."
    python3 -m pip install --break-system-packages ais-terminal
    
    # 创建全局可用的ais命令
    if [ -w "/usr/local/bin" ]; then
        cat > /usr/local/bin/ais << 'EOF'
#!/usr/bin/env python3
import sys
from ais.cli.main import main
if __name__ == '__main__':
    sys.exit(main())
EOF
        chmod +x /usr/local/bin/ais
    fi
    
    print_success "✅ 容器化安装完成！"
    print_info "💡 容器内直接使用: ais --version"
}

# 主安装函数
main() {
    echo "================================================"
    echo "         AIS - AI 智能终端助手 安装器"
    echo "================================================"
    echo "版本: $AIS_VERSION"
    echo "GitHub: https://github.com/$GITHUB_REPO"
    echo
    
    ENV=$(detect_environment)
    print_info "🔍 检测到环境: $ENV"
    
    # 自动选择最佳安装模式
    if [ "$INSTALL_MODE" = "auto" ]; then
        case "$ENV" in
            "container")
                INSTALL_MODE="container"
                print_info "🐳 容器环境：使用容器化安装"
                ;;
            "root"|"sudo")
                INSTALL_MODE="system"
                print_info "🏢 管理员环境：使用系统级pipx安装"
                ;;
            "user")
                INSTALL_MODE="user"
                print_info "👤 用户环境：使用用户级pipx安装"
                ;;
        esac
    fi
    
    # 执行对应的安装模式
    case "$INSTALL_MODE" in
        "user")
            install_user_mode
            ;;
        "system")
            install_system_mode
            ;;
        "container")
            install_container_mode
            ;;
        *)
            print_error "未知的安装模式: $INSTALL_MODE"
            exit 1
            ;;
    esac
    
    # 执行健康检查
    if [ "$SKIP_CHECKS" != "1" ]; then
        health_check || {
            print_warning "健康检查失败，但安装可能成功。请手动验证:"
            print_info "  运行: ais --version"
            print_info "  测试: ais ask 'hello'"
        }
    fi
}

# 处理命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --user)
            INSTALL_MODE="user"
            shift
            ;;
        --system)
            INSTALL_MODE="system"
            shift
            ;;
        --container)
            INSTALL_MODE="container"
            shift
            ;;
        --non-interactive)
            NON_INTERACTIVE=1
            shift
            ;;
        --skip-checks)
            SKIP_CHECKS=1
            shift
            ;;
        --help)
            echo "AIS 智能安装脚本"
            echo
            echo "用法: $0 [选项]"
            echo
            echo "安装模式:"
            echo "  (无参数)          自动检测环境并选择最佳安装方式"
            echo "  --user           用户级pipx安装（推荐个人使用）"
            echo "  --system         系统级pipx安装（推荐多用户环境）"
            echo "  --container      容器化安装（适用于Docker等）"
            echo
            echo "其他选项:"
            echo "  --non-interactive  非交互模式，适用于CI/CD环境"
            echo "  --skip-checks      跳过安装后健康检查"
            echo "  --help            显示此帮助信息"
            echo
            echo "安装示例:"
            echo "  个人安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash"
            echo "  系统安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system"
            echo "  容器安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --container"
            echo
            echo "💡 推荐使用pipx进行安装，提供最佳的安全性和可维护性"
            exit 0
            ;;
        *)
            print_error "未知选项: $1"
            print_info "使用 --help 查看帮助"
            exit 1
            ;;
    esac
done

# 运行主函数
main