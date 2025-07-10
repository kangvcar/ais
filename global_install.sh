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

echo "5. 测试新配置..."
bash -c "source ~/.bashrc && declare -f _ais_precmd >/dev/null && echo '✅ shell 集成已加载' || echo '❌ shell 集成未加载'"

echo
echo "✅ 全局安装完成！"
echo
echo "现在在任何新终端中都可以使用 ais 命令了。"
echo "请测试："
echo "  1. 打开新终端"
echo "  2. 执行: mkdirr /tmp/test"
echo "  3. 应该会看到自动分析结果"