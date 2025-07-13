#!/bin/bash
# AIS - AI智能终端助手
# 全局安装脚本 - 所有用户可用
# 
# 默认安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
# 从源码安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --from-source
# 
# GitHub: https://github.com/kangvcar/ais

set -e  # 遇到错误立即退出

# 版本信息
AIS_VERSION="latest"
GITHUB_REPO="kangvcar/ais"

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




# 主安装函数
main() {
    echo "================================================"
    echo "         AIS - AI 智能终端助手 安装器"
    echo "================================================"
    echo "版本: $AIS_VERSION"
    echo "GitHub: https://github.com/$GITHUB_REPO"
    echo
    
    # 智能安装建议
    print_info "🧠 安装方式建议:"
    if command_exists pipx; then
        print_info "  ✨ 检测到pipx，有多种安装选择:"
        print_info "  1. pipx install ais-terminal           (仅当前用户)"
        print_info "  2. sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal  (所有用户，推荐)"
        print_info "  3. 继续当前的系统级安装                    (传统方式)"
        echo
        print_warning "📋 选择安装方式 (1-3)，或按回车使用pipx全局安装:"
        read -r choice
        
        case "$choice" in
            "1")
                print_info "💡 使用pipx用户级安装:"
                print_info "   pipx install ais-terminal"
                print_info "   ais setup"
                exit 0
                ;;
            "2"|"")
                print_info "🚀 使用pipx全局安装:"
                if [ "$EUID" -eq 0 ]; then
                    print_info "   正在执行: PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal"
                    PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal
                    print_success "✅ pipx全局安装完成！所有用户都可以使用ais命令"
                    print_info "💡 用户可以运行: ais setup 来设置shell集成"
                else
                    print_info "   sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal"
                    print_info "   ais setup"
                fi
                exit 0
                ;;
            "3")
                print_info "继续使用系统级安装脚本..."
                ;;
            *)
                print_error "无效选择，继续使用系统级安装"
                ;;
        esac
    elif [ "$EUID" -ne 0 ] && [ -z "$SUDO_USER" ]; then
        print_info "  💡 个人使用推荐: pipx install ais-terminal"
        print_info "  🏢 多用户环境推荐: 当前的全局安装"
    fi
    echo
    
    # 检测安装方式 - 只支持全局安装
    if [ -f "pyproject.toml" ] && grep -q "ais" pyproject.toml 2>/dev/null; then
        INSTALL_MODE="local"
        print_info "检测到开发环境，将从当前目录全局安装"
    elif [[ "$1" == "--from-source" ]]; then
        INSTALL_MODE="source"
        print_info "将从 GitHub 源码全局安装"
    elif [[ "$1" == "--global-exec" ]]; then
        # 内部执行全局安装（已有sudo权限）
        shift  # 移除 --global-exec 参数
        INSTALL_MODE="global"
        print_info "执行全局安装..."
    else
        # 默认全局安装模式
        INSTALL_MODE="global"
        print_info "全局安装模式：为所有用户安装 AIS"
        
        # 检查权限
        if [[ "$EUID" != "0" ]] && [[ -z "$SUDO_USER" ]]; then
            print_warning "全局安装需要管理员权限"
            echo "继续安装吗？(Y/n)"
            read -r response
            if [[ "$response" =~ ^[Nn]$ ]]; then
                print_info "已取消安装。"
                exit 0
            fi
        fi
        
        # 执行全局安装
        exec sudo bash "$0" --global-exec "$@"
    fi
    
    # 所有安装模式都使用全局安装脚本
    if [[ "$INSTALL_MODE" == "global" ]]; then
        # 下载并执行全局安装脚本
        temp_script=$(mktemp)
        curl -sSL "https://raw.githubusercontent.com/$GITHUB_REPO/main/scripts/install_global.sh" -o "$temp_script"
        chmod +x "$temp_script"
        exec "$temp_script" "$@"
    elif [[ "$INSTALL_MODE" == "local" ]]; then
        # 开发环境也使用全局安装
        temp_script=$(mktemp)
        curl -sSL "https://raw.githubusercontent.com/$GITHUB_REPO/main/scripts/install_global.sh" -o "$temp_script"
        chmod +x "$temp_script"
        exec "$temp_script" "$@"
    elif [[ "$INSTALL_MODE" == "source" ]]; then
        # 源码安装也使用全局安装
        temp_script=$(mktemp)
        curl -sSL "https://raw.githubusercontent.com/$GITHUB_REPO/main/scripts/install_global.sh" -o "$temp_script"
        chmod +x "$temp_script"
        exec "$temp_script" --from-source "$@"
    fi
    
    # 如果到达这里说明有错误
    print_error "未知的安装模式: $INSTALL_MODE"
    exit 1
}

# 处理命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --from-source)
            FROM_SOURCE=1
            shift
            ;;
        --global-exec)
            GLOBAL_EXEC=1
            shift
            ;;
        --help)
            echo "AIS 全局安装脚本"
            echo
            echo "用法: $0 [选项]"
            echo
            echo "选项:"
            echo "  --from-source    从 GitHub 源码安装"
            echo "  --help          显示此帮助信息"
            echo
            echo "安装方式:"
            echo "  默认全局安装（所有用户可用）:"
            echo "    curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash"
            echo
            echo "  从源码全局安装:"
            echo "    curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --from-source"
            echo
            echo "  注意：AIS 现在只支持全局安装，确保所有用户都可以使用。"
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
if [[ "$FROM_SOURCE" == "1" ]]; then
    main --from-source
elif [[ "$GLOBAL_EXEC" == "1" ]]; then
    main --global-exec
else
    main
fi