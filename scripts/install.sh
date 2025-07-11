#!/bin/bash
# AIS - AI-powered terminal assistant
# 一键安装脚本
# 
# 快速安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/install.sh | bash
# 从源码安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/install.sh | bash -s -- --from-source
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
    if [ -f "pyproject.toml" ] && grep -q "ais" pyproject.toml 2>/dev/null; then
        INSTALL_METHOD="local"
        print_info "检测到开发环境，将从当前目录安装"
    elif [[ "$1" == "--from-source" ]]; then
        INSTALL_METHOD="source"
        print_info "将从 GitHub 源码安装"
    else
        INSTALL_METHOD="pypi"
        print_info "将从 PyPI 安装"
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
    
    # 第4步：配置 Shell 集成
    print_step 4 "配置 Shell 集成"
    
    shell_config=$(detect_shell_config)
    print_info "Shell 配置文件: $shell_config"
    
    # 备份配置文件
    if [ -f "$shell_config" ]; then
        cp "$shell_config" "${shell_config}.backup.$(date +%Y%m%d_%H%M%S)"
        print_info "已创建配置文件备份"
    fi
    
    # 移除旧的集成配置
    if grep -q "# START AIS INTEGRATION" "$shell_config" 2>/dev/null; then
        print_info "移除旧的集成配置..."
        sed -i '/# START AIS INTEGRATION/,/# END AIS INTEGRATION/d' "$shell_config" 2>/dev/null || true
    fi
    
    # 查找集成脚本路径
    integration_script=""
    
    # 方法1: 查找pipx安装的位置
    if command_exists ais; then
        ais_path=$(which ais)
        ais_dir=$(dirname "$ais_path")
        possible_script="$ais_dir/../share/ais/shell/integration.sh"
        if [ -f "$possible_script" ]; then
            integration_script="$possible_script"
        fi
    fi
    
    # 方法2: 查找系统安装位置
    if [ -z "$integration_script" ]; then
        for path in "/usr/local/share/ais" "/opt/ais" "$HOME/.local/share/ais"; do
            if [ -f "$path/shell/integration.sh" ]; then
                integration_script="$path/shell/integration.sh"
                break
            fi
        done
    fi
    
    # 方法3: 如果是本地安装，使用当前目录
    if [ -z "$integration_script" ] && [ -f "shell/integration.sh" ]; then
        integration_script="$(pwd)/shell/integration.sh"
        # 创建系统级别的副本
        sudo mkdir -p /usr/local/share/ais/shell
        sudo cp shell/integration.sh /usr/local/share/ais/shell/
        integration_script="/usr/local/share/ais/shell/integration.sh"
    fi
    
    # 添加新的集成配置
    if [ -n "$integration_script" ]; then
        cat >> "$shell_config" << EOF

# START AIS INTEGRATION - Auto-added by installer
# 确保 AIS 命令在 PATH 中
export PATH="\$HOME/.local/bin:\$PATH"

# 加载 AIS shell 集成
if [ -f "$integration_script" ]; then
    source "$integration_script"
fi
# END AIS INTEGRATION
EOF
        print_success "Shell 集成脚本: $integration_script"
    else
        print_warning "未找到集成脚本，请手动配置"
    fi
    
    print_success "Shell 集成已配置"
    
    # 第5步：初始化配置
    print_step 5 "初始化配置"
    
    # 初始化配置目录
    ais config >/dev/null 2>&1 || true
    
    # 开启自动分析（可选）
    ais on >/dev/null 2>&1 || true
    
    print_success "配置初始化完成"
    
    # 第6步：安装完成
    print_step 6 "安装完成"
    
    echo
    print_success "🎉 AIS 安装成功！"
    echo
    print_info "📋 开始使用:"
    print_info "  1. 重新加载配置: source $shell_config"
    print_info "  2. 或者重启终端"
    print_info "  3. 测试自动分析: mkdirr /tmp/test  (故意输错)"
    print_info "  4. 手动提问: ais ask \"如何使用 docker?\""
    print_info "  5. 查看帮助: ais --help"
    echo
    print_info "🔧 常用命令:"
    print_info "  ais config        - 查看配置"
    print_info "  ais on/off         - 开启/关闭自动分析"
    print_info "  ais history        - 查看命令历史"
    print_info "  ais learn git      - 学习命令行知识"
    echo
    print_warning "⚠️  重要: 请运行以下命令激活配置:"
    print_warning "  source $shell_config"
    echo
}

# 处理命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --from-source)
            FROM_SOURCE=1
            shift
            ;;
        --help)
            echo "AIS 安装脚本"
            echo
            echo "用法: $0 [选项]"
            echo
            echo "选项:"
            echo "  --from-source    从 GitHub 源码安装"
            echo "  --help          显示此帮助信息"
            echo
            echo "快速安装:"
            echo "  curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/install.sh | bash"
            echo
            echo "从源码安装:"
            echo "  curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/install.sh | bash -s -- --from-source"
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