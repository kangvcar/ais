#!/bin/bash

# AIS 安装测试脚本
# 测试各种安装方式和功能

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
    
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    print_step "$TESTS_TOTAL" "$test_name"
    
    if eval "$test_cmd" >/dev/null 2>&1; then
        print_success "$test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_error "$test_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# 测试安装流程
test_installation() {
    echo "================================================"
    echo "         AIS 安装测试套件"
    echo "================================================"
    echo
    
    # 基本命令测试
    run_test "AIS 命令可用性" "command -v ais"
    run_test "AIS 版本显示" "ais --version"
    run_test "AIS 帮助信息" "ais --help"
    run_test "AIS 配置命令" "ais config"
    
    # 功能测试
    run_test "开启自动分析" "ais on"
    run_test "关闭自动分析" "ais off"
    run_test "列出服务商" "ais list-provider"
    run_test "查看历史记录" "ais history"
    run_test "学习命令可用" "ais learn --help"
    run_test "建议命令可用" "ais suggest --help"
    
    # 配置测试
    run_test "配置设置" "ais config --set test_key=test_value"
    run_test "配置获取" "ais config --get test_key"
    
    # 文件结构测试
    run_test "配置目录存在" "[ -d ~/.config/ais ]"
    run_test "数据目录存在" "[ -d ~/.local/share/ais ]"
    run_test "集成脚本存在" "grep -q 'START AIS INTEGRATION' ~/.bashrc"
    
    # Python 模块测试
    run_test "Python 模块导入" "python3 -c 'import ais; print(ais.__version__)'"
    run_test "CLI 模块可用" "python3 -m ais.cli --version"
    
    # 安装脚本测试
    run_test "安装脚本存在" "[ -f install.sh ]"
    run_test "卸载脚本存在" "[ -f uninstall.sh ]"
    run_test "发布脚本存在" "[ -f release.sh ]"
    
    # 构建测试
    print_step "$((TESTS_TOTAL + 1))" "包构建测试"
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    if python3 -m build --help >/dev/null 2>&1; then
        print_info "尝试构建包..."
        if python3 -m build >/dev/null 2>&1; then
            print_success "包构建测试"
            TESTS_PASSED=$((TESTS_PASSED + 1))
            
            # 检查构建文件
            if [ -d "dist" ] && [ -n "$(ls dist/*.whl 2>/dev/null)" ]; then
                print_info "✓ Wheel 文件已生成"
            fi
            if [ -d "dist" ] && [ -n "$(ls dist/*.tar.gz 2>/dev/null)" ]; then
                print_info "✓ 源码包已生成"
            fi
        else
            print_error "包构建测试"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        print_warning "build 模块未安装，跳过构建测试"
        TESTS_TOTAL=$((TESTS_TOTAL - 1))
    fi
}

# 测试AI功能（可选）
test_ai_functionality() {
    print_step "$((TESTS_TOTAL + 1))" "AI 功能测试"
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    
    # 测试基本AI问答（这可能会因网络或API问题失败）
    if timeout 10 ais ask "hello" >/dev/null 2>&1; then
        print_success "AI 功能测试"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_warning "AI 功能测试（可能由于网络或API限制失败）"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# 错误分析测试
test_error_analysis() {
    print_step "$((TESTS_TOTAL + 1))" "错误分析功能"
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    
    # 测试手动错误分析
    if ais analyze --exit-code 127 --command "nonexistent_command" --stderr "command not found" >/dev/null 2>&1; then
        print_success "错误分析功能"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_error "错误分析功能"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# 显示测试结果
show_results() {
    echo
    echo "================================================"
    echo "         测试结果统计"
    echo "================================================"
    echo
    print_info "总测试数: $TESTS_TOTAL"
    print_success "通过: $TESTS_PASSED"
    if [ $TESTS_FAILED -gt 0 ]; then
        print_error "失败: $TESTS_FAILED"
    else
        print_info "失败: $TESTS_FAILED"
    fi
    
    echo
    if [ $TESTS_FAILED -eq 0 ]; then
        print_success "🎉 所有测试通过！AIS 安装完整且功能正常。"
    else
        print_warning "⚠️  部分测试失败，请检查安装或配置。"
    fi
    
    # 给出建议
    echo
    print_info "💡 建议的下一步操作:"
    print_info "  1. 在新终端中测试: mkdirr /tmp/test"
    print_info "  2. 手动提问 AI: ais ask \"如何使用 ls 命令?\""
    print_info "  3. 学习新知识: ais learn git"
    print_info "  4. 查看配置: ais config"
    echo
}

# 主测试流程
main() {
    test_installation
    test_error_analysis
    
    # AI功能测试（可选，可能失败）
    print_info "是否测试 AI 功能？（需要网络连接）"
    read -p "输入 y 进行 AI 测试，其他任意键跳过: " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        test_ai_functionality
    fi
    
    show_results
    
    # 返回适当的退出码
    if [ $TESTS_FAILED -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# 处理参数
case "${1:-}" in
    --help)
        echo "AIS 安装测试脚本"
        echo
        echo "用法: $0 [选项]"
        echo
        echo "选项:"
        echo "  --help     显示此帮助"
        echo
        echo "此脚本将测试 AIS 的安装和基本功能。"
        exit 0
        ;;
    *)
        main
        ;;
esac