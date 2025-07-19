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

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 进度条配置
PROGRESS_TOTAL=100
PROGRESS_CURRENT=0
PROGRESS_WIDTH=20

# Spinner配置
SPINNER_CHARS=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
SPINNER_SIMPLE=("-" "\\" "|" "/")
SPINNER_ARROWS=("←" "↖" "↑" "↗" "→" "↘" "↓" "↙")
SPINNER_DOTS=("⣾" "⣽" "⣻" "⢿" "⡿" "⣟" "⣯" "⣷")
SPINNER_CURRENT=0
SPINNER_PID=""

# 进度条函数
show_progress() {
    local current=$1
    local total=$2
    local message=$3
    local force_newline=${4:-auto}  # auto, true, false
    local percentage=$((current * 100 / total))
    local filled=$((current * PROGRESS_WIDTH / total))
    local empty=$((PROGRESS_WIDTH - filled))
    
    # 构建进度条
    local bar=""
    for ((i=0; i<filled; i++)); do
        bar+="#"
    done
    for ((i=0; i<empty; i++)); do
        bar+="-"
    done
    
    # 清空整行并在同一行更新显示
    printf "\r\033[K${CYAN}[${bar}] ${percentage}%% ${NC}${message}${NC}"
    
    # 根据参数决定是否换行
    if [ "$force_newline" = "true" ] || ([ "$force_newline" = "auto" ] && [ "$current" -eq "$total" ]); then
        echo
    fi
}

# 更新进度
update_progress() {
    local increment=${1:-5}
    local message=${2:-""}
    PROGRESS_CURRENT=$((PROGRESS_CURRENT + increment))
    if [ $PROGRESS_CURRENT -gt $PROGRESS_TOTAL ]; then
        PROGRESS_CURRENT=$PROGRESS_TOTAL
    fi
    show_progress $PROGRESS_CURRENT $PROGRESS_TOTAL "$message"
}

# 带有Spinner的进度更新
update_progress_with_spinner() {
    local increment=${1:-5}
    local message=${2:-""}
    local spinner_type="${3:-dots}"
    local show_duration=${4:-1}  # 显示时间（秒）
    
    PROGRESS_CURRENT=$((PROGRESS_CURRENT + increment))
    if [ $PROGRESS_CURRENT -gt $PROGRESS_TOTAL ]; then
        PROGRESS_CURRENT=$PROGRESS_TOTAL
    fi
    
    # 简化显示逻辑，避免重复输出
    show_progress_with_spinner $PROGRESS_CURRENT $PROGRESS_TOTAL "$message" "$spinner_type"
    sleep 0.3  # 短暂停留，显示动画效果
    
    # 最后显示静态版本
    show_progress $PROGRESS_CURRENT $PROGRESS_TOTAL "$message"
}

