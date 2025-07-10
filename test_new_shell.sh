#!/bin/bash

echo "=== 新 Shell 会话测试 ==="
echo "当前工作目录: $(pwd)"
echo "PATH: $PATH"
echo

# 检查 ais 命令
echo "1. 检查 ais 命令..."
if command -v ais >/dev/null 2>&1; then
    echo "✅ ais 命令可用: $(which ais)"
    ais --version
else
    echo "❌ ais 命令不可用"
    echo "尝试手动添加到 PATH..."
    export PATH="/root/.local/bin:$PATH"
    if command -v ais >/dev/null 2>&1; then
        echo "✅ 手动添加 PATH 后 ais 可用"
        echo "请将以下行添加到 ~/.bashrc:"
        echo 'export PATH="/root/.local/bin:$PATH"'
    else
        echo "❌ 仍然无法找到 ais"
    fi
fi

echo
echo "2. 检查集成脚本..."
if [ -f "/root/ais/shell/integration.sh" ]; then
    echo "✅ 集成脚本存在"
    source "/root/ais/shell/integration.sh"
    echo "✅ 集成脚本已加载"
    
    # 检查函数是否存在
    if declare -f _ais_precmd >/dev/null; then
        echo "✅ _ais_precmd 函数已定义"
    else
        echo "❌ _ais_precmd 函数未定义"
    fi
    
    # 检查 PROMPT_COMMAND
    echo "PROMPT_COMMAND: '$PROMPT_COMMAND'"
else
    echo "❌ 集成脚本不存在"
fi

echo
echo "3. 测试错误分析..."
if command -v ais >/dev/null 2>&1; then
    echo "执行测试命令: mkdirr /tmp/test"
    
    # 模拟错误命令的分析
    _ais_last_command="mkdirr /tmp/test"
    _ais_last_exit_code=127
    
    echo "调用分析函数..."
    if declare -f _ais_precmd >/dev/null; then
        _ais_precmd
    else
        echo "❌ 无法调用 _ais_precmd 函数"
    fi
else
    echo "❌ 无法测试，ais 命令不可用"
fi

echo
echo "=== 测试完成 ==="