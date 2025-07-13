#!/bin/bash
# AIS Shell 集成脚本
# 这个脚本通过 PROMPT_COMMAND 机制捕获命令执行错误

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

# precmd 钩子：命令执行后调用
_ais_precmd() {
    local current_exit_code=$?

    # 只处理非零退出码且非中断信号（Ctrl+C 是 130）
    if [ $current_exit_code -ne 0 ] && [ $current_exit_code -ne 130 ]; then
        # 检查功能是否开启
        if _ais_check_auto_analysis; then
            local last_command
            last_command=$(history 1 | sed 's/^[ ]*[0-9]*[ ]*//' 2>/dev/null)

            # 过滤内部命令和特殊情况
            if [[ "$last_command" != *"_ais_"* ]] &&                [[ "$last_command" != *"ais_"* ]] &&                [[ "$last_command" != *"history"* ]]; then
                # 调用 ais analyze 进行分析
                echo  # 添加空行分隔
                ais analyze --exit-code "$current_exit_code"                     --command "$last_command"
            fi
        fi
    fi
}

# 根据不同 shell 设置钩子
if [ -n "$ZSH_VERSION" ]; then
    # Zsh 设置
    autoload -U add-zsh-hook 2>/dev/null || return
    add-zsh-hook precmd _ais_precmd
elif [ -n "$BASH_VERSION" ]; then
    # Bash 设置
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
