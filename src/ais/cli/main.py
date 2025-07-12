"""Main CLI interface for AIS."""

import click
from rich.console import Console
from rich.markdown import Markdown

from ..core.config import get_config, set_config
from ..core.ai import ask_ai

console = Console()


def _create_integration_script(script_path: str):
    """创建Shell集成脚本。"""
    import os

    with open(script_path, "w") as f:
        f.write(
            """#!/bin/bash
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
            if [[ "$last_command" != *"_ais_"* ]] && \
               [[ "$last_command" != *"ais_"* ]] && \
               [[ "$last_command" != *"history"* ]]; then
                # 调用 ais analyze 进行分析
                echo  # 添加空行分隔
                ais analyze --exit-code "$current_exit_code" \
                    --command "$last_command"
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
"""
        )
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
        # 自动运行setup-shell但不显示输出
        import ais

        package_path = os.path.dirname(ais.__file__)
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
# AIS - AI 智能终端助手自动集成
if [ -f "{script_path}" ]; then
    source "{script_path}"
fi
# END AIS INTEGRATION
"""
                with open(config_file, "a") as f:
                    f.write(integration_config)

        # 确保默认配置中启用自动分析
        config_file_path = config_dir / "config.toml"
        if not config_file_path.exists():
            default_config = """# AIS 配置文件
default_provider = "default_free"
auto_analysis = true
context_level = "standard"
sensitive_dirs = ["~/.ssh", "~/.config/ais", "~/.aws"]

