#!/bin/bash

echo "=== 修复 Shell 集成 ==="

# 1. 确保 PATH 包含 pipx 安装路径
echo "1. 检查和修复 PATH..."
if ! echo "$PATH" | grep -q "/root/.local/bin"; then
    echo "添加 /root/.local/bin 到 PATH"
    echo 'export PATH="/root/.local/bin:$PATH"' >> ~/.bashrc
fi

# 2. 重新安装 ais (确保最新版本)
echo "2. 重新安装 ais..."
pipx uninstall ais-cli 2>/dev/null || true
pipx install -e /root/ais

# 3. 更新 bashrc 中的集成代码
echo "3. 更新 shell 集成..."

# 移除旧的集成代码
sed -i '/# START AIS INTEGRATION/,/# END AIS INTEGRATION/d' ~/.bashrc

# 添加新的集成代码
cat >> ~/.bashrc << 'EOF'

# START AIS INTEGRATION - Updated
# 确保 PATH 包含 pipx 路径
export PATH="/root/.local/bin:$PATH"

# 清除可能的旧函数定义
unset -f _ais_precmd _ais_preexec _ais_check_availability _ais_check_auto_analysis 2>/dev/null

# 加载 AIS shell 集成
if [ -f "/root/ais/shell/integration.sh" ]; then
    source "/root/ais/shell/integration.sh"
fi
# END AIS INTEGRATION
EOF

echo "4. 验证安装..."
source ~/.bashrc

if command -v ais >/dev/null 2>&1; then
    echo "✅ ais 命令可用: $(which ais)"
    ais --version
else
    echo "❌ ais 命令仍然不可用"
    exit 1
fi

if declare -f _ais_precmd >/dev/null; then
    echo "✅ shell 集成函数已加载"
else
    echo "❌ shell 集成函数未加载"
    exit 1
fi

echo
echo "✅ 修复完成！"
echo
echo "请运行以下命令重新加载配置："
echo "  source ~/.bashrc"
echo
echo "然后在新终端中测试："
echo "  mkdirr /tmp/test"