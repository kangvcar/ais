#!/bin/bash
# AIS Shell 集成脚本
# 这个脚本通过 PROMPT_COMMAND 机制捕获命令执行错误和错误输出

# 全局变量
_AIS_STDERR_FILE="/tmp/ais_stderr_$$"
_AIS_ORIGINAL_FD3_SET=false

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

# 获取配置中的分析冷却时间
_ais_get_analysis_cooldown() {
    local config_file="$HOME/.config/ais/config.toml"
    local cooldown=60  # 默认60秒
    
    if [ -f "$config_file" ]; then
        # 尝试从配置文件中读取 analysis_cooldown 值
        local config_cooldown=$(grep "analysis_cooldown = " "$config_file" 2>/dev/null | head -1 | cut -d'=' -f2 | tr -d ' ')
        if [ -n "$config_cooldown" ] && [ "$config_cooldown" -gt 0 ] 2>/dev/null; then
            cooldown=$config_cooldown
        fi
    fi
    
    echo $cooldown
}

# 全局变量用于去重检测
_AIS_LAST_ANALYZED_COMMAND=""
_AIS_LAST_ANALYZED_TIME=0

# 初始化 stderr 捕获
_ais_init_stderr_capture() {
    # 避免重复初始化
    if [ "$_AIS_ORIGINAL_FD3_SET" = true ]; then
        return 0
    fi
    
    # 创建临时文件
    touch "$_AIS_STDERR_FILE" 2>/dev/null || return 1
    
    # 保存原始 stderr 到文件描述符 3
    exec 3>&2 2>/dev/null || return 1
    _AIS_ORIGINAL_FD3_SET=true
    
    # 重定向 stderr 到 tee，同时显示和保存
    exec 2> >(tee -a "$_AIS_STDERR_FILE" >&3 2>/dev/null)
    
    return 0
}

# 获取并清理捕获的 stderr
_ais_get_captured_stderr() {
    local stderr_content=""
    
    if [ -f "$_AIS_STDERR_FILE" ]; then
        # 等待一小段时间确保 tee 完成写入
        sleep 0.1
        
        # 读取最后 100 行内容（避免过长）
        stderr_content=$(tail -n 100 "$_AIS_STDERR_FILE" 2>/dev/null | head -c 2000)
        
        # 清空文件内容以准备下次捕获
        > "$_AIS_STDERR_FILE" 2>/dev/null
    fi
    
    echo "$stderr_content"
}

# 清理 stderr 捕获资源
_ais_cleanup_stderr_capture() {
    # 恢复原始 stderr
    if [ "$_AIS_ORIGINAL_FD3_SET" = true ]; then
        exec 2>&3 3>&- 2>/dev/null
        _AIS_ORIGINAL_FD3_SET=false
    fi
    
    # 清理临时文件
    if [ -f "$_AIS_STDERR_FILE" ]; then
        rm -f "$_AIS_STDERR_FILE" 2>/dev/null
    fi
}

# 过滤和清理 stderr 内容
_ais_filter_stderr() {
    local stderr_content="$1"
    
    # 过滤掉一些不相关的内容
    stderr_content=$(echo "$stderr_content" | grep -v "^\s*$" | \
                    grep -v "_ais_" | \
                    grep -v "tee:" | \
                    head -c 1500)
    
    # URL 编码特殊字符以便安全传递
    stderr_content=$(echo "$stderr_content" | sed 's/"/\\"/g' | tr '\n' ' ')
    
    echo "$stderr_content"
}

# 检查命令是否应该被分析（去重机制）
_ais_should_analyze_command() {
    local command="$1"
    local current_time=$(date +%s)
    
    # 如果命令为空，跳过
    if [ -z "$command" ]; then
        return 1
    fi
    
    # 获取配置的冷却时间
    local cooldown=$(_ais_get_analysis_cooldown)
    
    # 如果与上次分析的命令相同，且时间间隔小于配置的冷却时间，跳过
    if [ "$command" = "$_AIS_LAST_ANALYZED_COMMAND" ]; then
        local time_diff=$((current_time - _AIS_LAST_ANALYZED_TIME))
        if [ $time_diff -lt $cooldown ]; then
            return 1  # 跳过重复分析
        fi
    fi
    
    # 更新记录
    _AIS_LAST_ANALYZED_COMMAND="$command"
    _AIS_LAST_ANALYZED_TIME=$current_time
    
    return 0  # 可以分析
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
            if [[ "$last_command" != *"_ais_"* ]] && \
               [[ "$last_command" != *"ais_"* ]] && \
               [[ "$last_command" != *"history"* ]]; then
                
                # 检查是否应该分析此命令（去重机制）
                if _ais_should_analyze_command "$last_command"; then
                    # 获取捕获的 stderr 内容
                    local captured_stderr=$(_ais_get_captured_stderr)
                    local filtered_stderr=$(_ais_filter_stderr "$captured_stderr")
                    
                    # 调用 ais analyze 进行分析，传递 stderr
                    echo  # 添加空行分隔
                    if [ -n "$filtered_stderr" ]; then
                        ais analyze --exit-code "$current_exit_code" \
                            --command "$last_command" \
                            --stderr "$filtered_stderr"
                    else
                        ais analyze --exit-code "$current_exit_code" \
                            --command "$last_command"
                    fi
                fi
            fi
        fi
    fi
}

# 初始化 stderr 捕获
_ais_init_stderr_capture

# 设置退出时清理
trap '_ais_cleanup_stderr_capture' EXIT INT TERM

# 根据不同 shell 设置钩子
if [ -n "$ZSH_VERSION" ]; then
    # Zsh 设置
    autoload -U add-zsh-hook 2>/dev/null || return
    add-zsh-hook precmd _ais_precmd
    
    # Zsh 退出清理
    add-zsh-hook zshexit _ais_cleanup_stderr_capture
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
