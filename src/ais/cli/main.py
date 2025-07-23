"""Main CLI interface for AIS."""

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .. import __version__
from ..core.config import get_config, set_config
from ..ui.panels import panels

console = Console()


def _create_integration_script(script_path: str):
    """创建Shell集成脚本。"""
    import os

    # 获取配置中的重复分析间隔时间
    try:
        config = get_config()
        analysis_cooldown = config.get("advanced", {}).get("analysis_cooldown", 60)
    except Exception:
        analysis_cooldown = 60  # 默认60秒

    script_content = """#!/bin/bash
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
    stderr_content=$(echo "$stderr_content" | grep -v "^\\s*$" | \\
                    grep -v "_ais_" | \\
                    grep -v "tee:" | \\
                    head -c 1500)

    # URL 编码特殊字符以便安全传递
    stderr_content=$(echo "$stderr_content" | sed 's/"/\\\\"/g' | tr '\\n' ' ')

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

    # 如果与上次分析的命令相同，且时间间隔小于{analysis_cooldown}秒，跳过
    if [ "$command" = "$_AIS_LAST_ANALYZED_COMMAND" ]; then
        local time_diff=$((current_time - _AIS_LAST_ANALYZED_TIME))
        if [ $time_diff -lt {analysis_cooldown} ]; then
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
            if [[ "$last_command" != *"_ais_"* ]] && \\
               [[ "$last_command" != *"ais_"* ]] && \\
               [[ "$last_command" != *"history"* ]]; then

                # 检查是否应该分析此命令（去重机制）
                if _ais_should_analyze_command "$last_command"; then
                    # 获取捕获的 stderr 内容
                    local captured_stderr=$(_ais_get_captured_stderr)
                    local filtered_stderr=$(_ais_filter_stderr "$captured_stderr")

                    # 调用 ais analyze 进行分析，传递 stderr
                    echo  # 添加空行分隔
                    if [ -n "$filtered_stderr" ]; then
                        ais analyze --exit-code "$current_exit_code" \\
                            --command "$last_command" \\
                            --stderr "$filtered_stderr"
                    else
                        ais analyze --exit-code "$current_exit_code" \\
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
"""

    # 使用配置值格式化脚本内容
    formatted_script = script_content.format(analysis_cooldown=analysis_cooldown)

    with open(script_path, "w") as f:
        f.write(formatted_script)
    os.chmod(script_path, 0o755)


def _auto_setup_shell_integration():
    """自动设置Shell集成（首次运行时）"""
    import os
    from pathlib import Path

    # 检查是否已经设置过
    marker_file = Path.home() / ".config" / "ais" / ".auto_setup_done"
    if marker_file.exists():
        return

    # 创建配置目录
    config_dir = Path.home() / ".config" / "ais"
    config_dir.mkdir(parents=True, exist_ok=True)

    try:
        import ais

        package_path = os.path.dirname(ais.__file__)

        # Unix shell 自动设置
        _auto_setup_unix_integration(package_path, config_dir)

        # 确保默认配置中启用自动分析
        config_file_path = config_dir / "config.toml"
        if not config_file_path.exists():
            default_config = """# AIS 配置文件
default_provider = "default_free"
auto_analysis = true
context_level = "detailed"
sensitive_dirs = ["~/.ssh", "~/.config/ais", "~/.aws"]

[providers.default_free]
base_url = "https://api.deepbricks.ai/v1/chat/completions"
model_name = "gpt-4o-mini"
api_key = "sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg"
"""
            config_file_path.write_text(default_config)

        # 标记已完成自动设置
        marker_file.write_text("auto setup completed")

    except Exception:
        # 静默失败，不影响正常使用
        pass


def _auto_setup_unix_integration(package_path, config_dir):
    """自动设置 Unix shell 集成"""
    import os
    from pathlib import Path

    script_path = os.path.join(package_path, "shell", "integration.sh")

    # 如果集成脚本不存在，创建它
    if not os.path.exists(script_path):
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        _create_integration_script(script_path)

    # 自动添加到用户的shell配置文件
    shell = os.environ.get("SHELL", "/bin/bash")
    shell_name = os.path.basename(shell)

    # 检测用户使用的Shell配置文件
    config_files = {
        "bash": [Path.home() / ".bashrc", Path.home() / ".bash_profile"],
        "zsh": [Path.home() / ".zshrc"],
    }

    target_files = config_files.get(shell_name, [Path.home() / ".bashrc"])

    # 找到存在的配置文件或创建默认的
    config_file = None
    for cf in target_files:
        if cf.exists():
            config_file = cf
            break

    if not config_file:
        config_file = target_files[0]
        config_file.touch()  # 创建文件

    # 检查是否已经添加了集成配置
    if config_file.exists():
        content = config_file.read_text()
        if "# START AIS INTEGRATION" not in content:
            # 添加集成配置
            integration_config = f"""

# START AIS INTEGRATION
# AIS - 上下文感知的错误分析学习助手自动集成
if [ -f "{script_path}" ]; then
    source "{script_path}"
fi
# END AIS INTEGRATION
"""
            with open(config_file, "a") as f:
                f.write(integration_config)

    # 显示一次性提示
    setup_message = f"""[green]🎉 AIS 已自动配置完成！[/green]

[green]✓  Shell集成配置已添加到:[/green] [dim]{config_file}[/dim]

[green]✨ 正在自动加载配置，让改动立即生效...[/green]"""
    panels.success(setup_message, "🎉 AIS 自动配置完成")

    # 自动执行 source 命令让配置立即生效
    import subprocess

    try:
        # 使用当前shell执行source命令
        shell = os.environ.get("SHELL", "/bin/bash")
        subprocess.run([shell, "-c", f"source {config_file}"], check=False)
        console.print("[green]✓  配置已自动加载，AIS功能立即可用！[/green]")
        console.print("[green]✨ 命令失败时将自动显示AI分析！[/green]")
    except Exception as e:
        console.print(f"[yellow]⚠️ 自动加载配置失败: {e}[/yellow]")
        console.print(f"[dim]请手动运行: source {config_file}[/dim]")


