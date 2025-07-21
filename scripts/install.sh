#!/bin/bash
# AIS - 上下文感知的错误分析学习助手
# 智能安装脚本 - 基于多发行版测试验证优化
# 
# 推荐安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
# 用户安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --user
# 系统安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system
# 
# GitHub: https://github.com/kangvcar/ais

set -e  # 遇到错误立即退出
set -o pipefail  # 管道中任何命令失败都会导致整个管道失败

# 清理函数
cleanup() {
    stop_spinner
    printf "\r\033[K"  # 清空当前行
}

# 注册清理函数
trap cleanup EXIT INT TERM

# 版本信息
AIS_VERSION="latest"
GITHUB_REPO="kangvcar/ais"

# 安装选项
NON_INTERACTIVE=0
INSTALL_MODE="auto"  # auto, user, system, container
SKIP_CHECKS=0
DEBUG_MODE=0  # 调试模式，显示详细错误信息
FORCE_REINSTALL=0  # 强制重新安装模式

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 进度和状态显示配置
SPINNER="⠋⠙⠹⠸⠼⠴⠦⠧"
SPINNER_PID=""
PROGRESS_TOTAL=100
PROGRESS_CURRENT=0

# 获取当前时间戳
get_timestamp() {
    date '+%H:%M:%S'
}

# 状态显示函数 - 带改进的spinner、时间戳和进度百分比
show_status() {
    local message="$1"
    local success="${2:-false}"
    local timestamp=$(get_timestamp)
    local progress_display=""
    
    # 计算进度百分比显示
    if [ $PROGRESS_CURRENT -le $PROGRESS_TOTAL ]; then
        progress_display="[${PROGRESS_CURRENT}%]"
    fi
    
    if [ "$success" = "true" ]; then
        printf "\r\033[K${GREEN}✓${NC} [%s]%s %s\n" "$timestamp" "$progress_display" "$message"
    else
        # 使用毫秒级时间戳获得更好的动态效果
        local spinner_index=$(( ($(date +%s%3N) / 100) % 8 ))
        local spinner_char="${SPINNER:$spinner_index:1}"
        printf "\r\033[K${CYAN}%s${NC} [%s]%s %s" "$spinner_char" "$timestamp" "$progress_display" "$message"
    fi
}

# 进度更新函数（保持接口兼容）
update_progress() {
    local new_progress=${1:-5}
    local message=${2:-""}
    PROGRESS_CURRENT=$new_progress
    show_status "$message"
}

# 带Spinner的进度更新（保持接口兼容）
update_progress_with_spinner() {
    local new_progress=${1:-5}
    local message=${2:-""}
    PROGRESS_CURRENT=$new_progress
    show_status "$message"
    sleep 0.1
}

# 停止Spinner（保持接口兼容）
stop_spinner() {
    if [ -n "$SPINNER_PID" ]; then
        kill "$SPINNER_PID" 2>/dev/null || true
        wait "$SPINNER_PID" 2>/dev/null || true
        SPINNER_PID=""
    fi
    printf "\r\033[K"
}

# 执行带有状态显示的长时间操作
run_with_spinner() {
    local message="$1"
    local command="$2"
    local spinner_type="${3:-dots}"  # 保持参数兼容性
    local success_message="${4:-$message}"
    
    # 显示初始状态
    show_status "$message"
    
    # 创建临时文件捕获错误输出
    local error_file="/tmp/ais_install_error_$$"
    
    # 在后台执行命令并显示spinner
    eval "$command" >/dev/null 2>"$error_file" &
    local cmd_pid=$!
    
    # 显示动态spinner直到命令完成
    while kill -0 "$cmd_pid" 2>/dev/null; do
        show_status "$message"
        sleep 0.2
    done
    
    # 等待命令完成并获取退出码
    wait "$cmd_pid"
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        show_status "$success_message" true
        rm -f "$error_file"
        return 0
    else
        printf "\r\033[K${RED}✗${NC} ${message} 失败\n"
        
        # 错误处理逻辑保持不变
        if [ "$DEBUG_MODE" -eq 1 ] || [ -s "$error_file" ]; then
            local error_size=$(wc -c < "$error_file" 2>/dev/null || echo 0)
            if [ "$error_size" -gt 0 ]; then
                echo
                print_error "错误详情："
                echo "----------------------------------------"
                if [ "$error_size" -gt 5000 ]; then
                    echo "错误输出过长，显示最后50行："
                    tail -50 "$error_file"
                else
                    cat "$error_file"
                fi
                echo "----------------------------------------"
                echo
            fi
        fi
        
        if [ "$DEBUG_MODE" -eq 1 ] && [ -s "$error_file" ]; then
            local log_file="/tmp/ais_install_debug.log"
            echo "=== $(date) ===" >> "$log_file"
            echo "Command: $command" >> "$log_file"
            echo "Exit code: $exit_code" >> "$log_file"
            cat "$error_file" >> "$log_file"
            echo "" >> "$log_file"
            print_info "错误日志已保存到: $log_file"
        fi
        
        rm -f "$error_file"
        return $exit_code
    fi
}

# 统一的消息打印函数
print_msg() {
    local type="$1" message="$2"
    case "$type" in
        "info") echo -e "${BLUE}ℹ️  ${message}${NC}" ;;
        "success") echo -e "${GREEN}✓${NC} ${message}" ;;
        "warning") echo -e "${YELLOW}⚠️  ${message}${NC}" ;;
        "error") echo -e "${RED}✗  ${message}${NC}" ;;
    esac
}