# Spinner函数
show_spinner() {
    local message="$1"
    local spinner_type="${2:-dots}"  # dots, simple, arrows, chars
    local spinner_array
    
    case "$spinner_type" in
        "simple")
            spinner_array=("${SPINNER_SIMPLE[@]}")
            ;;
        "arrows")
            spinner_array=("${SPINNER_ARROWS[@]}")
            ;;
        "chars")
            spinner_array=("${SPINNER_CHARS[@]}")
            ;;
        *)
            spinner_array=("${SPINNER_DOTS[@]}")
            ;;
    esac
    
    local spinner_char="${spinner_array[$SPINNER_CURRENT]}"
    printf "\r\033[K${CYAN}${spinner_char} ${NC}${message}${NC}"
    
    SPINNER_CURRENT=$(( (SPINNER_CURRENT + 1) % ${#spinner_array[@]} ))
}

# 启动后台Spinner
start_spinner() {
    local message="$1"
    local spinner_type="${2:-dots}"
    local interval="${3:-0.1}"
    
    # 停止之前的spinner
    stop_spinner
    
    # 启动新的spinner
    {
        while true; do
            show_spinner "$message" "$spinner_type"
            sleep "$interval"
        done
    } &
    
    SPINNER_PID=$!
    # 禁用作业控制消息
    disown
}

# 停止Spinner
stop_spinner() {
    if [ -n "$SPINNER_PID" ]; then
        kill "$SPINNER_PID" 2>/dev/null || true
        wait "$SPINNER_PID" 2>/dev/null || true
        SPINNER_PID=""
    fi
    # 清空Spinner行
    printf "\r\033[K"
}

# 带有Spinner的进度条显示
show_progress_with_spinner() {
    local current=$1
    local total=$2
    local message=$3
    local spinner_type="${4:-dots}"
    local percentage=$((current * 100 / total))
    local filled=$((current * PROGRESS_WIDTH / total))
    local empty=$((PROGRESS_WIDTH - filled))
    
    # 构建进度条
    local bar=""
    for ((i=0; i<filled; i++)); do
        bar+="#"
    done
    for ((i=0; i<empty; i++)); do
        bar+="-"
    done
    
    # 获取spinner字符
    local spinner_array
    case "$spinner_type" in
        "simple")
            spinner_array=("${SPINNER_SIMPLE[@]}")
            ;;
        "arrows")
            spinner_array=("${SPINNER_ARROWS[@]}")
            ;;
        "chars")
            spinner_array=("${SPINNER_CHARS[@]}")
            ;;
        *)
            spinner_array=("${SPINNER_DOTS[@]}")
            ;;
    esac
    
    local spinner_char="${spinner_array[$SPINNER_CURRENT]}"
    
    # 清空整行并显示进度条和spinner
    printf "\r\033[K${CYAN}[${bar}] ${percentage}%% ${spinner_char} ${NC}${message}${NC}"
    
    # 更新spinner位置
    SPINNER_CURRENT=$(( (SPINNER_CURRENT + 1) % ${#spinner_array[@]} ))
    
    # 如果完成，停止spinner并换行
    if [ "$current" -eq "$total" ]; then
        printf "\r\033[K${CYAN}[${bar}] ${percentage}%% ✓ ${NC}${message}${NC}"
        echo
        SPINNER_CURRENT=0
    fi
}

# 执行带有Spinner的长时间操作
run_with_spinner() {
    local message="$1"
    local command="$2"
    local spinner_type="${3:-dots}"
    local success_message="${4:-$message}"
    
    # 启动spinner
    start_spinner "$message" "$spinner_type"
    
    # 创建临时文件捕获错误输出
    local error_file="/tmp/ais_install_error_$$"
    
    # 执行命令
    if eval "$command" >/dev/null 2>"$error_file"; then
        stop_spinner
        printf "\r\033[K${GREEN}✓ ${NC}${success_message}${NC}\n"
        rm -f "$error_file"
        return 0
    else
        local exit_code=$?
        stop_spinner
        printf "\r\033[K${RED}✗ ${NC}${message} 失败${NC}\n"
        
        # 如果是调试模式或错误文件较小，显示错误信息
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
        
        # 保存错误日志（如果是调试模式）
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

# 诊断编译环境
diagnose_compile_environment() {
    echo
    print_info "🔍 正在诊断编译环境..."
    
    # 检查基本工具
    echo "基本工具检查："
    for tool in gcc make tar wget; do
        if command_exists "$tool"; then
            echo "  ✅ $tool: $(which $tool)"
        else
            echo "  ❌ $tool: 未找到"
        fi
    done
    
    # 检查编译器版本
    echo
    echo "编译器信息："
    if command_exists gcc; then
        echo "  GCC版本: $(gcc --version 2>/dev/null | head -1)"
    fi
    if command_exists make; then
        echo "  Make版本: $(make --version 2>/dev/null | head -1)"
    fi
    
    # 检查系统资源
    echo
    echo "系统资源："
    echo "  CPU核心数: $(nproc 2>/dev/null || echo "未知")"
    echo "  内存信息: $(free -h 2>/dev/null | grep "Mem:" | awk '{print $2" 总计, "$7" 可用"}' || echo "未知")"
    
    # 检查磁盘空间
    local temp_dir="/tmp"
    local available_space=$(df "$temp_dir" 2>/dev/null | tail -1 | awk '{print $4}')
    if [ -n "$available_space" ]; then
        local space_gb=$((available_space / 1024 / 1024))
        echo "  磁盘空间: ${space_gb}GB 可用 (在 $temp_dir)"
        if [ "$space_gb" -lt 2 ]; then
            echo "  ⚠️  磁盘空间可能不足，建议至少2GB"
        fi
    fi
    
    # 检查关键头文件
    echo
    echo "开发库检查："
    for header in "/usr/include/zlib.h" "/usr/include/openssl/ssl.h" "/usr/include/sqlite3.h"; do
        if [ -f "$header" ]; then
            echo "  ✅ $(basename $header): 存在"
        else
            echo "  ❌ $(basename $header): 缺失"
        fi
    done
    
    # 检查Python源码完整性
    if [ -f "Python-3.9.23.tar.xz" ]; then
        echo
        echo "Python源码检查："
        local file_size=$(stat -c%s "Python-3.9.23.tar.xz" 2>/dev/null || echo "0")
        echo "  文件大小: $((file_size / 1024 / 1024))MB"
        if [ "$file_size" -gt 10000000 ]; then  # 大于10MB
            echo "  ✅ 文件大小正常"
        else
            echo "  ❌ 文件大小异常，可能下载不完整"
        fi
    fi
    
    echo
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
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
        echo "compile_python39"  # 需要编译安装Python 3.9.23
        return
    fi
    
    # 根据测试验证结果确定安装策略
    case "$os_name" in
        "ubuntu")
            case "$os_version" in
                "24.04"|"24."*)
                    echo "pipx_native"  # Ubuntu 24.04支持原生pipx
                    ;;
                "22.04"|"22."*)
                    echo "pip_direct"   # Ubuntu 22.04直接用pip
                    ;;
                "20.04"|"20."*)
                    echo "python_upgrade"  # Ubuntu 20.04需要升级Python
                    ;;
                *)
                    echo "pip_direct"
                    ;;
            esac
            ;;
        "debian")
            case "$os_version" in
                "12"|"12."*)
                    echo "pipx_native"  # Debian 12支持原生pipx
                    ;;
                "11"|"11."*)
                    echo "pip_direct"   # Debian 11直接用pip
                    ;;
                *)
                    echo "pip_direct"
                    ;;
            esac
            ;;
        "rocky")
            case "$os_version" in
                "9"|"9."*)
                    echo "pip_direct"   # Rocky Linux 9直接用pip
                    ;;
                "8"|"8."*)
                    echo "python_upgrade"  # Rocky Linux 8需要升级Python
                    ;;
                *)
                    echo "pip_direct"
                    ;;
            esac
            ;;
        "centos")
            case "$os_version" in
                "7"|"7."*)
                    echo "compile_python310"  # CentOS 7需要编译Python 3.10.9
                    ;;
                "8"|"8."*)
                    echo "python_upgrade"  # CentOS 8需要升级Python
                    ;;
                "9"|"9."*)
                    echo "pip_direct"
                    ;;
                *)
                    echo "pip_direct"
                    ;;
            esac
            ;;
        "fedora")
            echo "pip_direct"  # Fedora通常有较新的Python
            ;;
        "openeuler")
            echo "pip_direct"  # openEuler直接用pip
            ;;
        "kylin")
            # Kylin Linux Advanced Server V10需要编译Python 3.10.9
            echo "compile_python310"  # Kylin Linux编译Python 3.10.9
            ;;
        *)
            # 基于Python版本判断
            if [[ "$python_version" == "3.12"* ]] || [[ "$python_version" == "3.11"* ]] || [[ "$python_version" == "3.10"* ]]; then
                # 新版本Python，检查是否支持pipx
                if command_exists pipx || (command_exists apt && apt list pipx 2>/dev/null | grep -q pipx); then
                    echo "pipx_native"
                else
                    echo "pip_direct"
                fi
            elif [[ "$python_version" == "3.9"* ]] || [[ "$python_version" == "3.8"* ]]; then
                echo "pip_direct"
            else
                echo "compile_python39"
            fi
            ;;
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

