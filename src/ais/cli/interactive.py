"""交互式菜单模块。"""

import subprocess
import sys
from typing import List, Dict, Any
from rich.console import Console
from rich.markdown import Markdown


def execute_command(command: str) -> bool:
    """执行命令并显示结果。"""
    try:
        print(f"\n🚀 执行命令: {command}")
        print("=" * 50)

        result = subprocess.run(
            command,
            shell=True,
            capture_output=False,
            text=True,  # 让输出直接显示给用户
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
    print("\n⚠️  这是一个危险操作:")
    print(f"   {command}")
    print("\n⚠️  此命令可能会:")
    print("   • 删除重要文件")
    print("   • 修改系统配置")
    print("   • 造成数据丢失")

    while True:
        choice = input("\n❓ 你确定要执行吗？(yes/no): ").lower().strip()
        if choice in ["yes", "y"]:
            return True
        elif choice in ["no", "n"]:
            return False
        else:
            print("请输入 yes 或 no")


def show_command_details(suggestion: Dict[str, Any], console: Console) -> None:
    """显示命令的详细信息。"""
    separator = "=" * 60
    console.print(f"\n{separator}")
    console.print("[bold blue]📖 命令详细说明[/bold blue]")
    console.print(separator)

    # 显示命令
    console.print(
        f"[bold green]命令:[/bold green] "
        f"[bold]{suggestion.get('command', 'N/A')}[/bold]"
    )

    # 显示风险等级
    risk_level = suggestion.get("risk_level", "safe")
    risk_info = {
        "safe": ("green", "🟢 安全操作"),
        "moderate": ("yellow", "🟡 需要谨慎"),
        "dangerous": ("red", "🔴 危险操作"),
    }

    color, text = risk_info[risk_level]
    console.print(f"[bold]风险等级:[/bold] [{color}]{text}[/{color}]")

    # 显示说明和解释
    for field, title in [
        ("description", "💡 解决方案说明"),
        ("explanation", "🔧 技术原理"),
    ]:
        if suggestion.get(field):
            console.print(f"\n[bold cyan]{title}:[/bold cyan]")
            console.print(suggestion[field])

    console.print(separator)


def ask_follow_up_question(
    console: Console, predefined_questions: List[str] = None
) -> None:
    """询问后续问题，支持预设问题选择。"""
    console.print("\n[bold blue]💬 后续问题[/bold blue]")

    # 如果有预设问题，先显示选项
    if predefined_questions:
        console.print("\n[bold cyan]AI 建议的学习问题:[/bold cyan]")
        for i, q in enumerate(predefined_questions, 1):
            console.print(f"  {i}. {q}")
        console.print(f"  {len(predefined_questions) + 1}. 自定义问题")

        try:
            choice = input(
                f"\n请选择问题 (1-{len(predefined_questions) + 1}, 或回车跳过): "
            ).strip()
            if not choice:
                return

            choice_num = int(choice)
            if 1 <= choice_num <= len(predefined_questions):
                question = predefined_questions[choice_num - 1]
            elif choice_num == len(predefined_questions) + 1:
                question = input("请输入你的问题: ").strip()
                if not question:
                    return
            else:
                console.print("[yellow]无效选择[/yellow]")
                return
        except ValueError:
            console.print("[yellow]无效输入[/yellow]")
            return
    else:
        question = input("请输入你的问题（按回车跳过）: ").strip()
        if not question:
            return

    try:
        from ..core.ai import ask_ai
        from ..core.config import get_config

        config = get_config()
        response = ask_ai(
            f"关于刚才的错误分析，用户有一个后续问题：{question}", config
        )

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


def show_interactive_menu(
    suggestions: List[Dict[str, Any]],
    console: Console,
    follow_up_questions: List[str] = None,
) -> None:
    """显示交互式建议菜单。"""
    # 检查是否在交互式终端中
    if not sys.stdin.isatty():
        show_simple_menu(suggestions, console, follow_up_questions)
        return

    try:
        import questionary
    except ImportError:
        # 如果 questionary 不可用，使用简化版本
        show_simple_menu(suggestions, console, follow_up_questions)
        return

    while True:
        # 构建菜单选项
        choices = []

        # 添加建议选项
        for i, suggestion in enumerate(suggestions, 1):
            command = suggestion.get("command", "N/A")
            description = suggestion.get("description", "无描述")
            risk_level = suggestion.get("risk_level", "safe")

            # 风险等级图标 - 按用户要求的格式
            risk_icon = "✅" if risk_level == "safe" else "⚠️"

            # 格式化选项文本：编号. 命令名称    风险图标 (描述)
            choice_text = f"{i}. {command:<25} {risk_icon} ({description})"
            choices.append({"name": choice_text, "value": f"execute_{i-1}"})

        # 添加分割线
        separator_line = "-" * 75
        choices.append(questionary.Separator(separator_line))

        # 添加固定选项 - 继续编号
        next_num = len(suggestions) + 1
        choices.extend(
            [
                {"name": f"{next_num}. Edit a command...", "value": "edit"},
                {
                    "name": f"{next_num + 1}. Ask follow-up question",
                    "value": "question",
                },
                {"name": f"{next_num + 2}. Exit", "value": "exit"},
            ]
        )

        # 显示菜单
        action = questionary.select(
            "Select an action:",
            choices=choices,
            instruction="",
            use_shortcuts=True,
        ).ask()

        if not action or action == "exit":
            console.print("[yellow]👋 再见！[/yellow]")
            break

        elif action.startswith("execute_"):
            # 执行命令
            index = int(action.split("_")[1])
            suggestion = suggestions[index]
            command = suggestion.get("command", "")
            risk_level = suggestion.get("risk_level", "safe")

            # 显示命令详情
            show_command_details(suggestion, console)

            # 危险命令需要确认
            if risk_level == "dangerous":
                if not confirm_dangerous_command(command):
                    console.print("[yellow]❌ 已取消执行[/yellow]")
                    continue

            # 执行命令
            success = execute_command(command)

            if success:
                console.print(
                    "\n[green]🎉 太好了！命令执行成功。你学到了新知识吗？[/green]"
                )
            else:
                console.print(
                    "\n[yellow]🤔 命令执行失败了。要不要试试其他解决方案？[/yellow]"
                )

            # 询问是否继续
            if not questionary.confirm("是否继续查看其他建议？").ask():
                break

        elif action == "details":
            # 查看详情
            choices = [
                f"{i}. {sug.get('command', 'N/A')[:30]}..."
                for i, sug in enumerate(suggestions, 1)
            ]
            choices.append("返回")

            detail_choice = questionary.select(
                "选择要查看详情的命令:", choices=choices
            ).ask()

            if detail_choice and detail_choice != "返回":
                index = int(detail_choice.split(".")[0]) - 1
                show_command_details(suggestions[index], console)
                input("\n按回车继续...")

        elif action == "edit":
            # 编辑命令
            choices = [
                f"{i}. {sug.get('command', 'N/A')}"
                for i, sug in enumerate(suggestions, 1)
            ]
            choices.append("返回")

            edit_choice = questionary.select(
                "选择要编辑的命令:", choices=choices
            ).ask()

            if edit_choice and edit_choice != "返回":
                index = int(edit_choice.split(".")[0]) - 1
                original_command = suggestions[index].get("command", "")
                new_command = edit_command(original_command)

                if new_command != original_command:
                    console.print(
                        f"\n✅ 命令已修改为: [bold]{new_command}[/bold]"
                    )

                    if questionary.confirm("是否执行修改后的命令？").ask():
                        execute_command(new_command)

        elif action == "question":
            # 询问后续问题
            ask_follow_up_question(console, follow_up_questions)


def show_simple_menu(
    suggestions: List[Dict[str, Any]],
    console: Console,
    follow_up_questions: List[str] = None,
) -> None:
    """简化版菜单（当 questionary 不可用时）。"""
    console.print()
    console.print("? Select an action:")

    for i, suggestion in enumerate(suggestions, 1):
        command = suggestion.get("command", "N/A")
        description = suggestion.get("description", "无描述")
        risk_level = suggestion.get("risk_level", "safe")

        # 风险等级图标
        risk_icon = "✅" if risk_level == "safe" else "⚠️"
        prefix = "  ▸ " if i == 1 else "    "

        console.print(
            f"{prefix}{i}. {command:<25} {risk_icon} ({description})"
        )

        if suggestion.get("explanation"):
            console.print(
                f"       [dim]说明: {suggestion['explanation']}[/dim]"
            )

    # 添加固定选项
    separator = "    " + "-" * 75
    console.print(separator)

    next_num = len(suggestions) + 1
    fixed_options = [
        f"{next_num}. Edit a command...",
        f"{next_num + 1}. Ask follow-up question",
        f"{next_num + 2}. Exit",
    ]

    for option in fixed_options:
        console.print(f"    {option}")

    console.print(
        "\n[dim]提示: 你可以手动复制并执行上述命令，或者在交互式终端中获得更好的体验。[/dim]"
    )