# 保持向后兼容的函数别名
print_info() { print_msg "info" "$1"; }
print_success() { print_msg "success" "$1"; }
print_warning() { print_msg "warning" "$1"; }
print_error() { print_msg "error" "$1"; }


# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# ==================== 幂等性和状态检查函数 ====================

# 检查包是否已安装
is_package_installed() {
    local package="$1"
    if command_exists yum; then
        yum list installed "$package" >/dev/null 2>&1
    elif command_exists dnf; then
        dnf list installed "$package" >/dev/null 2>&1
    elif command_exists apt; then
        dpkg -l "$package" 2>/dev/null | grep -q "^ii.*$package"
    else
        return 1
    fi
}

# 批量检查包是否已安装
check_packages_installed() {
    local packages=("$@")
    local missing_packages=()
    
    for package in "${packages[@]}"; do
        if ! is_package_installed "$package"; then
            missing_packages+=("$package")
        fi
    done
    
    if [ ${#missing_packages[@]} -gt 0 ]; then
        echo "${missing_packages[@]}"
        return 1
    fi
    return 0
}

# 安装包（带幂等性检查）
install_package_if_needed() {
    local message="$1"
    local package_cmd="$2"
    local success_msg="$3"
    local packages="${4:-}"
    
    # 如果提供了包列表，检查是否已安装
    if [ -n "$packages" ]; then
        local missing_packages
        missing_packages=$(check_packages_installed $packages 2>/dev/null || echo "$packages")
        if [ -z "$missing_packages" ] || [ "$missing_packages" = " " ]; then
            print_success "$success_msg (已安装)"
            return 0
        fi
    fi
    
    # 根据环境决定是否使用sudo
    if [ "$(detect_environment)" = "user" ]; then
        package_cmd="sudo $package_cmd"
    fi
    
    run_with_spinner "$message" "$package_cmd" "dots" "$success_msg"
}

# 检查Python环境状态
check_python_environment() {
    local strategy="$1"
    
    case "$strategy" in
        "compile_python310")
            # 检查Python 3.10是否已安装
            if [ -x "/usr/local/bin/python3.10" ]; then
                local version=$(/usr/local/bin/python3.10 --version 2>/dev/null | grep -o "3\.10\.[0-9]*")
                if [ "$version" = "3.10.9" ]; then
                    export PYTHON_CMD="/usr/local/bin/python3.10"
                    export PIP_CMD="/usr/local/bin/python3.10 -m pip"
                    print_success "Python 3.10.9已安装并可用"
                    return 0
                fi
            fi
            return 1
            ;;
        "python_upgrade")
            # 检查Python 3.9是否可用
            if command_exists python3.9 && python3.9 --version >/dev/null 2>&1; then
                export PYTHON_CMD="python3.9"
                export PIP_CMD="python3.9 -m pip"
                print_success "Python 3.9已可用"
                return 0
            fi
            return 1
            ;;
        "pipx_native")
            # 检查pipx是否可用
            if command_exists pipx; then
                print_success "pipx已可用"
                return 0
            fi
            return 1
            ;;
        *)
            # 检查系统默认Python
            if command_exists python3; then
                export PYTHON_CMD="python3"
                export PIP_CMD="python3 -m pip"
                print_success "系统Python已可用"
                return 0
            fi
            return 1
            ;;
    esac
}

# 检查AIS安装状态
check_ais_installation() {
    local strategy="$1"
    
    case "$strategy" in
        "pipx_native")
            if command_exists pipx && pipx list | grep -q "ais-terminal"; then
                local version=$(pipx list | grep ais-terminal | grep -o "version [0-9.]*" | cut -d' ' -f2 2>/dev/null || echo "unknown")
                print_success "AIS已通过pipx安装 (版本: $version)"
                return 0
            fi
            ;;
        *)
            # 检查pip安装的AIS
            if [ -n "$PIP_CMD" ] && $PIP_CMD show ais-terminal >/dev/null 2>&1; then
                local version=$($PIP_CMD show ais-terminal | grep Version | cut -d' ' -f2 2>/dev/null || echo "unknown")
                print_success "AIS已安装 (版本: $version)"
                
                # 检查命令是否可用
                if command_exists ais; then
                    return 0
                else
                    print_warning "AIS包已安装但命令不可用，需要修复"
                    return 2  # 需要修复
                fi
            fi
            ;;
    esac
    return 1  # 未安装
}

# 检查Shell集成状态
check_shell_integration() {
    local config_file="$HOME/.bashrc"
    [ -n "$ZSH_VERSION" ] && config_file="$HOME/.zshrc"
    
    if [ -f "$config_file" ]; then
        # 检查新版集成
        if grep -q "ais shell-integration" "$config_file" 2>/dev/null; then
            print_success "Shell集成已配置 (新版本)"
            return 0
        fi
        
        # 检查旧版集成
        if grep -q "# AIS INTEGRATION" "$config_file" 2>/dev/null; then
            print_warning "检测到旧版Shell集成，需要更新"
            return 2  # 需要更新
        fi
    fi
    
    return 1  # 未配置
}

