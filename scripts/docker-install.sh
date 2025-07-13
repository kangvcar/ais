#!/bin/bash
# AIS Docker 安装脚本
# 提供多种Docker安装选择

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

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查Docker环境
check_docker() {
    print_info "🔍 检查Docker环境..."
    
    if ! command_exists docker; then
        print_error "Docker未安装。请先安装Docker:"
        print_info "  Ubuntu/Debian: sudo apt install docker.io"
        print_info "  CentOS/RHEL: sudo yum install docker"
        print_info "  或访问: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # 检查Docker是否运行
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker服务未运行。请启动Docker:"
        print_info "  sudo systemctl start docker"
        exit 1
    fi
    
    # 检查用户权限
    if ! docker ps >/dev/null 2>&1; then
        print_warning "当前用户没有Docker权限，将使用sudo"
        DOCKER_CMD="sudo docker"
    else
        DOCKER_CMD="docker"
    fi
    
    print_success "Docker环境检查通过"
}

# 检查Docker Compose
check_docker_compose() {
    if command_exists docker-compose; then
        COMPOSE_CMD="docker-compose"
    elif $DOCKER_CMD compose version >/dev/null 2>&1; then
        COMPOSE_CMD="$DOCKER_CMD compose"
    else
        print_warning "Docker Compose未找到，将只提供基础Docker安装"
        return 1
    fi
    return 0
}

# 构建AIS Docker镜像
build_image() {
    print_info "🏗️  构建AIS Docker镜像..."
    
    # 下载源码（如果当前目录没有Dockerfile）
    if [ ! -f "Dockerfile" ]; then
        print_info "📥 下载AIS源码..."
        if command_exists git; then
            git clone https://github.com/kangvcar/ais.git ais-source
            cd ais-source
        else
            print_error "需要git或在AIS源码目录中运行此脚本"
            exit 1
        fi
    fi
    
    # 构建镜像
    $DOCKER_CMD build -t ais-terminal:latest .
    print_success "镜像构建完成"
}

# 运行AIS容器
run_container() {
    local mode="$1"
    
    case "$mode" in
        "interactive")
            print_info "🚀 启动交互式AIS容器..."
            $DOCKER_CMD run -it --rm \
                --name ais-interactive \
                -v "$PWD:/workspace:ro" \
                ais-terminal:latest bash
            ;;
        "daemon")
            print_info "🚀 启动AIS守护进程容器..."
            $DOCKER_CMD run -d \
                --name ais-daemon \
                --restart unless-stopped \
                -v "$PWD:/workspace:ro" \
                -v ais-config:/home/ais/.config/ais \
                ais-terminal:latest tail -f /dev/null
            print_success "AIS守护进程已启动"
            print_info "💡 使用容器: $DOCKER_CMD exec -it ais-daemon bash"
            ;;
        "oneshot")
            print_info "🚀 运行一次性AIS命令..."
            shift  # 移除mode参数
            $DOCKER_CMD run --rm \
                -v "$PWD:/workspace:ro" \
                ais-terminal:latest ais "$@"
            ;;
    esac
}

# 使用Docker Compose
run_compose() {
    print_info "🐙 使用Docker Compose启动AIS服务..."
    
    if [ ! -f "docker-compose.yml" ]; then
        print_info "📥 下载docker-compose.yml..."
        curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/docker-compose.yml -o docker-compose.yml
    fi
    
    $COMPOSE_CMD up -d ais
    print_success "AIS服务已启动"
    print_info "💡 查看日志: $COMPOSE_CMD logs -f ais"
    print_info "💡 进入容器: $COMPOSE_CMD exec ais bash"
    print_info "💡 停止服务: $COMPOSE_CMD down"
}

# 主函数
main() {
    echo "================================================"
    echo "       AIS - Docker 安装脚本"
    echo "================================================"
    echo "提供多种Docker运行方式"
    echo
    
    check_docker
    
    # 检查是否已存在镜像
    if ! $DOCKER_CMD images ais-terminal:latest --format "table {{.Repository}}" | grep -q ais-terminal; then
        build_image
    else
        print_success "发现已存在的AIS镜像"
    fi
    
    # 提供运行选择
    echo
    print_info "🎯 选择运行方式:"
    echo "1. 交互式容器 (推荐)"
    echo "2. 守护进程容器"
    echo "3. 一次性命令"
    if check_docker_compose; then
        echo "4. Docker Compose (完整服务)"
    fi
    echo
    
    read -p "请选择 (1-4): " choice
    
    case "$choice" in
        "1")
            run_container "interactive"
            ;;
        "2")
            run_container "daemon"
            ;;
        "3")
            echo "请输入AIS命令 (例如: --version):"
            read -r cmd
            run_container "oneshot" $cmd
            ;;
        "4")
            if check_docker_compose; then
                run_compose
            else
                print_error "Docker Compose不可用"
                exit 1
            fi
            ;;
        *)
            print_error "无效选择"
            exit 1
            ;;
    esac
}

# 处理命令行参数
case "${1:-}" in
    --help|-h)
        echo "AIS Docker 安装脚本"
        echo
        echo "用法: $0 [选项]"
        echo
        echo "选项:"
        echo "  --help, -h     显示帮助信息"
        echo "  --build        只构建镜像"
        echo "  --interactive  启动交互式容器"
        echo "  --daemon       启动守护进程容器"
        echo "  --compose      使用Docker Compose"
        echo
        echo "快速开始:"
        echo "  curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/docker-install.sh | bash"
        exit 0
        ;;
    --build)
        check_docker
        build_image
        exit 0
        ;;
    --interactive)
        check_docker
        build_image 2>/dev/null || true
        run_container "interactive"
        exit 0
        ;;
    --daemon)
        check_docker
        build_image 2>/dev/null || true
        run_container "daemon"
        exit 0
        ;;
    --compose)
        check_docker
        check_docker_compose || {
            print_error "Docker Compose不可用"
            exit 1
        }
        run_compose
        exit 0
        ;;
    "")
        main
        ;;
    *)
        print_error "未知选项: $1"
        print_info "使用 --help 查看帮助"
        exit 1
        ;;
esac