# 安装系统依赖
install_system_dependencies() {
    local strategy=$1
    # 更新进度条并显示步骤
    show_progress 25 $PROGRESS_TOTAL "正在安装系统依赖..." "true"
    PROGRESS_CURRENT=25
    
    case "$strategy" in
        "compile_python39")
            # 安装编译依赖
            if command_exists yum; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_with_spinner "正在安装编译依赖包..." "sudo yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel git wget tar" "dots" "编译依赖包安装完成"
                else
                    run_with_spinner "正在安装编译依赖包..." "yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel git wget tar" "dots" "编译依赖包安装完成"
                fi
            fi
            ;;
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
                    if [ "$(detect_environment)" = "user" ]; then
                        run_with_spinner "正在安装EPEL源..." "sudo yum install -y epel-release" "dots" "EPEL源安装完成"
                        run_with_spinner "正在安装编译依赖包..." "sudo yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel tk-devel libffi-devel xz-devel openssl11 openssl11-devel openssl11-libs ncurses-devel gdbm-devel db4-devel libpcap-devel expat-devel" "dots" "编译依赖包安装完成"
                    else
                        run_with_spinner "正在安装EPEL源..." "yum install -y epel-release" "dots" "EPEL源安装完成"
                        run_with_spinner "正在安装编译依赖包..." "yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel tk-devel libffi-devel xz-devel openssl11 openssl11-devel openssl11-libs ncurses-devel gdbm-devel db4-devel libpcap-devel expat-devel" "dots" "编译依赖包安装完成"
                    fi
                else
                    # Kylin Linux 或其他系统
                    if [ "$(detect_environment)" = "user" ]; then
                        run_with_spinner "正在安装编译依赖包..." "sudo yum install -y gcc make patch zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel" "dots" "编译依赖包安装完成"
                    else
                        run_with_spinner "正在安装编译依赖包..." "yum install -y gcc make patch zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel" "dots" "编译依赖包安装完成"
                    fi
                fi
            elif command_exists dnf; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_with_spinner "正在安装开发工具..." "sudo dnf groupinstall -y 'Development Tools'" "dots" "开发工具安装完成"
                    run_with_spinner "正在安装依赖库..." "sudo dnf install -y zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel git wget tar" "dots" "依赖库安装完成"
                else
                    run_with_spinner "正在安装开发工具..." "dnf groupinstall -y 'Development Tools'" "dots" "开发工具安装完成"
                    run_with_spinner "正在安装依赖库..." "dnf install -y zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel git wget tar" "dots" "依赖库安装完成"
                fi
            elif command_exists apt-get; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_with_spinner "正在更新软件包列表..." "sudo apt update" "dots" "软件包列表更新完成"
                    run_with_spinner "正在安装编译依赖..." "sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget tar" "dots" "编译依赖安装完成"
                else
                    run_with_spinner "正在更新软件包列表..." "apt update" "dots" "软件包列表更新完成"
                    run_with_spinner "正在安装编译依赖..." "apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget tar" "dots" "编译依赖安装完成"
                fi
            fi
            ;;
        "python_upgrade")
            # 安装Python升级包
            if command_exists dnf; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_with_spinner "正在安装Python 3.9..." "sudo dnf install -y python39 python39-pip" "dots" "Python 3.9安装完成"
                else
                    run_with_spinner "正在安装Python 3.9..." "dnf install -y python39 python39-pip" "dots" "Python 3.9安装完成"
                fi
            elif command_exists apt-get; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_with_spinner "正在更新软件包列表..." "sudo apt update" "dots" "软件包列表更新完成"
                    run_with_spinner "正在安装必要工具..." "sudo apt install -y software-properties-common" "dots" "必要工具安装完成"
                    run_with_spinner "正在添加Python源..." "sudo add-apt-repository -y ppa:deadsnakes/ppa" "dots" "Python源添加完成"
                    run_with_spinner "正在安装Python 3.9..." "sudo apt install -y python3.9 python3.9-venv python3.9-dev" "dots" "Python 3.9安装完成"
                else
                    run_with_spinner "正在更新软件包列表..." "apt update" "dots" "软件包列表更新完成"
                    run_with_spinner "正在安装必要工具..." "apt install -y software-properties-common" "dots" "必要工具安装完成"
                    run_with_spinner "正在添加Python源..." "add-apt-repository -y ppa:deadsnakes/ppa" "dots" "Python源添加完成"
                    run_with_spinner "正在安装Python 3.9..." "apt install -y python3.9 python3.9-venv python3.9-dev" "dots" "Python 3.9安装完成"
                fi
            fi
            ;;
        "pipx_native")
            # 安装pipx
            if command_exists apt-get; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_with_spinner "正在更新软件包列表..." "sudo apt update" "dots" "软件包列表更新完成"
                    run_with_spinner "正在安装pipx..." "sudo apt install -y pipx" "dots" "pipx安装完成"
                else
                    run_with_spinner "正在更新软件包列表..." "apt update" "dots" "软件包列表更新完成"
                    run_with_spinner "正在安装pipx..." "apt install -y pipx" "dots" "pipx安装完成"
                fi
            elif command_exists dnf; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_with_spinner "正在安装pipx..." "sudo dnf install -y pipx" "dots" "pipx安装完成"
                else
                    run_with_spinner "正在安装pipx..." "dnf install -y pipx" "dots" "pipx安装完成"
                fi
            fi
            ;;
    esac
}

