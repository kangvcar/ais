"""交互式菜单模块。"""

import subprocess
import sys
from typing import List, Dict, Any
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text


def execute_command(command: str) -> bool:
    """执行命令并显示结果。"""
    try:
        print(f"\n🚀 执行命令: {command}")
        print("=" * 50)
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=False,  # 让输出直接显示给用户
            text=True
        )
        
        print("=" * 50)
        if result.returncode == 0:
            print("✅ 命令执行成功")
        else:
            print(f"❌ 命令执行失败，退出码: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False


def confirm_dangerous_command(command: str) -> bool:
    """对危险命令进行二次确认。"""
    print(f"\n⚠️  这是一个危险操作:")
    print(f"   {command}")
    print("\n⚠️  此命令可能会:")
    print("   • 删除重要文件")
    print("   • 修改系统配置")
    print("   • 造成数据丢失")
    
    while True:
        choice = input("\n❓ 你确定要执行吗？(yes/no): ").lower().strip()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print("请输入 yes 或 no")


def show_command_details(suggestion: Dict[str, Any], console: Console) -> None:
    """显示命令的详细信息。"""
    console.print("\n" + "="*60)
    console.print("[bold blue]📖 命令详细说明[/bold blue]")
    console.print("="*60)
    
    # 显示命令
    console.print(f"[bold green]命令:[/bold green] [bold]{suggestion.get('command', 'N/A')}[/bold]")
    
    # 显示风险等级
    risk_level = suggestion.get('risk_level', 'safe')
    risk_colors = {'safe': 'green', 'moderate': 'yellow', 'dangerous': 'red'}
    risk_texts = {
        'safe': '🟢 安全操作',
        'moderate': '🟡 需要谨慎',
        'dangerous': '🔴 危险操作'
    }
    
    console.print(f"[bold]风险等级:[/bold] [{risk_colors[risk_level]}]{risk_texts[risk_level]}[/{risk_colors[risk_level]}]")
    
    # 显示说明
    if suggestion.get('description'):
        console.print(f"\n[bold cyan]💡 解决方案说明:[/bold cyan]")
        console.print(suggestion['description'])
    
    # 显示技术解释
    if suggestion.get('explanation'):
        console.print(f"\n[bold magenta]🔧 技术原理:[/bold magenta]")
        console.print(suggestion['explanation'])
    
    console.print("="*60)


def ask_follow_up_question(console: Console) -> None:
    """询问后续问题。"""
    console.print("\n[bold blue]💬 后续问题[/bold blue]")
    
    question = input("请输入你的问题（按回车跳过）: ").strip()
    if not question:
        return
    
    try:
        from .ai import ask_ai
        from .config import get_config
        
        config = get_config()
        response = ask_ai(f"关于刚才的错误分析，用户有一个后续问题：{question}", config)
        
        if response:
            console.print("\n[bold green]🤖 AI 回答:[/bold green]")
            console.print(Markdown(response))
        else:
            console.print("[red]❌ 无法获取 AI 回答[/red]")
            
    except Exception as e:
        console.print(f"[red]❌ 处理问题时出错: {e}[/red]")


def edit_command(command: str) -> str:
    """让用户编辑命令。"""
    print(f"\n✏️  当前命令: {command}")
    new_command = input("请输入修改后的命令: ").strip()
    return new_command if new_command else command


def show_interactive_menu(suggestions: List[Dict[str, Any]], console: Console) -> None:
    """显示交互式建议菜单。"""
    # 检查是否在交互式终端中
    if not sys.stdin.isatty():
        show_simple_menu(suggestions, console)
        return
        
    try:
        import questionary
    except ImportError:
        # 如果 questionary 不可用，使用简化版本
        show_simple_menu(suggestions, console)
        return
    
    while True:
        # 构建菜单选项
        choices = []
        
        # 添加建议选项
        for i, suggestion in enumerate(suggestions, 1):
            command = suggestion.get('command', 'N/A')
            description = suggestion.get('description', '无描述')
            risk_level = suggestion.get('risk_level', 'safe')
            
            # 风险等级图标
            risk_icons = {
                'safe': '🟢',
                'moderate': '🟡', 
                'dangerous': '🔴'
            }
            
            choice_text = f"{risk_icons.get(risk_level, '🟢')} {i}. {description[:50]}..."
            choices.append({
                'name': choice_text,
                'value': f'execute_{i-1}'
            })
        
        # 添加其他选项
        choices.extend([
            questionary.Separator(),
            {'name': '📖 查看命令详情...', 'value': 'details'},
            {'name': '✏️  编辑命令...', 'value': 'edit'},
            {'name': '💬 询问后续问题', 'value': 'question'},
            {'name': '🚪 退出', 'value': 'exit'}
        ])
        
        # 显示菜单
        action = questionary.select(
            "请选择一个操作:",
            choices=choices,
            instruction="(使用方向键选择，回车确认)"
        ).ask()
        
        if not action or action == 'exit':
            console.print("[yellow]👋 再见！[/yellow]")
            break
            
        elif action.startswith('execute_'):
            # 执行命令
            index = int(action.split('_')[1])
            suggestion = suggestions[index]
            command = suggestion.get('command', '')
            risk_level = suggestion.get('risk_level', 'safe')
            
            # 显示命令详情
            show_command_details(suggestion, console)
            
            # 危险命令需要确认
            if risk_level == 'dangerous':
                if not confirm_dangerous_command(command):
                    console.print("[yellow]❌ 已取消执行[/yellow]")
                    continue
            
            # 执行命令
            success = execute_command(command)
            
            if success:
                console.print("\n[green]🎉 太好了！命令执行成功。你学到了新知识吗？[/green]")
            else:
                console.print("\n[yellow]🤔 命令执行失败了。要不要试试其他解决方案？[/yellow]")
            
            # 询问是否继续
            if not questionary.confirm("是否继续查看其他建议？").ask():
                break
                
        elif action == 'details':
            # 查看详情
            choices = [
                f"{i}. {sug.get('command', 'N/A')[:30]}..."
                for i, sug in enumerate(suggestions, 1)
            ]
            choices.append("返回")
            
            detail_choice = questionary.select(
                "选择要查看详情的命令:",
                choices=choices
            ).ask()
            
            if detail_choice and detail_choice != "返回":
                index = int(detail_choice.split('.')[0]) - 1
                show_command_details(suggestions[index], console)
                input("\n按回车继续...")
                
        elif action == 'edit':
            # 编辑命令
            choices = [
                f"{i}. {sug.get('command', 'N/A')}"
                for i, sug in enumerate(suggestions, 1)
            ]
            choices.append("返回")
            
            edit_choice = questionary.select(
                "选择要编辑的命令:",
                choices=choices
            ).ask()
            
            if edit_choice and edit_choice != "返回":
                index = int(edit_choice.split('.')[0]) - 1
                original_command = suggestions[index].get('command', '')
                new_command = edit_command(original_command)
                
                if new_command != original_command:
                    console.print(f"\n✅ 命令已修改为: [bold]{new_command}[/bold]")
                    
                    if questionary.confirm("是否执行修改后的命令？").ask():
                        execute_command(new_command)
                        
        elif action == 'question':
            # 询问后续问题
            ask_follow_up_question(console)


def show_simple_menu(suggestions: List[Dict[str, Any]], console: Console) -> None:
    """简化版菜单（当 questionary 不可用时）。"""
    console.print("\n[bold cyan]💡 可用的解决方案:[/bold cyan]")
    
    for i, suggestion in enumerate(suggestions, 1):
        risk_level = suggestion.get('risk_level', 'safe')
        risk_colors = {'safe': 'green', 'moderate': 'yellow', 'dangerous': 'red'}
        risk_texts = {
            'safe': '🟢 安全',
            'moderate': '🟡 谨慎',
            'dangerous': '🔴 危险'
        }
        
        console.print(f"\n{i}. [{risk_colors[risk_level]}]{risk_texts[risk_level]}[/{risk_colors[risk_level]}] {suggestion.get('description', '')}")
        console.print(f"   命令: [bold]{suggestion.get('command', '')}[/bold]")
        
        if suggestion.get('explanation'):
            console.print(f"   说明: {suggestion['explanation']}")
    
    console.print(f"\n[dim]提示: 你可以手动复制并执行上述命令，或者安装 questionary 库以获得更好的交互体验。[/dim]")