def _check_shell_integration():
    """策略3: 检查shell集成是否已配置"""
    import os
    from pathlib import Path

    # 检测shell配置文件
    shell = os.environ.get("SHELL", "/bin/bash")
    shell_name = os.path.basename(shell)

    config_files = {
        "bash": [Path.home() / ".bashrc", Path.home() / ".bash_profile"],
        "zsh": [Path.home() / ".zshrc"],
    }

    target_files = config_files.get(shell_name, [Path.home() / ".bashrc"])

    # 检查是否已配置
    for config_file in target_files:
        if config_file.exists():
            content = config_file.read_text()
            if "# START AIS INTEGRATION" in content:
                return True  # 已配置

    return False  # 未配置


def _show_setup_reminder():
    """显示配置提醒"""
    console.print()
    console.print("[yellow]💡 检测到AIS尚未配置Shell集成[/yellow]")
    console.print()
    console.print("运行以下命令完成配置：")
    console.print("[bold cyan]ais setup[/bold cyan]")
    console.print()
    console.print("[dim]配置后可启用自动错误分析功能[/dim]")
    console.print()


@click.group()
@click.version_option(version=__version__, prog_name="ais")
@click.pass_context
def main(ctx):
    """AIS - 上下文感知的错误分析学习助手。

    通过深度Shell集成架构，实现多维上下文感知和智能错误分析，让每次报错都是成长。

    💡 提示: 大多数命令都支持 --help-detail 选项查看详细使用说明

    示例:
      ais ask --help-detail     查看 ask 命令详细帮助
      ais config --help-context 查看配置帮助
      ais history --help-detail 查看历史命令帮助
    """
    # 只在执行具体命令时进行检查（不是--help时）
    if ctx.invoked_subcommand and ctx.invoked_subcommand not in [
        "help",
        "setup",
    ]:
        _auto_setup_shell_integration()

        # 策略3: 首次运行自动提示
        if not _check_shell_integration():
            _show_setup_reminder()


def _handle_error(error_msg: str) -> None:
    """统一的错误处理函数。"""
    error_panel = Panel(
        f"[red]{error_msg}[/red]",
        title="[bold red]✗  错误信息[/bold red]",
        border_style="red",
        padding=(1, 2),
        expand=False,
    )
    console.print(error_panel)


@main.command()
@click.argument("question", required=False)
@click.option("--help-detail", is_flag=True, help="显示ask命令详细使用说明")
def ask(question, help_detail):
    """Ask AI a question."""
    if help_detail:
        help_content = """[bold]功能:[/bold]
  智能问答模式，基于当前环境上下文提供精准回答
  结合项目、Git、系统状态等信息给出针对性建议

[bold]用法:[/bold]
  ais ask <问题>

[bold]智能上下文感知:[/bold]
  • 自动识别当前项目类型和技术栈
  • 结合Git分支和状态信息
  • 考虑当前目录和文件结构
  • 根据用户权限和系统环境调整回答

[bold]适用场景:[/bold]
  • 解释概念："什么是Docker容器？"
  • 快速答疑："Git冲突是什么意思？"
  • 概念查询："Linux权限755代表什么？"
  • 项目相关："如何在当前项目中添加依赖？"
  • 故障诊断："为什么我的构建命令失败？"

[bold]上下文配置:[/bold]
  ais config --set ask.context_level=minimal   - 仅基础信息
  ais config --set ask.context_level=standard  - 包含项目和Git信息
  ais config --set ask.context_level=detailed  - 完整系统和环境信息

[bold]vs 其他命令:[/bold]
  • 想系统学习主题 → 使用 ais learn

[bold]提示:[/bold]
  • 问题用引号包围，避免 shell 解析问题
  • AI会根据你的当前环境提供更精准的建议
  • 在项目目录下使用时效果更佳

[bold]相关命令:[/bold]
  ais config                   - 查看当前上下文配置
  ais config --list-providers  - 查看可用的 AI 服务商
  ais learn <主题>             - 学习特定主题知识"""
        panels.info(help_content, "📚 ais ask 命令详细使用说明")
        return

    if not question:
        error_message = """错误: 请提供要询问的问题

用法: ais ask "你的问题"
帮助: ais ask --help-detail"""
        panels.error(error_message, "✗  参数错误")
        return

    try:
        from ..core.streaming import create_streaming_asker

        config = get_config()

        # 创建流式问答器
        streaming_asker = create_streaming_asker(console)

        # 使用带上下文的流式输出进行问答
        from ..core.ai import ask_ai_with_context

        response = streaming_asker.ask_with_streaming(ask_ai_with_context, question, config)

        if response:
            panels.ai_analysis(Markdown(response), "🤖 AI 回答")
        else:
            panels.error("Failed to get AI response")
    except Exception as e:
        _handle_error(str(e))


