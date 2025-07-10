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
def config():
    """Show current configuration."""
    try:
        config = get_config()
        console.print("[green]Current configuration:[/green]")
        console.print(f"Provider: {config.get('default_provider', 'default_free')}")
        console.print(f"Auto analysis: {config.get('auto_analysis', True)}")
        console.print(f"Context level: {config.get('context_level', 'standard')}")
    except Exception as e:
        console.print(f"[red]Error reading config: {e}[/red]")


@main.command()
def on():
    """Enable automatic error analysis."""
    try:
        set_config("auto_analysis", True)
        console.print("[green]✓ Automatic error analysis enabled[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@main.command()
def off():
    """Disable automatic error analysis."""
    try:
        set_config("auto_analysis", False)
        console.print("[yellow]✓ Automatic error analysis disabled[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()