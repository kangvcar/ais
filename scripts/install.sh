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

# 清理函数
cleanup() {
    echo  # 确保输出换行
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
PROGRESS_WIDTH=25

# 步骤计数器
STEP_COUNTER=0


# 简单进度显示
show_progress() {
    local current=$1
    local total=$2
    local message="$3"
    local percentage=$((current * 100 / total))
    
    # 只在重要节点显示进度
    if [ $((percentage % 10)) -eq 0 ] || [ "$current" -eq "$total" ]; then
        printf "\r\033[2K${CYAN}[进度] ${percentage}%% - ${message}${NC}\n"
    fi
}

# 显示步骤完成
show_step_complete() {
    local step_name="$1"
    STEP_COUNTER=$((STEP_COUNTER + 1))
    printf "\n${GREEN}[步骤 $STEP_COUNTER] ✓ ${step_name}${NC}\n"
}

# 开始任务
start_task() {
    # 忽略大部分参数，只显示任务名
    local task_name="$3"
    if [ -n "$task_name" ]; then
        printf "${BLUE}▶ ${NC}${task_name}\n"
    fi
}

complete_task() {
    local task_name="$1"
    show_step_complete "$task_name"
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






# 静默执行命令
run_command() {
    local message="$1"
    local command="$2"
    local spinner_type="$3"  # 兼容旧参数，但忽略
    local success_message="${4:-$message}"
    
    # 创建临时文件捕获错误输出
    local error_file="/tmp/ais_install_error_$$"
    
    # 执行命令
    if eval "$command" >/dev/null 2>"$error_file"; then
        rm -f "$error_file"
        return 0
    else
        local exit_code=$?
        printf "${RED}✗ ${NC}${message} 失败${NC}\n"
        
        # 如果是调试模式，显示错误信息
        if [ "$DEBUG_MODE" -eq 1 ] && [ -s "$error_file" ]; then
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
    
    # 检测操作系统 - CentOS优先检测
    if [ -f /etc/redhat-release ] && grep -q "CentOS" /etc/redhat-release; then
        os_name="centos"
        os_version=$(grep -oP '\d+(\.\d+)?' /etc/redhat-release | head -1)
    elif [ -f /etc/redhat-release ] && grep -q "Rocky" /etc/redhat-release; then
        os_name="rocky"
        os_version=$(grep -oP '\d+(\.\d+)?' /etc/redhat-release | head -1)
    elif [ -f /etc/os-release ]; then
        . /etc/os-release
        os_name="$ID"
        os_version="$VERSION_ID"
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
    
    # 根据测试验证结果确定安装策略
    # CentOS 7有特殊处理，优先检查
    # 注意：此函数只能输出策略名称，不能有其他输出
    
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
                    # CentOS 7特别检查 - 基于实测验证
                    echo "compile_python310"  # CentOS 7强制使用Python 3.10.9
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
    # 进度将在具体步骤中更新
    
    case "$strategy" in
        "compile_python39")
            # 安装编译依赖
            if command_exists yum; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_command "正在安装编译依赖包..." "sudo yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel git wget tar" "dots" "编译依赖包安装完成"
                else
                    run_command "正在安装编译依赖包..." "yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel git wget tar" "dots" "编译依赖包安装完成"
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
                    update_progress 3 "正在安装EPEL源..."
                    if [ "$(detect_environment)" = "user" ]; then
                        run_command "正在安装EPEL源..." "sudo yum install -y epel-release" "dots" "EPEL源安装完成"
                    else
                        run_command "正在安装EPEL源..." "yum install -y epel-release" "dots" "EPEL源安装完成"
                    fi
                    
                    update_progress 8 "正在安装编译依赖包..."
                    if [ "$(detect_environment)" = "user" ]; then
                        run_command "正在安装编译依赖包..." "sudo yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel tk-devel libffi-devel xz-devel openssl11 openssl11-devel openssl11-libs ncurses-devel gdbm-devel db4-devel libpcap-devel expat-devel" "dots" "编译依赖包安装完成"
                    else
                        run_command "正在安装编译依赖包..." "yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel tk-devel libffi-devel xz-devel openssl11 openssl11-devel openssl11-libs ncurses-devel gdbm-devel db4-devel libpcap-devel expat-devel" "dots" "编译依赖包安装完成"
                    fi
                    complete_task "系统依赖安装 (CentOS 7)"
                else
                    # Kylin Linux 或其他系统
                    if [ "$(detect_environment)" = "user" ]; then
                        run_command "正在安装编译依赖包..." "sudo yum install -y gcc make patch zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel" "dots" "编译依赖包安装完成"
                    else
                        run_command "正在安装编译依赖包..." "yum install -y gcc make patch zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel" "dots" "编译依赖包安装完成"
                    fi
                fi
            elif command_exists dnf; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_command "正在安装开发工具..." "sudo dnf groupinstall -y 'Development Tools'" "dots" "开发工具安装完成"
                    run_command "正在安装依赖库..." "sudo dnf install -y zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel git wget tar" "dots" "依赖库安装完成"
                else
                    run_command "正在安装开发工具..." "dnf groupinstall -y 'Development Tools'" "dots" "开发工具安装完成"
                    run_command "正在安装依赖库..." "dnf install -y zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel git wget tar" "dots" "依赖库安装完成"
                fi
            elif command_exists apt-get; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_command "正在更新软件包列表..." "sudo apt update" "dots" "软件包列表更新完成"
                    run_command "正在安装编译依赖..." "sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget tar" "dots" "编译依赖安装完成"
                else
                    run_command "正在更新软件包列表..." "apt update" "dots" "软件包列表更新完成"
                    run_command "正在安装编译依赖..." "apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget tar" "dots" "编译依赖安装完成"
                fi
            fi
            ;;
        "python_upgrade")
            # 安装Python升级包
            if command_exists dnf; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_command "正在安装Python 3.9..." "sudo dnf install -y python39 python39-pip" "dots" "Python 3.9安装完成"
                else
                    run_command "正在安装Python 3.9..." "dnf install -y python39 python39-pip" "dots" "Python 3.9安装完成"
                fi
            elif command_exists apt-get; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_command "正在更新软件包列表..." "sudo apt update" "dots" "软件包列表更新完成"
                    run_command "正在安装必要工具..." "sudo apt install -y software-properties-common" "dots" "必要工具安装完成"
                    run_command "正在添加Python源..." "sudo add-apt-repository -y ppa:deadsnakes/ppa" "dots" "Python源添加完成"
                    run_command "正在安装Python 3.9..." "sudo apt install -y python3.9 python3.9-venv python3.9-dev" "dots" "Python 3.9安装完成"
                else
                    run_command "正在更新软件包列表..." "apt update" "dots" "软件包列表更新完成"
                    run_command "正在安装必要工具..." "apt install -y software-properties-common" "dots" "必要工具安装完成"
                    run_command "正在添加Python源..." "add-apt-repository -y ppa:deadsnakes/ppa" "dots" "Python源添加完成"
                    run_command "正在安装Python 3.9..." "apt install -y python3.9 python3.9-venv python3.9-dev" "dots" "Python 3.9安装完成"
                fi
            fi
            ;;
        "pipx_native")
            # 安装pipx
            if command_exists apt-get; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_command "正在更新软件包列表..." "sudo apt update" "dots" "软件包列表更新完成"
                    run_command "正在安装pipx..." "sudo apt install -y pipx" "dots" "pipx安装完成"
                else
                    run_command "正在更新软件包列表..." "apt update" "dots" "软件包列表更新完成"
                    run_command "正在安装pipx..." "apt install -y pipx" "dots" "pipx安装完成"
                fi
            elif command_exists dnf; then
                if [ "$(detect_environment)" = "user" ]; then
                    run_command "正在安装pipx..." "sudo dnf install -y pipx" "dots" "pipx安装完成"
                else
                    run_command "正在安装pipx..." "dnf install -y pipx" "dots" "pipx安装完成"
                fi
            fi
            ;;
    esac
}