@main.command()
@click.option("--set", "set_key", help="设置配置项 (key=value)")
@click.option("--get", "get_key", help="获取配置项值")
@click.option("--list-providers", is_flag=True, help="列出所有可用的 AI 服务商")
@click.option("--help-context", is_flag=True, help="显示上下文级别配置帮助")
@click.option("--init", is_flag=True, help="初始化配置文件（覆盖已存在的文件）")
def config(set_key, get_key, list_providers, help_context, init):
    """显示或修改配置。"""
    try:
        if init:
            # 初始化配置文件
            from ..core.config import init_config, get_config_path

            config_path = get_config_path()
            success = init_config(force=True)

            if success:
                panels.success(
                    f"✓ 配置文件已初始化: {config_path}\n\n"
                    + "包含以下默认设置:\n"
                    + "• 默认AI提供商: default_free (gpt-4o-mini)\n"
                    + "• 自动错误分析: 开启\n"
                    + "• 上下文收集: 详细级别\n"
                    + "• HTTP请求超时: 120秒\n\n"
                    + "使用 'ais config' 查看完整配置",
                    "🔧 配置初始化完成",
                )
            else:
                panels.error("配置初始化失败", "✗ 初始化错误")
            return

        config = get_config()

        if set_key:
            # 设置配置项
            if "=" not in set_key:
                console.print("[red]格式错误，请使用 key=value 格式[/red]")
                return
            key, value = set_key.split("=", 1)

            # 验证和转换配置值
            if key == "context_level":
                if value not in ["minimal", "standard", "detailed"]:
                    console.print(
                        "[red]错误: context_level 必须是 minimal, " "standard 或 detailed[/red]"
                    )
                    console.print("[dim]使用 'ais config --help-context' 查看详细说明[/dim]")
                    return
            elif key == "ask.context_level":
                if value not in ["minimal", "standard", "detailed"]:
                    console.print(
                        "[red]错误: ask.context_level 必须是 minimal, " "standard 或 detailed[/red]"
                    )
                    console.print("[dim]这个配置项专门控制 ask 命令的上下文收集级别[/dim]")
                    return
            elif key == "auto_analysis":
                if value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                else:
                    console.print("[red]错误: auto_analysis 必须是 true 或 false[/red]")
                    return
            elif value.lower() in ["true", "false"]:
                value = value.lower() == "true"
            elif value.isdigit():
                value = int(value)

            set_config(key, value)
            console.print(f"[green]✓ {key} = {value}[/green]")

            # 提供额外的设置提示
            if key == "context_level":
                console.print(f"[dim]上下文收集级别已设置为 {value}[/dim]")

        elif get_key:
            # 获取配置项
            value = config.get(get_key, "未设置")
            console.print(f"{get_key}: {value}")

        elif list_providers:
            # 列出所有提供商
            providers = config.get("providers", {})
            console.print("[green]可用的 AI 服务商:[/green]")
            for name, provider in providers.items():
                current = "✓" if name == config.get("default_provider") else " "
                console.print(f"{current} {name}: {provider.get('model_name', 'N/A')}")

        elif help_context:
            # 显示上下文配置帮助
            help_content = """[bold]可用级别:[/bold]
  • [blue]minimal[/blue]  - 只收集基本信息（命令、退出码、目录）
  • [blue]standard[/blue] - 收集标准信息（+ 命令历史、文件列表、Git状态）[dim]（默认）[/dim]
  • [blue]detailed[/blue] - 收集详细信息（+ 系统信息、环境变量、完整目录）

[bold]设置方法:[/bold]
  ais config --set context_level=minimal
  ais config --set context_level=standard
  ais config --set context_level=detailed

[bold]其他配置项:[/bold]
  auto_analysis=true/false    - 开启/关闭自动错误分析
  default_provider=name       - 设置默认AI服务提供商
  advanced.analysis_cooldown=秒数 - 重复分析避免间隔时间（默认60秒）

[dim]查看当前配置: ais config[/dim]"""
            panels.config(help_content, "⚙️ 上下文收集级别配置帮助")

        else:
            # 显示当前配置
            auto_analysis = config.get("auto_analysis", True)
            auto_status = "✓  开启" if auto_analysis else "✗  关闭"
            context_level = config.get("context_level", "detailed")
            ask_context_level = config.get("ask", {}).get("context_level", "minimal")
            sensitive_count = len(config.get("sensitive_dirs", []))

            # UI配置 - 流式输出始终启用，progressive模式

            config_content = f"""默认提供商: {
                config.get(
                    'default_provider',
                    'default_free')}
自动分析: {auto_status}
错误分析上下文级别: {context_level}
Ask命令上下文级别: {ask_context_level}
敏感目录: {sensitive_count} 个

[dim]💡 提示:[/dim]
[dim]  ais config --help-context    - 查看上下文配置帮助[/dim]
[dim]  ais config --list-providers  - 查看AI服务提供商[/dim]
[dim]  ais config --set key=value   - 修改配置[/dim]
[dim]  ais config --set ask.context_level=standard - 设置Ask上下文级别[/dim]"""
            panels.config(config_content, "⚙️ 当前配置")

    except Exception as e:
        panels.error(f"配置错误: {e}")


def _toggle_auto_analysis(enabled: bool) -> None:
    """开启/关闭自动分析的通用函数。"""
    try:
        set_config("auto_analysis", enabled)
        status = "已开启" if enabled else "已关闭"
        message = f"✓ 自动错误分析{status}"
        if enabled:
            panels.success(message)
        else:
            panels.warning(message)
    except Exception as e:
        _handle_error(str(e))


@main.command()
def on():
    """开启自动错误分析。"""
    _toggle_auto_analysis(True)


@main.command()
def off():
    """关闭自动错误分析。"""
    _toggle_auto_analysis(False)


def _handle_provider_operation(operation, name, success_msg, error_prefix, *args):
    """处理提供商操作的通用函数。"""
    try:
        operation(name, *args)
        panels.success(f"✓ {success_msg}: {name}")
    except Exception as e:
        panels.error(f"{error_prefix}失败: {e}")