# 设置Python环境
setup_python_environment() {
    local strategy=$1
    # 更新进度条并显示步骤
    show_progress 45 $PROGRESS_TOTAL "正在设置Python环境..." "true"
    PROGRESS_CURRENT=45
    
    case "$strategy" in
        "compile_python39")
            # 直接编译安装Python 3.9.23
            local python_prefix="/usr/local/python3.9"
            
            # 检查是否已经安装
            if [ -x "$python_prefix/bin/python3" ]; then
                print_info "Python 3.9.23已经安装"
                export PYTHON_CMD="$python_prefix/bin/python3"
                export PIP_CMD="$python_prefix/bin/python3 -m pip"
                return 0
            fi
            
            # Python 3.9.23 编译安装逻辑...
            ;;
        "compile_python310")
            # 编译安装Python 3.10.9 - 按照成功的手动测试流程
            local python_prefix="/usr/local"
            
            # 检查是否已经安装
            if [ -x "$python_prefix/bin/python3.10" ]; then
                print_info "Python 3.10.9已经安装"
                export PYTHON_CMD="$python_prefix/bin/python3.10"
                export PIP_CMD="$python_prefix/bin/python3.10 -m pip"
                return 0
            fi
            
            
            # 创建临时目录
            local temp_dir="/tmp/python_build"
            mkdir -p "$temp_dir"
            cd "$temp_dir"
            
            # 下载Python 3.10.9源码
            local python_url="https://repo.huaweicloud.com/artifactory/python-local/3.10.9/Python-3.10.9.tgz"
            if ! run_with_spinner "正在下载Python 3.10.9源码..." "wget -q $python_url" "dots" "Python 3.10.9源码下载完成"; then
                print_error "Python源码下载失败"
                return 1
            fi
            
            if ! run_with_spinner "正在解压Python源码..." "tar -xf Python-3.10.9.tgz" "dots" "源码解压完成"; then
                print_error "源码解压失败"
                return 1
            fi
            
            cd "Python-3.10.9"
            
            
            # 检测是否为CentOS 7，需要特殊处理OpenSSL
            local is_centos7=0
            if [ -f "/etc/centos-release" ]; then
                local centos_version=$(cat /etc/centos-release 2>/dev/null | grep -oE '[0-9]+' | head -n1)
                if [ "$centos_version" = "7" ]; then
                    is_centos7=1
                fi
            fi
            
            if [ "$is_centos7" -eq 1 ]; then
                # CentOS 7特殊处理 - 修改configure文件支持OpenSSL 1.1
                if ! run_with_spinner "正在修改configure文件..." "sed -i 's/PKG_CONFIG openssl /PKG_CONFIG openssl11 /g' configure" "dots" "configure文件修改完成"; then
                    print_warning "configure文件修改失败，继续使用默认配置"
                fi
                
                # 配置编译选项
                if ! run_with_spinner "正在配置编译选项..." "./configure --prefix=$python_prefix --with-ensurepip=install" "chars" "编译配置完成"; then
                    print_error "编译配置失败"
                    return 1
                fi
            else
                # Kylin Linux 或其他系统 - 启用优化
                if ! run_with_spinner "正在配置编译选项..." "./configure --prefix=$python_prefix --enable-optimizations --with-ensurepip=install" "chars" "编译配置完成"; then
                    print_error "编译配置失败"
                    return 1
                fi
            fi
            
            local cpu_count=$(nproc 2>/dev/null || echo "2")
            if ! run_with_spinner "正在编译Python 3.10.9..." "make -j$cpu_count" "chars" "Python编译完成"; then
                print_error "Python编译失败"
                return 1
            fi
            
            if [ "$(detect_environment)" = "user" ]; then
                if ! run_with_spinner "正在安装Python到系统..." "sudo make altinstall" "chars" "Python安装完成"; then
                    print_error "Python安装失败"
                    return 1
                fi
            else
                if ! run_with_spinner "正在安装Python到系统..." "make altinstall" "chars" "Python安装完成"; then
                    print_error "Python安装失败"
                    return 1
                fi
            fi
            
            # 验证Python安装
            if [ ! -x "$python_prefix/bin/python3.10" ]; then
                print_error "Python 3.10.9安装不完整"
                return 1
            fi
            
            export PYTHON_CMD="$python_prefix/bin/python3.10"
            export PIP_CMD="$python_prefix/bin/python3.10 -m pip"
            
            # 清理临时文件
            cd /
            rm -rf "$temp_dir"
            
            echo -e "${GREEN}✓ ${NC}Python 3.10.9编译安装完成"
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
    show_progress 75 $PROGRESS_TOTAL "正在安装AIS..." "true"
    PROGRESS_CURRENT=75
    
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
        "compile_python39")
            # 使用编译的Python 3.9.23安装
            run_with_spinner "正在安装AIS..." "$PIP_CMD install ais-terminal" "arrows" "AIS安装完成"
            
            # 创建ais命令的软链接到/usr/local/bin/ais
            local ais_binary=""
            if [ -x "/usr/local/python3.9/bin/ais" ]; then
                ais_binary="/usr/local/python3.9/bin/ais"
            else
                # 查找ais命令位置
                ais_binary=$($PYTHON_CMD -c "import ais, os; print(os.path.dirname(ais.__file__))" 2>/dev/null)/../../../bin/ais
                if [ ! -x "$ais_binary" ]; then
                    ais_binary="/usr/local/python3.9/bin/ais"
                fi
            fi
            
            if [ "$(detect_environment)" = "user" ]; then
                sudo ln -sf "$ais_binary" /usr/local/bin/ais 2>/dev/null || true
            else
                ln -sf "$ais_binary" /usr/local/bin/ais 2>/dev/null || true
            fi
            
            # 验证ais命令可用
            if [ ! -x "/usr/local/bin/ais" ]; then
                print_warning "软链接创建失败，请手动添加Python路径到PATH"
            fi
            ;;
        "compile_python310")
            # 使用编译的Python 3.10.9安装
            run_with_spinner "正在安装AIS..." "$PIP_CMD install ais-terminal" "arrows" "AIS安装完成"
            
            # 验证ais命令可用性
            if [ ! -x "/usr/local/bin/ais" ]; then
                print_warning "AIS命令未安装到/usr/local/bin，请手动添加Python路径到PATH"
            fi
            ;;
        *)
            # 标准pip安装
            run_with_spinner "正在安装AIS..." "$PIP_CMD install ais-terminal" "arrows" "AIS安装完成"
            ;;
    esac
}