# 设置Python环境
setup_python_environment() {
    local strategy=$1
    update_progress 15 "正在设置Python环境..."
    
    if [ "$DEBUG_MODE" -eq 1 ]; then
        print_info "调试：设置Python环境，策略=$strategy"
    fi
    
    if [ -z "$strategy" ]; then
        print_error "策略变量为空，无法设置Python环境"
        return 1
    fi
    
    case "$strategy" in
        "compile_python39")
            # 直接编译安装Python 3.9.23
            local python_prefix="/usr/local/python3.9"
            
            # 检查是否已经安装
            if [ -x "$python_prefix/bin/python3.9" ]; then
                print_info "Python 3.9.23已经安装"
                export PYTHON_CMD="$python_prefix/bin/python3.9"
                export PIP_CMD="$python_prefix/bin/pip3.9"
                return 0
            fi
            
            print_warning "Python 3.9编译安装策略未完全实现"
            print_info "建议手动安装更新的Python版本或使用其他系统"
            return 1
            ;;
        "compile_python310")
            # 编译安装Python 3.10.9 - 严格按照测试流程
            local python_prefix="/usr/local/python3.10"
            
            if [ "$DEBUG_MODE" -eq 1 ]; then
                print_info "调试：检查Python 3.10.9安装状态"
                ls -la "$python_prefix/bin/" 2>/dev/null || print_info "调试：目录 $python_prefix/bin/ 不存在"
            fi
            
            # 检查是否已经安装且功能正常
            if [ -x "$python_prefix/bin/python3.10" ] && [ -x "$python_prefix/bin/pip3.10" ]; then
                if [ "$DEBUG_MODE" -eq 1 ]; then
                    print_info "调试：Python 3.10.9和pip已存在，验证功能..."
                fi
                
                # 验证Python和pip功能
                if "$python_prefix/bin/python3.10" -c "import ssl, sqlite3, zlib" 2>/dev/null && \
                   "$python_prefix/bin/pip3.10" --version >/dev/null 2>&1; then
                    print_info "Python 3.10.9已经安装且功能正常"
                    export PYTHON_CMD="$python_prefix/bin/python3.10"
                    export PIP_CMD="$python_prefix/bin/pip3.10"
                    if [ "$DEBUG_MODE" -eq 1 ]; then
                        print_info "调试：使用已安装的Python 3.10.9"
                        print_info "调试：PYTHON_CMD=$PYTHON_CMD"
                        print_info "调试：PIP_CMD=$PIP_CMD"
                    fi
                    return 0
                else
                    print_warning "Python 3.10.9存在但功能异常，将重新编译"
                    if [ "$DEBUG_MODE" -eq 1 ]; then
                        print_info "调试：删除损坏的Python安装"
                        rm -rf "$python_prefix" 2>/dev/null || true
                    fi
                fi
            else
                if [ "$DEBUG_MODE" -eq 1 ]; then
                    print_info "调试：Python 3.10.9未安装，开始编译"
                else
                    print_info "开始编译Python 3.10.9（预计需要5-10分钟）..."
                fi
            fi
            
            update_progress 2 "正在准备编译Python 3.10.9..."
            
            # 创建临时目录
            local temp_dir="/tmp/python_build"
            mkdir -p "$temp_dir"
            cd "$temp_dir"
            
            # 下载Python 3.10.9源码
            update_progress 5 "正在下载Python 3.10.9源码..."
            local python_url="https://repo.huaweicloud.com/artifactory/python-local/3.10.9/Python-3.10.9.tgz"
            if ! run_command "正在下载Python 3.10.9源码..." "wget -q $python_url" "dots" "Python源码下载完成"; then
                print_error "Python源码下载失败"
                return 1
            fi
            
            update_progress 3 "正在解压源码..."
            if ! run_command "正在解压Python源码..." "tar -xf Python-3.10.9.tgz" "dots" "源码解压完成"; then
                print_error "源码解压失败"
                return 1
            fi
            
            cd "Python-3.10.9"
            
            update_progress 5 "正在配置编译选项..."
            
            # 检测是否为CentOS 7，需要特殊处理OpenSSL
            local is_centos7=0
            if [ -f "/etc/centos-release" ]; then
                local centos_version=$(cat /etc/centos-release 2>/dev/null | grep -oE '[0-9]+' | head -n1)
                if [ "$centos_version" = "7" ]; then
                    is_centos7=1
                fi
            fi
            
            if [ "$is_centos7" -eq 1 ]; then
                # CentOS 7特殊处理 - 严格按照实测成功步骤
                if ! run_command "正在修改configure文件支持OpenSSL 1.1..." "sed -i 's/PKG_CONFIG openssl /PKG_CONFIG openssl11 /g' configure" "dots" "configure文件修改完成"; then
                    print_warning "configure文件修改失败，继续使用默认配置"
                fi
                
                # 按照实测步骤：先单独执行configure，但需要指定prefix
                if ! run_command "正在执行configure配置..." "./configure --prefix=$python_prefix --with-ensurepip=install" "chars" "configure执行完成"; then
                    print_error "configure执行失败"
                    return 1
                fi
            else
                # Kylin Linux 或其他系统 - 启用优化
                if ! run_command "正在配置编译选项..." "./configure --prefix=$python_prefix --enable-optimizations --with-ensurepip=install" "chars" "编译配置完成"; then
                    print_error "编译配置失败"
                    return 1
                fi
            fi
            
            update_progress 25 "正在编译Python 3.10.9（这可能需要几分钟）..."
            # CentOS 7按照实测步骤使用单线程make，其他系统可以使用多线程
            if [ "$is_centos7" -eq 1 ]; then
                if ! run_command "正在编译Python 3.10.9..." "make" "chars" "Python编译完成"; then
                    print_error "Python编译失败"
                    return 1
                fi
            else
                local cpu_count=$(nproc 2>/dev/null || echo "2")
                if ! run_command "正在编译Python 3.10.9..." "make -j$cpu_count" "chars" "Python编译完成"; then
                    print_error "Python编译失败"
                    return 1
                fi
            fi
            
            update_progress 10 "正在安装Python到系统..."
            if [ "$(detect_environment)" = "user" ]; then
                if ! run_command "正在安装Python到系统..." "sudo make altinstall" "chars" "Python安装完成"; then
                    print_error "Python安装失败"
                    return 1
                fi
            else
                if ! run_command "正在安装Python到系统..." "make altinstall" "chars" "Python安装完成"; then
                    print_error "Python安装失败"
                    return 1
                fi
            fi
            
            # 验证Python安装
            if [ ! -x "$python_prefix/bin/python3.10" ]; then
                print_error "Python 3.10.9安装不完整"
                if [ "$DEBUG_MODE" -eq 1 ]; then
                    print_info "调试：检查可能的安装位置"
                    print_info "调试：期望位置 $python_prefix/bin/python3.10"
                    find /usr/local -name "python3.10" -type f 2>/dev/null || print_info "调试：未找到python3.10文件"
                    print_info "调试：检查所有Python相关文件："
                    find /usr/local -name "python*" -type f 2>/dev/null | head -10 || print_info "调试：未找到Python文件"
                fi
                return 1
            fi
            
            # 验证Python功能性
            if ! "$python_prefix/bin/python3.10" -c "import ssl, sqlite3, zlib" 2>/dev/null; then
                print_warning "Python安装可能缺少某些模块，但将继续安装"
            fi
            
            # 验证pip是否可用
            if [ ! -x "$python_prefix/bin/pip3.10" ]; then
                print_warning "pip3.10不存在，尝试使用python -m pip"
                export PYTHON_CMD="$python_prefix/bin/python3.10"
                export PIP_CMD="$python_prefix/bin/python3.10 -m pip"
            else
                export PYTHON_CMD="$python_prefix/bin/python3.10"
                export PIP_CMD="$python_prefix/bin/pip3.10"
            fi
            
            # 最终验证pip命令
            if ! $PIP_CMD --version >/dev/null 2>&1; then
                print_error "pip命令验证失败，Python安装可能有问题"
                if [ "$DEBUG_MODE" -eq 1 ]; then
                    print_info "调试信息："
                    print_info "  PYTHON_CMD: $PYTHON_CMD"
                    print_info "  PIP_CMD: $PIP_CMD"
                    print_info "  Python路径: $python_prefix"
                    print_info "  Python可执行文件: $(ls -la $python_prefix/bin/python* 2>/dev/null || echo '无')"
                    print_info "  Pip文件: $(ls -la $python_prefix/bin/pip* 2>/dev/null || echo '无')"
                fi
                return 1
            fi
            
            if [ "$DEBUG_MODE" -eq 1 ]; then
                print_info "Python环境验证成功："
                print_info "  PYTHON_CMD: $PYTHON_CMD"
                print_info "  PIP_CMD: $PIP_CMD"
                print_info "  Pip版本: $($PIP_CMD --version)"
            else
                print_info "Python 3.10.9环境配置完成"
            fi
            
            # 在CentOS 7上创建python3.10的软链接到更通用的路径
            if [ "$is_centos7" -eq 1 ]; then
                if [ "$(detect_environment)" = "user" ]; then
                    sudo ln -sf "$python_prefix/bin/python3.10" /usr/local/bin/python3.10 2>/dev/null || true
                    sudo ln -sf "$python_prefix/bin/pip3.10" /usr/local/bin/pip3.10 2>/dev/null || true
                else
                    ln -sf "$python_prefix/bin/python3.10" /usr/local/bin/python3.10 2>/dev/null || true
                    ln -sf "$python_prefix/bin/pip3.10" /usr/local/bin/pip3.10 2>/dev/null || true
                fi
            fi
            
            # 清理临时文件
            cd /
            rm -rf "$temp_dir"
            
            complete_task "Python 3.10.9编译安装"
            print_info "Python 3.10.9编译安装完成"
            ;;
        "python_upgrade")
            # 使用升级的Python版本
            export PYTHON_CMD="python3.9"
            export PIP_CMD="python3.9 -m pip"
            ;;
        "")
            # 策略为空，无法继续
            print_error "安装策略为空，无法设置Python环境"
            return 1
            ;;
        *)
            # 未知策略
            print_error "未知的安装策略: $strategy"
            return 1
            ;;
    esac
}

