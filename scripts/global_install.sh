#!/bin/bash

echo "=== AIS 全局安装脚本 ==="

# 1. 创建全局可执行的 ais 脚本
echo "1. 创建全局 ais 命令..."
sudo tee /usr/local/bin/ais > /dev/null << 'EOF'
#!/bin/bash
# AIS 全局启动脚本
cd /root/ais
/root/.local/bin/ais "$@"
EOF

sudo chmod +x /usr/local/bin/ais

# 2. 测试全局命令
echo "2. 测试全局命令..."
if command -v ais >/dev/null 2>&1; then
    echo "✅ ais 全局命令可用: $(which ais)"
    ais --version
else
    echo "❌ ais 全局命令不可用"
    exit 1
fi

# 3. 更新集成脚本路径
echo "3. 更新 shell 集成..."
cp /root/ais/shell/integration.sh /usr/local/share/ais-integration.sh

# 4. 更新 bashrc
echo "4. 更新 ~/.bashrc..."

# 移除旧的集成代码
sed -i '/# START AIS INTEGRATION/,/# END AIS INTEGRATION/d' ~/.bashrc

# 添加新的全局集成代码
cat >> ~/.bashrc << 'EOF'

# START AIS INTEGRATION - Global
if [ -f "/usr/local/share/ais-integration.sh" ]; then
    source "/usr/local/share/ais-integration.sh"
fi
# END AIS INTEGRATION
EOF

echo "5. 加载集成到当前会话..."
source ~/.bashrc

echo "6. 测试集成是否生效..."
if declare -f _ais_precmd >/dev/null 2>&1; then
    echo "✅ shell 集成已加载到当前会话"
else
    echo "❌ shell 集成未能加载，请重新打开终端"
fi

echo
echo "✅ 全局安装完成！"
echo
echo "Shell 集成已在当前会话中激活，可以直接测试："
echo "  执行: mkdirr /tmp/test"
echo "  应该会看到自动分析结果"
echo
echo "注意：其他终端需要重新打开才能使用 AIS 集成功能"