@main.command("provider-add")
@click.argument("name", required=False)
@click.option("--url", help="API 基础 URL")
@click.option("--model", help="模型名称")
@click.option("--key", help="API 密钥 (可选)")
@click.option("--help-detail", is_flag=True, help="显示provider-add命令详细使用说明")
def add_provider_cmd(name, url, model, key, help_detail):
    """添加新的 AI 服务商。"""
    if help_detail:
        help_content = """[bold]功能:[/bold]
  添加新的 AI 服务提供商配置，支持自定义 API 服务

[bold]用法:[/bold]
  ais provider-add <名称> --url <API地址> --model <模型名> [--key <密钥>]

[bold]参数:[/bold]
  名称       提供商的唯一标识名称
  --url      API 基础 URL 地址
  --model    使用的模型名称
  --key      API 密钥（可选，某些服务需要）

[bold]示例:[/bold]
  # 添加 OpenAI 服务
  ais provider-add openai \\
    --url https://api.openai.com/v1/chat/completions \\
    --model gpt-4 \\
    --key your_api_key

  # 添加本地 Ollama 服务
  ais provider-add ollama \\
    --url http://localhost:11434/v1/chat/completions \\
    --model llama3

[bold]常用服务配置:[/bold]
  • OpenAI: https://api.openai.com/v1/chat/completions
  • Azure OpenAI: https://your-resource.openai.azure.com/
    openai/deployments/your-deployment/chat/completions?api-version=2023-05-15
  • Ollama: http://localhost:11434/v1/chat/completions
  • Claude (Anthropic): https://api.anthropic.com/v1/messages

[bold]相关命令:[/bold]
  ais provider-list         - 查看所有配置的提供商
  ais provider-use <名称>   - 切换默认提供商
  ais provider-remove <名称> - 删除提供商配置

[dim]💡 提示: 添加后使用 'ais provider-use <名称>' 切换到新提供商[/dim]"""
        panels.info(help_content, "📚 ais provider-add 命令详细使用说明")
        return

    if not name or not url or not model:
        error_message = """错误: 缺少必需参数

用法: ais provider-add <名称> --url <地址> --model <模型>
帮助: ais provider-add --help-detail"""
        panels.error(error_message, "✗  参数错误")
        return

    from ..core.config import add_provider

    _handle_provider_operation(add_provider, name, "已添加提供商", "添加提供商", url, model, key)


@main.command("provider-remove")
@click.argument("name")
def remove_provider_cmd(name):
    """删除 AI 服务商。"""
    from ..core.config import remove_provider

    _handle_provider_operation(remove_provider, name, "已删除提供商", "删除提供商")


@main.command("provider-use")
@click.argument("name")
def use_provider_cmd(name):
    """切换默认 AI 服务商。"""
    from ..core.config import use_provider

    _handle_provider_operation(use_provider, name, "已切换到提供商", "切换提供商")


@main.command("provider-list")
@click.option("--help-detail", is_flag=True, help="显示provider-list命令详细使用说明")
def list_provider(help_detail):
    """列出所有可用的 AI 服务商。"""
    if help_detail:
        help_content = """[bold]功能:[/bold]
  列出所有已配置的 AI 服务提供商及其详细信息

[bold]用法:[/bold]
  ais provider-list

[bold]显示信息:[/bold]
  • 提供商名称和当前状态（✓ 表示当前使用）
  • 使用的模型名称
  • API 端点地址
  • 是否配置了 API 密钥（🔑 图标表示）

[bold]状态说明:[/bold]
  ✓ 当前正在使用的默认提供商
  🔑 已配置 API 密钥
     无图标表示无需密钥或未配置密钥

[bold]示例输出:[/bold]
  可用的 AI 服务商:
  ✓ default_free: gpt-4o-mini (https://api.deepbricks.ai/v1/chat/completions) 🔑
    ollama: llama3 (http://localhost:11434/v1/chat/completions)
    openai: gpt-4 (https://api.openai.com/v1/chat/completions) 🔑

[bold]相关命令:[/bold]
  ais provider-use <名称>    - 切换到指定提供商
  ais provider-add ...       - 添加新的提供商
  ais provider-remove <名称> - 删除提供商
  ais config                 - 查看当前配置状态"""
        panels.info(help_content, "📚 ais provider-list 命令详细使用说明")
        return

    try:
        config = get_config()
        providers = config.get("providers", {})

        if not providers:
            panels.warning("没有配置任何 AI 服务商")
            return

        provider_list = []
        for name, provider in providers.items():
            # 显示当前使用的提供商
            current = "✓" if name == config.get("default_provider") else " "
            model = provider.get("model_name", "N/A")
            url = provider.get("base_url", "N/A")
            has_key = "🔑" if provider.get("api_key") else "  "
            provider_list.append(f"{current} {name}: {model} ({url}) {has_key}")

        content = "\n".join(provider_list)
        panels.config(content, "🔧 可用的 AI 服务商")

    except Exception as e:
        panels.error(f"列出提供商失败: {e}")


