#!/bin/bash

echo "=== AIS Shell 集成验证脚本 ==="
echo
echo "1. 检查 AIS 命令是否可用..."
if command -v ais >/dev/null 2>&1; then
    echo "✅ AIS 命令可用"
    ais --version
else
    echo "❌ AIS 命令不可用"
    exit 1
fi

echo
echo "2. 检查配置状态..."
ais config

echo
echo "3. 检查 shell 集成..."
if grep -q "START AIS INTEGRATION" ~/.bashrc; then
    echo "✅ Shell 集成已配置"
else
    echo "❌ Shell 集成未配置"
    echo "请运行: ais setup-shell"
    exit 1
fi

echo
echo "4. 手动测试分析功能..."
echo "测试命令: mkdirr /tmp/test"
ais analyze --exit-code 127 --command "mkdirr /tmp/test" --stderr "mkdirr: 未找到命令"

echo
echo "=== 验证完成 ==="
echo
echo "如果所有检查都通过，请在新的终端窗口中测试："
echo "1. 打开新的终端或运行: bash"
echo "2. 执行错误命令: mkdirr /tmp/test"
echo "3. 应该会立即看到 AI 分析结果和交互菜单"
echo
echo "注意：自动分析只在交互式终端中有效，不支持脚本环境。"