# 健康检查和自动修复
perform_health_check() {
    local strategy="$1"
    
    local issues_found=0
    
    # 检查Python环境
    if ! check_python_environment "$strategy"; then
        ((issues_found++))
    fi
    
    # 检查AIS安装
    local ais_status
    check_ais_installation "$strategy"
    ais_status=$?
    if [ $ais_status -eq 1 ]; then
        ((issues_found++))
    elif [ $ais_status -eq 2 ]; then
        ((issues_found++))
    fi
    
    # 检查Shell集成
    local shell_status
    check_shell_integration
    shell_status=$?
    if [ $shell_status -eq 1 ]; then
        ((issues_found++))
    elif [ $shell_status -eq 2 ]; then
        ((issues_found++))
    fi
    
    if [ $issues_found -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

# 获取系统信息
get_system_info() {
    local os_name=""
    local os_version=""
    local python_version=""
    
    # 检测操作系统
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        os_name="$ID"
        os_version="$VERSION_ID"
    elif [ -f /etc/redhat-release ]; then
        if grep -q "CentOS" /etc/redhat-release; then
            os_name="centos"
            os_version=$(grep -oP '\d+\.\d+' /etc/redhat-release | head -1)
        elif grep -q "Rocky" /etc/redhat-release; then
            os_name="rocky"
            os_version=$(grep -oP '\d+\.\d+' /etc/redhat-release | head -1)
        fi
    fi
    
    # 检测Python版本
    if command_exists python3; then
        python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    fi
    
    echo "$os_name|$os_version|$python_version"
}

# 比较Python版本
compare_python_version() {
    local version1=$1
    local version2=$2
    
    # 移除版本号中的非数字字符，只保留主版本号和次版本号
    local v1_major=$(echo "$version1" | sed 's/[^0-9.]//g' | cut -d. -f1)
    local v1_minor=$(echo "$version1" | sed 's/[^0-9.]//g' | cut -d. -f2)
    local v2_major=$(echo "$version2" | sed 's/[^0-9.]//g' | cut -d. -f1)
    local v2_minor=$(echo "$version2" | sed 's/[^0-9.]//g' | cut -d. -f2)
    
    # 处理空值
    v1_major=${v1_major:-0}
    v1_minor=${v1_minor:-0}
    v2_major=${v2_major:-0}
    v2_minor=${v2_minor:-0}
    
    # 比较主版本号
    if [ "$v1_major" -lt "$v2_major" ]; then
        return 1  # version1 < version2
    elif [ "$v1_major" -gt "$v2_major" ]; then
        return 0  # version1 > version2
    else
        # 主版本号相同，比较次版本号
        if [ "$v1_minor" -lt "$v2_minor" ]; then
            return 1  # version1 < version2
        else
            return 0  # version1 >= version2
        fi
    fi
}

# 检测安装策略
detect_install_strategy() {
    local system_info
    system_info=$(get_system_info)
    IFS='|' read -r os_name os_version python_version <<< "$system_info"
    
    # 优先检查特殊系统配置
    if [ "$os_name" = "centos" ] && ([[ "$os_version" =~ ^7\. ]] || [ "$os_version" = "7" ]); then
        echo "compile_python310"  # CentOS 7需要编译Python 3.10.9
        return
    fi
    
    if [ "$os_name" = "kylin" ]; then
        echo "compile_python310"  # Kylin Linux需要编译Python 3.10.9
        return
    fi
    
    # 然后检查Python版本，如果小于3.9则需要编译安装
    if [ -n "$python_version" ] && ! compare_python_version "$python_version" "3.9"; then
        echo "compile_python310"  # 需要编译安装Python 3.10.9
        return
    fi
    
    # 根据测试验证结果确定安装策略
    case "$os_name:$os_version" in
        "ubuntu:24."*|"debian:12"*) echo "pipx_native" ;;
        "ubuntu:20."*|"rocky:8"*|"centos:8"*) echo "python_upgrade" ;;
        "centos:7"*) echo "compile_python310" ;;
        "kylin:"*) echo "compile_python310" ;;
        "ubuntu:"*|"debian:"*|"rocky:"*|"centos:"*|"fedora:"*|"openeuler:"*) echo "pip_direct" ;;
        *)
            # 基于Python版本判断
            case "$python_version" in
                "3.12"*|"3.11"*|"3.10"*)
                    if command_exists pipx || (command_exists apt && apt list pipx 2>/dev/null | grep -q pipx); then
                        echo "pipx_native"
                    else
                        echo "pip_direct"
                    fi ;;
                "3.9"*|"3.8"*) echo "pip_direct" ;;
                *) echo "compile_python310" ;;
            esac ;;
    esac
}

# 检测环境类型
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

# 统一的包管理执行函数
run_pkg_manager() {
    local message="$1" cmd="$2" success_msg="$3"
    
    # 根据环境决定是否使用sudo
    if [ "$(detect_environment)" = "user" ]; then
        cmd="sudo $cmd"
    fi
    
    run_with_spinner "$message" "$cmd" "dots" "$success_msg"
}

# 安装系统依赖
install_system_dependencies() {
    local strategy=$1
    # 更新进度条并显示步骤
    update_progress 15 "正在安装系统依赖..."
    
    case "$strategy" in
        "compile_python310")
            # CentOS 7.x 和 Kylin Linux 编译Python 3.10.9 - 严格按照测试流程
            if command_exists yum; then
                # 检测是否为CentOS 7
                local is_centos7=0
                if [ -f "/etc/centos-release" ]; then
                    local centos_version=$(cat /etc/centos-release 2>/dev/null | grep -oE '[0-9]+' | head -n1)
                    if [ "$centos_version" = "7" ]; then
                        is_centos7=1
                    fi
                fi
                
                if [ "$is_centos7" -eq 1 ]; then
                    # CentOS 7.x 特殊处理
                    PROGRESS_CURRENT=20
                    install_package_if_needed "正在安装EPEL源..." "yum install -y epel-release" "EPEL源安装完成" "epel-release"
                    PROGRESS_CURRENT=30
                    install_package_if_needed "正在安装编译依赖包..." "yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel tk-devel libffi-devel xz-devel openssl11 openssl11-devel openssl11-libs ncurses-devel gdbm-devel db4-devel libpcap-devel expat-devel" "编译依赖包安装完成" "gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel tk-devel libffi-devel xz-devel openssl11 openssl11-devel openssl11-libs ncurses-devel gdbm-devel db4-devel libpcap-devel expat-devel"
                else
                    # Kylin Linux 或其他系统
                    install_package_if_needed "正在安装编译依赖包..." "yum install -y gcc make patch zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel" "编译依赖包安装完成" "gcc make patch zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel"
                fi
            elif command_exists dnf; then
                # 检查Development Tools组是否已安装
                if ! dnf group list --installed | grep -q "Development Tools"; then
                    run_pkg_manager "正在安装开发工具..." "dnf groupinstall -y 'Development Tools'" "开发工具安装完成"
                else
                    print_success "开发工具安装完成 (已安装)"
                fi
                install_package_if_needed "正在安装依赖库..." "dnf install -y zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel git wget tar" "依赖库安装完成" "zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel git wget tar"
            elif command_exists apt-get; then
                # 检查是否需要更新包列表（通过检查最近更新时间）
                local apt_update_needed=1
                if [ -f "/var/lib/apt/lists/lock" ]; then
                    local last_update=$(stat -c %Y /var/lib/apt/lists/* 2>/dev/null | sort -nr | head -1 2>/dev/null || echo 0)
                    local current_time=$(date +%s)
                    local time_diff=$((current_time - last_update))
                    # 如果上次更新在1小时内，跳过更新
                    if [ $time_diff -lt 3600 ]; then
                        apt_update_needed=0
                        print_success "软件包列表更新完成 (最近已更新)"
                    fi
                fi
                
                if [ $apt_update_needed -eq 1 ]; then
                    run_pkg_manager "正在更新软件包列表..." "apt update" "软件包列表更新完成"
                fi
                
                install_package_if_needed "正在安装编译依赖..." "apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget tar" "编译依赖安装完成" "build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget tar"
            fi
            ;;
        "python_upgrade")
            # 安装Python升级包
            if command_exists dnf; then
                install_package_if_needed "正在安装Python 3.9..." "dnf install -y python39 python39-pip" "Python 3.9安装完成" "python39 python39-pip"
            elif command_exists apt-get; then
                # 检查是否需要更新包列表
                local apt_update_needed=1
                if [ -f "/var/lib/apt/lists/lock" ]; then
                    local last_update=$(stat -c %Y /var/lib/apt/lists/* 2>/dev/null | sort -nr | head -1 2>/dev/null || echo 0)
                    local current_time=$(date +%s)
                    local time_diff=$((current_time - last_update))
                    if [ $time_diff -lt 3600 ]; then
                        apt_update_needed=0
                        print_success "软件包列表更新完成 (最近已更新)"
                    fi
                fi
                
                if [ $apt_update_needed -eq 1 ]; then
                    run_pkg_manager "正在更新软件包列表..." "apt update" "软件包列表更新完成"
                fi
                
                install_package_if_needed "正在安装必要工具..." "apt install -y software-properties-common" "必要工具安装完成" "software-properties-common"
                
                # 检查PPA是否已添加
                if ! grep -q "deadsnakes/ppa" /etc/apt/sources.list.d/* 2>/dev/null; then
                    run_pkg_manager "正在添加Python源..." "add-apt-repository -y ppa:deadsnakes/ppa && apt update" "Python源添加完成"
                else
                    print_success "Python源添加完成 (已存在)"
                fi
                
                install_package_if_needed "正在安装Python 3.9..." "apt install -y python3.9 python3.9-venv python3.9-dev" "Python 3.9安装完成" "python3.9 python3.9-venv python3.9-dev"
            fi
            ;;
        "pipx_native")
            # 安装pipx
            if command_exists apt-get; then
                # 检查是否需要更新包列表
                local apt_update_needed=1
                if [ -f "/var/lib/apt/lists/lock" ]; then
                    local last_update=$(stat -c %Y /var/lib/apt/lists/* 2>/dev/null | sort -nr | head -1 2>/dev/null || echo 0)
                    local current_time=$(date +%s)
                    local time_diff=$((current_time - last_update))
                    if [ $time_diff -lt 3600 ]; then
                        apt_update_needed=0
                        print_success "软件包列表更新完成 (最近已更新)"
                    fi
                fi
                
                if [ $apt_update_needed -eq 1 ]; then
                    run_pkg_manager "正在更新软件包列表..." "apt update" "软件包列表更新完成"
                fi
                
                install_package_if_needed "正在安装pipx..." "apt install -y pipx" "pipx安装完成" "pipx"
            elif command_exists dnf; then
                install_package_if_needed "正在安装pipx..." "dnf install -y pipx" "pipx安装完成" "pipx"
            fi
            ;;
    esac
}

# 设置Python环境
# Python 3.10.9编译安装函数
compile_python310() {
    local python_prefix="/usr/local"
    local original_dir="$(pwd)"  # 保存原始工作目录
    
    # 检查是否已经安装
    if [ -x "$python_prefix/bin/python3.10" ]; then
        print_info "Python 3.10.9已经安装"
        export PYTHON_CMD="$python_prefix/bin/python3.10"
        export PIP_CMD="$python_prefix/bin/python3.10 -m pip"
        return 0
    fi
    
    # 创建临时目录并下载源码
    local temp_dir="/tmp/python_build"
    mkdir -p "$temp_dir"
    cd "$temp_dir" || {
        print_error "无法进入临时目录: $temp_dir"
        return 1
    }
    
    # 下载Python源码 - 优先使用国内镜像源
    local python_file="Python-3.10.9.tgz"
    local python_urls=(
        "https://repo.huaweicloud.com/artifactory/python-local/3.10.9/Python-3.10.9.tgz"
        "https://mirrors.aliyun.com/python-release/3.10.9/Python-3.10.9.tgz"
        "https://www.python.org/ftp/python/3.10.9/Python-3.10.9.tgz"
    )
    
    # 检查是否已下载且大小合理（大于10MB）
    if [ -f "$python_file" ]; then
        local file_size=$(stat -c%s "$python_file" 2>/dev/null || echo 0)
        if [ "$file_size" -gt 10485760 ]; then  # 大于10MB
            print_success "检测到已下载的Python源码，跳过下载"
        else
            print_warning "已下载文件大小异常，重新下载"
            rm -f "$python_file"
        fi
    fi
    
    # 下载文件（如果需要）
    if [ ! -f "$python_file" ]; then
        local download_success=0
        PROGRESS_CURRENT=45
        for url in "${python_urls[@]}"; do
            for attempt in 1 2; do
                if run_with_spinner "正在下载Python源码..." "wget --timeout=30 --tries=2 -O '$python_file' '$url'" "dots" "源码下载完成"; then
                    local file_size=$(stat -c%s "$python_file" 2>/dev/null || echo 0)
                    if [ "$file_size" -gt 10485760 ]; then  # 验证文件大小而不是SHA256
                        download_success=1
                        break 2
                    else
                        rm -f "$python_file"
                    fi
                fi
                sleep 2
            done
        done
        
        if [ $download_success -eq 0 ]; then
            print_error "Python源码下载失败，已尝试所有镜像源"
            print_info "请手动下载并放在当前目录：${python_urls[0]}"
            return 1
        fi
    fi
    
    # 解压并编译
    PROGRESS_CURRENT=50
    run_with_spinner "正在解压Python源码..." "tar -xf '$python_file'" "dots" "源码解压完成" || {
        cd "$original_dir" 2>/dev/null || true
        return 1
    }
    cd "Python-3.10.9" || {
        print_error "无法进入Python源码目录"
        cd "$original_dir" 2>/dev/null || true
        return 1
    }
    
    # CentOS 7特殊处理
    local is_centos7=0
    [ -f "/etc/centos-release" ] && grep -q "release 7" /etc/centos-release && is_centos7=1
    
    if [ "$is_centos7" -eq 1 ]; then
        run_with_spinner "正在修改configure文件..." "sed -i 's/PKG_CONFIG openssl /PKG_CONFIG openssl11 /g' configure" "dots" "configure修改完成"
        run_with_spinner "正在配置编译选项..." "./configure --prefix=$python_prefix --with-ensurepip=install" "chars" "编译配置完成" || {
            cd "$original_dir" 2>/dev/null || true
            return 1
        }
    else
        run_with_spinner "正在配置编译选项..." "./configure --prefix=$python_prefix --enable-optimizations --with-ensurepip=install" "chars" "编译配置完成" || {
            cd "$original_dir" 2>/dev/null || true
            return 1
        }
    fi
    
    # 编译和安装
    local cpu_cores=$(nproc 2>/dev/null || echo 2)
    run_with_spinner "正在编译Python..." "make -j$cpu_cores" "chars" "Python编译完成" || {
        cd "$original_dir" 2>/dev/null || true
        return 1
    }
    run_with_spinner "正在安装Python..." "make altinstall" "dots" "Python安装完成" || {
        cd "$original_dir" 2>/dev/null || true
        return 1
    }
    
    # 恢复原始工作目录
    cd "$original_dir" || print_warning "无法恢复原始工作目录"
    
    # 设置环境变量
    export PYTHON_CMD="$python_prefix/bin/python3.10"
    export PIP_CMD="$python_prefix/bin/python3.10 -m pip"
    show_status "Python 3.10.9编译安装完成" true
    
    # 确保返回成功
    return 0
}

setup_python_environment() {
    local strategy=$1
    update_progress 40 "正在设置Python环境..."
    
    case "$strategy" in
        "compile_python310")
            compile_python310
            ;;
        "python_upgrade")
            # 使用升级的Python版本
            export PYTHON_CMD="python3.9"
            export PIP_CMD="python3.9 -m pip"
            ;;
        *)
            # 使用系统默认Python
            export PYTHON_CMD="python3"
            export PIP_CMD="python3 -m pip"
            ;;
    esac
}

# 安装AIS
install_ais() {
    local strategy=$1
    # 更新进度条并显示步骤
    update_progress 60 "正在安装AIS..."
    
    # 检查AIS安装状态（除非强制重新安装）
    if [ "$FORCE_REINSTALL" -eq 0 ]; then
        local ais_status
        check_ais_installation "$strategy"
        ais_status=$?
        
        if [ $ais_status -eq 0 ]; then
            print_success "AIS已正确安装，跳过安装步骤"
            return 0
        elif [ $ais_status -eq 2 ]; then
            print_info "检测到AIS安装需要修复，正在修复..."
            repair_ais_installation "$strategy"
            return $?
        fi
    fi
    
    case "$strategy" in
        "pipx_native")
            # 使用pipx安装
            if ! command_exists pipx; then
                run_with_spinner "正在安装pipx..." "$PIP_CMD install --user pipx" "dots" "pipx安装完成"
                pipx ensurepath >/dev/null 2>&1
                export PATH="$HOME/.local/bin:$PATH"
            fi
            
            if pipx list | grep -q "ais-terminal"; then
                run_with_spinner "正在更新AIS到最新版本..." "pipx upgrade ais-terminal" "arrows" "AIS更新完成"
            else
                run_with_spinner "正在安装AIS..." "pipx install ais-terminal" "arrows" "AIS安装完成"
            fi
            pipx ensurepath >/dev/null 2>&1
            ;;
        "compile_python310")
            # 检查是否已安装，决定安装还是升级
            local install_cmd="install"
            if $PIP_CMD show ais-terminal >/dev/null 2>&1; then
                install_cmd="install --upgrade"
            fi
            
            # 使用编译的Python 3.10.9安装，增加详细的错误检查
            if run_with_spinner "正在${install_cmd}AIS..." "$PIP_CMD $install_cmd ais-terminal" "arrows" "AIS${install_cmd}完成"; then
                # 验证安装是否成功
                if ! $PIP_CMD show ais-terminal >/dev/null 2>&1; then
                    print_error "AIS包安装验证失败"
                    return 1
                fi
                
                # 修复AIS命令可用性
                fix_ais_command "$strategy"
            else
                print_error "AIS安装失败"
                return 1
            fi
            ;;
        *)
            # 标准pip安装 - 检查是否需要升级
            local install_cmd="install"
            if [ -n "$PIP_CMD" ] && $PIP_CMD show ais-terminal >/dev/null 2>&1; then
                install_cmd="install --upgrade"
            fi
            
            run_with_spinner "正在${install_cmd}AIS..." "$PIP_CMD $install_cmd ais-terminal" "arrows" "AIS${install_cmd}完成"
            ;;
    esac
}

# 修复AIS安装
repair_ais_installation() {
    local strategy="$1"
    
    case "$strategy" in
        "compile_python310")
            fix_ais_command "$strategy"
            ;;
        *)
            # 重新安装
            if [ -n "$PIP_CMD" ]; then
                $PIP_CMD uninstall -y ais-terminal >/dev/null 2>&1 || true
                run_with_spinner "正在重新安装AIS..." "$PIP_CMD install ais-terminal" "arrows" "AIS重新安装完成"
            fi
            ;;
    esac
}

# 修复AIS命令可用性
fix_ais_command() {
    local strategy="$1"
    
    # 查找ais命令的实际位置
    local ais_executable=""
    # 方法1: 查找pip安装的scripts目录
    local python_scripts_dir=$($PYTHON_CMD -c "import sysconfig; print(sysconfig.get_path('scripts'))" 2>/dev/null)
    if [ -n "$python_scripts_dir" ] && [ -f "$python_scripts_dir/ais" ]; then
        ais_executable="$python_scripts_dir/ais"
    # 方法2: 查找常见位置
    elif [ -f "/usr/local/bin/ais" ]; then
        ais_executable="/usr/local/bin/ais"
    # 方法3: 使用which命令
    elif command -v ais >/dev/null 2>&1; then
        ais_executable=$(command -v ais)
    fi
    
    # 创建或验证ais命令
    if [ -n "$ais_executable" ] && [ -f "$ais_executable" ]; then
        if [ "$ais_executable" != "/usr/local/bin/ais" ]; then
            run_with_spinner "正在创建AIS命令链接..." "ln -sf '$ais_executable' /usr/local/bin/ais" "dots" "AIS命令链接创建完成"
        fi
        show_status "AIS命令已修复: $ais_executable" true
    else
        # 作为最后手段，创建包装脚本
        print_warning "未找到ais可执行文件，创建包装脚本"
        cat > /usr/local/bin/ais << EOF
#!/bin/bash
# AIS wrapper script
export PATH="/usr/local/bin:\$PATH"
exec $PYTHON_CMD -c "
import sys
sys.path.insert(0, '$($PYTHON_CMD -c "import site; print(site.getsitepackages()[0])" 2>/dev/null)')
try:
    from ais.cli import main
    main()
except ImportError as e:
    print(f'Error: {e}')
    print('AIS package may not be properly installed')
    sys.exit(1)
" "\$@"
EOF
        chmod +x /usr/local/bin/ais
        show_status "已创建AIS包装脚本" true
    fi
}

# 创建Shell集成脚本
create_integration_script() {
    local script_path="$1"
    local ais_path
    
    # 查找AIS安装路径中的原始集成脚本
    ais_path=$(command -v ais 2>/dev/null)
    if [ -n "$ais_path" ]; then
        local source_script="$(dirname "$(dirname "$ais_path")")/src/ais/shell/integration.sh"
        if [ -f "$source_script" ]; then
            # 创建目录并复制原始脚本
            mkdir -p "$(dirname "$script_path")"
            cp "$source_script" "$script_path"
            chmod 755 "$script_path"
            return 0
        fi
    fi
    
    # 如果找不到原始脚本，创建简化版本
    mkdir -p "$(dirname "$script_path")"
    cat > "$script_path" << 'EOF'
#!/bin/bash
# 简化的AIS Shell集成
command -v ais >/dev/null 2>&1 && {
    _ais_precmd() {
        local exit_code=$?
        [ $exit_code -ne 0 ] && [ $exit_code -ne 130 ] && \
        grep -q "auto_analysis = true" "$HOME/.config/ais/config.toml" 2>/dev/null && {
            local cmd=$(history 1 | sed 's/^[ ]*[0-9]*[ ]*//' 2>/dev/null)
            [[ "$cmd" != *"_ais_"* ]] && [[ "$cmd" != *"history"* ]] && \
            echo && ais analyze --exit-code "$exit_code" --command "$cmd"
        }
    }
    [ -n "$BASH_VERSION" ] && PROMPT_COMMAND="_ais_precmd;${PROMPT_COMMAND}"
    [ -n "$ZSH_VERSION" ] && autoload -U add-zsh-hook 2>/dev/null && add-zsh-hook precmd _ais_precmd
}
EOF
    chmod 755 "$script_path"
}


