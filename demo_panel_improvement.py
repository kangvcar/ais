#!/usr/bin/env python3
"""演示AIS Panel美化效果的示例脚本。"""

from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel

console = Console()

def demo_original_output():
    """演示原始输出样式"""
    console.print("\n" + "="*60)
    console.print("[bold red]📄 原始输出样式（当前）[/bold red]")
    console.print("="*60)
    
    # 原始AI分析输出
    console.print("\n[bold blue]🤖 AI 错误分析[/bold blue]")
    console.print()
    console.print(Markdown("""
**错误分析**: chmod 999 aa.txt 命令失败是因为权限模式 999 是无效的。在 Linux/macOS 中，文件权限由三个数字组成，分别表示所有者、所属组和其他用户的读（r）、写（w）和执行（x）权限。每个数字的取值范围是 0-7。
    """))
    
    # 原始建议表格
    console.print("\n[bold blue]💡 AI 建议的解决方案:[/bold blue]")
    table = Table(show_header=True, header_style="bold blue", box=None)
    table.add_column("#", style="cyan", width=3)
    table.add_column("命令", style="bold", min_width=20)
    table.add_column("风险", justify="center", width=6)
    table.add_column("说明", style="dim")
    
    table.add_row("1", "chmod 755 aa.txt", "🟢", "使用有效的权限模式设置文件权限")
    table.add_row("2", "chmod 644 aa.txt", "🟢", "设置为只读权限")
    
    console.print(table)
    
    # 原始成功消息
    console.print("\n[green]✅ 命令执行成功！[/green]")


def demo_panel_output():
    """演示使用Panel的美化输出"""
    console.print("\n" + "="*60)
    console.print("[bold green]✨ Panel美化样式（改进后）[/bold green]") 
    console.print("="*60)
    
    # 美化的AI分析输出
    analysis_content = Markdown("""
**错误分析**: chmod 999 aa.txt 命令失败是因为权限模式 999 是无效的。在 Linux/macOS 中，文件权限由三个数字组成，分别表示所有者、所属组和其他用户的读（r）、写（w）和执行（x）权限。每个数字的取值范围是 0-7。
    """)
    
    ai_panel = Panel(
        analysis_content,
        title="[bold blue]🤖 AI 错误分析[/bold blue]",
        border_style="blue",
        padding=(1, 2),
        expand=False
    )
    console.print(ai_panel)
    
    # 美化的建议表格
    table = Table(show_header=True, header_style="bold blue", box=None)
    table.add_column("#", style="cyan", width=3)
    table.add_column("命令", style="bold", min_width=20)
    table.add_column("风险", justify="center", width=6)
    table.add_column("说明", style="dim")
    
    table.add_row("1", "chmod 755 aa.txt", "🟢", "使用有效的权限模式设置文件权限")
    table.add_row("2", "chmod 644 aa.txt", "🟢", "设置为只读权限")
    
    suggestions_panel = Panel(
        table,
        title="[bold green]💡 AI 建议的解决方案[/bold green]",
        border_style="green",
        padding=(1, 1),
        expand=False
    )
    console.print(suggestions_panel)
    
    # 美化的成功消息
    success_panel = Panel(
        "[green]🚀 命令执行成功: chmod 755 aa.txt[/green]",
        title="[bold green]✅ 操作成功[/bold green]",
        border_style="green",
        padding=(1, 2),
        expand=False
    )
    console.print(success_panel)


def demo_different_panel_types():
    """演示不同类型的Panel样式"""
    console.print("\n" + "="*60)
    console.print("[bold magenta]🎨 不同Panel类型展示[/bold magenta]")
    console.print("="*60)
    
    # 错误面板
    error_panel = Panel(
        "[red]命令未找到: xyz-command[/red]",
        title="[bold red]❌ 错误信息[/bold red]",
        border_style="red",
        padding=(1, 2),
        expand=False
    )
    console.print(error_panel)
    
    # 警告面板
    warning_panel = Panel(
        "[yellow]此操作可能会删除重要文件，请谨慎操作[/yellow]",
        title="[bold yellow]⚠️ 警告信息[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
        expand=False
    )
    console.print(warning_panel)
    
    # 配置信息面板
    config_content = """[cyan]当前配置:[/cyan]
• 默认AI服务商: OpenAI
• 自动分析: 已启用
• 上下文级别: 标准"""
    
    config_panel = Panel(
        config_content,
        title="[bold magenta]⚙️ 配置信息[/bold magenta]",
        border_style="magenta",
        padding=(1, 2),
        expand=False
    )
    console.print(config_panel)


def demo_implementation_code():
    """展示实现代码示例"""
    console.print("\n" + "="*60)
    console.print("[bold cyan]📝 实现代码示例[/bold cyan]")
    console.print("="*60)
    
    code_example = """
# 原始代码
console.print("\\n[bold blue]🤖 AI 错误分析[/bold blue]")
console.print(Markdown(analysis["explanation"]))

# 美化后代码
from ais.ui.panels import panels
panels.ai_analysis(
    Markdown(analysis["explanation"]),
    title="🤖 AI 错误分析"
)
    """
    
    implementation_panel = Panel(
        code_example.strip(),
        title="[bold cyan]🔧 代码改动示例[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
        expand=False
    )
    console.print(implementation_panel)


if __name__ == "__main__":
    console.print("[bold]🎨 AIS Panel美化效果演示[/bold]")
    
    demo_original_output()
    demo_panel_output()
    demo_different_panel_types()
    demo_implementation_code()
    
    console.print("\n[bold green]✨ 总结:[/bold green]")
    console.print("• Panel提供清晰的视觉边界，更容易区分AIS输出")
    console.print("• 不同颜色的边框表示不同类型的信息")
    console.print("• 标题栏提供上下文信息")
    console.print("• 代码改动最小，主要是包装现有输出")
    console.print("• 可以逐步迁移，不影响现有功能")