# 创建Shell集成脚本
create_integration_script() {
    local script_path="$1"
    
    # 创建目录
    mkdir -p "$(dirname "$script_path")"
    
    # 创建集成脚本
    cat > "$script_path" << 'EOF'
#!/bin/bash
# AIS Shell 集成脚本
# 这个脚本通过 PROMPT_COMMAND 机制捕获命令执行错误

# 检查 AIS 是否可用
_ais_check_availability() {
    command -v ais >/dev/null 2>&1
}

# 检查自动分析是否开启
_ais_check_auto_analysis() {
    if ! _ais_check_availability; then
        return 1
    fi

    # 检查配置文件中的 auto_analysis 设置
    local config_file="$HOME/.config/ais/config.toml"
    if [ -f "$config_file" ]; then
        grep -q "auto_analysis = true" "$config_file" 2>/dev/null
    else
        return 1  # 默认关闭
    fi
}

# precmd 钩子：命令执行后调用
_ais_precmd() {
    local current_exit_code=$?

    # 只处理非零退出码且非中断信号（Ctrl+C 是 130）
    if [ $current_exit_code -ne 0 ] && [ $current_exit_code -ne 130 ]; then
        # 检查功能是否开启
        if _ais_check_auto_analysis; then
            local last_command
            last_command=$(history 1 | sed 's/^[ ]*[0-9]*[ ]*//' 2>/dev/null)

            # 过滤内部命令和特殊情况
            if [[ "$last_command" != *"_ais_"* ]] && \
               [[ "$last_command" != *"ais_"* ]] && \
               [[ "$last_command" != *"history"* ]]; then
                # 调用 ais analyze 进行分析
                echo  # 添加空行分隔
                ais analyze --exit-code "$current_exit_code" \
                    --command "$last_command"
            fi
        fi
    fi
}

# 根据不同 shell 设置钩子
if [ -n "$ZSH_VERSION" ]; then
    # Zsh 设置
    autoload -U add-zsh-hook 2>/dev/null || return
    add-zsh-hook precmd _ais_precmd
elif [ -n "$BASH_VERSION" ]; then
    # Bash 设置
    if [[ -z "$PROMPT_COMMAND" ]]; then
        PROMPT_COMMAND="_ais_precmd"
    else
        PROMPT_COMMAND="_ais_precmd;$PROMPT_COMMAND"
    fi
else
    # 对于其他 shell，提供基本的 PROMPT_COMMAND 支持
    if [[ -z "$PROMPT_COMMAND" ]]; then
        PROMPT_COMMAND="_ais_precmd"
    else
        PROMPT_COMMAND="_ais_precmd;$PROMPT_COMMAND"
    fi
fi
EOF
    
    # 设置执行权限
    chmod 755 "$script_path"
}

# 自动设置Shell集成（用于一键安装脚本）
setup_shell_integration_automatically() {
    # 检测Shell类型
    local shell=$(basename "${SHELL:-/bin/bash}")
    local config_file=""
    
    case "$shell" in
        "bash")
            config_file="$HOME/.bashrc"
            ;;
        "zsh")
            config_file="$HOME/.zshrc"
            ;;
        *)
            config_file="$HOME/.bashrc"
            ;;
    esac
    
    # 创建配置文件（如果不存在）
    [ ! -f "$config_file" ] && touch "$config_file"
    
    # 检查是否已经添加了AIS集成
    if grep -q "# START AIS INTEGRATION" "$config_file" 2>/dev/null; then
        echo -e "${YELLOW}ℹ️  Shell集成配置已存在${NC}"
        return 0
    fi
    
    # 获取AIS集成脚本路径
    local script_path=""
    if command -v python3 >/dev/null 2>&1; then
        script_path=$(python3 -c "
import sys
try:
    import ais
    import os
    package_path = os.path.dirname(ais.__file__)
    script_path = os.path.join(package_path, 'shell', 'integration.sh')
    print(script_path)
except:
    pass
" 2>/dev/null)
    fi
    
    # 如果无法获取路径，尝试查找可能的安装路径
    if [ -z "$script_path" ]; then
        for path in "/usr/local/lib/python"*"/site-packages/ais/shell/integration.sh" \
                   "/usr/lib/python"*"/site-packages/ais/shell/integration.sh" \
                   "$HOME/.local/lib/python"*"/site-packages/ais/shell/integration.sh"; do
            if [ -d "$(dirname "$path")" ]; then
                script_path="$path"
                break
            fi
        done
    fi
    
    # 如果还是找不到路径，使用默认路径
    if [ -z "$script_path" ]; then
        script_path="/usr/local/lib/python3.9/site-packages/ais/shell/integration.sh"
    fi
    
    # 确保集成脚本存在 - 关键修复！
    if [ ! -f "$script_path" ]; then
        echo -e "${BLUE}🔧 正在创建AIS集成脚本...${NC}"
        create_integration_script "$script_path"
        echo -e "${GREEN}✅ 集成脚本创建完成: $script_path${NC}"
    fi
    
    # 确保AIS配置文件存在并启用自动分析
    local ais_config_dir="$HOME/.config/ais"
    local ais_config_file="$ais_config_dir/config.toml"
    
    if [ ! -f "$ais_config_file" ]; then
        echo -e "${BLUE}🔧 正在创建AIS配置文件...${NC}"
        mkdir -p "$ais_config_dir"
        cat > "$ais_config_file" << 'EOF'
# AIS 配置文件
default_provider = "default_free"
auto_analysis = true
context_level = "detailed"
sensitive_dirs = ["~/.ssh", "~/.config/ais", "~/.aws"]

[providers.default_free]
base_url = "https://api.deepbricks.ai/v1/chat/completions"
model_name = "gpt-4o-mini"
api_key = "sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg"
EOF
        echo -e "${GREEN}✅ AIS配置文件创建完成: $ais_config_file${NC}"
    fi
    
    # 添加AIS集成配置
    cat >> "$config_file" << EOF

# START AIS INTEGRATION
# AIS - 上下文感知的错误分析学习助手自动集成
if [ -f "$script_path" ]; then
    source "$script_path"
fi
# END AIS INTEGRATION
EOF
    echo -e "${GREEN}✅ Shell集成配置已添加到: $config_file${NC}"
}