# 安装AIS
install_ais() {
    local strategy=$1
    update_progress 5 "正在安装AIS应用..."
    
    case "$strategy" in
        "pipx_native")
            # 使用pipx安装
            if ! command_exists pipx; then
                run_command "正在安装pipx..." "$PIP_CMD install --user pipx" "dots" "pipx安装完成"
                pipx ensurepath >/dev/null 2>&1
                export PATH="$HOME/.local/bin:$PATH"
            fi
            
            if pipx list | grep -q "ais-terminal"; then
                update_progress 5 "正在更新AIS到最新版本..."
                run_command "正在更新AIS到最新版本..." "pipx upgrade ais-terminal" "arrows" "AIS更新完成"
            else
                run_command "正在安装AIS..." "pipx install ais-terminal" "arrows" "AIS安装完成"
            fi
            pipx ensurepath >/dev/null 2>&1
            ;;
        "compile_python39")
            # 使用编译的Python 3.9.23安装
            # 验证PIP_CMD是否正确设置
            if [ -z "$PIP_CMD" ] || ! command -v "$PIP_CMD" >/dev/null 2>&1; then
                print_warning "PIP_CMD未正确设置，尝试使用备用方案"
                if [ -x "/usr/local/python3.9/bin/pip3.9" ]; then
                    export PIP_CMD="/usr/local/python3.9/bin/pip3.9"
                elif [ -x "/usr/local/python3.9/bin/python3.9" ]; then
                    export PIP_CMD="/usr/local/python3.9/bin/python3.9 -m pip"
                else
                    print_error "无法找到有效的pip命令"
                    return 1
                fi
            fi
            
            run_command "正在安装AIS..." "$PIP_CMD install ais-terminal" "arrows" "AIS安装完成"
            
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
            if [ -x "/usr/local/bin/ais" ]; then
                print_info "AIS命令已创建软链接: /usr/local/bin/ais"
            else
                print_warning "软链接创建失败，请手动添加Python路径到PATH"
            fi
            ;;
        "compile_python310")
            # 使用编译的Python 3.10.9安装
            # 验证PIP_CMD是否正确设置
            if [ -z "$PIP_CMD" ] || ! command -v "$PIP_CMD" >/dev/null 2>&1; then
                print_warning "PIP_CMD未正确设置，尝试使用备用方案"
                if [ -x "/usr/local/python3.10/bin/pip3.10" ]; then
                    export PIP_CMD="/usr/local/python3.10/bin/pip3.10"
                elif [ -x "/usr/local/python3.10/bin/python3.10" ]; then
                    export PIP_CMD="/usr/local/python3.10/bin/python3.10 -m pip"
                else
                    print_error "无法找到有效的pip命令"
                    return 1
                fi
            fi
            
            run_command "正在安装AIS..." "$PIP_CMD install ais-terminal" "arrows" "AIS安装完成"
            
            # 创建ais命令的软链接到/usr/local/bin/ais
            local ais_binary=""
            if [ -x "/usr/local/python3.10/bin/ais" ]; then
                ais_binary="/usr/local/python3.10/bin/ais"
            else
                # 查找ais命令位置
                ais_binary=$($PYTHON_CMD -c "import ais, os; print(os.path.dirname(ais.__file__))" 2>/dev/null)/../../../bin/ais
                if [ ! -x "$ais_binary" ]; then
                    ais_binary="/usr/local/python3.10/bin/ais"
                fi
            fi
            
            if [ "$(detect_environment)" = "user" ]; then
                sudo ln -sf "$ais_binary" /usr/local/bin/ais 2>/dev/null || true
            else
                ln -sf "$ais_binary" /usr/local/bin/ais 2>/dev/null || true
            fi
            
            # 验证ais命令可用
            if [ -x "/usr/local/bin/ais" ]; then
                print_info "AIS命令已创建软链接: /usr/local/bin/ais"
            else
                print_warning "软链接创建失败，请手动添加Python路径到PATH"
            fi
            ;;
        *)
            # 标准pip安装
            run_command "正在安装AIS..." "$PIP_CMD install ais-terminal" "arrows" "AIS安装完成"
            ;;
    esac
    complete_task "AIS应用安装"
}

