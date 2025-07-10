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


if __name__ == "__main__":
    main()