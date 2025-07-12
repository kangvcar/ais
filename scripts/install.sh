#!/bin/bash
# AIS - AI智能终端助手
# 一键安装脚本 - 零配置体验
# 
# 快速安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
# 从源码安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --from-source
# 全局安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --global
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

print_step() {
    echo -e "${BLUE}📋 第$1步: $2${NC}"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检测操作系统
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command_exists apt-get; then
            echo "ubuntu"
        elif command_exists yum; then
            echo "centos"
        elif command_exists pacman; then
            echo "arch"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# 检测用户的 shell 配置文件
detect_shell_config() {
    shell_name=$(basename "$SHELL")
    case $shell_name in
        zsh)
            echo "$HOME/.zshrc"
            ;;
        bash)
            if [ -f "$HOME/.bashrc" ]; then
                echo "$HOME/.bashrc"
            else
                echo "$HOME/.bash_profile"
            fi
            ;;
        *)
            echo "$HOME/.bashrc"
            ;;
    esac
}

# 检查并安装系统依赖
install_system_deps() {
    os_type=$(detect_os)
    print_info "检测到操作系统: $os_type"
    
    case $os_type in
        ubuntu)
            if ! command_exists python3; then
                print_info "安装 Python 3..."
                sudo apt update && sudo apt install -y python3 python3-pip python3-venv
            fi
            if ! command_exists pipx; then
                print_info "安装 pipx..."
                sudo apt install -y pipx
            fi
            ;;
        centos)
            if ! command_exists python3; then
                print_info "安装 Python 3..."
                sudo yum install -y python3 python3-pip
            fi
            if ! command_exists pipx; then
                print_info "安装 pipx..."
                python3 -m pip install --user pipx
            fi
            ;;
        macos)
            if ! command_exists python3; then
                print_error "请先安装 Python 3: https://www.python.org/downloads/"
                exit 1
            fi
            if ! command_exists pipx; then
                print_info "安装 pipx..."
                python3 -m pip install --user pipx
            fi
            ;;
        *)
            print_warning "未知操作系统，请手动安装 Python 3.8+ 和 pipx"
            ;;
    esac
}

# 安装 AIS
install_ais() {
    if [[ "$INSTALL_METHOD" == "source" ]]; then
        print_info "从源码安装 AIS..."
        temp_dir=$(mktemp -d)
        git clone "https://github.com/$GITHUB_REPO.git" "$temp_dir"
        cd "$temp_dir"
        pipx install -e .
        cd - >/dev/null
        rm -rf "$temp_dir"
    elif [[ "$INSTALL_METHOD" == "local" ]]; then
        print_info "从当前目录安装 AIS..."
        pipx install -e .
    else
        print_info "从 PyPI 安装 AIS..."
        # 注意: 这里需要实际发布到PyPI后才能工作
        pipx install ais-terminal || {
            print_warning "PyPI 安装失败，尝试从源码安装..."
            INSTALL_METHOD="source"
            install_ais
        }
    fi
}

