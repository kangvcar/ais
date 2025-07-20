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

# 进度和状态显示配置
SPINNER="⠋⠙⠹⠸⠼⠴⠦⠧"
SPINNER_PID=""

# 简化的状态显示函数
show_status() {
    local message="$1"
    local success="${2:-false}"
    if [ "$success" = "true" ]; then
        printf "\r\033[K${GREEN}✓${NC} ${message}\n"
    else
        local spinner_char="${SPINNER:$(( $(date +%s) % 8 )):1}"
        printf "\r\033[K${CYAN}${spinner_char}${NC} ${message}"
    fi
}

# 进度更新函数（保持接口兼容）
update_progress() {
    local increment=${1:-5}
    local message=${2:-""}
    show_status "$message"
}

# 带Spinner的进度更新（保持接口兼容）
update_progress_with_spinner() {
    local increment=${1:-5}
    local message=${2:-""}
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
    
    # 显示进行中状态
    show_status "$message"
    
    # 创建临时文件捕获错误输出
    local error_file="/tmp/ais_install_error_$$"
    
    # 执行命令
    if eval "$command" >/dev/null 2>"$error_file"; then
        show_status "$success_message" true
        rm -f "$error_file"
        return 0
    else
        local exit_code=$?
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
        "success") echo -e "${GREEN}✅ ${message}${NC}" ;;
        "warning") echo -e "${YELLOW}⚠️  ${message}${NC}" ;;
        "error") echo -e "${RED}❌ ${message}${NC}" ;;
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
    update_progress 25 "正在安装系统依赖..."
    
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
                    run_pkg_manager "正在安装EPEL源..." "yum install -y epel-release" "EPEL源安装完成"
                    run_pkg_manager "正在安装编译依赖包..." "yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel tk-devel libffi-devel xz-devel openssl11 openssl11-devel openssl11-libs ncurses-devel gdbm-devel db4-devel libpcap-devel expat-devel" "编译依赖包安装完成"
                else
                    # Kylin Linux 或其他系统
                    run_pkg_manager "正在安装编译依赖包..." "yum install -y gcc make patch zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel" "编译依赖包安装完成"
                fi
            elif command_exists dnf; then
                run_pkg_manager "正在安装开发工具..." "dnf groupinstall -y 'Development Tools'" "开发工具安装完成"
                run_pkg_manager "正在安装依赖库..." "dnf install -y zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel git wget tar" "依赖库安装完成"
            elif command_exists apt-get; then
                run_pkg_manager "正在更新软件包列表..." "apt update" "软件包列表更新完成"
                run_pkg_manager "正在安装编译依赖..." "apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget tar" "编译依赖安装完成"
            fi
            ;;
        "python_upgrade")
            # 安装Python升级包
            if command_exists dnf; then
                run_pkg_manager "正在安装Python 3.9..." "dnf install -y python39 python39-pip" "Python 3.9安装完成"
            elif command_exists apt-get; then
                run_pkg_manager "正在更新软件包列表..." "apt update" "软件包列表更新完成"
                run_pkg_manager "正在安装必要工具..." "apt install -y software-properties-common" "必要工具安装完成"
                run_pkg_manager "正在添加Python源..." "add-apt-repository -y ppa:deadsnakes/ppa" "Python源添加完成"
                run_pkg_manager "正在安装Python 3.9..." "apt install -y python3.9 python3.9-venv python3.9-dev" "Python 3.9安装完成"
            fi
            ;;
        "pipx_native")
            # 安装pipx
            if command_exists apt-get; then
                run_pkg_manager "正在更新软件包列表..." "apt update" "软件包列表更新完成"
                run_pkg_manager "正在安装pipx..." "apt install -y pipx" "pipx安装完成"
            elif command_exists dnf; then
                run_pkg_manager "正在安装pipx..." "dnf install -y pipx" "pipx安装完成"
            fi
            ;;
    esac
}