# 设置Shell集成
setup_shell_integration() {
    update_progress 3 "正在设置Shell集成..."
    
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
    complete_task "Shell集成配置"
}

# 验证安装
verify_installation() {
    start_task 3 "verify" "正在验证安装..."
    
    # 更新PATH
    export PATH="$HOME/.local/bin:$PATH"
    hash -r 2>/dev/null || true
    
    # 检查ais命令
    update_progress 1 "正在检查AIS命令..."
    if ! command_exists ais; then
        print_error "安装失败：ais命令不可用"
        return 1
    fi
    
    update_progress 1 "正在验证版本信息..."
    
    # 获取版本信息
    local version
    if ! version=$(ais --version 2>/dev/null | head -n1); then
        print_error "安装失败：无法获取版本信息"
        return 1
    fi
    
    # 确保进度条达到100%
    update_progress 0 "安装验证完成"
    complete_task "安装验证"
    return 0
}

# 主安装函数
main() {
    echo "================================================"
    echo "         AIS - 上下文感知的错误分析学习助手 安装器"
    echo "              基于多发行版测试验证优化"
    echo "================================================"
    echo "版本: $AIS_VERSION"
    echo "GitHub: https://github.com/$GITHUB_REPO"
    echo
    
    # 初始化进度系统
    echo
    start_task 1 "init" "正在初始化安装程序..."
    sleep 0.5
    
    # 检测系统环境 (2-5%)
    start_task 2 "detect_env" "正在检测系统环境..."
    local env
    env=$(detect_environment)
    
    update_progress 1 "正在分析安装策略..."
    local strategy
    strategy=$(detect_install_strategy)
    
    update_progress 1 "正在获取系统信息..."
    local system_info
    system_info=$(get_system_info)
    IFS='|' read -r os_name os_version python_version <<< "$system_info"
    
    complete_task "系统检测: $os_name $os_version, Python: $python_version"
    
    if [ "$DEBUG_MODE" -eq 1 ]; then
        print_info "调试：环境类型=$env"
        print_info "调试：安装策略=$strategy"
        print_info "调试：系统信息=$system_info"
        print_info "调试：策略检测 - os_name='$os_name', os_version='$os_version', python_version='$python_version'"
        if [ "$strategy" = "compile_python310" ]; then
            print_info "调试：匹配到CentOS 7分支，使用Python 3.10.9编译策略"
        fi
    fi
    
    # 显示安装策略 (6%)
    start_task 1 "strategy" "正在准备安装策略..."
    case "$strategy" in
        "pipx_native")
            update_progress 0 "策略: pipx原生安装"
            ;;
        "pip_direct")
            update_progress 0 "策略: pip直接安装"
            ;;
        "python_upgrade")
            update_progress 0 "策略: Python升级安装"
            ;;
        "compile_python39")
            update_progress 0 "策略: Python 3.9.23编译安装"
            ;;
        "compile_python310")
            update_progress 0 "策略: Python 3.10.9编译安装"
            if [ "$DEBUG_MODE" -eq 1 ]; then
                print_info "检测到CentOS 7系统（Python $python_version），基于实测验证："
                print_info "  • 使用华为云镜像源加速下载"
                print_info "  • 专门配置OpenSSL 1.1支持"
                print_info "  • 完整的依赖包安装"
                print_info "  • 严格按照实测成功的编译步骤执行"
            else
                print_info "CentOS 7系统检测完成，将编译安装Python 3.10.9"
            fi
            ;;
    esac
    complete_task "安装策略: $strategy"
    
    # 执行安装步骤
    if [ "$DEBUG_MODE" -eq 1 ]; then
        print_info "调试：开始执行安装步骤，策略=$strategy"
    fi
    
    # 安装系统依赖 (7-20%)
    start_task 1 "dependencies" "正在安装系统依赖..."
    install_system_dependencies "$strategy"
    
    # 设置Python环境 (21-80%)
    start_task 1 "python_env" "正在设置Python环境..."
    setup_python_environment "$strategy"
    
    # 安装AIS (81-90%)
    start_task 1 "install_ais" "正在安装AIS应用..."
    install_ais "$strategy"
    
    # 设置Shell集成 (91-95%)
    start_task 1 "shell_integration" "正在配置Shell集成..."
    setup_shell_integration
    
    # 验证安装
    if verify_installation; then
        echo
        print_success "🎉 AIS安装成功！"
        
        # 获取版本信息
        local version
        version=$(ais --version 2>/dev/null | head -n1)
        print_info "版本: $version"
        
        echo
        print_warning "🔧 重要：请按以下步骤完成配置："
        
        # 根据安装策略提供不同的后续步骤
        case "$strategy" in
            "compile_python310")
                print_info "   1. 运行: ais setup"
                print_info "   2. 重新加载环境: source ~/.bashrc"
                print_info "   💡 Python 3.10.9已安装到: /usr/local/python3.10/"
                print_info "   💡 按照您的实测步骤，AIS应该已经正确安装"
                ;;
            "compile_python39")
                print_info "   1. 首先运行: python3.9 -m pip install ais-terminal" 
                print_info "   2. 然后运行: ais setup"
                print_info "   3. 重新加载环境: source ~/.bashrc"
                print_info "   💡 Python 3.9已安装到: /usr/local/python3.9/"
                ;;
            *)
                print_info "   1. 首先运行: ais setup"
                print_info "   2. 然后运行: source ~/.bashrc  # 或 source ~/.zshrc"
                print_info "   3. 或者直接重新打开终端"
                ;;
        esac
        
        echo
        print_info "✨ 配置完成后，命令失败时将自动显示AI分析！"
        echo
        print_info "🚀 快速测试: ais ask '你好'"
        print_info "📖 配置帮助: ais config --help"
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

# 运行主函数（只在直接执行时运行）
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi