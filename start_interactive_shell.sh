#!/bin/bash

echo "启动新的交互式 shell 来测试 AIS..."
echo "在新的 shell 中，请尝试执行: mkdirr /tmp/test"
echo "如果自动分析不工作，可以手动运行: ais analyze --exit-code 127 --command 'mkdirr /tmp/test' --stderr ''"
echo
echo "按 Ctrl+D 或输入 'exit' 退出测试 shell"
echo "================================================"

# 启动新的交互式 bash，确保加载完整的环境
exec bash --login -i