# 设置Python环境
# Python 3.10.9编译安装函数
compile_python310() {
    local python_prefix="/usr/local"
    
    # 检查是否已经安装
    if [ -x "$python_prefix/bin/python3.10" ]; then
        print_info "Python 3.10.9已经安装"
        export PYTHON_CMD="$python_prefix/bin/python3.10"
        export PIP_CMD="$python_prefix/bin/python3.10 -m pip"
        return 0
    fi
    
    # 创建临时目录并下载源码
    local temp_dir="/tmp/python_build"
    mkdir -p "$temp_dir" && cd "$temp_dir"
    
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
        for url in "${python_urls[@]}"; do
            print_info "尝试从源下载：$(echo "$url" | cut -d'/' -f3)"
            for attempt in 1 2; do
                if run_with_spinner "正在下载Python源码(尝试$attempt)..." "wget --timeout=30 --tries=2 -O '$python_file' '$url'" "dots" "源码下载完成"; then
                    local file_size=$(stat -c%s "$python_file" 2>/dev/null || echo 0)
                    if [ "$file_size" -gt 10485760 ]; then  # 验证文件大小而不是SHA256
                        print_success "Python源码下载完成 ($(( file_size / 1024 / 1024 ))MB)"
                        download_success=1
                        break 2
                    else
                        print_warning "下载文件大小异常，重试"
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
    run_with_spinner "正在解压Python源码..." "tar -xf '$python_file'" "dots" "源码解压完成" || return 1
    cd "Python-3.10.9"
    
    # CentOS 7特殊处理
    local is_centos7=0
    [ -f "/etc/centos-release" ] && grep -q "release 7" /etc/centos-release && is_centos7=1
    
    if [ "$is_centos7" -eq 1 ]; then
        run_with_spinner "正在修改configure文件..." "sed -i 's/PKG_CONFIG openssl /PKG_CONFIG openssl11 /g' configure" "dots" "configure修改完成"
        run_with_spinner "正在配置编译选项..." "./configure --prefix=$python_prefix --with-ensurepip=install" "chars" "编译配置完成" || return 1
    else
        run_with_spinner "正在配置编译选项..." "./configure --prefix=$python_prefix --enable-optimizations --with-ensurepip=install" "chars" "编译配置完成" || return 1
    fi
    
    # 编译和安装
    local cpu_cores=$(nproc 2>/dev/null || echo 2)
    run_with_spinner "正在编译Python..." "make -j$cpu_cores" "chars" "Python编译完成" || return 1
    run_with_spinner "正在安装Python..." "make altinstall" "dots" "Python安装完成" || return 1
    
    # 设置环境变量
    export PYTHON_CMD="$python_prefix/bin/python3.10"
    export PIP_CMD="$python_prefix/bin/python3.10 -m pip"
    print_success "Python 3.10.9编译安装完成"
}

setup_python_environment() {
    local strategy=$1
    update_progress 45 "正在设置Python环境..."
    
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
    update_progress 75 "正在安装AIS..."
    
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
    update_progress 85 "正在设置Shell集成..."
    
    # 确定配置文件
    local config_file="$HOME/.bashrc"
    [ -n "$ZSH_VERSION" ] && config_file="$HOME/.zshrc"
    [ ! -f "$config_file" ] && touch "$config_file"
    
    # 检查是否已添加集成
    if grep -q "# AIS INTEGRATION" "$config_file" 2>/dev/null; then
        print_info "Shell集成配置已存在"
        return 0
    fi
    
    # 添加简化的集成配置
    cat >> "$config_file" << 'EOF'

# AIS INTEGRATION
command -v ais >/dev/null 2>&1 && eval "$(ais shell-integration 2>/dev/null || true)"
EOF
    
    # 创建基础配置文件
    mkdir -p "$HOME/.config/ais"
    [ ! -f "$HOME/.config/ais/config.toml" ] && cat > "$HOME/.config/ais/config.toml" << 'EOF'
[general]
auto_analysis = true
default_provider = "default_free"

[providers.default_free]
base_url = "https://api.deepbricks.ai/v1/chat/completions"
model_name = "gpt-4o-mini"
# 默认测试密钥，建议使用 'ais provider-add --help-detail' 配置专属密钥
api_key = "sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg"
EOF
}

# 验证安装
verify_installation() {
    # 更新进度条并显示步骤
    update_progress 95 "正在验证安装..."
    
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
    update_progress 100 "安装验证完成"
    return 0
}

# 主安装函数
main() {
    echo -e "${GREEN}🚀 AIS - 上下文感知的错误分析学习助手${NC}"
    echo -e "${BLUE}版本: $AIS_VERSION | GitHub: https://github.com/$GITHUB_REPO${NC}"
    echo
    
    # 检测系统环境
    update_progress 10 "正在检测系统环境..."
    local env
    env=$(detect_environment)
    local strategy
    strategy=$(detect_install_strategy)
    local system_info
    system_info=$(get_system_info)
    IFS='|' read -r os_name os_version python_version <<< "$system_info"
    
    update_progress 15 "检测到系统: $os_name $os_version, Python: $python_version"
    
    # 显示安装策略
    echo -e "${GREEN}✓${NC} 安装策略: $strategy"
    [ "$strategy" = "compile_python310" ] && echo -e "${YELLOW}⏱️  ${NC}编译过程可能需要3-5分钟，请耐心等待..."
    
    # 执行安装步骤
    install_system_dependencies "$strategy"
    setup_python_environment "$strategy"
    install_ais "$strategy"
    setup_shell_integration
    
    # 验证安装
    if verify_installation; then
        echo
        echo -e "${GREEN}✅ AIS 安装成功完成！${NC}"
        echo
        echo -e "版本信息：$(ais --version 2>/dev/null | head -n1)"
        echo
        echo -e "配置Shell集成：${CYAN}ais setup && source ~/.bashrc${NC}"
        echo -e "配置AI提供商：${CYAN}ais provider-add --help-detail${NC}"
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
            echo "AIS 智能安装脚本"
            echo "用法: $0 [--user|--system|--debug|--help]"
            echo "支持20+种Linux发行版，自动检测并选择最佳安装策略"
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