# 设置Shell集成
setup_shell_integration() {
    update_progress 80 "正在设置Shell集成..."
    
    # 检查Shell集成状态
    local shell_status
    check_shell_integration
    shell_status=$?
    
    if [ $shell_status -eq 0 ]; then
        print_success "Shell集成配置已是最新版本"
        return 0
    fi
    
    # 确定配置文件
    local config_file="$HOME/.bashrc"
    [ -n "$ZSH_VERSION" ] && config_file="$HOME/.zshrc"
    [ ! -f "$config_file" ] && touch "$config_file"
    
    # 如果是旧版集成，先清理
    if [ $shell_status -eq 2 ]; then
        # 移除旧的AIS集成配置块
        sed -i '/# AIS INTEGRATION/,/^$/d' "$config_file" 2>/dev/null || true
        # 移除可能存在的其他旧配置
        sed -i '/command -v ais.*eval.*ais shell-integration/d' "$config_file" 2>/dev/null || true
    fi
    
    # 添加新版集成配置
    cat >> "$config_file" << 'EOF'

# AIS INTEGRATION
command -v ais >/dev/null 2>&1 && eval "$(ais shell-integration 2>/dev/null || true)"
EOF
    
    show_status "Shell集成配置已更新" true
    
    # 安全创建配置文件，保护用户现有配置
    setup_ais_config
}