@main.command("analyze")
@click.option("--exit-code", type=int, required=True, help="命令退出码")
@click.option("--command", required=True, help="失败的命令")
@click.option("--stderr", default="", help="错误输出")
def analyze_error(exit_code, command, stderr):
    """分析命令错误。"""
    try:
        from ..core.context import collect_context
        from ..core.ai import analyze_error
        from ..core.database import save_command_log
        from ..core.streaming import create_streaming_analyzer
        import os

        # 收集上下文信息
        context = collect_context(command, exit_code, stderr)

        # 获取配置
        config = get_config()

        # 检查是否有相似的历史错误
        from ..core.database import get_similar_commands

        similar_logs = get_similar_commands(command, 3)

        if similar_logs:
            console.print("\n[bold yellow]🔍 发现相似的历史错误[/bold yellow]")
            for i, log in enumerate(similar_logs, 1):
                time_str = log.timestamp.strftime("%m-%d %H:%M")
                status = "已解决" if log.ai_explanation else "未分析"
                console.print(f"  {i}. {log.original_command} ({time_str}) - {status}")

            console.print("[dim]💡 你可以使用 'ais history <索引>' " "查看之前的分析[/dim]")

        # 创建流式分析器
        streaming_analyzer = create_streaming_analyzer(console)

        # 使用流式输出进行 AI 分析
        analysis = streaming_analyzer.analyze_with_streaming(
            analyze_error, command, exit_code, stderr, context, config
        )

        # 保存到数据库
        username = os.getenv("USER", "unknown")
        save_command_log(
            username=username,
            command=command,
            exit_code=exit_code,
            stderr=stderr,
            context=context,
            ai_explanation=analysis.get("explanation", ""),
            ai_suggestions=analysis.get("suggestions", []),
        )

        # 显示分析结果
        if analysis and isinstance(analysis, dict) and analysis.get("explanation"):
            # 使用Panel美化AI分析结果输出
            analysis_panel = Panel(
                Markdown(analysis["explanation"]),
                title="[bold blue]🤖 AI 错误分析[/bold blue]",
                border_style="blue",
                padding=(1, 2),
                expand=False,
            )
            console.print(analysis_panel)
        elif analysis:
            # 如果analysis不是字典格式，显示调试信息
            # 使用Panel美化错误信息输出
            error_panel = Panel(
                "[red]⚠️  AI返回了非预期格式的数据[/red]",
                title="[bold red]✗  数据格式错误[/bold red]",
                border_style="red",
                padding=(1, 2),
                expand=False,
            )
            console.print(error_panel)
            console.print(f"[dim]调试信息: {type(analysis)}[/dim]")
            if isinstance(analysis, str):
                # 尝试解析字符串中的JSON
                try:
                    import json as json_module

                    parsed_analysis = json_module.loads(analysis)
                    if parsed_analysis.get("explanation"):
                        console.print(Markdown(parsed_analysis["explanation"]))
                        analysis = parsed_analysis  # 更新analysis用于后续处理
                except Exception:
                    console.print("[yellow]原始内容:[/yellow]")
                    console.print(analysis)

        suggestions = analysis.get("suggestions", [])
        follow_up_questions = analysis.get("follow_up_questions", [])
        if suggestions:
            # 显示交互式菜单
            from .interactive import show_interactive_menu

            show_interactive_menu(suggestions, console, follow_up_questions)

    except Exception as e:
        console.print(f"[red]分析失败: {e}[/red]")


@main.command("history")
@click.argument("index", type=int, required=False)
@click.option("--limit", "-n", default=10, help="显示的历史记录数量")
@click.option("--failed-only", is_flag=True, help="只显示失败的命令")
@click.option("--command-filter", help="按命令名称过滤")
@click.option("--help-detail", is_flag=True, help="显示history命令详细使用说明")
def show_history(index, limit, failed_only, command_filter, help_detail):
    """显示命令历史记录或查看指定索引的详细信息。"""
    if help_detail:
        console.print("[green]ais history 命令详细使用说明:[/green]")
        console.print()
        console.print("[bold]功能:[/bold]")
        console.print("  查看和分析命令执行历史记录，包括成功和失败的命令")
        console.print("  也可以查看指定索引的详细分析信息")
        console.print()
        console.print("[bold]用法:[/bold]")
        console.print("  ais history [索引] [选项]")
        console.print()
        console.print("[bold]参数:[/bold]")
        console.print("  索引                      查看指定记录的详细信息（可选）")
        console.print()
        console.print("[bold]选项:[/bold]")
        console.print("  -n, --limit <数量>        限制显示记录数量 (默认: 10)")
        console.print("  --failed-only            只显示失败的命令")
        console.print("  --command-filter <关键词> 按命令名称过滤")
        console.print()
        console.print("[bold]示例:[/bold]")
        console.print("  ais history                    # 显示最近10条记录")
        console.print("  ais history 3                  # 查看第3条记录的详细信息")
        console.print("  ais history -n 20              # 显示最近20条记录")
        console.print("  ais history --failed-only      # 只显示失败的命令")
        console.print("  ais history --command-filter git # 只显示包含git的命令")
        console.print()
        console.print("[bold]历史记录内容:[/bold]")
        console.print("  • 执行时间和用户")
        console.print("  • 原始命令和退出码")
        console.print("  • 是否有AI分析结果")
        console.print("  • 成功/失败状态标识")
        console.print()
        console.print("[bold]相关命令:[/bold]")
        console.print("  ais analyze               - 手动分析上一个失败命令")
        console.print()
        console.print("[dim]💡 提示: 历史记录存储在本地数据库中，保护你的隐私[/dim]")
        return

    # 如果提供了索引，显示详细信息
    if index is not None:
        show_history_detail_content(index)
        return

    try:
        from ..core.database import get_recent_logs, get_similar_commands
        from rich.table import Table
        from rich.text import Text

        console.print("\n[bold blue]📚 最近的命令历史[/bold blue]")

        # 获取历史记录
        if command_filter:
            logs = get_similar_commands(command_filter, limit)
        else:
            logs = get_recent_logs(limit)

        if failed_only:
            logs = [log for log in logs if log.exit_code != 0]

        if not logs:
            console.print("[yellow]没有找到符合条件的历史记录[/yellow]")
            return

        # 创建表格
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("索引", style="cyan", width=6, justify="center")
        table.add_column("时间", style="dim", width=16)
        table.add_column("命令", style="bold", min_width=20)
        table.add_column("状态", justify="center", width=8)
        table.add_column("分析", width=20)

        for index, log in enumerate(logs, 1):
            # 格式化时间
            time_str = log.timestamp.strftime("%m-%d %H:%M")

            # 状态显示
            if log.exit_code == 0:
                status = Text("✓  成功", style="green")
            else:
                status = Text(f"✗  {log.exit_code}", style="red")

            # 命令显示（截断长命令）
            cmd_display = log.original_command
            if len(cmd_display) > 30:
                cmd_display = cmd_display[:27] + "..."

            # 是否有 AI 分析
            has_analysis = "🤖 已分析" if log.ai_explanation else ""

            table.add_row(str(index), time_str, cmd_display, status, has_analysis)

        console.print(table)

        # 提示用户可以查看详情
        console.print("\n[dim]💡 使用 'ais history <索引>' 查看详细分析[/dim]")

    except Exception as e:
        console.print(f"[red]获取历史记录失败: {e}[/red]")


