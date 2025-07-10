#!/bin/bash
# AIS Shell 集成脚本
# 这个脚本通过 PROMPT_COMMAND 机制捕获命令执行错误

# 全局变量用于跟踪命令状态
_ais_last_command=""
_ais_last_exit_code=0

# 检查 AIS 是否可用
_ais_check_availability() {
    command -v ais >/dev/null 2>&1
}

# 检查自动分析是否开启
_ais_check_auto_analysis() {
    if ! _ais_check_availability; then
        return 1
    fi
    
    # 检查配置文件中的 auto_analysis 设置
    local config_file="$HOME/.config/ais/config.toml"
    if [ -f "$config_file" ]; then
        grep -q "auto_analysis = true" "$config_file" 2>/dev/null
    else
        return 1  # 默认关闭
    fi
}

# preexec 钩子：命令执行前调用
_ais_preexec() {
    _ais_last_command="$1"
}

# precmd 钩子：命令执行后调用
_ais_precmd() {
    _ais_last_exit_code=$?
    
    # 只处理非零退出码且非中断信号（Ctrl+C 是 130）
    if [ $_ais_last_exit_code -ne 0 ] && [ $_ais_last_exit_code -ne 130 ]; then
        # 检查功能是否开启
        if _ais_check_auto_analysis; then
            # 同步调用分析，立即显示结果和交互菜单
            echo  # 添加空行分隔
            
            # 调用 ais analyze 进行分析
            ais analyze \
                --exit-code "$_ais_last_exit_code" \
                --command "$_ais_last_command" \
                --stderr ""
        fi
    fi
}

# 根据不同 shell 设置钩子
if [ -n "$ZSH_VERSION" ]; then
    # Zsh 设置
    autoload -U add-zsh-hook 2>/dev/null || return
    add-zsh-hook preexec _ais_preexec
    add-zsh-hook precmd _ais_precmd
    
elif [ -n "$BASH_VERSION" ]; then
    # Bash 设置
    # 使用 DEBUG trap 来捕获 preexec
    trap '_ais_preexec "$BASH_COMMAND"' DEBUG
    
    # 将 precmd 添加到 PROMPT_COMMAND
    if [[ -z "$PROMPT_COMMAND" ]]; then
        PROMPT_COMMAND="_ais_precmd"
    else
        PROMPT_COMMAND="_ais_precmd;$PROMPT_COMMAND"
    fi
    
else
    # 对于其他 shell，提供基本的 PROMPT_COMMAND 支持
    if [[ -z "$PROMPT_COMMAND" ]]; then
        PROMPT_COMMAND="_ais_precmd"
    else
        PROMPT_COMMAND="_ais_precmd;$PROMPT_COMMAND"
    fi
fi

# 提供手动分析功能的便捷函数
ais_analyze_last() {
    if [ -n "$_ais_last_command" ] && [ $_ais_last_exit_code -ne 0 ]; then
        ais analyze \
            --exit-code "$_ais_last_exit_code" \
            --command "$_ais_last_command"
    else
        echo "没有失败的命令需要分析"
    fi
}

# 显示 AIS 状态的便捷函数
ais_status() {
    if _ais_check_availability; then
        echo "✅ AIS 可用"
        if _ais_check_auto_analysis; then
            echo "🤖 自动错误分析: 开启"
        else
            echo "😴 自动错误分析: 关闭"
        fi
    else
        echo "❌ AIS 不可用"
    fi
}

# 导出函数供用户使用
export -f ais_analyze_last ais_status 2>/dev/null || true