# 安全设置AIS配置文件
setup_ais_config() {
    local config_dir="$HOME/.config/ais"
    local config_file="$config_dir/config.toml"
    
    # 创建配置目录
    mkdir -p "$config_dir"
    
    # 检查配置文件是否存在
    if [ -f "$config_file" ]; then
        # 检查配置文件是否包含基本配置项
        local needs_update=0
        
        if ! grep -q "auto_analysis" "$config_file" 2>/dev/null; then
            needs_update=1
        fi
        
        if ! grep -q "default_provider" "$config_file" 2>/dev/null; then
            needs_update=1
        fi
        
        if [ $needs_update -eq 1 ]; then
            cp "$config_file" "$config_file.backup.$(date +%s)"
        else
            print_success "配置文件已存在且完整，保持现有配置"
            return 0
        fi
    fi
    
    # 创建或更新配置文件
    cat > "$config_file" << 'EOF'
[general]
auto_analysis = true
default_provider = "default_free"

[providers.default_free]
base_url = "https://api.deepbricks.ai/v1/chat/completions"
model_name = "gpt-4o-mini"
# 默认测试密钥，建议使用 'ais provider-add --help-detail' 配置专属密钥
api_key = "sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg"
EOF
    
    show_status "AIS配置文件已创建" true
}