def show_history_detail_content(index):
    """显示历史命令的详细分析内容。"""
    try:
        from ..core.database import get_recent_logs
        import json

        logs = get_recent_logs(50)  # 获取更多记录用于索引

        if index < 1 or index > len(logs):
            console.print(f"[red]索引超出范围。请使用 1-{len(logs)} 之间的数字[/red]")
            return

        log = logs[index - 1]

        console.print("\n[bold blue]📖 命令详细信息[/bold blue]")
        console.print("=" * 60)

        # 基本信息
        console.print(f"[bold]时间:[/bold] {log.timestamp}")
        console.print(f"[bold]用户:[/bold] {log.username}")
        console.print(f"[bold]命令:[/bold] {log.original_command}")
        console.print(f"[bold]退出码:[/bold] {log.exit_code}")

        if log.stderr_output:
            console.print(f"[bold]错误输出:[/bold] {log.stderr_output}")

        # 上下文信息
        if log.context_json:
            try:
                context = json.loads(log.context_json)
                console.print("\n[bold cyan]📋 执行上下文:[/bold cyan]")
                console.print(f"工作目录: {context.get('cwd', 'N/A')}")
                if context.get("git_branch"):
                    console.print(f"Git 分支: {context.get('git_branch')}")
            except Exception:
                pass

        # AI 分析
        if log.ai_explanation:
            console.print("\n[bold green]🤖 AI 分析:[/bold green]")
            console.print(Markdown(log.ai_explanation))

        # AI 建议
        if log.ai_suggestions_json:
            try:
                suggestions = json.loads(log.ai_suggestions_json)
                console.print("\n[bold yellow]💡 AI 建议:[/bold yellow]")
                for i, suggestion in enumerate(suggestions, 1):
                    risk_icon = "✓ " if suggestion.get("risk_level") == "safe" else "⚠️"
                    console.print(f"{i}. {suggestion.get('command', 'N/A')} {risk_icon}")
                    console.print(f"   {suggestion.get('description', '')}")
            except Exception:
                pass

        console.print("=" * 60)

    except Exception as e:
        console.print(f"[red]获取详细信息失败: {e}[/red]")


@main.command("learn")
@click.argument("topic", required=False)
@click.option("--help-detail", is_flag=True, help="显示learn命令详细使用说明")
def learn_command(topic, help_detail):
    """学习命令行知识。"""
    if help_detail:
        console.print("[green]ais learn 命令详细使用说明:[/green]")
        console.print()
        console.print("[bold]功能:[/bold]")
        console.print("  系统学习模式，提供特定主题的完整知识体系")
        console.print("  适合从零开始学习或深入了解某个工具/概念")
        console.print()
        console.print("[bold]用法:[/bold]")
        console.print("  ais learn [主题]")
        console.print("  ais learn             # 显示所有可学习主题")
        console.print()
        console.print("[bold]内置主题:[/bold]")
        console.print("  • git     - Git 版本控制基础")
        console.print("  • ssh     - 远程连接和密钥管理")
        console.print("  • docker  - 容器化技术基础")
        console.print("  • vim     - 文本编辑器使用")
        console.print("  • grep    - 文本搜索和正则表达式")
        console.print("  • find    - 文件查找技巧")
        console.print("  • permissions - Linux 权限管理")
        console.print("  • process - 进程管理")
        console.print("  • network - 网络工具和诊断")
        console.print()
        console.print("[bold]适用场景:[/bold]")
        console.print('  • 系统学习："我想全面学习Git"')
        console.print('  • 深入了解："Docker的核心概念和常用操作"')
        console.print('  • 技能提升："掌握Vim编辑器的使用"')
        console.print('  • 知识补全："Linux权限管理完整知识"')
        console.print()
        console.print("[bold]vs 其他命令:[/bold]")
        console.print("  • 快速解答问题 → 使用 ais ask")
        console.print()
        console.print("[bold]学习内容包括:[/bold]")
        console.print("  • 概念介绍和重要性说明")
        console.print("  • 5-10个最常用命令和示例")
        console.print("  • 每个命令的使用场景")
        console.print("  • 实践建议和学习路径")
        console.print("  • 最佳实践和注意事项")
        console.print()
        console.print("[bold]相关命令:[/bold]")
        console.print("  ais ask <问题>         - 直接提问具体问题")
        console.print()
        console.print("[dim]💡 提示: 可以学习任何主题，即使不在内置列表中[/dim]")
        return

    try:
        from ..core.ai import ask_ai
        from ..core.streaming import create_streaming_learner

        if not topic:
            # 显示学习主题
            console.print("[bold blue]📚 可学习的主题:[/bold blue]")
            topics = [
                "git - Git 版本控制基础",
                "ssh - 远程连接和密钥管理",
                "docker - 容器化技术基础",
                "vim - 文本编辑器使用",
                "grep - 文本搜索和正则表达式",
                "find - 文件查找技巧",
                "permissions - Linux 权限管理",
                "process - 进程管理",
                "network - 网络工具和诊断",
            ]

            for i, topic in enumerate(topics, 1):
                console.print(f"  {i}. {topic}")

            console.print("\n[dim]使用 'ais learn <主题>' 开始学习，例如: ais learn git[/dim]")
            return

        # 获取配置
        config = get_config()

        # 创建学习函数
        def generate_learning_content(topic: str, config: dict) -> str:
            learning_prompt = f"""
            用户想学习关于 "{topic}" 的命令行知识。请提供：
            1. 这个主题的简要介绍和重要性
            2. 5-10 个最常用的命令和示例
            3. 每个命令的简单解释和使用场景
            4. 实践建议和学习路径

            请用中文回答，使用 Markdown 格式，让内容易于理解和实践。
            """
            return ask_ai(learning_prompt, config)

        # 创建流式学习器
        streaming_learner = create_streaming_learner(console)

        # 使用流式输出进行学习内容生成
        response = streaming_learner.learn_with_streaming(generate_learning_content, topic, config)

        if response:
            panels.learning_content(Markdown(response), topic.upper())
        else:
            console.print("[red]无法获取学习内容，请检查网络连接[/red]")

    except Exception as e:
        console.print(f"[red]学习功能出错: {e}[/red]")


