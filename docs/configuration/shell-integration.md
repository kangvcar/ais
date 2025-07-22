# Shell 集成

Shell 集成是 AIS 的核心功能，通过钩子机制自动捕获命令执行错误并触发智能分析。

## 🐚 支持的 Shell

### 完全支持
- **Bash** 4.0+
- **Zsh** 5.0+  
- **Fish** 3.0+

### 基本支持
- **Dash** - 基本错误捕获
- **Ksh** - 基本错误捕获

## 🚀 自动设置

### 一键设置
```bash
# 自动检测并配置当前 Shell
ais setup

# 设置完成后重新加载配置
source ~/.bashrc    # Bash
source ~/.zshrc     # Zsh
exec fish          # Fish
```

### 验证设置
```bash
# 测试 Shell 集成
ais test-integration

# 查看集成状态
ais status

# 触发测试错误
false && echo "这个命令会失败"
```

## 🔧 手动配置

### Bash 配置
```bash
# 添加到 ~/.bashrc
echo 'eval "$(ais shell-integration bash)"' >> ~/.bashrc

# 或者手动添加以下内容到 ~/.bashrc
__ais_trap() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        ais analyze --exit-code $exit_code --command "$BASH_COMMAND" &
    fi
}
trap __ais_trap ERR
```

### Zsh 配置
```bash
# 添加到 ~/.zshrc
echo 'eval "$(ais shell-integration zsh)"' >> ~/.zshrc

# 或者手动添加以下内容到 ~/.zshrc
__ais_preexec() {
    AIS_CURRENT_COMMAND="$1"
}
__ais_precmd() {
    local exit_code=$?
    if [[ $exit_code -ne 0 && -n "$AIS_CURRENT_COMMAND" ]]; then
        ais analyze --exit-code $exit_code --command "$AIS_CURRENT_COMMAND" &
    fi
    AIS_CURRENT_COMMAND=""
}
add-zsh-hook preexec __ais_preexec
add-zsh-hook precmd __ais_precmd
```

### Fish 配置
```bash
# 添加到 ~/.config/fish/config.fish
echo 'eval (ais shell-integration fish)' >> ~/.config/fish/config.fish

# 或者手动添加以下内容到 ~/.config/fish/config.fish
function __ais_command_not_found --on-event fish_command_not_found
    ais analyze --exit-code 127 --command "$argv[1]" &
end

function __ais_postexec --on-event fish_postexec
    if test $status -ne 0
        ais analyze --exit-code $status --command "$argv[1]" &
    end
end
```

## ⚙️ 集成选项

### 基本选项
```bash
# 查看集成选项
ais config show shell-integration

# 启用/禁用集成
ais config set shell-integration true
ais config set shell-integration false

# 设置触发延迟（秒）
ais config set shell-integration-delay 1
```


## 🎯 触发条件

### 默认触发条件
- 命令退出码非零（失败）
- 命令不是 AIS 内部命令

## 🔍 调试集成

### 常见问题诊断
```bash
# 检查集成状态
ais test-integration

# 验证钩子函数
type __ais_trap      # Bash
type __ais_precmd    # Zsh
functions __ais_postexec  # Fish
```

## 🛠️ 高级配置

### 上下文收集
```bash
# 设置上下文收集级别
ais config --set context_level=standard
```

## 🔒 安全考虑

### 敏感信息保护
- AIS 默认已配置敏感目录保护
- 自动过滤常见的敏感信息（密码、密钥等）



## 🚫 禁用和卸载

### 临时禁用
```bash
# 临时禁用自动分析
ais off

# 临时禁用 Shell 集成
ais config set shell-integration false

# 重新启用
ais on
ais config set shell-integration true
```

### 完全卸载
```bash
# 手动移除 Bash 集成
sed -i '/ais shell-integration/d' ~/.bashrc

# 手动移除 Zsh 集成
sed -i '/ais shell-integration/d' ~/.zshrc

# 手动移除 Fish 集成
sed -i '/ais shell-integration/d' ~/.config/fish/config.fish
```

## 📋 集成模板

### 开发环境模板
```bash
# 适合开发环境的集成配置
ais config --set auto_analysis=true
ais config --set context_level=detailed
```

### 生产环境模板
```bash
# 适合生产环境的集成配置
ais config --set auto_analysis=false
ais config --set context_level=minimal
```

---

## 下一步

- [隐私设置](./privacy-settings) - 配置隐私保护
- [错误分析](../features/error-analysis) - 了解错误分析功能
- [故障排除](../troubleshooting/common-issues) - 解决集成问题

---

::: tip 提示
建议使用 `ais setup` 命令自动配置 Shell 集成，它会自动检测并配置最佳设置。
:::

::: info 性能影响
Shell 集成对性能影响极小，分析过程在后台异步执行，不会影响正常命令执行。
:::

::: warning 注意
修改 Shell 集成配置后，需要重新加载 Shell 配置或重启终端才能生效。
:::