# 验证安装
verify_installation() {
    # 更新进度条并显示步骤
    update_progress 90 "正在验证安装..."
    
    # 更新PATH - 包括所有可能的路径
    export PATH="/usr/local/bin:$HOME/.local/bin:$PATH"
    hash -r 2>/dev/null || true
    
    # 多重检查ais命令可用性
    local ais_found=0
    
    # 方法1: 直接检查command
    if command_exists ais; then
        ais_found=1
    # 方法2: 检查/usr/local/bin/ais
    elif [ -x "/usr/local/bin/ais" ]; then
        ais_found=1
    # 方法3: 尝试通过Python CLI模块调用
    elif $PYTHON_CMD -c 'from ais.cli import main; main()' --version >/dev/null 2>&1; then
        ais_found=1
        print_info "检测到AIS可通过CLI模块调用"
        # 创建便捷脚本
        cat > /usr/local/bin/ais << EOF
#!/bin/bash
exec $PYTHON_CMD -c "
import sys
from ais.cli import main
sys.exit(main())
" "\$@"
EOF
        chmod +x /usr/local/bin/ais
        show_status "已创建 AIS 便捷命令" true
    fi
    
    if [ $ais_found -eq 0 ]; then
        print_error "安装失败：ais命令不可用"
        print_info "请尝试手动运行: /usr/local/bin/python3.10 -m ais --version"
        return 1
    fi
    
    # 最终进度更新
    PROGRESS_CURRENT=100
    show_status "安装验证完成" true
    return 0
}