# 主安装函数
main() {
    echo "================================================"
    echo "         AIS - AI 智能终端助手 安装器"
    echo "================================================"
    echo "版本: $AIS_VERSION"
    echo "GitHub: https://github.com/$GITHUB_REPO"
    echo
    
    # 检测安装方式
    if [[ "$1" == "--global" ]]; then
        # 全局安装：下载并执行全局安装脚本
        print_info "全局安装模式：为所有用户安装"
        temp_script=$(mktemp)
        curl -sSL "https://raw.githubusercontent.com/$GITHUB_REPO/main/scripts/install_global.sh" -o "$temp_script"
        chmod +x "$temp_script"
        exec sudo "$temp_script"
    elif [ -f "pyproject.toml" ] && grep -q "ais" pyproject.toml 2>/dev/null; then
        INSTALL_METHOD="local"
        print_info "检测到开发环境，将从当前目录安装"
    elif [[ "$1" == "--from-source" ]]; then
        INSTALL_METHOD="source"
        print_info "将从 GitHub 源码安装"
    else
        INSTALL_METHOD="pypi"
        print_info "将从 PyPI 安装（推荐）"
    fi
    
    # 第1步：检查系统环境
    print_step 1 "检查系统环境"
    
    # 检查Python版本
    if command_exists python3; then
        python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)'; then
            print_success "Python $python_version (满足要求 >=3.8)"
        else
            print_error "Python 版本过低 ($python_version)，需要 3.8 或更高版本"
            exit 1
        fi
    else
        print_info "Python 3 未安装，准备安装..."
    fi
    
    # 第2步：安装系统依赖
    print_step 2 "安装系统依赖"
    install_system_deps
    
    # 确保pipx在PATH中
    if ! command_exists pipx; then
        export PATH="$HOME/.local/bin:$PATH"
        if ! command_exists pipx; then
            print_error "pipx 安装失败或不在 PATH 中"
            exit 1
        fi
    fi
    print_success "pipx 已可用"
    
    # 第3步：安装 AIS
    print_step 3 "安装 AIS"
    install_ais
    
    # 验证安装
    if ! command_exists ais; then
        export PATH="$HOME/.local/bin:$PATH"
        if ! command_exists ais; then
            print_error "AIS 安装失败，命令不可用"
            exit 1
        fi
    fi
    
    ais_version=$(ais --version 2>/dev/null | head -n1 || echo "unknown")
    print_success "AIS 已安装: $ais_version"
    
    # 第4步：自动配置功能
    print_step 4 "自动配置功能"
    
    # 确保PATH包含pipx安装的目录
    if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
        shell_config=$(detect_shell_config)
        if [ -f "$shell_config" ]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$shell_config"
            print_info "已添加 ~/.local/bin 到 PATH"
        fi
    fi
    
    # AIS现在支持自动配置，首次运行时会自动设置所有必要的配置
    print_info "AIS 现在支持零配置安装！"
    print_info "首次运行任何 ais 命令时，将自动完成所有配置"
    ais on >/dev/null 2>&1 || true
    
    print_success "配置初始化完成"
    
    # 第6步：安装完成
    print_step 6 "安装完成"
    
    echo
    print_success "🎉 AIS 安装成功！"
    echo
    print_info "🚀 立即体验 (零配置):"
    print_info "  1. 运行任意命令触发自动配置: ais config"
    print_info "  2. 重新加载Shell: source ~/.bashrc (或重启终端)"
    print_info "  3. 测试自动分析: mkdirr /tmp/test  (故意输错)"
    print_info "  4. 手动提问: ais ask \"如何使用 docker?\""
    print_info "  5. 查看完整帮助: ais --help"
    echo
    print_info "🔧 常用功能:"
    print_info "  ais config        - 查看当前配置"
    print_info "  ais on/off         - 控制自动错误分析"
    print_info "  ais history        - 查看命令历史和分析"
    print_info "  ais learn git      - 学习命令行知识"
    print_info "  ais suggest \"任务\" - 获取命令建议"
    echo
    print_info "✨ 特色功能:"
    print_info "  • 🤖 自动错误分析 - 命令失败时智能提供解决方案"
    print_info "  • 📚 交互式学习 - 不仅告诉你怎么做，还解释为什么"
    print_info "  • 🎯 上下文感知 - 基于当前环境提供个性化建议"
    print_info "  • 🔒 隐私保护 - 本地数据存储，敏感信息自动过滤"
    echo
}

# 处理命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --from-source)
            FROM_SOURCE=1
            shift
            ;;
        --global)
            GLOBAL_INSTALL=1
            shift
            ;;
        --help)
            echo "AIS 安装脚本"
            echo
            echo "用法: $0 [选项]"
            echo
            echo "选项:"
            echo "  --from-source    从 GitHub 源码安装"
            echo "  --global         全局安装 (需要sudo权限，为所有用户安装)"
            echo "  --help          显示此帮助信息"
            echo
            echo "安装方式:"
            echo "  快速安装 (推荐):"
            echo "    curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash"
            echo
            echo "  全局安装 (所有用户可用):"
            echo "    curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --global"
            echo
            echo "  从源码安装:"
            echo "    curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --from-source"
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
else
    main
fi