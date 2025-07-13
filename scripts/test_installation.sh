#!/bin/bash
# AIS 安装测试脚本
# 全面测试各种安装方式和功能

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
print_step() { echo -e "${BLUE}📋 测试 $1: $2${NC}"; }

# 测试结果统计
TESTS_TOTAL=0
TESTS_PASSED=0
TESTS_FAILED=0

# 运行测试函数
run_test() {
    local test_name="$1"
    local test_cmd="$2"
    local expected_result="${3:-0}"  # 默认期望返回值为0
    
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    print_step "$TESTS_TOTAL" "$test_name"
    
    if eval "$test_cmd" >/dev/null 2>&1; then
        local result=$?
        if [ $result -eq $expected_result ]; then
            TESTS_PASSED=$((TESTS_PASSED + 1))
            print_success "$test_name"
        else
            TESTS_FAILED=$((TESTS_FAILED + 1))
            print_error "$test_name (返回值: $result, 期望: $expected_result)"
        fi
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        print_error "$test_name (执行失败)"
    fi
}

# 运行带输出的测试
run_test_with_output() {
    local test_name="$1"
    local test_cmd="$2"
    local expected_pattern="$3"
    
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    print_step "$TESTS_TOTAL" "$test_name"
    
    local output
    if output=$(eval "$test_cmd" 2>&1); then
        if [[ "$output" =~ $expected_pattern ]]; then
            TESTS_PASSED=$((TESTS_PASSED + 1))
            print_success "$test_name"
        else
            TESTS_FAILED=$((TESTS_FAILED + 1))
            print_error "$test_name (输出不匹配)"
            echo "  期望匹配: $expected_pattern"
            echo "  实际输出: $output"
        fi
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        print_error "$test_name (执行失败)"
        echo "  错误输出: $output"
    fi
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 清理函数
cleanup() {
    print_info "🧹 清理测试环境..."
    
    # 卸载可能的测试安装
    if command_exists pipx; then
        pipx uninstall ais-terminal 2>/dev/null || true
    fi
    
    # 清理配置文件
    rm -rf ~/.config/ais 2>/dev/null || true
    rm -rf ~/.local/share/ais 2>/dev/null || true
    rm -rf ~/.cache/ais 2>/dev/null || true
    
    print_success "测试环境清理完成"
}

# 测试基础环境
test_environment() {
    print_info "🔍 测试基础环境..."
    
    run_test "Python可用性" "python3 --version"
    run_test "pip可用性" "python3 -m pip --version"
    run_test "curl可用性" "curl --version"
    run_test "git可用性" "git --version"
    
    # 测试网络连接
    run_test "PyPI连接" "curl -s -I https://pypi.org/simple/ais-terminal/ | head -n1 | grep -q '200'"
}

# 测试pipx用户级安装
test_pipx_user_install() {
    print_info "👤 测试pipx用户级安装..."
    
    # 清理环境
    cleanup
    
    # 安装pipx（如果需要）
    if ! command_exists pipx; then
        print_info "安装pipx..."
        python3 -m pip install --user pipx
        python3 -m pipx ensurepath
        export PATH="$HOME/.local/bin:$PATH"
    fi
    
    # 测试安装
    run_test "pipx用户级安装" "pipx install ais-terminal"
    run_test "ais命令可用" "command -v ais"
    run_test_with_output "ais版本检查" "ais --version" "ais.*0\\.1\\.0"
    run_test "ais配置命令" "ais config --help"
    
    # 测试shell集成
    run_test "shell集成设置" "ais setup"
    
    # 卸载测试
    run_test "pipx卸载" "pipx uninstall ais-terminal"
}

# 测试安装脚本
test_install_script() {
    print_info "📜 测试安装脚本..."
    
    # 清理环境
    cleanup
    
    # 测试脚本语法
    run_test "安装脚本语法检查" "bash -n scripts/install.sh"
    
    # 测试脚本帮助
    run_test_with_output "安装脚本帮助" "bash scripts/install.sh --help" "AIS.*智能安装脚本"
    
    # 测试用户级安装
    if [ "$CI" != "true" ]; then  # 跳过CI环境中的实际安装测试
        run_test "脚本用户级安装" "bash scripts/install.sh --user --skip-checks"
        
        if command_exists ais; then
            run_test_with_output "脚本安装验证" "ais --version" "ais.*0\\.1\\.0"
            run_test "脚本安装卸载" "bash scripts/uninstall.sh --force"
        fi
    else
        print_warning "跳过CI环境中的实际安装测试"
    fi
}

# 测试Docker安装脚本
test_docker_script() {
    print_info "🐳 测试Docker安装脚本..."
    
    # 测试脚本语法
    run_test "Docker脚本语法检查" "bash -n scripts/docker-install.sh"
    
    # 测试脚本帮助
    run_test_with_output "Docker脚本帮助" "bash scripts/docker-install.sh --help" "AIS.*Docker.*安装脚本"
    
    # 如果有Docker，测试构建
    if command_exists docker; then
        run_test "Dockerfile语法检查" "docker build --dry-run -f Dockerfile ."
        
        # 在CI环境中可能没有权限构建镜像
        if [ "$CI" != "true" ]; then
            run_test "Docker镜像构建" "docker build -t ais-test ."
            if [ $? -eq 0 ]; then
                run_test "Docker容器运行" "docker run --rm ais-test ais --version"
                run_test "Docker镜像清理" "docker rmi ais-test"
            fi
        fi
    else
        print_warning "Docker未安装，跳过Docker相关测试"
    fi
}

# 测试卸载脚本
test_uninstall_script() {
    print_info "🗑️  测试卸载脚本..."
    
    # 测试脚本语法
    run_test "卸载脚本语法检查" "bash -n scripts/uninstall.sh"
    
    # 测试脚本帮助
    run_test_with_output "卸载脚本帮助" "bash scripts/uninstall.sh --help" "AIS.*智能卸载脚本"
}

# 测试文档完整性
test_documentation() {
    print_info "📚 测试文档完整性..."
    
    run_test "README.md存在" "[ -f README.md ]"
    run_test "安装文档存在" "[ -f docs/INSTALLATION.md ]"
    run_test "快速开始存在" "[ -f docs/QUICK_START.md ]"
    run_test "Docker指南存在" "[ -f docs/DOCKER_GUIDE.md ]"
    run_test "开发指南存在" "[ -f docs/DEVELOPMENT.md ]"
    run_test "更新日志存在" "[ -f docs/CHANGELOG.md ]"
    
    # 检查文档链接
    run_test_with_output "README链接检查" "grep -o 'docs/[A-Z_]*.md' README.md | head -1" "docs/.*\\.md"
}

# 测试项目配置
test_project_config() {
    print_info "⚙️  测试项目配置..."
    
    run_test "pyproject.toml存在" "[ -f pyproject.toml ]"
    run_test "pyproject.toml语法" "python3 -c 'import tomllib; tomllib.load(open(\"pyproject.toml\", \"rb\"))'" 2>/dev/null || \
        run_test "pyproject.toml语法(fallback)" "python3 -c 'import toml; toml.load(\"pyproject.toml\")'"
    
    run_test "包结构检查" "[ -d src/ais ]"
    run_test "CLI模块存在" "[ -f src/ais/cli/main.py ]"
    run_test "核心模块存在" "[ -f src/ais/core/ai.py ]"
    
    run_test "测试目录存在" "[ -d tests ]"
    run_test "Docker配置存在" "[ -f Dockerfile ]"
    run_test "Docker Compose存在" "[ -f docker-compose.yml ]"
}

# 显示测试结果
show_results() {
    echo
    echo "================================================"
    echo "              测试结果汇总"
    echo "================================================"
    echo -e "总测试数: ${BLUE}$TESTS_TOTAL${NC}"
    echo -e "通过: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "失败: ${RED}$TESTS_FAILED${NC}"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "结果: ${GREEN}✅ 所有测试通过${NC}"
        return 0
    else
        echo -e "结果: ${RED}❌ 有 $TESTS_FAILED 个测试失败${NC}"
        return 1
    fi
}

# 主函数
main() {
    echo "================================================"
    echo "           AIS 安装测试套件"
    echo "================================================"
    echo "全面测试各种安装方式和功能"
    echo
    
    # 检查是否在项目根目录
    if [ ! -f "pyproject.toml" ] || ! grep -q "ais-terminal" pyproject.toml; then
        print_error "请在AIS项目根目录运行此脚本"
        exit 1
    fi
    
    # 运行所有测试
    test_environment
    test_project_config
    test_documentation
    test_uninstall_script
    test_docker_script
    
    # 根据环境决定是否运行安装测试
    if [ "${SKIP_INSTALL_TESTS:-}" != "1" ]; then
        test_install_script
        test_pipx_user_install
    else
        print_warning "跳过安装测试 (SKIP_INSTALL_TESTS=1)"
    fi
    
    # 显示结果
    show_results
}

# 处理命令行参数
case "${1:-}" in
    --help|-h)
        echo "AIS 安装测试脚本"
        echo
        echo "用法: $0 [选项]"
        echo
        echo "选项:"
        echo "  --help, -h     显示帮助信息"
        echo "  --cleanup      只执行清理操作"
        echo
        echo "环境变量:"
        echo "  SKIP_INSTALL_TESTS=1  跳过实际安装测试"
        echo "  CI=true              CI环境模式"
        exit 0
        ;;
    --cleanup)
        cleanup
        exit 0
        ;;
esac

# 设置错误处理
trap 'echo "测试过程中发生错误，正在清理..."; cleanup; exit 1' ERR

# 运行主函数
main