"""Main CLI interface for AIS."""

import click
from rich.console import Console
from rich.markdown import Markdown

from .config import get_config, set_config
from .ai import ask_ai

console = Console()


@click.group()
@click.version_option()
def main():
    """AIS - AI-powered terminal assistant."""
    pass


@main.command()
@click.argument("question", required=True)
def ask(question):
    """Ask AI a question."""
    try:
        config = get_config()
        response = ask_ai(question, config)
        
        if response:
            console.print(Markdown(response))
        else:
            console.print("[red]Failed to get AI response[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@main.command()
@click.option('--set', 'set_key', help='设置配置项 (key=value)')
@click.option('--get', 'get_key', help='获取配置项值')
@click.option('--list-providers', is_flag=True, help='列出所有可用的 AI 服务商')
def config(set_key, get_key, list_providers):
    """显示或修改配置。"""
    try:
        config = get_config()
        
        if set_key:
            # 设置配置项
            if '=' not in set_key:
                console.print("[red]格式错误，请使用 key=value 格式[/red]")
                return
            key, value = set_key.split('=', 1)
            # 简单的类型转换
            if value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
            elif value.isdigit():
                value = int(value)
            set_config(key, value)
            console.print(f"[green]✓ {key} = {value}[/green]")
            
        elif get_key:
            # 获取配置项
            value = config.get(get_key, '未设置')
            console.print(f"{get_key}: {value}")
            
        elif list_providers:
            # 列出所有提供商
            providers = config.get('providers', {})
            console.print("[green]可用的 AI 服务商:[/green]")
            for name, provider in providers.items():
                current = "✓" if name == config.get('default_provider') else " "
                console.print(f"{current} {name}: {provider.get('model_name', 'N/A')}")
            
        else:
            # 显示当前配置
            console.print("[green]当前配置:[/green]")
            console.print(f"默认提供商: {config.get('default_provider', 'default_free')}")
            console.print(f"自动分析: {config.get('auto_analysis', True)}")
            console.print(f"上下文级别: {config.get('context_level', 'standard')}")
            console.print(f"敏感目录: {len(config.get('sensitive_dirs', []))} 个")
            
    except Exception as e:
        console.print(f"[red]配置错误: {e}[/red]")


@main.command()
def on():
    """开启自动错误分析。"""
    try:
        set_config("auto_analysis", True)
        console.print("[green]✓ 自动错误分析已开启[/green]")
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")


@main.command()
def off():
    """关闭自动错误分析。"""
    try:
        set_config("auto_analysis", False)
        console.print("[yellow]✓ 自动错误分析已关闭[/yellow]")
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")


@main.command("add-provider")
@click.argument('name')
@click.option('--url', required=True, help='API 基础 URL')
@click.option('--model', required=True, help='模型名称')
@click.option('--key', help='API 密钥 (可选)')
def add_provider(name, url, model, key):
    """添加新的 AI 服务商。"""
    try:
        from .config import add_provider as add_provider_config
        add_provider_config(name, url, model, key)
        console.print(f"[green]✓ 已添加提供商: {name}[/green]")
    except Exception as e:
        console.print(f"[red]添加提供商失败: {e}[/red]")


@main.command("remove-provider")
@click.argument('name')
def remove_provider(name):
    """删除 AI 服务商。"""
    try:
        from .config import remove_provider as remove_provider_config
        remove_provider_config(name)
        console.print(f"[green]✓ 已删除提供商: {name}[/green]")
    except Exception as e:
        console.print(f"[red]删除提供商失败: {e}[/red]")


@main.command("use-provider")
@click.argument('name')
def use_provider(name):
    """切换默认 AI 服务商。"""
    try:
        from .config import use_provider as use_provider_config
        use_provider_config(name)
        console.print(f"[green]✓ 已切换到提供商: {name}[/green]")
    except Exception as e:
        console.print(f"[red]切换提供商失败: {e}[/red]")


@main.command("list-provider")
def list_provider():
    """列出所有可用的 AI 服务商。"""
    try:
        config = get_config()
        providers = config.get('providers', {})
        
        if not providers:
            console.print("[yellow]没有配置任何 AI 服务商[/yellow]")
            return
            
        console.print("[green]可用的 AI 服务商:[/green]")
        for name, provider in providers.items():
            # 显示当前使用的提供商
            current = "✓" if name == config.get('default_provider') else " "
            model = provider.get('model_name', 'N/A')
            url = provider.get('base_url', 'N/A')
            has_key = "🔑" if provider.get('api_key') else "  "
            
            console.print(f"{current} {name}: {model} ({url}) {has_key}")
            
    except Exception as e:
        console.print(f"[red]列出提供商失败: {e}[/red]")


@main.command("analyze")
@click.option('--exit-code', type=int, required=True, help='命令退出码')
@click.option('--command', required=True, help='失败的命令')
@click.option('--stderr', default='', help='错误输出')
def analyze_error(exit_code, command, stderr):
    """分析命令错误。"""
    try:
        from .context import collect_context
        from .ai import analyze_error
        from .database import save_command_log
        import os
        
        # 收集上下文信息
        context = collect_context(command, exit_code, stderr)
        
        # 获取配置
        config = get_config()
        
        # 检查是否有相似的历史错误
        from .database import get_similar_commands
        similar_logs = get_similar_commands(command, 3)
        
        if similar_logs:
            console.print("\n[bold yellow]🔍 发现相似的历史错误[/bold yellow]")
            for i, log in enumerate(similar_logs, 1):
                time_str = log.timestamp.strftime("%m-%d %H:%M")
                status = "已解决" if log.ai_explanation else "未分析"
                console.print(f"  {i}. {log.original_command} ({time_str}) - {status}")
            
            console.print("[dim]💡 你可以使用 'ais history-detail <索引>' 查看之前的分析[/dim]")
        
        # 使用 AI 分析错误
        analysis = analyze_error(command, exit_code, stderr, context, config)
        
        # 保存到数据库
        username = os.getenv('USER', 'unknown')
        save_command_log(
            username=username,
            command=command,
            exit_code=exit_code,
            stderr=stderr,
            context=context,
            ai_explanation=analysis.get('explanation', ''),
            ai_suggestions=analysis.get('suggestions', [])
        )
        
        # 显示分析结果
        if analysis.get('explanation'):
            console.print("\n[bold blue]🤖 AI 错误分析[/bold blue]")
            console.print()
            console.print(Markdown(analysis['explanation']))
        
        suggestions = analysis.get('suggestions', [])
        if suggestions:
            # 显示交互式菜单
            from .interactive import show_interactive_menu
            show_interactive_menu(suggestions, console)
        
    except Exception as e:
        console.print(f"[red]分析失败: {e}[/red]")


@main.command("history")
@click.option('--limit', '-n', default=10, help='显示的历史记录数量')
@click.option('--failed-only', is_flag=True, help='只显示失败的命令')
@click.option('--command-filter', help='按命令名称过滤')
def show_history(limit, failed_only, command_filter):
    """显示命令历史记录。"""
    try:
        from .database import get_recent_logs, get_similar_commands
        from rich.table import Table
        from rich.text import Text
        import json
        
        console.print(f"\n[bold blue]📚 最近的命令历史[/bold blue]")
        
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
        console.print(f"\n[dim]💡 使用 'ais history-detail <索引>' 查看详细分析[/dim]")
        
    except Exception as e:
        console.print(f"[red]获取历史记录失败: {e}[/red]")


@main.command("history-detail")
@click.argument('index', type=int)
def show_history_detail(index):
    """显示历史命令的详细分析。"""
    try:
        from .database import get_recent_logs
        import json
        
        logs = get_recent_logs(50)  # 获取更多记录用于索引
        
        if index < 1 or index > len(logs):
            console.print(f"[red]索引超出范围。请使用 1-{len(logs)} 之间的数字[/red]")
            return
        
        log = logs[index - 1]
        
        console.print(f"\n[bold blue]📖 命令详细信息[/bold blue]")
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
                console.print(f"\n[bold cyan]📋 执行上下文:[/bold cyan]")
                console.print(f"工作目录: {context.get('cwd', 'N/A')}")
                if context.get('git_branch'):
                    console.print(f"Git 分支: {context.get('git_branch')}")
            except:
                pass
        
        # AI 分析
        if log.ai_explanation:
            console.print(f"\n[bold green]🤖 AI 分析:[/bold green]")
            console.print(Markdown(log.ai_explanation))
        
        # AI 建议
        if log.ai_suggestions_json:
            try:
                suggestions = json.loads(log.ai_suggestions_json)
                console.print(f"\n[bold yellow]💡 AI 建议:[/bold yellow]")
                for i, suggestion in enumerate(suggestions, 1):
                    risk_icon = '✅' if suggestion.get('risk_level') == 'safe' else '⚠️'
                    console.print(f"{i}. {suggestion.get('command', 'N/A')} {risk_icon}")
                    console.print(f"   {suggestion.get('description', '')}")
            except:
                pass
        
        console.print("=" * 60)
        
    except Exception as e:
        console.print(f"[red]获取详细信息失败: {e}[/red]")


@main.command("suggest")
@click.argument('task')
def suggest_command(task):
    """根据任务描述建议命令。"""
    try:
        from .ai import ask_ai
        
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
@click.argument('topic', required=False)
def learn_command(topic):
    """学习命令行知识。"""
    try:
        from .ai import ask_ai
        
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
                "network - 网络工具和诊断"
            ]
            
            for i, topic in enumerate(topics, 1):
                console.print(f"  {i}. {topic}")
            
            console.print(f"\n[dim]使用 'ais learn <主题>' 开始学习，例如: ais learn git[/dim]")
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
            console.print(f"\n[bold blue]📖 {topic.upper()} 学习指南[/bold blue]")
            console.print()
            console.print(Markdown(response))
        else:
            console.print("[red]无法获取学习内容，请检查网络连接[/red]")
            
    except Exception as e:
        console.print(f"[red]学习功能出错: {e}[/red]")


if __name__ == "__main__":
    main()