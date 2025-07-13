"""AIS UI面板组件模块 - 统一的美观输出样式。"""

from typing import Union
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table


class AISPanels:
    """AIS专用的美观面板组件集合。"""

    def __init__(self, console: Console):
        self.console = console

    def ai_analysis(
        self, content: Union[str, Markdown], title: str = "🤖 AI 错误分析"
    ) -> None:
        """显示AI分析结果面板。"""
        panel = Panel(
            content,
            title=f"[bold blue]{title}[/bold blue]",
            title_align="left",
            border_style="blue",
            padding=(1, 2),
            expand=False,
        )
        self.console.print(panel)

    def suggestions(
        self, table: Table, title: str = "💡 AI 建议的解决方案"
    ) -> None:
        """显示建议命令面板。"""
        panel = Panel(
            table,
            title=f"[bold green]{title}[/bold green]",
            title_align="left",
            border_style="green",
            padding=(1, 1),
            expand=False,
        )
        self.console.print(panel)

    def success(self, message: str, title: str = "✅ 操作成功") -> None:
        """显示成功消息面板。"""
        panel = Panel(
            f"[green]{message}[/green]",
            title=f"[bold green]{title}[/bold green]",
            title_align="left",
            border_style="green",
            padding=(1, 2),
            expand=False,
        )
        self.console.print(panel)

    def warning(self, message: str, title: str = "⚠️ 警告信息") -> None:
        """显示警告消息面板。"""
        panel = Panel(
            f"[yellow]{message}[/yellow]",
            title=f"[bold yellow]{title}[/bold yellow]",
            title_align="left",
            border_style="yellow",
            padding=(1, 2),
            expand=False,
        )
        self.console.print(panel)

    def error(self, message: str, title: str = "❌ 错误信息") -> None:
        """显示错误消息面板。"""
        panel = Panel(
            f"[red]{message}[/red]",
            title=f"[bold red]{title}[/bold red]",
            title_align="left",
            border_style="red",
            padding=(1, 2),
            expand=False,
        )
        self.console.print(panel)

    def info(self, content: Union[str, Table], title: str = "ℹ️ 信息") -> None:
        """显示信息面板。"""
        panel = Panel(
            content,
            title=f"[bold cyan]{title}[/bold cyan]",
            title_align="left",
            border_style="cyan",
            padding=(1, 2),
            expand=False,
        )
        self.console.print(panel)

    def config(
        self, content: Union[str, Table], title: str = "⚙️ 配置信息"
    ) -> None:
        """显示配置信息面板。"""
        panel = Panel(
            content,
            title=f"[bold magenta]{title}[/bold magenta]",
            title_align="left",
            border_style="magenta",
            padding=(1, 2),
            expand=False,
        )
        self.console.print(panel)

    def command_result(self, command: str, success: bool = True) -> None:
        """显示命令执行结果面板。"""
        if success:
            content = (
                f"[green]🚀 命令执行成功:[/green]\n[bold]{command}[/bold]"
            )
            border_style = "green"
            title = "✅ 命令执行成功"
        else:
            content = f"[red]❌ 命令执行失败:[/red]\n[bold]{command}[/bold]"
            border_style = "red"
            title = "❌ 命令执行失败"

        panel = Panel(
            content,
            title=f"[bold]{title}[/bold]",
            title_align="left",
            border_style=border_style,
            padding=(1, 2),
            expand=False,
        )
        self.console.print(panel)

    def learning_content(
        self, content: Union[str, Markdown], topic: str
    ) -> None:
        """显示学习内容面板。"""
        panel = Panel(
            content,
            title=f"[bold blue]📚 学习内容: {topic}[/bold blue]",
            title_align="left",
            border_style="blue",
            padding=(1, 2),
            expand=False,
        )
        self.console.print(panel)


# 全局面板实例，可以直接导入使用
_console = Console()
panels = AISPanels(_console)