# 主安装函数
main() {
    echo -e "${GREEN}🚀 AIS - 上下文感知的错误分析学习助手${NC}"
    echo -e "${BLUE}版本: $AIS_VERSION | GitHub: https://github.com/$GITHUB_REPO${NC}"
    echo
    
    # 初始化进度并检测系统环境
    PROGRESS_CURRENT=0
    update_progress 10 "正在检测系统环境..."
    local env
    env=$(detect_environment)
    local strategy
    strategy=$(detect_install_strategy)
    local system_info
    system_info=$(get_system_info)
    IFS='|' read -r os_name os_version python_version <<< "$system_info"
    
    PROGRESS_CURRENT=10
    show_status "检测到系统: $os_name $os_version, Python: $python_version" true
    
    # 显示安装策略和环境信息
    printf "${GREEN}✓${NC} 安装策略: $strategy\n"
    [ "$strategy" = "compile_python310" ] && printf "${YELLOW}⏱️  ${NC}编译过程可能需要3-5分钟，请耐心等待...\n"
    
    # 显示当前PATH信息（调试用）
    if [ "$DEBUG_MODE" -eq 1 ]; then
        print_info "当前PATH: $PATH"
        print_info "当前用户: $(whoami), UID: $EUID"
    fi
    echo
    
    # 执行健康检查（除非强制重新安装）
    if [ "$FORCE_REINSTALL" -eq 0 ] && perform_health_check "$strategy"; then
        echo -e "${GREEN}✓${NC} 系统健康检查通过！所有组件已正确安装"
        echo
        echo -e "配置Shell集成：${CYAN}source ~/.bashrc && ais setup && source ~/.bashrc${NC}"
        echo -e "配置AI提供商：${CYAN}ais provider-add --help-detail${NC}"
        echo
        return 0
    fi
    
    if [ "$FORCE_REINSTALL" -eq 1 ]; then
        print_warning "强制重新安装模式已启用，将重新安装所有组件"
        echo
    fi
    
    # 执行安装步骤
    # 步骤1：安装系统依赖
    if ! install_system_dependencies "$strategy"; then
        print_error "系统依赖安装失败"
        exit 1
    fi
    
    # 步骤2：设置Python环境  
    if ! setup_python_environment "$strategy"; then
        print_error "Python环境设置失败"
        exit 1
    fi
    
    # 步骤3：安装AIS
    if ! install_ais "$strategy"; then
        print_error "AIS安装失败"
        exit 1
    fi
    
    # 步骤4：设置Shell集成
    if ! setup_shell_integration; then
        print_error "Shell集成设置失败"
        exit 1
    fi
    
    # 验证安装
    if verify_installation; then
        echo
        echo -e "${GREEN}✓${NC} AIS 安装成功完成！"
        echo
        echo -e "配置Shell集成：${CYAN}source ~/.bashrc && ais setup && source ~/.bashrc${NC}"
        echo -e "配置AI提供商：${CYAN}ais provider-add --help-detail${NC}"
        echo
    else
        echo
        print_error "安装失败，请查看错误信息"
        
        # 提供诊断信息
        echo
        echo -e "${YELLOW}📋 诊断信息：${NC}"
        echo -e "• 操作系统：$os_name $os_version"
        echo -e "• 安装策略：$strategy" 
        echo -e "• Python版本：$python_version"
        
        if [ "$strategy" = "compile_python310" ]; then
            local python_status=$($PYTHON_CMD --version 2>/dev/null || echo '未安装')
            local ais_package_status=$($PIP_CMD show ais-terminal >/dev/null 2>&1 && echo '已安装' || echo '未安装')
            local ais_import_status=$($PYTHON_CMD -c 'import ais; print("可导入")' 2>/dev/null || echo '无法导入')
            
            echo -e "• Python 3.10安装：$python_status"
            echo -e "• AIS包状态：$ais_package_status"
            echo -e "• AIS模块导入：$ais_import_status"
            echo -e "• Python命令：$PYTHON_CMD"
            echo -e "• Pip命令：$PIP_CMD"
            echo -e "• 尝试手动运行：${CYAN}$PYTHON_CMD -c 'from ais.cli import main; main()' --version${NC}"
        fi
        
        echo -e "• 当前PATH：$PATH"
        echo
        exit 1
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
        --debug)
            DEBUG_MODE=1
            shift
            ;;
        --force)
            FORCE_REINSTALL=1
            shift
            ;;
        --help)
            echo "AIS 智能安装脚本"
            echo "用法: $0 [--user|--system|--debug|--force|--help]"
            echo "选项:"
            echo "  --user          用户模式安装"
            echo "  --system        系统模式安装"
            echo "  --debug         启用调试模式"
            echo "  --force         强制重新安装所有组件"
            echo "  --help          显示帮助信息"
            echo ""
            echo "支持20+种Linux发行版，自动检测并选择最佳安装策略"
            echo "具备完整的幂等性，支持多次安全执行"
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
# 检测执行方式：直接执行、管道执行、或source执行
if [[ "${BASH_SOURCE[0]}" == "${0}" ]] || [[ -z "${BASH_SOURCE[0]}" ]] || [[ "${0}" == "bash" ]]; then
    # 直接执行脚本文件 或 通过管道执行
    main "$@"
fi