# 设置Shell集成
setup_shell_integration() {
    # 更新进度条并显示步骤
    show_progress 85 $PROGRESS_TOTAL "正在设置Shell集成..." "true"
    PROGRESS_CURRENT=85
    
    # 检测当前Shell
    local shell_name=""
    if [ -n "$ZSH_VERSION" ]; then
        shell_name="zsh"
    elif [ -n "$BASH_VERSION" ]; then
        shell_name="bash"
    else
        case "$SHELL" in
            */zsh) shell_name="zsh" ;;
            */bash) shell_name="bash" ;;
            *) shell_name="bash" ;;
        esac
    fi
    
    # 确定配置文件
    local config_file=""
    case "$shell_name" in
        "zsh")
            config_file="$HOME/.zshrc"
            ;;
        "bash")
            if [ -f "$HOME/.bashrc" ]; then
                config_file="$HOME/.bashrc"
            else
                config_file="$HOME/.bash_profile"
            fi
            ;;
    esac
    
    # 创建配置文件如果不存在
    if [ ! -f "$config_file" ]; then
        touch "$config_file"
    fi
    
    # 检查是否已经添加了AIS集成
    if ! grep -q "# START AIS INTEGRATION" "$config_file" 2>/dev/null; then
        # 获取AIS集成脚本路径
        local ais_script_path=""
        ais_script_path=$($PYTHON_CMD -c "
try:
    import ais, os
    script_path = os.path.join(os.path.dirname(ais.__file__), 'shell', 'integration.sh')
    if os.path.exists(script_path):
        print(script_path)
except:
    pass
" 2>/dev/null)
        
        if [ -n "$ais_script_path" ] && [ -f "$ais_script_path" ]; then
            cat >> "$config_file" << EOF

# START AIS INTEGRATION
# AIS - 上下文感知的错误分析学习助手自动集成
if [ -f "$ais_script_path" ]; then
    source "$ais_script_path"
fi
# END AIS INTEGRATION
EOF
        fi
    fi
}

# 验证安装
verify_installation() {
    # 更新进度条并显示步骤
    show_progress 95 $PROGRESS_TOTAL "正在验证安装..." "true"
    PROGRESS_CURRENT=95
    
    # 更新PATH
    export PATH="$HOME/.local/bin:$PATH"
    hash -r 2>/dev/null || true
    
    # 检查ais命令
    if ! run_with_spinner "正在检查AIS命令..." "command_exists ais" "simple" "AIS命令检查完成"; then
        print_error "安装失败：ais命令不可用"
        return 1
    fi
    
    # 获取版本信息 - 简化版本获取逻辑
    if ! command_exists ais; then
        print_error "安装失败：ais命令不可用"
        return 1
    fi
    
    # 最终进度更新
    show_progress 100 $PROGRESS_TOTAL "安装验证完成" "true"
    PROGRESS_CURRENT=100
    return 0
}