[providers.default_free]
base_url = "https://api.deepbricks.ai/v1/chat/completions"
model_name = "gpt-4o-mini"
api_key = "sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg"
"""
            config_file_path.write_text(default_config)

        # 标记已完成自动设置
        marker_file.write_text("auto setup completed")

        # 显示一次性提示
        console.print("\n[green]🎉 AIS 已自动配置完成！[/green]")
        console.print(
            "[yellow]💡 为了启用自动错误分析，请重新加载Shell配置：[/yellow]"
        )
        console.print(f"[dim]   source {config_file}[/dim]")
        console.print("[dim]   或者重新打开终端[/dim]")
        console.print(
            "\n[green]✨ 之后当命令失败时，将自动显示AI分析！[/green]"
        )

    except Exception:
        # 静默失败，不影响正常使用
        pass


@click.group()
@click.version_option(version="0.1.0", prog_name="ais")
@click.pass_context
def main(ctx):
    """AIS - AI-powered terminal assistant.

    智能终端助手，通过 AI 技术帮助用户分析错误、学习命令和提高效率。

    💡 提示: 大多数命令都支持 --help-detail 选项查看详细使用说明

    示例:
      ais ask --help-detail     查看 ask 命令详细帮助
      ais config --help-context 查看配置帮助
      ais history --help-detail 查看历史命令帮助
    """
    # 只在执行具体命令时进行自动设置（不是--help时）
    if ctx.invoked_subcommand and ctx.invoked_subcommand != "help":
        _auto_setup_shell_integration()


def _handle_error(error_msg: str) -> None:
    """统一的错误处理函数。"""
    console.print(f"[red]错误: {error_msg}[/red]")


@main.command()
@click.argument("question", required=False)
@click.option("--help-detail", is_flag=True, help="显示ask命令详细使用说明")
def ask(question, help_detail):
    """Ask AI a question."""
    if help_detail:
        console.print("[green]ais ask 命令详细使用说明:[/green]")
        console.print()
        console.print("[bold]功能:[/bold]")
        console.print("  快速问答模式，立即获得具体问题的答案")
        console.print("  适合解决当前遇到的具体问题或疑惑")
        console.print()
        console.print("[bold]用法:[/bold]")
        console.print("  ais ask <问题>")
        console.print()
        console.print("[bold]适用场景:[/bold]")
        console.print('  • 解释概念："什么是Docker容器？"')
        console.print('  • 快速答疑："Git冲突是什么意思？"')
        console.print('  • 概念查询："Linux权限755代表什么？"')
        console.print('  • 故障诊断："为什么命令执行失败？"')
        console.print()
        console.print("[bold]vs 其他命令:[/bold]")
        console.print("  • 需要具体操作步骤 → 使用 ais suggest")
        console.print("  • 想系统学习主题 → 使用 ais learn")
        console.print()
        console.print("[bold]提示:[/bold]")
        console.print("  • 问题用引号包围，避免 shell 解析问题")
        console.print("  • 可以问任何编程、运维、工具使用相关问题")
        console.print("  • AI 会提供中文回答和实用建议")
        console.print("  • 回答基于当前配置的 AI 服务提供商")
        console.print()
        console.print("[bold]相关命令:[/bold]")
        console.print("  ais config --list-providers - 查看可用的 AI 服务商")
        console.print("  ais suggest <任务>          - 获取任务相关的命令建议")
        console.print("  ais learn <主题>            - 学习特定主题知识")
        return

    if not question:
        console.print("[red]错误: 请提供要询问的问题[/red]")
        console.print('[dim]用法: ais ask "你的问题"[/dim]')
        console.print("[dim]帮助: ais ask --help-detail[/dim]")
        return

    try:
        config = get_config()
        response = ask_ai(question, config)

        if response:
            console.print(Markdown(response))
        else:
            console.print("[red]Failed to get AI response[/red]")
    except Exception as e:
        _handle_error(str(e))


@main.command()
@click.option("--set", "set_key", help="设置配置项 (key=value)")
@click.option("--get", "get_key", help="获取配置项值")
@click.option(
    "--list-providers", is_flag=True, help="列出所有可用的 AI 服务商"
)
@click.option("--help-context", is_flag=True, help="显示上下文级别配置帮助")
def config(set_key, get_key, list_providers, help_context):
    """显示或修改配置。"""
    try:
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
                        "[red]错误: context_level 必须是 minimal, "
                        "standard 或 detailed[/red]"
                    )
                    console.print(
                        "[dim]使用 'ais config --help-context' 查看详细说明[/dim]"
                    )
                    return
            elif key == "auto_analysis":
                if value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                else:
                    console.print(
                        "[red]错误: auto_analysis 必须是 true 或 false[/red]"
                    )
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
                current = (
                    "✓" if name == config.get("default_provider") else " "
                )
                console.print(
                    f"{current} {name}: {provider.get('model_name', 'N/A')}"
                )

        elif help_context:
            # 显示上下文配置帮助
            console.print("[green]上下文收集级别配置帮助:[/green]")
            console.print()
            console.print("[bold]可用级别:[/bold]")
            console.print(
                "  • [blue]minimal[/blue]  - 只收集基本信息（命令、退出码、目录）"
            )
            console.print(
                "  • [blue]standard[/blue] - 收集标准信息"
                "（+ 命令历史、文件列表、Git状态）[dim]（默认）[/dim]"
            )
            console.print(
                "  • [blue]detailed[/blue] - 收集详细信息"
                "（+ 系统信息、环境变量、完整目录）"
            )
            console.print()
            console.print("[bold]设置方法:[/bold]")
            console.print("  ais config --set context_level=minimal")
            console.print("  ais config --set context_level=standard")
            console.print("  ais config --set context_level=detailed")
            console.print()
            console.print("[bold]其他配置项:[/bold]")
            console.print(
                "  auto_analysis=true/false    - 开启/关闭自动错误分析"
            )
            console.print(
                "  default_provider=name       - 设置默认AI服务提供商"
            )
            console.print()
            console.print("[dim]查看当前配置: ais config[/dim]")

        else:
            # 显示当前配置
            console.print("[green]当前配置:[/green]")
            console.print(
                f"默认提供商: {config.get('default_provider', 'default_free')}"
            )

            auto_analysis = config.get("auto_analysis", True)
            auto_status = "✅ 开启" if auto_analysis else "❌ 关闭"
            console.print(f"自动分析: {auto_status}")

            context_level = config.get("context_level", "standard")
            console.print(f"上下文级别: {context_level}")

            sensitive_count = len(config.get("sensitive_dirs", []))
            console.print(f"敏感目录: {sensitive_count} 个")

            console.print()
            console.print("[dim]💡 提示:[/dim]")
            console.print(
                "[dim]  ais config --help-context  - 查看上下文配置帮助[/dim]"
            )
            console.print(
                "[dim]  ais config --list-providers - 查看AI服务提供商[/dim]"
            )
            console.print(
                "[dim]  ais config --set key=value  - 修改配置[/dim]"
            )

    except Exception as e:
        console.print(f"[red]配置错误: {e}[/red]")


def _toggle_auto_analysis(enabled: bool) -> None:
    """开启/关闭自动分析的通用函数。"""
    try:
        set_config("auto_analysis", enabled)
        status = "已开启" if enabled else "已关闭"
        color = "green" if enabled else "yellow"
        console.print(f"[{color}]✓ 自动错误分析{status}[/{color}]")
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


def _handle_provider_operation(
    operation, name, success_msg, error_prefix, *args
):
    """处理提供商操作的通用函数。"""
    try:
        operation(name, *args)
        console.print(f"[green]✓ {success_msg}: {name}[/green]")
    except Exception as e:
        console.print(f"[red]{error_prefix}失败: {e}[/red]")


@main.command("add-provider")
@click.argument("name", required=False)
@click.option("--url", help="API 基础 URL")
@click.option("--model", help="模型名称")
@click.option("--key", help="API 密钥 (可选)")
@click.option(
    "--help-detail", is_flag=True, help="显示add-provider命令详细使用说明"
)
def add_provider_cmd(name, url, model, key, help_detail):
    """添加新的 AI 服务商。"""
    if help_detail:
        console.print("[green]ais add-provider 命令详细使用说明:[/green]")
        console.print()
        console.print("[bold]功能:[/bold]")
        console.print("  添加新的 AI 服务提供商配置，支持自定义 API 服务")
        console.print()
        console.print("[bold]用法:[/bold]")
        console.print(
            "  ais add-provider <名称> --url <API地址> --model <模型名> [--key <密钥>]"
        )
        console.print()
        console.print("[bold]参数:[/bold]")
        console.print("  名称       提供商的唯一标识名称")
        console.print("  --url      API 基础 URL 地址")
        console.print("  --model    使用的模型名称")
        console.print("  --key      API 密钥（可选，某些服务需要）")
        console.print()
        console.print("[bold]示例:[/bold]")
        console.print("  # 添加 OpenAI 服务")
        console.print("  ais add-provider openai \\")
        console.print(
            "    --url https://api.openai.com/v1/chat/completions \\"
        )
        console.print("    --model gpt-4 \\")
        console.print("    --key your_api_key")
        console.print()
        console.print("  # 添加本地 Ollama 服务")
        console.print("  ais add-provider ollama \\")
        console.print(
            "    --url http://localhost:11434/v1/chat/completions \\"
        )
        console.print("    --model llama3")
        console.print()
        console.print("[bold]常用服务配置:[/bold]")
        console.print("  • OpenAI: https://api.openai.com/v1/chat/completions")
        console.print(
            "  • Azure OpenAI: https://your-resource.openai.azure.com/"
            "openai/deployments/your-deployment/chat/completions"
            "?api-version=2023-05-15"
        )
        console.print("  • Ollama: http://localhost:11434/v1/chat/completions")
        console.print(
            "  • Claude (Anthropic): https://api.anthropic.com/v1/messages"
        )
        console.print()
        console.print("[bold]相关命令:[/bold]")
        console.print("  ais list-provider         - 查看所有配置的提供商")
        console.print("  ais use-provider <名称>   - 切换默认提供商")
        console.print("  ais remove-provider <名称> - 删除提供商配置")
        console.print()
        console.print(
            "[dim]💡 提示: 添加后使用 'ais use-provider <名称>' 切换到新提供商[/dim]"
        )
        return

    if not name or not url or not model:
        console.print("[red]错误: 缺少必需参数[/red]")
        console.print(
            "[dim]用法: ais add-provider <名称> --url <地址> --model <模型>[/dim]"
        )
        console.print("[dim]帮助: ais add-provider --help-detail[/dim]")
        return

    from ..core.config import add_provider

    _handle_provider_operation(
        add_provider, name, "已添加提供商", "添加提供商", url, model, key
    )


@main.command("remove-provider")
@click.argument("name")
def remove_provider_cmd(name):
    """删除 AI 服务商。"""
    from ..core.config import remove_provider

    _handle_provider_operation(
        remove_provider, name, "已删除提供商", "删除提供商"
    )


@main.command("use-provider")
@click.argument("name")
def use_provider_cmd(name):
    """切换默认 AI 服务商。"""
    from ..core.config import use_provider

    _handle_provider_operation(
        use_provider, name, "已切换到提供商", "切换提供商"
    )


@main.command("list-provider")
@click.option(
    "--help-detail", is_flag=True, help="显示list-provider命令详细使用说明"
)
def list_provider(help_detail):
    """列出所有可用的 AI 服务商。"""
    if help_detail:
        console.print("[green]ais list-provider 命令详细使用说明:[/green]")
        console.print()
        console.print("[bold]功能:[/bold]")
        console.print("  列出所有已配置的 AI 服务提供商及其详细信息")
        console.print()
        console.print("[bold]用法:[/bold]")
        console.print("  ais list-provider")
        console.print()
        console.print("[bold]显示信息:[/bold]")
        console.print("  • 提供商名称和当前状态（✓ 表示当前使用）")
        console.print("  • 使用的模型名称")
        console.print("  • API 端点地址")
        console.print("  • 是否配置了 API 密钥（🔑 图标表示）")
        console.print()
        console.print("[bold]状态说明:[/bold]")
        console.print("  ✓ 当前正在使用的默认提供商")
        console.print("  🔑 已配置 API 密钥")
        console.print("     无图标表示无需密钥或未配置密钥")
        console.print()
        console.print("[bold]示例输出:[/bold]")
        console.print("  [green]可用的 AI 服务商:[/green]")
        console.print(
            "  ✓ default_free: gpt-4o-mini "
            "(https://api.deepbricks.ai/v1/chat/completions) 🔑"
        )
        console.print(
            "    ollama: llama3 (http://localhost:11434/v1/chat/completions)"
        )
        console.print(
            "    openai: gpt-4 (https://api.openai.com/v1/chat/completions) 🔑"
        )
        console.print()
        console.print("[bold]相关命令:[/bold]")
        console.print("  ais use-provider <名称>    - 切换到指定提供商")
        console.print("  ais add-provider ...       - 添加新的提供商")
        console.print("  ais remove-provider <名称> - 删除提供商")
        console.print("  ais config                 - 查看当前配置状态")
        return

    try:
        config = get_config()
        providers = config.get("providers", {})

        if not providers:
            console.print("[yellow]没有配置任何 AI 服务商[/yellow]")
            return

        console.print("[green]可用的 AI 服务商:[/green]")
        for name, provider in providers.items():
            # 显示当前使用的提供商
            current = "✓" if name == config.get("default_provider") else " "
            model = provider.get("model_name", "N/A")
            url = provider.get("base_url", "N/A")
            has_key = "🔑" if provider.get("api_key") else "  "

            console.print(f"{current} {name}: {model} ({url}) {has_key}")

    except Exception as e:
        console.print(f"[red]列出提供商失败: {e}[/red]")


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
                console.print(
                    f"  {i}. {log.original_command} ({time_str}) - {status}"
                )

            console.print(
                "[dim]💡 你可以使用 'ais history-detail <索引>' "
                "查看之前的分析[/dim]"
            )

        # 使用 AI 分析错误
        analysis = analyze_error(command, exit_code, stderr, context, config)

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
        if (
            analysis
            and isinstance(analysis, dict)
            and analysis.get("explanation")
        ):
            console.print("\n[bold blue]🤖 AI 错误分析[/bold blue]")
            console.print()
            console.print(Markdown(analysis["explanation"]))
        elif analysis:
            # 如果analysis不是字典格式，显示调试信息
            console.print("\n[bold blue]🤖 AI 错误分析[/bold blue]")
            console.print()
            console.print("[red]⚠️  AI返回了非预期格式的数据[/red]")
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
@click.option("--limit", "-n", default=10, help="显示的历史记录数量")
@click.option("--failed-only", is_flag=True, help="只显示失败的命令")
@click.option("--command-filter", help="按命令名称过滤")
@click.option(
    "--help-detail", is_flag=True, help="显示history命令详细使用说明"
)
def show_history(limit, failed_only, command_filter, help_detail):
    """显示命令历史记录。"""
    if help_detail:
        console.print("[green]ais history 命令详细使用说明:[/green]")
        console.print()
        console.print("[bold]功能:[/bold]")
        console.print("  查看和分析命令执行历史记录，包括成功和失败的命令")
        console.print()
        console.print("[bold]用法:[/bold]")
        console.print("  ais history [选项]")
        console.print()
        console.print("[bold]选项:[/bold]")
        console.print(
            "  -n, --limit <数量>        限制显示记录数量 (默认: 10)"
        )
        console.print("  --failed-only            只显示失败的命令")
        console.print("  --command-filter <关键词> 按命令名称过滤")
        console.print()
        console.print("[bold]示例:[/bold]")
        console.print("  ais history                    # 显示最近10条记录")
        console.print("  ais history -n 20              # 显示最近20条记录")
        console.print("  ais history --failed-only      # 只显示失败的命令")
        console.print(
            "  ais history --command-filter git # 只显示包含git的命令"
        )
        console.print()
        console.print("[bold]历史记录内容:[/bold]")
        console.print("  • 执行时间和用户")
        console.print("  • 原始命令和退出码")
        console.print("  • 是否有AI分析结果")
        console.print("  • 成功/失败状态标识")
        console.print()
        console.print("[bold]相关命令:[/bold]")
        console.print("  ais history-detail <索引>  - 查看具体记录的详细分析")
        console.print("  ais analyze               - 手动分析上一个失败命令")
        console.print()
        console.print(
            "[dim]💡 提示: 历史记录存储在本地数据库中，保护你的隐私[/dim]"
        )
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
        table.add_column("时间", style="dim", width=16)
        table.add_column("命令", style="bold", min_width=20)
        table.add_column("状态", justify="center", width=8)
        table.add_column("分析", width=20)

        for log in logs:
            # 格式化时间
            time_str = log.timestamp.strftime("%m-%d %H:%M")

            # 状态显示
            if log.exit_code == 0:
                status = Text("✅ 成功", style="green")
            else:
                status = Text(f"❌ {log.exit_code}", style="red")

            # 命令显示（截断长命令）
            cmd_display = log.original_command
            if len(cmd_display) > 30:
                cmd_display = cmd_display[:27] + "..."

            # 是否有 AI 分析
            has_analysis = "🤖 已分析" if log.ai_explanation else ""

            table.add_row(time_str, cmd_display, status, has_analysis)

        console.print(table)

        # 提示用户可以查看详情
        console.print(
            "\n[dim]💡 使用 'ais history-detail <索引>' 查看详细分析[/dim]"
        )

    except Exception as e:
        console.print(f"[red]获取历史记录失败: {e}[/red]")


@main.command("history-detail")
@click.argument("index", type=int)
def show_history_detail(index):
    """显示历史命令的详细分析。"""
    try:
        from ..core.database import get_recent_logs
        import json

        logs = get_recent_logs(50)  # 获取更多记录用于索引

        if index < 1 or index > len(logs):
            console.print(
                f"[red]索引超出范围。请使用 1-{len(logs)} 之间的数字[/red]"
            )
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
                    risk_icon = (
                        "✅" if suggestion.get("risk_level") == "safe" else "⚠️"
                    )
                    console.print(
                        f"{i}. {suggestion.get('command', 'N/A')} {risk_icon}"
                    )
                    console.print(f"   {suggestion.get('description', '')}")
            except Exception:
                pass

        console.print("=" * 60)

    except Exception as e:
        console.print(f"[red]获取详细信息失败: {e}[/red]")


@main.command("suggest")
@click.argument("task", required=False)
@click.option(
    "--help-detail", is_flag=True, help="显示suggest命令详细使用说明"
)
def suggest_command(task, help_detail):
    """根据任务描述建议命令。"""
    if help_detail:
        console.print("[green]ais suggest 命令详细使用说明:[/green]")
        console.print()
        console.print("[bold]功能:[/bold]")
        console.print("  任务导向模式，提供完成具体任务的命令方案")
        console.print("  重点关注操作步骤、安全性和最佳实践")
        console.print()
        console.print("[bold]用法:[/bold]")
        console.print("  ais suggest <任务描述>")
        console.print()
        console.print("[bold]适用场景:[/bold]")
        console.print('  • 需要完成具体任务："压缩文件夹"')
        console.print('  • 寻找操作方法："批量重命名文件"')
        console.print('  • 系统管理任务："监控系统资源"')
        console.print('  • 数据处理任务："备份数据库"')
        console.print()
        console.print("[bold]vs 其他命令:[/bold]")
        console.print("  • 只想了解概念 → 使用 ais ask")
        console.print("  • 想深入学习主题 → 使用 ais learn")
        console.print()
        console.print("[bold]建议内容包括:[/bold]")
        console.print("  • 推荐命令（按安全性排序）")
        console.print("  • 每个命令的详细解释")
        console.print("  • 使用注意事项和风险提示")
        console.print("  • 相关学习资源和延伸知识")
        console.print("  • 最佳实践建议")
        console.print()
        console.print("[bold]安全特性:[/bold]")
        console.print("  • 命令按安全等级排序")
        console.print("  • 危险操作会特别标注")
        console.print("  • 提供风险评估和预防措施")
        console.print()
        console.print("[bold]适用场景:[/bold]")
        console.print("  • 不确定如何完成某个任务")
        console.print("  • 寻找更好的命令替代方案")
        console.print("  • 学习任务相关的工具和技巧")
        console.print("  • 了解操作的安全性和风险")
        console.print()
        console.print("[bold]相关命令:[/bold]")
        console.print("  ais ask <问题>         - 直接提问具体问题")
        console.print("  ais learn <主题>       - 学习特定主题知识")
        console.print()
        console.print("[dim]💡 提示: 任务描述越具体，建议越准确[/dim]")
        return

    if not task:
        console.print("[red]错误: 请提供任务描述[/red]")
        console.print('[dim]用法: ais suggest "你要完成的任务"[/dim]')
        console.print("[dim]帮助: ais suggest --help-detail[/dim]")
        return

    try:
        from ..core.ai import ask_ai

        config = get_config()

        suggestion_prompt = f"""
        用户想要完成这个任务："{task}"

        请提供：
        1. 推荐的命令（按安全性排序）
        2. 每个命令的详细解释
        3. 使用注意事项和风险提示
        4. 相关的学习资源或延伸知识

        请用中文回答，使用 Markdown 格式。重点关注安全性和最佳实践。
        """

        response = ask_ai(suggestion_prompt, config)

        if response:
            console.print(f"\n[bold blue]💡 任务建议: {task}[/bold blue]")
            console.print()
            console.print(Markdown(response))
        else:
            console.print("[red]无法获取建议，请检查网络连接[/red]")

    except Exception as e:
        console.print(f"[red]建议功能出错: {e}[/red]")


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
        console.print("  • 完成具体任务 → 使用 ais suggest")
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
        console.print("  ais suggest <任务>     - 获取任务相关命令建议")
        console.print()
        console.print(
            "[dim]💡 提示: 可以学习任何主题，即使不在内置列表中[/dim]"
        )
        return

    try:
        from ..core.ai import ask_ai

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

            console.print(
                "\n[dim]使用 'ais learn <主题>' 开始学习，例如: ais learn git[/dim]"
            )
            return

        # 生成学习内容
        config = get_config()

        learning_prompt = f"""
        用户想学习关于 "{topic}" 的命令行知识。请提供：
        1. 这个主题的简要介绍和重要性
        2. 5-10 个最常用的命令和示例
        3. 每个命令的简单解释和使用场景
        4. 实践建议和学习路径

        请用中文回答，使用 Markdown 格式，让内容易于理解和实践。
        """

        response = ask_ai(learning_prompt, config)

        if response:
            console.print(
                f"\n[bold blue]📖 {topic.upper()} 学习指南[/bold blue]"
            )
            console.print()
            console.print(Markdown(response))
        else:
            console.print("[red]无法获取学习内容，请检查网络连接[/red]")

    except Exception as e:
        console.print(f"[red]学习功能出错: {e}[/red]")


@main.command("setup-shell")
def setup_shell():
    """设置 shell 集成。"""
    import os

    console.print("[bold blue]🔧 设置 Shell 集成[/bold blue]")

    # 检测 shell 类型
    shell = os.environ.get("SHELL", "/bin/bash")
    shell_name = os.path.basename(shell)

    # 获取集成脚本路径
    import ais

    # 优先查找已安装包的路径
    package_path = os.path.dirname(ais.__file__)
    script_path = os.path.join(package_path, "shell", "integration.sh")

    # 如果包内没有，创建集成脚本目录和文件
    if not os.path.exists(script_path):
        os.makedirs(os.path.dirname(script_path), exist_ok=True)

        # 尝试从项目根目录复制脚本
        src_script = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "scripts",
            "shell",
            "integration.sh",
        )
        if os.path.exists(src_script):
            import shutil

            shutil.copy2(src_script, script_path)
        else:
            # 如果源脚本不存在，则创建内联脚本
            _create_integration_script(script_path)

    console.print(f"检测到的 Shell: {shell_name}")
    console.print(f"集成脚本路径: {script_path}")

    if not os.path.exists(script_path):
        console.print("[red]❌ 集成脚本不存在[/red]")
        return

    # 检测配置文件
    config_files = {
        "bash": ["~/.bashrc", "~/.bash_profile"],
        "zsh": ["~/.zshrc"],
    }

    target_files = config_files.get(shell_name, ["~/.bashrc"])

    console.print(
        "\n[bold yellow]📝 请手动添加以下内容到您的 shell 配置文件中:[/bold yellow]"
    )

    for config_file in target_files:
        expanded_path = os.path.expanduser(config_file)
        if os.path.exists(expanded_path):
            console.print(f"\n编辑文件: [bold]{config_file}[/bold]")
            break
    else:
        console.print(f"\n编辑文件: [bold]{target_files[0]}[/bold]")

    console.print(
        f"""