@main.command("setup")
def setup_shell():
    """设置 shell 集成。"""
    console.print("[bold blue]🔧 设置 Shell 集成[/bold blue]")

    # Unix shell 集成
    _setup_unix_shell_integration()


def _setup_unix_shell_integration():
    """设置 Unix shell 集成。"""
    import os
    import ais

    # 检测 shell 类型
    shell = os.environ.get("SHELL", "/bin/bash")
    shell_name = os.path.basename(shell)

    # 获取集成脚本路径
    package_path = os.path.dirname(ais.__file__)
    script_path = os.path.join(package_path, "shell", "integration.sh")

    # 如果包内没有，创建集成脚本目录和文件
    if not os.path.exists(script_path):
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        _create_integration_script(script_path)

    console.print(f"检测到的 Shell: {shell_name}")

    if not os.path.exists(script_path):
        console.print("[red]✗  集成脚本不存在[/red]")
        return

    # 检测配置文件
    config_files = {
        "bash": ["~/.bashrc", "~/.bash_profile"],
        "zsh": ["~/.zshrc"],
    }

    target_files = config_files.get(shell_name, ["~/.bashrc"])

    # 找到存在的配置文件或创建默认的
    config_file = None
    for cf in target_files:
        expanded_path = os.path.expanduser(cf)
        if os.path.exists(expanded_path):
            config_file = expanded_path
            break

    if not config_file:
        config_file = os.path.expanduser(target_files[0])
        # 创建文件
        open(config_file, "a").close()

    # 检查是否已经添加了集成配置
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            content = f.read()

        if "# START AIS INTEGRATION" not in content:
            # 自动添加集成配置
            integration_config = f"""

# START AIS INTEGRATION
# AIS - 上下文感知的错误分析学习助手自动集成
if [ -f "{script_path}" ]; then
    source "{script_path}"
fi
# END AIS INTEGRATION
"""
            with open(config_file, "a") as f:
                f.write(integration_config)

            console.print(
                f"\n[green]✓  集成配置已添加到: " f"{os.path.basename(config_file)}[/green]"
            )
            console.print(
                f"[bold cyan]source {config_file}[/bold cyan] " f"[dim]# 让配置立即生效[/dim]"
            )
            console.print("[green]✨ 完成后，命令失败时将自动显示AI分析[/green]")
        else:
            console.print(
                f"\n[yellow]ℹ️ 集成配置已存在: " f"{os.path.basename(config_file)}[/yellow]"
            )
            console.print("[green]✨ AIS功能已可用，命令失败时将自动显示AI分析[/green]")
    else:
        console.print("[red]✗  无法创建配置文件[/red]")


@main.command("test-integration")
def test_integration():
    """测试 shell 集成是否工作。"""
    console.print("[bold blue]🧪 测试 Shell 集成[/bold blue]")

    try:
        # 模拟一个错误命令的分析
        console.print("模拟命令错误: mdkirr /test")

        from ..core.context import collect_context
        from ..core.ai import analyze_error
        from ..core.database import save_command_log
        import os

        # 模拟上下文收集
        context = collect_context("mdkirr /test", 127, "mdkirr: command not found")
        config = get_config()

        console.print("✓  上下文收集: 成功")

        # 测试 AI 分析
        analysis = analyze_error("mdkirr /test", 127, "mdkirr: command not found", context, config)

        console.print("✓  AI 分析: 成功")

        # 测试数据库保存
        username = os.getenv("USER", "test")
        log_id = save_command_log(
            username=username,
            command="mdkirr /test",
            exit_code=127,
            stderr="mdkirr: command not found",
            context=context,
            ai_explanation=analysis.get("explanation", ""),
            ai_suggestions=analysis.get("suggestions", []),
        )

        console.print(f"✓  数据库保存: 成功 (ID: {log_id})")

        console.print("\n[bold green]🎉 所有组件都工作正常！[/bold green]")
        console.print("如果您遇到自动分析不工作的问题，请:")
        console.print("1. 运行 'ais setup' 设置 shell 集成")
        console.print("2. 确保您在交互式终端中")
        console.print("3. 重新加载 shell 配置")

    except Exception as e:
        console.print(f"[red]✗  测试失败: {e}[/red]")


