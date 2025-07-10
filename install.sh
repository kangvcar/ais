#!/bin/bash
# AIS 一键安装脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印彩色消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检测用户的 shell 配置文件
detect_shell_config() {
    if [ -n "$ZSH_VERSION" ]; then
        echo "$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        if [ -f "$HOME/.bashrc" ]; then
            echo "$HOME/.bashrc"
        else
            echo "$HOME/.bash_profile"
        fi
    else
        # 默认尝试 bashrc
        echo "$HOME/.bashrc"
    fi
}

# 主安装函数
main() {
    print_info "开始安装 AIS (AI-powered terminal assistant)..."
    
    # 1. 检查 Python
    print_info "检查 Python 环境..."
    if ! command_exists python3; then
        print_error "Python 3 未安装，请先安装 Python 3.8+"
        exit 1
    fi
    
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    print_success "Python $python_version 已安装"
    
    # 2. 检查并安装 uv
    print_info "检查 uv 包管理器..."
    if ! command_exists uv; then
        print_info "安装 uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.cargo/bin:$PATH"
        
        if ! command_exists uv; then
            print_error "uv 安装失败"
            exit 1
        fi
    fi
    print_success "uv 已可用"
    
    # 3. 安装 AIS
    print_info "安装 AIS..."
    
    # 如果在开发目录，使用本地安装
    if [ -f "pyproject.toml" ] && grep -q "ais-cli" pyproject.toml; then
        print_info "检测到开发环境，使用本地安装..."
        uv pip install --system -e .
    else
        # 从 PyPI 安装（暂时用本地路径模拟）
        print_warning "PyPI 安装暂未实现，请在项目目录运行此脚本"
        exit 1
    fi
    
    # 4. 验证安装
    print_info "验证 AIS 安装..."
    if ! command_exists ais; then
        print_error "AIS 安装失败，命令不可用"
        exit 1
    fi
    print_success "AIS 命令已可用"
    
    # 5. 配置 Shell 集成
    print_info "配置 Shell 集成..."
    
    shell_config=$(detect_shell_config)
    integration_script="$(dirname "$(which ais)")/../lib/python*/site-packages/ais/shell/integration.sh"
    
    # 查找实际的集成脚本路径
    if [ ! -f "$integration_script" ]; then
        integration_script="$(find /usr/local -name integration.sh 2>/dev/null | head -1)"
    fi
    
    # 如果在开发环境
    if [ -f "shell/integration.sh" ]; then
        integration_script="$(pwd)/shell/integration.sh"
    fi
    
    if [ -f "$integration_script" ]; then
        print_info "在 $shell_config 中添加 AIS 集成..."
        
        # 检查是否已经添加过
        if ! grep -q "# START AIS INTEGRATION" "$shell_config" 2>/dev/null; then
            cat >> "$shell_config" << EOF

# START AIS INTEGRATION
# This block is managed by ais-cli. Do not edit manually.
if [ -f "$integration_script" ]; then
    source "$integration_script"
fi
# END AIS INTEGRATION
EOF
            print_success "Shell 集成已添加到 $shell_config"
        else
            print_warning "Shell 集成已存在于 $shell_config"
        fi
    else
        print_warning "未找到集成脚本，请手动配置"
    fi
    
    # 6. 初始化配置
    print_info "初始化 AIS 配置..."
    ais config >/dev/null 2>&1 || true
    print_success "配置初始化完成"
    
    # 7. 完成安装
    print_success "AIS 安装完成！"
    print_info ""
    print_info "使用说明："
    print_info "  - 重新加载 shell: source $shell_config"
    print_info "  - 或者重启终端使配置生效"
    print_info "  - 查看帮助: ais --help"
    print_info "  - 开启自动分析: ais on"
    print_info "  - 测试对话: ais ask \"hello\""
    print_info "  - 查看状态: ais_status"
    print_info ""
    print_warning "请运行以下命令使 shell 集成生效："
    print_warning "  source $shell_config"
}

# 运行主函数
main "$@"