# 主安装函数
main() {
    echo
    echo -e "${CYAN}    ██████╗ ██╗███████╗"
    echo -e "   ██╔══██╗██║██╔════╝"
    echo -e "   ███████║██║███████╗"
    echo -e "   ██╔══██║██║╚════██║"
    echo -e "   ██║  ██║██║███████║"
    echo -e "   ╚═╝  ╚═╝╚═╝╚══════╝${NC}"
    echo
    echo -e "${GREEN}上下文感知的错误分析学习助手 - 智能安装器${NC}"
    echo -e "${BLUE}版本: $AIS_VERSION | GitHub: https://github.com/$GITHUB_REPO${NC}"
    echo
    
    # 初始化进度条
    show_progress 0 $PROGRESS_TOTAL "正在初始化..." "false"
    sleep 0.5
    
    # 检测系统环境
    show_progress 10 $PROGRESS_TOTAL "正在检测系统环境..." "false"
    local env
    env=$(detect_environment)
    local strategy
    strategy=$(detect_install_strategy)
    local system_info
    system_info=$(get_system_info)
    IFS='|' read -r os_name os_version python_version <<< "$system_info"
    
    show_progress 15 $PROGRESS_TOTAL "检测到系统: $os_name $os_version, Python: $python_version" "true"
    PROGRESS_CURRENT=15
    
    # 根据策略显示信息
    case "$strategy" in
        "pipx_native")
            echo -e "${GREEN}✓ ${NC}使用pipx原生安装策略"
            ;;
        "pip_direct")
            echo -e "${GREEN}✓ ${NC}使用pip直接安装策略"
            ;;
        "python_upgrade")
            echo -e "${GREEN}✓ ${NC}使用Python升级安装策略"
            ;;
        "compile_python39")
            echo -e "${GREEN}✓ ${NC}使用Python 3.9.23编译安装策略"
            ;;
        "compile_python310")
            echo -e "${GREEN}✓ ${NC}使用Python 3.10.9编译安装策略"
            echo -e "${YELLOW}⏱️  ${NC}编译过程可能需要3-5分钟，请耐心等待..."
            ;;
    esac
    
    # 执行安装步骤
    install_system_dependencies "$strategy"
    setup_python_environment "$strategy"
    install_ais "$strategy"
    setup_shell_integration
    
    # 验证安装
    if verify_installation; then
        echo
        echo -e "${GREEN}🎉 恭喜！AIS 安装成功完成！${NC}"
        echo -e "${GREEN}------------------------------------------------------------${NC}"
        echo
        
        # 获取版本信息
        local version
        version=$(ais --version 2>/dev/null | head -n1)
        echo -e "${CYAN}📦 版本信息:${NC} $version"
        echo
        # 策略2: 一键安装脚本自动配置
        echo -e "${BLUE}🔧 正在自动配置Shell集成...${NC}"
        
        # 自动执行shell集成配置
        setup_shell_integration_automatically
        
        echo
        echo -e "${GREEN}⚡ 最后一步：让配置立即生效${NC}"
        echo
        echo -e "请执行以下命令："
        echo -e "${CYAN}source ~/.bashrc${NC}"
        echo
        echo -e "${GREEN}✨ 执行后，命令失败时将自动显示AI错误分析！${NC}"
        echo -e "${BLUE}💡 提示：也可以重新打开终端让配置自动生效${NC}"
        echo
        echo -e "${GREEN}🚀 快速测试：${NC}ais ask '你好'"
        echo -e "${GREEN}📖 查看帮助：${NC}ais config --help"
        echo
        echo -e "${GREEN}------------------------------------------------------------${NC}"
        echo
    else
        print_error "安装失败，请查看错误信息"
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
        --help)
            echo "AIS 智能安装脚本 - 优化版"
            echo
            echo "用法: $0 [选项]"
            echo
            echo "安装模式:"
            echo "  (无参数)          自动检测环境并选择最佳安装方式"
            echo "  --user           强制用户级安装"
            echo "  --system         强制系统级安装"
            echo "  --container      强制容器化安装"
            echo
            echo "其他选项:"
            echo "  --non-interactive  非交互模式"
            echo "  --skip-checks      跳过安装后检查"
            echo "  --debug            调试模式，显示详细错误信息"
            echo "  --help            显示此帮助信息"
            echo
            echo "特性:"
            echo "  ✅ 基于实际测试验证的多发行版支持"
            echo "  ✅ 智能检测系统环境并选择最佳安装策略"
            echo "  ✅ 实时进度条显示安装进度"
            echo "  ✅ 支持旧版本系统的自动Python升级"
            echo "  ✅ 一键Shell集成配置"
            echo
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