@main.command("report")
@click.option("--html", is_flag=True, help="生成HTML格式的可视化报告")
@click.option("--output", "-o", default="ais_report.html", help="HTML报告输出文件名")
@click.option("--open", "open_browser", is_flag=True, help="生成后自动打开浏览器")
def generate_report(html, output, open_browser):
    """生成学习成长报告。"""
    try:
        if html:
            # 生成HTML报告
            _generate_html_report(output, open_browser)
        else:
            # 生成传统文本报告
            _generate_text_report()

    except Exception as e:
        console.print(f"[red]报告生成失败: {e}[/red]")
        console.print("[dim]提示: 请确保已有命令执行历史记录[/dim]")


def _generate_text_report():
    """生成传统文本报告。"""
    from ..core.report import LearningReportGenerator
    from rich.markdown import Markdown

    console.print("[bold blue]📊 生成学习成长报告...[/bold blue]")

    # 创建报告生成器
    report_generator = LearningReportGenerator(days_back=30)

    # 生成报告
    report = report_generator.generate_report()

    # 检查是否有数据
    if report["error_summary"]["total_errors"] == 0:
        console.print("\n[yellow]📝 暂无错误历史数据[/yellow]")
        console.print("\n[dim]提示:[/dim]")
        console.print("- 使用命令行时遇到错误，AIS会自动记录和分析")
        console.print("- 运行一些命令后再使用 'ais report' 查看学习报告")
        console.print("- 你也可以手动运行 'ais analyze' 分析特定错误")
        return

    # 格式化并显示报告
    formatted_report = report_generator.format_report_for_display(report)

    # 使用Panel显示报告
    panels.learning_content(Markdown(formatted_report), "📊 学习成长报告")


def _generate_html_report(output: str, open_browser: bool):
    """生成HTML格式报告。"""
    try:
        from ..core.html_report import HTMLReportGenerator
        import webbrowser
        import os

        console.print("[bold blue]📊 生成HTML可视化报告...[/bold blue]")

        # 创建HTML报告生成器
        html_generator = HTMLReportGenerator(days_back=30)

        # 生成HTML报告
        html_content = html_generator.generate_html_report()

        # 保存文件
        with open(output, "w", encoding="utf-8") as f:
            f.write(html_content)

        console.print(f"[green]✓ HTML报告已生成: {output}[/green]")
        console.print(f"[dim]文件路径: {os.path.abspath(output)}[/dim]")

        # 自动打开浏览器
        if open_browser:
            try:
                webbrowser.open(f"file://{os.path.abspath(output)}")
                console.print("[green]✓ 已在浏览器中打开报告[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️ 无法自动打开浏览器: {e}[/yellow]")
                console.print(f"[dim]请手动打开: {os.path.abspath(output)}[/dim]")

    except ImportError:
        console.print("[red]✗ 缺少依赖库[/red]")
        console.print("请安装必要的依赖：")
        console.print("[bold cyan]pip install plotly[/bold cyan]")
    except Exception as e:
        console.print(f"[red]HTML报告生成失败: {e}[/red]")


@main.command("help-all")
def help_all():
    """显示所有命令的详细帮助汇总。"""
    console.print("[bold green]🚀 AIS - 上下文感知的错误分析学习助手 详细帮助汇总[/bold green]")
    console.print()
    console.print("[bold]核心功能命令:[/bold]")
    console.print("  ais ask --help-detail       - AI 问答功能详细说明")
    console.print("  ais learn --help-detail     - 学习功能详细说明")
    console.print("  ais report                  - 生成文本格式学习成长报告")
    console.print("  ais report --html           - 生成HTML可视化报告（推荐）")
    console.print("  ais report --html --open    - 生成HTML报告并自动打开浏览器")
    console.print()
    console.print("[bold]配置管理命令:[/bold]")
    console.print("  ais config --help-context   - 配置管理详细说明")
    console.print("  ais on/off                  - 开启/关闭自动分析")
    console.print()
    console.print("[bold]历史记录命令:[/bold]")
    console.print("  ais history --help-detail   - 历史记录查看详细说明")
    console.print("  ais history <索引>         - 查看具体记录详情")
    console.print()
    console.print("[bold]AI 服务商管理:[/bold]")
    console.print("  ais provider-add --help-detail    - 添加服务商详细说明")
    console.print("  ais provider-list --help-detail   - 列出服务商详细说明")
    console.print("  ais provider-use <名称>           - 切换服务商")
    console.print("  ais provider-remove <名称>        - 删除服务商")
    console.print()
    console.print("[bold]系统管理命令:[/bold]")
    console.print("  ais analyze                  - 手动分析错误")
    console.print("  ais setup                   - 设置 Shell 集成")
    console.print("  ais test-integration         - 测试集成是否正常")
    console.print()
    console.print("[bold green]💡 使用技巧:[/bold green]")
    console.print("  • 每个命令都有 --help 选项查看基本帮助")
    console.print("  • 大多数命令支持 --help-detail 查看详细说明")
    console.print("  • 配置相关帮助使用 --help-context")
    console.print("  • 错误分析会自动触发，也可手动调用")
    console.print()
    console.print("[dim]更多信息请查看: ais --help[/dim]")


if __name__ == "__main__":
    main()