[dim]# START AIS INTEGRATION[/dim]
[green]if [ -f "{script_path}" ]; then
    source "{script_path}"
fi[/green]
[dim]# END AIS INTEGRATION[/dim]

然后运行: [bold]source ~/.bashrc[/bold] 或重启终端

💡 或者临时测试: [bold]source {script_path}[/bold]
"""
    )


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
        context = collect_context(
            "mdkirr /test", 127, "mdkirr: command not found"
        )
        config = get_config()

        console.print("✅ 上下文收集: 成功")

        # 测试 AI 分析
        analysis = analyze_error(
            "mdkirr /test", 127, "mdkirr: command not found", context, config
        )

        console.print("✅ AI 分析: 成功")

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

        console.print(f"✅ 数据库保存: 成功 (ID: {log_id})")

        console.print("\n[bold green]🎉 所有组件都工作正常！[/bold green]")
        console.print("如果您遇到自动分析不工作的问题，请:")
        console.print("1. 运行 'ais setup-shell' 设置 shell 集成")
        console.print("2. 确保您在交互式终端中")
        console.print("3. 重新加载 shell 配置")

    except Exception as e:
        console.print(f"[red]❌ 测试失败: {e}[/red]")


@main.command("which")
def which_command():
    """帮助选择合适的命令类型。"""
    console.print(
        "[bold green]🤔 不知道用哪个命令？让我来帮你选择！[/bold green]"
    )
    console.print()
    console.print("[bold blue]📊 命令选择指南：[/bold blue]")
    console.print()

    console.print(
        "[bold yellow]🔍 ais ask[/bold yellow] - [blue]快速问答模式[/blue]"
    )
    console.print("  适用：想了解概念、快速解答疑问")
    console.print('  示例："什么是Docker？" "Git冲突怎么回事？"')
    console.print()

    console.print(
        "[bold yellow]💡 ais suggest[/bold yellow] - [blue]任务解决模式[/blue]"
    )
    console.print("  适用：需要完成具体任务、寻找操作方法")
    console.print('  示例："压缩文件夹" "批量重命名文件"')
    console.print()

    console.print(
        "[bold yellow]📚 ais learn[/bold yellow] - [blue]系统学习模式[/blue]"
    )
    console.print("  适用：从头学习工具、深入掌握概念")
    console.print('  示例："git" "docker" "vim"')
    console.print()

    console.print("[bold green]🎯 快速决策树：[/bold green]")
    console.print("  ❓ 不懂概念/原理 → [yellow]ais ask[/yellow]")
    console.print("  🎯 要完成具体任务 → [yellow]ais suggest[/yellow]")
    console.print("  📖 想系统性学习 → [yellow]ais learn[/yellow]")
    console.print()

    console.print(
        "[dim]💡 提示：还可以用 ais help-all 查看所有命令详细说明[/dim]"
    )


@main.command("help-all")
def help_all():
    """显示所有命令的详细帮助汇总。"""
    console.print(
        "[bold green]🚀 AIS - AI 智能终端助手 详细帮助汇总[/bold green]"
    )
    console.print()
    console.print("[bold]核心功能命令:[/bold]")
    console.print("  ais ask --help-detail       - AI 问答功能详细说明")
    console.print("  ais suggest --help-detail   - 任务建议功能详细说明")
    console.print("  ais learn --help-detail     - 学习功能详细说明")
    console.print()
    console.print("[bold]配置管理命令:[/bold]")
    console.print("  ais config --help-context   - 配置管理详细说明")
    console.print("  ais on/off                  - 开启/关闭自动分析")
    console.print()
    console.print("[bold]历史记录命令:[/bold]")
    console.print("  ais history --help-detail   - 历史记录查看详细说明")
    console.print("  ais history-detail <索引>   - 查看具体记录详情")
    console.print()
    console.print("[bold]AI 服务商管理:[/bold]")
    console.print("  ais add-provider --help-detail    - 添加服务商详细说明")
    console.print("  ais list-provider --help-detail   - 列出服务商详细说明")
    console.print("  ais use-provider <名称>           - 切换服务商")
    console.print("  ais remove-provider <名称>        - 删除服务商")
    console.print()
    console.print("[bold]系统管理命令:[/bold]")
    console.print("  ais analyze                  - 手动分析错误")
    console.print("  ais setup-shell             - 设置 Shell 集成")
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
