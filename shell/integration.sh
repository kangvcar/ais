#!/bin/bash
# AIS Shell 集成脚本
# 这个脚本通过 PROMPT_COMMAND 机制捕获命令执行错误

# 全局变量用于跟踪命令状态
_ais_last_command=""
_ais_last_exit_code=0
_ais_last_stderr=""
AI_STDERR_FILE="/tmp/ais_stderr_$$"
AI_LAST_COMMAND=""
AI_LAST_EXIT_CODE=0

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
    _ais_last_stderr=""  # 清空之前的 stderr
}

# precmd 钩子：命令执行后调用
_ais_precmd() {
    local current_exit_code=$?
    
    # 只处理非零退出码且非中断信号（Ctrl+C 是 130）
    if [ $current_exit_code -ne 0 ] && [ $current_exit_code -ne 130 ]; then
        # 检查功能是否开启
        if _ais_check_auto_analysis; then
            local last_command=$(history 1 | sed 's/^[ ]*[0-9]*[ ]*//' 2>/dev/null || echo "$_ais_last_command")
            
            # 过滤内部命令和特殊情况
            if [[ "$last_command" != *"_ais_"* ]] && [[ "$last_command" != *"ais_"* ]] && [[ "$last_command" != *"history"* ]]; then
                
                # 尝试多种方式获取错误输出
                local stderr_output=""
                
                # 方法1: 优先使用ai_exec捕获的错误
                if [ -f "$AI_STDERR_FILE" ] && [ -s "$AI_STDERR_FILE" ]; then
                    stderr_output=$(cat "$AI_STDERR_FILE" 2>/dev/null || echo "")
                    > "$AI_STDERR_FILE" 2>/dev/null || true  # 清空文件
                fi
                
                # 方法2: 如果没有捕获到stderr，尝试重新执行命令获取错误信息（仅对安全命令）
                if [ -z "$stderr_output" ]; then
                    if [[ "$last_command" != *"|"* ]] && [[ "$last_command" != *">"* ]] && [[ "$last_command" != *"&"* ]] && [[ "$last_command" != *"sudo"* ]]; then
                        # 安全地重新执行命令，只获取stderr
                        stderr_output=$(eval "$last_command" 2>&1 >/dev/null || true)
                    fi
                    
                    # 如果还是没有捕获到错误，生成通用错误信息
                    if [ -z "$stderr_output" ]; then
                        local cmd_name=$(echo "$last_command" | awk '{print $1}')
                        if ! command -v "$cmd_name" >/dev/null 2>&1; then
                            stderr_output="bash: $cmd_name: command not found"
                        else
                            stderr_output="Command failed with exit code $current_exit_code"
                        fi
                    fi
                fi
                
                # 同步调用分析，立即显示结果和交互菜单
                echo  # 添加空行分隔
                
                # 调用 ais analyze 进行分析
                ais analyze \
                    --exit-code "$current_exit_code" \
                    --command "$last_command" \
                    --stderr "$stderr_output"
            fi
        fi
    fi
}

# 高级命令执行包装器 - 支持实时stderr捕获
ai_exec() {
    if [ $# -eq 0 ]; then
        echo "用法: ai_exec <命令>"
        echo "示例: ai_exec ls /nonexistent"
        return 1
    fi
    
    # 清空之前的错误
    > "$AI_STDERR_FILE" 2>/dev/null || true
    
    # 执行命令并捕获stderr，同时保持用户交互
    "$@" 2> >(tee "$AI_STDERR_FILE" >&2)
    local exit_code=$?
    
    AI_LAST_EXIT_CODE=$exit_code
    AI_LAST_COMMAND="$*"
    
    return $exit_code
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
        echo ""
        echo "💡 使用方法:"
        echo "  • 普通命令: 直接执行，失败时会基于命令和退出码分析"
        echo "  • 完整分析: ai_exec <命令> - 捕获完整错误信息进行分析"
        echo ""
        echo "示例: ai_exec chmod 999 /etc/passwd"
    else
        echo "❌ AIS 不可用"
    fi
}

# 导出函数供用户使用
export -f ais_analyze_last ais_status ai_exec 2>/dev/null || true