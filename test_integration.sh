#!/bin/bash

# 加载集成脚本
source /root/ais/shell/integration.sh

# 模拟交互式环境
echo "=== 测试开始 ==="
echo "执行错误命令: mkdirr /tmp/test"

# 手动设置变量来模拟 preexec 行为
_ais_last_command="mkdirr /tmp/test"

# 执行命令并捕获退出码
mkdirr /tmp/test 2>&1
exit_code=$?

# 手动调用 precmd 来模拟 PROMPT_COMMAND
_ais_last_exit_code=$exit_code
_ais_precmd

echo "=== 测试结束 ==="