#!/bin/bash

# AIS 发布脚本
# 用于构建和发布 AIS 到 PyPI

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

# 检查依赖
check_dependencies() {
    print_info "检查发布依赖..."
    
    if ! command -v python3 >/dev/null 2>&1; then
        print_error "Python 3 未安装"
        exit 1
    fi
    
    if ! command -v pip >/dev/null 2>&1; then
        print_error "pip 未安装"
        exit 1
    fi
    
    # 安装构建依赖
    print_info "安装构建依赖..."
    pip install --upgrade build twine
    
    print_success "依赖检查完成"
}

# 检查版本
check_version() {
    current_version=$(python3 -c "import ais; print(ais.__version__)")
    print_info "当前版本: $current_version"
    
    if [ -n "$1" ]; then
        new_version="$1"
        print_info "更新版本到: $new_version"
        
        # 更新 __init__.py 中的版本
        sed -i "s/__version__ = \".*\"/__version__ = \"$new_version\"/" ais/__init__.py
        
        # 更新 pyproject.toml 中的版本
        sed -i "s/version = \".*\"/version = \"$new_version\"/" pyproject.toml
        
        print_success "版本已更新到 $new_version"
    else
        print_info "使用当前版本进行发布"
    fi
}

# 运行测试
run_tests() {
    print_info "运行测试..."
    
    if [ -d "tests" ]; then
        python3 -m pytest tests/ -v
        print_success "测试通过"
    else
        print_warning "未找到测试目录，跳过测试"
    fi
}

# 清理构建目录
clean_build() {
    print_info "清理构建目录..."
    rm -rf dist/ build/ *.egg-info/
    print_success "构建目录已清理"
}

# 构建包
build_package() {
    print_info "构建 Python 包..."
    python3 -m build
    print_success "包构建完成"
    
    # 检查构建的文件
    print_info "构建的文件:"
    ls -la dist/
}

# 检查包
check_package() {
    print_info "检查包的完整性..."
    python3 -m twine check dist/*
    print_success "包检查通过"
}

# 发布到 TestPyPI
upload_to_testpypi() {
    print_info "上传到 TestPyPI..."
    read -p "确定要上传到 TestPyPI 吗？(y/N): " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 -m twine upload --repository testpypi dist/*
        print_success "已上传到 TestPyPI"
        print_info "测试安装: pip install --index-url https://test.pypi.org/simple/ ais-terminal"
    else
        print_info "跳过 TestPyPI 上传"
    fi
}

# 发布到 PyPI
upload_to_pypi() {
    print_info "上传到 PyPI..."
    print_warning "这将发布到正式的 PyPI，请谨慎操作！"
    read -p "确定要发布到 PyPI 吗？(y/N): " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 -m twine upload dist/*
        print_success "已发布到 PyPI"
        print_info "安装命令: pip install ais-terminal"
    else
        print_info "跳过 PyPI 发布"
    fi
}

# 创建 Git 标签
create_git_tag() {
    current_version=$(python3 -c "import ais; print(ais.__version__)")
    tag_name="v$current_version"
    
    print_info "创建 Git 标签: $tag_name"
    read -p "确定要创建标签并推送吗？(y/N): " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Release version $current_version" || true
        git tag -a "$tag_name" -m "Release version $current_version"
        git push origin main
        git push origin "$tag_name"
        print_success "Git 标签已创建并推送"
    else
        print_info "跳过 Git 标签创建"
    fi
}

# 显示帮助
show_help() {
    echo "AIS 发布脚本"
    echo
    echo "用法: $0 [选项] [版本号]"
    echo
    echo "选项:"
    echo "  --test-only     只发布到 TestPyPI"
    echo "  --pypi-only     只发布到 PyPI"
    echo "  --no-tag        不创建 Git 标签"
    echo "  --help          显示此帮助"
    echo
    echo "示例:"
    echo "  $0                    # 使用当前版本发布"
    echo "  $0 0.2.0              # 更新到 0.2.0 并发布"
    echo "  $0 --test-only 0.2.0  # 只发布到 TestPyPI"
}

# 主函数
main() {
    echo "================================================"
    echo "         AIS PyPI 发布工具"
    echo "================================================"
    echo
    
    TEST_ONLY=false
    PYPI_ONLY=false
    NO_TAG=false
    VERSION=""
    
    # 处理参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --test-only)
                TEST_ONLY=true
                shift
                ;;
            --pypi-only)
                PYPI_ONLY=true
                shift
                ;;
            --no-tag)
                NO_TAG=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            --*)
                print_error "未知选项: $1"
                show_help
                exit 1
                ;;
            *)
                VERSION="$1"
                shift
                ;;
        esac
    done
    
    # 执行发布流程
    check_dependencies
    check_version "$VERSION"
    run_tests
    clean_build
    build_package
    check_package
    
    if [ "$TEST_ONLY" = true ]; then
        upload_to_testpypi
    elif [ "$PYPI_ONLY" = true ]; then
        upload_to_pypi
    else
        upload_to_testpypi
        upload_to_pypi
    fi
    
    if [ "$NO_TAG" = false ]; then
        create_git_tag
    fi
    
    print_success "🎉 发布流程完成！"
}

# 运行主函数
main "$@"